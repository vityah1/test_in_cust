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
Create and edit simple txt finman_config.json file with next structure:

```json
{
"db_host": "your_db_host",
"db_user": "db_user",
"db_passwd": "db_password",
"db_db": "db_name",
"secret_key": "your_super_secret_key_for_jwt_auth",
}
```

## Create database tables
3. Execute commands:
```cmd
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

## Local run
4. python app.app if you run it localy

## Virtual apache shared hosting
5. edit .htaccess file according to your paths



