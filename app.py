#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
from urlparse import urlparse, parse_qs
import threading
import argparse
import re
import cgi
import caffe_wrapper.forward as nsfw
#import models.open_nsfw as nsfw
import ast

class HTTPRequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    if None != re.search('/open-nsfw/*', self.path):
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()

      content_len = int(self.headers.getheader('content-length', 0))
      post_body = self.rfile.read(content_len)
      input = ast.literal_eval(post_body)
      yHat = nsfw.run(input, "image", (256, 256, 3))

      self.wfile.write('[%s]' % ','.join(str(e) for e in yHat))
    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    return
 
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  allow_reuse_address = True
 
  def shutdown(self):
    self.socket.close()
    HTTPServer.shutdown(self)
 
class SimpleHttpServer():
  def __init__(self, ip, port):
    self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)
 
  def start(self):
    self.server_thread = threading.Thread(target=self.server.serve_forever)
    self.server_thread.daemon = True
    self.server_thread.start()
 
  def waitForThread(self):
    self.server_thread.join()
 
  def addRecord(self, recordID, jsonEncodedRecord):
    LocalData.records[recordID] = jsonEncodedRecord
 
  def stop(self):
    self.server.shutdown()
    self.waitForThread()
 
if __name__=='__main__':
  server = SimpleHttpServer("", 80)
  print 'Magic happens on port 80'
  server.start()
  server.waitForThread()
