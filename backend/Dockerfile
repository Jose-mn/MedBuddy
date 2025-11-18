FROM python:3.11-slim

# Set a working directory inside the container
WORKDIR /Medbuddy

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire repo into the container
COPY . .

# Expose port
EXPOSE 8000

# Start FastAPI by running main.py directly
CMD ["python", "backend/main.py"]
