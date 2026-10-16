import os
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")

CATEGORIES = [
    "Food", "Transport", "Shopping", "Bills", "Health",
    "Entertainment", "Education", "Travel", "Other"
]

def get_db_connection():
    """Create a fresh MySQL connection using environment variables."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "expense_tracker"),
        port=int(os.getenv("DB_PORT", "3306")),
    )

def query_db(sql, params=(), fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        result = cursor.fetchall() if fetch else cursor.lastrowid
        if not fetch:
            conn.commit()
        return result
    finally:
        cursor.close()
        conn.close()

def money(value):
    return float(value or 0)

@app.template_filter("inr")
def inr(value):
    try:
        return "₹{:,.2f}".format(float(value or 0))
    except (ValueError, TypeError):
        return "₹0.00"

@app.route("/")
def dashboard():
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        month = date.today().strftime("%Y-%m")

    where = ["DATE_FORMAT(expense_date, '%Y-%m') = %s"]
    params = [month]
    if search:
        where.append("(title LIKE %s OR notes LIKE %s)")
        params.extend([f"%{search}%", f"%{search}%"])
    if category in CATEGORIES:
        where.append("category = %s")
        params.append(category)

    expenses = query_db(
        "SELECT id, title, amount, category, expense_date, payment_method, notes "
        "FROM expenses WHERE " + " AND ".join(where) +
        " ORDER BY expense_date DESC, id DESC",
        tuple(params), fetch=True
    )

    month_total = query_db(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM expenses "
        "WHERE DATE_FORMAT(expense_date, '%Y-%m') = %s",
        (month,), fetch=True
    )[0]["total"]

    all_time_total = query_db(
        "SELECT COALESCE(SUM(amount), 0) AS total FROM expenses", fetch=True
    )[0]["total"]

    category_totals = query_db(
        "SELECT category, SUM(amount) AS total FROM expenses "
        "WHERE DATE_FORMAT(expense_date, '%Y-%m') = %s "
        "GROUP BY category ORDER BY total DESC",
        (month,), fetch=True
    )
    largest = query_db(
        "SELECT title, amount, expense_date FROM expenses "
        "WHERE DATE_FORMAT(expense_date, '%Y-%m') = %s "
        "ORDER BY amount DESC LIMIT 1",
        (month,), fetch=True
    )

    return render_template(
        "dashboard.html",
        expenses=expenses,
        month=month,
        month_total=month_total,
        all_time_total=all_time_total,
        category_totals=category_totals,
        largest=largest[0] if largest else None,
        categories=CATEGORIES,
        search=search,
        selected_category=category,
        today=date.today().isoformat(),
    )

def validate_expense(form):
    title = form.get("title", "").strip()
    amount_raw = form.get("amount", "").strip()
    category = form.get("category", "").strip()
    expense_date = form.get("expense_date", "").strip()
    payment_method = form.get("payment_method", "Other").strip()
    notes = form.get("notes", "").strip()

    if not title:
        raise ValueError("Please enter an expense title.")
    if len(title) > 100:
        raise ValueError("Title must be 100 characters or fewer.")
    try:
        amount = Decimal(amount_raw)
    except (InvalidOperation, ValueError):
        raise ValueError("Enter a valid amount.")
    if amount <= 0 or amount > Decimal("999999999.99"):
        raise ValueError("Amount must be greater than zero.")
    if category not in CATEGORIES:
        raise ValueError("Choose a valid category.")
    try:
        parsed_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Choose a valid expense date.")
    if payment_method not in ["Cash", "UPI", "Debit Card", "Credit Card", "Net Banking", "Other"]:
        payment_method = "Other"
    return (title, str(amount.quantize(Decimal("0.01"))), category,
            parsed_date.isoformat(), payment_method, notes)

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        try:
            data = validate_expense(request.form)
            query_db(
                "INSERT INTO expenses (title, amount, category, expense_date, payment_method, notes) "
                "VALUES (%s, %s, %s, %s, %s, %s)", data
            )
            flash("Expense added successfully.", "success")
            return redirect(url_for("dashboard"))
        except ValueError as exc:
            flash(str(exc), "error")
        except mysql.connector.Error:
            app.logger.exception("Database error while adding expense")
            flash("Could not save the expense. Check your database settings.", "error")
    return render_template("expense_form.html", mode="Add", expense=None,
                           categories=CATEGORIES, today=date.today().isoformat())

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    rows = query_db("SELECT * FROM expenses WHERE id = %s", (expense_id,), fetch=True)
    if not rows:
        flash("Expense not found.", "error")
        return redirect(url_for("dashboard"))
    expense = rows[0]
    if request.method == "POST":
        try:
            data = validate_expense(request.form)
            query_db(
                "UPDATE expenses SET title=%s, amount=%s, category=%s, expense_date=%s, "
                "payment_method=%s, notes=%s WHERE id=%s",
                data + (expense_id,)
            )
            flash("Expense updated successfully.", "success")
            return redirect(url_for("dashboard"))
        except ValueError as exc:
            flash(str(exc), "error")
        except mysql.connector.Error:
            app.logger.exception("Database error while updating expense")
            flash("Could not update the expense. Check your database settings.", "error")
        expense = {**expense, **request.form}
    return render_template("expense_form.html", mode="Edit", expense=expense,
                           categories=CATEGORIES, today=date.today().isoformat())

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    try:
        query_db("DELETE FROM expenses WHERE id = %s", (expense_id,))
        flash("Expense deleted.", "success")
    except mysql.connector.Error:
        app.logger.exception("Database error while deleting expense")
        flash("Could not delete the expense.", "error")
    return redirect(url_for("dashboard"))

@app.errorhandler(mysql.connector.Error)
def database_error(_error):
    return render_template("error.html"), 500

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
