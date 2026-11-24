import os
from datetime import date
from decimal import Decimal, InvalidOperation
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from mysql.connector import Error, IntegrityError
from database import get_db_connection, fetch_all, fetch_one

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-this-secret")

# This is the website's data dictionary. It mirrors the six tables in the
# supplied Gadget_renting.sql file. Only these whitelisted identifiers are
# used to construct SQL statements.
TABLES = {
    "customers": {
        "title": "Customers", "table": "Customers", "pk": "customer_id",
        "fields": [
            ("customer_name", "Customer name", "text", True),
            ("phone", "Phone", "tel", False),
            ("email", "Email", "email", False),
            ("address", "Address", "text", False),
        ],
    },
    "gadgets": {
        "title": "Gadgets", "table": "Gadgets", "pk": "gadget_id",
        "fields": [
            ("gadget_name", "Gadget name", "text", True),
            ("category", "Category", "text", False),
            ("brand", "Brand", "text", False),
            ("rent_per_day", "Rent per day", "number", True),
            ("availability_status", "Availability", "select:Available|Rented|Maintenance", False),
        ],
    },
    "rentals": {
        "title": "Rentals", "table": "Rentals", "pk": "rental_id",
        "fields": [
            ("customer_id", "Customer ID", "number", True),
            ("gadget_id", "Gadget ID", "number", True),
            ("start_date", "Start date", "date", True),
            ("end_date", "End date", "date", True),
            ("total_amount", "Total amount", "number", True),
            ("rental_status", "Rental status", "select:Active|Completed|Cancelled", False),
        ],
    },
    "payments": {
        "title": "Payments", "table": "Payments", "pk": "payment_id",
        "fields": [
            ("rental_id", "Rental ID", "number", True),
            ("amount", "Amount", "number", True),
            ("payment_date", "Payment date", "date", False),
            ("payment_method", "Payment method", "select:UPI|Cash|Card|Net Banking|Other", False),
        ],
    },
    "returns": {
        "title": "Returns", "table": "Returns", "pk": "return_id",
        "fields": [
            ("rental_id", "Rental ID", "number", True),
            ("return_date", "Return date", "date", True),
            ("gadget_condition", "Gadget condition", "select:Good|Damaged|Needs Repair", False),
        ],
    },
    "maintenance": {
        "title": "Maintenance", "table": "Maintenance", "pk": "maintenance_id",
        "fields": [
            ("gadget_id", "Gadget ID", "number", True),
            ("issue_description", "Issue description", "textarea", False),
            ("repair_cost", "Repair cost", "number", False),
            ("repair_status", "Repair status", "select:Pending|In Progress|Completed", False),
        ],
    },
}

def get_table(key):
    item = TABLES.get(key)
    if not item:
        abort(404)
    return item

def read_form_value(field_type, raw):
    if raw == "":
        return None
    if field_type == "number":
        try:
            return Decimal(raw)
        except InvalidOperation:
            raise ValueError("Please enter a valid number.")
    if field_type == "date":
        try:
            return date.fromisoformat(raw)
        except ValueError:
            raise ValueError("Please enter a valid date.")
    return raw.strip()

def dashboard_data():
    # The metrics are based on the user's existing table and column names.
    return {
        "customers": fetch_one("SELECT COUNT(*) AS total FROM Customers")["total"],
        "gadgets": fetch_one("SELECT COUNT(*) AS total FROM Gadgets")["total"],
        "available": fetch_one("SELECT COUNT(*) AS total FROM Gadgets WHERE availability_status = 'Available'")["total"],
        "active_rentals": fetch_one("SELECT COUNT(*) AS total FROM Rentals WHERE rental_status = 'Active'")["total"],
        "revenue": fetch_one("SELECT COALESCE(SUM(amount), 0) AS total FROM Payments")["total"],
        "recent_rentals": fetch_all("""
            SELECT r.rental_id, c.customer_name, g.gadget_name,
                   r.start_date, r.end_date, r.total_amount, r.rental_status
            FROM Rentals r
            JOIN Customers c ON c.customer_id = r.customer_id
            JOIN Gadgets g ON g.gadget_id = r.gadget_id
            ORDER BY r.rental_id DESC LIMIT 8
        """),
        "category_counts": fetch_all("""
            SELECT category, COUNT(*) AS total
            FROM Gadgets GROUP BY category ORDER BY total DESC
        """),
    }

