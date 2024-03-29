import urllib
from adapter import Adapter
import requests
import json
import re
import datetime


class Digitalisierungszentrum(Adapter):
    id = "digitalisierungszentrum"
    name = "Münchner DigitalisierungsZentrum"
    headers = {}
    host = "https://www.digitale-sammlungen.de"
    suchpfad = "/api/search"
    arguments = "?query={suchterm}&handler=simple-all&ocrContext=1&sortField={sort_field}&sortOrder={sort_order}&startPage={page}&pageSize={count}"

    def __init__(self):
        super().__init__(self.name)

    def request(self, suchstring, filters="", start=0, count=Adapter.LISTSIZE):
        if filters:
            for filter in filters:
                if filter["id"] == "discipline":
                    if "unknown" not in filter["options"]:
                        self.addcache(self.cachekey, start, 0, [])
                        return
                elif filter["id"] == "language":
                    for language in filter["options"]:
                        if language == "unknown":
                            language = "und"
                        self.arguments += f'&filter=language_bib:"{language}"'
                elif filter["id"] == "availability":
                    if "freeOnlineAvailable" not in filter["options"]:
                        self.addcache(self.cachekey, start, 0, [])
                        return
                elif filter["id"] == "year":
                    filter_from = str(filter["from"]).zfill(4)
                    filter_to = str(filter["to"]).zfill(4)
                    if filter["from"] == "":
                        filter_from = "0100"
                    if filter["to"] == "":
                        filter_to = datetime.date.today().year
                    self.arguments += (
                        f"&filter=date_facet:[{filter_from}-01-01+TO+{filter_to}-12-31]"
                    )
        urlsuchstring = urllib.parse.quote_plus(suchstring)
        sort_field = "relevancy"
        sort_order = "asc"
        page = (int)(start / count)
        argumente = self.arguments.format(
            suchterm=urlsuchstring,
            sort_field=sort_field,
            sort_order=sort_order,
            page=page,
            count=count,
        )
        response = requests.get(
            url=self.host + self.suchpfad + argumente, headers=self.headers
        )
        if response.status_code >= 300:
            return "http-response: " + str(response.status_code)
        data = json.loads(response.text)
        # print('xxx: ', json.dumps(data, indent=2))
        treffer = data["numTotal"]
        trefferliste = []
        if "docs" in data:
            for dokument in data["docs"]:
                zeile1 = dokument["title"]

                zeile2 = (
                    " • ".join(dokument["authors"]) if "authors" in dokument else ""
                )

                publication_places = (
                    ", ".join(dokument["publicationPlaces"])
                    if "publicationPlaces" in dokument
                    else ""
                )
                publishers = (
                    ", ".join(dokument["publishers"])
                    if "publishers" in dokument
                    else ""
                )
                publication_date = (
                    dokument["publicationDate"] if "publicationDate" in dokument else ""
                )
                zeile3 = f"{publication_places}: {publishers}, {publication_date}"

                url = "https://mdz-nbn-resolving.de/details:" + dokument["id"]
                trefferliste.append(
                    {
                        "engineId": self.id,
                        "description": [zeile1, zeile2, zeile3],
                        "url": url,
                    }
                )
        self.addcache(self.cachekey, start, treffer, trefferliste)
