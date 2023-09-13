import urllib
from adapter import Adapter
import requests
import json

class GoTriple(Adapter):
  id="gotriple"
  name = 'GoTriple'
  headers = {}
  host = 'https://api.gotriple.eu'
  suchpfad = '/documents'
  arguments = '?q={suchterm}&size={count}&page={page}&fq=topic={topic};conditions_of_access={access};in_language={language};year={filter_from}%2C{filter_to};&from=undefined&to=undefined'

  def __init__(self):
    super().__init__(self.name)

  def request(self, suchstring, filters='', start=0, count=Adapter.LISTSIZE):
    language = ''
    topic = ''
    access = ''
    filter_from = ''
    filter_to = ''
    if filters:
      for filter in filters:
        if filter['id'] == 'discipline':
          discipline_mappings = { 'law': 'droit' } # key: name in scigate, value: name in gotriple
          disciplines = []
          for option in filter['options']:
            if option == 'unknown': continue
            disciplines.append(discipline_mappings[option])
          topic = ','.join(disciplines)
        elif filter['id'] == 'language':
          if 'unknown' in filter['options']: filter['options'].remove('unknown')
          language = ','.join(filter['options'])
        elif filter['id'] == 'availability':
          availability_mappings = {
            'unknown': 'undefined,other',
            'freeOnlineAvailable': 'acr_open-access,acr_free-access,acr_public-domain',
            'restrictedOnlineAvailable': 'acr_all-rights-reserved,acr_restricted-access-or-use,acr_embargoed-access',
            'notOnlineAvailable': 'acr_closed-access'
          }
          availabilities = []
          for option in filter['options']:
            availabilities.append(availability_mappings[option])
          access = ','.join(availabilities)
        elif filter['id'] == 'date':
          filter_from = filter['from']
          filter_to = filter['to']
    urlsuchstring = urllib.parse.quote_plus(suchstring)
    page = (int)(start/count)+1
    argumente = self.arguments.format(suchterm=urlsuchstring, count=count, page=page, topic=topic, access=access, language=language, filter_from=filter_from, filter_to=filter_to)
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
        'engineId': self.id,
        'description': [zeile1, zeile2, zeile3],
        'url': url
      })
    self.addcache(self.cachekey,start,treffer,trefferliste)
