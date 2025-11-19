import os

class Budget:
    def __init__(self, category):
        self.category = category
        self.expenses = []

    def add_expense(self, name, amount):
        self.expenses.append((name, amount))

    def get_expenses_list(self):
        return self.expenses

    def total(self):
        return sum(amount for _, amount in self.expenses)