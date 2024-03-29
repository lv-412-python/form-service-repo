# 4m-form-service  [![Build Status](https://travis-ci.org/lv-412-python/form-service-repo.svg?branch=develop)](https://travis-ci.org/lv-412-python/form-service-repo)

## Description
This is the source code of the Form service which allows you create surveys with some title and some amount of different fields to fill. This app provides flexible and easy to use form-constructor.

## Technologies
* Python (3.6.8)
* PostgreSQL (11.4)
* Flask (1.0.3)
* Docker (18.09.7)

## ER diagram
![alt_text](diagrams/4m_forms.png)

## Install
For the next steps of service installation, you will need setup of Ubuntu 18.04 OS

### Install
For the next steps of service installation, you will need setup of Docker

### In the project root dockerize service:

```
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
sudo start.sh
flask db upgrade
```

OR

### Install and configure PostgreSQL server on your local machine:
```
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql postgres

postgres=# \password
Enter new password:
Enter it again:

postgres=# CREATE DATABASE your_custom_db_name;

postgres=# \q
```

Go to the folder with setup.py and create needed models with these commands:
```
python
>>> from form_service.db import DB
>>> from form_service.models.form import Form
>>> DB.create_all()
>>> DB.session.commit()
```
Now fill your database with some data:
```
>>> form1 = Form(title='Test', description='testing', owner=1)
>>> DB.session.add(form1)
>>> DB.session.commit()
>>> exit()
```

## Run Project
### In the project root create venv and install requirements with Make
```
export PYTHONPATH=$PYTHONPATH:/home/.../.../form-service-repo/form_service
```
### Flask
Go to the folder with setup.py file, run the server by command:
#### To run in development mode:
```
make run-dev
```
#### To run in production mode:
```
make run-prod
```
#### In case of failure:
```
. venv/bin/activate
pip install -r requirements.txt
```

## Run Unittests
Go to the folder with setup.py file, run all the tests by command:
```
python -m unittest
```

# Developer info:
  * Lv-412.WebUI/Python team:
    - @sikyrynskiy
    - @olya_petryshyn
    - @taraskonchak
    - @OlyaKh00
    - @ement06
    - @iPavliv
    - @Anastasia_Siromska
    - @Romichh
