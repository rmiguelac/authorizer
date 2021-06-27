

class Account:

    def __init__(self, available_limit: int, active_card: bool):
        self.available_limit = available_limit
        self.active_card = active_card
    
    def __str__(self):
        return f'Account with card {self.active_card} and available limit {self.available_limit}'
    
    def debit(self, amount):
        self.available_limit -= amount
        return self.available_limit