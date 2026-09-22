import sqlite3

DB_NAME = "task_manager.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def setup_db():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            employee_id TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        )
    """)

    con.commit()
    con.close()


def add_employee():
    print("\nAdd Employee")

    emp_id = input("Employee ID: ").strip()
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    department = input("Department: ").strip()

    if not emp_id or not name or not email or not department:
        print("All fields are required.")
        return

    if "@" not in email or "." not in email:
        print("Enter a valid email address.")
        return

    con = connect_db()
    cur = con.cursor()

    try:
        cur.execute(
            "INSERT INTO employees VALUES (?, ?, ?, ?)",
            (emp_id, name, email, department)
        )
        con.commit()
        print("Employee added successfully.")
    except sqlite3.IntegrityError:
        print("Employee ID already exists.")
    finally:
        con.close()


def choose_priority():
    while True:
        print("\nPriority")
        print("1. Low")
        print("2. Medium")
        print("3. High")

        choice = input("Choose priority: ").strip()

        if choice == "1":
            return "Low"
        if choice == "2":
            return "Medium"
        if choice == "3":
            return "High"

        print("Invalid choice.")


def choose_status():
    while True:
        print("\nStatus")
        print("1. Pending")
        print("2. In Progress")
        print("3. Completed")

        choice = input("Choose status: ").strip()

        if choice == "1":
            return "Pending"
        if choice == "2":
            return "In Progress"
        if choice == "3":
            return "Completed"

        print("Invalid choice.")


def employee_exists(emp_id):
    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "SELECT employee_id FROM employees WHERE employee_id = ?",
        (emp_id,)
    )

    row = cur.fetchone()
    con.close()
    return row is not None


def add_task():
    print("\nAdd Task")

    task_id = input("Task ID: ").strip()
    title = input("Task title: ").strip()
    description = input("Description: ").strip()
    emp_id = input("Assigned employee ID: ").strip()

    if not task_id or not title or not emp_id:
        print("Task ID, title and employee ID are required.")
        return

    if not employee_exists(emp_id):
        print("Employee not found.")
        return

    priority = choose_priority()
    status = choose_status()

    con = connect_db()
    cur = con.cursor()

    try:
        cur.execute("""
            INSERT INTO tasks
            (task_id, title, description, employee_id, priority, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            task_id,
            title,
            description,
            emp_id,
            priority,
            status
        ))

        con.commit()
        print("Task added successfully.")
    except sqlite3.IntegrityError:
        print("Task ID already exists.")
    finally:
        con.close()


def show_task(row):
    print(f"\nTask ID: {row[0]}")
    print(f"Title: {row[1]}")
    print(f"Description: {row[2]}")
    print(f"Employee ID: {row[3]}")
    print(f"Priority: {row[4]}")
    print(f"Status: {row[5]}")


def employee_dashboard():
    print("\nEmployee Dashboard")

    emp_id = input("Enter employee ID: ").strip()

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT employee_id, name, email, department
        FROM employees
        WHERE employee_id = ?
    """, (emp_id,))

    emp = cur.fetchone()

    if not emp:
        print("Employee not found.")
        con.close()
        return

    cur.execute("""
        SELECT task_id, title, description, employee_id, priority, status
        FROM tasks
        WHERE employee_id = ?
    """, (emp_id,))

    rows = cur.fetchall()

    completed = 0
    pending = 0

    for row in rows:
        if row[5] == "Completed":
            completed += 1
        elif row[5] == "Pending":
            pending += 1

    print(f"\nName: {emp[1]}")
    print(f"Department: {emp[3]}")
    print(f"Total tasks: {len(rows)}")
    print(f"Completed tasks: {completed}")
    print(f"Pending tasks: {pending}")

    if not rows:
        print("No tasks assigned.")
    else:
        print("\nAssigned Tasks")
        for row in rows:
            show_task(row)

    con.close()


def admin_dashboard():
    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM employees")
    total_employees = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Pending'")
    pending = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
    completed = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE status = 'Pending' AND priority = 'High'
    """)
    high_pending = cur.fetchone()[0]

    print("\nAdmin Dashboard")
    print(f"Total employees: {total_employees}")
    print(f"Total tasks: {total_tasks}")
    print(f"Pending tasks: {pending}")
    print(f"Completed tasks: {completed}")
    print(f"High-priority pending tasks: {high_pending}")

    con.close()


