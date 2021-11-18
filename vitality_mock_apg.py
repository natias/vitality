from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import socketserver

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True

httpd = ThreadedHTTPServer(('localhost', 4443), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="certs/mock/key.pem", 
        certfile='certs/mock/cert.pem', server_side=True)

httpd.serve_forever()
