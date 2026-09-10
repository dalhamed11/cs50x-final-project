from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "study-planner-secret-key"


def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def index():
    if "user_id" not in session:
        return render_template("index.html", username=None)

    connection = get_db_connection()

    subjects_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM subjects
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()[0]

    tasks_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()[0]

    completed_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id = ? AND completed = 1
        """,
        (session["user_id"],)
    ).fetchone()[0]

    pending_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id = ? AND completed = 0
        """,
        (session["user_id"],)
    ).fetchone()[0]

    upcoming_tasks = connection.execute(
        """
        SELECT tasks.title,
               tasks.due_date,
               subjects.name AS subject_name
        FROM tasks
        JOIN subjects ON tasks.subject_id = subjects.id
        WHERE tasks.user_id = ?
        AND tasks.completed = 0
        ORDER BY tasks.due_date
        LIMIT 5
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        username=session["username"],
        subjects_count=subjects_count,
        tasks_count=tasks_count,
        completed_count=completed_count,
        pending_count=pending_count,
        upcoming_tasks=upcoming_tasks
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return "يجب تعبئة جميع الحقول"

        if password != confirmation:
            return "كلمتا المرور غير متطابقتين"

        connection = get_db_connection()

        existing_user = connection.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing_user:
            connection.close()
            return "اسم المستخدم موجود مسبقًا"

        password_hash = generate_password_hash(password)

        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password_hash)
        )

        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "يجب تعبئة اسم المستخدم وكلمة المرور"

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if user is None:
            return "اسم المستخدم غير موجود"

        if not check_password_hash(user["password"], password):
            return "كلمة المرور غير صحيحة"

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/subjects", methods=["GET", "POST"])
def subjects():
    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    if request.method == "POST":
        name = request.form.get("name")

        if name:
            connection.execute(
                "INSERT INTO subjects (user_id, name) VALUES (?, ?)",
                (session["user_id"], name)
            )
            connection.commit()

    subjects = connection.execute(
        """
        SELECT *
        FROM subjects
        WHERE user_id = ?
        ORDER BY name
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template("subjects.html", subjects=subjects)


@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    if request.method == "POST":
        title = request.form.get("title")
        subject_id = request.form.get("subject_id")
        due_date = request.form.get("due_date")

        if title and subject_id and due_date:
            connection.execute(
                """
                INSERT INTO tasks (user_id, subject_id, title, due_date)
                VALUES (?, ?, ?, ?)
                """,
                (session["user_id"], subject_id, title, due_date)
            )

            connection.commit()

    subjects = connection.execute(
        """
        SELECT *
        FROM subjects
        WHERE user_id = ?
        ORDER BY name
        """,
        (session["user_id"],)
    ).fetchall()

    filter_status = request.args.get("status", "all")

    if filter_status == "completed":
        tasks = connection.execute(
            """
            SELECT tasks.id,
                   tasks.title,
                   tasks.due_date,
                   tasks.completed,
                   subjects.name AS subject_name
            FROM tasks
            JOIN subjects ON tasks.subject_id = subjects.id
            WHERE tasks.user_id = ?
            AND tasks.completed = 1
            ORDER BY tasks.due_date
            """,
            (session["user_id"],)
        ).fetchall()

    elif filter_status == "pending":
        tasks = connection.execute(
            """
            SELECT tasks.id,
                   tasks.title,
                   tasks.due_date,
                   tasks.completed,
                   subjects.name AS subject_name
            FROM tasks
            JOIN subjects ON tasks.subject_id = subjects.id
            WHERE tasks.user_id = ?
            AND tasks.completed = 0
            ORDER BY tasks.due_date
            """,
            (session["user_id"],)
        ).fetchall()

    else:
        tasks = connection.execute(
            """
            SELECT tasks.id,
                   tasks.title,
                   tasks.due_date,
                   tasks.completed,
                   subjects.name AS subject_name
            FROM tasks
            JOIN subjects ON tasks.subject_id = subjects.id
            WHERE tasks.user_id = ?
            ORDER BY tasks.due_date
            """,
            (session["user_id"],)
        ).fetchall()

    connection.close()

    return render_template(
        "tasks.html",
        subjects=subjects,
        tasks=tasks,
        filter_status=filter_status
    )


@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    connection.execute(
        """
        UPDATE tasks
        SET completed = 1
        WHERE id = ? AND user_id = ?
        """,
        (task_id, session["user_id"])
    )

    connection.commit()
    connection.close()

    return redirect("/tasks")


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    connection.execute(
        """
        DELETE FROM tasks
        WHERE id = ? AND user_id = ?
        """,
        (task_id, session["user_id"])
    )

    connection.commit()
    connection.close()

    return redirect("/tasks")


@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    task = connection.execute(
        """
        SELECT *
        FROM tasks
        WHERE id = ? AND user_id = ?
        """,
        (task_id, session["user_id"])
    ).fetchone()

    if task is None:
        connection.close()
        return "المهمة غير موجودة"

    if request.method == "POST":
        title = request.form.get("title")
        subject_id = request.form.get("subject_id")
        due_date = request.form.get("due_date")

        if not title or not subject_id or not due_date:
            connection.close()
            return "يجب تعبئة جميع الحقول"

        connection.execute(
            """
            UPDATE tasks
            SET title = ?, subject_id = ?, due_date = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                title,
                subject_id,
                due_date,
                task_id,
                session["user_id"]
            )
        )

        connection.commit()
        connection.close()

        return redirect("/tasks")

    subjects = connection.execute(
        """
        SELECT *
        FROM subjects
        WHERE user_id = ?
        ORDER BY name
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template(
        "edit_task.html",
        task=task,
        subjects=subjects
    )


if __name__ == "__main__":
    app.run(debug=True)
