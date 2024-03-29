"""Form view implementation."""  # pylint: disable=cyclic-import
from flask import request, Response, jsonify
from flask_api import status
from flask_restful import Resource, HTTPException
from marshmallow import ValidationError, fields
from sqlalchemy.exc import IntegrityError
from webargs.flaskparser import parser

from form_service import API
from form_service import APP
from form_service.db import DB
from form_service.models.form import Form
from form_service.serializers.form_schema import FORM_SCHEMA, FORMS_SCHEMA


def check_authority(view):
    """Decorator for resources."""
    def func_wrapper(*args, **kwargs):
        """Wrapper."""
        if request.cookies['admin'] == 'False' and request.method != 'GET':
            return {"error": "Forbidden."}, status.HTTP_403_FORBIDDEN
        return view(*args, **kwargs)
    return func_wrapper


class FormResource(Resource):
    """Class FormView implementation."""
    @check_authority
    def get(self, form_id=None):
        """
        Get method for Form Service.
        :return: requested forms with status code or error message with status code.
        """
        if form_id:
            output = Form.query.get(form_id)
            result = FORM_SCHEMA.dump(output).data
        else:
            url_args = {
                'owner': fields.List(fields.Int(validate=lambda value: value > 0)),
                'form_id': fields.List(fields.Int(validate=lambda value: value > 0))
            }
            try:
                args = parser.parse(url_args, request)
            except HTTPException as err:
                APP.logger.error(err.args)
                return {'error': 'Invalid URL.'}, status.HTTP_400_BAD_REQUEST
            if 'owner' in args:
                output = Form.query.filter(Form.owner.in_(args['owner']))
            if 'form_id' in args:
                output = Form.query.filter(Form.form_id.in_(args['form_id']))
            result = FORMS_SCHEMA.dump(output).data
        if result:
            resp = jsonify(result)
            resp.status_code = status.HTTP_200_OK

        return resp if result else ({'error': 'Does not exist.'}, status.HTTP_404_NOT_FOUND)

    @check_authority
    def delete(self, form_id):
        """
        Delete method for the form.
        :return: Response object or error message with status code.
        """
        form_to_delete = Form.query.get(form_id)
        if not form_to_delete:
            APP.logger.error('Form with id {} does not exist.'.format(form_id))
            return {'error': 'Does not exist.'}, status.HTTP_404_NOT_FOUND

        DB.session.delete(form_to_delete)
        DB.session.commit()
        return Response(status=status.HTTP_200_OK)

    @check_authority
    def put(self, form_id):
        """
        Put method for the form.
        :return: Response object or error message with status code.
        """
        updated_form = Form.query.get(form_id)
        if not updated_form:
            return {'error': 'Does not exist.'}, status.HTTP_404_NOT_FOUND
        try:
            updated_data = FORM_SCHEMA.load(request.json).data
        except ValidationError as err:
            APP.logger.error(err.args)
            return err.messages, status.HTTP_400_BAD_REQUEST

        for key, value in updated_data.items():
            setattr(updated_form, key, value)
        DB.session.commit()
        return Response(status=status.HTTP_200_OK)

    @check_authority
    def post(self):
        """
        Post method for creating a new form.
        :return: Response object or error message with status code.
        """
        try:
            new_form = FORM_SCHEMA.load(request.json).data
        except ValidationError as err:
            APP.logger.error(err.args)
            return err.messages, status.HTTP_400_BAD_REQUEST

        add_new_form = Form(**new_form)
        DB.session.add(add_new_form)

        try:
            DB.session.commit()
        except IntegrityError as err:
            APP.logger.error(err.args)
            DB.session.rollback()
            return {'error': 'Already exists.'}, status.HTTP_400_BAD_REQUEST
        return Response(status=status.HTTP_201_CREATED)


API.add_resource(FormResource, '/form/<int:form_id>', '/form')
