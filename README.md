# **Authorizer**

**Authorizer** is a simple python module that handles account creation, assuming only one, as well as that account transactions.

## **Design Decisions**

By far the most time spent while attempting to design the solution was on the violations. Since it should be _extensible_ but also simple, as well as, in my POV, transparent as how many violations where being processed, I did fallback to what python would interpret as the strategy pattern, yet different, more like Luciano Ramalho implementation on [_Python Fluente_](https://www.goodreads.com/book/show/36361456-python-fluente)

The idea behind that was, regardless of how many violations we would have, the _violations_ module would host it all and _get_violations_ method would go through them all.

As for the transaction history, added to the _Account_ class; Since in-memory was the requirement and there are violations that require transaction_history analysis, it seemed easier to just go for it as a class property.

## **Running**

To run the application, we require python 3.8+ installed.  
No need to install the requirements.txt as the only non-builtin library is the pytest, only used for testing.

running:
```bash
$ python authorizer.py < operations 
{"account": {"activeCard": true, "availableLimit": 100}, "violations": []}
{"account": {"activeCard": true, "availableLimit": 100}, "violations": ["account-already-initialized"]}
{"account": {"activeCard": true, "avilableLimit": 90}, "violations": []}
{"account": {"activeCard": true, "avilableLimit": 80}, "violations": []}
{"account": {"activeCard": true, "avilableLimit": 70}, "violations": []}
{"account": {"activeCard": true, "avilableLimit": 70}, "violations": ["high-frequenc-small-interval"]}
{"account": {"activeCard": true, "avilableLimit": 70}, "violations": ["high-frequenc-small-interval"]}
{"account": {"activeCard": true, "avilableLimit": 70}, "violations": ["double-transaction", "high-frequenc-small-interval"]}
{"account": {"activeCard": true, "avilableLimit": 70}, "violations": ["insufficient-limit"]}
{"account": {"activeCard": true, "avilableLimit": 20}, "violations": []}
```

## **Testing**

To run the tests, simply run ```python -m pytest -v```
```bash
$ python -m pytest -v
========================================================================================== test session starts ===========================================================================================
platform linux -- Python 3.8.2, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /home/rui/challenges/authorizer/bin/python
cachedir: .pytest_cache
rootdir: /home/rui/challenges/authorizer
collected 8 items                                                                                                                                                                                        

tests/test_account.py::test_account_is_created_with_availableLimit PASSED                                                                                                                          [ 12%]
tests/test_account.py::test_account_is_created_with_activeCard PASSED                                                                                                                              [ 25%]
tests/test_account.py::test_account_on_update_returns_account_already_initialized PASSED                                                                                                           [ 37%]
tests/test_transactions.py::test_transaction_outputs_current_account_state PASSED                                                                                                                  [ 50%]
tests/test_transactions.py::test_transaction_outputs_insufficient_limit_violation_on_insufficient_limit PASSED                                                                                     [ 62%]
tests/test_transactions.py::test_transaction_outputs_card_not_active_violation_on_card_not_active_account PASSED                                                                                   [ 75%]
tests/test_transactions.py::test_transaction_outputs_high_frequency_small_interval_violation_3_transactions_within_2_min PASSED                                                                    [ 87%]
tests/test_transactions.py::test_transaction_outputs_doubled_transaction_violation_when_2_similar_transactions_within_2_min PASSED                                                                 [100%]

=========================================================================================== 8 passed in 0.30s ============================================================================================
```