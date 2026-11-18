from mysql.connector import connect
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher
load_dotenv()


USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
IP = os.getenv("MYSQL_IP") # Default should be Localhost.
DATABASE = os.getenv("MYSQL_DATABASE")
PORT = int(os.getenv("MYSQL_PORT"))


def read_sql_file(path):
    """Read a .sql file and return its statements, skipping '--' comment lines."""
    with open(path, "r", encoding="utf-8") as file:
        lines = [line for line in file if not line.strip().startswith("--")]
    queries = "".join(lines).split(';')
    cleaned = []
    for query in queries:
        query = " ".join(query.split())  # collapse newlines/tabs/extra spaces
        if query:
            cleaned.append(query)
    return cleaned


# Step 1: create the database and tables
conn = connect(host=IP, user=USER, password=PASSWORD, port=PORT)
cursor = conn.cursor()

for query in read_sql_file("sql-set-up/intalize.sql"):
    print(query)
    cursor.execute(query)
    conn.commit()

cursor.close()
conn.close()

conn = connect(host=IP, user=USER, password=PASSWORD, database=DATABASE, port=PORT)
cursor = conn.cursor()

# Step 2: Account Creation Script
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
    'preston.smit@school.edu': 'somethingelsehereinstead',
    'harper.lee@school.edu': 'Willow#3317',
    'jacob.nguyen@school.edu': 'Canyon$7740',
    'mia.patel@school.edu': 'Lotus!2259'

}  # Fake accounts (15 students so every table has at least 15 rows)

def create_account(email, password, role='Student'):
    password_hash = hasher.hash(password)
    statement = "INSERT INTO Accounts (Email, PasswordHash, Role) VALUES (%s, %s, %s)"

    with conn.cursor() as cursor:
        cursor.execute(statement, (email, password_hash, role))
        conn.commit()


for email in students:
   create_account(email, students[email])


admins = {'vakeesan.moorthy@school.edu': "VMpass", 'esha.hooda@school.edu': "EHpass", 'tahereh.arabghalizi@school.edu': 'TApass'}

for admin in admins:
    create_account(admin, admins[admin], "Admin")

# Step 3: sample data for Students, Professors, Courses, Sections, Enrollments
for query in read_sql_file("sql-set-up/add_values.sql"):
    print(query)
    cursor.execute(query)
    conn.commit()

cursor.close()
conn.close()
print("Database set up complete.")
