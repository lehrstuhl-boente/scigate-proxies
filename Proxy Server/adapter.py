class Adapter():
	name="unknown"
	adapters={}
	
	def __init__(self,name):
		self.adapters[name]=self
	
	def execute(self, command):
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
					if 'start' in command: start=command['start']
					count=10
					if 'count' in command: count=command['count']
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
		return "error", "not implemented", 0

	def treffer(self, suchstring,von=0,bis=10):
		return "error", "not implemented", {}	

