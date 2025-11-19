import os

class Budget:
    def __init__(self, expense_type):
        self.expense_type = expense_type
        self.expenses_dict = {}

    def add_expense(self, name, amount):
        self.expenses_dict[name] = amount

    def get_expenses(self):
        return sum(self.expenses_dict.values())

    def get_expenses_list(self):
        return [(name, amount) for name, amount in self.expenses_dict.items()]

    def write_to_file(self, filename="data.txt"):
        with open(filename, "a") as file:
            file.write(f"{self.expense_type}\n")
            for name, amount in self.expenses_dict.items():
                file.write(f"{name} : ${amount:.2f}\n")
            file.write("\n")
