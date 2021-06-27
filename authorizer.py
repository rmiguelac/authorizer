import json
from sys import stdin

from core.account import Account
from core.handlers import handle_transaction

IS_ACCOUNT_SET=False

if __name__ == "__main__":
    acc = None
    output = []

    for line in stdin.readlines():
        transaction_request = json.loads(line)
        violation = None
        if 'account' in transaction_request.keys():
            if not IS_ACCOUNT_SET:
                acc = Account(
                    available_limit=transaction_request['account']['availableLimit'],
                    active_card=transaction_request['account']['activeCard']
                )
                response = json.dumps({'account': {'activeCard': acc.active_card, 'availableLimit': acc.available_limit}, 'violations': []})
                output.append(response)
                IS_ACCOUNT_SET=True
            else:
                response = json.dumps({'account': {'activeCard': acc.active_card, 'availableLimit': acc.available_limit}, 'violations': ['account-already-initialized']})
                output.append(response)
        elif 'transaction' in transaction_request.keys():
            response = handle_transaction(account=acc, transaction_request=transaction_request)
            output.append(response)
    
    
    for line in output:
        print(line)
    