# Use the official Python image
FROM python:3.9.18-alpine3.19

# Set the working directory in the container
WORKDIR /app

# Copy the application code
COPY . .

# Install pip and create requirements.txt from existing installed packages
RUN pip install --no-cache-dir pip
RUN pip freeze > requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Flask port
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["python", "run", "--host=0.0.0.0"]