def search_employee():
    print("\nSearch Employee")

    text = input("Enter employee ID or name: ").strip()

    if not text:
        print("Enter a search value.")
        return

    con = connect_db()
    cur = con.cursor()

    like_text = f"%{text}%"

    cur.execute("""
        SELECT employee_id, name, email, department
        FROM employees
        WHERE employee_id LIKE ? OR name LIKE ?
        ORDER BY name
    """, (like_text, like_text))

    rows = cur.fetchall()

    if not rows:
        print("No employee found.")
    else:
        for row in rows:
            print(f"\nEmployee ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Email: {row[2]}")
            print(f"Department: {row[3]}")

    con.close()


def filter_tasks():
    print("\nFilter Tasks")

    print("\nStatus")
    print("0. Any")
    print("1. Pending")
    print("2. In Progress")
    print("3. Completed")

    status_choice = input("Choose status: ").strip()

    status_map = {
        "0": None,
        "1": "Pending",
        "2": "In Progress",
        "3": "Completed"
    }

    if status_choice not in status_map:
        print("Invalid status choice.")
        return

    print("\nPriority")
    print("0. Any")
    print("1. Low")
    print("2. Medium")
    print("3. High")

    priority_choice = input("Choose priority: ").strip()

    priority_map = {
        "0": None,
        "1": "Low",
        "2": "Medium",
        "3": "High"
    }

    if priority_choice not in priority_map:
        print("Invalid priority choice.")
        return

    status = status_map[status_choice]
    priority = priority_map[priority_choice]

    query = """
        SELECT task_id, title, description, employee_id, priority, status
        FROM tasks
        WHERE 1 = 1
    """

    values = []

    if status:
        query += " AND status = ?"
        values.append(status)

    if priority:
        query += " AND priority = ?"
        values.append(priority)

    query += " ORDER BY task_id"

    con = connect_db()
    cur = con.cursor()
    cur.execute(query, values)

    rows = cur.fetchall()

    if not rows:
        print("No matching tasks found.")
    else:
        for row in rows:
            show_task(row)

    con.close()


def view_employees():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT employee_id, name, email, department
        FROM employees
        ORDER BY employee_id
    """)

    rows = cur.fetchall()

    print("\nAll Employees")

    if not rows:
        print("No employees found.")
    else:
        for row in rows:
            print(f"\nEmployee ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Email: {row[2]}")
            print(f"Department: {row[3]}")

    con.close()


def view_tasks():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT task_id, title, description, employee_id, priority, status
        FROM tasks
        ORDER BY task_id
    """)

    rows = cur.fetchall()

    print("\nAll Tasks")

    if not rows:
        print("No tasks found.")
    else:
        for row in rows:
            show_task(row)

    con.close()


def update_task_status():
    print("\nUpdate Task Status")

    task_id = input("Enter task ID: ").strip()

    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "SELECT task_id, title, status FROM tasks WHERE task_id = ?",
        (task_id,)
    )

    row = cur.fetchone()

    if not row:
        print("Task not found.")
        con.close()
        return

    print(f"Task: {row[1]}")
    print(f"Current status: {row[2]}")

    new_status = choose_status()

    cur.execute(
        "UPDATE tasks SET status = ? WHERE task_id = ?",
        (new_status, task_id)
    )

    con.commit()
    con.close()

    print("Task status updated successfully.")


def menu():
    while True:
        print("\nEmployee Task Management System")
        print("1. Add Employee")
        print("2. Add Task")
        print("3. Employee Dashboard")
        print("4. Admin Dashboard")
        print("5. Search Employee")
        print("6. Filter Tasks")
        print("7. View All Employees")
        print("8. View All Tasks")
        print("9. Update Task Status")
        print("0. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            add_employee()
        elif choice == "2":
            add_task()
        elif choice == "3":
            employee_dashboard()
        elif choice == "4":
            admin_dashboard()
        elif choice == "5":
            search_employee()
        elif choice == "6":
            filter_tasks()
        elif choice == "7":
            view_employees()
        elif choice == "8":
            view_tasks()
        elif choice == "9":
            update_task_status()
        elif choice == "0":
            print("Program closed.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    setup_db()
    menu()
