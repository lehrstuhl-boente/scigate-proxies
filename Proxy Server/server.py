from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
#import entscheidsuche
from boris import Boris
from zora import Zora
from swisscovery import Swisscovery
from entscheidsuche import Entscheidsuche

hostName = ""
serverPort = 8080
zora=Zora()
swisscovery=Swisscovery()
boris=Boris()
entscheidsuche=Entscheidsuche()

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		with open("index.html") as f:
			lines = f.readlines()
		f.close()
		for i in lines:
			self.wfile.write(bytes(i, "utf-8"))

	def do_POST(self):
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		reply={}
		if self.headers.get("Content-type").lower()=="application/json":
			data = self.rfile.read(int(self.headers.get('Content-Length')))
			sdata=json.loads(data)
			if 'engine' in sdata:
				engine=sdata['engine']
				if engine=='entscheidsuche':
					reply=entscheidsuche.execute(sdata)
				elif engine=='boris':
					reply=boris.execute(sdata)
				elif engine=='zora':
					reply=zora.execute(sdata)
				elif engine=='swisscovery':
					reply=swisscovery.execute(sdata)
				else:
					reply['error']='engine '+engine+' unknown'
		else:
			reply['error']='no engine specified'
		if 'error' in reply:
			reply['status']='error'
		else:
			reply['status']='ok'
		self.wfile.write(bytes(json.dumps(reply),'utf-8'))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

