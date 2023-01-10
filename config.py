from dotenv import load_dotenv
import os

load_dotenv()

user = "root"
password = "root"
host = "localhost"
database = "database"

DATABASE_CONNECTION_URI = f'mysql://{user}:{password}@{host}/{database}'
print(DATABASE_CONNECTION_URI)