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
	if not isinstance( d, dict ): return ''		

	if 'indices' in d:
		r = d['regex']

		for i in d['indices']:
			for ix,id in i.items():
				if 'sub' in r: ix = re.sub( r.get('sub'), r.get('repl'), ix )
				v = search( r.get('pre','')+ix+r.get('post',''), c ) 
				id.update( { 'value': v } )
	else:
		for k,x in d.items(): x = walk( x, c )
	return d

def flatten( d ):
	iidx = []
	def w( d ):
		if not isinstance( d, dict ): return ''

		if 'indices' in d:
			grp = d.get('group')
			pre = d.get('short-pre','')

			for i in d['indices']:
				for id in i.values():
					iidx.append( ( grp, pre+id.get('short'), id.get('value') ) )
		else:
			for k,x in d.items(): x = w( x )
			return d
	w(d)
	iidx.sort()
	return iidx


def parse_indices( pages ):

	indices = read_config()

	for k,idx in indices.items():
		p = [ i for i, s in enumerate(pages) if k in s ]
		compositepage = re.sub( r'.*%s.*' % (k,) , '', ''.join([ pages[x] for x in p ]) )
		compositepage = ' '.join( re.sub( r'\n+\d\n+', r'', compositepage ).split() )

		idx = walk( idx, compositepage )

	return zip( *flatten( indices ) )[1:]

if __name__ == "__main__": pass
