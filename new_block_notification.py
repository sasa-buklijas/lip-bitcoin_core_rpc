import zmq
import struct
import platform
import os
import time
import datetime as dt
from bitcoinrpc.authproxy import AuthServiceProxy
from config import config as c


def main():
    print(f'{os.getpid()=}')
    my_os = platform.system()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:29000")  
    # Subscribe to "pubhashblock" messages
    socket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")

    print("Subscribed to pubhashblock messages. Waiting for messages...")
    previous_block_time = None
    while True:
        topic, body, seq = socket.recv_multipart()  # blocking, until something(pubhashblock) is in ZeroMQ
        current_time = time.time()
        #print(f'{type(topic)=} {type(body)=} {type(seq)=}')
        #print(f'{topic=} {body=} {seq=}')
        sequence = str(struct.unpack('<I', seq)[-1])

        print('- HASH BLOCK ('+sequence+') -')
        print(body.hex())

        rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(c.rpc_user, c.rpc_password))
        block = rpc_connection.getblock(body.hex())
        stats = rpc_connection.getblockstats(body.hex())
        print(f'{str(block)[0:1000]}')
        print(stats)
        block_height = block['height']
        block_nTx = block['nTx']
        block_MB = float(block['size'])/1024/1024
        block_weight = float(block['weight'])/4_000_000*100
        block_time = block['time']
        block_mediantime = block['mediantime']
        #print(f'{current_time=} - {datetime.utcfromtimestamp(current_time).strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'{current_time=} - {dt.datetime.fromtimestamp(current_time, dt.UTC).strftime("%Y-%m-%d %H:%M:%S")}')
        #print(f'{block_time=} - {datetime.utcfromtimestamp(block_time).strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'{block_time=} - {dt.datetime.fromtimestamp(block_time, dt.UTC).strftime("%Y-%m-%d %H:%M:%S")}')
        #print(f'{block_mediantime=} - {datetime.utcfromtimestamp(block_mediantime).strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'{block_mediantime=} - {dt.datetime.fromtimestamp(block_mediantime, dt.UTC).strftime("%Y-%m-%d %H:%M:%S")}')
        min_fee_rate = stats['minfeerate']
        median_fee_rate = stats['feerate_percentiles'][2]
        avg_fee_rate = stats['avgfeerate']

        #print(f'{block_MB=} {block_weight=} ')
        block_template = ''
        if block_nTx == 1:
            block_template = '- IS_TEMPLATE '

        #if previous_block_time is None:
        #    seconds_since_previous_block = current_time - block_time 
        #else:
        #    seconds_since_previous_block = current_time - previous_block_time

        # human readable time since previous block
        human_time_since_previous_block = ''
        if previous_block_time:
            seconds_since_previous_block = current_time - previous_block_time

            if seconds_since_previous_block < 60:  
                human_time_since_previous_block = f'- {seconds_since_previous_block:.0f} sec' 
            else:
                minutes = seconds_since_previous_block // 60
                seconds = seconds_since_previous_block % 60
                human_time_since_previous_block = f'- {minutes:.0f} min {seconds:.0f} sec'

        # OS specific notification 
        if my_os == 'Darwin':  # OSX
            title = f'Block {block_height} {human_time_since_previous_block}'
            msg = f'{block_MB:.2f} MB ({block_weight:.2f}%) - {block_nTx} tx {block_template}- {min_fee_rate}/{median_fee_rate}/{avg_fee_rate} sat/vB'
            print(f'{title=}')
            print(f'{msg=}')
            print()
            os.system(f"osascript  -e 'display notification \"{msg}\" with title \"{title}\"'")

        previous_block_time = current_time


if __name__ == "__main__":
    main()