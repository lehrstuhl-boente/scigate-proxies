from adapter import Adapter
import urllib
import requests
import json

class Repositorium(Adapter):
	id="repositorium"
	name="Repositorium"
	headers={
		"Accept": "application/json, text/plain, */*",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
		"Connection": "keep-alive"
	}
	host="https://ukatie.com"
	suchpfad="/api/v2/ask"
	arguments="?domainId=20275809-8c17-4f3d-a3f7-0657c1435e54&question={suchterm}"

	def __init__(self):
		super().__init__(self.name)

	def request(self, suchstring, filters='', start=0, count=Adapter.LISTSIZE):
		if filters:
			for filter in filters:
				if filter['id'] == 'discipline':
					if 'law' not in filter['options']:
						self.addcache(self.cachekey,start,0,[])
						return
				elif filter['id'] == 'language':
					if 'unknown' not in filter['options']:
						self.addcache(self.cachekey,start,0,[])
						return
				elif filter['id'] == 'availability':
					if 'freeOnlineAvailable' not in filter['options']:
						self.addcache(self.cachekey,start,0,[])
						return
				elif filter['id'] == 'date':
					if filter['from'] != '' or filter['to'] != '':
						self.addcache(self.cachekey,start,0,[])
						return

		urlsuchstring=urllib.parse.quote_plus(suchstring)
		argumente = self.arguments.format(suchterm=urlsuchstring)
		response=requests.get(url=self.host+self.suchpfad+argumente, headers=self.headers)

		if response.status_code >= 300:
			return 'http-response: ' + str(response.status_code)
    
		rs=json.loads(response.text)
		treffer=len(rs)
		trefferliste=[]
		for dokument in rs:
			dokumentAnswer = json.loads(dokument["answer"])

			zeile1=dokumentAnswer["Titel"]
      
			coauthors = dokumentAnswer["Coauthors"]
			coauthorsArray = []
			if coauthors is not None:
				for author in coauthors:
					coauthorsArray.append(author["coauthor_first"]+author["coauthor_last"])
			else:
				coauthorsArray.append("No Author Provided")
			zeile2=", ".join(coauthorsArray)

			zeile3="Publish date: "+dokumentAnswer["Erschienen_am"]+" | "+dokumentAnswer["Erschienen_in"]
			trefferliste.append({
				'engineId': self.id,
				"description": [zeile1, zeile2, zeile3],
				"url": "https://dev.repositorium.ch/Entry/"+str(dokumentAnswer["id"])
			})


		self.addcache(self.cachekey,start,treffer,trefferliste)