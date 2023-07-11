from adapter import Adapter
import urllib
import requests
import json

class Legalanthology(Adapter):
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
    print(suchstring)
    multipart_form_data = {
      'action': (None, 'ajaxsearchpro_search'),
      'aspp': (None, suchstring),
      'asid': (None, '1'),
      'asp_inst_id': (None, '1_1'),
      'options': (None, 'filters_initial=1&filters_changed=0&qtranslate_lang=0&current_page_id=13')
    }
    response=requests.post(url=self.host+self.suchpfad, files=multipart_form_data, headers=self.headers)
    if response.status_code >= 300:
      return "http-response: "+str(response.status_code)
    # extract JSON from return text
    