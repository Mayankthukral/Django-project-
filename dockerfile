# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Copy the rest of the application code into the container at /app
COPY . /app/


# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "dcrm.wsgi:application", "--bind", "0.0.0.0:8000"]