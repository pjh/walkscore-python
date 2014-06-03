# Playground for exploring the Walk Score API. For now, just wrap the
# API calls with Python methods.
# Copyright (c) 2014 Peter Hornyack

from util.pjh_utils import *

class WalkScore:
	"""Class encapsulating Walk Score API calls."""
	tag = 'WalkScore'

	def __init__(self, api_key):
		tag = "{}.__init__".format(self.tag)

		self.api_key = api_key

		return

	def score(self, lat, lon, address):
		"""Returns the Walk Score of the specified location. Both the
		lat/lon and address are required.
		"""
		tag = "{}.score".format(self.tag)

		return

