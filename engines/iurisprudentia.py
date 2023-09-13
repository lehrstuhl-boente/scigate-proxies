import urllib
from adapter import Adapter
import requests
import json

class Iurisprudentia(Adapter):
  id='iurisprudentia'
  name = 'Iurisprudentia'
  headers = {
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Accept': '*/*'
  }
  host = 'https://transkribus.eu'
  suchpfad = '/r/search/search'
  arguments = ''

  def __init__(self):
    super().__init__(self.name)

  def request(self, suchstring, filters='', start=0,count=Adapter.LISTSIZE):
    body = {
      "term": suchstring,
      "collections": [
          70220,
          125620,
          193028,
          65112,
          72840,
          94274,
          72827,
          65559,
          65288,
          72893,
          70009,
          77749,
          72836,
          182280,
          64367,
          102017,
          129030,
          74609,
          104748,
          70219,
          72859,
          74610,
          58258,
          62597,
          66608,
          62075,
          62452,
          94844
      ],
      "fuzziness": 1,
      "limit": 100
    }
    response=requests.post(url=self.host+self.suchpfad, headers=self.headers, data=json.dumps(body))
    if response.status_code >= 300:
      return "http-response: " + str(response.status_code)
    rs=json.loads(response.text)
    treffer = rs['total']
    trefferliste = []
    for dokument in rs['results']:
      #url = f"http://rwi.app/iurisprudentia/de/___/documents/static/{dokument['id']}/pages/{dokument['761']}/?t={suchstring}"
      url = "http://rwi.app/iurisprudentia/"  # TODO: find out how link is built
      zeile1 = dokument['title']
      zeile2 = ''
      zeile3 = ''
      if len(dokument['snippets']) >= 1:
        for snippet in dokument['snippets'][0]:
          zeile2 += snippet['string']
      if len(dokument['snippets']) >= 2:
        for snippet in dokument['snippets'][1]:
          zeile3 += snippet['string']
      trefferliste.append({
        'engineId': self.id,
        'description':[zeile1, zeile2, zeile3],
        'url': url,
      })
    self.addcache(self.cachekey,start,treffer,trefferliste)