import sys, re

class Gutenberg:

	gutenberg_languages = {
	'English':'en',
	'French':'fr',
	'Finnish':'fi',
	'German':'de',
	'Italian':'it',
	'Dutch':'nl',
	'Spanish':'es',
	'Portuguese':'pt',
	'Chinese':'zh',
	'Hungarian':'hu',
	'Greek':'el',
	'Swedish':'sv',
	'Esperanto':'eo',
	'Danish':'da',
	'Tagalog':'tl',
	'Polish':'pl',
	'Catalan':'ca',
	'Norwegian':'no',
	'Japanese':'ja',
	'Welsh':'cy',
	'Czech':'cs',
	'Afrikaans':'af',
	'Russian':'ru',
	'Icelandic':'is',
	'Friulian':'fur',
	'Telugu':'te',
	'Bulgarian':'bg',
	'Hebrew':'he',
	'Serbian':'sr',
	'Romanian':'ro',
	'Frisian':'fy',
	'Cebuano':'ceb',
	'Slovenian':'sl',
	'Irish':'ga-IE',
	'Yiddish':'yi',
	'Slovak':'sk',
	'Scots Gaelic':'gd',
	'Quiche':'quc',
	'Ojibwa':'oj',
	'Neapolitan':'nap',
	'Nahuatl':'nah',
	'Lithuanian':'lt',
	'Inuktitut':'iu',
	'Interlingua':'ia',
	'Iloko':'ilo',
	'Ilocano':'ilo',
	'Gascon':'oc',
	'Galician':'gl',
	'Farsi':'fa',
	'Estonian':'et',
	'Dutch/Flemish':'nl',
	'Dutch and Flemish':'nl',
	'Breton':'br',
	'Arapaho':'arp',
	'Arabic':'ar',
	'Aleut':'ale'
	}

	def __init__(self, index_path):

		self.catalogue = self.parse_index(index_path)
		
	def get_key(self, line):
		return line.split(':')[0].split('[')[1].strip().lower()

	def get_val(self, line):
		return line.split(':')[1].split(']')[0].strip()

	def parse_index(self, index_path):
	
		body = False
		first = True
		
		catalogue = {}
		entries = {}
		entry = {'id': 0, 'language': 'English'}
		for line in open(index_path):
			if line.count('TITLE and AUTHOR') > 0:
				body = True
		
			if line.count('===============================================================================') > 0:
				body = False
		
			if line.count('<==End of GUTINDEX.ALL==>') > 0:
				body = False
			
			if body and line.strip() == '':
				first = True
				idx = entry['id']
				entries[idx] = entry
				locale = '_'
				lang = entry['language']
				if lang in self.gutenberg_languages:
					locale = self.gutenberg_languages[lang]
				if locale not in catalogue:
					catalogue[locale] = []
				catalogue[locale].append(idx)
				entry = {'id': 0, 'language': 'English'}
				continue
		
			if body:
				line = line.strip()
				if first:
					idx = re.findall(r'[0-9]+[A-Z]*$', line)
					if idx:
						entry['id'] = idx[0]
					entry['title'] = re.sub(r'[0-9]+[A-Z]*$', '', line).strip()
					first = False
				else:
					if line[0] == '[' and ':' in line:
						k = self.get_key(line)
						v = self.get_val(line)
						entry[k] = v
	
		return catalogue

		
	def get_catalogue(self, locale):
		if locale in self.catalogue:
			return self.catalogue[locale]
		else:
			return []
