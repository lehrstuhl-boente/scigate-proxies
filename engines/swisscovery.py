from adapter import Adapter
import requests
import json
import urllib
import re

class Swisscovery(Adapter):
	id="swisscovery"
	name="Swisscovery"
	headers={
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
		'Accept': '*/*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'Referer': 'https://swisscovery.slsp.ch',
		'content-type': 'application/json',
		'Origin': 'https://swisscovery.slsp.ch',
		'Connection': 'keep-alive',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin'
	}
	host="https://swisscovery.slsp.ch"
	suchpfad="/primaws/rest/pub/pnxs"
	#arguments="?blendFacetsSeparately=false&came_from=addFacet&citationTrailFilterByAvailability=true&disableCache=false&getMore=0&inst=41SLSP_NETWORK&lang=fr&limit={count}&multiFacets=facet_lang,include,ger&newspapersActive=false&newspapersSearch=false&offset={start}&pcAvailability=false&q=any,contains,{suchterm}&qExclude=&qInclude=&rapido=true&refEntryActive=true&rtaLinks=true&scope=DN_and_CI&searchInFulltextUserSelection=true&skipDelivery=Y&sort=rank&tab=41SLSP_NETWORK&vid=41SLSP_NETWORK:VU1_UNION"
	arguments="?blendFacetsSeparately=false&citationTrailFilterByAvailability=true&disableCache=false&getMore=0&inst=41SLSP_NETWORK&lang=de&limit={count}&newspapersActive=false&newspapersSearch=false&offset={start}&pcAvailability=false&q=any,contains,{suchterm}&qExclude=&qInclude=&rapido=true&refEntryActive=true&rtaLinks=true&scope=DN_and_CI&searchInFulltextUserSelection=true&skipDelivery=Y&sort=rank&tab=41SLSP_NETWORK&vid=41SLSP_NETWORK:VU1_UNION"
	dokumentpfad="/discovery/fulldisplay?docid={docid}&context={context}&vid=41SLSP_NETWORK:VU1_UNION&lang=de&search_scope=DN_and_CI&adaptor=Local%20Search%20Engine&tab=41SLSP_NETWORK"
	reDoppelklammern=re.compile("(?:<<|>>)")

	def __init__(self):
		super().__init__(self.name)

	def request(self, suchstring, filters='', start=0, count=Adapter.LISTSIZE):
		if filters:
			for filter in filters:
				if filter['id'] == 'discipline':
					if 'unknown' not in filter['options']:
						self.addcache(self.cachekey,start,0,[])
						return
				elif filter['id'] == 'language':
					language_mappings = { 'unknown': 'und', 'de': 'ger', 'fr': 'fre', 'en': 'eng', 'it': 'ita' }
					valid_option = False
					for option in filter['options']:
						if option not in language_mappings: continue
						self.arguments += f'&multiFacets=facet_lang,include,{language_mappings[option]}'
						valid_option = True
					if not valid_option:
						self.addcache(self.cachekey,start,0,[])
						return
				elif filter['id'] == 'availability':
					if 'freeOnlineAvailable' in filter['options']:
						self.arguments += '&multiFacets=facet_tlevel,include,open_access'
					else:
						self.addcache(self.cachekey,start,0,[])
						return
				elif filter['id'] == 'year':	# TODO: implement year filter
					pass

		# count is only a recommendation
		urlsuchstring=urllib.parse.quote_plus(suchstring)
		argumente=self.arguments.format(count=count, start=start, suchterm=urlsuchstring)	
		response=requests.get(url=self.host+self.suchpfad+argumente, headers=self.headers)
		if response.status_code >= 300:
			return "http-response: "+str(response.status_code)
		rs=json.loads(response.text)
		if not 'info' in rs:
			return "no valid response"
		treffer=rs['info']['total']
		trefferliste=[]
		for dokument in rs['docs']:
			zeile1=""
			zeile2=""
			zeile3=""
			if 'sort' in dokument['pnx']:
				if 'title' in dokument['pnx']['sort']:
					zeile1=self.reDoppelklammern.sub("",dokument['pnx']['sort']['title'][0])
				if 'author' in dokument['pnx']['sort']:
					zeile2=dokument['pnx']['sort']['author'][0]

			if 'addata' in dokument['pnx']:
				if 'btitle' in dokument['pnx']['addata']:
					zeile3=dokument['pnx']['addata']['btitle'][0]
				elif 'date' in dokument['pnx']['addata']:
					zeile3=dokument['pnx']['addata']['date'][0]
					
			docid=dokument['pnx']['control']['recordid'][0]
			context="XXX"
			if 'context' in dokument:
				context=dokument['context']
			else:
				print("Fehler: "+json.dumps(dokument))
			url=self.host+self.dokumentpfad.format(docid=docid, context=context)
			trefferliste.append({
				'engineId': self.id,
				'description': [zeile1, zeile2, zeile3],
				'url': url
			})
		self.addcache(self.cachekey,start,treffer,trefferliste)