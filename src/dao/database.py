from cs50 import SQL
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv('DB')
db = SQL(DB_URL)

