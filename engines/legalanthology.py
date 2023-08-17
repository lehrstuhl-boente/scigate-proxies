from adapter import Adapter
import requests
import json
import re

class Legalanthology(Adapter):
  id="legalanthology"
  name="The Anthology of Swiss Legal Culture"
  headers = {
    "accept": "text/html",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  }
  host="https://www.legalanthology.ch"
  suchpfad="/wp-admin/admin-ajax.php"
  arguments=""

  def __init__(self):
    super().__init__(self.name)

  def request(self, suchstring, filters='', start=0, count=Adapter.LISTSIZE):
    # count is ignored here
    # starts at page 0, always 10 hits per page (first 10 hits on page 0, second 10 hits on page 1, ...)
    page = (int)(start/10)
    form_data = {
      'action': (None, 'ajaxsearchpro_search'),
      'aspp': (None, suchstring), # search phrase
      'asid': (None, '1'),  # search ID
      'asp_inst_id': (None, '1_1'), # search instance ID --> one search can have multiple instances
      'options': (None, 'filters_initial=1&filters_changed=0&qtranslate_lang=0&current_page_id=13'), # serialized string of search form options
      'asp_call_num': (None, page) # which page of the results
    }
    response=requests.post(url=self.host+self.suchpfad, files=form_data, headers=self.headers)
    if response.status_code >= 300:
      return "http-response: "+str(response.status_code)
    result = re.search('___ASPSTART_DATA___(.*)___ASPEND_DATA___', response.text)
    data = json.loads(result.group(1)) # extract JSON from return text
    treffer=data['full_results_count']
    trefferliste=[]
    for dokument in data['results']:
      zeile1 = dokument['title']
      zeile2 = dokument['content']
      zeile3 = dokument['date']
      trefferliste.append({
        'engineId': self.id,
        "description": [zeile1, zeile2, zeile3],
        "url": dokument['link']
      })
    self.addcache(suchstring+'#'+filters,start,treffer,trefferliste)