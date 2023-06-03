import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')  # API TOKEN TELEGRAM BOT
ADMIN = [int(item) for item in os.getenv('ADMIN').split()]

# DATABASE
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')