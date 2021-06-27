from inspect import getmembers, isfunction
from typing import List

from core.account import Account
from core.transaction import Transaction
from core import violations


def get_violations(account: Account, transaction: Transaction):
    """Given an Account and a Transaction, return all violations"""

    violats = [func for name, func in getmembers(violations, isfunction)]

    transaction_violations = [func(account, transaction) for func in violats if func(account,transaction)]
    return transaction_violations