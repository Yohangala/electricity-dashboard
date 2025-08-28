import os
import random
from datetime import date, timedelta
import numpy as np
from faker import Faker
from db_connector import connect_to_db


def generate_data():
    """
    Populates the database with realistic mock customer and bill data.
    """
    db_conn = connect_to_db()
    if not db_conn:
        print("Could not connect to DB, aborting.")
        return

    cursor = db_conn.cursor()
    fake = Faker('en_IN')  # Generates Indian-style names and addresses

    # --- Clear existing data to prevent duplicates on re-run ---
    print("Clearing existing bill and customer data...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE bill;")
    cursor.execute("TRUNCATE TABLE customer;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # --- Generate Customer Data ---
    customers = []
    for i in range(50):  # Create 50 customers
        customer = (
            f"CUST{1001 + i}",  # Customer ID
            fake.name(),  # Name
            fake.address().replace('\n', ', '),  # Address
            fake.email(),  # Email
            fake.phone_number(),  # Phone
            f"MTR{5001 + i}"  # Meter No
        )
        customers.append(customer)

    insert_customer_query = """
    INSERT INTO customer (cid, name, address, email, phone, meterno) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_customer_query, customers)
    print(f"Successfully inserted {len(customers)} customers.")

    # --- Generate Bill Data ---
    bills = []
    for customer in customers:
        meterno = customer[5]
        previous_units = random.randint(1000, 2000)

        for month in range(24):  # Create 24 months of data
            bill_date = date(2023, 1, 1) + timedelta(days=month * 30)

            # Simulate seasonal consumption (higher in summer)
            month_of_year = bill_date.month
            if 3 <= month_of_year <= 6:  # Summer months
                consumed = random.randint(250, 700)
            else:  # Other months
                consumed = random.randint(100, 400)

            current_units = previous_units + consumed

            # Calculate bill amount based on your old logic
            if consumed < 200:
                amount = 4 * consumed
            elif consumed < 400:
                amount = 6 * consumed
            else:
                amount = 8 * consumed

            due_date = bill_date + timedelta(days=15)
            # 90% chance the bill is 'Paid', 10% 'Unpaid'
            paid_status = np.random.choice(['Paid', 'Unpaid'], p=[0.9, 0.1])

            bill = (meterno, bill_date, current_units, previous_units, consumed, amount, due_date, paid_status)
            bills.append(bill)
            previous_units = current_units

    insert_bill_query = """
    INSERT INTO bill (meterno, billdate, current_units, previous_units, consumed, amount, duedate, paid) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_bill_query, bills)
    print(f"Successfully inserted {len(bills)} bill records.")

    # --- Commit and close ---
    db_conn.commit()
    cursor.close()
    db_conn.close()
    print("Data generation complete. Connection closed.")


if __name__ == '__main__':
    generate_data()