#
# ███╗   ███╗██████╗ ██████╗ ██╗  ██╗
# ████╗ ████║╚═══╗██╗██╔══██╗██║ ██╔╝
# ██╔████╔██║███████║██████╔╝█████╔╝
# ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗
# ██║ ╚═╝ ██║ █████╔╝██║  ██║██║  ██╗
# ╚═╝     ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
# Copyright (C) 2021  Daniel Hetrick
# https://github.com/nutjob-laboratories/merk
# https://github.com/nutjob-laboratories
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

SSL_AVAILABLE = True

import sys
import random
import time
import uuid

from twisted.internet import reactor, protocol

try:
	from twisted.internet import ssl
except ImportError as error:
	SSL_AVAILABLE = False
except Exception as exception:
	pass

from twisted.words.protocols import irc
from twisted.words.protocols.irc import ctcpStringify

from .resources import *
from . import config

def connect(**kwargs):
	bot = IRC_Connection_Factory(**kwargs)
	reactor.connectTCP(kwargs["server"],kwargs["port"],bot)

def connectSSL(**kwargs):
	bot = IRC_Connection_Factory(**kwargs)
	reactor.connectSSL(kwargs["server"],kwargs["port"],bot,ssl.ClientContextFactory())

def reconnect(**kwargs):
	bot = IRC_ReConnection_Factory(**kwargs)
	reactor.connectTCP(kwargs["server"],kwargs["port"],bot)

def reconnectSSL(**kwargs):
	bot = IRC_ReConnection_Factory(**kwargs)
	reactor.connectSSL(kwargs["server"],kwargs["port"],bot,ssl.ClientContextFactory())

