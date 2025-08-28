import os
import mysql.connector
from dotenv import load_dotenv

def connect_to_db():
    """
    Connects to the MySQL database using credentials from the .env file.
    Returns the connection object or None if connection fails.
    """
    load_dotenv() # Load environment variables from .env file

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            print("Successfully connected to the database.")
            return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

if __name__ == '__main__':
    # This block allows you to test the connection directly
    conn = connect_to_db()
    if conn:
        conn.close()
        print("Database connection closed.")