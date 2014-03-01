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

def walk( dd, foo ):
	if not isinstance( dd, dict ): return ''		

	if 'indices' in dd:
		foo( dd )
	else:
		for k,x in dd.items(): x = walk( x, foo )
	return dd

def extract( iidx, pages ):
	def grab( d ):
		r = d['regex']
		for i in d['indices']:
			for ix,id in i.items():
				if 'sub' in r: ix = re.sub( r['sub'], r.get('repl',''), ix )
				v = search( r.get('pre','')+ix+r.get('post',''), pages ) 
				id.update( { 'value': v } )
	return walk( iidx, grab )

def flatten( iidx ):
	def show( d ):
		grp = d.get('group')
		pre = d.get('short-pre','')

		for i in d['indices']:
			for id in i.values():
				indices.append( ( grp, pre+id.get('short'), id.get('value') ) )
	indices = []
	walk( iidx, show )
	indices.sort()
	return indices


def parse_indices( pages ):

	indices = read_config()

	for k,idx in indices.items():

		p = re.sub( r'.*%s.*' % (k,), '', ''.join( [ x for x in pages if k in x ] ) )
		p = ' '.join( re.sub( r'\n+\s+\d\s+\n+', r' ', p ).split() )

		idx = extract( idx, p )

	return zip( *flatten( indices ) )[1:]

if __name__ == "__main__": pass
