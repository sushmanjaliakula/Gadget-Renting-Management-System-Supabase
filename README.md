# Gadget Renting Management System

A Flask + MySQL web application built around the supplied `gadget_renting` database.

## Features

- Dashboard metrics and recent rentals
- CRUD screens for Customers, Gadgets, Rentals, Payments, Returns and Maintenance
- Uses the existing MySQL table and column names
- Responsive interface with dark/light theme switch
- MySQL foreign-key errors are surfaced as user-friendly messages
- Render deployment configuration and health endpoint

## Database schema

The application expects the six existing tables from the supplied SQL file:

- `Customers`
- `Gadgets`
- `Rentals`
- `Payments`
- `Returns`
- `Maintenance`

It does **not** automatically create, drop, reset or seed the database. Preserve your existing database and data.

## 1. Local development

Requirements: Python 3.11+ and a reachable MySQL server.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then enter your local MySQL connection details. Do not commit `.env`.

```bash
python app.py
```

Open http://127.0.0.1:5000

## 2. Existing SQL files

The `sql/source_files/` directory contains the original SQL files supplied for this project. Read `sql/README.md` before executing any SQL. The original setup script contains `CREATE DATABASE` and sample `INSERT` statements; do not rerun it against a populated database unless you have a verified backup and intend to do so.

## 3. Deploy to GitHub

1. Create a new GitHub repository.
2. Extract this ZIP.
3. Open the extracted project folder in VS Code.
4. Review `.gitignore`; it excludes `.env`.
5. Commit and push the project.

```bash
git init
git add .
git commit -m "Add Gadget Renting Management System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your own repository URL.

## 4. Prepare a cloud MySQL database

Render runs your Flask backend online. Your local MySQL Workbench database is not automatically accessible to Render.

Before deploying:
1. Choose a managed MySQL provider that permits connections from Render.
2. Create a database named `gadget_renting` (or configure `DB_NAME` to match).
3. Import the schema and data from your existing database using a database export/backup.
4. Verify that all six tables, foreign keys, the `Rental_Details` view (if desired), and records are present.
5. Obtain the host, port, username, password and database name from that provider.
6. Restrict database access using the provider's network/security controls where available. Use TLS/SSL when required.

Do not expose database credentials in GitHub or in frontend JavaScript.

## 5. Deploy Flask on Render

1. Sign in to Render and choose **New + → Web Service**.
2. Connect the GitHub repository.
3. Runtime: Python.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Add these environment variables in Render:

| Key | Value |
|---|---|
| `SECRET_KEY` | Long random secret |
| `DB_HOST` | Cloud MySQL host |
| `DB_PORT` | Cloud MySQL port, usually 3306 |
| `DB_USER` | Cloud database username |
| `DB_PASSWORD` | Cloud database password |
| `DB_NAME` | `gadget_renting` |

The included `render.yaml` can prefill the service configuration, but secret database values must still be entered in Render.

After deployment, open `/health` on your Render URL. A successful response reports `"status": "ok"` and `"database": true`.

## Important limitations / next production tasks

This is a database-connected project foundation, not a fully hardened commercial rental platform. Before public production use, add administrator authentication and authorization, CSRF protection, audit logging, pagination, stronger validation and automated tests. Rental creation should also be enhanced with an atomic availability check/update, date-overlap validation, and coordinated return/payment workflows. Do not expose this admin interface publicly until access control is implemented.
