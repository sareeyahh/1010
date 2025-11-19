import os
from library.classes import Budget
from library import functions

os.system('cls' if os.name == 'nt' else 'clear')

name = input("Enter your name: ")
os.system('cls' if os.name == 'nt' else 'clear')

print(f"Hey {name}, this is BudgetBuddy! Your personal Budgeting Assistant")

while True:
    user_input = input("\nEnter your yearly income (numbers only): ")
    try:
        income = float(user_input)
        break
    except ValueError:
        print("\nError: Please enter numbers only.")

total_expenses = []

grocery = Budget("Grocery")
car = Budget("Car")

grocery.add_expenses()
car.add_expenses()

total_expenses.append(grocery.get_expenses())
total_expenses.append(car.get_expenses())

balance = functions.calc_balance(income, sum(total_expenses))
functions.financial_status(balance)
