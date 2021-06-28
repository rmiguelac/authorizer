import json

from core.handlers import handle_account, handle_transaction

CREATE_ACCOUNT_REQUEST=json.loads('{ "account": { "activeCard": true, "availableLimit": 100 } }')
CREATE_NOT_ACTIVE_ACCOUNT_REQUEST=json.loads('{ "account": { "activeCard": false, "availableLimit": 100 } }')
PLACE_TRANSACTION=json.loads('{ "transaction": { "merchant": "Massimo", "amount": 10, "time": "2019-02-13T09:58:55.000Z" } }')
OVERLIMIT_TRANSACTION=json.loads('{ "transaction": { "merchant": "PlaceX", "amount": 110, "time": "2019-02-13T09:58:57.000Z" } }')
HIGH_FREQUENCY_TRANSACTION=json.loads('{ "transaction": { "merchant": "PlaceY", "amount": 10, "time": "2019-02-13T09:58:58.000Z" } }')
HIGH_FREQUENCY_TRANSACTION_FOURTH=json.loads('{ "transaction": { "merchant": "OtherPlace", "amount": 10, "time": "2019-02-13T09:58:59.000Z" } }')
DOUBLE_TRANSACTION=json.loads('{ "transaction": { "merchant": "Massimo", "amount": 10, "time": "2019-02-13T09:59:00.000Z" } }')

def test_transaction_outputs_current_account_state():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    response = handle_transaction(account=acc, transaction_request=PLACE_TRANSACTION)
    assert response == json.dumps({
        'account': {
            'activeCard': acc.active_card,
            'availableLimit': acc.available_limit
        },
        'violations': []
    })

def test_transaction_outputs_insufficient_limit_violation_on_insufficient_limit():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    _ = handle_transaction(account=acc, transaction_request=PLACE_TRANSACTION)
    response = handle_transaction(account=acc, transaction_request=OVERLIMIT_TRANSACTION)
    assert response == json.dumps({
        'account': {
            'activeCard': acc.active_card,
            'availableLimit': acc.available_limit
        },
        'violations': ["insufficient-limit"]
    })

def test_transaction_outputs_card_not_active_violation_on_card_not_active_account():
    acc, _ = handle_account(account_request=CREATE_NOT_ACTIVE_ACCOUNT_REQUEST)
    response = handle_transaction(account=acc, transaction_request=PLACE_TRANSACTION)
    assert response == json.dumps({
        'account': {
            'activeCard': acc.active_card,
            'availableLimit': acc.available_limit
        },
        'violations': ["card-not-active"]
    })

def test_transaction_outputs_high_frequency_small_interval_violation_3_transactions_within_2_min():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    _ = handle_transaction(account=acc, transaction_request=PLACE_TRANSACTION)
    _ = handle_transaction(account=acc, transaction_request=OVERLIMIT_TRANSACTION)
    _ = handle_transaction(account=acc, transaction_request=HIGH_FREQUENCY_TRANSACTION)
    response = handle_transaction(account=acc, transaction_request=HIGH_FREQUENCY_TRANSACTION_FOURTH)
    assert response == json.dumps({
        'account': {
            'activeCard': acc.active_card,
            'availableLimit': acc.available_limit
        },
        'violations': ["high-frequency-small-interval"]
    })

def test_transaction_outputs_doubled_transaction_violation_when_2_similar_transactions_within_2_min():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    _ = handle_transaction(account=acc, transaction_request=PLACE_TRANSACTION)
    response = handle_transaction(account=acc, transaction_request=DOUBLE_TRANSACTION)
    assert response == json.dumps({
        'account': {
            'activeCard': acc.active_card,
            'availableLimit': acc.available_limit
        },
        'violations': ["doubled-transaction"]
    })