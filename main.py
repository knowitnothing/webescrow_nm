import os
import zmq
import json
from tornado import web, ioloop, httpserver

import ssss
import webcfg
import bitcoin

INVALID = json.dumps({'error': 'Invalid data'})
MISSING_EMAIL = json.dumps({'error': 'Email missing'})

class IndexHandler(web.RequestHandler):

    def initialize(self, sock):
        self.sock = sock

    def get(self):
        return self.render(os.path.join(webcfg.html_path, "index.html"))

    def post(self):
        # Validate input.
        try:
            data = json.loads(self.request.body)
        except Exception, e:
            print "POST failed: %s (%s)" % (e, self.request.body)
            self.write(INVALID)
            return
        try:
            n = int(data['n'])
            m = int(data['m'])
            if n < 2 or m < n:
                raise Exception("Invalid values for n,m")
        except Exception, e:
            print "POST failed: %s (%s, %s)" % (e, n, m)
            self.write(INVALID)
            return
        if 'email' not in data or '' in data['email']:
            self.write(MISSING_EMAIL)
            return
        for item in data['email']:
            if not isinstance(item, list) or len(item) != 2:
                self.write(INVALID)
                return
            if not item[0] or not item[1]:
                self.write(MISSING_EMAIL)
                return
            try:
                item[0] = item[0].encode('ascii')
                item[1] = item[1].encode('ascii')
            except Exception, e:
                print "Invalid email: %s" % e
                self.write(INVALID)
                return

        # Generate a new private key, and a bitcoin address from it.
        pk, wif_pk = bitcoin.privatekey()
        addr = bitcoin.address(pk)
        # Split the private key in m parts.
        shares = ssss.split(wif_pk, n, m)
        # Send the shares by email.
        for share, email in zip(shares, data['email']):
            self.sock.send_multipart([share, addr, email[0], email[1]])

        self.write(json.dumps({'success': addr}))

def setup_handler(main='/'):
    zmq_ctx = zmq.Context.instance()
    zmq_sock = zmq_ctx.socket(zmq.PUSH)
    zmq_sock.connect(webcfg.zmqemail)
    return (main, IndexHandler, dict(sock=zmq_sock))

def main():
    # Check that ssss-split exists.
    if not os.path.exists(webcfg.ssss_split):
        raise Exception("%s doesn't exist, check webcfg.py" % webcfg.ssss_split)

    static_handler = []
    if not webcfg.using_nginx:
        static_handler.append((r'/static/(.*)',
            web.StaticFileHandler, {'path': webcfg.static_path}))
    app = web.Application([setup_handler()] + static_handler)

    server = httpserver.HTTPServer(app, ssl_options=webcfg.ssl_conf)
    server.listen(webcfg.port, webcfg.host)
    print "Listening @ %s:%s" % (webcfg.host, webcfg.port)
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
