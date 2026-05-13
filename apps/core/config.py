import os

from dotenv import load_dotenv

load_dotenv()

# 예: postgresql+psycopg://user:password@localhost:5432/dbname
DATABASE_URL = os.getenv("DATABASE_URL")
