
from core.account import Account
from core.transaction import Transaction


def insufficient_limit_violation(account: Account, transaction: Transaction):
    """Return insufficient-limit violation"""
    if account.available_limit < transaction.amount:
        return 'insufficient-limit'

def card_not_active(account: Account, transaction: Transaction):
    """Return card-not-active violation"""
    if not account.active_card:
        return 'card-not-active'

def high_frequency_small_interval(account: Account, transaction: Transaction):
    """Return high-frequency-small-interval violation"""

def double_transaction(account: Account, transaction: Transaction):
    """Return double-transaction violation"""