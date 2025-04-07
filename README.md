# NomNomBox

IS213 AY2024/2025 Semester 2 Project for G6 Team 2

## Description

NomNomBox is a food delivery application built with microservices architecture. The system enables customers to order meal kits, interact with chatbots for recommendations, and provides a delivery management system.

### Key Features & Scenarios

#### Scenario 1: Order Meal Kit

- Customers can browse and select meal kits through the customer UI
- The system processes orders by checking customer details and inventory availability
- Payment integration with Stripe for secure transactions
- Order confirmation and status updates sent through notifications
- Full integration between Order, Customer, Inventory and Payment services

#### Scenario 2: Chatbot Recommendations

- Customers can request meal kit recommendations through the chatbot interface
- The system utilizes Gemini AI for intelligent meal suggestions
- Chat history is stored for context-aware conversations
- The chatbot retrieves customer information, past orders, and available inventory
- Personalized recommendations based on customer preferences and order history

#### Scenario 3: Delivery Management

From Customer's perspective:

- Customers can set preferred delivery times for their orders
- The system checks and confirms delivery availability
- Order and delivery confirmations are sent to customers

From Driver's perspective:

- Drivers can acknowledge order pickups and send status updates
- Drivers can set their availability dates and times
- The schedule service manages driver availability
- Real-time notifications for new deliveries via AMQP (RabbitMQ)
- Driver schedule updates are processed via Kafka messaging

The application uses modern technologies including:

- RabbitMQ and Kafka for messaging and event processing
- Redis for caching
- Microservices architecture for scalability and resilience
- RESTful APIs for service communication

## Prerequisites

- Docker and Docker Compose installed on your machine
- Git (to clone the repository if needed)

### Setting up Docker

1. Install Docker Desktop

   - Download Docker Desktop from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
   - Follow the installation instructions for your operating system

2. Create a Docker Hub account

   - Visit [https://hub.docker.com/signup](https://hub.docker.com/signup) if you don't already have an account

3. Log in to Docker

   - Open a terminal or command prompt
   - Run the command:
     ```
     docker login
     ```
   - Enter your Docker Hub username and password when prompted

4. Verify Docker installation
   - Run the following command to check that Docker is working properly:
     ```
     docker --version
     ```

## Steps to Run the Application

1. Clone the repository (if you haven't already):

   ```
   gh repo clone Danwidj/NomNomBox
   cd NomNomBox
   ```

2. Build and start all services using Docker Compose:

   ```
   docker-compose up -d
   ```

   This will build and start all the microservices defined in the docker-compose.yml file

3. To access the applications:

   - Customer Frontend: http://localhost:5173
   - Driver Frontend: http://localhost:3000
   - API Documentation: http://localhost:8080/docs
   - RabbitMQ Management Console: http://localhost:15672

4. To view logs for a specific service:

   ```
   docker-compose logs -f <service-name>
   ```

   Or using Docker directly:

   ```
   docker logs -f <container-name>
   ```

   **Note on service names vs container names:**

   - **Service Name**: Used with docker-compose commands, this is the name defined in the docker-compose.yml file (e.g., customer_frontend, order, delivery)
   - **Container Name**: The actual running container instance name, used with docker commands. Docker Compose automatically generates these names by combining the project name, service name, and an instance number

   Container names:

   - nomnombox-customer_frontend-1
   - nomnombox-driver_frontend-1
   - nomnombox-order-1
   - nomnombox-customer-1
   - nomnombox-payment-1
   - nomnombox-order_composite-1
   - nomnombox-inventory-1
   - nomnombox-schedule-1
   - nomnombox-delivery-1
   - nomnombox-manage_deliveries-1
   - nomnombox-chathistory-1
   - nomnombox-send_query-1
   - nomnombox-gemini-1
   - nomnombox-api-docs-1
   - nomnombox-notifications-1
   - nomnombox-rabbitmq-1
   - kafka
   - zookeeper
   - redis

5. To stop all services:

   ```
   docker-compose down
   ```

6. To stop all services and remove volumes (including kafka_data):

   ```
   docker-compose down -v
   ```

7. To rebuild a specific service after making changes:
   ```
   docker-compose build <service-name>
   docker-compose up -d <service-name>
   ```

## Services Overview

### Frontend Services

- Customer Frontend: http://localhost:5173
- Driver Frontend: http://localhost:3000

### Backend Services

- Order Service: http://localhost:5001
- Customer Service: http://localhost:5003
- Payment Service: http://localhost:5004
- Order Composite Service: http://localhost:5005
- Inventory Service: http://localhost:5006
- Schedule Service: http://localhost:5007
- Delivery Service: http://localhost:5010
- Manage Deliveries Service: http://localhost:5000
- Chat History Service: http://localhost:5012
- Send Query Service: http://localhost:5100
- Gemini Service: http://localhost:5009
- API Documentation: http://localhost:8080
- OutSystems API Documentation: https://personal-6fbyxkeb.outsystemscloud.com/DriverService/rest/v1/

### Infrastructure

- Kafka: port 9092
- Zookeeper: port 22181
- Redis: port 6379
- RabbitMQ:
  - AMQP: port 5672
  - Management Console: http://localhost:15672 (default credentials: guest/guest)

For detailed API documentation, visit http://localhost:8080/docs after starting the application.

## Using Scripts for Different Platforms

### Linux/macOS Shell Scripts

For Linux or macOS systems, you can use the shell scripts:

1. Make the shell scripts executable:

   ```
   chmod +x start-nomnombox.sh stop-nomnombox.sh
   ```

2. To start all services:

   ```
   ./start-nomnombox.sh
   ```

3. To stop all services and remove volumes:

   ```
   ./stop-nomnombox.sh
   ```

### Windows Batch Files

For Windows systems, you can use the batch files:

1. To start all services:

   ```
   start-nomnombox.bat
   ```

2. To stop all services and remove volumes:

   ```
   stop-nomnombox.bat
   ```
