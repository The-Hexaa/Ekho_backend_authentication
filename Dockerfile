# Use the official Python image
FROM python:3.11.9-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 4000

# Define the command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
