import json

from core.handlers import handle_account

CREATE_ACCOUNT_REQUEST=json.loads('{ "account": { "activeCard": true, "availableLimit": 100 } }')

def test_account_is_created_with_availableLimit():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    assert acc.available_limit == CREATE_ACCOUNT_REQUEST['account']['availableLimit']

def test_account_is_created_with_activeCard():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    assert acc.active_card == CREATE_ACCOUNT_REQUEST['account']['activeCard']

def test_account_on_update_returns_account_already_initialized():
    acc, _ = handle_account(account_request=CREATE_ACCOUNT_REQUEST)
    _, response = handle_account(account_request=CREATE_ACCOUNT_REQUEST, account=acc)
    assert json.loads(response) == json.loads('{"account": {"activeCard": true, "availableLimit": 100, "allowListed": false}, "violations": ["account-already-initialized"]}')