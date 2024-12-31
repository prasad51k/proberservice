# Use the official Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the port the app runs on (default for Django is 8000)
EXPOSE 8000

# Run the Django application
CMD ["gunicorn", "proberservice.wsgi:application", "--bind", "0.0.0.0:8000"]
