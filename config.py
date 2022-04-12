from os import environ
import dotenv

dotenv.load_dotenv()

cfg = {}
cfg["secret_key"] = environ["secret_key"]
cfg["DATABASE_URL"] = environ["DATABASE_URL"]
cfg["PORT"] = environ["PORT"]
