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
	
	"""
		public()
		Arguments:		channel (string), user (string), message (string)
		Returns:		None
		Description:	Triggered when MERK receives a public (channel) message.
						channel contains the name of the channel the message was
						sent to, user contains the nickname and hostmask (in the
						format NICKNAME!USERNAME@HOST) of the user that sent the
						message, and message contains the message sent.
	"""
	def public(self,channel,user,message):
		pass

	"""
		private()
		Arguments:		user (string), message (string)
		Returns:		None
		Description:	Triggered when MERK receives a private message.
						user contains the nickname and hostmask (in the format
						NICKNAME!USERNAME@HOST) of the user that sent the
						message, and message contains the message sent.
	"""
	def private(self,user,message):
		pass
	