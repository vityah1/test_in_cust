from os import environ
import dotenv

dotenv.load_dotenv()

cfg = {}
cfg["secret_key"] = environ["secret_key"]
# external mysql db
# cfg["DATABASE_URL"] = environ["DATABASE_URL"]
# heroku pg db
cfg["DATABASE_URL"] = environ["HEROKU_POSTGRESQL_MAUVE_URL"]
cfg["PORT"] = environ["PORT"]
