flask api-rest boilerplate with auth and migration 0.0.1

Small and compact back-end rest-api written on flask with jwt auth.  

Instalation:
## Requirements
This is not ideal code but this is simple solution and practise for use flask, jwt tehnologies

## Instalation:
```cmd
python -m venv venv
venv\scripts\activate
pip3 install -r requirements.txt
```
## Configuration and setting
Create and edit .env file with next vars:

```.env
db_host=your db host
db_user = your db user
db_passwd = your db password
db_db = your db
secret_key = your super secret key
```

## Create database tables
Execute commands:
```cmd
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

## Swagger UI
http://127.0.0.1:5000/apidocs/
## Local run
if you run it localy
```cmd
python app.app 
```

## Deploy on virtual apache shared hosting
edit .htaccess file according to your paths

## Deploy on Heroku
- SigUp you account
- create app `name your app`
- download heroku CLI
- excecute:
```cmd
heroku login
heroku git:clone -a `name your app`
git push heroku master 
```

