from adapter import Adapter
import requests
import json

class Zora(Adapter):
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
		
	def suche(self, suchstring):
		body={"highlight":{"fragment_size":400,"number_of_fragments":1,"fields":{"metadata.eprint.title.*":{"number_of_fragments":1,"fragment_size":400},"metadata.eprint.abstract.*":{"number_of_fragments":1,"fragment_size":400},"fulltext.eprint.fulltext.*":{"number_of_fragments":1,"fragment_size":400},"citation.eprint.*":{"number_of_fragments":1,"fragment_size":10000}}},"_source":["id","fulltext.eprint.security","metadata.eprint.title","citation.eprint.es_title","citation.eprint.es_publication","citation.eprint.es_contributors"],"aggs":{},"export_plugin_selected":"false","query":{"bool":{"must":[{"query_string":{"query":suchstring,"default_operator":"AND"}},{"nested":{"path":"metadata.eprint.eprint_status","query":{"bool":{"must":[{"term":{"metadata.eprint.eprint_status.key":"archive"}}]}}}}],"filter":[{"bool":{"should":[{"term":{"agg_dewey_en":"340 Law"}}],"minimum_should_match":1}}]}},"size":10}
		response=requests.post(url=self.host+self.suchpfad, headers=self.headers, data=json.dumps(body))
		rs=json.loads(response.text)
		treffer=rs['hits']['total']['value']
		return "ok", "", treffer
		
	def treffer(self, suchstring, start, count):
		body={"highlight":{"fragment_size":400,"number_of_fragments":1,"fields":{"metadata.eprint.title.*":{"number_of_fragments":1,"fragment_size":400},"metadata.eprint.abstract.*":{"number_of_fragments":1,"fragment_size":400},"fulltext.eprint.fulltext.*":{"number_of_fragments":1,"fragment_size":400},"citation.eprint.*":{"number_of_fragments":1,"fragment_size":10000}}},"_source":["id","fulltext.eprint.security","metadata.eprint.title","citation.eprint.es_title","citation.eprint.es_publication","citation.eprint.es_contributors"],"aggs":{},"export_plugin_selected":"false","query":{"bool":{"must":[{"query_string":{"query":suchstring,"default_operator":"AND"}},{"nested":{"path":"metadata.eprint.eprint_status","query":{"bool":{"must":[{"term":{"metadata.eprint.eprint_status.key":"archive"}}]}}}}],"filter":[{"bool":{"should":[{"term":{"agg_dewey_en":"340 Law"}}],"minimum_should_match":1}}]}},"size":count,"from":start}
		response=requests.post(url=self.host+self.suchpfad, headers=self.headers, data=json.dumps(body))
		rs=json.loads(response.text)
		trefferliste=[]
		for dokument in rs['hits']['hits']:
			zeile1=dokument['_source']['proxy_title']
			zeile2=", ".join(dokument['_source']['agg_name_key'])
			zeile3=""
			if 'highlight' in dokument:
				for h in dokument['highlight']:
					if 0 in dokument['highlight'][h]:
						zeile3=dokument['highlight'][h][0]
						break
			url=self.host+self.dokumentpfad+dokument['_id']+"/"
			trefferliste.append({'description':[zeile1, zeile2, zeile3],'url': url})
		return "ok", "", trefferliste