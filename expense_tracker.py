import json
import os
from datetime import datetime
from json import JSONDecodeError


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
        self.expense = self.load_expenses()

    def load_expenses(self):
        if not os.path.isfile(self.storagefile):
            return {}

        with open(self.storagefile, 'r') as f:
            try:
                data = json.load(f)
                return [Expense.from_json(expense) for expense in data]
            except JSONDecodeError:
                return {}

    def save_expenses(self):
        with open(self.storagefile, 'w') as f:
            json.dump([expense.to_json() for expense in self.expense], f, indent=4)

    def _get_next_id(self):
        return max((expense.id for expense in self.expense), default=0) + 1

    def _find_by_id(self, expense_id):
        for expense in self.expense:
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
        self.expense.append(expense)
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


    def view_expenses(self):
        pass

    def delete_expense(self, id):
        pass

    def summarize_expenses(self):
        pass

