from adapter import Adapter
import requests
import json
import urllib
import re
import time
import datetime

class Entscheidsuche(Adapter):
	id="entscheidsuche"
	name="Entscheidsuche"
	headers={
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
		'Accept': '*/*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'Referer': 'https://www.zora.uzh.ch/search/?q=test&size=n_10_n',
		'content-type': 'application/json',
		'Origin': 'https://www.zora.uzh.ch',
		'Connection': 'keep-alive',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin'
	}
	host="https://entscheidsuche.pansoft.de:9200"
	suchpfad="/entscheidsuche-*/_search"
	dokumentpfad="/id/eprint/"
	reStrip=re.compile(r"<br>")
	
	def __init__(self):
		super().__init__(self.name)
		
	def request(self, suchstring, filters='', start=0, count=Adapter.LISTSIZE):
		filter_object = []
		if filters:
			for filter in filters:
				if filter['id'] == 'language':
					options = filter['options']
					if 'unknown' in options:
						options.remove('unknown')
					filter_object.append({
						'terms': {
							'attachment.language': options
						}
					})
				elif filter['id'] == 'date':
					base = { 'range': { 'date': {} } }
					if filter['from'] != '':
						date_string = f"01.01.{filter['from']}"
						date_object = datetime.datetime.strptime(date_string, '%d.%m.%Y')
						date_object = date_object.replace(tzinfo=datetime.timezone.utc)
						timestamp = datetime.datetime.timestamp(date_object)	# timestamp in seconds
						base['range']['date']['gte'] = int(timestamp)*1000	# convert to milliseconds
					if filter['to'] != '':
						date_string = f"31.12.{filter['to']}"
						date_object = datetime.datetime.strptime(date_string, '%d.%m.%Y')
						date_object = date_object.replace(tzinfo=datetime.timezone.utc)
						timestamp = datetime.datetime.timestamp(date_object)
						base['range']['date']['lte'] = int(timestamp)*1000
					filter_object.append(base)
		body = {
			"size": count,
			"_source": {
				"excludes": ["attachment.content"]
			},
			"track_total_hits": True,
			"query": {
				"bool": {
					"filter": filter_object,
					"must": {
						"query_string": {
							"query": suchstring,
							"default_operator": "AND",
							"type":"cross_fields",
							"fields": ["title.*^5", "abstract.*^3", "meta.*^10", "attachment.content", "reference^3"]
						}
					}
				}
			},
			"sort": [
				{ "_score": "desc" },
				{ "id": "desc" }
			],
			"from": start
		}
		cachekey=suchstring+'#'
		# Wenn der letzte Eintrag davor bekannt ist, "search_after" verwenden.
		if start>0 and cachekey in self.cache:
			treffercache=self.cache[cachekey].trefferliste
			if start-1 in treffercache:
				sort = treffercache[start-1]['sort']
				body['from'] = 0
				body['search_after'] = sort
        #"filter":[{"terms":{"attachment.language":["de"]}},{"terms":{"hierarchy":["AG"]}},{"range":{"date":{"lte":1509015759293}}}]}}
        #"filters":"{"language":{"type":"language","payload":["de"]},"hierarchie":{"type":"hierarchie","payload":["CH"]}}"
		response=requests.post(url=self.host+self.suchpfad, headers=self.headers, data=json.dumps(body))
		if response.status_code >= 300:
			return "http-response: "+str(response.status_code)
		rs=json.loads(response.text)
		if not 'hits' in rs:
			return "no valid response"
		treffer=rs['hits']['total']['value']
		trefferliste=[]
		for dokument in rs['hits']['hits']:
			zeile1=self.reStrip.sub(" ",dokument['_source']['title']['de'])
			if 'abstract' in dokument['_source']: zeile2=self.reStrip.sub(" ",dokument['_source']['abstract']['de'])
			else: zeile2=""
			zeile3=""
			sort=dokument['sort']
			url="https://entscheidsuche.ch/view/"+dokument['_id']
			trefferliste.append({
				'engineId': self.id,
				'description':[zeile1, zeile2, zeile3],
				'url': url,
				'sort': sort
			})
		self.addcache(suchstring+'#',start,treffer,trefferliste)
		return	
