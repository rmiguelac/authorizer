import json
from sys import stdin

from core.handlers import handle_account, handle_transaction, handle_account_mutation


if __name__ == "__main__":
    acc = None
    output = []

    for line in stdin.readlines():
        transaction_request = json.loads(line)
        violation = None
        if 'account' in transaction_request.keys():
            acc, response = handle_account(account_request=transaction_request, account=acc)
            output.append(response)
        elif 'transaction' in transaction_request.keys():
            response = handle_transaction(account=acc, transaction_request=transaction_request)
            output.append(response)
        elif 'allowList' in transaction_request.keys():
            response = handle_account_mutation(account=acc, transaction_request=transaction_request)
            output.append(response)
    
    
    for line in output:
        print(line)
    