# user_ops.py
import bcrypt
from db import create_connection, close_connection

def register_user(userid, password, role):
    """
    Registers a new user (student, lecturer, admin) with hashed password.
    """
    connection = create_connection()
    if not connection:
        print("[-] Registration failed: No DB connection.")
        return False

    cursor = connection.cursor()

    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert user into database
        sql = "INSERT INTO users (userid, password_hash, role) VALUES (%s, %s, %s)"
        cursor.execute(sql, (userid, hashed_password, role))
        connection.commit()
        print(f"[+] User '{userid}' registered successfully as '{role}'.")
        return True

    except Exception as e:
        print(f"[-] Error during registration: {e}")
        return False

    finally:
        cursor.close()
        close_connection(connection)

def login_user(userid, password):
    """
    Authenticates a user based on userid and password.
    """
    connection = create_connection()
    if not connection:
        print("[-] Login failed: No DB connection.")
        return False

    cursor = connection.cursor(dictionary=True)

    try:
        # Retrieve user record
        sql = "SELECT * FROM users WHERE userid = %s"
        cursor.execute(sql, (userid,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            print(f"[+] User '{userid}' logged in successfully as '{user['role']}'.")
            return user  # return user details (could be useful for session management)
        else:
            print("[-] Invalid credentials.")
            return None

    except Exception as e:
        print(f"[-] Error during login: {e}")
        return None

    finally:
        cursor.close()
        close_connection(connection)
