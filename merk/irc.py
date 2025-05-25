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
from collections import defaultdict

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
from . import user

CONNECTIONS = {}

def connect(**kwargs):
	kwargs["client_id"] = str(uuid.uuid4())
	bot = IRC_Connection_Factory(**kwargs)
	reactor.connectTCP(kwargs["server"],kwargs["port"],bot)

def connectSSL(**kwargs):
	kwargs["client_id"] = str(uuid.uuid4())
	bot = IRC_Connection_Factory(**kwargs)
	reactor.connectSSL(kwargs["server"],kwargs["port"],bot,ssl.ClientContextFactory())

def reconnect(**kwargs):
	kwargs["client_id"] = str(uuid.uuid4())
	bot = IRC_ReConnection_Factory(**kwargs)
	reactor.connectTCP(kwargs["server"],kwargs["port"],bot)

def reconnectSSL(**kwargs):
	kwargs["client_id"] = str(uuid.uuid4())
	bot = IRC_ReConnection_Factory(**kwargs)
	reactor.connectSSL(kwargs["server"],kwargs["port"],bot,ssl.ClientContextFactory())

class IRC_Connection(irc.IRCClient):
	nickname = 'merk'
	realname = 'merk'
	username = 'merk'

	versionName = APPLICATION_NAME
	versionNum = APPLICATION_VERSION
	sourceURL = APPLICATION_SOURCE

	heartbeatInterval = 120

	def __init__(self,**kwargs):

		self.kwargs = kwargs

		objectconfig(self,**kwargs)

		self.oldnick = self.nickname
		self.uptime = 0
		self.registered = False
		self.last_tried_nickname = ''

		self.names = {}
		self.usermodes = ''
		self.channelmodes = {}
		self.channelkeys = {}
		self.whoisdata = {}
		self.who = {}
		self.whowas = {}

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
		self.is_away = False
		self.request_whois = []
		self.do_whois = []

		self.server_channel_list = []
		self.doing_list_refresh = False

		self.banlists = defaultdict(list)


	def irc_RPL_LIST(self,prefix,params):
		server = prefix
		channel_name = params[1]
		channel_count = params[2]
		channel_topic = params[3].strip()
		self.server_channel_list.append( [channel_name,channel_count,channel_topic] )

	def irc_RPL_LISTEND(self,prefix,params):
		if self.doing_list_refresh:
			self.gui.gotRefreshEnd(self)
			self.doing_list_refresh = False

	def irc_RPL_LISTSTART(self,prefix,params):
		self.server_channel_list = []

	def uptime_beat(self):

		self.uptime = self.uptime + 1

		if config.GET_HOSTMASKS_ON_CHANNEL_JOIN:
			if len(self.do_whois)>0:
				nick = self.do_whois.pop(0)
				if len(nick.strip())>0:
					self.request_whois.append(nick)
					self.sendLine("WHOIS "+nick)

		self.gui.uptime(self,self.uptime)

	def connectionMade(self):

		# PROTOCTL UHNAMES
		self.sendLine("PROTOCTL UHNAMES")

		irc.IRCClient.connectionMade(self)

		CONNECTIONS[self.client_id] = self

		self.gui.connectionMade(self)

	def connectionLost(self, reason):
		global CONNECTIONS

		if hasattr(self,"uptimeTimer"):
			self.uptimeTimer.stop()
			self.uptime = 0

		self.registered = False

		del CONNECTIONS[self.client_id]

		self.gui.connectionLost(self)

		irc.IRCClient.connectionLost(self, reason)

	def signedOn(self):

		self.uptimeTimer = UptimeHeartbeat()
		self.uptimeTimer.beat.connect(self.uptime_beat)
		self.uptimeTimer.start()

		self.registered = True

		if config.REQUEST_CHANNEL_LIST_ON_CONNECTION:
			self.sendLine(f"LIST")

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

	def irc_RPL_TIME(self,prefix,params):

		server = params[1]
		time = params[2]

		self.gui.gotTime(self,server,time)

	def irc_RPL_BANLIST(self,prefix,params):
		# bans
		channel = params[1]
		mask = params[2]
		banner = params[3]
		timestamp = params[4]

		e = [mask,banner,timestamp]

		self.banlists[channel].append(e)


	def irc_RPL_ENDOFBANLIST(self,prefix,params):
		# bans end
		channel = params[1]

		banlist = []
		if channel in self.banlists:
			banlist = self.banlists[channel]
			self.banlists[channel] = []

		self.gui.gotBanlist(self,channel,banlist)

	def modeChanged(self, user, channel, mset, modes, args):
		if "b" in modes: self.sendLine(f"MODE {channel} +b")
		if "o" in modes: self.sendLine("NAMES "+channel)
		if "v" in modes: self.sendLine("NAMES "+channel)

		for m in modes:
			if mset:
				
				if channel==self.nickname: 
					self.usermodes = self.usermodes + m

				if channel in self.channelmodes:
					if not m in self.channelmodes[channel]:
						self.channelmodes[channel] = self.channelmodes[channel] + m
					else:
						continue
				else:
					self.channelmodes[channel] = m

				# Remove 'o' from channel modes
				self.channelmodes[channel] = self.channelmodes[channel].replace('o','')

				# Remove 'k' from channel modes
				self.channelmodes[channel] = self.channelmodes[channel].replace('k','')

				if m=='k':
					self.channelkeys[channel] = args[0]
					self.gui.setMode(self,user,channel,m,args[0])
					continue
				if m=='o':
					self.gui.setMode(self,user,channel,m,[args[0]])
					continue
				self.gui.setMode(self,user,channel,m,[])

			else:
				
				if channel==self.nickname: self.usermodes = self.usermodes.replace(m,'')

				if channel in self.channelmodes:
					self.channelmodes[channel] = self.channelmodes[channel].replace(m,'')

				if m=="k":
					if channel in self.channelkeys: del self.channelkeys[channel]
				if m=='o':
					self.gui.unsetMode(self,user,channel,m,[args[0]])
					continue

				self.gui.unsetMode(self,user,channel,m,[])

	def irc_RPL_CHANNELMODEIS(self, prefix, params):
		params.pop(0)
		target = params.pop(0)

		for m in params:
			if len(m)>0:
				if m[0] == "+":
					m = m[1:]

					if m=="k":
						params.pop(0)
						chankey = params.pop(0)
						self.channelkeys[target] = chankey
						self.gui.serverSetMode(self,target,m,chankey)
						continue

					if target==self.nickname:
						self.usermodes = self.usermodes+m

					if target[:1]=='#' or target[:1]=='&' or target[:1]=='!' or target[:1]=='+':
						if target in self.channelmodes:
							if not m in self.channelmodes[target]:
								self.channelmodes[target] = self.channelmodes[target] + m
							else:
								continue
						else:
							self.channelmodes[target] = m

					self.gui.serverSetMode(self,target,m,None)

				else:
					m = m[1:]

					if m=="k":
						if target in self.channelkeys: del self.channelkeys[target]
					
					if target==self.nickname:
						self.usermodes = self.usermodes.replace(m,'')

					if target[:1]=='#' or target[:1]=='&' or target[:1]=='!' or target[:1]=='+':
						if target in self.channelmodes:
							self.channelmodes[target] = self.channelmodes[target].replace(m,'')


					# mode removed
					self.gui.serverUnsetMode(self,target,m,[])

	def nickChanged(self,nick):
		self.nickname = nick

	def userJoined(self, user, channel):
		if user.split('!')[0] == self.nickname:
			return

		p = user.split('!')
		if len(p)==2:
			self.gui.updateHostmask(self,p[0],p[1])
		else:
			if user == self.nickname: return
			if config.GET_HOSTMASKS_ON_CHANNEL_JOIN:
				self.do_whois.append(user)

		self.sendLine("NAMES "+channel)

		self.gui.userJoined(self,user,channel)

	def userLeft(self, user, channel):

		p = user.split('!')
		if len(p)==2:
			if p[0] == self.nickname: return
			self.gui.updateHostmask(self,p[0],None)
		else:
			if user == self.nickname: return
			if config.GET_HOSTMASKS_ON_CHANNEL_JOIN:
				self.do_whois.append(user)

		self.sendLine("NAMES "+channel)

		self.gui.userLeft(self,user,channel)

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

		self.gui.userRenamed(self,oldname,newname)

	def action(self, user, channel, data):
		pnick = user.split('!')[0]
		phostmask = user.split('!')[1]

		self.gui.action(self,user,channel,data)

	def userKicked(self, kickee, channel, kicker, message):
		if kickee!=self.nickname: self.sendLine("NAMES "+channel)

		self.gui.userKicked(self,kickee,channel,kicker,message)

	def kickedFrom(self, channel, kicker, message):
		
		self.gui.kickedFrom(self,channel,kicker,message)

	def irc_RPL_VERSION(self, prefix, params):
		sversion = params[1]
		server = params[2]

		self.gui.gotVersion(self,server,sversion)

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

		self.gui.irc_QUIT(self,nick,msg)

	def irc_RPL_NAMREPLY(self, prefix, params):
		channel = params[2].lower()
		nicklist = params[3].split(' ')

		if config.GET_HOSTMASKS_ON_CHANNEL_JOIN:
			for u in nicklist:
				p = u.split('!')
				if len(p)!=2:
					u = u.replace('@','')
					u = u.replace('+','')
					if not self.gui.doesChannelHaveHostmask(self,channel,u):
						self.do_whois.append(u)

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

		self.gui.topicChanged(self,'',channel,TOPIC)

		return irc.IRCClient.irc_RPL_TOPIC(self, prefix, params)

	def topicUpdated(self, user, channel, newTopic):

		self.gui.topicChanged(self,user,channel,newTopic)

		return irc.IRCClient.topicUpdated(self, user, channel, newTopic)

	def irc_RPL_WHOISCHANNELS(self, prefix, params):
		params.pop(0)
		nick = params.pop(0)
		channels = ", ".join(params)

		if nick in self.request_whois: return

		if nick in self.whoisdata:
			self.whoisdata[nick].channels = channels
		else:
			self.whoisdata[nick] = WhoisData()
			self.whoisdata[nick].nickname = nick
			self.whoisdata[nick].channels = channels

	def irc_RPL_WHOISUSER(self, prefix, params):
		nick = params[1]
		username = params[2]
		host = params[3]
		realname = params[5]

		if nick in self.request_whois:
			self.gui.updateHostmask(self,nick,username+"@"+host)
			return

		if nick in self.whoisdata:
			self.whoisdata[nick].username = username
			self.whoisdata[nick].host = host
			self.whoisdata[nick].realname = realname
		else:
			self.whoisdata[nick] = WhoisData()
			self.whoisdata[nick].nickname = nick
			self.whoisdata[nick].username = username
			self.whoisdata[nick].host = host
			self.whoisdata[nick].realname = realname

	def irc_RPL_WHOISIDLE(self, prefix, params):
		params.pop(0)
		nick = params.pop(0)
		idle_time = params.pop(0)
		signed_on = params.pop(0)

		if nick in self.request_whois: return

		if nick in self.whoisdata:
			self.whoisdata[nick].idle = idle_time
			self.whoisdata[nick].signon = signed_on
		else:
			self.whoisdata[nick] = WhoisData()
			self.whoisdata[nick].nickname = nick
			self.whoisdata[nick].idle = idle_time
			self.whoisdata[nick].signon = signed_on

	def irc_RPL_WHOISSERVER(self, prefix, params):
		nick = params[1]
		server = params[2]

		if nick in self.request_whois: return

		if nick in self.whoisdata:
			self.whoisdata[nick].server = server
		else:
			self.whoisdata[nick] = WhoisData()
			self.whoisdata[nick].nickname = nick
			self.whoisdata[nick].server = server

	def irc_RPL_WHOISOPERATOR(self,prefix,params):
		nick = params[1]
		privs = params[2]

		if nick in self.request_whois: return

		if nick in self.whoisdata:
			self.whoisdata[nick].privs = privs
		else:
			self.whoisdata[nick] = WhoisData()
			self.whoisdata[nick].nickname = nick
			self.whoisdata[nick].privs = privs

	def irc_RPL_ENDOFWHOIS(self, prefix, params):
		nick = params[1]

		if nick in self.request_whois:
			try:
				self.request_whois.remove(nick)
			except:
				pass
			return

		if nick in self.whoisdata:
			self.gui.whois(self,self.whoisdata[nick])
			del self.whoisdata[nick]

	def irc_RPL_WHOREPLY(self, prefix, params):
		channel = params[1]
		username = params[2]
		host = params[3]
		server = params[4]
		nick = params[5]
		hr = params[7].split(' ')

		if nick in self.who:
			entry = WhoData()
			entry.channel = channel
			entry.username = username
			entry.host = host
			entry.server = server
			self.who[nick].append(entry)
		else:
			self.who[nick] = []
			entry = WhoData()
			entry.channel = channel
			entry.username = username
			entry.host = host
			entry.server = server
			self.who[nick].append(entry)


	def irc_RPL_ENDOFWHO(self, prefix, params):
		nick = params[1]

		if nick in self.who:
			replies = self.who[nick]
			del self.who[nick]
			self.gui.who(self,nick,replies)

	def irc_RPL_WHOWASUSER(self, prefix, params):
		nick = params[1]
		username = params[2]
		host = params[3]
		realname = params[5]

		if nick in self.whowas:
			entry = WhoWasData()
			entry.username = username
			entry.host = host
			entry.realname = realname
			self.whowas[nick].append(entry)
		else:
			self.whowas[nick] = []
			entry = WhoWasData()
			entry.username = username
			entry.host = host
			entry.realname = realname
			self.whowas[nick].append(entry)

	def irc_RPL_ENDOFWHOWAS(self, prefix, params):
		nick = params[1]

		if nick in self.whowas:
			replies = self.whowas[nick]
			del self.whowas[nick]
			self.gui.whowas(self,nick,replies)

	def irc_INVITE(self,prefix,params):
		p = prefix.split("!")
		if len(p)==2:
			nick = p[0]
			hostmask = p[1]
		else:
			nick = prefix
			hostmask = None

		target = params[0]
		channel = params[1]

		self.gui.invited(self,prefix,channel)
		
	def irc_RPL_INVITING(self,prefix,params):
		user = params[1]
		channel = params[2]

		self.gui.inviting(self,user,channel)

	def sendLine(self,line):

		return irc.IRCClient.sendLine(self, line)

	def irc_ERR_NOSUCHNICK(self,prefix,params):
		self.gui.receivedError(self,params[1]+": "+params[2])

	def irc_ERR_NOSUCHSERVER(self,prefix,params):
		self.gui.receivedError(self,params[1]+": "+params[2])

	def irc_ERR_NOSUCHCHANNEL(self,prefix,params):
		self.gui.receivedError(self,params[1]+": "+params[2])

	def irc_ERR_CANNOTSENDTOCHAN(self,prefix,params):
		self.gui.receivedError(self,params[1]+": "+params[2])

	def irc_RPL_AWAY(self,prefix,params):
		user = params[1]
		msg = params[2]

	def irc_RPL_UNAWAY(self,prefix,params):
		msg = params[1]

		self.is_away = False
		self.gui.rerenderUserlists()
		self.gui.back(self)

	def irc_RPL_NOWAWAY(self,prefix,params):

		msg = params[1]

		self.is_away = True
		self.gui.rerenderUserlists()
		self.gui.away(self,msg)

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

		#print(line2)

		if "Cannot join channel (+k)" in line2:
			self.gui.receivedError(self,"Cannot join channel (wrong or missing password)")
			pass
		if "Cannot join channel (+l)" in line2:
			self.gui.receivedError(self,"Cannot join channel (channel is full)")
			pass
		if "Cannot join channel (+b)" in line2:
			self.gui.receivedError(self,"Cannot join channel (banned)")
			pass
		if "Cannot join channel (+i)" in line2:
			self.gui.receivedError(self,"Cannot join channel (channel is invite only)")
			pass
		if "not an IRC operator" in line2:
			self.gui.receivedError(self,"Permission denied (you're not an IRC operator)")
			pass
		if "not channel operator" in line2:
			self.gui.receivedError(self,"Permission denied (you're not channel operator)")
			pass
		if "is already on channel" in line2:
			self.gui.receivedError(self,"Invite failed (user is already in channel)")
			pass
		if "not on that channel" in line2:
			self.gui.receivedError(self,"Permission denied (you're not in channel)")
			pass
		if "aren't on that channel" in line2:
			self.gui.receivedError(self,"Permission denied (target user is not in channel)")
			pass
		if "have not registered" in line2:
			self.gui.receivedError(self,"You're not registered")
			pass
		if "may not reregister" in line2:
			self.gui.receivedError(self,"You can't reregister")
			pass
		if "enough parameters" in line2:
			self.gui.receivedError(self,"Not enough parameters supplied to command")
			pass
		if "isn't among the privileged" in line2:
			self.gui.receivedError(self,"Registration refused (server isn't setup to allow connections from your host)")
			pass
		if "Password incorrect" in line2:
			self.gui.receivedError(self,"Permission denied (incorrect password)")
			pass
		if "banned from this server" in line2:
			self.gui.receivedError(self,"You are banned from this server")
			pass
		if "kill a server" in line2:
			self.gui.receivedError(self,"Permission denied (you can't kill a server)")
			pass
		if "O-lines for your host" in line2:
			self.gui.receivedError(self,"No O-lines for your host")
			pass
		if "Unknown MODE flag" in line2:
			self.gui.receivedError(self,"Unknown MODE flag")
			pass
		if "change mode for other users" in line2:
			self.gui.receivedError(self,"Permission denied (can't change mode for other users)")
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

		self.gui.serverMessage(self,' '.join(options))

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

		if hasattr(self,'network'):
			if self.network:

				user_history = list(user.HISTORY)

				newhistory = []
				change = False
				for s in user_history:
					if s[0]==self.server:
						if s[1]==str(self.port):
							if s[2]==UNKNOWN_NETWORK:
								s[2] = self.network
								change = True
					newhistory.append(s)

				if change:
					user.HISTORY = newhistory
					user.save_user(user.USER_FILE)


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

		if key=="client_id":
			obj.client_id = value

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

		if key=="execute_script":
			obj.execute_script = value

