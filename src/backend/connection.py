from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()


USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
IP = os.getenv("MYSQL_IP") # Default should be Localhost.
DATABASE = os.getenv("MYSQL_DATABASE")



engine = create_engine(
    f'mysql+mysqlconnector://{USER}:{PASSWORD}@{IP}/{DATABASE}'
)


