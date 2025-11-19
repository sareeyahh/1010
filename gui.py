
class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")

        self.grocery = Budget("Grocery")
        self.car = Budget("Car")
        self.total_income = 0
        self.user_name = ""

        tk.Label(root, text="BudgetBuddy", font=("Arial", 22, "bold")).pack(pady=10)

        name_frame = tk.Frame(root)
        name_frame.pack(pady=5)

        tk.Label(name_frame, text="Enter your name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(name_frame, width=20)
        self.name_entry.grid(row=0, column=1)

        tk.Button(name_frame, text="Submit Name", command=self.save_name).grid(row=0, column=2, padx=10)

        income_frame = tk.Frame(root)
        income_frame.pack(pady=5)

        tk.Label(income_frame, text="Yearly Income ($):").grid(row=0, column=0)
        self.income_entry = tk.Entry(income_frame, width=20)
        self.income_entry.grid(row=0, column=1)

        tk.Button(income_frame, text="Save Income", command=self.save_income).grid(row=0, column=2, padx=10)

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

        self.output_box = tk.Text(root, width=50, height=15, borderwidth=2, relief="sunken")
        self.output_box.pack(pady=10)

        tk.Button(root, text="Calculate Balance", command=self.calculate_balance).pack(pady=10)
