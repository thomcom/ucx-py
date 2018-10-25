# Copyright (c) 2018, NVIDIA CORPORATION. All rights reserved.
# See file LICENSE for terms.

import call_myucp as ucp
import time
import argparse
import pickle
import sys

def send_recv(ep, msg_log, is_server, is_cuda):
    my_list = []
    obj_bytes = None
    if 1 == is_server:
        my_list = [1, 2, 3, 4]
        print('sender :' + str(my_list))
        obj_bytes = pickle.dumps(my_list)
        ep.send_pickle(obj_bytes, sys.getsizeof(obj_bytes))
    else:
        my_list = [5, 6, 7, 8]
        print('receiver :' + str(my_list))
        obj_bytes = pickle.dumps(my_list)
        ep.recv_pickle(obj_bytes, sys.getsizeof(obj_bytes))
    ep.wait_pickle()
    my_new_list = pickle.loads(obj_bytes)
    print('new :' + str(my_new_list))

accept_cb_started = 0
new_client_ep = None

def server_accept_callback(client_ep):
    global accept_cb_started
    global new_client_ep
    print("in python accept callback")
    new_client_ep = client_ep
    accept_cb_started = 1

max_msg_log = 23
parser = argparse.ArgumentParser()
parser.add_argument('-s','--server', help='enter server ip', required=False)
parser.add_argument('-p','--port', help='enter server port number', required=False)
args = parser.parse_args()

## initiate ucp
init_str = ""
is_server = 0
if args.server is None:
    is_server = 1
else:
    is_server = 0
    init_str = args.server

## setup endpoints
ucp.init(init_str.encode(), server_accept_callback, is_server, server_listens = 1)
server_ep = None
if 0 == is_server:
    #connect to server
    server_ep = ucp.get_endpoint(init_str.encode(), int(args.port))
    is_cuda = False
    send_recv(server_ep, max_msg_log, is_server, is_cuda)
    is_cuda = True
    send_recv(server_ep, max_msg_log, is_server, is_cuda)
else:
    while 0 == accept_cb_started:
        ucp.ucp_progress()
    assert new_client_ep != None
    is_cuda = False
    send_recv(new_client_ep, max_msg_log, is_server, is_cuda)
    is_cuda = True
    send_recv(new_client_ep, max_msg_log, is_server, is_cuda)

if 1 == is_server:
    assert new_client_ep != None
    ucp.destroy_ep(new_client_ep)
else:
    ucp.destroy_ep(server_ep)

if args.server is None:
    print("Server Finalized")
else:
    print("Client Finalized")
