# Django-project-

# save following Environment variable in .env file at root of the project

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=


# create virtual environment
virtualenv .venv
# Activate virtual environment
.venv\Scripts\activate

# install the dependencies
pip install -r requirements.txt

# create a new database at the server level
python mydb.py  

 # To apply database migrations.
python manage.py migrate 
