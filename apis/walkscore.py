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
		Returns the Walk Score of the specified location. Both the
		lat/lon and address are required. On error, None is returned.
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
		#print_debug(tag, ("api_url: {}").format(api_url))

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
			#print_debug(tag, ("header={}, value={}").format(header, value))
			if header == 'Content-Type':
				if value != 'application/xml; charset=utf-8':
					print_error(tag, ("received unexpected Content-Type: "
						"{}").format(value))
					return None
				break

		# The expected byte string looks like:
		#   <?xml version="1.0" encoding="utf-8"?>
		#   <result xmlns="http://walkscore.com/2008/results">
		#   <status>1</status>
		#       <walkscore>95</walkscore>
		#   ...
		# XML processing: https://docs.python.org/3/library/xml.html
		# https://docs.python.org/3/library/xml.etree.elementtree.html
		# http://stackoverflow.com/a/10338267/1230197, but ->
		# http://stackoverflow.com/a/14124492/1230197
		body = response.read().decode('utf-8')   # bytes -> str
		print_debug(tag, ("body: {}").format(body))
		root = ET.fromstring(body)
		score_element = root.find('ws:walkscore',
				namespaces={'ws':'http://walkscore.com/2008/results'})
		if score_element is not None:
			print_debug(tag, ("score_element={}").format(score_element))
		else:
			print_debug(tag, ("no score_element found"))

		return None

