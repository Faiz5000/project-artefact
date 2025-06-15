from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
CORS(app)

auth = HTTPBasicAuth()
users = {
    "test": generate_password_hash("test@123456")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

#utilizing sqlite
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'customers.db')

def init_db():
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()
init_db()

@app.route("/customers", methods=["GET"])
@auth.login_required
def get_customers():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"id": row[0], "name": row[1], "email": row[2], "phone": row[3]} for row in rows])

@app.route("/customers", methods=["POST"])
@auth.login_required
def add_customer():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
              (data["name"], data["email"], data["phone"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Customer added"}), 201

@app.route("/customers/<int:customer_id>", methods=["PUT"])
@auth.login_required
def update_customer(customer_id):
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE customers SET name = ?, email = ?, phone = ? WHERE id = ?",
              (data["name"], data["email"], data["phone"], customer_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Customer updated"})

@app.route("/customers/<int:customer_id>", methods=["DELETE"])
@auth.login_required
def delete_customer(customer_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Customer deleted"})

if __name__ == "__main__":
    app.run(debug=True)