class IRC_Connection(irc.IRCClient):
	nickname = 'bot'
	realname = 'bot'
	username = 'bot'

	versionName = APPLICATION_NAME
	versionNum = APPLICATION_VERSION

	heartbeatInterval = 120

	def __init__(self,**kwargs):

		self.kwargs = kwargs

		objectconfig(self,**kwargs)

		self.client_id = str(uuid.uuid4())

		self.oldnick = self.nickname
		self.uptime = 0
		self.registered = False
		self.last_tried_nickname = ''

		self.names = {}

		self.maxnicklen = 0
		self.maxchannels = 0
		self.channellen = 0
		self.topiclen = 0
		self.kicklen = 0
		self.awaylen = 0
		self.maxtargets = 0
		self.casemapping = ""
		self.cmds = []
		self.prefix = []
		self.chanmodes = []
		self.supports = []
		self.modes = 0
		self.maxmodes = []


	def uptime_beat(self):

		self.uptime = self.uptime + 1

	def connectionMade(self):

		# PROTOCTL UHNAMES
		self.sendLine("PROTOCTL UHNAMES")

		irc.IRCClient.connectionMade(self)

		self.gui.connectionMade(self)

	def connectionLost(self, reason):

		if hasattr(self,"uptimeTimer"):
			self.uptimeTimer.stop()
			self.uptime = 0

		self.registered = False

		irc.IRCClient.connectionLost(self, reason)

		self.gui.connectionLost(self)

	def signedOn(self):

		self.uptimeTimer = UptimeHeartbeat()
		self.uptimeTimer.beat.connect(self.uptime_beat)
		self.uptimeTimer.start()

		self.registered = True

		self.gui.signedOn(self)

	def joined(self, channel):
		self.sendLine(f"MODE {channel}")
		self.sendLine(f"MODE {channel} +b")

		self.gui.joined(self,channel)

	def left(self, channel):
		self.gui.left(self,channel)

	def privmsg(self, user, target, msg):
		pnick = user.split('!')[0]
		phostmask = user.split('!')[1]

		self.gui.privmsg(self,user,target,msg)

	def noticed(self, user, channel, msg):
		tok = user.split('!')
		if len(tok) >= 2:
			pnick = tok[0]
			phostmask = tok[1]
		else:
			pnick = user
			phostmask = user

		self.gui.noticed(self,user,channel,msg)

	def receivedMOTD(self, motd):
		
		self.gui.receivedMOTD(self,motd)

	def nickChanged(self,nick):
		self.nickname = nick

	def userJoined(self, user, channel):
		if user.split('!')[0] == self.nickname:
			return

		self.sendLine("NAMES "+channel)

	def userLeft(self, user, channel):

		self.sendLine("NAMES "+channel)

	def nickChanged(self,nick):
		self.nickname = nick

		self.gui.nickChanged(self)

	def irc_ERR_NICKNAMEINUSE(self, prefix, params):

		if self.registered:
			# Since we're already registered, just
			# let the user know that the desired nickname
			# is already in use
			return

		oldnick = params[1]

		if self.last_tried_nickname=='':
			self.last_tried_nickname = self.alternate
			self.setNick(self.alternate)
			return

		rannum = random.randrange(1,99)

		self.last_tried_nickname = self.last_tried_nickname + str(rannum)
		self.setNick(self.last_tried_nickname)

	def userRenamed(self, oldname, newname):
		pass

	def topicUpdated(self, user, channel, newTopic):
		pass

	def action(self, user, channel, data):
		pnick = user.split('!')[0]
		phostmask = user.split('!')[1]

	def userKicked(self, kickee, channel, kicker, message):
		self.sendLine("NAMES "+channel)

	def kickedFrom(self, channel, kicker, message):
		pass

	def irc_QUIT(self,prefix,params):
		x = prefix.split('!')
		if len(x) >= 2:
			nick = x[0]
		else:
			nick = prefix
		if len(params) >=1:
			m = params[0].split(':')
			if len(m)>=2:
				msg = m[1].strip()
			else:
				msg = ""
		else:
			msg = ""

	def irc_RPL_NAMREPLY(self, prefix, params):
		channel = params[2].lower()
		nicklist = params[3].split(' ')

		if channel in self.names:
			for nick in nicklist:
				self.names[channel].append(nick)
		else:
			self.names[channel] = nicklist

	def irc_RPL_ENDOFNAMES(self, prefix, params):

		channel = params[1].lower()

		if channel in self.names:
			self.gui.names(self,channel,self.names[channel])
			del self.names[channel]

	def irc_RPL_TOPIC(self, prefix, params):
		if not params[2].isspace():
			TOPIC = params[2]
		else:
			TOPIC = ""

		channel = params[1]

	def lineReceived(self, line):

		# Decode the incoming text line
		try:
			line2 = line.decode('utf-8')
		except UnicodeDecodeError:
			try:
				line2 = line.decode('iso-8859-1')
			except UnicodeDecodeError:
				line2 = line.decode("CP1252", 'replace')

		# Re-encode the text line to utf-8 for all other
		# IRC events (this fixes an error raised when attempting
		# to get a channel list from a server)
		line = line2.encode('utf-8')

		d = line2.split(" ")
		if len(d) >= 2:
			if d[1].isalpha(): return irc.IRCClient.lineReceived(self, line)

		if "Cannot join channel (+k)" in line2:
			#events.received_error(self.gui,self,f"Cannot join channel (wrong or missing password)")
			pass
		if "Cannot join channel (+l)" in line2:
			#events.received_error(self.gui,self,f"Cannot join channel (channel is full)")
			pass
		if "Cannot join channel (+b)" in line2:
			#events.received_error(self.gui,self,f"Cannot join channel (banned)")
			pass
		if "Cannot join channel (+i)" in line2:
			#events.received_error(self.gui,self,f"Cannot join channel (channel is invite only)")
			pass
		if "not an IRC operator" in line2:
			#events.received_error(self.gui,self,"Permission denied (you're not an IRC operator")
			pass
		if "not channel operator" in line2:
			#events.received_error(self.gui,self,"Permission denied (you're not channel operator)")
			pass
		if "is already on channel" in line2:
			#events.received_error(self.gui,self,"Invite failed (user is already in channel)")
			pass
		if "not on that channel" in line2:
			#events.received_error(self.gui,self,"Permission denied (you're not in channel)")
			pass
		if "aren't on that channel" in line2:
			#events.received_error(self.gui,self,"Permission denied (target user is not in channel)")
			pass
		if "have not registered" in line2:
			#events.received_error(self.gui,self,"You're not registered")
			pass
		if "may not reregister" in line2:
			#events.received_error(self.gui,self,"You can't reregister")
			pass
		if "enough parameters" in line2:
			#events.received_error(self.gui,self,"Error: not enough parameters supplied to command")
			pass
		if "isn't among the privileged" in line2:
			#events.received_error(self.gui,self,"Registration refused (server isn't setup to allow connections from your host)")
			pass
		if "Password incorrect" in line2:
			#events.received_error(self.gui,self,"Permission denied (incorrect password)")
			pass
		if "banned from this server" in line2:
			#events.received_error(self.gui,self,"You are banned from this server")
			pass
		if "kill a server" in line2:
			#events.received_error(self.gui,self,"Permission denied (you can't kill a server)")
			pass
		if "O-lines for your host" in line2:
			#events.received_error(self.gui,self,"Error: no O-lines for your host")
			pass
		if "Unknown MODE flag" in line2:
			#events.received_error(self.gui,self,"Error: unknown MODE flag")
			pass
		if "change mode for other users" in line2:
			#events.received_error(self.gui,self,"Permission denied (can't change mode for other users)")
			pass

		return irc.IRCClient.lineReceived(self, line)

	def isupport(self,options):
		self.options = options

		for o in options:
			p = o.split('=')
			if len(p)==2:
				if p[0].lower()=='network':
					self.network = p[1]

		self.server_options(options)

	def server_options(self,options):

		# Options are sent in chunks: not every option
		# will be set in each chunk

		supports = []
		maxchannels = 0
		maxnicklen = 0
		nicklen = 0
		channellen = 0
		topiclen = 0
		kicklen = 0
		awaylen = 0
		maxtargets = 0
		modes = 0
		maxmodes = []
		chanmodes = []
		prefix = []
		cmds = []
		casemapping = "none"

		for o in options:
			if "=" in o:
				p = o.split("=")
				if len(p)>1:
					if p[0].lower() == "maxchannels": maxchannels = int(p[1])
					if p[0].lower() == "maxnicklen": maxnicklen = int(p[1])
					if p[0].lower() == "nicklen": nicklen = int(p[1])
					if p[0].lower() == "channellen": channellen = int(p[1])
					if p[0].lower() == "topiclen": topiclen = int(p[1])
					if p[0].lower() == "kicklen": kicklen = int(p[1])
					if p[0].lower() == "awaylen": awaylen = int(p[1])
					if p[0].lower() == "maxtargets": maxtargets = int(p[1])
					if p[0].lower() == "modes": modes = int(p[1])
					if p[0].lower() == "casemapping": casemapping = p[1]

					if p[0].lower() == "cmds":
						for c in p[1].split(","):
							cmds.append(c)

					if p[0].lower() == "prefix":
						pl = p[1].split(")")
						if len(pl)>=2:
							pl[0] = pl[0][1:]	# get rid of prefixed (

							for i in range(len(pl[0])):
								entry = [ pl[0][i], pl[1][i] ]
								prefix.append(entry)

					if p[0].lower() == "chanmodes":
						for e in p[1].split(","):
							chanmodes.append(e)

					if p[0].lower() == "maxlist":
						for e in p[1].split(","):
							ml = e.split(':')
							if len(ml)==2:
								entry = [ml[0],int(ml[1])]
								maxmodes.append(entry)
			else:
				supports.append(o)

		if len(maxmodes)>0: self.maxmodes = maxmodes
		if maxnicklen>0: self.maxnicklen = maxnicklen
		if maxchannels > 0: self.maxchannels = maxchannels
		if channellen > 0: self.channellen = channellen
		if topiclen > 0: self.topiclen = topiclen
		if kicklen > 0: self.kicklen = kicklen
		if awaylen > 0: self.awaylen = awaylen
		if maxtargets > 0: self.maxtargets = maxtargets
		if modes > 0: self.modes = modes
		if casemapping != "": self.casemapping = casemapping

		if len(cmds)>0:
			for c in cmds:
				self.cmds.append(c)

		if len(prefix)>0: self.prefix = prefix
		if len(chanmodes)>0: self.chanmodes = chanmodes
		if len(supports)>0:
			for s in supports:
				self.supports.append(s)

