import json

from core.handlers import handle_account_mutation, handle_account


CREATE_ACCOUNT_REQUEST=json.loads('{ "account": { "activeCard": true, "availableLimit": 100 } }')
ALLOW_LISTED_TRUE_REQUEST=json.loads('{"allowList": {"active": true}}')
ALLOW_LISTED_FALSE_REQUEST=json.loads('{"allowList": {"active": false}}')


def test_set_allowed_list_true_mutates_account_to_true():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    handle_account_mutation(acc, transaction_request=ALLOW_LISTED_TRUE_REQUEST)
    assert acc.allow_listed == True

def test_set_allowed_list_false_mutates_account_to_false():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    handle_account_mutation(acc, transaction_request=ALLOW_LISTED_TRUE_REQUEST)
    handle_account_mutation(acc, transaction_request=ALLOW_LISTED_FALSE_REQUEST)
    assert acc.allow_listed == False

def test_set_allowed_list_returns_expected_output():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    response = handle_account_mutation(acc, transaction_request=ALLOW_LISTED_TRUE_REQUEST)
    assert json.loads(response) == json.loads('{"account": {"activeCard": true, "availableLimit": 100, "allowListed": true}, "violations": []}')