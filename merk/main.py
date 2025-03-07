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

import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

import emoji

from .resources import *
from . import config
from . import styles
from . import widgets
from . import render
from . import irc
from . import logs
from . import user
from .dialog import *
from . import commands

class Merk(QMainWindow):

	# ===========
	# Constructor
	# ===========

	# Arguments:
	# 	app (QApplication)
	#	configuration_location (string: config directory path, default: none)
	#	configuration_directory_name (string: config directory name, default: .merk)
	#	configuration_file (string: config filename, default: none)
	# 	parent (parent window, default: None)

	def __init__(
			self,
			app,
			configuration_location=None,
			configuration_directory_name=".merk",
			connection_info=None,
			application_font=None,
			no_commands=False,
			channels=[],
			parent=None,
		):
		super(Merk, self).__init__(parent)

		# Save any arguments passed to the class
		self.app = app
		self.parent = parent
		self.configuration_location = configuration_location
		self.configuration_directory_name = configuration_directory_name
		self.application_font = application_font
		self.no_commands = no_commands
		self.join_channels = channels

		# Set the application font
		self.app.setFont(self.application_font)

		# Set the widget font
		self.setFont(self.application_font)

		# Internal attributes
		self.quitting = {}
		self.hiding = {}
		self.scripts = {}
		self.reconnecting = {}

		# Create the central object of the client,
		# the MDI widget
		self.MDI = QMdiArea()
		self.setCentralWidget(self.MDI)
		self.MDI.subWindowActivated.connect(self.subWindowActivated)

		# Set the background image of the MDI widget
		if config.MDI_BACKGROUND_IMAGE!=None:
			backgroundPix = QPixmap(config.MDI_BACKGROUND_IMAGE)
		else:
			backgroundPix = QPixmap(MDI_BACKGROUND)
		backgroundBrush = QBrush(backgroundPix)
		self.MDI.setBackground(backgroundBrush)

		# Set the window title
		self.setWindowTitle(config.DISPLAY_NAME)
		self.setWindowIcon(QIcon(config.DISPLAY_ICON))

		# Menubar
		self.menubar = self.menuBar()

		self.buildMenu()

		if connection_info:
			self.connectToIrc(connection_info)

		if config.COMMANDLINE_NO_SCRIPT==False:
			# Add /script to autocomplete
			commands.AUTOCOMPLETE[config.ISSUE_COMMAND_SYMBOL+"script"] = config.ISSUE_COMMAND_SYMBOL+"script "

			# Add the /script command to the /help display
			entry = [ "<b>"+config.ISSUE_COMMAND_SYMBOL+"script [FILENAME]</b>", "Executes a list of commands in a file" ]
			commands.COMMAND_HELP_INFORMATION.append(entry)

			# Rebuild the command help, with the "/script" command added
			hdisplay = []
			for e in commands.COMMAND_HELP_INFORMATION:
				t = commands.HELP_ENTRY_TEMPLATE
				t = t.replace("%_USAGE_%",e[0])
				t = t.replace("%_DESCRIPTION_%",e[1])
				hdisplay.append(t)
			commands.help_display = commands.HELP_DISPLAY_TEMPLATE.replace("%_LIST_%","\n".join(hdisplay))

			commands.help_display = commands.help_display.replace("%_SCRIPTING_%", "")

			commands.HELP = Message(RAW_SYSTEM_MESSAGE,'',commands.help_display)
		else:
			commands.help_display = commands.help_display.replace("%_SCRIPTING_%", "Scripting is turned off.")
			commands.HELP = Message(RAW_SYSTEM_MESSAGE,'',commands.help_display)


	# |==================|
	# | BEGIN IRC EVENTS |
	# |==================|

	def connectionMade(self,client):
		w = self.newServerWindow(client.server+":"+str(client.port),client)
		c = w.widget()
		t = Message(SYSTEM_MESSAGE,'',"Connected to "+client.server+":"+str(client.port)+"!")
		c.writeText(t)

		self.buildMainMenu()

	def connectionLost(self,client):
		
		windows = self.getAllSubWindows(client)
		for w in windows:
			w.close()

		# Forcibly remove server window
		w = self.getServerSubWindow(client)
		self.MDI.removeSubWindow(w)
		self.buildWindowsMenu()

		self.buildMainMenu()

	def signedOn(self,client):

		w = self.getServerWindow(client)
		if w:
			t = Message(SYSTEM_MESSAGE,'',"Registered with server!")
			w.writeText(t)

			if client.hostname:
				w.name = client.hostname
				w.updateTitle()

			w.nick_button.setEnabled(True)
			w.join_button.setEnabled(True)
			w.info_button.setEnabled(True)

			self.buildWindowsMenu()
		
		self.nickChanged(client)

		if not self.no_commands:
			w = self.getServerWindow(client)
			if w:
				hostid = client.server+":"+str(client.port)
				if config.COMMANDLINE_NO_SCRIPT==False:
					if hostid in user.COMMANDS:
						commands.executeScript(self,w,user.COMMANDS[hostid])

		if len(self.join_channels)>0:
			for e in self.join_channels:
				client.join(e[0],e[1])
			self.join_channels = []

	def receivedMOTD(self,client,motd):

		m = "<br>".join(motd)
		w = self.getServerWindow(client)
		if w:
			t = Message(SERVER_MESSAGE,'',m)
			w.writeText(t)

		w = self.getServerWindow(client)
		if w:
			w.refreshInfoMenu()

	def serverMessage(self,client,msg):
		w = self.getServerWindow(client)
		if w:
			t = Message(SERVER_MESSAGE,'',msg)
			w.writeText(t)

	def joined(self,client,channel):
		
		# Create a new channel window
		w = self.newChannelWindow(channel,client)
		if w:
			c = w.widget()
			t = Message(SYSTEM_MESSAGE,'',"Joined "+channel)
			c.writeText(t)

		w = self.getServerWindow(client)
		if w:
			t = Message(SYSTEM_MESSAGE,'',"You joined "+channel)
			w.writeText(t)

	def left(self,client,channel):

		w = self.getSubWindow(channel,client)
		if w:
			c = w.widget()
			if hasattr(c,"saveLogs"): c.saveLogs()
			self.MDI.removeSubWindow(w)
			self.buildWindowsMenu()

		w = self.getServerWindow(client)
		if w:
			t = Message(SYSTEM_MESSAGE,'',"You left "+channel)
			w.writeText(t)
		

	def privmsg(self,client,user,target,msg):

		p = user.split("!")
		if len(p)==2:
			nickname = p[0]
			hostmask = p[1]
		else:
			nickname = user
			hostmask = None

		if target[:1]=='#' or target[:1]=='&' or target[:1]=='!' or target[:1]=='+':
			# Channel message
			w = self.getWindow(target,client)
			if w:
				t = Message(CHAT_MESSAGE,user,msg)
				w.writeText(t)
				return

		if target==client.nickname:
			displayed_private_message = False

			# It's a private message, so try to write the message
			# to the private message window, if there is one
			w = self.getWindow(nickname,client)
			if w:
				t = Message(CHAT_MESSAGE,user,msg)
				w.writeText(t)
				displayed_private_message = True

			if config.WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW:
				# Write the private message to the server window
				w = self.getServerWindow(client)
				if w:
					t = Message(CHAT_MESSAGE,user,msg)
					w.writeText(t)

			if displayed_private_message: return

			if config.CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES:
				# Create a new private message window and write
				# the message to it
				w = self.newPrivateWindow(nickname,client)
				if w:
					c = w.widget()
					t = Message(CHAT_MESSAGE,user,msg)
					c.writeText(t)
					self.MDI.setActiveSubWindow(w)
					return

			# Client has received a private message, and will
			# NOT see it, so write it to the current window
			w = self.MDI.activeSubWindow()
			if w:
				c = w.widget()
				t = Message(PRIVATE_MESSAGE,user,msg)
				c.writeText(t)

	def action(self,client,user,target,msg):

		p = user.split("!")
		if len(p)==2:
			nickname = p[0]
			hostmask = p[1]
		else:
			nickname = user
			hostmask = None

		# Channel message
		if target[:1]=='#' or target[:1]=='&' or target[:1]=='!' or target[:1]=='+':
			w = self.getWindow(target,client)
			if w:
				t = Message(ACTION_MESSAGE,nickname,msg)
				w.writeText(t)
				return

		# Try to display it as a private message
		w = self.getWindow(nickname,client)
		if w:
			t = Message(ACTION_MESSAGE,nickname,msg)
			w.writeText(t)
		else:
			if config.CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES:
				# Create a new private message window and write
				# the message to it
				w = self.newPrivateWindow(nickname,client)
				if w:
					c = w.widget()
					t = Message(ACTION_MESSAGE,nickname,msg)
					c.writeText(t)
					return

	def noticed(self,client,user,target,msg):

		p = user.split("!")
		if len(p)==2:
			nickname = p[0]
			hostmask = p[1]
		else:
			nickname = user
			hostmask = None

		# Server notices get written to the server window only
		if target=='*':
			w = self.getServerWindow(client)
			if w:
				t = Message(NOTICE_MESSAGE,'',msg)
				w.writeText(t)
			return

		p = user.split("!")
		if len(p)==2:
			nickname = p[0]
			hostmask = p[1]
		else:
			nickname = user
			hostmask = None

		# Try and send the message to the right window
		w = self.getWindow(nickname,client)
		if w:
			t = Message(NOTICE_MESSAGE,nickname,msg)
			w.writeText(t)
		else:
			# Write the notice to the current window
			current = self.MDI.activeSubWindow()
			if w:
				c = current.widget()
				t = Message(PRIVATE_MESSAGE,user,msg)
				c.writeText(t)

			# Write the notice to the server window
			w = self.getServerWindow(client)
			if w:
				# If the current window is the server
				# window, then don't write the message
				# twice
				if w is current: return
				t = Message(NOTICE_MESSAGE,nickname,msg)
				w.writeText(t)

	def names(self,client,channel,users):
		w = self.getWindow(channel,client)
		if w:
			w.writeUserlist(users)

	def nickChanged(self,client):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				if c.client.client_id == client.client_id:
					c.refreshNickDisplay()
				if c.window_type==CHANNEL_WINDOW:
					c.client.sendLine("NAMES "+c.name)

		# Write a notification to the current window
		write_to_server_window = True
		wid = None
		w = self.MDI.activeSubWindow()
		if w:
			c = w.widget()
			t = Message(SYSTEM_MESSAGE,"","You are now known as \""+client.nickname+"\"")
			c.writeText(t)
			wid = c.subwindow_id

		# Write a notification to the server window,
		# but *only* if the current window is *not*
		# the server window
		w = self.getServerWindow(client)
		if wid:
			if w:
				if wid==w.subwindow_id: write_to_server_window = False

		if write_to_server_window:
			if w:
				t = Message(SYSTEM_MESSAGE,"","You are now known as \""+client.nickname+"\"")
				w.writeText(t)

	def topicChanged(self,client,user,channel,newTopic):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				if c.client.client_id == client.client_id:
					if c.window_type==CHANNEL_WINDOW:
						if c.name==channel:
							c.setTopic(newTopic)

							if user!='':
								t = Message(SYSTEM_MESSAGE,"",user+" has changed the topic to \""+newTopic+"\"")
								c.writeText(t)

	def userJoined(self,client,user,channel):
		w = self.getWindow(channel,client)
		if w:
			t = Message(SYSTEM_MESSAGE,'',user+" joined "+channel)
			w.writeText(t)
			return

	def userLeft(self,client,user,channel):
		w = self.getWindow(channel,client)
		if w:
			t = Message(SYSTEM_MESSAGE,'',user+" left "+channel)
			w.writeText(t)
			return

	def userRenamed(self,client,oldname,newname):
		windows = self.getAllSubWindows(client)

		for subwindow in windows:
			c = subwindow.widget()
			if hasattr(c,"client"):
				if c.window_type==CHANNEL_WINDOW:
					if oldname in c.nicks:
						# Changer is present, get the new user list
						c.client.sendLine("NAMES "+c.name)
						# Now notify the client
						t = Message(SYSTEM_MESSAGE,"",oldname+" is now known as "+newname)
						c.writeText(t)
				# If we're chatting with the changer, then
				# change the settings of the chat window
				# to relect the new nick
				if c.window_type==PRIVATE_WINDOW:
					if c.name==oldname:
						c.name=newname
						c.updateTitle()
						# Notify the client of the change
						t = Message(SYSTEM_MESSAGE,"",oldname+" is now known as "+newname)
						c.writeText(t)

	def irc_QUIT(self,client,nickname,msg):
		windows = self.getAllSubWindows(client)

		for subwindow in windows:
			c = subwindow.widget()
			if hasattr(c,"client"):
				if c.window_type==CHANNEL_WINDOW:
					if nickname in c.nicks:
						c.client.sendLine("NAMES "+c.name)
						# Now notify the client
						if msg!='':
							t = Message(SYSTEM_MESSAGE,"",nickname+" has quit IRC ("+msg+")")
						else:
							t = Message(SYSTEM_MESSAGE,"",nickname+" has quit IRC")
						c.writeText(t)
				if c.window_type==PRIVATE_WINDOW:
					if c.name==nickname:
						if msg!='':
							t = Message(SYSTEM_MESSAGE,"",nickname+" has quit IRC ("+msg+")")
						else:
							t = Message(SYSTEM_MESSAGE,"",nickname+" has quit IRC")
						c.writeText(t)

	def serverSetMode(self,client,target,mode,argument):
		self.refreshModeDisplay(client)

		if len(mode.strip())==0: return

		if argument:
			c = []
			for e in argument:
				if e: c.append(e)
			argument = c
		else:
			argument = []

		t = Message(SYSTEM_MESSAGE,'',"Server set mode +"+mode+" "+' '.join(argument))

		if mode=="k":
			t = Message(SYSTEM_MESSAGE,'',"Server set mode +"+mode+" "+''.join(argument))

		w = self.getWindow(target,client)
		if w: w.writeText(t)

		t = Message(SYSTEM_MESSAGE,'',"Server set mode +"+mode+" "+' '.join(argument)+" on "+target)

		if mode=="k":
			t = Message(SYSTEM_MESSAGE,'',"Server set mode +"+mode+" "+''.join(argument)+" on "+target)

		w = self.getServerWindow(client)
		if w: w.writeText(t)

	def serverUnsetMode(self,client,target,mode):
		self.refreshModeDisplay(client)

		if len(mode.strip())==0: return

		t = Message(SYSTEM_MESSAGE,'',"Server set mode -"+mode)

		w = self.getWindow(target,client)
		if w: w.writeText(t)

		t = Message(SYSTEM_MESSAGE,'',"Server set mode -"+mode+" on "+target)

		w = self.getServerWindow(client)
		if w: w.writeText(t)

	def setMode(self,client,user,target,mode,argument):
		self.refreshModeDisplay(client)

		if len(mode.strip())==0: return

		if argument:
			c = []
			for e in argument:
				if e: c.append(e)
			argument = c
		else:
			argument = []

		t = Message(SYSTEM_MESSAGE,'',user+" set mode +"+mode+" "+' '.join(argument))

		if mode=='k':
			t = Message(SYSTEM_MESSAGE,'',user+" set mode +"+mode+" "+''.join(argument))

		w = self.getWindow(target,client)
		if w: w.writeText(t)

		t = Message(SYSTEM_MESSAGE,'',user+" set mode +"+mode+" "+' '.join(argument)+" on "+target)

		if mode=='k':
			t = Message(SYSTEM_MESSAGE,'',user+" set mode +"+mode+" "+''.join(argument)+" on "+target)

		w = self.getServerWindow(client)
		if w: w.writeText(t)

	def unsetMode(self,client,user,target,mode,argument):
		self.refreshModeDisplay(client)

		if len(mode.strip())==0: return

		t = Message(SYSTEM_MESSAGE,'',user+" set mode -"+mode+" "+' '.join(argument))

		if mode=="k":
			t = Message(SYSTEM_MESSAGE,'',user+" set mode -"+mode+" "+''.join(argument))

		w = self.getWindow(target,client)
		if w: w.writeText(t)

		t = Message(SYSTEM_MESSAGE,'',user+" set mode -"+mode+" "+' '.join(argument)+" on "+target)

		if mode=="k":
			t = Message(SYSTEM_MESSAGE,'',user+" set mode -"+mode+" "+''.join(argument)+" on "+target)

		w = self.getServerWindow(client)
		if w: w.writeText(t)

	def userKicked(self,client,kickee,channel,kicker,message):
		
		if len(message)>0:
			t = Message(SYSTEM_MESSAGE,'',kicker+" kicked "+kickee+" from "+channel+" ("+message+")")
		else:
			t = Message(SYSTEM_MESSAGE,'',kicker+" kicked "+kickee+" from "+channel)

		w = self.getWindow(channel,client)
		if w: w.writeText(t)

		w = self.getServerWindow(client)
		if w: w.writeText(t)

	def kickedFrom(self,client,channel,kicker,message):
		
		w = self.getSubWindow(channel,client)
		if w:
			self.MDI.removeSubWindow(w)
			self.buildWindowsMenu()

		w = self.getServerWindow(client)
		if w:
			if len(message)>0:
				t = Message(SYSTEM_MESSAGE,'',kicker+" kicked you from "+channel+" ("+message+")")
			else:
				t = Message(SYSTEM_MESSAGE,'',kicker+" kicked you from "+channel)
			w.writeText(t)

	def receivedError(self,client,message):

		t = Message(ERROR_MESSAGE,'',message)

		w = self.getServerWindow(client)
		if w: w.writeText(t)

		a = self.MDI.activeSubWindow()
		c = a.widget()

		if hasattr(c,"subwindow_id"):
			if c.subwindow_id==w.subwindow_id:
				return

			c.writeText(t)

	def uptime(self,client,uptime):

		# getAllSubWindows(self,client):
		for w in self.getAllSubWindows(client):
			c = w.widget()
			c.tickUptime(uptime)

	def whois(self,client,whoisdata):

		displaynick = "["+whoisdata.nickname+"]"

		wd = [
			Message(WHOIS_MESSAGE,displaynick, whoisdata.username+"@"+whoisdata.host+": \x02"+whoisdata.realname+"\x0F"),
			Message(WHOIS_MESSAGE,displaynick, "\x02"+whoisdata.server+"\x0F"),
			Message(WHOIS_MESSAGE,displaynick, "\x02"+whoisdata.channels+"\x0F"),
			Message(WHOIS_MESSAGE,displaynick, "\x02Signed on:\x0F "+datetime.fromtimestamp(int(whoisdata.signon)).strftime('%m/%d/%Y, %H:%M:%S')),
			Message(WHOIS_MESSAGE,displaynick, "\x02Idle:\x0F "+whoisdata.idle+" seconds"),
			Message(WHOIS_MESSAGE,displaynick, "\x02"+whoisdata.privs+"\x0F"),
		]

		w = self.MDI.activeSubWindow()
		if w:
			c = w.widget()
			for msg in wd:
				c.writeText(msg,False)

	def who(self,client,nick,whodata):

		w = self.MDI.activeSubWindow()
		if w:
			c = w.widget()
			for entry in whodata:
				t = Message(WHOIS_MESSAGE,nick, entry.username+"@"+entry.host+": \x02"+entry.channel+"\x0F ("+entry.server+")")
				c.writeText(t,False)

	def whowas(self,client,nick,whodata):

		w = self.MDI.activeSubWindow()
		if w:
			c = w.widget()
			for entry in whodata:
				t = Message(WHOIS_MESSAGE,nick, entry.username+"@"+entry.host+": \x02"+entry.realname+"\x0F")
				c.writeText(t,False)

	def invited(self,client,user,channel):

		w = self.MDI.activeSubWindow()
		if w:
			c = w.widget()
			t = Message(SYSTEM_MESSAGE,'', user+" invited you to "+channel)
			c.writeText(t)

		w = self.getServerWindow(client)
		if w:
			t = Message(SYSTEM_MESSAGE,'', user+" invited you to "+channel)
			w.writeText(t)

	def inviting(self,client,user,channel):
		w = self.MDI.activeSubWindow()
		if w:
			c = w.widget()
			t = Message(SYSTEM_MESSAGE,'', "You invited "+user+" to "+channel)
			c.writeText(t)

		w = self.getServerWindow(client)
		if w:
			t = Message(SYSTEM_MESSAGE,'', "You invited "+user+" to "+channel)
			w.writeText(t)


	# |================|
	# | END IRC EVENTS |
	# |================|

	def connectToIrcFail(self,message,reason):
		connection = ConnectDialogNoLogo(self.app,self,message,reason,self.no_commands)

		if connection:
			
			if connection.reconnect:
				if connection.ssl:
					irc.reconnectSSL(
						nickname=connection.nickname,
						server=connection.host,
						port=connection.port,
						alternate=connection.alternate,
						password=connection.password,
						username=connection.username,
						realname=connection.realname,
						ssl=connection.ssl,
						gui=self,
						failreconnect=True,
					)
				else:
					irc.reconnect(
						nickname=connection.nickname,
						server=connection.host,
						port=connection.port,
						alternate=connection.alternate,
						password=connection.password,
						username=connection.username,
						realname=connection.realname,
						ssl=connection.ssl,
						gui=self,
						failreconnect=True,
					)
			else:
				if connection.ssl:
					irc.connectSSL(
						nickname=connection.nickname,
						server=connection.host,
						port=connection.port,
						alternate=connection.alternate,
						password=connection.password,
						username=connection.username,
						realname=connection.realname,
						ssl=connection.ssl,
						gui=self,
						failreconnect=True,
					)
				else:
					irc.connect(
						nickname=connection.nickname,
						server=connection.host,
						port=connection.port,
						alternate=connection.alternate,
						password=connection.password,
						username=connection.username,
						realname=connection.realname,
						ssl=connection.ssl,
						gui=self,
						failreconnect=True,
					)

	def connectToIrc(self,connection_info=None):
		if connection_info:
			connection = connection_info
		else:
			connection = ConnectDialogNoLogo(self.app,self,'','',self.no_commands)
		if connection:
			
			if connection.reconnect:
				if connection.ssl:
					irc.reconnectSSL(
						nickname=connection.nickname,
						server=connection.host,
						port=connection.port,
						alternate=connection.alternate,
						password=connection.password,
						username=connection.username,
						realname=connection.realname,
						ssl=connection.ssl,
						gui=self,
						failreconnect=True,
					)
				else:
					irc.reconnect(
						nickname=connection.nickname,
						server=connection.host,
						port=connection.port,
						alternate=connection.alternate,
						password=connection.password,
						username=connection.username,
						realname=connection.realname,
						ssl=connection.ssl,
						gui=self,
						failreconnect=True,
					)
			else:
				if connection.ssl:
					irc.connectSSL(
						nickname=connection.nickname,
						server=connection.host,
						port=connection.port,
						alternate=connection.alternate,
						password=connection.password,
						username=connection.username,
						realname=connection.realname,
						ssl=connection.ssl,
						gui=self,
						failreconnect=True,
					)
				else:
					irc.connect(
						nickname=connection.nickname,
						server=connection.host,
						port=connection.port,
						alternate=connection.alternate,
						password=connection.password,
						username=connection.username,
						realname=connection.realname,
						ssl=connection.ssl,
						gui=self,
						failreconnect=True,
					)

	def refreshModeDisplay(self,client):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				if c.client.client_id == client.client_id:
					c.refreshModeDisplay()

	def setAllFont(self,newfont):
		for window in self.MDI.subWindowList():
			c = window.widget()
			c.setFont(newfont)
			if hasattr(c,"chat"): c.chat.setFont(newfont)
			if hasattr(c,"userlist"): c.userlist.setFont(newfont)
			if hasattr(c,"input"): c.input.setFont(newfont)
			if hasattr(c,"topic"): c.topic.setFont(newfont)
			if hasattr(c,"channelUptime"): c.channelUptime.setFont(newfont)
			if hasattr(c,"nick_display"): c.nick_display.setFont(newfont)
			if hasattr(c,"mode_display"): c.mode_display.setFont(newfont)
			if hasattr(c,"spellcheckMenu"): c.spellcheckMenu.setFont(newfont)
			if hasattr(c,"status"): c.status.setFont(newfont)
			if hasattr(c,"status_server"): c.status_server.setFont(newfont)
			if hasattr(c,"key_value"): c.key_value.setFont(newfont)

	def rerenderUserlists(self):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"userlist"):
				c.rerenderUserlist()

	def toggleNickDisplay(self):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"nick_display"):
				c.toggleNickDisplay()

	def setAllLanguage(self,newlang):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"menuSetLanguage"):
				c.menuSetLanguage(newlang)

	def reRenderAll(self):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"rerenderChatLog"):
				c.rerenderChatLog()

	def reApplyStyle(self):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"applyStyle"):
				c.applyStyle()

	def handleUserInput(self,window,user_input):

		# Handle chat commands
		if commands.handleChatCommands(self,window,user_input,False): return

		# Handle common commands
		if commands.handleCommonCommands(self,window,user_input,False): return
		
		# Add emojis to the message
		if config.ENABLE_EMOJI_SHORTCODES:
			user_input = emoji.emojize(user_input,language='alias')

		if len(user_input)>0:
			# Client has sent a chat message, so send the message
			window.client.msg(window.name,user_input)
			# ...and then display it to the user
			t = Message(SELF_MESSAGE,window.client.nickname,user_input)
			window.writeText(t)

	
	def handleConsoleInput(self,window,user_input):
		
		# Handle common commands
		if commands.handleCommonCommands(self,window,user_input,False): return

		t = Message(ERROR_MESSAGE,'',"Unrecognized command: "+user_input)
		window.writeText(t)

	def closeAndRemoveAllWindows(self):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"saveLogs"): c.saveLogs()
			if hasattr(c,"client"):
				c.client.quit(config.DEFAULT_QUIT_MESSAGE)
			if window:
				self.MDI.removeSubWindow(window)

	def openPrivate(self,client,nick):

		# Find and raise the private chat window
		# if it already exists
		w = self.getSubWindow(nick,client)
		if w:
			self.showSubWindow(w)
			return

		# Create a new private chat window
		w = self.newPrivateWindow(nick,client)
		self.showSubWindow(w)

	def getWindow(self,channel,client):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"name"):
				if c.name.lower() == channel.lower():
					if hasattr(c,"client"):
						if c.client.client_id == client.client_id:
							return c
		return None

	def getServerWindow(self,client):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if c.window_type==SERVER_WINDOW:
					if hasattr(c,"client"):
						if c.client.client_id == client.client_id:
							return c
		return None

	def hideServerWindow(self,client):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if c.window_type==SERVER_WINDOW:
					if hasattr(c,"client"):
						if c.client.client_id == client.client_id:
							window.hide()
							self.hiding[client.client_id] = client
							self.buildWindowsMenu()

	def getSubWindow(self,channel,client):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"name"):
				if c.name.lower() == channel.lower():
					if hasattr(c,"client"):
						if c.client.client_id == client.client_id:
							return window
		return None

	def getServerSubWindow(self,client):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if c.window_type==SERVER_WINDOW:
					if hasattr(c,"client"):
						if c.client.client_id == client.client_id:
							return window
		return None

	def getAllServerWindows(self):
		retval = []
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if c.window_type==SERVER_WINDOW:
					retval.append(window)
		return retval

	def getAllSubWindows(self,client):
		retval = []
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				if c.client.client_id == client.client_id:
					retval.append(window)
		return retval

	def getAllSubChatWindows(self,client):
		retval = []
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				if c.client.client_id == client.client_id:
					if c.window_type==CHANNEL_WINDOW:
						retval.append(window)
					elif c.window_type==PRIVATE_WINDOW:
						retval.append(window)
		return retval

	def getAllChatNames(self):
		retval = []
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				retval.append(window.widget().name)
		return retval

	def getAllSubChannelWindows(self,client):
		retval = []
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				if c.client.client_id == client.client_id:
					if c.window_type==CHANNEL_WINDOW:
						retval.append(window)
		return retval

	def getAllSubPrivateWindows(self,client):
		retval = []
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				if c.client.client_id == client.client_id:
					if c.window_type==PRIVATE_WINDOW:
						retval.append(window)
		return retval

	def showSubWindow(self,window):
		window.showNormal()
		self.MDI.setActiveSubWindow(window)

	def hideSubWindow(self,subwindow_id):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"subwindow_id"):
				if c.subwindow_id==subwindow_id:
					window.hide()

	def closeSubWindow(self,subwindow_id):
		# Step through the list of MDI windows
		# and remove the subwindow associated with this ID
		for window in self.MDI.subWindowList():

			# Get the chat window instance associated
			# with the current subwindow
			c = window.widget()

			# Check to see if the subwindow_id passed
			# to this function is the one we're looking
			# to remove
			if hasattr(c,"subwindow_id"):
				if c.subwindow_id==subwindow_id:
					# Pass the *SUBWINDOW* widget to actually
					# delete it from the MDI area
					self.MDI.removeSubWindow(window)
					self.buildWindowsMenu()

	def newChannelWindow(self,name,client):
		w = QMdiSubWindow(self)
		w.setWidget(widgets.Window(name,client,CHANNEL_WINDOW,self.app,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		w.setWindowIcon(QIcon(CHANNEL_WINDOW_ICON))
		self.MDI.addSubWindow(w)
		w.show()
		self.buildWindowsMenu()

		return w

	def newServerWindow(self,name,client):
		w = QMdiSubWindow(self)
		w.setWidget(widgets.Window(name,client,SERVER_WINDOW,self.app,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		self.MDI.addSubWindow(w)
		w.show()
		self.buildWindowsMenu()

		return w

	def newPrivateWindow(self,name,client):
		w = QMdiSubWindow(self)
		w.setWidget(widgets.Window(name,client,PRIVATE_WINDOW,self.app,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		w.setWindowIcon(QIcon(PRIVATE_WINDOW_ICON))
		self.MDI.addSubWindow(w)
		w.show()
		self.buildWindowsMenu()

		return w

	def openLinkInBrowser(self,url):
		u = QUrl()
		u.setUrl(url)
		QDesktopServices.openUrl(u)


	# |--------------|
	# | MENU METHODS |
	# |--------------|

	def buildMenu(self):
		self.menubar.clear()

		# Main menu
		self.mainMenu = self.menubar.addMenu("IRC")

		self.buildMainMenu()

		# Tools menu
		self.settingsMenu = self.menubar.addMenu("Settings")

		entry = widgets.ExtendedMenuItem(self,SETTINGS_ICON,'Settings','Edit settings',25,self.openSettings)
		self.settingsMenu.addAction(entry)

		entry = widgets.ExtendedMenuItem(self,STYLE_ICON,'Style','Edit default text style&nbsp;&nbsp;',25,self.menuEditStyle)
		self.settingsMenu.addAction(entry)

		entry = widgets.ExtendedMenuItem(self,LOG_ICON,'Export','Export logs to text or JSON&nbsp;&nbsp;',25,self.menuExportLog)
		self.settingsMenu.addAction(entry)

		self.settingsMenu.addSeparator()

		sm = self.settingsMenu.addMenu(QIcon(FOLDER_ICON),"Application folders")

		entry = QAction(QIcon(SETTINGS_ICON),"Settings directory",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+config.CONFIG_DIRECTORY))))
		sm.addAction(entry)

		entry = QAction(QIcon(STYLE_ICON),"Styles directory",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+styles.STYLE_DIRECTORY))))
		sm.addAction(entry)

		entry = QAction(QIcon(LOG_ICON),"Logs directory",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+logs.LOG_DIRECTORY))))
		sm.addAction(entry)

		if config.COMMANDLINE_NO_SCRIPT==False:
			entry = QAction(QIcon(SCRIPT_ICON),"Scripts directory",self)
			entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+commands.SCRIPTS_DIRECTORY))))
			sm.addAction(entry)

		# Windows menu
		self.windowsMenu = self.menubar.addMenu("Windows")

		self.buildWindowsMenu()

		# Help menu
		self.helpMenu = self.menubar.addMenu("Help")

		entry = widgets.ExtendedMenuItem(self,ABOUT_ICON,'About',APPLICATION_NAME+" "+APPLICATION_VERSION,25,self.showAbout)
		self.helpMenu.addAction(entry)

		self.helpMenu.addSeparator()

		entry = QAction(QIcon(LINK_ICON),"Supported emoji shortcodes",self)
		entry.triggered.connect(lambda state,u="https://carpedm20.github.io/emoji/all.html?enableList=enable_list_alias": self.openLinkInBrowser(u))
		self.helpMenu.addAction(entry)

		entry = QAction(QIcon(LINK_ICON),"Source code repository",self)
		entry.triggered.connect(lambda state,u=APPLICATION_SOURCE: self.openLinkInBrowser(u))
		self.helpMenu.addAction(entry)

		entry = QAction(QIcon(LINK_ICON),"GPLv3 License",self)
		entry.triggered.connect(lambda state,u="https://www.gnu.org/licenses/gpl-3.0.en.html": self.openLinkInBrowser(u))
		self.helpMenu.addAction(entry)

	def menuEditStyle(self):
		x = StylerDefaultDialog(self)

	def disconnectAll(self):
		windows = self.getAllServerWindows()
		if len(windows)>0:

			dc = []
			for w in windows:
				c = w.widget()
				dc.append(c.client)

			if self.askDisconnectMulti(dc):
				for w in windows:
					c = w.widget()

					no_hostname = False
					if not hasattr(c.client,"hostname"): no_hostname = True
					if not c.client.hostname: no_hostname = True

					if no_hostname:
						self.quitting[c.client.client_id] = 0
						c.client.quit()
						self.hideServerWindow(c.client)
					else:
						self.quitting[c.client.client_id] = 0
						c.client.quit(config.DEFAULT_QUIT_MESSAGE)


	def buildMainMenu(self):
		self.mainMenu.clear()

		entry = widgets.ExtendedMenuItem(self,CONNECT_ICON,'Connect','Connect to a server',25,self.connectToIrc)
		self.mainMenu.addAction(entry)

		windows = self.getAllServerWindows()

		# Make sure that clients that are still connected
		# but in the process of disconnecting don't cause
		# the "disconnect" menu entry to appear
		clean = []
		for w in windows:
			c = w.widget()
			if c.client.client_id in self.quitting: continue
			clean.append(w)
		windows = clean

		if len(windows)>0:
			if len(windows)==1:
				title = "Disconnect"
				desc = 'Disconnect from server'
			else:
				title = "Disconnect all"
				desc = 'Disconnect from '+str(len(windows))+' servers'
			entry = widgets.ExtendedMenuItem(self,DISCONNECT_ICON,title,desc,25,self.disconnectAll)
			self.mainMenu.addAction(entry)

		self.mainMenu.addSeparator()

		entry = QAction(QIcon(QUIT_ICON),"Quit",self)
		entry.setShortcut('Ctrl+Q')
		entry.triggered.connect(self.close)
		self.mainMenu.addAction(entry)

	def askDisconnect(self,client):

		no_hostname = False
		if not hasattr(client,"hostname"): no_hostname = True
		if not client.hostname: no_hostname = True

		do_disconnect = True

		if config.ASK_BEFORE_DISCONNECT:
			msgBox = QMessageBox()
			msgBox.setIconPixmap(QPixmap(DISCONNECT_DIALOG_IMAGE))
			msgBox.setWindowIcon(QIcon(config.DISPLAY_ICON))
			if no_hostname:
				msgBox.setText("Are you sure you want to disconnect from "+client.server+":"+str(client.port)+"?")
			else:
				msgBox.setText("Are you sure you want to disconnect from "+client.hostname+"?")
			msgBox.setWindowTitle("Disconnect")
			msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

			rval = msgBox.exec()
			if rval == QMessageBox.Cancel:
				do_disconnect = False

		return do_disconnect

	def askDisconnectMulti(self,list_of_client):

		if len(list_of_client)>1:
			conns = []
			for client in list_of_client:
				no_hostname = False
				if not hasattr(client,"hostname"): no_hostname = True
				if not client.hostname: no_hostname = True

				if no_hostname:
					conns.append(client.server+":"+str(client.port))
				else:
					conns.append(client.hostname)

			last = conns.pop()
			cstr = ", ".join(conns)+" and "+last
		else:
			c = list_of_client.pop(0)
			no_hostname = False
			if not hasattr(c,"hostname"): no_hostname = True
			if not c.hostname: no_hostname = True

			if no_hostname:
				cstr = c.server+":"+str(c.port)
			else:
				cstr = c.hostname

		do_disconnect = True

		if config.ASK_BEFORE_DISCONNECT:
			msgBox = QMessageBox()
			msgBox.setIconPixmap(QPixmap(DISCONNECT_DIALOG_IMAGE))
			msgBox.setWindowIcon(QIcon(config.DISPLAY_ICON))
			msgBox.setText("Are you sure you want to disconnect from "+cstr+"?")
			msgBox.setWindowTitle("Disconnect")
			msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

			rval = msgBox.exec()
			if rval == QMessageBox.Cancel:
				do_disconnect = False

		return do_disconnect

	def openSettings(self):
		self.settingsDialog = SettingsDialog(self.app,self)

	def showAbout(self):
		self.__about_dialog = AboutDialog()
		self.__about_dialog.show()

	def menuExportLog(self):
		d = ExportLogDialog(logs.LOG_DIRECTORY,None)
		if d:
			elog = d[0]
			dlog = d[1]
			llog = d[2]
			do_json = d[3]
			do_epoch = d[4]
			if not do_json:
				options = QFileDialog.Options()
				options |= QFileDialog.DontUseNativeDialog
				fileName, _ = QFileDialog.getSaveFileName(self,"Save export As...",INSTALL_DIRECTORY,"Text File (*.txt);;All Files (*)", options=options)
				if fileName:
					# extension = os.path.splitext(fileName)[1]
					# if extension.lower()!='txt': fileName = fileName + ".txt"
					efl = len("txt")+1
					if fileName[-efl:].lower()!=f".txt": fileName = fileName+f".txt"
					dump = logs.dumpLog(elog,dlog,llog,do_epoch)
					code = open(fileName,mode="w",encoding="utf-8")
					code.write(dump)
					code.close()
			else:
				options = QFileDialog.Options()
				options |= QFileDialog.DontUseNativeDialog
				fileName, _ = QFileDialog.getSaveFileName(self,"Save export As...",INSTALL_DIRECTORY,"JSON File (*.json);;All Files (*)", options=options)
				if fileName:
					# extension = os.path.splitext(fileName)[1]
					# if extension.lower()!='json': fileName = fileName + ".json"
					efl = len("json")+1
					if fileName[-efl:].lower()!=f".json": fileName = fileName+f".json"
					dump = logs.dumpLogJson(elog,do_epoch)
					code = open(fileName,mode="w",encoding="utf-8")
					code.write(dump)
					code.close()

	def buildWindowsMenu(self):

		self.windowsMenu.clear()

		entry1 = QAction(QIcon(CASCADE_ICON),"Cascade windows",self)
		entry1.triggered.connect(self.MDI.cascadeSubWindows)
		self.windowsMenu.addAction(entry1)

		entry2 = QAction(QIcon(TILE_ICON),"Tile windows",self)
		entry2.triggered.connect(self.MDI.tileSubWindows)
		self.windowsMenu.addAction(entry2)

		self.windowsMenu.addSeparator()

		listOfConnections = {}
		for i in irc.CONNECTIONS:
			add_to_list = True
			for j in self.hiding:
				if self.hiding[j] is irc.CONNECTIONS[i]: add_to_list = False
			if add_to_list: listOfConnections[i] = irc.CONNECTIONS[i]

		if len(listOfConnections)==0:
			entry1.setEnabled(False)
			entry2.setEnabled(False)

			# Reset application title, due to there being
			# no connections
			self.subWindowActivated(None)

		if len(listOfConnections)>0:

			for i in listOfConnections:
				entry = listOfConnections[i]
				if entry.hostname:
					name = entry.hostname
				else:
					name = entry.server+":"+str(entry.port)

				sw = self.getServerSubWindow(entry)
				wl = self.getAllSubChatWindows(entry)
				total = self.getAllSubWindows(entry)

				if len(total)>0:
					sm = self.windowsMenu.addMenu(QIcon(NETWORK_ICON),name)

					entry = QAction(QIcon(CONSOLE_ICON),name,self)
					entry.triggered.connect(lambda state,u=sw: self.showSubWindow(u))
					sm.addAction(entry)

					sm.addSeparator()

					for w in wl:
						c = w.widget()

						if c.window_type==CHANNEL_WINDOW:
							icon = CHANNEL_ICON
						elif c.window_type==SERVER_WINDOW:
							icon = CONSOLE_ICON
						elif c.window_type==PRIVATE_WINDOW:
							icon = PRIVATE_ICON

						entry = QAction(QIcon(icon),c.name,self)
						entry.triggered.connect(lambda state,u=w: self.showSubWindow(u))
						sm.addAction(entry)

			self.windowsMenu.addSeparator()

			entry = QAction(QIcon(NEXT_ICON),"Next window",self)
			entry.setShortcut('Ctrl++')
			entry.triggered.connect(self.MDI.activateNextSubWindow)
			self.windowsMenu.addAction(entry)

			entry = QAction(QIcon(PREVIOUS_ICON),"Previous window",self)
			entry.setShortcut('Ctrl+-')
			entry.triggered.connect(self.MDI.activatePreviousSubWindow)
			self.windowsMenu.addAction(entry)

	# |---------------|
	# | EVENT METHODS |
	# |---------------|

	# closeEvent()
	# Triggered when the client window is closed, via
	# any method 
	def closeEvent(self, event):

		self.closeAndRemoveAllWindows()
		self.app.quit()

	# subWindowActivated()
	# Triggered whenever a subwindow is activated
	def subWindowActivated(self,subwindow):

		# Reset the window title
		self.setWindowTitle(config.DISPLAY_NAME)

		if subwindow==None: return

		w = subwindow.widget()
		if hasattr(w,"name"):
			# It's a named subwindow
			if config.DISPLAY_ACTIVE_CHAT_IN_TITLE:
				if w.client.hostname:
					server = w.client.hostname
				else:
					server = w.client.server+":"+str(w.client.port)
				if w.window_type==SERVER_WINDOW:
					self.setWindowTitle(config.DISPLAY_NAME+" - "+server)
				else:
					self.setWindowTitle(config.DISPLAY_NAME+" - "+w.name+" ("+server+")")
			pass

		if hasattr(w,"input"):
			w.input.setFocus()