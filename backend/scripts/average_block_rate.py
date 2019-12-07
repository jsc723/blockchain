from backend.blockchain.blockchain import Blockchain
import time
from backend.config import SECONDS
blockchain = Blockchain()

times = []

for i in range(1000):
    start_time = time.time_ns()
    blockchain.add_block(i)
    end_time = time.time_ns()
    time_to_mind = (end_time - start_time) / SECONDS
    times.append(time_to_mind)

    average_time = sum(times) / len(times)
    print(f'new block diff: {blockchain.chain[-1].difficulty}')
    print(f'time to mine new block: {time_to_mind}s')
    print(f'average to add blocks: {average_time}s\n')