from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from config import config as c

rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(c.rpc_user, c.rpc_password))

best_block_hash = rpc_connection.getbestblockhash()
print(f'{best_block_hash=}')