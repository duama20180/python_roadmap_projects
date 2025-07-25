import os
import sys
from datetime import datetime
import json

class Expense:
    def __init__(self, id, date, description, amount):
        self.id = id
        self.date = date
        self.description = description
        self.amount = amount

    def to_json(self):
        return  {
            'id': self.id,
            'date': self.date,
            'description': self.description,
            'amount': self.amount
        }

    @staticmethod
    def from_json(data):
        return Expense(id = data['id'],
                       date = data['date'],
                       description = data['description'],
                       amount = data['amount']
                       )

class ExpenseTracker:
    def __init__(self, storagefile = 'expenses.json'):
        self.storagefile = storagefile
        self.expenses = self.load_expenses()

    def load_expenses(self):
        if not os.path.isfile(self.storagefile):
            return []

        with open(self.storagefile, 'r') as f:
            try:
                data = json.load(f)
                return [Expense.from_json(expense) for expense in data]
            except json.JSONDecodeError:
                return []

    def save_expenses(self):
        with open(self.storagefile, 'w') as f:
            json.dump([expense.to_json() for expense in self.expenses], f, indent=4)

    def _get_next_id(self):
        return max((expense.id for expense in self.expenses), default=0) + 1

    def _find_by_id(self, expense_id):
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None

    def add_expense(self, description, amount):
        expense = Expense(
            id = self._get_next_id(),
            date = datetime.now().strftime('%Y-%m-%d'),
            description = description,
            amount = float(amount)
        )
        self.expenses.append(expense)
        self.save_expenses()
        print(f"expense successfully added")

    def update_expense(self, id, description, amount):
        expense = self._find_by_id(id)
        if expense:
            expense.description = description
            expense.amount = float(amount)
            self.save_expenses()
            print(f"Expense successfully updated")
        else:
            print(f"Expense not found")

    def view_expenses(self, category_status = None):

        filtered = self.expenses

        if category_status:
            filtered = [expense for expense in filtered if expense.description == category_status]

        if not filtered:
            print("No expenses found")
            return

        for expense in filtered:
            print(f"{expense.id}: {expense.date}| {expense.description} | {expense.amount}")

    def delete_expense(self, id):
        expense = self._find_by_id(id)
        if expense:
            self.expenses.remove(expense)
            self.save_expenses()
            print(f"Expense successfully deleted")
        else:
            print(f"Expense not found")

    def summarize_expenses(self, chosen_month=None):
        all_expenses = self.expenses

        if not all_expenses:
            print("No expenses found")
            return

        total = 0.0

        for expense in all_expenses:
            try:
                date_obj = datetime.strptime(expense.date, '%Y-%m-%d')
                amount = float(expense.amount)
            except (ValueError, TypeError):
                continue

            if chosen_month:
                if date_obj.strftime('%m') == chosen_month and date_obj.strftime('%Y') == datetime.now().strftime('%Y'):
                    total += amount
            else:
                total += amount

        print(f"Total expenses value: {total}")

class CLIHandler:
    def __init__(self, expense_tracker):
        self.expense_tracker = expense_tracker
        self.commands = {
            "add" : self._add_expense,
            "update" : self._update_expense,
            "delete" : self._delete_expense,
            "view" : self._view_expenses,
            "summarize" : self._summarize_expenses,
            "help" : self._print_help,
        }

    @staticmethod
    def _get_id_from_args (args, usage_message):
        if not args:
            print(usage_message)
            return
        try:
            return int(args[0])
        except ValueError:
            print("Invalid ID format")
            return None

    @staticmethod
    def _parse_description_and_amount(args):
        if len(args) < 2:
            return None, None

        *description_parts, amount_str = args
        description = " ".join(description_parts)
        return description, amount_str

    def handle_command(self, args):
        if not args:
            print("No command provided. Type 'help' for a list of commands.")
            return

        command = args[0].lower() # Convert command to lowercase
        handler = self.commands.get(command)

        if handler:
            handler(args[1:]) # Pass the rest of the arguments to the handler
        else:
            print(f"Unknown command: '{command}'. Type 'help' for usage.")
            self._print_help()

    def _add_expense(self, args):
        description, amount_str = self._parse_description_and_amount(args)

        if description is None or amount_str is None:
            print("Usage: add \"<description>\" <amount>")
            print("Example: add \"Groceries\" 50.00")
            return

        self.expense_tracker.add_expense(description, amount_str)

    def _update_expense(self, args):
        if len(args) < 2:  # At least ID and something else
            print("Usage: update <id> \"<new description>\" <new amount>")
            print("Example: update 1 \"New Description\" 75.50")
            return

        expense_id = self._get_id_from_args([args[0]], "Usage: update <id> \"<new description>\" <new amount>")
        if expense_id is None:
            return

        description, amount_str = self._parse_description_and_amount(args[1:])  # Pass remaining args for desc/amount

        if description is None or amount_str is None:
            print("Usage: update <id> \"<new description>\" <new amount>")
            print("Example: update 1 \"New Description\" 75.50")
            return

        self.expense_tracker.update_expense(expense_id, description, amount_str)

    def _view_expenses(self, args):
        if len(args) == 1:
            category = args[0]
            self.expense_tracker.view_expenses(category)
        elif not args:
            self.expense_tracker.view_expenses()
        else:
            print("Usage: view [category]")
            print("Example: view Groceries")

    def _delete_expense(self, args):
        expense_id = self._get_id_from_args(args, "Usage: delete <id>")
        if expense_id is None:
            return
        self.expense_tracker.delete_expense(expense_id)

    def _summarize_expenses(self, args):
        if len(args) == 1:
            month = args[0]
            self.expense_tracker.summarize_expenses(month)
        elif not args:
            self.expense_tracker.summarize_expenses()
        else:
            print("Usage: summarize [month_number]")
            print("Example: summarize 07 (for July)")

    def _print_help(self, args = None):
        print("""
--- Expense Tracker Commands ---
  add "<description>" <amount>   - Add a new expense.
                                     Example: add "Dinner with friends" 45.75
  update <id> "<new description>" <new amount> - Update an existing expense.
                                     Example: update 3 "Coffee" 3.50
  view [category]                - View all expenses, or filter by category.
                                     Example: view or view Groceries
  delete <id>                    - Delete an expense by its ID.
                                     Example: delete 5
  summarize [month_number]       - Show total expenses (all or for a specific month).
                                     Example: summarize 07 (for July)
  help                           - Show this help message.
  exit/quit                      - Exit the application.
--------------------------------
        """)


def main():
    expense_tracker = ExpenseTracker()
    cli = CLIHandler(expense_tracker)

    if len(sys.argv) == 1:
        print("Enter your commands to proceed:")
        cli._print_help()
        while True:
            try:
                user_input = input("expense-tracker> ").strip()
                if user_input.lower() in ("exit", "quit"):
                    print("Exiting Expense Tracker")
                    break
                if user_input == "":
                    continue

                args = user_input.split()
                cli.handle_command(args)

            except ValueError as e:
                print(f"Error parsing input: {e}")
                continue
            except KeyboardInterrupt:
                print("\nInterrupted. Exiting Expense Tracker. Goodbye!")
                break
    else:
        try:
            full_command_string = " ".join(sys.argv[1:])
            parsed_args = full_command_string.split()
            cli.handle_command(parsed_args)

        except ValueError as e:
            print(f"Error parsing command line arguments: {e}")
            print("Ensure quoted arguments are correctly closed.")

if __name__ == '__main__':
    main()