from adapter import Adapter
import requests
import json
import urllib
import re

class SwisslexGreen(Adapter):
	id="swisslexgreen"
	name="Swisslex Green"

	host="https://lexcampus.swisslex.ch"
	suchpfad="/api/retrieval/postSearch?sourceDetails=search-button"
	dokpfad="/de/doc/bookdoc/"
	headers={
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0',
		'Accept': 'application/json, text/plain, */*',
		'Accept-Language': 'de-CH',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/json',
		'Authenticated': 'false',
		'Origin': 'https://lexcampus.swisslex.ch',
		'DNT': '1',
		'Connection': 'keep-alive',
		'Referer': 'https://lexcampus.swisslex.ch/de/doc/bookdoc/dccd9ec9-9956-44a8-a550-3a38a3e7b61e/search/177362334',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache'
	}
	
	def __init__(self):
		super().__init__(self.name)
		
	def request(self, suchwort, filters='',start=0,count=Adapter.LISTSIZE):

		page=(int)(start/count+1)
		print("start", start)
		print("count", count)
		print("page:", page)
		skip = start-count*(page-1)
		body={"paging":{"CurrentPage":page,"HitsPerPage":count},"searchFilter":{"searchText":suchwort,"navigation":"","searchLanguage":1,"law":"","articleNumber":"","paragraph":"","subParagraph":"","dateFrom":"","dateUntil":"","reference":"","author":"","practiceAreaGroupsCriteria":[],"assetTypeGroupsCriteria":[],"thesaurusType":1,"userSearchFilterId":"","bookmarkSearchFilterId":"","thesaurusInformation":"","nSelected":0,"journalCriteria":[],"caseCollectionCriteria":[],"bookCriteria":[],"paging":{"CurrentPage":1,"HitsPerPage":25},"drillDownFilter":{"sortOrder":0},"expandedFacettes":[],"filterAggregationQuery":False,"expandReferences":True,"selectedParts":31,"portalLanguage":"de"},"refineFilter":{"aggregationsFilter":[],"transformationFilter":[],"retrievalSortByDate":False},"reRunTransactionID":"","sourceTransactionID":""}

		response=requests.post(url=self.host+self.suchpfad, data=json.dumps(body), headers=self.headers)
		if response.status_code >= 300:
			return "http-response: "+str(response.status_code)
		print(response.text)
		print("Skip: ",skip)
		#r=response.content
		#ru=r.decode("ascii")
		#rs=json.loads(ru.encode("utf-8"))
		print(response.text)
		rs=json.loads(response.text)
		if not 'hits' in rs:
			return "no valid response"
		treffer=rs['numberOfHits']
		trefferliste=[]
		print("Hits found:", treffer)
		for dokument in rs['hits']:
			if skip>0:
				skip-=1
			else:
				zeile1=dokument['title']
				zeile2=dokument['description']
				if 'authors' in dokument:
					zeile3=dokument['authors']
				else:
					zeile3=""	
				if 'bookTitle' in dokument:
					zeile3+=" "+dokument['bookTitle']
				if 'series' in dokument:
					zeile3+=" "+dokument['series']
				url=self.host+self.dokpfad+dokument['targetID']
				trefferliste.append({'description':[zeile1, zeile2, zeile3],'url': urllib.parse.unquote(url)})
		self.addcache(suchwort+'#',start,treffer,trefferliste)	
		return	
