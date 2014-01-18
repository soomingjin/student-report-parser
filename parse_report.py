#!/usr/bin/env python2

from __future__ import print_function
from datetime import datetime
import sys, csv, re

import indices
from pdftext import get

reports = ( 'Singapore Student Narrative Report', 'Basic Interpretive Report' )

def parse_report_data( filename, cover ):
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
		name = ''
		print( "no name in %s" % ( filename, ), file=sys.stderr )

	report_date = ''
	try:
		textdate = re.search( 'Date: ([^\s]* [^\s]* \d*)', cover).group(1)
		try:
			report_date = datetime.strptime( textdate, '%B %d, %Y' ).strftime( '%Y-%m-%d' )
		except ValueError:
			print( "%s date format unknown" % ( filename, ), file=sys.stderr )
	except AttributeError:
		print( "no date in %s" % ( filename, ), file=sys.stderr )

	return ( UID, name, report_date )

def parse_report( filename ):
#
#	Beef
#
	file = get( filename )

	if not file:
		print( "error! no text could be read from %s" % ( filename, ), file=sys.stderr )
		return False

	report_type, pages = [ ( rt, file.split(rt)[1:] ) for rt in reports if rt in file ][0]

	return ( parse_report_data( filename, pages[0] ), indices.parse_indices( pages ) )

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

	header = [ 'ID', 'Name', 'Date' ]
	header.extend( indices.flatten( indices.basic_short ) )
	header.extend( indices.flatten( indices.composite_short ) )
	header.extend( indices.flatten( indices.criterion_short ) )

	with open( 'BIR.csv', 'w' ) as csvfile:
		CSV = csv.writer( csvfile )

		CSV.writerow(header)

		for filename in args:
			report = parse_report( filename )
			if report:
				row = list( report[0] )
				row.extend( [ i for x in report[1] for i in indices.flatten(x) ] ) 
				CSV.writerow( row ) 

if __name__ == "__main__": main(sys.argv)
