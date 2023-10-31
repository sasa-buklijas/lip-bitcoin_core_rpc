# lip-bitcoin_core_rpc

## Requirements
Developed with Python:
 - [version](https://github.com/sasa-buklijas/lip-bitcoin_core_rpc/blob/main/.python-version)
 - [packages](https://github.com/sasa-buklijas/lip-bitcoin_core_rpc/blob/main/requirements.txt)

## Code Examples
### [new_block_notification.py](https://github.com/sasa-buklijas/lip-bitcoin_core_rpc/blob/main/new_block_notification.py)  
Uses bitcon-core ZeroMQ(zmqpubhashblock) to monitor for new blocks.  
On OSX(macOS) notification is displayed on screen with block statistic.  

### [getbestblockhash.py](https://github.com/sasa-buklijas/lip-bitcoin_core_rpc/blob/main/getbestblockhash.py)  
Hello world example for bitcon-core RPC.

### [mempool_change.py](https://github.com/sasa-buklijas/lip-bitcoin_core_rpc/blob/main/mempool_change.py)  
Polling bitcoin-core mempool via RPC(getmempoolinfo) to calculate difference between added and removed txids.  
If pooling is to slow, use [bitcoin-core ZeroMQ streams](https://bitcoindev.network/accessing-bitcoins-zeromq-interface/). 


