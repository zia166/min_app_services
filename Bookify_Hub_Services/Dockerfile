# Use an official Python runtime as a parent image
FROM python:3.11.1

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /var/www/webapp

# Copy the current directory contents into the container at /app
COPY . .
RUN pip install -U pip
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install the corsheaders module
RUN pip install django-cors-headers
# Install the pymongo module
RUN pip install pymongo
# Install the certifi module
RUN pip install certifi
# Install necessary dependencies
RUN pip install boto3

# Install additional dependencies, including decouple
RUN pip install python-decouple

# Expose port 8080
EXPOSE 8000

# Run Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]