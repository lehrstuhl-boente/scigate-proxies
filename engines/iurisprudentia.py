import urllib
from adapter import Adapter
import requests
import json

class Iurisprudentia(Adapter):
  id="iurisprudentia"
  name = 'Iurisprudentia'
  headers = {}
  host = 'https://transkribus.eu'
  suchpfad = '/r/search/search'
  arguments = ''

  def __init__(self, name):
    super().__init__(name)

  def request(self, suche, von=0):
    pass