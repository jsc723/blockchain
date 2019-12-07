import time
from pubnub.pubnub  import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

subscribe_key = 'sub-c-40ff3bda-fa0f-11e9-be22-ea7c5aada356'
publish_key = 'pub-c-82ea9863-daab-4086-8c63-39b1d1bb8c36'

pnconfig = PNConfiguration()
pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key


CHANNELS = {
    'TEST' : 'TEST',
    'BLOCK' : 'BLOCK',
    'TRANSACTION' : 'TRANSACTION'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_obj):
        print(f'\n-- Channel: {message_obj.channel} | Message: {message_obj.message}')
        if message_obj.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_obj.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(self.blockchain)
                print('\n -- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n -- Dit not replace chain: {e}')
        elif message_obj.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_obj.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n -- Set the new transaction in the transaction pool')




class PubSub:
    """
    Handles the publish subscirbe layer of app
    communication between the nodes of the blockchain network
    """
    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))
    
    def publish(self, channel, message):
        """
        Publish the message object to the channel.
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes.
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes.
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())

if __name__ == '__main__':
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'foo':'bar'})


