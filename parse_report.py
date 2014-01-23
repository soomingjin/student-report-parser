#!/usr/bin/env python2

from __future__ import print_function
from datetime import datetime
import sys, re

import indices as ix
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
	print( "[%s] Reading %s ... " % (datetime.now().strftime('%H:%M:%S'), filename), end='' )

	file = get( filename )

	if not file:
		print( "error! No text in %s" % (filename,), file=sys.stderr )
		return False

	print( "Ok. ", end='' )

	report_type, pages = [ ( rt, file.split(rt)[1:] ) for rt in reports if rt in file ][0]

	print( "Parsing %s ... " % (report_type,), end='' )

	r_d = parse_report_data( filename, pages[0] )
	r_i = ix.parse_indices( pages )

	print( "OK" )

	return ( r_d, r_i )

def wtf( filename, header, data ):
	import csv
	with open( filename, 'w' ) as csvfile:
		CSV = csv.writer( csvfile )
		CSV.writerow(header)
		for row in data: CSV.writerow(row)


def main(arg):
	import getopt

	def usage():
		print ( 'usage: %s file ...' % argv[0] )
		return 100

	try:
		opts, args = getopt.getopt( arg[1:], 'do:v' ['output-file='] )
	except getopt.GetoptError:
		return usage()

	write_out = False

	for o, a in opts:
		if o in ( "-o", "--output-file" ):
			write_out = o[1]

	if not args: return usage()

	data = []

	for filename in args:
		r = parse_report( filename )

		if r:
			row = list( r[0] )
			row.extend( ix.flatten( r[1] ) )
			data.append( row )

	if write_out:
		header = [ 'ID', 'Name', 'Date' ].extend( ix.flatten( ix.read_config() ) )
		wtf( write_out, header, data )

if __name__ == "__main__": sys.exit(main(sys.argv))
