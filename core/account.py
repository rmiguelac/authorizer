

class Account:
    """Account class to handle the account object as well as its transactions"""

    def __init__(self, available_limit: int, active_card: bool):
        self.available_limit = available_limit
        self.active_card = active_card
        self.transaction_history = []
    
    def debit(self, amount: int):
        self.available_limit -= amount
        return self.available_limit

    def __str__(self):
        return f'Account with card {self.active_card} and available limit {self.available_limit}'

    def __repr__(self):
        return f'Account(available_limit={self.available_limit}, active_card={self.active_card}'
    