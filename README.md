# Expense Tracker Manager

A beginner-friendly expense tracking web application built with **Python, Flask, MySQL, HTML, CSS, and JavaScript**.

## Features

- Add, view, edit, and delete expenses (CRUD).
- Track category, date, payment method, and notes.
- Dashboard cards for selected-month and all-time spending.
- Filter expenses by month and category; search title and notes.
- Category spending breakdown and largest expense for the selected month.
- Form validation, parameterized SQL queries, and database error handling.
- Responsive interface for desktop and mobile.

## Project structure

```text
expense-tracker-manager/
├── app.py
├── schema.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── expense_form.html
│   └── error.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Requirements

- Python 3.10+
- MySQL Server (MySQL Workbench is optional)
- A web browser

## Setup

### 1. Download or clone this project

```bash
git clone https://github.com/YOUR-USERNAME/expense-tracker-manager.git
cd expense-tracker-manager
```

If you downloaded the ZIP, extract it and open a terminal in the extracted folder.

### 2. Create a virtual environment

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Open MySQL Workbench, connect to your local MySQL server, open `schema.sql`, and execute it.

The SQL file creates the `expense_tracker` database and the `expenses` table. It also inserts three optional demo records; remove those INSERT statements if you do not want sample data.

### 5. Configure database credentials

Set the environment variables for your terminal session.

Windows PowerShell:

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
$env:DB_NAME="expense_tracker"
$env:FLASK_SECRET_KEY="change-this-to-a-long-random-value"
```

macOS/Linux:

```bash
export DB_HOST="localhost"
export DB_PORT="3306"
export DB_USER="root"
export DB_PASSWORD="YOUR_MYSQL_PASSWORD"
export DB_NAME="expense_tracker"
export FLASK_SECRET_KEY="change-this-to-a-long-random-value"
```

Replace `YOUR_MYSQL_PASSWORD` with your local MySQL password. These are local environment variables; do not upload your real password.

### 6. Run the application

```bash
python app.py
```

Open the address shown in the terminal (usually http://127.0.0.1:5000).

## Upload to GitHub using the website

1. Extract the ZIP file on your computer.
2. Create a new repository on GitHub named `expense-tracker-manager`.
3. Open the repository and select **Add file → Upload files**.
4. Drag the *contents* of the extracted project folder into the upload area. Keep the `templates` and `static` folders intact.
5. Commit the upload with a message such as `Add Expense Tracker Manager project`.

GitHub's browser uploader supports multiple files, but keep each uploaded file within its current size limit. See the official [GitHub file upload guide](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).

## Notes

- This project runs locally; it is not automatically hosted online.
- Never commit `.env`, database passwords, API keys, or other secrets.
- Flask debug mode is disabled by default. Do not enable debug mode on a public server.
- This is a portfolio starter project. Review and test it in your own environment before presenting it as your work.
