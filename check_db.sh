#!/bin/bash

# Function to check if the database exists
check_database() {
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d postgres -c "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1
}

# Call the function and check the database
if check_database; then
    echo "Database already exists. Skipping steps."
    exit 0
else
    echo "Database does not exist."
    exit 1
fi
