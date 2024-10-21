# import os
# from dotenv import load_dotenv

# load_dotenv()

# MONGODB_URL = os.getenv("MONGODB_URL")
# MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "profitsniffer")

# class Config:
#     MONGODB_URL = MONGODB_URL
#     MONGODB_DB_NAME = MONGODB_DB_NAME
#     TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
#     FRONTEND_URL = os.getenv("FRONTEND_URL")
#     SCRAPER_URL = os.getenv("SCRAPER_URL", "http://host.docker.internal:3000/cf-clearance-scraper")

# config = Config()
import os

class Config:
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "profitsniffer")
    MONGODB_URL = os.getenv("MONGODB_URL")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://elegant-duckanoo-d8e6c0.netlify.app")
    SCRAPER_URL = os.getenv("SCRAPER_URL", "https://cfclearance-231e275bd969.herokuapp.com/cf-clearance-scraper")
    BACKEND_URL = os.getenv("BACKEND_URL", "https://your-heroku-app-name.herokuapp.com")

config = Config()
