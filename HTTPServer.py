#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler

import requests

PROXIES_DICT = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

AMAZON_EP = "http://s3-ap-northeast-1.amazonaws.com"


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with requests.Session() as http_session:
            http_session.proxies = PROXIES_DICT

            headers = self.headers.dict
            headers['host'] = 's3-ap-northeast-1.amazonaws.com'
            response = requests.get(AMAZON_EP + self.path,
                                    headers=headers,
                                    stream=True
                                    )
        self.send_response(response.status_code)
        chunked = False
        for (key, value) in response.headers.items():
            if value == 'chunked':
                chunked = True
                print "!!!!!!!!!!!!!!!!"
            self.send_header(key, value)

        self.end_headers()
        if chunked:
            for chunk in response.iter_content(6780):
                hexstring = '%.4X' % len(chunk)
                print hexstring
                self.wfile.write("{0}\r\n{1}".format(hexstring.lower(), chunk))

            self.wfile.write('\r\n0\r\n\r\n')
        else:
            self.wfile.write(response.text)
        return

    def do_PUT(self):
        with requests.Session() as http_session:
            http_session.proxies = PROXIES_DICT

            headers = self.headers.dict
            headers['host'] = 's3-ap-northeast-1.amazonaws.com'
            response = requests.put(AMAZON_EP + self.path,
                                    data='aaaaa',
                                    headers=headers,
                                    stream=True
                                    )
            print response
        self.send_response(response.status_code)
        chunked = False
        for (key, value) in response.headers.items():
            if value == 'chunked':
                chunked = True
                print "!!!!!!!!!!!!!!!!"
            self.send_header(key, value)

        self.end_headers()
        if chunked:
            for chunk in response.iter_content(6780):
                hexstring = '%.4X' % len(chunk)
                print hexstring
                self.wfile.write("{0}\r\n{1}".format(hexstring.lower(), chunk))

            self.wfile.write('\r\n0\r\n\r\n')
        else:
            self.wfile.write(response.text)
        return

    def do_HEAD(self):
        with requests.Session() as http_session:
            http_session.proxies = PROXIES_DICT

            headers = self.headers.dict
            headers['host'] = 's3-ap-northeast-1.amazonaws.com'
            response = requests.head(AMAZON_EP + self.path,
                                    headers=headers,
                                    stream=True
                                    )
            print response
        self.send_response(response.status_code)
        chunked = False
        for (key, value) in response.headers.items():
            if value == 'chunked':
                chunked = True
                print "!!!!!!!!!!!!!!!!"
            self.send_header(key, value)

        self.end_headers()
        if chunked:
            for chunk in response.iter_content(6780):
                hexstring = '%.4X' % len(chunk)
                print hexstring
                self.wfile.write("{0}\r\n{1}".format(hexstring.lower(), chunk))

            self.wfile.write('\r\n0\r\n\r\n')
        else:
            self.wfile.write(response.text)
        return

    def send_response(self, code, message=None):
        """Send the response header and log the response code.

        Also send two standard headers with the server software
        version and the current date.

        """
        self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s %d %s\r\n" %
                             (self.protocol_version, code, message))
            # print (self.protocol_version, code, message)


Handler = MyRequestHandler
Handler.protocol_version = 'HTTP/1.1'
server = SocketServer.TCPServer(('0.0.0.0', 8082), Handler)

server.serve_forever()
