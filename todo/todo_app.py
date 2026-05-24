import os

TODO_FILE = 'tasks.txt'

def load_tasks():
    if not os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'w') as f:
            pass # Create the file if it doesn't exist
    with open(TODO_FILE, 'r') as f:
        tasks = [line.strip() for line in f if line.strip()]
    return tasks

def save_tasks(tasks):
    with open(TODO_FILE, 'w') as f:
        for task in tasks:
            f.write(task + '\n')

def display_tasks(tasks):
    if not tasks:
        print("No tasks in the todo list.")
        return
    print("\n--- Your Todo List ---")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print("----------------------")

def add_task(task, tasks):
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{task}' added.")

def remove_task(task_number, tasks):
    try:
        task_index = int(task_number) - 1
        if 0 <= task_index < len(tasks):
            removed_task = tasks.pop(task_index)
            save_tasks(tasks)
            print(f"Task '{removed_task}' removed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    tasks = load_tasks()
    while True:
        display_tasks(tasks)
        print("\nCommands: add <task>, remove <number>, list, exit")
        command_line = input("Enter command: ").strip()
        parts = command_line.split(' ', 1)
        command = parts[0].lower()

        if command == 'add':
            if len(parts) > 1:
                add_task(parts[1], tasks)
            else:
                print("Usage: add <task>")
        elif command == 'remove':
            if len(parts) > 1:
                remove_task(parts[1], tasks)
            else:
                print("Usage: remove <number>")
        elif command == 'list':
            pass # Tasks are displayed at the beginning of each loop
        elif command == 'exit':
            print("Exiting todo app. Goodbye!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
