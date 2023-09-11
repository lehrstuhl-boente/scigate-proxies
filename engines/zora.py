from adapter import Adapter
import requests
import json

class Zora(Adapter):
	id="zora"
	name="Zora"
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
	host="https://www.zora.uzh.ch"
	suchpfad="/cgi/zora/es-zora-proxy"
	dokumentpfad="/id/eprint/"
	
	def __init__(self):
		super().__init__(self.name)
		
	def request(self, suchstring, filters='', start=0,count=Adapter.LISTSIZE):
		zora_filters = []
		if filters:
			for filter in filters:
				if filter['id'] == 'discipline':
					discipline_mappings = { 'law': '340 Recht' }
					discipline_filters = []
					for option in filter['options']:
						if option == 'unknown':
							if len(filter['options']) == 1: # unknown is the only selected option
								self.addcache(self.cachekey,start,0,[])
								return
							else:
								continue	# just ignore it
						if option not in discipline_mappings.keys(): continue
						discipline_filters.append({ "term": { "agg_dewey_de": discipline_mappings[option] } })
					zora_filters.append({
						'bool': {
							'should': discipline_filters
						}
					})
				elif filter['id'] == 'language':
					pass
				elif filter['id'] == 'availability':
					pass
				elif filter['id'] == 'date':
					pass
		# count is only a recommendation
		body={
			"highlight": {
				"fragment_size":400,
				"number_of_fragments":1,
				"fields": {
					"metadata.eprint.title.*": {
						"number_of_fragments":1,
						"fragment_size":400
					},
					"metadata.eprint.abstract.*": {
						"number_of_fragments":1,
						"fragment_size":400
					},
					"fulltext.eprint.fulltext.*": {
						"number_of_fragments":1,
						"fragment_size":400
					},
					"citation.eprint.*": {
						"number_of_fragments":1,
						"fragment_size":10000
					}
				}
			},
			"_source": [
				"id",
				"fulltext.eprint.security",
				"metadata.eprint.title",
				"citation.eprint.es_title",
				"citation.eprint.es_publication",
				"citation.eprint.es_contributors"
			],
			"aggs":{},
			"export_plugin_selected": "false",
			"query": {
				"bool": {
					"must": [
						{
							"query_string": {
								"query": suchstring,
								"default_operator": "AND"
							}
						},
						{
							"nested": {
								"path": "metadata.eprint.eprint_status",
								"query": {
									"bool": {
										"must": [
											{
												"term": {
													"metadata.eprint.eprint_status.key": "archive"
												}
											}
										]
									}
								}
							}
						}
					],
					"filter": zora_filters
				}
			},
			"size": count,
			"from": start
		}
		response=requests.post(url=self.host+self.suchpfad, headers=self.headers, data=json.dumps(body))
		if response.status_code >= 300:
			return "http-response: "+str(response.status_code)
		rs=json.loads(response.text)
		if not 'hits' in rs:
			return "no valid response"
		treffer=rs['hits']['total']['value']
		trefferliste=[]
		for dokument in rs['hits']['hits']:
			zeile2=dokument['_source']['proxy_title'].encode('raw_unicode_escape').decode('utf-8')
			zeile1=(", ".join(dokument['_source']['agg_name_key'])).encode('raw_unicode_escape').decode('utf-8')
			zeile3=""
			if 'highlight' in dokument:
				for h in dokument['highlight']:
					if 0 in dokument['highlight'][h]:
						zeile3=dokument['highlight'][h][0]
						break
			url=self.host+self.dokumentpfad+dokument['_id']+"/"
			trefferliste.append({
				'engineId': self.id,
				'description': [zeile1, zeile2, zeile3],
				'url': url
			})
		self.addcache(self.cachekey,start,treffer,trefferliste)