import psycopg2
import os

# Retrieve sensitive information from environment variables

# Connect to Azure PostgreSQL using the provided server name
connection = psycopg2.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    dbname='postgres',  # Connect to the default 'postgres' database
    port=os.environ.get('DB_PORT'),  # Default PostgreSQL port
    sslmode='require' # Add SSL mode for secure connection
)


# Set autocommit to True
connection.autocommit = True

# Create a cursor object
cursor = connection.cursor()

# Create a database named 'elderco'
db_name = os.environ['DB_NAME']
cursor.execute(f'CREATE DATABASE {db_name}')

# Close the cursor and connection
cursor.close()
connection.close()

print("All Done!")
