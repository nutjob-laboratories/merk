from merk import *

"""
	PACKAGE is the name that the plugin will display
	in MERK's plugin menu; any classes in this file will
	be shown in a submenu.
"""
PACKAGE = "MERK Plugin"

class MERKPlugin(Plugin):
	"""
		This is a basic "blank" MERK plugin with all the
		event methods available. Just change the name of
		the class, change the "NAME", "VERSION", and
		"DESCRIPTION" class attributes, and you're half-
		way to writing a MERK plugin!
	"""
	NAME = "MERK Plugin"
	VERSION = "1.0"
	DESCRIPTION = "This is a MERK plugin"

	"""
		load()
		Arguments:		None
		Returns:		None
		Description:	Triggered when MERK initially loads the plugin.
	"""
	def load(self):
		pass

	"""
		unload()
		Arguments:		None
		Returns:		None
		Description:	Triggered when MERK unloads the plugin (when it is closing).
	"""
	def unload(self):
		pass

	"""
		line_in()
		Arguments:		data (string)
		Returns:		None
		Description:	Triggered when MERK receives data from the IRC server. data
						contains the information sent by the server.
	"""
	def line_in(self,data):
		pass

	"""
		line_out()
		Arguments:		data (string)
		Returns:		None
		Description:	Triggered when MERK sends data to the IRC server. data
						contains the information sent to the server.
	"""
	def line_out(self,data):
		pass
	