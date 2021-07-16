import json

from core.transaction import Transaction
from core.account import Account
from core.violation import get_violations


def handle_account(account_request: dict, account: Account = None):
    """ Takes an account_request and handles its creation or violation is raised"""

    if account:
        response = json.dumps({
                    'account': {
                        'activeCard': account.active_card,
                        'availableLimit': account.available_limit,
                        'allowListed': account.allow_listed
                    },
                    'violations': ['account-already-initialized']
                })
        return account, response
    else:
        acc = Account(
            available_limit=account_request['account']['availableLimit'],
            active_card=account_request['account']['activeCard']
        )
        response = json.dumps({'account': {'activeCard': acc.active_card, 'availableLimit': acc.available_limit, 'allowListed': acc.allow_listed}, 'violations': []})

    return acc, response

def handle_transaction(account: Account, transaction_request: dict):
    """ Takes a transaction request and handles it againts given Account
    
        Take input and translate it to Transaction object
        With Account and Transaction objects, check for violations with current transaction
        debit or raise violation 
        Add to account transaction history
    """

    transaction = Transaction(
        merchant=transaction_request['transaction']['merchant'],
        amount=transaction_request['transaction']['amount'],
        time=transaction_request['transaction']['time']
    )
    violations = get_violations(account=account, transaction=transaction)
    response = json.dumps({
        'account': {
            'activeCard': account.active_card,
            'availableLimit': account.debit(transaction.amount) if not violations else account.available_limit,
            'allowListed': account.allow_listed
            },
        'violations': violations
        }
    )
    account.transaction_history.append(transaction)
    return response

def handle_account_mutation(account: Account, transaction_request):
    """ Handles the account mutation as to allow only 2 violations to be checked

    1. The transaction amount should not be above limit
    2. No transaction should be approved when the card is blocked

    example request: {"allowList": {"active": true}}
    """
    
    account.set_allow_listed(transaction_request['allowList']['active'])
    response = json.dumps({
        'account': {
            'activeCard': account.active_card,
            'availableLimit': account.available_limit,
            'allowListed': account.allow_listed
        },
        'violations': []})
    return response 
