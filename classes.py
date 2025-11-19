class Budget:
    def __init__(self, expense_type):
        self.expense_type = expense_type
        # self.expenses = []
        # self.categories = []
        self.expenses_dict = {}

    def add_expenses(self):
        while True:
            try:
                num_expenses = int(input(f"\nEnter number of {self.expense_type} expenses you want to add (numbers only): "))
                break
            except:
                print()
                print("* Error! *")
                print("Enter integers only :-)")
                print()

        print("Enter expenses in \"Type Cost\" format. For e.g, Milk 10 or Gas 25")
        for i in range(num_expenses):
            while True:
                try:
                    type, expense_val = (input(f"\nEnter expense {i + 1}: ")).split()
                    self.expenses_dict[type] = float(expense_val)
                    # self.expenses.append(float(expense_val)) 
                    # self.categories.append(type) 
                    break
                except:
                    print()
                    print("* ERROR *")
                    print("Wrong input format. Please type expenses in this format: Milk 10")
                    print()

        self.write_to_file

    def get_expenses(self):
        total = sum(self.expenses_dict.values())
        print(f"\nTotal money spent on {self.expense_type}: ${total:.2f}")
        return total
    
    def get_expenses_list(self):
        print(f"\nMoney spent on {self.expense_type} are:\n")
        for type, expense_val in self.expenses_dict.items():
                print(f"{type} : ${str(expense_val)}")

    def write_to_file(self):
        with open("data.txt", "a") as data:
            data.write(self.expense_type)
            data.write("\n")

            for type, expense_val in self.expenses_dict.item():
                data.write(f"{type} : ${str(expense_val)}")
                data.write("\n")
            data.write("\n")