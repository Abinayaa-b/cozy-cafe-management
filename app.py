from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "cozy_cafe_secret_key_2024"

# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db()
    cur = conn.cursor()

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # Default users
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users VALUES (NULL,'owner','owner123','owner')")
        cur.execute("INSERT INTO users VALUES (NULL,'staff','staff123','staff')")

    # Menu
    cur.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        price INTEGER,
        available TEXT
    )
    """)

    # Orders
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_no TEXT,
        item_name TEXT,
        quantity INTEGER,
        total INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

# ---------- ROUTES ----------
@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    u = request.form["username"]
    p = request.form["password"]

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (u, p)
    ).fetchone()
    conn.close()

    if user:
        session["role"] = user["role"]
        session["username"] = user["username"]
        return redirect("/dashboard")
    
    return render_template("login.html", error="Invalid login")

@app.route("/dashboard")
def dashboard():
    if "role" not in session:
        return redirect("/")
    
    if session["role"] == "owner":
        return render_template("admin_dashboard.html")
    else:
        return render_template("staff_dashboard.html")

@app.route("/menu")
def menu():
    if "role" not in session:
        return redirect("/")
    
    conn = get_db()
    items = conn.execute("SELECT * FROM menu").fetchall()
    conn.close()
    return render_template("menu.html", items=items, role=session.get("role"))

@app.route("/toggle_availability/<int:item_id>")
def toggle_availability(item_id):
    if session.get("role") != "owner":
        return redirect("/menu")
    
    conn = get_db()
    item = conn.execute("SELECT available FROM menu WHERE id=?", (item_id,)).fetchone()
    
    new_status = "No" if item["available"] == "Yes" else "Yes"
    conn.execute("UPDATE menu SET available=? WHERE id=?", (new_status, item_id))
    conn.commit()
    conn.close()
    
    return redirect("/menu")

@app.route("/order", methods=["GET", "POST"])
def order():
    if "role" not in session:
        return redirect("/")
    
    conn = get_db()
    items = conn.execute(
        "SELECT * FROM menu WHERE available='Yes'"
    ).fetchall()

    if request.method == "POST":
        table_no = request.form["table_no"]
        item = request.form["item"]
        qty = int(request.form["quantity"])

        price = conn.execute(
            "SELECT price FROM menu WHERE item_name=?",
            (item,)
        ).fetchone()["price"]

        total = price * qty
        time = datetime.now().strftime("%d-%m-%Y %H:%M")

        conn.execute(
            "INSERT INTO orders VALUES (NULL,?,?,?,?,?)",
            (table_no, item, qty, total, time)
        )
        conn.commit()
        conn.close()
        return redirect("/orders")

    conn.close()
    return render_template("order.html", items=items)

@app.route("/orders")
def view_orders():
    if "role" not in session:
        return redirect("/")
    
    conn = get_db()
    orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("orders.html", orders=orders)

@app.route("/bill/<int:order_id>")
def bill(order_id):
    if "role" not in session:
        return redirect("/")
    
    conn = get_db()
    order = conn.execute(
        "SELECT * FROM orders WHERE id=?",
        (order_id,)
    ).fetchone()
    conn.close()
    return render_template("bill.html", order=order)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)