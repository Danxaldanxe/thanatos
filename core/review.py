import difflib

def show_diff(oldtext, text):
	sm= difflib.SequenceMatcher(None, oldtext, text)
	high_light(sm)
	accept = input("do you agree these changes? [Y/N] ")
	if accept == "y" or accept == "yes" or accept == "Y" or accept == "YES":
		return True
	return False

def high_light(seqm):
	green= '\033[32m'
	red = '\033[91m'
	end = '\033[0m'
	bold = '\033[1m'
	underline = '\033[4m'
	bu = bold+underline
	output= []
	for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
		if opcode == 'equal':
			output.append(seqm.a[a0:a1])
		elif opcode == 'insert':
			output.append(bu + green + seqm.b[b0:b1] + end)
		elif opcode == 'delete':
			output.append(bu + red + seqm.a[a0:a1] + end)
		elif opcode == 'replace':
			output.append(bu + green + seqm.b[b0:b1] + end)
		else:
			print("unexpected opcode")
	print(''.join(output))

def show_diffl(oldtext, text):
	sm= difflib.SequenceMatcher(None, oldtext, text)
	high_light2(sm)
	accept = input("do you agree these changes? [Y/N] ")
	if accept == "y" or accept == "yes" or accept == "Y" or accept == "YES":
		return True
	return False

def high_light2(seqm):
	green= '\033[32m'
	red = '\033[91m'
	end = '\033[0m'
	whg = '\033[1;47m'
	ehg = '\033[1;m'
	output= []
	for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
		if opcode == 'equal':
			output.append(seqm.a[a0:a1])
		elif opcode == 'insert':
			output.append(whg + green + seqm.b[b0:b1] + end + ehg)
		elif opcode == 'delete':
			output.append(whg + red + seqm.a[a0:a1] + end + ehg)
		elif opcode == 'replace':
			output.append(whg + green + seqm.b[b0:b1] + end + ehg)
		else:
			print("unexpected opcode")
	print(''.join(output))
