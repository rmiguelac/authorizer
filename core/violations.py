from core.account import Account
from core.transaction import Transaction


def insufficient_limit_violation(account: Account, transaction: Transaction):
    """Return insufficient-limit violation"""
    if account.available_limit < transaction.amount:
        return 'insufficient-limit'

def card_not_active(account: Account, *args):
    """Return card-not-active violation"""
    if not account.active_card:
        return 'card-not-active'

def high_frequency_small_interval(account: Account, transaction: Transaction):
    """Return high-frequency-small-interval violation"""

    """ Assuming transactions are only given in a increase datetime,
        take the last three, reverse it to get from newest to last
        and take the difference of current transaction and last one.
        
        If this would be the fourth transaction within the 2m time frame,
        return the expected violation
    """
    account_last_three_transactions = account.transaction_history[-3:].copy()[::-1]
    if len(account_last_three_transactions) >= 3:
        if (transaction.time - account_last_three_transactions[-1].time).seconds <= 120:
            return 'high-frequency-small-interval'

def double_transaction(account: Account, transaction: Transaction):
    """Return doubled-transaction violation"""
    account_last_transactions = account.transaction_history.copy()[::-1]

    """ Take all the transactions from account from newest to oldest
        Filter out the ones that do not happened in the last 2m time frame
        
        If merchant and amount match, return expected violation
    """
    last_two_min_transactions = [
        x for x in account_last_transactions if (transaction.time - x.time).seconds <= 120
    ]
    for transact in last_two_min_transactions:
        if (transact.merchant == transaction.merchant) and (transact.amount == transaction.amount):
            return 'doubled-transaction'