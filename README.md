# SEA-web-app

A Django-based Client Request Management System (CRMS) with Docker development environment and production hosting on Render.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Prerequisites](#prerequisites)
- [Using the Makefile](#docker--django-management-with-makefile)
- [Makefile Commands](#available-makefile-commands)
- [Setup & Development](#setup--development)  
- [Management Commands](#management-commands)  
- [Testing](#testing)  
- [Deployment](#deployment)  

---

## Project Overview

SEA-web-app is a Django application designed to manage client requests efficiently. The app uses Docker for local development to ensure consistency across environments and is deployed to Render for production hosting.

---

## Features

- User authentication and authorization with custom user groups  
- Client, Request Type, and Client Request management via Django admin  
- Custom permission groups for fine-grained access control  
- Inline editing of related models in the admin interface  
- Dockerized development environment for easy setup  
- Management commands for seeding example data and wiping the database  

---

## Prerequisites

- Docker & Docker Compose installed  
- Python 3.11+ (if running outside Docker)  
- Render account for production deployment  

---

## Docker & Django Management with Makefile

To simplify running common Docker and Django commands, this project includes a `Makefile` with predefined targets. This allows you to execute complex commands easily by running:

```bash
make <command>
```

## Available Makefile Commands

| Command           | Description                                      |
|-------------------|--------------------------------------------------|
| `make build`        | Build the Docker containers                      |
| `make up`           | Start the Docker containers in detached mode    |
| `make down`         | Stop and remove the Docker containers            |
| `make makemigrations` | Create new Django migrations                     |
| `make migrate`      | Apply Django database migrations                 |
| `exampledata`       | Seed users and example data                      |
| `make test`         | Run tests inside the Docker container using pytest |
| `make coverage`     | Run tests with coverage report                    |
| `make collectstatic`| Collect static files for production               |
| `make flush`        | Flush the database (delete all data)             |
| `make shell`        | Open a Django shell inside the Docker container  |

## How to Use

Instead of typing long `docker-compose exec` commands, just run:

```bash
make migrate
make test
make collectstatic
make flush
```
and so on.

## Setup & Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sea-web-app.git
   cd sea-web-app
   ```

2. Build the Docker image:
   ```bash
   make build
   ```

3. Start the development environment:
   ```bash
   make up
   ```

4. Apply migrations, create users and seed data:
   ```bash
   make makemigrations
   make migrate
   make exampledata
   ```

5. Collect static files (for local testing):
   ```bash
   make collectstatic
   ```

6. Access the app locally at http://localhost:8000


## Management Commands

### Wipe Database
Remove all data from all models (including users):

```bash
docker-compose exec web python manage.py wipe_data
```
or
```bash
make flush
```

### Seed Example Data
Seed all models with example data:
```bash
make exampledata
```

## Testing
Run the test suite with pytest inside the Docker container:
```bash
make test
```

Run tests with coverage report:
```bash
make coverage
```

Generate HTML coverage report:
```bash
docker-compose exec web pytest --cov=main --cov-report=html
```


## Deployment

This project uses Render for hosting in production.

### Production Checklist

- Switch `psycopg2-binary` to `psycopg2` in your `requirements.txt` before deploying.

- Run `collectstatic` on Render or as part of the deployment script:

```bash
python manage.py collectstatic --noinput
```