# Employee Task Management System

A small command-line Python application for managing employees and their tasks.

## Technology

* Python 3
* SQLite
* Python built-in `sqlite3` module

No external package is required.

## Features

The application supports:

* Add an employee
* Add a task
* Assign a task to an employee
* Set task priority as Low, Medium, or High
* Set task status as Pending, In Progress, or Completed
* Employee dashboard
* Admin dashboard
* Search employee by ID or name
* Filter tasks by status and priority
* View all employees
* View all tasks
* Update task status

## Database

The program automatically creates:

`task\_manager.db`

The database contains two tables:

* `employees`
* `tasks`

You do not need to create the database manually.

## Project Files

```text
employee\_task\_manager/
    app.py
    README.md
    .gitignore
```

The SQLite database file will appear after running the program.

## How to Run

Open a terminal in the project folder.

Run:

```bash
python app.py
```

If your system uses `python3`, run:

```bash
python3 app.py
```

## Example Test Data

Employee 1:

```text
Employee ID: E101
Name: Madhav Kumar
Email: madhav@gmail.com
Department: IT
```

Employee 2:

```text
Employee ID: E102
Name: Rahul Sharma
Email: rahul@gmail.com
Department: HR
```

Task 1:

```text
Task ID: T101
Task title: Prepare monthly report
Description: Prepare employee performance report
Assigned employee ID: E101
Priority: High
Status: Pending
```

Task 2:

```text
Task ID: T102
Task title: Fix login issue
Description: Check and fix login page error
Assigned employee ID: E101
Priority: Medium
Status: In Progress
```

Task 3:

```text
Task ID: T103
Task title: Update employee records
Description: Update employee information in system
Assigned employee ID: E102
Priority: Low
Status: Completed
```

Task 4:

```text
Task ID: T104
Task title: Database backup
Description: Create backup of employee database
Assigned employee ID: E101
Priority: High
Status: Pending
```

## Suggested Screenshots

For submission, useful screenshots are:

1. Main menu
2. Employee added successfully
3. Task added successfully
4. Employee dashboard
5. Admin dashboard
6. Search employee result
7. Filtered task result

## Notes

The database is stored locally in `task\_manager.db`.

If you want to start again with an empty database, close the program and delete `task\_manager.db`. The application will create a fresh database on the next run.

