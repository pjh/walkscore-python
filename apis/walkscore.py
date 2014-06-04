# Playground for exploring the Walk Score API. For now, just wrap the
# API calls with Python methods.
# Copyright (c) 2014 Peter Hornyack

from util.pjh_utils import *
import urllib.request
import xml.etree.ElementTree as ET

# http://www.walkscore.com/professional/api.php
BASE_URL = 'http://api.walkscore.com'

class WalkScore:
	"""
	Class encapsulating Walk Score API calls. Must be initialized with
	a particular API key.
	"""
	tag = 'WalkScore'

	def __init__(self, api_key):
		tag = "{}.__init__".format(self.tag)

		self.api_key = api_key

		return

	def score(self, lat, lon, address):
		"""
		Performs a Walk Score API call for the specified location (both
		the lat/lon and the address are required). On success, returns
		a dict with keys matching the XML result names listed at
		http://www.walkscore.com/professional/api.php. On error,
		returns None.
		"""
		tag = "{}.score".format(self.tag)

		# Basic HTTP requests in Python:
		# https://docs.python.org/3/library/urllib.request.html#examples
		# There are various ways to construct the HTTP request, but the
		# basic urlopen with a string URL suffices to start. Eventually,
		# to make multiple repeated API calls, may want to open an HTTP
		# connection to BASE_URL and then issue multiple requests, a la
		# https://docs.python.org/3/library/http.client.html#examples.

		api_url = ("{}/score?format=xml&address={}&lat={}"
			"&lon={}&wsapikey={}").format(BASE_URL, address, lat, lon,
			self.api_key)

		# On success, urlopen returns an http.client.HTTPResponse object.
		try:
			response = urllib.request.urlopen(api_url)
		except HTTPException as e:
			print_error(tag, ("Received HTTPException: type {}, value "
				"{}").format(type(e), e.value))
			return None
		if response.status != 200:
			print_error(tag, ("Received HTTP status code {}").format(
				response.status))
			return None

		# Get the type and encoding for the response's body. For now,
		# just check for expected response: XML with utf-8 encoding.
		for (header, value) in response.getheaders():
			if header == 'Content-Type':
				if value != 'application/xml; charset=utf-8':
					print_error(tag, ("received unexpected Content-Type: "
						"{}").format(value))
					return None
				break

		# The expected XML body looks like:
		#   <?xml version="1.0" encoding="utf-8"?>
		#   <result xmlns="http://walkscore.com/2008/results">
		#       <status>1</status>
		#       <walkscore>95</walkscore>
		#       ...
		#   </result>
		# XML processing: https://docs.python.org/3/library/xml.html
		# https://docs.python.org/3/library/xml.etree.elementtree.html
		#
		# The element with tag 'result' is the root of the XML tree;
		# there can only be one result (or else it would be a forest,
		# not a tree!).
		body = response.read().decode('utf-8')   # bytes -> str
		root = ET.fromstring(body)

		# The 'xmlns' attribute in the result element is a namespace
		# specifier, which necessitates some special handling when parsing
		# / finding elements; if the target namespace is not specified
		# correctly, then it is implicitly prepended to the .tag value of
		# every Element, which is annoying.
		#   http://stackoverflow.com/a/10338267/1230197, but ->
		#   http://stackoverflow.com/a/14124492/1230197
		# For now, the namespace is hard-coded here, but it could be
		# pulled out of the root element's tag instead.
		ns = {'ws':'http://walkscore.com/2008/results'}

		# Before constructing the result dict, check the status that was
		# returned: we may have received an HTTP 200, but the API's status
		# could indicate an unsuccessful result.
		status = int(root.find('ws:status', namespaces=ns).text)
		if status != 1:
			if status == 2:
				descr = ('Score is being calculated and is not currently '
					'available.')
			elif status == 40:
				descr = ('Your WSAPIKEY is invalid.')
			elif status == 41:
				descr = ('Your daily API quota has been exceeded.')
			elif status == 42:
				descr = ('Your IP address has been blocked.')
			else:
				descr = ('Unknown')
			print_error(tag, ("Response has bad status code {}: {}").format(
				status, descr))
			return None

		result = dict()
		result['status'] = status
		result['walkscore'] = int(root.find('ws:walkscore',
		                                    namespaces=ns).text)
		result['description'] = root.find('ws:description', namespaces=ns).text
		result['updated'] = root.find('ws:updated', namespaces=ns).text
		result['logo_url'] = root.find('ws:logo_url', namespaces=ns).text
		result['more_info_icon'] = root.find('ws:more_info_icon',
		                                     namespaces=ns).text
		result['more_info_link'] = root.find('ws:more_info_link',
		                                     namespaces=ns).text
		result['ws_link'] = root.find('ws:ws_link', namespaces=ns).text
		result['snapped_lat'] = float(root.find('ws:snapped_lat',
		                                        namespaces=ns).text)
		result['snapped_lon'] = float(root.find('ws:snapped_lon',
		                                        namespaces=ns).text)

		return result

