📄 PDF Tools – Django + Docker + Nginx + Postgres

A containerized PDF utility application built with:

Django, Gunicorn, Nginx, PostgreSQL, Docker & Docker Compose

This project demonstrates a production-style container architecture suitable for DevOps learning and deployment. This project was made using AI tools like claude and ChatGPT. for example the code used int he view.py and the HTML content that shows in the browser are entirely AI made. This project was only for learning purpose and to see how a django project can has a CICD pipeline.

🏗 Architecture
Browser
↓
Nginx (reverse proxy)
↓
Gunicorn
↓
Django App
↓
PostgreSQL
🚀 Features

Convert PDF → Images

Convert Images → PDF

Merge multiple PDFs

Static & Media file handling

Production-ready configuration

Dockerized multi-service setup

📦 Requirements

Docker

Docker Compose

Check versions:

docker --version
docker compose version
⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/sujanst98644/pdftools.git
cd pdftools
2️⃣ Create .env file

Create a file named .env in the project root:

SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=pdftools
DB_USER=pdftoolsuser
DB_PASSWORD=strongpassword
DB_HOST=db
DB_PORT=5432

Important:

DB_HOST must be db (Docker service name)

Do not use localhost inside containers

3️⃣ Build and Start Containers
docker compose up --build

This will start:

PostgreSQL

Django (Gunicorn)

Nginx

4️⃣ Apply Migrations

Open another terminal:

docker compose exec web python manage.py migrate
5️⃣ Collect Static Files (Production)
docker compose exec web python manage.py collectstatic --noinput
6️⃣ Access Application

Open browser:

http://localhost
🛠 Development Mode (Optional)

To run in development mode:

Change in docker-compose:

environment:
DJANGO_SETTINGS_MODULE: pdftools.settings.development

Set in .env:

DEBUG=True

Restart containers:

docker compose down
docker compose up --build
📂 Project Structure
pdftools/
│
├── converter/
├── pdftools/
│ └── settings/
│ ├── base.py
│ ├── development.py
│ └── production.py
│
├── nginx/
│ └── default.conf
│
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
🗄 Volumes Used

postgres_data → Database persistence

staticfiles → Collected static files

media → Uploaded files

🔐 Production Notes

DEBUG=False

Gunicorn used instead of Django runserver

Nginx serves static & media

Postgres is isolated in Docker network

Environment variables loaded via .env

🧪 Common Commands

Stop containers:

docker compose down

Rebuild containers:

docker compose up --build

View logs:

docker compose logs -f

Access container shell:

docker compose exec web sh
📘 DevOps Concepts Demonstrated

Docker layer caching

Multi-container architecture

Reverse proxy setup

Environment-based Django settings

Persistent volumes

Service-to-service networking

Production WSGI server (Gunicorn)

📌 Future Improvements

HTTPS with Certbot

CI/CD pipeline

Docker image optimization (multi-stage builds)

Cloud deployment (AWS, DigitalOcean, etc.)

Healthchecks
