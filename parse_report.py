#!/usr/bin/env python2

from __future__ import print_function
from datetime import datetime

import sys, re
import pdftext
import indices as id

reports = ( 'Singapore Student Narrative Report', 'Basic Interpretive Report' )
data_keywords = ( 'Score Summary', 'Singapore Student Assessment Information', 'Global Factors', 'Criterion Scores' )

def main(argv):
	import getopt

	def usage():
		print ( 'usage: %s file ...' % argv[0] )
		return 100
	try:
		( opts, args ) = getopt.getopt( argv[1:], 'd' )
	except getopt.GetoptError:
		return usage()

	if not args: return usage()

# create and write header to CSV

#	csv = open( '16PFs.csv', 'w' )
#	print( 'UID,Name,IM,IN,AC,A,B,C,E,F,G,H,I,L,M,N,O,Q1,Q2,Q3,Q4,G1,G2,G3,G4,G5', file=csv )

	for filename in args:
		file = pdftext.get( filename )

		if not file:
			print( "error! no text could be read from %s" % ( filename, ) )
			return False
			 
		print( parse_report( file ) )
#		print( , file=csv )

	return

def parse_report(pages):

	report_type, pages = [ ( rt, pages.split(rt)[1:] ) for rt in reports if rt in pages ][0]
		
	cover = pages[0]
	page = [ [ i for i, s in enumerate(pages) if k in s ] for k in data_keywords ]

	#
	#	Getting the ID, Name and Date of the Report
	#

	ID_IS_IC = False

	for s in re.findall( r'U?ID:\s*([^\s]*)', cover):
		if 'Date' in s: s = re.split( 'Date', s )[0]
		if re.findall( r'[stgfSTGF]\d{7}[A-Z]', s ):
			ID_IS_IC = True
			UID = s
		if not ID_IS_IC: UID = s

	try:
		name = re.search( 'Name: (.*)', cover).group(1)
	except AttributeError:
		print( "no name in %s" % ( filename, ) )

	try:
		textdate = re.search( 'Date: ([^\s]* [^\s]* \d*)', cover).group(1)
		try:
			report_date = datetime.strptime( textdate, '%B %d, %Y' ).strftime( '%Y-%m-%d' )
		except ValueError:
			print( "%s date format unknown" % ( filename, ) )
	except AttributeError:
		print( "no date in %s" % ( filename, ) )

	#
	#	Parse indices out of text
	#

	basic_profile = {}
	composite_profile = {}
	criterion_scores = {}

	if page[0]:
		pf_page = pages[page[0][0]]
	else:
		pf_page = pages[page[2][0]]

	basic_profile['16PF'] = [ re.search( '(1?\d) '+t, pf_page ).group(1) for t in id.basic_indices['16PF'] ]

	if page[1]:
		compositepage = ''.join([ pages[x] for x in page[1] ])

		for k,x in id.composite_indices.iteritems():
			try:
				composite_profile[k] = [ re.search( t+' (1?\d.\d)', compositepage).group(1) for t in x ]
			except AttributeError:
				pass

	if page[2]:
		basic_profile['Response Style'] = [ re.search( t+' (\d?\d)', pages[page[2][0]] ).group(1) for t in id.basic_indices['Response Style'] ]
		basic_profile['Global Factors'] = [ re.search( '(1?\d) '+t, pages[page[2][0]] ).group(1) for t in id.basic_indices['Global Factors'] ]

	if page[3]:
		compositepage = re.sub( r'.*Criterion Scores.*', '', ''.join([ pages[x] for x in page[3] ]) )
		verbose_report = ' '.join( re.sub( r'\s\s\d\s\s', r'', compositepage ).split() )

		criterion_scores = { k: [ re.search( t+'.*?\((1?\d)\).', verbose_report ).group(1) for t in x ] for k,x in id.criterion_indices.iteritems() }

	return ( UID, name, report_date, basic_profile, composite_profile, criterion_scores )

if __name__ == '__main__': sys.exit(main(sys.argv))
