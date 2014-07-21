import sys

if __package__ is None and not hasattr(sys, 'frozen'):
	import os.path
	path = os.path.realpath(os.path.abspath(__file))
	sys.path.append(os.path.dirname(os.path.dirname(path)))
