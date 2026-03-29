import json
from pathlib import Path

STORAGE_FILE = Path(__file__).resolve().parent / "todo_store.json"


def load_tasks():
    if STORAGE_FILE.exists():
        try:
            with STORAGE_FILE.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_tasks(tasks):
    try:
        with STORAGE_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2, ensure_ascii=False)
    except OSError:
        print("Error: unable to save todo list.")


def list_tasks(tasks):
    if not tasks:
        print("No tasks in your todo list.")
        return

    print("\nYour todo list:")
    for index, task in enumerate(tasks, start=1):
        print(f" {index}. {task}")
    print()


def add_task(tasks, task_text):
    task_text = task_text.strip()
    if not task_text:
        print("Please provide a task to add.")
        return

    tasks.append(task_text)
    save_tasks(tasks)
    print(f"Added: {task_text}")


def remove_task(tasks, token):
    token = token.strip()
    if not token:
        print("Please provide the number of the task to remove.")
        return

    if not token.isdigit():
        print("Please use the task number to remove a task.")
        return

    index = int(token) - 1
    if index < 0 or index >= len(tasks):
        print("Task number out of range.")
        return

    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Removed: {removed}")


def show_help():
    print(
        "\nCommands:\n"
        "  add <task>       - Add a new task\n"
        "  remove <number>  - Remove a completed task by its number\n"
        "  list             - Show current tasks\n"
        "  clear            - Remove all tasks\n"
        "  help             - Show this message\n"
        "  exit             - Quit the script\n"
    )


def main():
    tasks = load_tasks()

    print("Simple Todo Script")
    print("Type 'help' for commands.")

    while True:
        command = input("todo> ").strip()
        if not command:
            continue

        parts = command.split(maxsplit=1)
        action = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""

        if action in {"add", "a"}:
            add_task(tasks, argument)
        elif action in {"remove", "rm", "done", "del"}:
            remove_task(tasks, argument)
        elif action in {"list", "ls"}:
            list_tasks(tasks)
        elif action == "clear":
            tasks.clear()
            save_tasks(tasks)
            print("All tasks cleared.")
        elif action in {"help", "h", "?"}:
            show_help()
        elif action in {"exit", "quit", "q"}:
            print("Goodbye!")
            break
        else:
            add_task(tasks, command)


if __name__ == "__main__":
    main()