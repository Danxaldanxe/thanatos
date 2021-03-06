from core.algcore import *
import re
from topy import topy

class Algorithm:
	zeroedit = False
	error_count = 0
	parse = True

	comments = {
		"fi0": u"korjasi typon",
		"en0": u"fixed typo",
	}

	def __init__(self):
		self.error_count = 0

	def run(self, page, text):
		oldtext = text
		text = topy.fixtypo(text)
		if text != oldtext:
			self.error_count += 1

		return text, self.error_count
