import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Establishes a connection to the MySQL database.
    Returns the connection object if successful, else None.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',         # change if needed
            user='root',      # your MySQL username
            password='pass1',  # your MySQL password
            database='elearning_platform'   # your MySQL database name
        )
        if connection.is_connected():
            print("[+] Connected to MySQL database ✅")
            return connection

    except Error as e:
        print(f"[-] Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("[+] MySQL connection closed ✅")