class UptimeHeartbeat(QThread):

	beat = pyqtSignal()

	def __init__(self,parent=None):
		super(UptimeHeartbeat, self).__init__(parent)
		self.threadactive = True

	def run(self):
		while self.threadactive:
			time.sleep(1)
			self.beat.emit()

	def stop(self):
		self.threadactive = False
		self.wait()

def objectconfig(obj,**kwargs):

	for key, value in kwargs.items():

		if key=="nickname":
			obj.nickname = value
		
		if key=="alternate":
			obj.alternate = value

		if key=="username":
			obj.username = value

		if key=="realname":
			obj.realname = value

		if key=="server":
			obj.server = value

		if key=="port":
			obj.port = value

		if key=="ssl":
			obj.usessl = value

		if key=="password":
			obj.password = value

		if key=="gui":
			obj.gui = value

		if key=="reconnect":
			obj.reconnect = value

		if key=="failreconnect":
			obj.failreconnect = value

class IRC_Connection_Factory(protocol.ClientFactory):
	def __init__(self,**kwargs):
		self.kwargs = kwargs

	def buildProtocol(self, addr):
		bot = IRC_Connection(**self.kwargs)
		bot.factory = self
		return bot

	def clientConnectionLost(self, connector, reason):
		pass

	def clientConnectionFailed(self, connector, reason):
		pass

class IRC_ReConnection_Factory(protocol.ReconnectingClientFactory):
	def __init__(self,**kwargs):
		self.kwargs = kwargs

	def buildProtocol(self, addr):
		bot = IRC_Connection(**self.kwargs)
		bot.factory = self
		return bot

	def clientConnectionLost(self, connector, reason):
		
		protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):

		if self.kwargs["failreconnect"]:
			protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

