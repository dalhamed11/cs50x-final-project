# Design Document - Study Planner

## Overview

Study Planner is a web application designed to help students organize
their subjects and academic tasks in one place.

Users can create an account, log in, add subjects, create tasks, set
due dates, mark tasks as completed, edit tasks, delete tasks, and filter
tasks by completion status.

## Files

### app.py

This is the main Python file.

It contains the Flask application, routes, database operations,
user authentication, session management, and task management.

### database.db

This is the SQLite database used by the application.

It stores:

- Users
- Subjects
- Tasks

### templates/

This directory contains the HTML templates.

The main pages include:

- index.html
- login.html
- register.html
- subjects.html
- tasks.html
- edit_task.html
- layout.html

### static/

This directory contains the CSS files used to style the application.

## Database Design

The application uses three main tables.

### users

Stores information about registered users.

Important columns:

- id
- username
- password

### subjects

Stores the subjects created by users.

Important columns:

- id
- user_id
- name

Each subject belongs to a specific user.

### tasks

Stores the tasks created by users.

Important columns:

- id
- user_id
- subject_id
- title
- due_date
- completed

Each task belongs to a specific user and subject.

## User Authentication

Users can register with a username and password.

Passwords are not stored as plain text. Flask Werkzeug is used to
hash passwords before storing them in the database.

After logging in, the user's ID and username are stored in a Flask session.

The application uses the session to make sure users can only access
their own subjects and tasks.

## Task Management

Users can create tasks by providing:

- Task title
- Subject
- Due date

Users can also:

- View tasks
- Edit tasks
- Delete tasks
- Mark tasks as completed

Tasks can be filtered into:

- All tasks
- Pending tasks
- Completed tasks

## Dashboard

The homepage contains a dashboard showing:

- Number of subjects
- Number of tasks
- Number of completed tasks
- Number of pending tasks
- Upcoming tasks

The dashboard helps users quickly understand their current workload.

## Design Decisions

I chose Flask because it provides a simple way to build a web
application using Python.

I chose SQLite because it is lightweight and does not require a
separate database server.

I used Jinja templates to connect the Python backend with the HTML
pages.

I used sessions to keep users logged in between requests.

The application separates HTML templates, CSS files, Python logic,
and database data to keep the project organized.

## Future Improvements

Possible future improvements include:

- Task priorities
- Calendar view
- Search
- Progress charts
- Notifications
- Recurring tasks
- More customization options
