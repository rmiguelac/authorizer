from inspect import getmembers, isfunction

from core.account import Account
from core.transaction import Transaction
from core import violations
from config import ALLOW_LISTED_VIOLATIONS


def get_violations(account: Account, transaction: Transaction):
    """Given an Account and a Transaction, return all violations"""

    # This list comprehension takes all functions from violations and saves it to violats
    violats = [func for _, func in getmembers(violations, isfunction) if not account.allow_listed or func in ALLOW_LISTED_VIOLATIONS]

    """ For every violation found in the violations module, execute it againts
        the account with current transaction and return all violations for 
        current transaction taking into consideration the account state (allow listed)
        and its current configured violations
    """
    transaction_violations = [func(account, transaction) for func in violats if func(account,transaction)]
    return transaction_violations