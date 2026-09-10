# Study Planner

#### Video Demo: https://youtu.be/Z0VDWpQBOH4

#### Description:

Study Planner is a web application designed to help students organize their academic work in one place. The application allows users to manage their subjects and tasks, set due dates, track completed work, and view upcoming tasks from a simple dashboard.

The application was built using Python, Flask, SQLite, SQL, HTML, CSS, and Jinja templates. Flask is used to handle the web application and its routes, while SQLite is used as the database for storing users, subjects, and tasks.

Users can create an account and log in securely. The application uses Flask sessions to keep track of the currently logged-in user. Passwords are stored securely using password hashing rather than storing them as plain text.

After logging in, users can create and manage their subjects. They can also create tasks and associate each task with a subject and a due date. Tasks can be edited, deleted, and marked as completed.

The task page allows users to filter their tasks according to their status. They can view all tasks, only pending tasks, or only completed tasks. This makes it easier for students to focus on the work that still needs to be completed.

The dashboard provides an overview of the user's academic workload. It displays information about subjects, tasks, completed tasks, pending tasks, and upcoming deadlines.

The project separates the application into different components. The Python code in `app.py` contains the Flask application, routes, authentication logic, session handling, and database operations. The `database.db` file stores the application's data using SQLite. The files in the `templates` directory contain the HTML pages rendered by Flask and Jinja. The files in the `static` directory contain the CSS used to style the application. The `requirements.txt` file lists the Python dependencies required to run the project.

I chose Flask because it provides a straightforward way to build a web application with Python. I chose SQLite because it is lightweight and works well for a project of this size without requiring a separate database server. I used separate templates and static files to keep the project organized and make the application easier to maintain.

One of the main goals of Study Planner was to create a practical application that solves a real problem for students. Instead of keeping assignments and deadlines in different places, users can manage their academic tasks through one application.

In the future, the application could be expanded with features such as task priorities, a calendar view, search functionality, progress charts, notifications, recurring tasks, and additional customization options.
