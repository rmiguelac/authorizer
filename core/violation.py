from inspect import getmembers, isfunction

from core.account import Account
from core.transaction import Transaction
from core import violations


def get_violations(account: Account, transaction: Transaction):
    """Given an Account and a Transaction, return all violations"""

    # This list comprehension takes all functions from violations and saves it to violats
    violats = [func for _, func in getmembers(violations, isfunction)]

    """ For every violation found in the violations module, execute it againts
        the account with current transaction and return all violations for 
        current transaction
    """
    transaction_violations = [func(account, transaction) for func in violats if func(account,transaction)]
    return transaction_violations