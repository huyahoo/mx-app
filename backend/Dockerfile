# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# --------------------------------------------------------
# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
# --------------------------------------------------------



# --------------------------------------------------------
# Set environment variables
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
# EXPOSE 5000

# Run the application
# CMD ["flask", "run"]
# --------------------------------------------------------