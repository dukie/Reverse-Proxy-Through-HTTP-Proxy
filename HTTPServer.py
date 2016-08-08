#!/usr/bin/env python
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import requests

PROXIES_DICT = {
    'http': 'http://login:password@address:port',
    'https': 'http://login:password@address:port'
}

AMAZON_EP = "https://s3-ap-northeast-1.amazonaws.com"

CHUNK_SIZE = 1024
PROTOCOL = 'HTTP/1.1'


class MyRequestHandler(BaseHTTPRequestHandler):
    def standard_response_builder(self, response):
        self.send_response(response.status_code)
        is_chunk = False
        for (key, value) in response.headers.items():
            if value == 'chunked':
                is_chunk = True
                print "!!!!!!!!!!!!!!!!"
            self.send_header(key, value)
        self.end_headers()
        if is_chunk:
            for chunk in response.iter_content(CHUNK_SIZE):
                hex_chunk_length = '%X\r\n' % len(chunk)
                print hex_chunk_length
                self.wfile.write("{0}{1}\r\n".format(hex_chunk_length.lower(), chunk))

            self.wfile.write('0\r\n\r\n')
        else:
            for chunk in response.iter_content(CHUNK_SIZE):
                self.wfile.write(chunk)
        return

    def do_GET(self):

        with requests.Session() as http_session:
            http_session.proxies = PROXIES_DICT

            headers = self.headers.dict
            headers['host'] = 's3-ap-northeast-1.amazonaws.com'
            response = requests.get(AMAZON_EP + self.path,
                                    headers=headers,
                                    stream=True,
                                    proxies=PROXIES_DICT,
                                    verify=False
                                    )
            return self.standard_response_builder(response)

    def do_PUT(self):
        with requests.Session() as http_session:
            http_session.proxies = PROXIES_DICT

            headers = self.headers.dict
            headers['host'] = 's3-ap-northeast-1.amazonaws.com'
            length = int(self.headers.getheader('content-length'))
            ff = self.rfile.read(length)
            response = requests.put(AMAZON_EP + self.path,
                                    data=ff,
                                    headers=headers,
                                    stream=True,
                                    proxies=PROXIES_DICT,
                                    verify=False
                                    )

            return self.standard_response_builder(response)

    def do_POST(self):
        with requests.Session() as http_session:
            http_session.proxies = PROXIES_DICT

            headers = self.headers.dict
            headers['host'] = 's3-ap-northeast-1.amazonaws.com'
            length = int(self.headers.getheader('content-length'))
            ff = self.rfile.read(length)
            response = requests.post(AMAZON_EP + self.path,
                                     data=ff,
                                     headers=headers,
                                     stream=True,
                                     proxies=PROXIES_DICT,
                                     verify=False
                                     )

            return self.standard_response_builder(response)

    def do_HEAD(self):
        with requests.Session() as http_session:
            http_session.proxies = PROXIES_DICT

            headers = self.headers.dict
            headers['host'] = 's3-ap-northeast-1.amazonaws.com'
            response = requests.head(AMAZON_EP + self.path,
                                     headers=headers,
                                     stream=True,
                                     proxies=PROXIES_DICT,
                                     verify=False
                                     )
        self.send_response(response.status_code)
        for (key, value) in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        for chunk in response.iter_content(CHUNK_SIZE):
            self.wfile.write(chunk)
        return

    def do_DELETE(self):
        with requests.Session() as http_session:
            http_session.proxies = PROXIES_DICT

            headers = self.headers.dict
            headers['host'] = 's3-ap-northeast-1.amazonaws.com'
            response = requests.delete(AMAZON_EP + self.path,
                                       headers=headers,
                                       stream=True,
                                       proxies=PROXIES_DICT,
                                       verify=False
                                       )

            return self.standard_response_builder(response)

    def send_response(self, code, message=None):
        """Send the response header and log the response code.
        Also send two standard headers with the server software
        version and the current date.
        """
        self.request_version = PROTOCOL
        self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s %d %s\r\n" %
                             (self.protocol_version, code, message))


class ThreadedHTTPServer(SocketServer.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


Handler = MyRequestHandler
Handler.protocol_version = PROTOCOL
server = ThreadedHTTPServer(('0.0.0.0', 8081), Handler)

server.serve_forever()
