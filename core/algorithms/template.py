from core.algcore import *

class Algorithm:
	zeroedit = False
	error_count = 0
	parse = True

	comments = {
		"fi0": "comment1",
		"fi1": "comment2",
	}

	def __init__(self):
		self.error_count = 0

	def run(self, page, text):
		return text, self.error_count
