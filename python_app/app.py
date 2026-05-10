import os
from functools import wraps

from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DB = os.getenv("MONGODB_DB", "tododb")

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
users_collection = db["users"]
tasks_collection = db["tasks"]


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapper


def _parse_object_id(task_id: str):
    try:
        return ObjectId(task_id)
    except Exception:
        return None


def _get_priority_order(priority):
    order = {"high": 0, "medium": 1, "low": 2}
    return order.get(priority, 3)


def _priority_to_number(priority):
    """Convert priority string to number (1=high, 2=medium, 3=low)"""
    mapping = {"high": 1, "medium": 2, "low": 3}
    return mapping.get(priority, 3)


def _priority_select_flags(priority):
    priority = priority or "medium"
    return {
        "selected_low": "selected" if priority == "low" else "",
        "selected_medium": "selected" if priority == "medium" else "",
        "selected_high": "selected" if priority == "high" else "",
    }


@app.route("/")
@login_required
def index():
    username = session["username"]
    tab = request.args.get("tab", "all").lower()
    search = request.args.get("search", "").strip()
    
    # Get all tasks for the user
    query = {"owner": username}
    tasks = list(tasks_collection.find(query).sort("_id", -1))
    
    # Filter by completion status
    if tab == "completed":
        tasks = [t for t in tasks if t.get("status") == "completed"]
    elif tab == "uncompleted":
        tasks = [t for t in tasks if t.get("status") != "completed"]
    
    # Filter by search
    if search:
        tasks = [t for t in tasks if search.lower() in t.get("title", "").lower()]
    
    # Sort by priority
    tasks.sort(key=lambda t: (_get_priority_order(t.get("priority", "low")), t["_id"]))
    
    # Add priority numbers
    for t in tasks:
        t["priority_num"] = _priority_to_number(t.get("priority", "low"))
        # Format date for display: stored as ISO YYYY-MM-DD -> display DD-MM-YYYY
        raw_date = t.get("date", "")
        if raw_date:
            try:
                parsed = datetime.fromisoformat(raw_date)
                t["date"] = parsed.strftime("%d-%m-%Y")
            except Exception:
                # keep raw string if parsing fails
                t["date"] = raw_date
        else:
            t["date"] = "N/A"
    
    return render_template("index.html", tasks=tasks, username=username, tab=tab, search=search)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = users_collection.find_one({"username": username, "password": password})
        if user:
            session["username"] = username
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid username or password")

    if "username" in session:
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/tasks/add", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "low").strip()
        date_str = request.form.get("date", "").strip()

        if not title:
            flash("Task title is required.")
            return render_template(
                "add.html",
                title=title,
                description=description,
                date=date_str,
                **_priority_select_flags(priority),
            )

        if priority not in ["high", "medium", "low"]:
            priority = "low"

        # Validate date (expected format YYYY-MM-DD) and store as ISO string
        date_to_store = ""
        if date_str:
            try:
                parsed = datetime.strptime(date_str, "%Y-%m-%d").date()
                date_to_store = parsed.isoformat()
            except Exception:
                flash("Invalid date format. Use YYYY-MM-DD.")
                return render_template(
                    "add.html",
                    title=title,
                    description=description,
                    date=date_str,
                    **_priority_select_flags(priority),
                )

        tasks_collection.insert_one(
            {
                "title": title,
                "description": description,
                "priority": priority,
                "status": "uncompleted",
                "owner": session["username"],
                "date": date_to_store,
            }
        )
        return redirect(url_for("index"))

    return render_template("add.html", title="", description="", date="", **_priority_select_flags("low"))


@app.route("/tasks/<task_id>")
@login_required
def view_task(task_id):
    object_id = _parse_object_id(task_id)
    if not object_id:
        return "Invalid task id", 400

    task = tasks_collection.find_one({"_id": object_id, "owner": session["username"]})
    if not task:
        return "Task not found", 404

    return render_template("view.html", task=task)


@app.route("/tasks/<task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    object_id = _parse_object_id(task_id)
    if not object_id:
        return "Invalid task id", 400

    task = tasks_collection.find_one({"_id": object_id, "owner": session["username"]})
    if not task:
        return "Task not found", 404

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "medium").strip()
        date_str = request.form.get("date", "").strip()

        if not title:
            flash("Task title is required.")
            form_task = dict(task)
            form_task.update({"title": title, "description": description, "priority": priority})
            form_task.update({"date": date_str})
            return render_template("edit.html", task=form_task, **_priority_select_flags(priority))

        if priority not in ["high", "medium", "low"]:
            priority = "medium"

        # Validate date if provided
        date_to_store = ""
        if date_str:
            try:
                parsed = datetime.strptime(date_str, "%Y-%m-%d").date()
                date_to_store = parsed.isoformat()
            except Exception:
                flash("Invalid date format. Use YYYY-MM-DD.")
                form_task = dict(task)
                form_task.update({"title": title, "description": description, "priority": priority, "date": date_str})
                return render_template("edit.html", task=form_task, **_priority_select_flags(priority))

        update_fields = {"title": title, "description": description, "priority": priority}
        if date_to_store != "":
            update_fields["date"] = date_to_store
        else:
            update_fields["date"] = ""

        tasks_collection.update_one(
            {"_id": object_id, "owner": session["username"]},
            {"$set": update_fields},
        )
        return redirect(url_for("index"))

    return render_template("edit.html", task=task, **_priority_select_flags(task.get("priority")))


@app.route("/tasks/<task_id>/delete")
@login_required
def delete_task(task_id):
    object_id = _parse_object_id(task_id)
    if not object_id:
        return "Invalid task id", 400

    tasks_collection.delete_one({"_id": object_id, "owner": session["username"]})
    return redirect(request.referrer or url_for("index"))


@app.route("/tasks/<task_id>/toggle")
@login_required
def toggle_task(task_id):
    object_id = _parse_object_id(task_id)
    if not object_id:
        return "Invalid task id", 400

    task = tasks_collection.find_one({"_id": object_id, "owner": session["username"]})
    if not task:
        return "Task not found", 404

    new_status = "completed" if task.get("status") != "completed" else "uncompleted"
    tasks_collection.update_one(
        {"_id": object_id, "owner": session["username"]},
        {"$set": {"status": new_status}},
    )
    return redirect(request.referrer or url_for("index"))


@app.route("/health")
def health():
    try:
        client.admin.command("ping")
        return {"status": "ok"}, 200
    except Exception as exc:
        return {"status": "error", "message": str(exc)}, 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
