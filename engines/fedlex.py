from adapter import Adapter
import requests
import json
import urllib
import datetime

class Fedlex(Adapter):
	id="fedlex"
	name="Fedlex"

	host="https://www.fedlex.admin.ch"
	suchpfad="/elasticsearch/proxy/_search?index=data"
	headers={
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
		'Accept': '*/*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'Referer': 'https://swisscovery.slsp.ch',
		'content-type': 'application/json',
		'Connection': 'keep-alive',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Vary': 'accept-encoding,origin,access-control-request-headers,access-control-request-method,accept-encoding'
	}
	
	def __init__(self):
		super().__init__(self.name)
		
	def request(self, suchwort, filters='',start=0,count=Adapter.LISTSIZE):
		body = {
			"size": count,
			"from": start,
			"aggs": {
				"results_language": {
					"filter": {
						"match_all": {}
					},
					"aggs": {
						"http://publications.europa.eu/resource/authority/language/DEU": {
							"filter": {
								"bool": {
									"should": [
										{
											"match": {
												"data.attributes.titleTreaty.rdf:langString.de": suchwort
											}
										},
										{
											"match": {
												"included.attributes.eventTitle.rdf:langString.de": suchwort
											}
										},
										{
											"match": {
												"data.attributes.title.rdf:langString.de": suchwort
											}
										},
										{
											"multi_match": {
												"query": suchwort,
												"fields": [
													"facets.content.de",
													"facets.title.de^10",
													"facets.titleAlternative.de",
													"facets.titleShort.de",
													"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/DEU^10"
												],
												"boost": 10,
												"type": "phrase_prefix"
											}
										},
										{
											"query_string": {
												"query": suchwort,
												"fields": [
													"facets.content.de",
													"facets.title.de^10",
													"facets.titleAlternative.de",
													"facets.titleShort.de",
													"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/DEU^10"
												],
												"boost": 100
											}
										}
									],
									"minimum_should_match": 1
								}
							}
						},
						"http://publications.europa.eu/resource/authority/language/FRA": {
							"filter": {
								"bool": {
									"should": [
										{
											"match": {
												"data.attributes.titleTreaty.rdf:langString.fr": suchwort
											}
										},
										{
											"match": {
												"included.attributes.eventTitle.rdf:langString.fr": suchwort
											}
										},
										{
											"match": {
												"data.attributes.title.rdf:langString.fr": suchwort
											}
										},
										{
											"multi_match": {
												"query": suchwort,
												"fields": [
													"facets.content.fr",
													"facets.title.fr^10",
													"facets.titleAlternative.fr",
													"facets.titleShort.fr",
													"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/FRA^10"
												],
												"boost": 10,
												"type": "phrase_prefix"
											}
										},
										{
											"query_string": {
												"query": suchwort,
												"fields": [
													"facets.content.fr",
													"facets.title.fr^10",
													"facets.titleAlternative.fr",
													"facets.titleShort.fr",
													"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/FRA^10"
												],
												"boost": 100
											}
										}
									],
									"minimum_should_match": 1
								}
							}
						},
						"http://publications.europa.eu/resource/authority/language/ITA": {
							"filter": {
								"bool": {
									"should": [
										{
											"match": {
												"data.attributes.titleTreaty.rdf:langString.it": suchwort
											}
										},
										{
											"match": {
												"included.attributes.eventTitle.rdf:langString.it": suchwort
											}
										},
										{
											"match": {
												"data.attributes.title.rdf:langString.it": suchwort
											}
										},
										{
											"multi_match": {
												"query": suchwort,
												"fields": [
													"facets.content.it",
													"facets.title.it^10",
													"facets.titleAlternative.it",
													"facets.titleShort.it",
													"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ITA^10"
												],
												"boost": 10,
												"type": "phrase_prefix"
											}
										},
										{
											"query_string": {
												"query": suchwort,
												"fields": [
													"facets.content.it",
													"facets.title.it^10",
													"facets.titleAlternative.it",
													"facets.titleShort.it",
													"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ITA^10"
												],
												"boost": 100
											}
										}
									],
									"minimum_should_match": 1
								}
							}
						},
						"http://publications.europa.eu/resource/authority/language/ROH": {
							"filter": {
								"bool": {
									"should": [
										{
											"match": {
												"data.attributes.titleTreaty.rdf:langString.rm": suchwort
											}
										},
										{
											"match": {
												"included.attributes.eventTitle.rdf:langString.rm": suchwort
											}
										},
										{
											"match": {
												"data.attributes.title.rdf:langString.rm": suchwort
											}
										},
										{
											"multi_match": {
												"query": suchwort,
												"fields": [
													"facets.content.rm",
													"facets.title.rm^10",
													"facets.titleAlternative.rm",
													"facets.titleShort.rm",
													"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ROH^10"
												],
												"boost": 10,
												"type": "phrase_prefix"
											}
										},
										{
											"query_string": {
												"query": suchwort,
												"fields": [
													"facets.content.rm",
													"facets.title.rm^10",
													"facets.titleAlternative.rm",
													"facets.titleShort.rm",
													"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ROH^10"
												],
												"boost": 100
											}
										}
									],
									"minimum_should_match": 1
								}
							}
						},
						"http://publications.europa.eu/resource/authority/language/ENG": {
							"filter": {
								"bool": {
									"should": [
										{
											"match": {
												"data.attributes.titleTreaty.rdf:langString.en": suchwort
											}
										},
										{
											"match": {
												"included.attributes.eventTitle.rdf:langString.en": suchwort
											}
										},
										{
											"match": {
												"data.attributes.title.rdf:langString.en": suchwort
											}
										},
										{
											"multi_match": {
												"query": suchwort,
												"fields": [
													"facets.content.en",
													"facets.title.en^10",
													"facets.titleAlternative.en",
													"facets.titleShort.en",
													"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ENG^10"
												],
												"boost": 10,
												"type": "phrase_prefix"
											}
										},
										{
											"query_string": {
												"query": suchwort,
												"fields": [
													"facets.content.en",
													"facets.title.en^10",
													"facets.titleAlternative.en",
													"facets.titleShort.en",
													"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ENG^10"
												],
												"boost": 100
											}
										}
									],
									"minimum_should_match": 1
								}
							}
						}
					}
				},
				"result_count": {
					"value_count": {
						"field": "data.uri.keyword"
					}
				}
			},
			"query": {
				"bool": {
					"filter": [
						{
							"terms": {
								"data.type.keyword": [
									"Act",
									"ConsolidationAbstract",
									"InitialDraft",
									"TreatyProcess"
								]
							}
						}
					],
					"must": [
						{
							"match_all": {}
						},
						{
							"bool": {
								"should": [
									{
										"multi_match": {
											"query": suchwort,
											"fields": [
												"facets.content.de",
												"facets.content.fr",
												"facets.content.it",
												"facets.content.rm",
												"facets.content.en",
												"facets.title.de^10",
												"facets.title.fr^10",
												"facets.title.it^10",
												"facets.title.rm^10",
												"facets.title.en^10",
												"facets.titleAlternative.de",
												"facets.titleAlternative.fr",
												"facets.titleAlternative.it",
												"facets.titleAlternative.rm",
												"facets.titleAlternative.en",
												"facets.titleShort.de",
												"facets.titleShort.fr",
												"facets.titleShort.it",
												"facets.titleShort.rm",
												"facets.titleShort.en",
												"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/DEU^10",
												"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/FRA^10",
												"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ITA^10",
												"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ROH^10",
												"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ENG^10"
											],
											"boost": 10,
											"type": "phrase_prefix"
										}
									},
									{
										"query_string": {
											"query": suchwort,
											"fields": [
												"facets.content.de",
												"facets.content.fr",
												"facets.content.it",
												"facets.content.rm",
												"facets.content.en",
												"facets.title.de^10",
												"facets.title.fr^10",
												"facets.title.it^10",
												"facets.title.rm^10",
												"facets.title.en^10",
												"facets.titleAlternative.de",
												"facets.titleAlternative.fr",
												"facets.titleAlternative.it",
												"facets.titleAlternative.rm",
												"facets.titleAlternative.en",
												"facets.titleShort.de",
												"facets.titleShort.fr",
												"facets.titleShort.it",
												"facets.titleShort.rm",
												"facets.titleShort.en",
												"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/DEU^10",
												"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/FRA^10",
												"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ITA^10",
												"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ROH^10",
												"facets.memorialLabel.http://publications.europa.eu/resource/authority/language/ENG^10"
											],
											"default_operator": "and",
											"boost": 1000
										}
									},
									{
										"multi_match": {
											"query": suchwort,
											"fields": [
												"data.attributes.titleTreaty.rdf:langString.de",
												"data.attributes.titleTreaty.rdf:langString.fr",
												"data.attributes.titleTreaty.rdf:langString.it",
												"data.attributes.titleTreaty.rdf:langString.rm",
												"data.attributes.titleTreaty.rdf:langString.en"
											],
											"type": "cross_fields"
										}
									},
									{
										"multi_match": {
											"query": suchwort,
											"fields": [
												"included.attributes.eventTitle.rdf:langString.de",
												"included.attributes.eventTitle.rdf:langString.fr",
												"included.attributes.eventTitle.rdf:langString.it",
												"included.attributes.eventTitle.rdf:langString.rm",
												"included.attributes.eventTitle.rdf:langString.en"
											],
											"type": "cross_fields"
										}
									},
									{
										"multi_match": {
											"query": suchwort,
											"fields": [
												"included.attributes.title.rdf:langString.de",
												"included.attributes.title.rdf:langString.fr",
												"included.attributes.title.rdf:langString.it",
												"included.attributes.title.rdf:langString.rm",
												"included.attributes.title.rdf:langString.en"
											],
											"type": "cross_fields"
										}
									}
								],
								"minimum_should_match": 1
							}
						},
						{
							"bool": {
								"should": [
									{
										"bool": {
											"minimum_should_match": 1,
											"should": [
												{
													"bool": {
														"must": [
															{
																"exists": {
																	"boost": 100000,
																	"field": "data.attributes.publicationDate.xsd:date"
																}
															},
															{
																"range": {
																	"data.attributes.publicationDate.xsd:date": {
																		"lte": "2023-04-30"
																	}
																}
															}
														],
														"must_not": [
															{
																"exists": {
																	"field": "data.attributes.dateEntryInForce.xsd:date"
																}
															},
															{
																"exists": {
																	"field": "data.attributes.dateNoLongerInForce.xsd:date"
																}
															},
															{
																"exists": {
																	"field": "data.attributes.dateEndApplicability.xsd:date"
																}
															}
														]
													}
												},
												{
													"bool": {
														"must": [
															{
																"exists": {
																	"field": "data.attributes.publicationDate.xsd:date",
																	"boost": 100000
																}
															},
															{
																"exists": {
																	"field": "data.attributes.dateEntryInForce.xsd:date",
																	"boost": 100000
																}
															},
															{
																"range": {
																	"data.attributes.publicationDate.xsd:date": {
																		"lte": "2023-04-30"
																	}
																}
															},
															{
																"range": {
																	"data.attributes.dateEntryInForce.xsd:date": {
																		"lte": "2023-04-30"
																	}
																}
															}
														],
														"must_not": [
															{
																"exists": {
																	"field": "data.attributes.dateNoLongerInForce.xsd:date"
																}
															},
															{
																"exists": {
																	"field": "data.attributes.dateEndApplicability.xsd:date"
																}
															}
														]
													}
												},
												{
													"bool": {
														"must": [
															{
																"exists": {
																	"field": "data.attributes.dateEntryInForce.xsd:date",
																	"boost": 100000
																}
															},
															{
																"range": {
																	"data.attributes.dateEntryInForce.xsd:date": {
																		"lte": "2023-04-30"
																	}
																}
															}
														],
														"must_not": [
															{
																"exists": {
																	"field": "data.attributes.publicationDate.xsd:date"
																}
															},
															{
																"exists": {
																	"field": "data.attributes.dateNoLongerInForce.xsd:date"
																}
															},
															{
																"exists": {
																	"field": "data.attributes.dateEndApplicability.xsd:date"
																}
															}
														]
													}
												}
											]
										}
									}
								],
								"filter": {
									"bool": {
										"minimum_should_match": 1,
										"should": [
											{
												"bool": {
													"should": [
														{
															"match": {
																"included.attributes.memorialName.xsd:string.keyword": "FF"
															}
														},
														{
															"match": {
																"included.attributes.memorialName.xsd:string.keyword": "BBl"
															}
														},
														{
															"match": {
																"included.attributes.memorialName.xsd:string.keyword": "FF"
															}
														},
														{
															"match": {
																"included.attributes.memorialName.xsd:string.keyword": "FGA"
															}
														},
														{
															"match": {
																"included.attributes.memorialName.xsd:string.keyword": "FUF"
															}
														}
													],
													"minimum_should_match": 1
												}
											},
											{
												"bool": {
													"filter": {
														"terms": {
															"data.type.keyword": [
																"Act"
															]
														}
													}
												}
											},
											{
												"bool": {
													"filter": {
														"terms": {
															"data.type.keyword": [
																"ConsolidationAbstract"
															]
														}
													}
												}
											},
											{
												"bool": {
													"filter": {
														"terms": {
															"data.type.keyword": [
																"InitialDraft"
															]
														}
													},
													"must": {
														"exists": {
															"field": "data.references.draftHasTask.keyword"
														}
													}
												}
											},
											{
												"bool": {
													"filter": {
														"terms": {
															"data.type.keyword": [
																"TreatyProcess"
															]
														}
													}
												}
											}
										]
									}
								}
							}
						}
					],
					"should": [
						{
							"terms": {
								"data.type.keyword": [
									"Act",
									"Consolidation",
									"ConsolidationAbstract",
									"ConsultationPhase",
									"ConsultationPreparation",
									"InitialDraft",
									"PositionStatementPublication",
									"ResultOfAConsultationPublication",
									"TreatyProcess"
								],
								"boost": 1.1
							}
						}
					]
				}
			}
		}
		if filters:
			for filter in filters:
				if filter['id'] == 'discipline':
					if 'law' not in filter['options']:
						self.addcache(self.cachekey,start,0,[])
						return
				elif filter['id'] == 'language':
					pass
				elif filter['id'] == 'availability':
					if 'freeOnlineAvailable' not in filter['options']:
						self.addcache(self.cachekey,start,0,[])
						return
				elif filter['id'] == 'date':
					filter_from = filter['from']
					filter_to = filter['to']
					if filter_from == '':
						filter_from = '2000'
					if filter_to == '':
						filter_to = str(datetime.now().year)
					body['query']['bool']['must'].append({
						"bool": {
							"should": [
								{
									"bool": {
										"must": {
											"range": {
												"data.attributes.publicationDate.xsd:date": { "lte": f"{filter_to}-12-31", "gte": f"{filter_from}-01-01" }
											}
										}
									}
								},
								{
									"bool": {
										"must": {
											"range": {
												"data.attributes.dateApplicability.xsd:date": { "lte": f"{filter_to}-12-31", "gte": f"{filter_from}-01-01" }
											}
										}
									}
								},
								{
									"bool": {
										"must": {
											"range": {
												"data.attributes.treatySignatureDate.xsd:date": { "lte": f"{filter_to}-12-31", "gte": f"{filter_from}-01-01" }
											}
										}
									}
								},
								{
									"bool": {
										"must": {
											"range": { "data.attributes.eventStartDate.xsd:date": { "lte": f"{filter_to}-12-31", "gte": f"{filter_from}-01-01" } }
										}
									}
								},
								{
									"bool": {
										"must": {
											"range": {
												"data.attributes.foreseenEventStartDate.xsd:date": { "lte": f"{filter_to}-12-31", "gte": f"{filter_from}-01-01" }
											}
										}
									}
								}
							],
							"minimum_should_match": 1
						}
					})
		da_uu=json.dumps(body)
		da_ascii=da_uu.encode('utf-8')

		response=requests.post(url=self.host+self.suchpfad, data=da_ascii, headers=self.headers)
		if response.status_code >= 300:
			return "http-response: "+str(response.status_code)
		#r=response.content
		#ru=r.decode("ascii")
		#rs=json.loads(ru.encode("utf-8"))
		rs=json.loads(response.text)
		if not 'hits' in rs:
			return "no valid response"
		treffer=rs['aggregations']['result_count']['value']
		trefferliste=[]
		for dokument in rs['hits']['hits']:
			z=[]
			i=0
			if 'included' in dokument['_source']:
				j=1
				while j<4:
					if 'attributes' in dokument['_source']['included'][j]:
						if 'title' in dokument['_source']['included'][j]['attributes']:
							z.append(dokument['_source']['included'][j]['attributes']['title']['xsd:string'])
							i+=1
					j+=1
			if len(z) == 0:
				if 'data' in dokument['_source'] and 'attributes' in dokument['_source']['data']:
					if 'titleTreaty' in dokument['_source']['data']['attributes']:
						tmp = dokument['_source']['data']['attributes']
						if 'de' in tmp:
							z.append(dokument['_source']['data']['attributes']['titleTreaty']['rdf:langString']['de'][0])
							i += 1
						if 'fr' in tmp:
							z.append(dokument['_source']['data']['attributes']['titleTreaty']['rdf:langString']['fr'][0])
							i += 1
						if 'it' in tmp:
							z.append(dokument['_source']['data']['attributes']['titleTreaty']['rdf:langString']['it'][0])
							i += 1
			if len(z) == 0: continue	# documents that don't have a title and that aren't treaties are skipped

			zeile1=z[0]
			zeile2 = ''
			zeile3 = ''
			if i >= 2:
				zeile2 = z[1]
			if i >= 3:
				zeile3 = z[2]
			
			url=dokument['_id']
			trefferliste.append({
				'engineId': self.id,
				'description':[zeile1, zeile2, zeile3],
				'url': urllib.parse.unquote(url)
			})
		self.addcache(self.cachekey,start,treffer,trefferliste)