class IRC_Connection_Factory(protocol.ClientFactory):
	def __init__(self,**kwargs):
		self.kwargs = kwargs

	def buildProtocol(self, addr):
		bot = IRC_Connection(**self.kwargs)
		bot.factory = self
		return bot

	def clientConnectionLost(self, connector, reason):
		
		if self.kwargs["client_id"] in self.kwargs["gui"].quitting:
			del self.kwargs["gui"].quitting[self.kwargs["client_id"]]
			return

		if config.NOTIFY_ON_LOST_OR_FAILED_CONNECTION:
			msg = "Connection to "+self.kwargs["server"]+":"+str(self.kwargs["port"])+" lost."

			msgBox = QMessageBox()
			msgBox.setIconPixmap(QPixmap(DISCONNECT_DIALOG_IMAGE))
			msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
			msgBox.setText(msg)
			msgBox.setInformativeText(reason.getErrorMessage())
			msgBox.setWindowTitle("Connection lost")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()

	def clientConnectionFailed(self, connector, reason):
		
		if self.kwargs["client_id"] in self.kwargs["gui"].quitting:
			del self.kwargs["gui"].quitting[self.kwargs["client_id"]]
			return

		if config.PROMPT_ON_FAILED_CONNECTION:
			msg = "Connection to "+self.kwargs["server"]+":"+str(self.kwargs["port"])+" failed."
			self.kwargs["gui"].connectToIrcFail(msg,reason.getErrorMessage())
		else:
			if config.NOTIFY_ON_LOST_OR_FAILED_CONNECTION:
				msg = "Connection to "+self.kwargs["server"]+":"+str(self.kwargs["port"])+" failed."

				msgBox = QMessageBox()
				msgBox.setIconPixmap(QPixmap(DISCONNECT_DIALOG_IMAGE))
				msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
				msgBox.setText(msg)
				msgBox.setWindowTitle("Connection failed")
				msgBox.setStandardButtons(QMessageBox.Ok)
				msgBox.exec()

