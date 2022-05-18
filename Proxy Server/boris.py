from adapter import Adapter
import requests
import json
import lxml.html
import urllib
import re

class Boris(Adapter):
	name="Boris"
	headers={
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
		'Accept': '*/*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'Referer': 'https://boris.unibe.ch/cgi/search/archive/simple?screen=Search&order=&q=test&_action_search=Search&dataset=archive',
		'Origin': 'https://boris.unibe.ch',
		'Connection': 'keep-alive',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin'
	}
	host="https://boris.unibe.ch"
	suchpfad="/cgi/search/archive/simple"
	arguments="?screen=Search&order=&q={suchterm}&_action_search=Search&dataset=archive"
	arguments="?exp=0|1||archive|-|q::ALL:IN:{suchterm}|-|&_action_search=1&order=&screen=Search&search_offset={start}"
	dokumentpfad="/id/eprint/"
	leerplatz=re.compile(r'[\n\r\s]+')
	
	def __init__(self):
		super().__init__(self.name)
		
	def suche(self, suchstring):
		urlsuchstring=urllib.parse.quote_plus(suchstring)
		argumente=self.arguments.format(count=10, start=0, suchterm=urlsuchstring)
		response=requests.get(url=self.host+self.suchpfad+argumente, headers=self.headers)
		tree = lxml.html.fromstring(response.text)
		counts=tree.xpath("//div[@class='ep_search_controls']/div/span[@class='ep_search_number']/text()")
		treffer=int(counts[len(counts)-1])
		return "ok", "", treffer
		
	def treffer(self, suchstring, start, count):
		urlsuchstring=urllib.parse.quote_plus(suchstring)
		argumente=self.arguments.format(count=count, start=start, suchterm=urlsuchstring)
		response=requests.get(url=self.host+self.suchpfad+argumente, headers=self.headers)
		trefferliste=[]
		tree = lxml.html.fromstring(response.text)
		for dokument in tree.xpath("//tr[@class='ep_search_result']"):
			s=dokument.xpath("string(./td[span])").strip()
			zeile1=self.leerplatz.sub(" ",s)
			zeile2=""
			zeile3=""
			url=dokument.xpath("./td[span]/a[1]/@href")
			trefferliste.append({'description':[zeile1, zeile2, zeile3],'url': url})
		return "ok", "", trefferliste