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
- [User Manual](#user-manual)

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


## User Manual

Assistive screenshots are in the Appendicies of Isaac Patrickson's Final submission point: Software Engineering and Agile end-of-module assessment

### Register Journey (Appendix D)
1. On the homepage, the user presses the register button.
2. The user enters their details which match the requirements for each field and presses the register button.
3. The fields are wiped and a success message is displayed showing the user they have successfully registered.

See the limited permissions user login journey to continue to the dashboard.

### Limited User Login Journey (Appendix E)
1. On the homepage, the user presses the login button.
2. The user is taken to the login page. Valid limited user credentials are entered and the user logs in.
3. The limited user is greeted with the dashboard screen which shows a limited list of tables and a list of recent changes made by the user.

### Admin User Login Journey (Appendix G)
1. On the homepage, the user presses the login button.
2. The user is taken to the login page. Valid admin credentials are entered and the user logs in.
3. The admin user is greeted with the dashboard screen which shows all tables and a list of recent changes made by the user.

### Logout Journey (Appendix H)
1. Once in the dashboard, any user can logout by pressing the logout button.
2. Once the logout button is pressed, the user is presented with a success message confirming that they have successfully logged out. They are given the option to return to the login page.
3. Upon clicking the button to log in again, the user is taken to the custom login page.

### Create, Read, Update and Delete Actions (Appendix E; Appendix G)
1. An admin/limited user has pressed the Client Requests button to view the client requests table (READ).
2. An admin/limited user has pressed the add button to add a new client request (CREATE).
3. An admin/limited user has clicked on the id of a record and they are taken to the view for changing the details of a client request (UPDATE).
4. An admin user has pressed the delete button when updating a record which takes them to the deletion confirmation page (DELETE).