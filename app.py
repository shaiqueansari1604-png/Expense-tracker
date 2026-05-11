from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "expenses.json"

CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Health", "Entertainment", "Other"]

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

@app.route("/")
def index():
    expenses = load_expenses()
    total = sum(e["amount"] for e in expenses)
    breakdown = {}
    for cat in CATEGORIES:
        cat_total = sum(e["amount"] for e in expenses if e["category"] == cat)
        if cat_total > 0:
            breakdown[cat] = round(cat_total, 2)
    return render_template("index.html",
        expenses=expenses[::-1],
        total=round(total, 2),
        breakdown=breakdown,
        categories=CATEGORIES)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    amount = request.form.get("amount", "0").strip()
    category = request.form.get("category", "Other")
    try:
        amount = round(float(amount), 2)
        if title and amount > 0:
            expenses = load_expenses()
            expenses.append({
                "id": int(datetime.now().timestamp() * 1000),
                "title": title,
                "amount": amount,
                "category": category,
                "date": datetime.now().strftime("%b %d, %Y")
            })
            save_expenses(expenses)
    except ValueError:
        pass
    return redirect(url_for("index"))

@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    expenses = load_expenses()
    expenses = [e for e in expenses if e["id"] != expense_id]
    save_expenses(expenses)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
