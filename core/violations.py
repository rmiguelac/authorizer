
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
    account_last_three_transactions = account.transaction_history[-3:].copy()[::-1]
    if len(account_last_three_transactions) >= 3:
        if (transaction.time - account_last_three_transactions[-1].time).seconds <= 120:
            return 'high-frequenc-small-interval'

def double_transaction(account: Account, transaction: Transaction):
    """Return double-transaction violation"""