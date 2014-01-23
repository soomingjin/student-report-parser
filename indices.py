#!/usr/bin/env python2

import re, yaml

def read_config():
	from os import listdir
	idir = 'indices'
	idxs = {}

	for f in listdir(idir):
		if f.endswith('.yaml'): idxs.update(yaml.load(open(idir+'/'+f)))

	return idxs

def search( needle, haystack ):
	try:
		return re.search( needle, haystack ).group(1)
	except AttributeError:
		return ''

def walk( d, c ):
	if 'indices' in d:
		r = d['regex']

		for i in d['indices']:
			for ix in i.keys():
				if 'sub' in r: ix = re.sub( r.get('sub'), r.get('repl'), ix )
				v = search( r.get('pre','')+ix+r.get('post',''), c ) 
				i.values()[0].update( { 'value': v } )
	else:
		if isinstance( d, dict ):
			for k,x in d.items():
				x = walk( x, c )
	return d

def parse_indices( pages ):

	indices = read_config()

	for k,idx in indices.items():
		p = [ i for i, s in enumerate(pages) if k in s ]
		compositepage = re.sub( r'.*%s.*' % (k,) , '', ''.join([ pages[x] for x in p ]) )
		compositepage = ' '.join( re.sub( r'\n+\d\n+', r'', compositepage ).split() )

		print walk( idx, compositepage )


if __name__ == "__main__": pass
