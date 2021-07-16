import json

from core.handlers import handle_account, handle_transaction, handle_account_mutation

CREATE_ACCOUNT_REQUEST=json.loads('{ "account": { "activeCard": true, "availableLimit": 100 } }')
CREATE_NOT_ACTIVE_ACCOUNT_REQUEST=json.loads('{ "account": { "activeCard": false, "availableLimit": 100 } }')
PLACE_TRANSACTION=json.loads('{ "transaction": { "merchant": "Massimo", "amount": 10, "time": "2019-02-13T09:58:55.000Z" } }')
OVERLIMIT_TRANSACTION=json.loads('{ "transaction": { "merchant": "PlaceX", "amount": 110, "time": "2019-02-13T09:58:57.000Z" } }')
HIGH_FREQUENCY_TRANSACTION=json.loads('{ "transaction": { "merchant": "PlaceY", "amount": 10, "time": "2019-02-13T09:58:58.000Z" } }')
HIGH_FREQUENCY_TRANSACTION_FOURTH=json.loads('{ "transaction": { "merchant": "OtherPlace", "amount": 10, "time": "2019-02-13T09:58:59.000Z" } }')
DOUBLE_TRANSACTION=json.loads('{ "transaction": { "merchant": "Massimo", "amount": 10, "time": "2019-02-13T09:59:00.000Z" } }')
ALLOW_LISTED_TRUE_REQUEST=json.loads('{"allowList": {"active": true}}')


CREATE_ACCOUNT_REQUEST_MIL=json.loads('{ "account": { "activeCard": true, "availableLimit": 1000 } }')
PAYLOAD_ONE=json.loads('{ "transaction": { "merchant": "A", "amount": 20, "time": "2019-02-13T10:00:00.000Z" } }')
PTWO=json.loads('{ "transaction": { "merchant": "B", "amount": 30, "time": "2019-02-13T10:00:01.000Z" } }')
PTHREE=json.loads('{ "transaction": { "merchant": "C", "amount": 40, "time": "2019-02-13T10:00:02.000Z" } }')
PFOUR=json.loads('{ "transaction": { "merchant": "D", "amount": 50, "time": "2019-02-13T10:00:03.000Z" } }')
PFIFTH=json.loads('{ "transaction": { "merchant": "E", "amount": 2000, "time": "2019-02-13T10:00:04.000Z" } }')


def test_transaction_outputs_current_account_state():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    response = handle_transaction(account=acc, transaction_request=PLACE_TRANSACTION)
    assert response == json.dumps({
        'account': {
            'activeCard': acc.active_card,
            'availableLimit': acc.available_limit,
            'allowListed': acc.allow_listed
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
            'availableLimit': acc.available_limit,
            'allowListed': acc.allow_listed
        },
        'violations': ["insufficient-limit"]
    })

def test_transaction_outputs_card_not_active_violation_on_card_not_active_account():
    acc, _ = handle_account(account_request=CREATE_NOT_ACTIVE_ACCOUNT_REQUEST)
    response = handle_transaction(account=acc, transaction_request=PLACE_TRANSACTION)
    assert response == json.dumps({
        'account': {
            'activeCard': acc.active_card,
            'availableLimit': acc.available_limit,
            'allowListed': acc.allow_listed
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
            'availableLimit': acc.available_limit,
            'allowListed': acc.allow_listed
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
            'availableLimit': acc.available_limit,
            'allowListed': acc.allow_listed
        },
        'violations': ["doubled-transaction"]
    })

def test_transaction_with_account_true_raises_only_expected_violations():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST_MIL)
    handle_account_mutation(account=acc, transaction_request=ALLOW_LISTED_TRUE_REQUEST)
    handle_transaction(account=acc, transaction_request=PAYLOAD_ONE)
    handle_transaction(account=acc, transaction_request=PTWO)
    handle_transaction(account=acc, transaction_request=PTHREE)
    handle_transaction(account=acc, transaction_request=PFOUR)
    response = handle_transaction(account=acc, transaction_request=PFIFTH)
    assert response == json.dumps({
        'account': {
            'activeCard': acc.active_card,
            'availableLimit': 860,
            'allowListed': acc.allow_listed
        },
        'violations': ["insufficient-limit"]
    })