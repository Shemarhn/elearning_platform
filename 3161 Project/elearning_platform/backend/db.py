import os
import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Establishes a connection to the MySQL database.
    Returns the connection object if successful, else None.
    """
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'pass1'),
            database=os.environ.get('DB_NAME', 'elearning_platform')
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