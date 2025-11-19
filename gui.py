import tkinter as tk
from tkinter import messagebox
from library.classes import Budget
from library import functions
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os

DATA_FILE = "data.txt"

class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")
        self.root.geometry("500x500")

        self.username = ""
        self.income = 0
        self.categories = {}

        self.load_data()
        self.show_name_screen()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return

        current_cat = None
        with open(DATA_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if ":" not in line:
                    current_cat = line
                    if current_cat not in self.categories:
                        self.categories[current_cat] = Budget(current_cat)
                else:
                    name, amount = line.split(":")
                    name = name.strip()
                    amount = float(amount.replace("$", "").strip())
                    self.categories[current_cat].add_expense(name, amount)

    def save_to_file(self):
        existing = {}
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                lines = f.readlines()
            current_cat = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if ":" not in line:
                    current_cat = line
                    existing[current_cat] = {}
                else:
                    name, amount = line.split(":")
                    name = name.strip()
                    amount = float(amount.replace("$", "").strip())
                    existing[current_cat][name] = amount

        for cat, budget in self.categories.items():
            if cat not in existing:
                existing[cat] = {}
            for name, amount in budget.get_expenses_list():
                existing[cat][name] = amount

        # Write merged file
        with open(DATA_FILE, "w") as f:
            for cat, items in existing.items():
                f.write(f"{cat}\n")
                for name, amount in items.items():
                    f.write(f"{name} : ${amount:.2f}\n")
                f.write("\n")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_name_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to BudgetBuddy!", font=("Cambria", 20, "bold")).pack(pady=20)
        tk.Label(self.root, text="Enter your name:", font=("Cambria", 14)).pack(pady=10)

        entry = tk.Entry(self.root, font=("Cambria", 12))
        entry.pack()

        def save_name():
            name = entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Name cannot be empty.")
                return
            self.username = name
            self.show_income_screen()

        tk.Button(self.root, text="Continue", font=("Cambria", 12), command=save_name).pack(pady=15)

    def show_income_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Hi {self.username}!", font=("Cambria", 16)).pack(pady=20)
        tk.Label(self.root, text="Enter your yearly income (numbers only):", font=("Cambria", 14)).pack(pady=10)

        entry = tk.Entry(self.root, font=("Cambria", 12))
        entry.pack()

        def save_income():
            try:
                value = float(entry.get().strip())
                if value <= 0:
                    raise ValueError
                self.income = value
                self.show_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for income.")

        tk.Button(self.root, text="Continue", font=("Cambria", 12), command=save_income).pack(pady=15)

    def show_main_menu(self):
        self.clear_screen()
        greeting = f"Hey {self.username}, this is BudgetBuddy!\nYour personal Budgeting Assistant"
        tk.Label(self.root, text=greeting, font=("Cambria", 16), justify="center").pack(pady=20)
        tk.Label(self.root, text=f"Yearly Income: ${self.income:.2f}", font=("Cambria", 14)).pack(pady=5)

        tk.Button(self.root, text="Add Category", command=self.show_add_category_screen).pack(pady=10)
        tk.Button(self.root, text="Add Expense", command=self.show_add_expense_screen).pack(pady=10)
        tk.Button(self.root, text="View Results", command=self.show_results_screen).pack(pady=10)
        tk.Button(self.root, text="Save All to File", bg="lightgreen", command=self.save_to_file).pack(pady=20)

    def show_add_category_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Category Name:", font=("Cambria", 14)).pack(pady=10)
        entry = tk.Entry(self.root, font=("Cambria", 12))
        entry.pack()

        def add_category():
            name = entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Category cannot be empty.")
                return
            if name not in self.categories:
                self.categories[name] = Budget(name)
                self.save_to_file()
            messagebox.showinfo("Success", f"Category '{name}' added!")
            self.show_main_menu()

        tk.Button(self.root, text="Add", command=add_category).pack(pady=15)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack()

    def show_add_expense_screen(self):
        self.clear_screen()
        if not self.categories:
            tk.Label(self.root, text="No categories yet. Add one first!", fg="red").pack(pady=10)
            tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=10)
            return

        tk.Label(self.root, text="Select Category:", font=("Cambria", 14)).pack(pady=10)
        cat_var = tk.StringVar(self.root)
        cat_names = list(self.categories.keys())
        cat_var.set(cat_names[0])
        tk.OptionMenu(self.root, cat_var, *cat_names).pack(pady=5)

        tk.Label(self.root, text="Expense Name:", font=("Cambria", 12)).pack(pady=5)
        name_entry = tk.Entry(self.root, font=("Cambria", 12))
        name_entry.pack()

        tk.Label(self.root, text="Amount:", font=("Cambria", 12)).pack(pady=5)
        amount_entry = tk.Entry(self.root, font=("Cambria", 12))
        amount_entry.pack()

        def save_expense():
            cat = cat_var.get()
            name = name_entry.get().strip()
            try:
                amount = float(amount_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")
                return
            if not name:
                messagebox.showerror("Error", "Name cannot be empty.")
                return

            self.categories[cat].add_expense(name, amount)
            self.save_to_file()
            messagebox.showinfo("Added", f"{name} - ${amount:.2f} added to {cat}!")
            self.show_main_menu()

        tk.Button(self.root, text="Add Expense", command=save_expense).pack(pady=15)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=10)

        labels = []
        sizes = []
        for cat, budget in self.categories.items():
            if budget.total() > 0:
                labels.append(cat)
                sizes.append(budget.total())

        if sizes:
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.set_title("Expenses by Category")

            self.canvas = FigureCanvasTkAgg(fig, master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=10)

        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=15)

    def show_results_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Expense Summary", font=("Cambria", 18, "bold")).pack(pady=10)

        total_expenses = 0
        for cat, budget in self.categories.items():
            tk.Label(self.root, text=f"{cat}: ${budget.total():.2f}", font=("Cambria", 14)).pack()
            total_expenses += budget.total()

        balance = self.income - total_expenses
        tk.Label(self.root, text=f"\nTotal Expenses: ${total_expenses:.2f}", font=("Cambria", 16, "bold")).pack(pady=5)
        tk.Label(self.root, text=f"Remaining Balance: ${balance:.2f}", font=("Cambria", 16, "bold")).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=15)

def start_gui():
    root = tk.Tk()
    BudgetGUI(root)
    root.mainloop()