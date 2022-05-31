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
		print("execute: "+json.dumps(command))
		status='error'
		if 'type' in command:
			if command['type']=='search':
				if 'term' in command:
					status, fehler, trefferzahl=self.suche(command['term'])
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
					status, fehler, trefferliste=self.treffer(command['term'], start, count)
					if status=='ok':
						return {'hitlist': trefferliste}
				else:
					fehler='no searchterm given'
			else:
				fehler='unknown command '+command['type']
		else:
			fehler='no command type given'
		return {'error': fehler}
			
	def suche(self, suchstring):
		if suchstring in self.cache:
			if (datetime.datetime.now()-self.cache[suchstring].zeit).total_seconds()<86000:
				return "ok", "", self.cache[suchstring].trefferzahl
			else:
				del self.cache[suchstring]
		
		fehler=self.request(suchstring)
		if fehler:
			return "error", fehler, 0
		else:
			return "ok", "", self.cache[suchstring].trefferzahl
	
	def treffer(self, suchstring,von=0,zahl=10):
		if suchstring in self.cache:
			if (datetime.datetime.now()-self.cache[suchstring].zeit).total_seconds()>86000:
				del self.cache[suchstring]				
				fehler=self.request(suchstring, von, max(self.LISTSIZE,zahl))
				if fehler:
					return "error", fehler, []
		else:
			fehler=self.request(suchstring, von, max(self.LISTSIZE,zahl))
			if fehler:
				return "error", fehler, []
		
		trefferzahl=self.cache[suchstring].trefferzahl
		if trefferzahl<=von and von>0:
			return "error", "Search has only "+str(self.cache[suchstring].trefferzahl)+ " Hits. Cannot serve a hitlist starting with hit "+str(von)+".", []
		else:
			treffercache=self.cache[suchstring].trefferliste
			i=von
			ergebnis=[]
			while i<min(von+zahl,trefferzahl) :
				if i not in treffercache:
					fehler=self.request(suchstring, i, max(self.LISTSIZE,zahl-(i-von)))
					if fehler:
						return "error", fehler, []
					treffercache=self.cache[suchstring].trefferliste# 
				if i in treffercache:
					ergebnis.append(treffercache[i])
				else:
					print("Treffer "+str(i)+" nicht erhalten.")
				i+=1
			print("Für Suchanfrage '"+suchstring+"' "+str(trefferzahl)+" Treffer gefunden und ab Position "+str(von)+" "+str(len(ergebnis))+" Ergebnisse zurückgegeben.")
			return "ok","",ergebnis
						
	def addcache(self, suchstring,start,treffer,trefferliste):
		print("Addcache ab "+str(start)+" mit "+str(len(trefferliste))+" Treffern in der Liste.")
		if suchstring in self.cache:
			if self.cache[suchstring].update(suchstring, treffer, trefferliste, start):
				del self.cache[suchstring]
		if not suchstring in self.cache:
			self.cache[suchstring]=Cacheeintrag(suchstring, treffer, trefferliste, start)
	
	def request(self, suche, von=0):
		return "not implemented"

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
			return false
		for i in trefferliste:
			self.trefferliste[start]=copy.deepcopy(i)
			start+=1
		return True