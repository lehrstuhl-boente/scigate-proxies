from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import json
from adapter import Adapter
from engines.boris import Boris
from engines.zora import Zora
from engines.swisscovery import Swisscovery
from engines.entscheidsuche import Entscheidsuche
from engines.fedlex import Fedlex
from engines.repositorium import Repositorium
from engines.swisslexGreen import SwisslexGreen
from engines.legalanthology import Legalanthology
from engines.digitalisierungszentrum import Digitalisierungszentrum
from engines.gotriple import GoTriple
from engines.iurisprudentia import Iurisprudentia

hostName=""
serverPort=8080

class MyServer(BaseHTTPRequestHandler):
	def do_OPTIONS(self):
		self.send_response(204,"ok")
		self.send_header('Access-Control-Allow-Credentials', 'true')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type, Origin, Accept")
		self.send_header("Access-Control-Max-Age", "86400")
		self.end_headers()
		
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
		self.send_header("Content-type", "application/json; charset=utf-8")
		self.send_header("Access-Control-Allow-Origin", "*")
		self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
		self.send_header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS')
		self.end_headers()
		reply={}
		if "application/json" in self.headers.get("Content-type").lower():
			data = self.rfile.read(int(self.headers.get('Content-Length')))
			sdata=json.loads(data)
			if 'engine' in sdata:
				engines = [
					Zora(),
					Swisscovery(),
					Boris(),
					Entscheidsuche(),
					Fedlex(),
					Repositorium(),
					SwisslexGreen(),
					Legalanthology(),
					Digitalisierungszentrum(),
					GoTriple(),
					Iurisprudentia()
				]
				engineUnknown = True
				engine: Adapter	# type hint
				for engine in engines:
					if engine.id == sdata['engine']:
						reply = engine.execute(sdata)
						engineUnknown = False
						break
				if engineUnknown:
					reply['error'] = 'engine ' + sdata['engine'] + ' unknown'
		else:
			reply['error']='unexpected Content-type: '+self.headers.get("Content-type")
		if 'error' in reply:
			reply['status']='error'
		else:
			reply['status']='ok'
		string=json.dumps(reply, ensure_ascii=False).encode('utf8')
		self.wfile.write(string)
		
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    #server.serve_forwever()
    
if __name__ == "__main__":        
    webServer = ThreadedHTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


