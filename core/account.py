

class Account:
    """Account class to handle the account object as well as its transactions"""

    def __init__(self, available_limit: int, active_card: bool, allow_listed: bool = False):
        self.available_limit = available_limit
        self.active_card = active_card
        self.allow_listed = allow_listed
        self.transaction_history = []
    
    def debit(self, amount: int):
        self.available_limit -= amount
        return self.available_limit
    
    def set_allow_listed(self, allow_listed: bool):
        self.allow_listed = allow_listed
        return self.allow_listed


    def __str__(self):
        return f'Account with card {self.active_card}, available limit {self.available_limit} and allow listed {self.allow_listed}'

    def __repr__(self):
        return f'Account(available_limit={self.available_limit}, active_card={self.active_card}, allow_listed={self.allow_listed})'
    