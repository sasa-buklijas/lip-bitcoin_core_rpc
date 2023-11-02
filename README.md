# lip-bitcoin_core_rpc

## Requirements
Developed with Python:
 - [version](https://github.com/sasa-buklijas/lip-bitcoin_core_rpc/blob/main/.python-version)
 - [packages](https://github.com/sasa-buklijas/lip-bitcoin_core_rpc/blob/main/requirements.txt)

## Code Examples
### [new_block_notification.py](./new_block_notification.py)  
Uses bitcon-core ZeroMQ(zmqpubhashblock) to monitor for new blocks.  
On OSX(macOS) notification is displayed on screen with block statistic.  
OSX screenshots:  
OSX Notification Pop-up  
![OSX notification](./documentation/screenshots/osx_notification.png)  
OSX Notification Center  
![OSX notifications](./documentation/screenshots/osx_notifications.png)

### [getbestblockhash.py](./getbestblockhash.py)  
Hello world example for bitcon-core RPC.

### [mempool_change.py](./mempool_change.py)  
Polling bitcoin-core mempool via RPC(getmempoolinfo) to calculate difference between added and removed txids.  
If pooling is to slow, use [bitcoin-core ZeroMQ streams](https://bitcoindev.network/accessing-bitcoins-zeromq-interface/). 


