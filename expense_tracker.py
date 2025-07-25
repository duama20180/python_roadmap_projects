import json
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
            return {}

        with open(self.storagefile, 'r') as f:
            try:
                data = json.load(f)
                return [Expense.from_json(expense) for expense in data]
            except json.JSONDecodeError:
                return {}

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
            amount = amount
        )
        self.expenses.append(expense)
        self.save_expenses()
        print(f"expense successfully added")

    def update_expense(self, id, description, amount):
        expense = self._find_by_id(id)
        if expense:
            expense.description = description
            expense.amount = amount
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

    def summarize_expenses(self, chosen_month = None):

        all_expenses = self.expenses

        if not all_expenses:
            print("No expenses found")

        if chosen_month:
            summarize_expenses = sum([expense.amount for expense in all_expenses
                                      if (datetime.strftime(expense.date, '%m') == chosen_month and
                                        datetime.strftime(expense.date, '%Y') == datetime.now().strftime('%Y')) ])
        else:
            summarize_expenses = sum(expenses.amount for expenses in all_expenses)

        print(f"All expenses value is {summarize_expenses}")


class CLIHandler:
    def __init__(self, expense_tracker):
        self.expense_tracker = expense_tracker

    def handle_command(self, args):
        pass


def main():
    expense_tracker = ExpenseTracker()
    cli = CLIHandler(expense_tracker)

    if len(sys.argv) == 1:
        print("Enter your commands to proceed:")
        while True:
            try:
                user_input = input("expense-tracker ").strip()
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

if __name__ == '__main__':
    main()