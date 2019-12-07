from backend.wallet.transaction import Transaction
from backend.wallet.wallet  import Wallet
import pytest
from backend.config import MINEING_REWARD, MINEING_REWARD_INPUT
from backend.config import STARTING_BALANCE

def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount

    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key

    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match='Amount exceeds balance'):
        Transaction(Wallet(), 'recipient', 20000)


def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    with pytest.raises(Exception, match='Amount exceeds balance'):
        transaction.update(sender_wallet, 'new_recipient', 9000)

def test_transaction_update():
    sender_wallet = Wallet()
    first_rec = 'first'
    first_amount = 50
    transaction = Transaction(sender_wallet, first_rec, first_amount)
    next_rec = 'second'
    next_amount = 75
    transaction.update(sender_wallet, next_rec, next_amount)

    assert transaction.output[next_rec] == next_amount
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

    to_first_again_amount = 25
    transaction.update(sender_wallet, first_rec, to_first_again_amount)
    assert transaction.output[first_rec] == first_amount + to_first_again_amount
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount - to_first_again_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_valid_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'recipient', 50))

def test_valid_transaction_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.output[sender_wallet.address] = 9001
    with pytest.raises(Exception, match='Invalid transaction output values'):
        Transaction.is_valid_transaction(transaction)

def test_valid_transaction_invalid_signature():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)
    with pytest.raises(Exception, match='Invalid signature'):
        Transaction.is_valid_transaction(transaction)

def test_reward_transaction():
    miner_wallet = Wallet()
    transaction = Transaction.reward_transaction(miner_wallet)

    assert transaction.input == MINEING_REWARD_INPUT
    assert transaction.output[miner_wallet.address] \
        == MINEING_REWARD

def test_valid_reward_transaction():
    reward_transaction = Transaction.reward_transaction(Wallet())
    Transaction.is_valid_transaction(reward_transaction)

def test_invalid_reward_transaction_extra_recipient():
    reward_transaction = Transaction.reward_transaction(Wallet())
    reward_transaction.output['extra_recipient'] = 60
    with pytest.raises(Exception, match='Invalid mining reward'):
        Transaction.is_valid_transaction(reward_transaction)

def test_invalid_reward_transaction_invalid_amount():
    miner_wallet = Wallet()
    reward_transaction = Transaction.reward_transaction(miner_wallet)
    reward_transaction.output[miner_wallet.address] = 9001
    with pytest.raises(Exception, match='Invalid mining reward'):
        Transaction.is_valid_transaction(reward_transaction)
