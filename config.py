# import json

# with open("config.json", "r", encoding="utf8") as json_file:
#     cfg = json.load(json_file)
import os
import dotenv

dotenv.load_dotenv()

cfg = {}
cfg["secret_key"] = os.environ["secret_key"]
cfg["DATABASE_URL"] = os.environ["DATABASE_URL"]
