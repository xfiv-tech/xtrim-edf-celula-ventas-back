from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
database = os.getenv("database")

DATABASE_CONNECTION_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}'
print(DATABASE_CONNECTION_URI)

engine = create_engine(DATABASE_CONNECTION_URI, echo=True)


meta = MetaData()

db = engine.connect()