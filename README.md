# Crossrecherche
Crossrecherche nach juristischen Inhalten in akademischen Datebanken

## Purpose and Requirements
This is a prototype to have a combined search in different academic databases with a focus on legal content.
The requirement can be found in "Leistungsbeschrieb.pdf" in this repository.
A proposition of layouts can be found here: https://www.figma.com/proto/9ZuPfkKwlPOt3vIWMW1FVr/Sci-Gate?node-id=2%3A2&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=5%3A716
The first layout implemented will be the tabs view (page 3). The layouts on page 2 (parallel view) and page 5 (mixed view) might be added at a later stage.

## Architecture
A serverless and web-application will access proxies for the different search engines. These proxies are availabe for Boris, Zora, Swisscovery and entscheidsuche.ch.

## Proxy-API
These procies have a JSON REST-API:

### General usage
- address: http://v2202109132150164038.luckysrv.de:8080/
- Input JSON 
   - type: search|hitlist
   - engine: entscheidsuche|swisscovery|boris|zora
- Output JSON
   - status: ok|error
   - error: Error message (only present if status=error

### type=search
(Only additional parameters described here)

- Input JSON
   - term: search term or search terms, no syntax translation is currently done for the search engines
- Output JSON
   - hits: number of hits for the search

### type=hitlist
(Only additional parameters described here)

- Input JSON
   - term: search term or search terms, no syntax translation is currently done for the search engines
   - start: position in the hitlist to start (default=0)
   - count: number of hits to fetch (default=10). Not all search engines support more than 10 hits
- Output JSON
   - hitlist: list of hits every hit has the following attributes
      - description: list of 3 string describing the hit. As markup can be included <span>-Tags with the classes hl1 and hl2 for bold and italic.
      - url: URL to the hit at the search engine. Can be opened without context and should be opened in a new tab
