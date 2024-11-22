import sqlite3
from colorama import Fore, Style

DB_NAME = "tasks.db"

def create_database():
    """
    Creates the tasks table if it doesn't already exist.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_task(name):
    """
    Adds a new task to the database.
    Args:
        name (str): The name of the task.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, completed) VALUES (?, ?)", (name, False))
    conn.commit()
    conn.close()

def list_tasks():
    """
    Fetches and displays all tasks from the database.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    print("\nTasks:")
    for task in tasks:
        if task[2]:
            status = f"{Fore.GREEN}[X]{Style.RESET_ALL}"  # Green for completed
        else:
            status = "[ ]"  # White for incomplete
        print(f"{task[0]}. {status} {task[1]}")
    print()

def mark_task_completed(task_id):
    """
    Marks a task as completed in the database.
    Args:
        task_id (int): The ID of the task to mark as completed.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"Task {task_id} marked as completed!")

def delete_task(task_id):
    """
    Deletes a task from the database.
    Args:
        task_id (int): The ID of the task to delete.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"Task {task_id} deleted!")

def main():
    """
    Main function to manage the task list.
    """
    create_database()

    while True:
        print("\nOptions:")
        print("1. Add a new task")
        print("2. List all tasks")
        print("3. Mark a task as completed")
        print("4. Delete a task")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            task_name = input("Enter the task name: ")
            add_task(task_name)
            print(f"Task '{task_name}' added!")
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            list_tasks()
            try:
                task_id = int(input("Enter the task ID to mark as completed: "))
                mark_task_completed(task_id)
            except ValueError:
                print("Invalid input. Please enter a valid task ID.")
        elif choice == "4":
            list_tasks()
            try:
                task_id = int(input("Enter the task ID to delete: "))
                delete_task(task_id)
            except ValueError:
                print("Invalid input. Please enter a valid task ID.")
        elif choice == "5":
            print("Exiting the task manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
