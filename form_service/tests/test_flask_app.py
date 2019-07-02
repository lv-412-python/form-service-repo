"""Tests for form service."""
from unittest import main
from flask_testing import TestCase
from form_service import APP
from form_service.db import DB
from form_service.models.form import Form
from form_service.config.test_config import TestConfiguration


def create_app(config_obj):
    """
    Creates Flask app with configuration, you need.
    :param config_obj: name of configuration.
    :return: flask app.
    """
    app = APP
    app.config.from_object(config_obj)
    return app


class AllFormsTest(TestCase):
    """Tests for get resource."""
    def create_app(self):
        """
        Creates Flask app with Test Configuration.
        :return: flask app.
        """
        return create_app(TestConfiguration)

    def setUp(self):
        """Creates tables and puts objects into database."""
        DB.create_all()
        form1 = Form(title="Test", description="testing.", owner=2)
        form2 = Form(title="Another test", description="new one", owner=2)
        DB.session.add(form1)
        DB.session.add(form2)
        DB.session.commit()
        id1 = Form.query.filter_by(title="Test", description="testing.",
                                   owner=2).first()
        self.owner_id = id1.owner
        self.forms_id_1 = id1.form_id
        id2 = Form.query.filter_by(title="Another test", description="new one",
                                   owner=2).first()
        self.forms_id_2 = id2.form_id

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()

    def test_get(self):
        """Tests get resource."""
        with self.create_app().test_client() as client:
            response = client.get('/forms/{}'.format(self.owner_id))
            check = [{
                "title": "Test",
                "description": "testing.",
                "owner": self.owner_id,
                "form_id": self.forms_id_1
            }, {
                "title": "Another test",
                "description": "new one",
                "owner": self.owner_id,
                "form_id": self.forms_id_2
            }]
            self.assertEqual(response.json, check)

    def test_get_no_owner(self):
        """Tests get resource."""
        with self.create_app().test_client() as client:
            response = client.get('/forms/123464367')
            self.assertEqual(response.json, {'message': 'Forms by this user could not be found.'})


class SingleFormTest(TestCase):
    """Tests for get, put, delete resources."""
    def create_app(self):
        """
        Creates Flask app with Test Configuration.
        :return: flask app.
        """
        return create_app(TestConfiguration)

    def setUp(self):
        """Creates tables and puts objects into database."""
        DB.create_all()
        form = Form(title="Test", description="testing.", owner=2)
        DB.session.add(form)
        DB.session.commit()
        form = Form.query.filter_by(title="Test", description="testing.",
                                    owner=2).first()
        self.forms_id = form.form_id

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()

    def test_get(self):
        """Tests get resource."""
        with self.create_app().test_client() as client:
            response = client.get('/form/{}'.format(self.forms_id))
            check = [{
                "title": "Test",
                "description": "testing.",
                "owner": 2,
                "form_id": self.forms_id
            }]
            self.assertEqual(response.json, check)

    def test_get_no_form(self):
        """Tests get resource."""
        with self.create_app().test_client() as client:
            response = client.get('/form/17457930')
            self.assertEqual(response.json, {'message': 'Form with this id could not be found.'})

    def test_put(self):
        """Tests put resource."""
        with self.create_app().test_client() as client:
            new = {
                "title": "Test",
                "description": "testing.",
                "owner": 2
            }
            client.put('/form/{}'.format(self.forms_id), json=new)
            form = Form.query.filter_by(form_id=self.forms_id).first()
            self.assertEqual(form.owner, 2)

    def test_delete(self):
        """Tests delete resource."""
        with self.create_app().test_client() as client:
            response = client.delete('/form/{}'.format(self.forms_id))
            form = Form.query.filter_by(form_id=self.forms_id).first()
            self.assertEqual(form, None)
            self.assertEqual(response.status_code, 200)

    def test_delete_no_id(self):
        """Tests delete resource."""
        with self.create_app().test_client() as client:
            response = client.delete('/form/167057395')
            self.assertEqual(response.status_code, 400)


class PostTest(TestCase):
    """Tests for post resource."""
    def create_app(self):
        """
        Creates Flask app with Test Configuration.
        :return: flask app.
        """
        return create_app(TestConfiguration)

    def setUp(self):
        """Creates tables."""
        DB.create_all()

    def test_post_success(self):
        """Tests post resource success."""
        with self.create_app().test_client() as client:
            response = client.post('/form/new',
                                   json={"title": "Test", "description": "testing.",
                                         "owner": 2})
            self.assertEqual(response.status_code, 200)

    def test_post_failure(self):
        """Tests post resource failure."""
        with self.create_app().test_client() as client:
            client.post('/form/new', json={"title": "Test", "description": "testing.",
                                           "owner": 2})
            response = client.post('/form/new',
                                   json={"title": "Test", "description": "testing.",
                                         "owner": 2})
            self.assertEqual(response.status_code, 400)

    def tearDown(self):
        """Drops all tables."""
        DB.session.remove()
        DB.drop_all()


if __name__ == '__main__':
    main()