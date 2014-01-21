#!/usr/bin/env python2

from __future__ import print_function
from datetime import datetime
import sys, re, csv

import indices
from pdftext import get

reports = ( 'Singapore Student Narrative Report', 'Basic Interpretive Report' )

def parse_report_data( filename, cover ):
#
#	Getting the ID, Name and Date of the Report
#
	UID=''
	for s in re.findall( r'(U?ID):\s*([^\s]*)', cover):
		UID = s[1]
		if s[0] == 'UID': break 
		if 'Date' in UID: UID = re.split( 'Date', UID )[0]

	try:
		name = re.search( 'Name: (.*)', cover).group(1)
	except AttributeError:
		name = ''
		print( "no name in %s" % ( filename, ), file=sys.stderr )

	r_date = ''
	try:
		textdate = re.search( 'Date: ([^\s]* [^\s]* \d*)', cover).group(1)
		try:
			r_date = datetime.strptime(textdate,'%B %d, %Y').strftime('%Y-%m-%d')
		except ValueError:
			print( "%s date format unknown" % ( filename, ), file=sys.stderr )
	except AttributeError:
		print( "no date in %s" % ( filename, ), file=sys.stderr )

	return ( UID, name, r_date )

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

	data = []

	header = [ 'ID', 'Name', 'Date' ]
	header.extend( indices.flatten( indices.basic_short ) )
	header.extend( indices.flatten( indices.composite_short ) )
	header.extend( indices.flatten( indices.criterion_short ) )

	data.append( header )

	for filename in args:
		r = parse_report( filename )

		if r:
			row = list( r[0] )
			row.extend( [ i for x in r[1] for i in indices.flatten(x) ] ) 
			data.append( row )

	with open( 'BIR.csv', 'w' ) as csvfile:
		CSV = csv.writer( csvfile )
		for row in data: CSV.writerow(row)

if __name__ == "__main__": sys.exit(main(sys.argv))
