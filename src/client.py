#!/usr/bin/env python
"""
Simple client for testing ( windows, use wget in linux :)
"""

import httplib
import sys

#get http server ip
http_server = "127.0.0.1:8000"
if (len(sys.argv) == 2 ):
    http_server = sys.argv[1]
#create a connection
conn = httplib.HTTPConnection(http_server)

while 1:
    cmdStr = raw_input('input command (ex. GET index.html): ')
    cmd = cmdStr.split()

    if cmd[0] == 'exit': #tipe exit to end it
        break
    
    #request command to server
    conn.request(cmd[0], cmdStr[len(cmd[0]):])

    #get response from server
    rsp = conn.getresponse()
    
    #print server response and data
    print(rsp.status, rsp.reason)
    data_received = rsp.read()
    print(data_received)
    
conn.close()