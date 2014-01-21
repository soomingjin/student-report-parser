#!/usr/bin/env python2

from subprocess import check_output

def get( filename ): return check_output( [ "ps2ascii", filename ] )

if __name__ == "__main__":
	import sys, getopt

	try:
		( opts, args ) = getopt.getopt( sys.argv[1:], 'd' )
	except getopt.GetoptError:
		pass

	for filename in args: 
		file = get( filename )
		if not file: print filename
