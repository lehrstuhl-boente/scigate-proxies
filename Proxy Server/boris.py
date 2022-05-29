from adapter import Adapter
import requests
import json
import lxml.html
import urllib
import re
from lxml.etree import tostring

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

	def request(self, suchstring, start=0, count=Adapter.LISTSIZE):
		# count is ignored here
		print("Start Boris-Request für "+suchstring+" ab "+str(start))
		urlsuchstring=urllib.parse.quote_plus(suchstring)
		argumente=self.arguments.format(start=start, suchterm=urlsuchstring)
		response=requests.get(url=self.host+self.suchpfad+argumente, headers=self.headers)

		if response.status_code >= 300:
			return "http-response: "+str(response.status_code)

		trefferliste=[]
		tree = lxml.html.fromstring(response.text)
		counts=tree.xpath("//div[@class='ep_search_controls']/div/span[@class='ep_search_number']/text()")
		trefferzahl=int(counts[len(counts)-1])

		for dokument in tree.xpath("//tr[@class='ep_search_result']"):
			# print(tostring(dokument))
			autor=dokument.xpath("(./td/span|/td[span]/text())[not(preceding-sibling::a)]")
			autors=""
			for a in autor:
				autors+=tostring(a).decode("utf-8")
			titel1=dokument.xpath("string(./td[span]/a[1])")
			titel2=dokument.xpath("string(./td[span]/a[1]/following-sibling::text()[count(preceding-sibling::a)=1])")
			sonst1=dokument.xpath("string(./td[span]/a[2])")
			sonst2=dokument.xpath("string(./td[span]/a[2]/following-sibling::text())")
			
			zeile1=self.leerplatz.sub(" ",autors)
			zeile2=" <span @class='hl1'>"+self.leerplatz.sub(" ",titel1)+"</span> "+self.leerplatz.sub(" ",titel2)
			if sonst1:
				zeile3="DOI: "+self.leerplatz.sub(" ",sonst1)
				if sonst2:
					zeile3+=" <span @class='hl2'>"+self.leerplatz.sub(" ",sonst2)+"</span>"
			else:
				zeile3=""
			url=dokument.xpath("./td[span]/a[1]/@href")
			trefferliste.append({'description':[zeile1, zeile2, zeile3],'url': url})

		self.addcache(suchstring,start,trefferzahl,trefferliste)
		# print("Ende Boris-Request")		
		return
