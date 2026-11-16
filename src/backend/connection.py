from mysql.connector import connect
from dotenv import load_dotenv
import os
load_dotenv()


USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
IP = os.getenv("MYSQL_IP") # Default should be Localhost.
DATABASE = os.getenv("MYSQL_DATABASE")


def create_connection():
    return connect(host=IP, user=USER, password=PASSWORD, database=DATABASE)


