import os
import mysql.connector
from dotenv import load_dotenv


def setup_database():
    """
    Creates the database and required tables if they don't already exist.
    """
    load_dotenv()

    # First, connect to MySQL server without specifying a database
    try:
        db_conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = db_conn.cursor()
        db_name = os.getenv("DB_NAME")

        # Create the database
        print(f"Creating database '{db_name}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print("Database created successfully or already exists.")

        # Now, connect to the specific database
        cursor.execute(f"USE {db_name}")

        # Create the customer table
        print("Creating table 'customer'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            cid VARCHAR(20) PRIMARY KEY,
            name VARCHAR(50),
            address VARCHAR(100),
            email VARCHAR(50),
            phone VARCHAR(20),
            meterno VARCHAR(20) UNIQUE
        )
        """)
        print("Table 'customer' created successfully.")

        # Create the bill table
        print("Creating table 'bill'...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bill (
            bill_id INT AUTO_INCREMENT PRIMARY KEY,
            meterno VARCHAR(20),
            billdate DATE,
            current_units INT,
            previous_units INT,
            consumed INT,
            amount DECIMAL(10, 2),
            duedate DATE,
            paid VARCHAR(20),
            FOREIGN KEY (meterno) REFERENCES customer(meterno)
        )
        """)
        print("Table 'bill' created successfully.")

    except mysql.connector.Error as err:
        print(f"Failed to set up database: {err}")
    finally:
        if 'db_conn' in locals() and db_conn.is_connected():
            cursor.close()
            db_conn.close()
            print("Database setup connection closed.")


if __name__ == '__main__':
    setup_database()