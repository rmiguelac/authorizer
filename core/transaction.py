from datetime import datetime


class Transaction:

    def __init__(self, merchant: str, amount: int, time: str):
        self.merchant = merchant
        self.amount = amount
        self.time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fz')

    def __str__(self):
        return f'Transaction to {self.merchant} at {self.time} with value {self.amount}'    
