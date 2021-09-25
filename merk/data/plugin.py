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

	"""
		action()
		Arguments:		target (string), user (string), message (string)
		Returns:		None
		Description:	Triggered when MERK receives a CTCP action message.
						target contains the name of the target the message was
						sent to (channel or user), user contains the nickname
						and hostmask (in the format NICKNAME!USERNAME@HOST)
						of the user that sent the message, and message contains
						the message sent.
	"""
	def action(self,target,user,message):
		pass

	"""
		notice()
		Arguments:		target (string), user (string), message (string)
		Returns:		None
		Description:	Triggered when MERK receives a notice message.
						target contains the name of the target (channel or
						user) the message was sent to, user contains the
						nickname and hostmask (in the format NICKNAME!USERNAME@HOST)
						of the user that sent the message, and message
						contains the message sent.
	"""
	def notice(self,target,user,message):
		pass

	"""
		join()
		Arguments:		channel (string), user (string)
		Returns:		None
		Description:	Triggered when MERK "sees" someone joins a channel, including
						the user of the MERK client. channel is the name of the
						channel being joined, and user is the user joining.
	"""
	def join(self,channel,user):
		pass

	"""
		part()
		Arguments:		channel (string), user (string)
		Returns:		None
		Description:	Triggered when MERK "sees" someone leaves a channel, including
						the user of the MERK client. channel is the name of the
						channel being left, and user is the user leaving.
	"""
	def part(self,channel,user):
		pass

	"""
		connect()
		Arguments:		None
		Returns:		None
		Description:	Triggered when MERK completes registration with an IRC server.
	"""
	def connect(self):
		pass

	"""
		tick()
		Arguments:		uptime (integer)
		Returns:		None
		Description:	Triggers once a second while MERK is connected to a server.
						uptime contains the number of seconds the current connection
						has been connected to the server.
	"""
	def tick(self,uptime):
		pass

	"""
		topic()
		Arguments:		channel (string), newtopic (string)
		Returns:		None
		Description:	Triggered when the topic changes in a channel that MERK is "in".
						channel contains the name of the channel, and newtopic contains
						the new channel topic.
	"""
	def topic(self,channel,newtopic):
		pass

	"""
		rename()
		Arguments:		oldname (string), newname (string)
		Returns:		None
		Description:	Triggered when the nickname of a user changes in MERK's "presence".
						oldname is the user's old nickname, and newname is the user's new
						nickname.
	"""
	def rename(self,oldname,newname):
		pass

	"""
		quit()
		Arguments:		user (string), message (string)
		Returns:		None
		Description:	Triggered when a user disconnects from IRC in MERK's "presence".
						user is the nickname of the user that quit, and message is
						the quit message the user left (if they left one; if they did not,
						message will be an empty string).
	"""
	def quit(self,user,message):
		pass

	"""
		kick()
		Arguments:		channel (string), kicker (string), kickee (string), message (string)
		Returns:		None
		Description:	Triggered when a user is kicked from a channel that MERK is "in".
						channel is the name of the channel the user was kicked from, kicker
						is the user performed the kick, kickee is the user that was kicked,
						and message is the kick message.
	"""
	def kick(self,channel,kicker,kickee,message):
		pass

	"""
		kicked()
		Arguments:		channel (string), kicker (string), message (string)
		Returns:		None
		Description:	Triggered when MERK is kicked from a channel. channel is
						the name of the channel, kicker is the user that perfomed
						the kick, and message is the kick message.
	"""
	def kicked(self,channel,kicker,message):
		pass

	"""
		mode()
		Arguments:		target (string), user (string), mset (boolean), modes (string), args (tuple)
		Returns:		None
		Description:	Triggered when MERK receives a mode change notification.
						target is the target of the mode change, user is the
						user setting the mode, mset is True if the mode is being set
						and False if the mode is being unset, modes is the modes
						being set or unset, and args is any arguments to the mode being
						set or unset
	"""
	def mode(self,target,user,mset,modes,args):
		pass

	"""
		invite()
		Arguments:		channel (string), user (string)
		Returns:		None
		Description:	Triggered when MERK receives a channel invite. channel contains
						the name of the channel, and user user contains the
						nickname and hostmask (in the format NICKNAME!USERNAME@HOST)
						of the user that sent the invitation.
	"""
	def invite(self,channel,user):
		pass
	