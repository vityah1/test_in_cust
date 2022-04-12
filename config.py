# import json

# with open("config.json", "r", encoding="utf8") as json_file:
#     cfg = json.load(json_file)
import os
import dotenv

dotenv.load_dotenv()

cfg = {}
# cfg["db_host"] = os.environ["db_host"]
# cfg["db_user"] = os.environ["db_user"]
# cfg["db_passwd"] = os.environ["db_passwd"]
# cfg["db_db"] = os.environ["db_db"]
cfg["secret_key"] = os.environ["secret_key"]
cfg["DATABASE_URL"] = os.environ["DATABASE_URL"]
