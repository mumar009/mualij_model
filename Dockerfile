FROM python:3.9

# Install required system packages
RUN apt-get update && apt-get install -y libgomp1

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
