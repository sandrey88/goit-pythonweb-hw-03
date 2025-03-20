# goit-pythonweb-hw-03

# Web Application with HTTP Server

This is a simple web application built with Python's built-in HTTP server. It allows users to send and read messages, which are stored in a JSON file.

## Features

- Simple HTTP server implementation
- Message sending and storage functionality
- Docker support with persistent storage

## Requirements

### For Local Development

- Python 3.x
- Jinja2 template engine

### For Docker Deployment

- Docker
- Docker Compose

## Installation and Running

### Local Setup

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
python3 main.py
```

4. Open your browser and navigate to:

```
http://localhost:3000
```

### Docker Setup

#### Using Docker Compose (Recommended)

1. Build and start the container:

```bash
docker-compose up --build
```

2. To run in background:

```bash
docker-compose up -d
```

3. To stop the container:

```bash
docker-compose down
```

#### Using Docker Directly

1. Build the Docker image:

```bash
docker build -t message-app .
```

2. Create a Docker volume for persistent storage:

```bash
docker volume create message_app_data
```

3. Run the container:

```bash
docker run -d \
  --name message-app \
  -p 3000:3000 \
  -v message_app_data:/app/storage \
  message-app
```

4. To stop the container:

```bash
docker stop message-app
```

5. To remove the container:

```bash
docker rm message-app
```

### Docker Volume Management

- View volume data:

```bash
docker volume inspect message_app_data
```

- Remove volume (will delete all messages):

```bash
docker volume rm message_app_data
```

## Note

Messages are stored in `storage/data.json` within the Docker volume
