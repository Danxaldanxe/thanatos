# Import python modules

# Import core modules
from core import check_page
from core.algorithm_loader import *
from core import config
from core import adiffer
from core import colors
from core.log import *
from core import wikipedia_worker
import threading, queue
import webbrowser
import pywikibot.exceptions
from core import warning

class PageLoader(threading.Thread):
	running = True
	pages = None
	pageobjects = None
	killer = None

	def __init__(self, pages, pageobjects, killer):
		self.pages = pages
		self.pageobjects = pageobjects
		self.killer = killer
		threading.Thread.__init__(self)

	def run(self):
		for page in self.pages:
			if self.killer.kill == True:
				return
			if page.isspace():
				continue
			self.pageobjects.append(wikipedia_worker.loadpage(page))
		self.running = False

class PageSaver(threading.Thread):
	wpage = None
	comments = None

	def __init__(self, wpage, comments):
		self.wpage = wpage
		self.comments = comments
		threading.Thread.__init__(self)

	def run(self):
		try:
			self.wpage.save(self.comments)
			log("saved "+str(self.wpage))
		except pywikibot.exceptions.EditConflict:
			log("edit conflict not saved "+str(self.wpage))

class Killer:
	kill = False
	def __init__(self):
		self.kill = False

def page_handler(algorithms, pageobjects, pageloader):
	num = 0
	while True:
		try:
			printlog("checking: "+str(pageobjects[num][1]))
			data = check_page.run(pageobjects[num][2], pageobjects[num][3], algorithms)

			if data[2] == False:
				save_page(pageobjects[num][1], pageobjects[num][2], data[0], data[1])

			if num == len(pageobjects)-1 and pageloader.running == False:
				break

			num += 1

		except IndexError:
			if num == len(pageobjects)-1 and pageloader.running == False:
				break
savethreads = []

def check_pages(pages):
	try:
		algorithms = load_algorithms()
		killer = Killer()
		pageobjects = []
		pageloader = PageLoader(pages, pageobjects, killer)
		pageloader.start()
		page_handler(algorithms, pageobjects, pageloader)

		print("saving pages...")
	except KeyboardInterrupt:
		killer.kill = True
		print("\nplease wait saving pages...")
		for thread in savethreads:
			thread.join()
		print()
		raise


def save_page(wpage, text, newtext, comments):
	if text == '':
		printlog("error: this page is empty or it doesn't exist")
		return
	if comments == None:
		comments = "thanatos bot edit"

	if newtext != text:
		if config.review == True:
			adiffer.show_diff(text, newtext)
			print(colors.yellow+str(wpage)+": "+comments+colors.end)
			warning.check(text, str(wpage))
			answer = input('do you agree these changes? [Y/N] ')
			if answer == 'p':
				print(newtext)
				answer = input('do you agree these changes? [Y/N] ')
			elif answer == 'e':
				artc = str(wpage).replace("[["+config.lang+":", "").replace("]]", "")
				webbrowser.open_new_tab("https://"+config.lang+".wikipedia.org/w/index.php?title="+artc+"&action=edit")
			if answer == 'y' or answer == 'Y':
				pass
			else:
				return
			wpage.text = newtext
			pagesaver = PageSaver(wpage, comments)
			pagesaver.start()
			savethreads.append(pagesaver)

		else:
			wpage.text = newtext
			pagesaver = PageSaver(wpage, comments)
			pagesaver.start()
			savethreads.append(pagesaver)
	else:
		warning.check(text, str(wpage))