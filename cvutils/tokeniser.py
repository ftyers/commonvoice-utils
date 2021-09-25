"""Tokenisers."""

"""
	FIXME:
		- Put the linguistic data in separate files in the data directories
"""

import re

class Tokeniser:

	def __init__(self, lang):
		self.tokenise = self._default

		if lang in ["as", "asm"]:
			self.tokenise = self._asm
		if lang in ["azz"]:
			self.tokenise = self._azz
		if lang in ["br", "bre"]:
			self.tokenise = self._bre
		if lang in ["ca", "cat"]:
			self.tokenise = self._cat
		if lang in ["cy", "cym"]:
			self.tokenise = self._cym
		if lang in ["dv", "div"]:
			self.tokenise = self._div
		if lang in ["en", "eng"]:
			self.tokenise = self._eng
		if lang in ["fa", "pes"]:
			self.tokenise = self._pes
		if lang in ["fr", "fra"]:
			self.tokenise = self._fra
		if lang in ["fy", "fry"] or lang.startswith("fy-"):
			self.tokenise = self._fry
		if lang in ["ga", "gle"] or lang.startswith("ga-"):
			self.tokenise = self._gle
	#	if lang in ["ja", "jpn"]:
	#		import nagisa
	#		self.tokenise = self._jpn(nagisa, sentence)
		if lang in ["kab"]:
			self.tokenise = self._kab
		if lang in ["ka", "kat"]:
			self.tokenise = self._kat
		if lang in ["lg", "lug"]:
			self.tokenise = self._lug
		if lang in ["hi", "hin"]:
			self.tokenise = self._hin
		if lang in ["gn", "grn", "gug"]:
			self.tokenise = self._grn
		if lang in ["it", "ita"]:
			self.tokenise = self._ita
		if lang in ["mt", "mlt"]:
			self.tokenise = self._mlt
		if lang in ["or", "ori"]:
			self.tokenise = self._ori
		if lang in ["pa", "pan"] or lang.startswith("pa-"):
			self.tokenise = self._pan
		if lang in ["pt", "por"]:
			self.tokenise = self._por
		if lang in ["rm", "roh"] or lang.startswith("rm-"):
			self.tokenise = self._roh
		if lang in ["ta", "tam"]:
			self.tokenise = self._tam
	#	if lang in ["th", "tha"]:
	#		import thai_segmenter
	#		self.tokenise = self.thai_segmenter.tokenize
		if lang in ["tr", "tur"]:
			self.tokenise = self._tur
		if lang in ["uk", "ukr"]:
			self.tokenise = self._ukr
	#	if lang in ["zh", "zho"] or lang.startswith("zh-"):
	#		import jieba
	
	#		self.tokenise = self.jieba.lcut
			
	def _quc(self, sentence):
		"""Tokeniser for quc."""
		o = sentence
		o = re.sub("'", "ʼ", o)
		o = re.sub("’", "ʼ", o)
	
		return [i for i in re.split("(\\w+)", o) if not i.strip() == ""]

	def _grn(self, sentence):
		"""Tokeniser for grn."""
		o = sentence
		o = re.sub("'", "ʼ", o)
		o = re.sub("’", "ʼ", o)
	
		return [i for i in re.split("(\\w+)", o) if not i.strip() == ""]
		
	def _azz(self, sentence):
		"""Tokeniser for azz.
	
			>>> tokenise('mayejyeualtik tepitsin saj. *Bueno** amo mapijpitsakueyak, *sino que** mamej...,
		mayejyeualtik uaukilit.', lang='azz')
			['mayejyeualtik', 'tepitsin', 'saj', '.', '*', 'Bueno', '**', 'amo', 'mapijpitsakueyak', ',', '*',
		'sino', 'que', '**', 'mamej', '...,', 'mayejyeualtik', 'uaukilit', '.']
		"""
		# !"'()*,./:;<>?[]¡´¿꞉$24aAábBcCdDeEéÉfFgGhHiIíjJkKlLmMnNñoOópPqQrRsStTuUúÚvVwWxXyYzZ
		o = sentence
		o = re.sub(r"([!'*,./:;<>?¡´¿]+)", r" \g<1> ", o)
		o = o.replace("[", " [ ")
		o = o.replace('"', ' " ')
		o = o.replace("]", " ] ")
		o = o.replace("(", " ( ")
		o = o.replace(")", " ) ")
		o = re.sub(r"  *", " ", o)
		o = o.strip()
		return [i.strip() for i in o.split(" ") if not i.strip() == ""]
	
	def _ita(self, sentence):
		"""Tokeniser for ita.
	
			>>> tokenise('L’Olivetti sopravvisse mentre l’Olimpia, il suo competitor più grande, chiuse.', lang='ita')
			['L’', 'Olivetti', 'sopravvisse', 'mentre', 'l’', 'Olimpia', ',', 'il', 'suo',
		'competitor', 'più', 'grande', ',', 'chiuse', '.']
		"""
		o = sentence
		o = re.sub(r"([!\"#$+,./:;<=>?~¡«°»–‘“”„…]+)", r" \g<1> ", o)
		o = o.replace("[", " [ ")
		o = o.replace("]", " ] ")
		o = o.replace("(", " ( ")
		o = o.replace(")", " ) ")
		o = o.replace("L'", " L' ")
		contractions = [
			"l",
			"dell",
			"all",
			"d",
			"un",
			"nell",
			"dall",
			"c",
			"quest",
			"sull",
			"anch",
			"quell",
			"po",
			"tutt",
			"s",
			"vent",
			"trent",
			"de",
			"sant",
		]
		for tok in contractions:
			o = o.replace(tok.title() + "'", tok.title() + "' ")
			o = o.replace(tok.title() + "’", tok.title() + "’ ")
			o = o.replace(" " + tok + "'", " " + tok + "' ")
			o = o.replace(" " + tok + "’", " " + tok + "’ ")
		o = re.sub(r"  *", " ", o)
		o = o.strip()
		return [i.strip() for i in o.split(" ") if not i.strip() == ""]
	
	
	def _tam(self, sentence):
		r"""Tokeniser for tam.
	
		>>> tokenise("கோலத்தினைக் கொய்வ துண்டோ? - \\"பெண்கள்", lang="tam")
		['கோலத்தினைக்', 'கொய்வ', 'துண்டோ', '?', '-', '"', 'பெண்கள்']
		"""
		o = sentence
		o = re.sub(r"([!\"',.:;?·–—‘’• ½¾-]+)", r" \g<1> ", o)
		o = re.sub(r"  *", " ", o)
		return [i.strip() for i in o.split(" ") if not i.strip() == ""]
	
	
	def _pan(self, sentence):
		"""Tokeniser for pan.
	
		>>> tokenise("ਮੇਰਾ ਸਭਾਵ ਦ੍ਰਸ਼ਟਾ ਦਾ ਹੈ; ਮੈਂ ਤਿੰਨਾਂ ਤੋਂ ਪਾਰ ਚੌਥੇ ਨੂੰ ਪਛਾਣ ਲਿਆ ਹੈ", lang="pan")
		['ਮੇਰਾ', 'ਸਭਾਵ', 'ਦ੍ਰਸ਼ਟਾ', 'ਦਾ', 'ਹੈ', ';', 'ਮੈਂ', 'ਤਿੰਨਾਂ', 'ਤੋਂ', 'ਪਾਰ', 'ਚੌਥੇ', 'ਨੂੰ', 'ਪਛਾਣ', 'ਲਿਆ', 'ਹੈ']
		"""
		o = sentence
		o = re.sub(r"([.;¦×॥–’¤]+)", r" \g<1> ", o)
		o = re.sub(r"  *", " ", o)
		return [i.strip() for i in o.split(" ") if not i.strip() == ""]
	
	
	def _por(self, sentence):
		"""Tokeniser for por.
	
		>>> tokenise("Tu comestes 'bem? se tu vieres sozinho disse dos infortúnios", lang="por")
		['Tu', 'comestes', "'bem", '?', 'se', 'tu', 'vieres', 'sozinho', 'disse', 'dos', 'infortúnios']
		"""
		o = sentence
		o = re.sub(r"([!\",./:;?’]+)", r" \g<1> ", o)
		o = o.replace(" d'", " d' ")
		o = re.sub(r"  *", " ", o)
	
		return [i.strip() for i in o.split(" ") if not i.strip() == ""]
	
	
	def _lug(self, sentence):
		"""Tokeniser for lug.
	
		>>> tokenise("Kika kya nnyimba ki ky'osinga okwagala?", lang="lug")
		['Kika', 'kya', 'nnyimba', 'ki', "ky'osinga", 'okwagala', '?']
		"""
		o = sentence
		o = re.sub(r"([!\",./:;?’-]+)", r" \g<1> ", o)
		o = re.sub(r"  *", " ", o)
	
		return [i.replace("ʼ", "'") for i in o.split(" ") if not i.strip() == ""]
	
	
	def _cym(self, sentence):
		"""Tokeniser for cym.
	
		>>> tokenise("Ond meddylia mae ’na ddoethuriaeth i'w sgwennu.", lang="cym")
		['Ond', 'meddylia', 'mae', "'na", 'ddoethuriaeth', "i'w", 'sgwennu', '.']
		"""
		o = sentence
		o = re.sub(r"([!,.:;?¬–—‘-]+)", r" \g<1> ", o)
		o = re.sub(r"['’]", "ʼ", o)
		o = re.sub(r"  *", " ", o)
	
		return [i.replace("ʼ", "'") for i in o.split(" ") if not i.strip() == ""]
	
	
	def _fry(self, sentence):
		"""Tokeniser for fry.
	
		>>> tokenise("Wêr't er ek nei harket, dy muzyk is allegearre like hurd.", lang="fry")
		["Wêr't", 'er', 'ek', 'nei', 'harket', ',', 'dy', 'muzyk', 'is', 'allegearre', 'like', 'hurd', '.']
		"""
		o = sentence
		o = re.sub(r"([!,\"\.:;?‘-]+)", r" \g<1> ", o)
		o = re.sub(r"  *", " ", o)
		return [i for i in o.split(" ") if not i.strip() == ""]
	
	
	def _cat(self, sentence):
		r"""Tokeniser for cat.
	
			>>> tokenise("L'eslògan \\"that\\'d be great\\" (\\"això seria genial\\") de Lumbergh
		també s'ha transformat en un popular mem d'internet.", lang="cat")
			["L'", 'eslògan', '"', "that'd", 'be', 'great', '"', '("', 'això', 'seria', 'genial', '")',
		'de', 'Lumbergh', 'també', "s'", 'ha', 'transformat', 'en', 'un', 'popular', 'mem', "d'", 'internet', '.']
		"""
		o = sentence
		o = re.sub(r"([!\"()*+,./:;?@|~¡«°·»¿–—―’“”…]+)", r" \g<1> ", o)
		o = re.sub(r"([DLSM]['’])", r"\g<1> ", o)
		o = re.sub(r"( [dlsm]['’])", r" \g<1> ", o)
		o = re.sub(r"  *", " ", o)
		return [i.replace("ʼ", "'") for i in o.split(" ") if not i.strip() == ""]
	
	
	def _fra(self, sentence):
		"""Tokeniser for fra."""
		o = sentence
		o = re.sub(r"([!*+,./\":;?@|~¡«°·»¿–—―’“”…']+)", r" \g<1> ", o)
		o = re.sub(r"([JDLSMN]) (['’])", r"\g<1>\g<2>", o)
		o = re.sub(r"( [jdlsmn]) (['’])", r"\g<1>\g<2>", o)
		o = re.sub(r"([Qq]u) (['’])", r"\g<1>\g<2>", o)
		o = re.sub(r"  *", " ", o)
		return [i.replace("ʼ", "'") for i in o.split(" ") if not i.strip() == ""]
	
	
	def _eng(self, sentence):
		"""Tokeniser for eng.
	
		>>> tokenise("O'Brien's protege and eventual successor in Hollywood was Ray Harryhausen.", lang="eng")
		["O'Brien", "'s", 'protege', 'and', 'eventual', 'successor', 'in', 'Hollywood', 'was', 'Ray', 'Harryhausen', '.']
		>>> tokenise("oh!", lang="eng")
		['oh', '!']
		"""
		o = sentence
		o = re.sub(r'(["&()+,./:;<>?–—‘’“”!-]+)', r" \g<1> ", o)
		o = o.replace("'ve ", " 've ")
		o = o.replace("'s ", " 's ")
		o = o.replace("I'm ", "I 'm ")
		o = re.sub(r"  *", " ", o)
		return [i.replace("ʼ", "'") for i in o.split(" ") if not i.strip() == ""]
	
	
	def _bre(self, sentence):
		"""Tokeniser for bre.
	
		>>> tokenise("Tennañ a rit da'm c'hoar.", lang="bre")
		['Tennañ', 'a', 'rit', 'da', "'m", "c'hoar", '.']
		"""
		o = sentence
		o = o.replace(r"P'", "Pʼ ")
		o = o.replace(r"p'", "pʼ ")
		o = o.replace(r"c'h", "cʼh")
		o = o.replace(r"C'h", "Cʼh")
		o = o.replace(r"C'H", "CʼH")
		o = re.sub(r"([!%()*+,\./:;=>?«»–‘’“”…€½]+)", r" \g<1> ", o)
		o = re.sub(r"'", " '", o)
		o = re.sub(r"  *", " ", o)
	
		return [i.replace("ʼ", "'") for i in o.split(" ") if not i.strip() == ""]
	
	
	def _ukr(self, sentence):
		"""Tokeniser for ukr.
	
		>>> tokenise("— А далій не вб'єш, — проказав коваль.", lang="ukr")
		['— ', 'А', 'далій', 'не', "вб'єш", ', — ', 'проказав', 'коваль', '.']
		"""
		o = re.sub("'", "ʼ", sentence)
	
		return [i.replace("ʼ", "'") for i in re.split("(\\w+)", o) if not i.strip() == ""]
	
	
	def _tur(self, sentence):
		"""Tokeniser for tur.
	
		>>> tokenise("İlk Balkan Schengen'i mi?", lang="tur")
		['İlk', 'Balkan', "Schengen'i", 'mi', '?']
		"""
		o = re.sub("'", "ʼ", sentence)
	
		return [i.replace("ʼ", "'") for i in re.split("(\\w+)", o) if not i.strip() == ""]
	
	
	def _hin(self, sentence):
		"""Tokeniser for hin.
	
		>>> tokenise("हिट एंड रन केस: भाग्यश्री के खिलाफ भी सलमान खान जैसी शिकायत!", lang="hin")
		['हिट', 'एंड', 'रन', 'केस', ':', 'भाग्यश्री', 'के', 'खिलाफ', 'भी', 'सलमान', 'खान', 'जैसी', 'शिकायत', '!']
		"""
		o = sentence
		o = re.sub(r"([!&,.:?|।‘-]+)", r" \g<1> ", o)
		o = re.sub(r'"', ' " ', o)
		o = re.sub(r"'", " ' ", o)
		o = re.sub(r"  *", " ", o)
	
		return [x for x in re.split(" ", o) if not x.strip() == ""]
	
	
	def _asm(self, sentence):
		"""Tokeniser for asm.
	
		>>> tokenise("“অ’ গৰখীয়া, অ’ গৰখীয়া গৰু নাৰাখ কিয়?”", lang="asm")
		['“', 'অ’', 'গৰখীয়া', ',', 'অ’', 'গৰখীয়া', 'গৰু', 'নাৰাখ', 'কিয়', '?', '”']
		"""
		o = sentence
		o = re.sub(r"([!',.:;°।৷৹‘“-]+)", r" \g<1> ", o)
		o = re.sub(r'"', ' " ', o)
		o = o.replace("?", " ? ")
		o = re.sub(r"  *", " ", o)
	
		return [x for x in re.split(" ", o) if not x.strip() == ""]
	
	
	def _jpn(self, nagisa, sentence):
		"""Tokeniser for jpn.
	
		>>> tokenise("自然消滅することは目に見えてるじゃん。", lang="jpn")
		['自然', '消滅', 'する', 'こと', 'は', '目', 'に', '見え', 'てる', 'じゃん', '。']
		"""
		return nagisa.tagging(sentence).words
	
	
	def _kab(self, sentence):
		"""Tokeniser for kab.
	
			>>> tokenise("Leqbayel ttemḥaddin lawan-nni m'ara mmlaqan deg leswaq n
		Waεraben, leǧwayeh n Sṭif.", lang="kab")
			['Leqbayel', 'ttemḥaddin', 'lawan-nni', "m'ara", 'mmlaqan', 'deg', 'leswaq',
		'n', 'Waεraben', ',', 'leǧwayeh', 'n', 'Sṭif', '.']
		"""
		o = sentence
		o = re.sub(r"([!&(),./:;?«»–‘’“”‟…↓̣$€]+)", r" \g<1> ", o)
		o = re.sub(r"  *", " ", o)
	
		return [x for x in re.split(" ", o) if not x.strip() == ""]
	
	
	def _kat(self, sentence):
		"""Tokeniser for kat.
	
		>>> tokenise("გიორგიმ შენზე თქვა, წერა-კითხვა არ იცისო, მართალია?", lang="kat")
		['გიორგიმ', 'შენზე', 'თქვა', ',', 'წერა-კითხვა', 'არ', 'იცისო', ',', 'მართალია', '?']
		"""
		o = sentence
		o = re.sub(r"([!,.:;?–—“„]+)", r" \g<1> ", o)
		o = re.sub(r"  *", " ", o)
	
		return [x for x in re.split(" ", o) if not x.strip() == ""]
	
	
	def _mlt(self, sentence):
		"""Tokeniser for mlt.
	
		>>> tokenise("Ħadd ma weġġa' f'dan l-inċident.", lang="mlt")
		['Ħadd', 'ma', "weġġa'", "f'", 'dan', 'l-', 'inċident', '.']
		"""
		o = sentence
		for tok in [
			"ad-",
			"al-",
			"an-",
			"as-",
			"bħall-",
			"bħar-",
			"bħas-",
			"bħat-",
			"biċ-",
			"bid-",
			"bil-",
			"bin-",
			"bir-",
			"bis-",
			"bit-",
			"bix-",
			"bl-",
			"ċ-",
			"d-",
			"dal-",
			"dar-",
			"das-",
			"emm-",
			"erbatax-",
			"feed-",
			"fiċ-",
			"fid-",
			"fil-",
			"fin-",
			"fir-",
			"fis-",
			"fit-",
			"fix-",
			"fl-",
			"għaċ-",
			"għad-",
			"għal-",
			"għall-",
			"għan-",
			"għar-",
			"għas-",
			"għat-",
			"għax-",
			"ġod-",
			"ġol-",
			"ħal-",
			"ħall-",
			"ħdax-",
			"iċ-",
			"id-",
			"il-",
			"ill-",
			"in-",
			"ir-",
			"is-",
			"it-",
			"ix-",
			"kemm-",
			"l-",
			"lid-",
			"lill-",
			"lin-",
			"lir-",
			"lis-",
			"lit-",
			"maċ-",
			"mad-",
			"mal-",
			"man-",
			"mar-",
			"mas-",
			"mat-",
			"max-",
			"maz-",
			"mid-",
			"mil-",
			"mill-",
			"min-",
			"mir-",
			"mis-",
			"mit-",
			"mix-",
			"n-",
			"r-",
			"s-",
			"sal-",
			"sas-",
			"sat-",
			"sbatax-",
			"sittax-",
			"t-",
			"taċ-",
			"tad-",
			"tal-",
			"tan-",
			"tar-",
			"tas-",
			"tat-",
			"tax-",
			"tmintax-",
			"tnax-",
			"x-",
			"z-",
		]:
			o = o.replace(" " + tok, " " + tok + " ")
		for tok in ["b'", "f'", "m'", "s'", "t'", "x'"]:
			o = o.replace(" " + tok, " " + tok + " ")
		o = re.sub(r"([!,.:;`’]+)", r" \g<1> ", o)
		o = o.replace('"', ' " ')
		o = o.replace("?", " ? ")
		o = re.sub(r"  *", " ", o)
	
		return [x for x in re.split(" ", o) if not x.strip() == ""]
	
	
	def _ori(self, sentence):
		"""Tokeniser for ori."""
		o = sentence
		o = re.sub(r"([!',.:;?|°।–—‘’“-]+)", r" \g<1> ", o)
		o = o.replace('"', ' " ')
		o = re.sub(r"  *", " ", o)
		return [x for x in re.split(" ", o) if not x.strip() == ""]
	
	
	def _roh(self, sentence):
		"""Tokeniser for roh.
	
		>>> tokenise("L'unic chi güda forsa, es ün chic sco effet da placebo.", lang="roh")
		["L'", 'unic', 'chi', 'güda', 'forsa', ',', 'es', 'ün', 'chic', 'sco', 'effet', 'da', 'placebo', '.']
		"""
		o = sentence
		o = re.sub(r"([!,.:;?«»–‘“„…‹›-]+)", r" \g<1> ", o)
		for tok in [
			"l'",
			"d'",
			"s'",
			"ch'",
			"süll'",
			"l’",
			"d’",
			"s’",
			"ch’",
			"süll’",
		]:
			o = o.replace(" " + tok, " " + tok + " ")
		o = re.sub("([LSD][’']|Ün[’'])", r" \g<1> ", o)
		o = re.sub(r"  *", " ", o)
		return [x.strip() for x in re.split(" ", o) if not x.strip() == ""]
	
	
	def _div(self, sentence):
		"""Tokeniser for div.
	
		>>> tokenise("ތީ ޝަބާބޭ! ތިހެންވީއިރު ޓްވިންސެއް ހުރޭތަ؟ ރީޙާން ޙައިރާންވި", lang="div")
		['ތީ', 'ޝަބާބޭ', '!', 'ތިހެންވީއިރު', 'ޓްވިންސެއް', 'ހުރޭތަ', '؟', 'ރީޙާން', 'ޙައިރާންވި']
		"""
		o = sentence
		o = re.sub(r"([!.:;،؟–‘’]+)", r" \g<1> ", o)
		o = o.replace("-", " - ")
		o = re.sub(r"  *", " ", o)
		return [x.strip() for x in re.split(" ", o) if not x.strip() == ""]
	
	
	def _gle(self, sentence):
		"""Tokeniser for gle.
	
		>>> tokenise("A sheansailéir, a leas-sheansailéir, a mhic léinn, a dhaoine uaisle", lang="gle")
		['A', 'sheansailéir', ',', 'a', 'leas-sheansailéir', ',', 'a', 'mhic', 'léinn', ',', 'a', 'dhaoine', 'uaisle']
		"""
		o = sentence
		o = re.sub(r"([!(),.:;?–‘’]+)", r" \g<1> ", o)
		o = o.replace('"', ' " ')
		for tok in ["an-", "n-", "t-"]:
			o = o.replace(" " + tok, " " + tok + " ")
		o = re.sub(r"([DB]['’])", r"\g<1> ", o)
		o = re.sub(r"( [db]['’])", r" \g<1> ", o)
		o = re.sub(r"  *", " ", o)
		return [x.strip() for x in re.split(" ", o) if not x.strip() == ""]
	
	
	def _pes(self, sentence):
		"""Tokeniser for pes.
	
		>>> tokenise("اوه خدا، چه بهم ریختگی!", lang="pes")
		['اوه', 'خدا', '،', 'چه', 'بهم', 'ریختگی', '!']
		"""
		o = sentence
		o = re.sub(r"([!#%&,./:;«»،؛؟٪٫٬–…]+)", r" \g<1> ", o)
		o = o.replace('"', ' " ')
		o = o.replace("(", " ( ")
		o = o.replace(")", " ) ")
		o = o.replace("]", " ] ")
		o = o.replace("[", " [ ")
		o = o.replace("-", " - ")
		o = re.sub(r"  *", " ", o)
		return [x.strip() for x in re.split(" ", o) if not x.strip() == ""]
	
	
	def _default(self, sentence):
		"""Break sentence into words."""
		return [x for x in re.split("(\\w+)", sentence) if x.strip()]

