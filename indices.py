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

def extract( haystack, needles, pre, post ):
	if isinstance( needles, dict ):
		return { k: [ search( pre+t+post, haystack ) for t in x ] for k,x in needles.iteritems() } 
	else:
		return [ search( pre+t+post, haystack ) for t in needles ]

def parse_indices( pages ):

	indices = read_config()
	headers = indices.keys()

	page = [ [ i for i, s in enumerate(pages) if k in s ] for k in headers  ]

	for p in page:
		compositepage = re.sub( r'.*.*' , '', ''.join([ pages[x] for x in p ]) )

	return False

	if page[1]:
		pf_page = ''.join([ pages[x] for x in page[1] ])
		c_profile = extract( pf_page, composite_indices, '', r' (1?\d.\d)' )

	if page[3]:
		verbose_report = ' '.join( re.sub( r'\s\s\d\s\s', r'', compositepage ).split() )

		ci = { k: [ re.sub(' ',' ?',t) for t in x ] for k,x in criterion_indices.iteritems() }
		criterion_scores = extract( verbose_report, ci, '', r'.*?\((1?\d)\).' )

	return ( b_profile, c_profile, criterion_scores )

if __name__ == "__main__": pass
