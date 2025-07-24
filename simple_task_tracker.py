import datetime
import json
import os
import sys


class Task:
    def __init__(self, id, description, status, created_at, update_at):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.update_at = update_at

    def to_json(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "update_at": self.update_at
        }

    @staticmethod
    def from_json(json_dict):
        return Task (
            id = json_dict["id"],
            description = json_dict["description"],
            status = json_dict["status"],
            created_at = json_dict["created_at"],
            update_at = json_dict["update_at"]
        )


class TaskTracker:
    def __init__(self, storagefile = 'storage.json'):
        self.storagefile = storagefile
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.storagefile):
            return []

        with open(self.storagefile, 'r') as f:
            try:
                data = json.load(f)
                return [Task.from_json(task_data) for task_data in data]
            except json.JSONDecodeError:
                return []

    def save_tasks(self):
        with open(self.storagefile, 'w') as f:
            json.dump([task.to_json() for task in self.tasks], f, indent=4)

    def _get_next_id(self):
        return max((task.id for task in self.tasks),  default=0) + 1

    def _find_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def add_task(self, description):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        task = Task(
            id = self._get_next_id(), # Removed the comma!
            description = description,
            status = 'todo',
            created_at = now,
            update_at = now
        )
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task added succesfully (ID: {task.id})")


    def update_task(self, id, new_description):
        task = self._find_by_id(id)
        if task:
            task.description = new_description
            task.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_tasks()
            print(f"Task updated succesfully (ID: {id})")
        else:
            print(f"Task not found: {id}")

    def delete_task(self, id):
        task = self._find_by_id(id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"Task deleted succesfully (ID: {id})")
        else:
            print(f"Task not found: {id}")

    def mark_in_progress(self, id):
        task = self._find_by_id(id)
        if task:
            task.status = 'in progress'
            task.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_tasks()
            print(f"Task updated succesfully (ID: {id})")
        else:
            print(f"Task not found: {id}")

    def mark_done(self, id):
        task = self._find_by_id(id)
        if task:
            task.status = 'done'
            task.update_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_tasks()
            print(f"Task updated succesfully (ID: {id})")
        else:
            print(f"Task not found: {id}")

    def list_tasks(self, filter_status = None):
        filtered = self.tasks
        if filter_status:
            filtered = [task for task in self.tasks if task.status == filter_status]

        if not filtered:
            print("Tasks no found")
            return

        for task in filtered:
            print(f"[{task.id}]{task.description} | {task.status} | Created: {task.created_at} | Updated: {task.update_at}")


class CLIHandler:
    def __init__(self, task_tracker):
        self.task_tracker = task_tracker

    def handle_command(self, args):
        if not args:
            print("No command provided. Type 'help' for usage.")
            return

        command = args[0]

        if command == "add":
            if len(args) < 2:
                print("Usage: task-cli add \"Task description\"")
                return
            description = " ".join(args[1:])
            self.task_tracker.add_task(description)

        elif command == "update":
            if len(args) < 3:
                print("Usage: task-cli update <id> \"New description\"")
                return
            try:
                task_id = int(args[1])
                new_description = " ".join(args[2:])
                self.task_tracker.update_task(task_id, new_description)
            except ValueError:
                print("Invalid ID format.")

        elif command == "delete":
            if len(args) != 2:
                print("Usage: task-cli delete <id>")
                return
            try:
                task_id = int(args[1])
                self.task_tracker.delete_task(task_id)
            except ValueError:
                print("Invalid ID format.")

        elif command == "mark-in-progress":
            if len(args) != 2:
                print("Usage: task-cli mark-in-progress <id>")
                return
            try:
                task_id = int(args[1])
                self.task_tracker.mark_in_progress(task_id)
            except ValueError:
                print("Invalid ID format.")

        elif command == "mark-done":
            if len(args) != 2:
                print("Usage: task-cli mark-done <id>")
                return
            try:
                task_id = int(args[1])
                self.task_tracker.mark_done(task_id)
            except ValueError:
                print("Invalid ID format.")

        elif command == "list":
            if len(args) == 2:
                status = args[1]
                if status not in ["todo", "done", "in-progress"]:
                    print("Invalid status. Use: todo, done, in-progress.")
                    return
                self.task_tracker.list_tasks(status)
            else:
                self.task_tracker.list_tasks()

        elif command == "help":
            self.print_help()

        else:
            print(f"Unknown command: {command}")
            self.print_help()

    def print_help(self):
        print("""
Available commands:
  add "description"                 Add a new task
  update <id> "new description"     Update an existing task
  delete <id>                       Delete a task
  mark-in-progress <id>             Mark a task as in progress
  mark-done <id>                    Mark a task as done
  list                              List all tasks
  list todo                         List tasks with status 'todo'
  list done                         List tasks with status 'done'
  list in-progress                  List tasks with status 'in-progress'
""")


def main():
    task_tracker = TaskTracker()
    cli = CLIHandler(task_tracker)

    if len(sys.argv) == 1:
        print("🔁 Task Tracker CLI — interactive mode. Type 'help' for commands.")
        while True:
            try:
                user_input = input("task-cli> ").strip()
                if user_input.lower() in ("exit", "quit"):
                    print("Exiting...")
                    break
                if user_input == "":
                    continue
                args = user_input.split()
                cli.handle_command(args)
            except KeyboardInterrupt:
                print("\nInterrupted. Exiting...")
                break
    else:
        cli.handle_command(sys.argv[1:])


if __name__ == "__main__":
    main()