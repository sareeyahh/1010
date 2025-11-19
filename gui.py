import tkinter as tk
from tkinter import messagebox
from library.classes import Budget
from library import functions
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")

        self.user_name = ""
        self.income = 0
        self.categories = {}
        self.canvas = None

        self.show_name_screen()

    def show_name_screen(self):
        self.clear()
        tk.Label(self.root, text="Enter your name:").pack(pady=10)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        tk.Button(self.root, text="Next", command=self.save_name).pack(pady=10)

    def save_name(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a valid name.")
            return
        self.user_name = name
        self.show_income_screen()

    def show_income_screen(self):
        self.clear()
        tk.Label(self.root, text=f"Hi {self.user_name}! Welcome to BudgetBuddy, your personal budgeting assistant. \nEnter your yearly income:").pack(pady=10)
        self.income_entry = tk.Entry(self.root)
        self.income_entry.pack()
        tk.Button(self.root, text="Next", command=self.save_income).pack(pady=10)

    def save_income(self):
        try:
            money = float(self.income_entry.get())
            if money <= 0:
                raise ValueError
            self.income = money
            self.show_num_categories_screen()
        except:
            messagebox.showerror("Error", "Please enter a valid number for income.")

    def show_num_categories_screen(self):
        self.clear()
        tk.Label(self.root, text="How many types of expenses do you want to add?").pack(pady=10)
        self.num_cat_entry = tk.Entry(self.root)
        self.num_cat_entry.pack()
        tk.Button(self.root, text="Next", command=self.save_num_categories).pack(pady=10)

    def save_num_categories(self):
        try:
            num = int(self.num_cat_entry.get())
            if num <= 0:
                raise ValueError
            self.num_categories = num
            self.category_names = []
            self.current_index = 0
            self.show_category_name_screen()
        except:
            messagebox.showerror("Error", "Enter a valid whole number.")

    def show_category_name_screen(self):
        self.clear()
        tk.Label(self.root, text=f"Enter name for category {self.current_index + 1}:").pack(pady=10)
        self.cat_name_entry = tk.Entry(self.root)
        self.cat_name_entry.pack()
        tk.Button(self.root, text="Next", command=self.save_category_name).pack(pady=10)

    def save_category_name(self):
        name = self.cat_name_entry.get().strip()
        if not name.isalpha():
            messagebox.showerror("Error", "Category name must contain only letters.")
            return

        self.category_names.append(name)
        self.categories[name] = Budget(name)

        self.current_index += 1
        if self.current_index < self.num_categories:
            self.show_category_name_screen()
        else:
            self.current_index = 0
            self.show_expense_entry_screen()

    def show_expense_entry_screen(self):
        self.clear()
        current_cat = self.category_names[self.current_index]

        tk.Label(self.root, text=f"Enter expenses for {current_cat}:").pack(pady=10)
        tk.Label(self.root, text="Format: word amount (e.g., milk 10)").pack()

        self.exp_entry = tk.Entry(self.root, width=40)
        self.exp_entry.pack()

        tk.Button(self.root, text="Add Expense", command=self.add_expense).pack(pady=5)
        tk.Button(self.root, text="Done", command=self.save_expenses_and_continue).pack(pady=10)

    def add_expense(self):
        raw = self.exp_entry.get().strip()
        parts = raw.split()
        if len(parts) != 2:
            messagebox.showerror("Error", "Format must be: word amount")
            return

        word, amount = parts
        if not word.isalpha():
            messagebox.showerror("Error", "Expense name must be letters only.")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Amount must be a number greater than 0.")
            return

        category = self.category_names[self.current_index]
        budget_obj = self.categories[category]
        budget_obj.add_expense(word, amount)

        messagebox.showinfo("Added", f"Added {word} - ${amount:.2f}")
        self.exp_entry.delete(0, tk.END)

    def save_expenses_and_continue(self):
        self.current_index += 1
        if self.current_index < len(self.category_names):
            self.show_expense_entry_screen()
        else:
            self.show_results_screen()

    def show_results_screen(self):
        self.clear()

        total_expenses = 0
        tk.Label(self.root, text="Budget Summary", font=("Cambria", 18, "bold")).pack(pady=10)
        tk.Label(self.root, text=f"Yearly Income: ${self.income:.2f}", font=("Cambria", 14)).pack(pady=5)

        for cat, obj in self.categories.items():
            cat_total = obj.get_expenses()
            total_expenses += cat_total
            tk.Label(self.root, text=f"{cat}: ${cat_total:.2f}", font=("Cambria", 12)).pack()

        tk.Label(self.root, text=f"\nTotal Expenses: ${total_expenses:.2f}", font=("Cambria", 14)).pack(pady=5)

        balance = functions.calc_balance(self.income, total_expenses)
        status = functions.financial_status_text(balance)

        tk.Label(self.root, text=f"Remaining Balance: ${balance:.2f}", font=("Cambria", 14)).pack(pady=5)
        tk.Label(self.root, text=status, font=("Cambria", 14),
                 fg="green" if balance > 0 else "red" if balance < 0 else "orange").pack(pady=10)

        self.show_pie_chart()

    def show_pie_chart(self):
        labels = []
        sizes = []
        for category, obj in self.categories.items():
            cat_total = obj.get_expenses()
            if cat_total > 0:
                labels.append(category)
                sizes.append(cat_total)

        if not sizes:
            return

        fig, ax = plt.subplots(figsize=(4,4))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title("Expenses by Category")

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=15)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


def start_gui():
    root = tk.Tk()
    app = BudgetGUI(root)
    root.mainloop()


if __name__ == "__main__":
    start_gui()
