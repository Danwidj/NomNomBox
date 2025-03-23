# Use Python 3.10 as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all files from your project folder into the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose port 5100
EXPOSE 5100

# Command to run the microservice
CMD ["python", "query.py"] 