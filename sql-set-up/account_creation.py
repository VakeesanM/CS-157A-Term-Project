from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher
load_dotenv()


USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
IP = os.getenv("MYSQL_IP") # Default should be Localhost.
DATABASE = os.getenv("MYSQL_DATABASE")



engine = create_engine(
    f'mysql+mysqlconnector://{USER}:{PASSWORD}@{IP}/{DATABASE}'
)


hasher = PasswordHasher()
students = { 
    "emma.johnson@school.edu": "Maple#2041",
    "liam.smith@school.edu": "River$5532",
    "olivia.garcia@school.edu": "Sunset!7718",
    "noah.martinez@school.edu": "Falcon&3094",
    "ava.brown@school.edu": "Cedar%6627",
    "ethan.davis@school.edu": "Harbor@1859",
    "sophia.lopez@school.edu": "Tulip*4476",
    "mason.wilson@school.edu": "Granite#9203",
    "isabella.clark@school.edu": "Meadow$8365",
    "lucas.young@school.edu": "Comet!5981",
    'justin.young@school.edu': 'somethinghere',
    'preston.smit@school.edu': 'somethingelsehereinstead'

}  # Fake accounts

def create_account(email, password, role='Student'):
    password_hash = hasher.hash(password)
    statement = text('INSERT INTO accounts (Email, PasswordHash, Role) Values (:email, :password_hash, :role)')

    with engine.connect() as conn:
        conn.execute(statement, {'email':email, 'password_hash':password_hash, 'role':role})
        conn.commit()


for email in students:
   create_account(email, students[email])


admins = {'vakeesan.moorthy@school.edu': "VMpass", 'esha.hooda@schooledu': "EHpass", 'tahereh.arabghalizi@school.edu': 'TApass'}

for admin in admins:
    create_account(admin, admins[admin], "Admin")