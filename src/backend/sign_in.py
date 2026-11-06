from backend.connection import engine
from sqlalchemy import text
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher()

def valid_email(email):
    query = text("Select COUNT(Email) AS Count FROM accounts WHERE Email = :email")
    with engine.connect() as conn:
        result = conn.execute(query, {'email': email}).fetchone()
    return result.Count == 1


def sign_in(email, password):

    if not valid_email(email):
        return None

    query = text("Select AccountID, PasswordHash, Role FROM accounts WHERE Email = :email")
    with engine.connect() as conn:
        result = conn.execute(query, {'email': email}).fetchone()

    try:
        hasher.verify(result.PasswordHash, password)
        return [result.AccountID , result.Role]
    except VerifyMismatchError:
        return None