class IRC_ReConnection_Factory(protocol.ReconnectingClientFactory):
	def __init__(self,**kwargs):
		self.kwargs = kwargs

	def buildProtocol(self, addr):
		bot = IRC_Connection(**self.kwargs)
		bot.factory = self
		return bot

	def clientConnectionLost(self, connector, reason):

		if self.kwargs["client_id"] in self.kwargs["gui"].quitting:
			del self.kwargs["gui"].quitting[self.kwargs["client_id"]]
			if self.kwargs["client_id"] in self.kwargs["gui"].reconnecting:
				del self.kwargs["gui"].reconnecting[self.kwargs["client_id"]]
			return

		self.kwargs["gui"].reconnecting[self.kwargs["client_id"]] = 0

		if config.ASK_BEFORE_RECONNECT:
			msg = "Connection to "+self.kwargs["server"]+":"+str(self.kwargs["port"])+" lost.\nTry to reconnect?"

			msgBox = QMessageBox()
			msgBox.setIconPixmap(QPixmap(DISCONNECT_DIALOG_IMAGE))
			msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
			msgBox.setText(msg)
			msgBox.setInformativeText(reason.getErrorMessage())
			msgBox.setWindowTitle("Connection lost")
			msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

			rval = msgBox.exec()
			if rval == QMessageBox.Cancel:
				pass
			else:
				protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
		else:
			protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

	def clientConnectionFailed(self, connector, reason):

		if self.kwargs["client_id"] in self.kwargs["gui"].quitting:
			del self.kwargs["gui"].quitting[self.kwargs["client_id"]]
			if self.kwargs["client_id"] in self.kwargs["gui"].reconnecting:
				del self.kwargs["gui"].reconnecting[self.kwargs["client_id"]]
			return

		if self.kwargs["client_id"] in self.kwargs["gui"].reconnecting:
			protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
		else:
			if config.PROMPT_ON_FAILED_CONNECTION:
				msg = "Connection to "+self.kwargs["server"]+":"+str(self.kwargs["port"])+" failed."
				self.kwargs["gui"].connectToIrcFail(msg,reason.getErrorMessage())
			else:
				if config.NOTIFY_ON_LOST_OR_FAILED_CONNECTION:
					msg = "Connection to "+self.kwargs["server"]+":"+str(self.kwargs["port"])+" failed."

					msgBox = QMessageBox()
					msgBox.setIconPixmap(QPixmap(DISCONNECT_DIALOG_IMAGE))
					msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
					msgBox.setText(msg)
					msgBox.setWindowTitle("Connection failed")
					msgBox.setStandardButtons(QMessageBox.Ok)
					msgBox.exec()


