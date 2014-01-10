#!/usr/bin/env python2

from subprocess import check_output

def get(filename):
	return check_output(["ps2ascii",filename])
