# Use the slim version of Python 3.11
FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update \
    && apt-get install -y gcc libpq-dev netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip

# Copy the requirements file to the app dir app/requirements.txt
COPY requirements.txt . 

# Install dependencies
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application files
COPY . .

# Make the wait-for-it.sh script executable
RUN chmod +x wait-for-it.sh

# Command to run the application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dev.wsgi:application"]

