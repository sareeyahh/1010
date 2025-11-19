def calc_balance(income, expenses):
    print(f"\nTotal expenses are ${expenses:.2f}")
    balance = income - expenses 
    return balance

def financial_status(balance):
    if balance > 0:
        print("\nGreat! You are saving money!")
    elif balance == 0:
     print("\nYou are breaking even.")
    else:
        print("\n**WARNING** You are overspending!")