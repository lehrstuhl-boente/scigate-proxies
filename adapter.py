import copy
import datetime
import json


class Adapter():
	LISTSIZE=20
	#Boris kann nichts anderes, da her wird das generell gesetzt.
	name="unknown"
	adapters={}
	
	def __init__(self,name):
		self.adapters[name]=self
		self.cache={}
	
	def execute(self, command):
		status='error'
		if not 'filters' in command:
			command['filters']=''
		if 'type' in command:
			if command['type']=='search':
				if 'term' in command:
					status, fehler, trefferzahl=self.suche(command['term'], self.format_filters(command['filters']))
					if status=='ok':
						return {'status': 'ok', 'hits': trefferzahl}
				else:
					fehler='no searchterm given'
			elif command['type']=='hitlist':
				if 'term' in command:
					start=0
					if 'start' in command:
						start=int(command['start'])
					count=10
					if 'count' in command:
						count=int(command['count'])
					status, fehler, trefferliste = self.treffer(command['term'], self.format_filters(command['filters']), start, count)
					if status=='ok':
						return {'status': 'ok', 'hitlist': trefferliste, 'start': start, 'searchterm': command['term'], 'filters': command['filters']}
				else:
					fehler='no searchterm given'
			else:
				fehler='unknown command '+command['type']
		else:
			fehler='no command type given'
		return {'error': fehler}
			
	def format_filters(self, filters):
		formatted_filters = []
		for filter in filters:
			if filter['type'] == 'checkbox':
				options = []
				for option in filter['options']:
					if option['checked']:
						options.append(option['name'])
				if len(options) > 0:	# only consider filter when at least one checkbox is checked
					formatted_filters.append({
						'id': filter['id'],
						'options': options
					})
			elif filter['type'] == 'date':
				if filter['from'] == '' and filter['to'] == '': continue	# don't add date filter if values are empty
				# TODO: don't add date filter if 
				formatted_filters.append(filter)
			elif filter['type'] == 'switch':
				pass	# TODO: implmement when first switch is in frontend
		return formatted_filters

	def suche(self, suchstring, filters):
		cachekey=suchstring+'#'
		if cachekey in self.cache:
			if (datetime.datetime.now()-self.cache[cachekey].zeit).total_seconds()<86000:
				return "ok", "", self.cache[cachekey].trefferzahl
			else:
				del self.cache[cachekey]

		# apply engine-wide filters here

		fehler=self.request(suchstring, filters)
		if fehler:
			return "error", fehler, 0
		else:
			return "ok", "", self.cache[cachekey].trefferzahl
	
	def treffer(self, suchstring, filters, von=0, zahl=10):
		cachekey=suchstring+'#'
		if cachekey in self.cache:
			if (datetime.datetime.now()-self.cache[cachekey].zeit).total_seconds()>86000:
				del self.cache[cachekey]				
				fehler=self.request(suchstring, filters, von, min(self.LISTSIZE,zahl))
				if fehler:
					return "error", fehler, []
		else:
			fehler=self.request(suchstring, filters, von, min(self.LISTSIZE,zahl))
			if fehler:
				return "error", fehler, []
		
		trefferzahl=self.cache[cachekey].trefferzahl
		if trefferzahl<=von and von>0:
			return "error", "Search has only "+str(self.cache[cachekey].trefferzahl)+ " Hits. Cannot serve a hitlist starting with hit "+str(von)+".", []
		else:
			treffercache=self.cache[cachekey].trefferliste
			i=von
			ergebnis=[]
			while i<min(von+zahl,trefferzahl):
				if i not in treffercache:
					fehler=self.request(suchstring, filters, i, max(self.LISTSIZE,zahl-(i-von)))
					if fehler:
						return "error", fehler, []
					treffercache=self.cache[cachekey].trefferliste 
				if i in treffercache:
					ergebnis.append(treffercache[i])
				else:
					#print("Treffer "+str(i)+" nicht erhalten.")
					pass
				i+=1
			#print("Für Suchanfrage '"+cachekey+"' "+str(trefferzahl)+" Treffer gefunden und ab Position "+str(von)+" "+str(len(ergebnis))+" Ergebnisse zurückgegeben.")
			return "ok","",ergebnis
						
	def addcache(self, cachekey, start,treffer,trefferliste):
		#print("Addcache ab "+str(start)+" mit "+str(len(trefferliste))+" Treffern in der Liste.")
		if cachekey in self.cache:
			if self.cache[cachekey].update(cachekey, treffer, trefferliste, start):
				del self.cache[cachekey]
		if not cachekey in self.cache:
			self.cache[cachekey]=Cacheeintrag(cachekey, treffer, trefferliste, start)
	
	def request(self, suche, von=0):
		raise NotImplementedError

class Cacheeintrag():

	def __init__(self, suche, trefferzahl, trefferliste, start=0):
		self.suche=suche
		self.trefferzahl=trefferzahl
		self.trefferliste={}
		for i in trefferliste:
			self.trefferliste[start]=copy.deepcopy(i)
			start+=1
		self.zeit=datetime.datetime.now()
		
	def update(self, suche, trefferzahl, trefferliste, start=0):
		# print("Start update mit start="+str(start)+" und "+str(len(trefferliste))+" Treffern in der Liste.")
		if suche!=self.suche:
			return False
		if trefferzahl!=self.trefferzahl:
			return False
		aktzeit=datetime.datetime.now()
		diff=(aktzeit-self.zeit).total_seconds()
		if diff>86000:
			return False
		for i in trefferliste:
			self.trefferliste[start]=copy.deepcopy(i)
			start+=1
		return True