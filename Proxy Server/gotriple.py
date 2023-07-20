import urllib
from adapter import Adapter
import requests
import json

class GoTriple(Adapter):
  name = 'GoTriple'
  headers = {}
  host = 'https://api.gotriple.eu'
  suchpfad = '/documents'
  arguments = '?q={suchterm}&size={count}&page={page}&fq=in_language={language};&from=undefined&to=undefined'

  def __init__(self):
    super().__init__(self.name)

  def request(self, suchstring, filters='', start=0, count=Adapter.LISTSIZE):
    urlsuchstring = urllib.parse.quote_plus(suchstring)
    page = (int)(start/count)+1
    language = 'de'
    argumente = self.arguments.format(suchterm=urlsuchstring, count=count, page=page, language=language)
    response = requests.get(url=self.host+self.suchpfad+argumente, headers=self.headers)
    if response.status_code >= 300:
      return "http-response: "+str(response.status_code)
    data = json.loads(response.text)
    treffer = data['hydra:totalItems']
    trefferliste = []
    for dokument in data['hydra:member']:
      # first show german, then english version if available, fallback to first given version
      zeile1 = ''
      if dokument['headline'] != []:
        current_lang = ''
        zeile1 = dokument['headline'][0]['text']
        for headline_item in dokument['headline']:
          if headline_item['lang'] == 'de':
            zeile3 = headline_item['text']
            current_lang = 'de'
          if headline_item['lang'] == 'en' and current_lang != 'de':
            zeile3 = headline_item['text']

      authors = []
      if dokument['author'] != []:
        for author in dokument['author']:
          authors.append(author['fullname'])
      zeile2 = dokument['date_published'] + ' | ' + ' • '.join(authors)

      # same as in zeile1
      zeile3 = ''
      if dokument['abstract'] != []:
        current_lang = ''
        zeile3 = dokument['abstract'][0]['text']
        for abstract_item in dokument['abstract']:
          if abstract_item['lang'] == 'de':
            zeile3 = abstract_item['text']
            current_lang = 'de'
          if abstract_item['lang'] == 'en' and current_lang != 'de':
            zeile3 = abstract_item['text']
      if len(zeile3) > 250:           # trim abstract bc. it can get too long
        zeile3 = zeile3[:250] + '…'

      #url = 'https://www.gotriple.eu' + dokument['@id']
      url = dokument['main_entity_of_page'][0]
      trefferliste.append({
        'description': [zeile1, zeile2, zeile3],
        'url': url
      })
    self.addcache(suchstring+'#'+filters,start,treffer,trefferliste)
