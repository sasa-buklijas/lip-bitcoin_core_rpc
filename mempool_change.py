import time
from bitcoinrpc.authproxy import AuthServiceProxy#, JSONRPCException
from config import config as c


def main():
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(c.rpc_user, c.rpc_password))

    while True:
        mempool_info = rpc_connection.getmempoolinfo()
        mempool_info_loaded = mempool_info['loaded']

        if mempool_info_loaded is False:
            print('Still waiting to load mempool after restart of bitcoin-core')
            print(f'{mempool_info=} {type(mempool_info)=}')
            time.sleep(25)  # check again in 25 seconds 
        else:
            break   # go to next step

    previous_txids = set()
    while True:
        all_txids = set(rpc_connection.getrawmempool())

        #print(f'{all_txids=} {type(all_txids)=}')
        #print(f'{len(all_txids)=} {type(all_txids)=}')

        if previous_txids:
            added_txids = all_txids - previous_txids
            removed_txids = previous_txids - all_txids

            print(f'{len(all_txids)=:6} {len(added_txids)=:6} {len(removed_txids)=:6}')
            if len(removed_txids) > 0:
                print(f'    {removed_txids=}')
                print(f'    TRANSACTION REMOVED: {len(removed_txids)=}')
                # need to check why each transaction was removed
        else:
            print('FIRST in loop')

        previous_txids = all_txids
        time.sleep(28)  # 30 not working, default timeout in AuthServiceProxy


if __name__ == "__main__":
    main()
