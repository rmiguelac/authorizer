import json

from core.transaction import Transaction
from core.account import Account
from core.violation import get_violations

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
    account.transaction_history.append(transaction)
    return response