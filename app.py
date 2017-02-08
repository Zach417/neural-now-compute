#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
from urlparse import urlparse, parse_qs
import threading
import argparse
import re
import cgi
import models.open_nsfw as nsfw

class HTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if None != re.search('/api/v1/run/*', self.path):
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()

      img_url = parse_qs(urlparse(self.path).query)['url'][0]
      yHat = nsfw.run(img_url)
      self.wfile.write({"prediction":yHat})
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
