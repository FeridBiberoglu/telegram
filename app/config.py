import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://feridbiberoglu88:Amsterdam1@profitsniffer.vxoqb.mongodb.net/")
MONGODB_DB_NAME = "profitsniffer"

class Config:
    MONGODB_URL = MONGODB_URL
    MONGODB_DB_NAME = MONGODB_DB_NAME
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    SCRAPER_URL = os.getenv("SCRAPER_URL", "http://host.docker.internal:3000/cf-clearance-scraper")

config = Config()
