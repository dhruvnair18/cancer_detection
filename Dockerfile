# Use Python 3.10 base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for the web app
EXPOSE 8000

# Run the Flask app with Gunicorn
CMD ["gunicorn", "cancer_app.app:app", "--bind", "0.0.0.0:8000"]
