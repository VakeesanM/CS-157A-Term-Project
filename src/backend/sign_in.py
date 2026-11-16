from backend.connection import create_connection
from sqlalchemy import text
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher()

def valid_email(email, conn):
    query = "Select COUNT(Email) AS Count FROM accounts WHERE Email = %s"
    

    with conn.cursor() as cursor:
        cursor.execute(query, (email,))
        result = cursor.fetchone()
    
    
    return result[0] == 1

def sign_in(email, password):
    conn = create_connection()
    if not valid_email(email, conn):
        conn.close()
        return None

    query = "Select AccountID, PasswordHash, Role FROM accounts WHERE Email = %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        conn.close()
    try:
        hasher.verify(result[1], password)
        return [result[0], result[2]]
    except VerifyMismatchError:
        return None
    


