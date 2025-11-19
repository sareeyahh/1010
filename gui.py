import tkinter as tk
from tkinter import messagebox

from classes import Budget
import functions

class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")

        # Data
        self.grocery = Budget("Grocery")
        self.car = Budget("Car")
        self.total_income = 0
        self.user_name = ""

        # ------------------------
        # TITLE
        # ------------------------
        tk.Label(root, text="BudgetBuddy", font=("Arial", 22, "bold")).pack(pady=10)

        # ------------------------
        # NAME INPUT
        # ------------------------
        name_frame = tk.Frame(root)
        name_frame.pack(pady=5)

        tk.Label(name_frame, text="Enter your name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(name_frame, width=20)
        self.name_entry.grid(row=0, column=1)

        tk.Button(name_frame, text="Submit", command=self.save_name).grid(row=0, column=2, padx=10)

        # ------------------------
        # INCOME INPUT
        # ------------------------
        income_frame = tk.Frame(root)
        income_frame.pack(pady=5)

        tk.Label(income_frame, text="Yearly Income ($):").grid(row=0, column=0)
        self.income_entry = tk.Entry(income_frame, width=20)
        self.income_entry.grid(row=0, column=1)

        tk.Button(income_frame, text="Save Income", command=self.save_income).grid(row=0, column=2, padx=10)

        # ------------------------
        # EXPENSE ENTRY AREA
        # ------------------------
        exp_frame = tk.LabelFrame(root, text="Add Expenses", padx=10, pady=10)
        exp_frame.pack(pady=10)

        tk.Label(exp_frame, text="Category (Grocery/Car):").grid(row=0, column=0)
        self.exp_category = tk.Entry(exp_frame, width=15)
        self.exp_category.grid(row=0, column=1)

        tk.Label(exp_frame, text="Type (ex: Milk, Gas):").grid(row=1, column=0)
        self.exp_type = tk.Entry(exp_frame, width=15)
        self.exp_type.grid(row=1, column=1)

        tk.Label(exp_frame, text="Amount ($):").grid(row=2, column=0)
        self.exp_amt = tk.Entry(exp_frame, width=15)
        self.exp_amt.grid(row=2, column=1)

        tk.Button(exp_frame, text="Add Expense", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=5)

        # ------------------------
        # OUTPUT BOX
        # ------------------------
        self.output_box = tk.Text(root, width=50, height=15, borderwidth=2, relief="sunken")
        self.output_box.pack(pady=10)

        tk.Button(root, text="Calculate Balance", command=self.calculate_balance).pack(pady=10)

    # ------------------------
    # FUNCTIONS
    # ------------------------

    def save_name(self):
        self.user_name = self.name_entry.get()
        if self.user_name.strip() == "":
            messagebox.showerror("Error", "Name cannot be empty.")
        else:
            messagebox.showinfo("Success", f"Hello {self.user_name}!")

    def save_income(self):
        try:
            self.total_income = float(self.income_entry.get())
            messagebox.showinfo("Success", "Income saved!")
        except ValueError:
            messagebox.showerror("Error", "Income must be a number.")

    def add_expense(self):
        category = self.exp_category.get().lower()
        exp_type = self.exp_type.get()
        exp_amt = self.exp_amt.get()

        if category == "grocery":
            budget = self.grocery
        elif category == "car":
            budget = self.car
        else:
            messagebox.showerror("Error", "Category must be Grocery or Car")
            return

        if not budget.add_expense(exp_type, exp_amt):
            messagebox.showerror("Error", "Amount must be a number.")
            return

        messagebox.showinfo("Success", f"{exp_type} added to {category.title()}.")
        self.refresh_output()

    def refresh_output(self):
        """Refresh the Text box contents."""
        self.output_box.delete("1.0", tk.END)

        self.output_box.insert(tk.END, "----- Grocery Expenses -----\n")
        for t, v in self.grocery.get_expense_list():
            self.output_box.insert(tk.END, f"{t}: ${v}\n")

        self.output_box.insert(tk.END, "\n----- Car Expenses -----\n")
        for t, v in self.car.get_expense_list():
            self.output_box.insert(tk.END, f"{t}: ${v}\n")

    def calculate_balance(self):
        total_expenses = self.grocery.get_total() + self.car.get_total()
        balance = functions.calc_balance(self.total_income, total_expenses)
        status = functions.financial_status(balance)

        self.output_box.insert(tk.END, f"\n\nTotal Expenses: ${total_expenses:.2f}")
        self.output_box.insert(tk.END, f"\nBalance: ${balance:.2f}\n")
        self.output_box.insert(tk.END, f"{status}\n")

        messagebox.showinfo("Financial Status", status)
