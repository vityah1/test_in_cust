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
Create .env file with next content:

```.env
DATABASE_URL = your database url
secret_key = your super secret key
```
## Create database tables
Execute commands:
```cmd
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
## Local run
if you run it localy
```cmd
python app.app 
```
## Deploy on virtual apache shared hosting
edit **.htaccess** file according to your paths
edit in **main.py** file path to your venv
## Deploy on Heroku
- SigUp you account on heroku.com
- create app `name your app`
- download heroku CLI
- excecute:
```cmd
heroku login
heroku git:clone -a `name your app`
git push heroku master 
```
### Add next env vars:
 - secret key = your super secret key
 - PORT = 5000
### For work with external mysql database
- DB_DATABASE_URL = your database url

## Swagger UI
http://127.0.0.1:5000/apidocs/
