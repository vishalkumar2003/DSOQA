import pandas as pd
import pymysql.cursors
import bcrypt

# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Viskav@2003",
    database="email",
    cursorclass=pymysql.cursors.DictCursor  # Optional, gives results as dictionaries
)

with conn.cursor() as cursor:
    # Create the 'users' table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            age INT,
            city VARCHAR(255),
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255)
        );
    """)
conn.commit()

# Fetch users sorted by email
with conn.cursor() as cursor:
    users = cursor.fetchall()  # Fetch all rows

# Hash passwords and update the database
with conn.cursor() as cursor:
    for user in users:
        email = user["email"]
        plain_password = user["password"]

        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode(), salt).decode()

        # Update the database with the hashed password
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))

    conn.commit()  # Commit changes

# Close the connection
conn.close()