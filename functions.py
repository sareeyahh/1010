def calc_balance(income, expenses):
    return income - expenses

def financial_status_text(balance):
    if balance > 0:
        return "Great! You are saving money!"
    elif balance == 0:
        return "You are breaking even."
    else:
        return "WARNING: You are overspending!"