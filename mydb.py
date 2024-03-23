import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to Azure PostgreSQL using environment variables
try:
    connection = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        dbname='postgres',  # Connect to the default 'postgres' database
        port=os.environ.get('DB_PORT'),  # Default PostgreSQL port
        sslmode='require'  # Add SSL mode for secure connection
    )

    # Set autocommit to True
    connection.autocommit = True

    # Create a cursor object
    cursor = connection.cursor()

    # Create a database using the DB_NAME environment variable
    db_name = os.environ.get('DB_NAME')
    cursor.execute(f'CREATE DATABASE {db_name}')

    # Close the cursor and connection
    cursor.close()
    connection.close()

    print("Database created successfully!")
except Exception as e:
    print(f"Error creating database: {e}")
