import zmq
import time
import os
from bitcoinrpc.authproxy import AuthServiceProxy
from config import config as c


def main():
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(c.rpc_user, c.rpc_password))

    # when mempool is ready
    while True:
        mempool_info = rpc_connection.getmempoolinfo()
        mempool_info_loaded = mempool_info['loaded']

        if mempool_info_loaded is False:
            print('Still waiting to load mempool after restart of bitcoin-core')
            print(f'{mempool_info=}')
            time.sleep(5)
        else:
            break   # go to next step

    # ZeroMQ
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:29000") 
    socket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")
    socket.setsockopt_string(zmq.SUBSCRIBE, "sequence")

    first_msg: bool = True
    print(f'Subscribed to ZeroMQ messages. {os.getpid()=} Waiting for messages...')
    while True:
        topic, body, seq = socket.recv_multipart()

        if first_msg:
            rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(c.rpc_user, c.rpc_password))
            all_txids = set(rpc_connection.getrawmempool())
            all_txids_with_rbf = all_txids
            first_msg = False

        if topic == b"hashblock":
            block_hash = body.hex()
            txid_missing: int = 0
            rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(c.rpc_user, c.rpc_password))
            block = rpc_connection.getblock(block_hash)
            block_nTx = block['nTx']

            for txid in block['tx']:
                if txid not in all_txids:
                    txid_missing += 1
                    # print(f'For block {block_hash} missing {txid=}')

                    if txid in all_txids_with_rbf:
                        print(f'    but {txid=} is in all_txids_with_rbf')

                # to keep it not too big, but it is note removing ancestors(so it is like a memory-leak)
                all_txids_with_rbf.discard(txid)
            print(f'Stats for {block_hash} missing {txid_missing}/{block_nTx} {txid_missing/block_nTx*100-100}%')
        elif topic == b"sequence":  #txid A|R 
            txid = body[:32].hex()
            label = chr(body[32])

            if label == 'A':
                all_txids.add(txid)
                all_txids_with_rbf.add(txid)
            elif label == 'R':
                all_txids.discard(txid) # discard no exception if txid in missing
            elif label == 'C':
                pass # new block found
            else:   # only D, is is for reorg
                print(f'UNKNOWN label {label=} for {txid=}')
        else:
            print(f'UNKNOWN topic {topic=}')


if __name__ == "__main__":
    main()