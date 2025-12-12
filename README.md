![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Framework-Django-092E20?logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Containerized-Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white)
![Tests](https://img.shields.io/badge/Testing-pytest-blue?logo=pytest)
![Full Stack](https://img.shields.io/badge/Application-Full%20Stack-green)
![Deployment](https://img.shields.io/badge/Hosted%20on-Render-8907fd?logo=render&logoColor=white)

#  **Client Request Management System**

### Django • Docker • PostgreSQL • Render • Agile • TDD

A full-stack **Client Request Management System (CRMS)** built with **Django**, **Docker**, and **PostgreSQL**, designed to help technical teams track client requests with clear visibility across clients, request types, and statuses.

This project was created as part of an Agile, Sprint-based workflow and demonstrates practical use of:

* Django models, admin customisation, and auth
* Role-based permissions (admin vs limited users)
* Dockerised local development
* PostgreSQL in production (Render)
* Automated testing with pytest + pytest-django
* Custom management commands
* Deployment workflow on Render
* Technical documentation and system design
* Scrum practices, Jira sprint boards & Agile diaries

📄 Full technical write-up (architecture, Agile analysis, sprint boards, TDD rationale) is located in:
**`/docs/Client_Request_Management_System_WriteUp.docx`** 

---

## 📌 **Project Overview**

The Client Request Management System is a lightweight web application built to solve a real problem: **client requests were being missed due to poor visibility and inconsistent tracking**.

This system provides:

* A dashboard for managing clients, request types, and client requests
* Inline viewing of related request records
* Role-based access:

  * **Admins** → full CRUD
  * **Limited users** → create, read, update (but no deletion)
* A clean login and registration interface
* A secure, scalable deployment pipeline through Docker → Render

This project was developed using **Scrum**, divided into epics and user stories, with documented sprint boards, Agile diary entries and TDD cycles included in the write-up.

---

## ✨ **Key Features**

### 🔐 Authentication & Permissions

* Custom user roles (Admin, Limited User)
* Limited users can manage requests but **cannot delete**
* Newly registered users default to limited permissions
* Account-disabled redirection for non-staff roles

### 📁 Request Tracking

* Manage:

  * Clients
  * Request Types
  * Client Requests
* Inline related objects within the Django admin UI
* Status flow: **Pending → In Progress → Completed**

### 🛠 Developer Experience

* **Full Docker environment**
* **Makefile** to streamline commands
* **Automated test suite** (pytest + coverage)
* **Management commands**: seeding, wiping data

### ☁️ Deployment

* Hosted on **Render**
* PostgreSQL production database
* Static files via WhiteNoise
* Gunicorn as WSGI server

---

## 📂 **Project Structure**

```
client-request-management-system/
│
├── main/                  # Django app
├── tests/                 # pytest test suite
├── docker/                # Docker config files
├── docs/
│    └── Client_Request_Management_System_WriteUp.docx
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🐳 **Docker & Makefile Workflow**

This project includes a Makefile so you can manage Django + Docker without long commands:

```bash
make <command>
```

### Common Commands

| Command               | Description                     |
| --------------------- | ------------------------------- |
| `make build`          | Build Docker containers         |
| `make up`             | Start containers                |
| `make down`           | Stop/remove containers          |
| `make makemigrations` | Create migrations               |
| `make migrate`        | Apply migrations                |
| `make exampledata`    | Seed example users + data       |
| `make test`           | Run tests inside Docker         |
| `make coverage`       | Run tests with coverage         |
| `make collectstatic`  | Collect static files            |
| `make flush`          | Wipe all DB data                |
| `make shell`          | Open Django shell inside Docker |

---

## ⚙️ **Setup & Development**

### 1. Clone the repository

```bash
git clone https://github.com/IsaacPatrickson/client-request-management-system.git
cd client-request-management-system
```

### 2. Build the Docker environment

```bash
make build
```

### 3. Start the development server

```bash
make up
```

### 4. Apply migrations & load seed data

```bash
make makemigrations
make migrate
make exampledata
```

### 5. Collect static files

```bash
make collectstatic
```

Access the app at:
**[http://localhost:8000](http://localhost:8000)**

---

## 🗄 **Management Commands**

### Wipe the database

```bash
make flush
```

### Seed example data

```bash
make exampledata
```

---

## 🧪 **Testing**

Run the full pytest suite:

```bash
make test
```

Run with coverage:

```bash
make coverage
```

Generate an HTML report:

```bash
docker-compose exec web pytest --cov=main --cov-report=html
```

The test suite includes:

* Form validation tests
* Registration tests
* Authentication and permission tests
* Model behaviour
* Dashboard and CRUD behaviour

All TDD details and screenshots are included in the write-up.


---

## 🚀 Deployment (Render – Production Setup)

This application was deployed to a live production environment using **Render**, backed by a **managed PostgreSQL database**.

Although the live deployment may not always be active, the configuration and workflow demonstrate a **real-world Django production deployment**, including cloud hosting, environment-based configuration, and database management.

## Deployment Architecture Overview

* **Hosting platform:** Render
* **Backend framework:** Django
* **Database:** Managed PostgreSQL (Render)
* **Application server:** Gunicorn
* **Static file serving:** WhiteNoise
* **Secrets & configuration:** Environment variables
* **Containerisation:** Docker (previous deployment)

Production-specific considerations included:

* Using `psycopg2` instead of `psycopg2-binary`
* Running database migrations against a hosted PostgreSQL instance
* Collecting and serving static files
* Disabling debug mode in production

This setup reflects a **real-world Django deployment pipeline** rather than a development-only configuration.

## Step-by-Step Deployment on Render

### 1️⃣ Create the PostgreSQL Database

1. Create a **PostgreSQL** database in Render.
2. Assign it to a **Project**.
3. Choose a **region**.
4. Ensure the database and web service use the **same region** (recommended).

### 2️⃣ Create the Web Service

1. Create a new **Web Service** in Render.
2. Connect it to this GitHub repository.
3. Set the region to match the PostgreSQL database.
4. Allow Render to build and deploy the service.

### 3️⃣ Configure Environment Variables

In the Render Web Service settings, add the following:

```text
ALLOWED_HOSTS=client-request-management-system.onrender.com
CSRF_TRUSTED_ORIGINS_URL=https://client-request-management-system.onrender.com
DATABASE_URL=<PostgreSQL database URL>
DEBUG=False
DJANGO_ENV=production
DJANGO_SECRET_KEY=<generated secret key>
```

Generate a secret key using:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 4️⃣ Initial Deployment

Once environment variables are set, Render will automatically build and deploy the application using:

* Gunicorn as the application server
* WhiteNoise for static file handling

### 5️⃣ Database Migration & Data Seeding (Paid Render Tier)

Access the **Render Shell** and run:

```bash
python manage.py migrate
python manage.py create_limited_user_group
python manage.py seed_users
python manage.py seed_generic_data
python manage.py seed_client_data
```

### 6️⃣ Wiping Seeded Data (Development Only)

To remove all records from the core tables:

```bash
python manage.py wipe_data
```

⚠️ This command is destructive and should only be used in development or testing environments.

### 7️⃣ Seeded User Credentials

Seeded credentials are defined in:

```
main/management/commands/seed_users.py
```

Example:

```text
Username: superadmin
Password: superpass123
```

---

## 📘 **User Manual (Simplified)**

Screenshots are included in the write-up and original appendices inside `/docs`.

### Registration

1. Click **Register**
2. Enter required fields
3. Success message appears

### Limited User Login

* View dashboard with limited tables
* Can create/edit requests
* Cannot delete

### Admin Login

* Full CRUD access for all models
* Admin dashboard view

### Logout

* Logout button → success message → redirect to login page

### CRUD Actions

* **READ**: View list of client requests
* **CREATE**: Add new client request
* **UPDATE**: Edit existing request
* **DELETE**: Admin-only

---

## 📄 **Full Technical Write-Up**

Architecture, Agile methods, TDD, sprint boards, ERDs, appendices, user journeys and screenshots are documented in:

👉 **`/docs/Client_Request_Management_System_WriteUp.docx`**


---

## 👤 **Author**

**Isaac Patrickson**
Software Engineering & Agile – Final Project
Level 6 Digital Technology Solutions Degree Apprentice

GitHub: [https://github.com/IsaacPatrickson](https://github.com/IsaacPatrickson)
Email: **[isaacspatrickson@gmail.com](mailto:isaacspatrickson@gmail.com)**
