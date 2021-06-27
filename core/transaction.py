from datetime import datetime
import json

from core.account import Account
from core.violation import get_violations


class Transaction:

    def __init__(self, merchant: str, amount: int, time: str):
        self.merchant = merchant
        self.amount = amount
        self.time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fz')

    def __str__(self):
        return f'Transaction to {self.merchant} at {self.time} with value {self.amount}'    


def handle_transaction(account: Account, transaction_request: dict):
    """Takes a transaction and handles it againts given account"""
    transaction = Transaction(
        merchant=transaction_request['transaction']['merchant'],
        amount=transaction_request['transaction']['amount'],
        time=transaction_request['transaction']['time']
    )
    violations = get_violations(account=account, transaction=transaction)
    response = json.dumps({
        'account': {
            'activeCard': account.active_card,
            'avilableLimit': account.debit(transaction.amount) if not violations else account.available_limit
            },
        'violations': violations
        }
    )
    return response