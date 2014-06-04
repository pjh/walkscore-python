#! /usr/bin/env python3

# Playground for exploring the Walk Score API. For now, just wrap the
# API calls with Python methods.
# Copyright (c) 2014 Peter Hornyack

from util.pjh_utils import *
from apis.walkscore import WalkScore
import argparse
import re
import sys

##############################################################################

def read_api_key(api_keyfile):
	"""Attempts to read the Walk Score API key from the specified file.
	The API key should be the only string on the first line of the
	file.

	Returns: the API key string on success, or None on error.
	"""
	tag = 'read_api_key'


	# Handle exceptions when using 'with' context manager:
	# http://stackoverflow.com/a/713814/1230197
	try:
		with open(api_keyfile, 'r') as f:
			firstline = f.readline()
	except IOError:
		print_error(tag, ("cannot open {}").format(api_keyfile))
		return None

	api_key_re = re.compile('^([a-zA-Z0-9]+)$')
	api_key_match = api_key_re.search(firstline)
	if api_key_match:
		api_key = api_key_match.group(0)
	else:
		print_error(tag, ("firstline didn't match API key regex: "
			"{}").format(firstline))
		return None
	
	return api_key

def build_arg_parser():
	"""Returns an ArgumentParser instance."""
	tag = 'build_arg_parser'

	parser = argparse.ArgumentParser(
		description=("Walk Score API playground"),
		add_help=True)
	parser.add_argument(
		'api_keyfile', metavar='api-keyfile', type=str,
		help='file containing WS API key')

	return parser

# Main:
if __name__ == '__main__':
	tag = 'main'

	parser = build_arg_parser()
	args = parser.parse_args(sys.argv[1:])
	#print_debug(tag, ("parsed args: {}").format(args))
	api_keyfile = args.api_keyfile

	api_key = read_api_key(api_keyfile)
	if api_key is None:
		print_error(tag, ("unable to read API key from {}").format(
			api_keyfile))
		sys.exit(1)

	test_lat = 47.6085
	test_lon = -122.3295
	test_addr = '1119%208th%20Avenue%20Seattle%20WA%2098101'
		# TODO: use urllib.parse.quote to escape spaces and special
		# characters in a normal address.

	ws = WalkScore(api_key)
	result = ws.score(test_lat, test_lon, test_addr)
	if result is None:
		sys.exit(1)
	
	print("Got walk score: {}".format(result['walkscore']))

	sys.exit(0)
else:
	print('Must run stand-alone')
	sys.exit(1)