@app.get("/health")
def health():
    try:
        row = fetch_one("SELECT 1 AS ok")
        return {"status": "ok", "database": bool(row and row["ok"] == 1)}, 200
    except Error:
        return {"status": "error", "database": False}, 503

@app.get("/")
def dashboard():
    try:
        return render_template("dashboard.html", metrics=dashboard_data())
    except Error as exc:
        app.logger.exception("Dashboard database query failed")
        return render_template("database_error.html", error=str(exc)), 503

@app.get("/<key>")
def list_records(key):
    item = get_table(key)
    try:
        rows = fetch_all(f"SELECT * FROM {item['table']} ORDER BY {item['pk']} DESC")
        columns = [item["pk"]] + [field[0] for field in item["fields"]]
        return render_template("list.html", item=item, key=key, rows=rows, columns=columns)
    except Error as exc:
        app.logger.exception("List query failed")
        flash(f"Could not load {item['title']}: {exc}", "danger")
        return redirect(url_for("dashboard"))

@app.route("/<key>/new", methods=["GET", "POST"])
def create_record(key):
    item = get_table(key)
    if request.method == "POST":
        try:
            columns, values = [], []
            for name, label, field_type, required in item["fields"]:
                raw = request.form.get(name, "").strip()
                if required and not raw:
                    raise ValueError(f"{label} is required.")
                columns.append(name)
                values.append(read_form_value(field_type, raw))
            placeholders = ", ".join(["%s"] * len(columns))
            sql = f"INSERT INTO {item['table']} ({', '.join(columns)}) VALUES ({placeholders})"
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute(sql, values)
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cur.close()
                conn.close()
            flash(f"{item['title']} record created successfully.", "success")
            return redirect(url_for("list_records", key=key))
        except (ValueError, Error) as exc:
            flash(str(exc), "danger")
    return render_template("form.html", item=item, key=key, record=None, mode="Create")

@app.route("/<key>/<int:record_id>/edit", methods=["GET", "POST"])
def edit_record(key, record_id):
    item = get_table(key)
    try:
        record = fetch_one(f"SELECT * FROM {item['table']} WHERE {item['pk']} = %s", (record_id,))
        if not record:
            abort(404)
        if request.method == "POST":
            assignments, values = [], []
            for name, label, field_type, required in item["fields"]:
                raw = request.form.get(name, "").strip()
                if required and not raw:
                    raise ValueError(f"{label} is required.")
                assignments.append(f"{name} = %s")
                values.append(read_form_value(field_type, raw))
            values.append(record_id)
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute(
                    f"UPDATE {item['table']} SET {', '.join(assignments)} WHERE {item['pk']} = %s",
                    values
                )
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cur.close()
                conn.close()
            flash(f"{item['title']} record updated successfully.", "success")
            return redirect(url_for("list_records", key=key))
        return render_template("form.html", item=item, key=key, record=record, mode="Edit")
    except (ValueError, Error) as exc:
        flash(str(exc), "danger")
        return render_template("form.html", item=item, key=key, record=record, mode="Edit")

@app.post("/<key>/<int:record_id>/delete")
def delete_record(key, record_id):
    item = get_table(key)
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {item['table']} WHERE {item['pk']} = %s", (record_id,))
        conn.commit()
        flash("Record deleted." if cur.rowcount else "Record was not found.", "success")
        cur.close()
    except IntegrityError:
        if conn:
            conn.rollback()
        flash("This record is referenced by another table. Remove or update dependent records first.", "danger")
    except Error as exc:
        if conn:
            conn.rollback()
        flash(f"Database error: {exc}", "danger")
    finally:
        if conn:
            conn.close()
    return redirect(url_for("list_records", key=key))

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(_error):
    return render_template("500.html"), 500

if __name__ == "__main__":
    # Local development only. Render starts the app with Gunicorn.
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=True)
