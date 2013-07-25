"""
Simple Server implementation , mostly taken from internet examples ( SimpleHttpServer )
Http interface based exact on api provided in exercise definition ( including typos)
"""

import sys
import BaseHTTPServer
from logging import info, error, exception

import logging.config
logging.config.fileConfig('logging.conf')

from BaseHTTPServer import BaseHTTPRequestHandler

Protocol   = "HTTP/1.0"

import urlparse

from pytwitterme.facade import PyTwitterMeFacade
facade = PyTwitterMeFacade()

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            o = urlparse.urlparse(self.path)
            cmdName = o.path.replace("/","")
            params = urlparse.parse_qs(o.query)
        except Exception as ex:
            exception(ex)
            self.send_error(404,'Failed to parse url: %s' % self.path)
            return

        try:
            if  cmdName == "CreateUser" :
                self.send_Response(  facade.createUser( params["UserName"][0] ) )
            elif cmdName == "PostMessage":
                self.send_Response(  facade.postMessage( params["UserId"][0], params["MessageText"][0] ) )
            elif cmdName == "Follow":
                self.send_Response(  facade.follow( params["FollowingUser"][0], params["FollowedUser"][0] ) )
            elif cmdName == "Unfollow":
                self.send_Response(  facade.unfollow( params["FollwingUser"][0], params["UnfollowedUser"][0] ) )
            elif cmdName == "GetFeed":
                self.send_Response(  facade.getFeed( params["ForUserId"][0] ) )
            elif cmdName == "GetGlobalFeed":
                self.send_Response(  facade.getGlobalFeed() )
            else:
                 self.send_error(404,'Non Supported command: %s' % self.path)
            return
        except Exception as ex:
            error( 'Failed to execute: %s  %s  from %s' % (cmdName, params, self.path))
            exception(ex)
            self.send_error(404,'Failed to execute: %s  %s  from %s' % (cmdName, params, self.path))


    def send_Response(self, response):
        self.send_response(200)
        self.send_header('Content-type',	'text/html')
        self.end_headers()
        self.wfile.write( str( response) )


    def do_POST(self):
       pass



def main():
    if len( sys.argv) ==3:
        server_address = ( sys.argv[1],  int(sys.argv[2]))
    else:
        server_address = ('127.0.0.1', 8000)


    MyHandler.protocol_version = Protocol
    httpd =  BaseHTTPServer.HTTPServer(server_address, MyHandler)

    sa = httpd.socket.getsockname()
    info( "Serving HTTP on %s port %s..." %( sa[0],  sa[1])  )

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        error( '^C received, shutting down server')
        httpd.socket.close()

if __name__ == '__main__':
    main()


