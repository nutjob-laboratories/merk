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
from .dialog import *

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
			parent=None,
		):
		super(Merk, self).__init__(parent)

		# Save any arguments passed to the class
		self.app = app
		self.parent = parent
		self.configuration_location = configuration_location
		self.configuration_directory_name = configuration_directory_name
		self.application_font = application_font

		# Set the application font
		self.app.setFont(self.application_font)

		# Set the widget font
		self.setFont(self.application_font)

		self.quitting = {}

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

		# Main menu
		self.mainMenu = self.menubar.addMenu(config.DISPLAY_NAME)

		entry = widgets.ExtendedMenuItem(self,CONNECT_ICON,'Connect','Connect to a server',25,self.connectToIrc)
		self.mainMenu.addAction(entry)

		entry = widgets.ExtendedMenuItem(self,SETTINGS_ICON,'Settings','Edit settings',25,self.openSettings)
		self.mainMenu.addAction(entry)

		self.mainMenu.addSeparator()

		entry = QAction(QIcon(QUIT_ICON),"Quit",self)
		entry.setShortcut('Ctrl+Q')
		entry.triggered.connect(self.close)
		self.mainMenu.addAction(entry)

		# Windows menu
		self.windowsMenu = self.menubar.addMenu("Windows")

		self.buildWindowsMenu()

		# Entries for command autocomplete
		self.command_autocomplete_data = {
				config.ISSUE_COMMAND_SYMBOL+"part": config.ISSUE_COMMAND_SYMBOL+"part ",
				config.ISSUE_COMMAND_SYMBOL+"join": config.ISSUE_COMMAND_SYMBOL+"join ",
				config.ISSUE_COMMAND_SYMBOL+"notice": config.ISSUE_COMMAND_SYMBOL+"notice ",
				config.ISSUE_COMMAND_SYMBOL+"nick": config.ISSUE_COMMAND_SYMBOL+"nick ",
				config.ISSUE_COMMAND_SYMBOL+"help": config.ISSUE_COMMAND_SYMBOL+"help",
				config.ISSUE_COMMAND_SYMBOL+"topic": config.ISSUE_COMMAND_SYMBOL+"topic ",
				config.ISSUE_COMMAND_SYMBOL+"quit": config.ISSUE_COMMAND_SYMBOL+"quit",
				config.ISSUE_COMMAND_SYMBOL+"msg": config.ISSUE_COMMAND_SYMBOL+"msg ",
				config.ISSUE_COMMAND_SYMBOL+"me": config.ISSUE_COMMAND_SYMBOL+"me ",
				config.ISSUE_COMMAND_SYMBOL+"mode": config.ISSUE_COMMAND_SYMBOL+"mode ",
				config.ISSUE_COMMAND_SYMBOL+"kick": config.ISSUE_COMMAND_SYMBOL+"kick ",
				config.ISSUE_COMMAND_SYMBOL+"whois": config.ISSUE_COMMAND_SYMBOL+"whois ",
				config.ISSUE_COMMAND_SYMBOL+"whowas": config.ISSUE_COMMAND_SYMBOL+"whowas ",
				config.ISSUE_COMMAND_SYMBOL+"who": config.ISSUE_COMMAND_SYMBOL+"who ",
			}

		# The command help system
		command_help_information = [
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"help</b>", "Displays command usage information" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"me MESSAGE</b>", "Sends a CTCP action message to the current chat" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"msg TARGET MESSAGE</b>", "Sends a message" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"notice TARGET MESSAGE</b>", "Sends a notice" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]</b>", "Joins a channel" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"part CHANNEL [MESSAGE]</b>", "Leaves a channel" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"nick NEW_NICKNAME</b>", "Changes your nickname" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC</b>", "Sets a channel topic" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"mode TARGET MODE...</b>", "Sets a mode on a channel or user" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"kick CHANNEL NICKNAME [MESSAGE]</b>", "Kicks a user from a channel" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"whois NICKNAME [SERVER]</b>", "Requests user information from the server" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"who NICKNAME [o]</b>", "Requests user information from the server" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"whowas NICKNAME [COUNT] [SERVER]</b>", "Requests information about previously connected users" ],
			[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"quit [MESSAGE]</b>", "Disconnects from the current IRC server" ],
		]

		global HELP_DISPLAY_TEMPLATE
		if config.AUTOCOMPLETE_COMMANDS:
			HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_AUTOCOMPLETE_%","Command autocomplete is turned on; to use autocomplete, type the first few characters of a command and press the \"tab\" key to complete the command.")
		else:
			HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_AUTOCOMPLETE_%","Command autocomplete is turned off.")

		hdisplay = []
		for e in command_help_information:
			t = HELP_ENTRY_TEMPLATE
			t = t.replace("%_USAGE_%",e[0])
			t = t.replace("%_DESCRIPTION_%",e[1])
			hdisplay.append(t)
		help_display = HELP_DISPLAY_TEMPLATE.replace("%_LIST_%","\n".join(hdisplay))

		self.HELP = Message(RAW_SYSTEM_MESSAGE,'',help_display)

		if connection_info:
			self.connectToIrc(connection_info)

	# BEGIN IRC EVENTS

	def connectionMade(self,client):
		w = self.newServerWindow(client.server+":"+str(client.port),client)
		c = w.widget()
		t = Message(SYSTEM_MESSAGE,'',"Connected to "+client.server+":"+str(client.port)+"!")
		c.writeText(t)

	def connectionLost(self,client):
		
		windows = self.getAllSubWindows(client)
		for w in windows:
			w.close()

		# Forcibly remove server window
		w = self.getServerSubWindow(client)
		self.MDI.removeSubWindow(w)
		self.buildWindowsMenu()

	def signedOn(self,client):

		w = self.getServerWindow(client)
		if w:
			t = Message(SYSTEM_MESSAGE,'',"Registered with server!")
			w.writeText(t)

			if client.hostname:
				w.name = client.hostname
				w.updateTitle()

			w.disconnect_button.setEnabled(True)
			w.nick_button.setEnabled(True)
			w.join_button.setEnabled(True)
			w.info_button.setEnabled(True)
		
		self.nickChanged(client)

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
		w = self.getWindow(target,client)
		if w:
			t = Message(NOTICE_MESSAGE,nickname,msg)
			w.writeText(t)
		else:
			# ...or write it to the server window
			w = self.getServerWindow(client)
			if w:
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

	# END IRC EVENTS

	def openSettings(self):
		self.settingsDialog = SettingsDialog(self.app,self)

	def connectToIrc(self,connection_info=None):
		if connection_info:
			connection = connection_info
		else:
			connection = ConnectDialog(self.app)
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

	def setAllLanguage(self,newlang):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"menuSetLanguage"):
				c.menuSetLanguage(newlang)

	def handleUserInput(self,window,user_input):

		# Handle chat commands
		if self.handleChatCommands(window,user_input): return

		# Handle common commands
		if self.handleCommonCommands(window,user_input): return
		
		# Add emojis to the message
		user_input = emoji.emojize(user_input,use_aliases=True)

		if len(user_input)>0:
			# Client has sent a chat message, so send the message
			window.client.msg(window.name,user_input)
			# ...and then display it to the user
			t = Message(SELF_MESSAGE,window.client.nickname,user_input)
			window.writeText(t)

	
	def handleConsoleInput(self,window,user_input):
		
		# Handle common commands
		if self.handleCommonCommands(window,user_input): return

		t = Message(ERROR_MESSAGE,'',"Unrecognized command: "+user_input)
		window.writeText(t)

	def handleChatCommands(self,window,user_input):
		tokens = user_input.split()

		# |-------|
		# | /kick |
		# |-------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'kick' and len(tokens)>=2:
				tokens.pop(0)
				if tokens[0][:1]=='#':
					# It's a channel, so do nothing; this will be handled
					# by handleCommonCommands()
					pass
				else:
					# If the current window is a channel, try to set the mode
					# on that channel; if not, then this will be handled
					# by handleCommonCommands()
					if window.name[:1]=='#' or window.name[:1]=='&' or window.name[:1]=='!' or window.name[:1]=='+':
						channel = window.name
						target = tokens.pop(0)
						msg = ' '.join(tokens)
						if len(msg.strip())==0: msg = None
						window.client.kick(channel,target,msg)
						return True
					else:
						pass

		# |-------|
		# | /mode |
		# |-------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'mode' and len(tokens)>=2:
				tokens.pop(0)
				if tokens[0][:1]=='#':
					# It's a channel, so do nothing; this will be handled
					# by handleCommonCommands()
					pass
				else:
					# If the current window is a channel, try to set the mode
					# on that channel; if not, then this will be handled
					# by handleCommonCommands()
					if window.name[:1]=='#' or window.name[:1]=='&' or window.name[:1]=='!' or window.name[:1]=='+':
						target = window.name
						mode = ' '.join(tokens)
						window.client.sendLine("MODE "+target+" "+mode)
						return True
					else:
						pass

		# |-----|
		# | /me |
		# |-----|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'me' and len(tokens)>=2:
				tokens.pop(0)
				msg = ' '.join(tokens)
				msg = emoji.emojize(msg,use_aliases=True)
				window.client.describe(window.name,msg)
				t = Message(ACTION_MESSAGE,window.client.nickname,msg)
				window.writeText(t)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'me':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"me MESSAGE")
				window.writeText(t)
				return True

		# |--------|
		# | /topic |
		# |--------|
		# The version of the command allows the user to omit the
		# channel name in the command, much like with /part
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'topic' and len(tokens)>=2:
				tokens.pop(0)
				if tokens[0][:1]=='#' or tokens[0][:1]=='&' or tokens[0][:1]=='!' or tokens[0][:1]=='+':
					# It's a channel, so do nothing; this will be handled
					# by handleCommonCommands()
					pass
				else:
					# Check to make sure that we're trying to set a topic on
					# a channel window and not a private message window
					if window.name[:1]=='#' or window.name[:1]=='&' or window.name[:1]=='!' or window.name[:1]=='+':
						channel = window.name
						msg = ' '.join(tokens)
						msg = emoji.emojize(msg,use_aliases=True)
						window.client.topic(channel,msg)
						return True
					else:
						t = Message(ERROR_MESSAGE,'',"Can't set topic for a private message")
						window.writeText(t)
						return True
		
		# |-------|
		# | /part |
		# |-------|
		# This version of the command allows the user to omit the channel
		# name in the command, with the channel name being the name of
		# the chat window it was issued from
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)==1:
				channel = window.name
				window.client.leave(channel,config.DEFAULT_QUIT_MESSAGE)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)>=2:
				tokens.pop(0)
				if tokens[0][:1]=='#' or tokens[0][:1]=='&' or tokens[0][:1]=='!' or tokens[0][:1]=='+':
					# It's a channel, so do nothing; this will be handled
					# by handleCommonCommands()
					pass
				else:
					# Channel name hasn't been passed, it must be a message
					channel = window.name
					msg = ' '.join(tokens)
					msg = emoji.emojize(msg,use_aliases=True)
					window.client.leave(channel,msg)
					return True

		return False

	def handleCommonCommands(self,window,user_input):
		tokens = user_input.split()

		# |---------|
		# | /whowas |
		# |---------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whowas' and len(tokens)==2:
				tokens.pop(0)
				nick = tokens.pop(0)
				window.client.sendLine("WHOWAS "+nick)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whowas' and len(tokens)==3:
				tokens.pop(0)
				nick = tokens.pop(0)
				arg = tokens.pop(0)
				try:
					arg = int(arg)
				except:
					t = Message(ERROR_MESSAGE,'',"Second argument for "+config.ISSUE_COMMAND_SYMBOL+"whowas must be numeric")
					window.writeText(t)
					return True
				window.client.sendLine("WHOWAS "+nick+" "+str(arg))
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whowas' and len(tokens)==4:
				tokens.pop(0)
				nick = tokens.pop(0)
				arg = tokens.pop(0)
				serv = tokens.pop(0)
				try:
					arg = int(arg)
				except:
					t = Message(ERROR_MESSAGE,'',"Second argument for "+config.ISSUE_COMMAND_SYMBOL+"whowas must be numeric")
					window.writeText(t)
					return True
				window.client.sendLine("WHOWAS "+nick+" "+str(arg)+" "+serv)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whowas':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"whowas NICKNAME [COUNT] [SERVER]")
				window.writeText(t)
				return True

		# |------|
		# | /who |
		# |------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'who' and len(tokens)==2:
				tokens.pop(0)
				nick = tokens.pop(0)
				window.client.sendLine("WHO "+nick)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'who' and len(tokens)==3:
				tokens.pop(0)
				nick = tokens.pop(0)
				arg = tokens.pop(0)
				if arg.lower()!='o':
					t = Message(ERROR_MESSAGE,'',"Improper argument for "+config.ISSUE_COMMAND_SYMBOL+"who")
					window.writeText(t)
					return True
				window.client.sendLine("WHO "+nick+" o")
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'who':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"who NICKNAME [o]")
				window.writeText(t)
				return True

		# |--------|
		# | /whois |
		# |--------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whois' and len(tokens)==2:
				tokens.pop(0)
				nick = tokens.pop(0)
				window.client.whois(nick)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whois' and len(tokens)==3:
				tokens.pop(0)
				nick = tokens.pop(0)
				server = tokens.pop(0)
				window.client.whois(nick,server)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whois':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"whois NICKNAME [SERVER]")
				window.writeText(t)
				return True

		# |-------|
		# | /kick |
		# |-------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'kick' and len(tokens)>=3:
				tokens.pop(0)
				channel = tokens.pop(0)
				target = tokens.pop(0)
				msg = ' '.join(tokens)
				if len(msg.strip())==0: msg = None
				window.client.kick(channel,target,msg)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'kick':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"kick CHANNEL NICKNAME [REASON]")
				window.writeText(t)
				return True

		# |-------|
		# | /mode |
		# |-------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'mode' and len(tokens)>=2:
				tokens.pop(0)
				target = tokens.pop(0)
				mode = ' '.join(tokens)
				window.client.sendLine("MODE "+target+" "+mode)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'mode':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"mode TARGET MODE...")
				window.writeText(t)
				return True


		# |---------|
		# | /notice |
		# |---------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'notice' and len(tokens)>=3:
				tokens.pop(0)
				target = tokens.pop(0)
				msg = ' '.join(tokens)
				msg = emoji.emojize(msg,use_aliases=True)
				window.client.notice(target,msg)

				# If we have the target's window open, write
				# the message there
				w = self.getWindow(target,window.client)
				if w:
					t = Message(NOTICE_MESSAGE,window.client.nickname,msg)
					w.writeText(t)

				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'notice':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"notice TARGET MESSAGE")
				window.writeText(t)
				return True

		# |------|
		# | /msg |
		# |------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'msg' and len(tokens)>=3:
				tokens.pop(0)
				target = tokens.pop(0)
				msg = ' '.join(tokens)
				msg = emoji.emojize(msg,use_aliases=True)
				window.client.msg(target,msg)

				# If we have the target's window open, write
				# the message there
				w = self.getWindow(target,window.client)
				if w:
					t = Message(SELF_MESSAGE,window.client.nickname,msg)
					w.writeText(t)

				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'msg':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"msg TARGET MESSAGE")
				window.writeText(t)
				return True

		# |-------|
		# | /help |
		# |-------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'help':
				window.writeText(self.HELP,False)
				return True

		# |--------|
		# | /topic |
		# |--------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'topic' and len(tokens)>=3:
				tokens.pop(0)
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				msg = emoji.emojize(msg,use_aliases=True)
				window.client.topic(channel,msg)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'topic':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC")
				window.writeText(t)
				return True

		# |-------|
		# | /quit |
		# |-------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quit' and len(tokens)==1:
				if len(config.DEFAULT_QUIT_MESSAGE)>0:
					window.client.quit(config.DEFAULT_QUIT_MESSAGE)
				else:
					window.client.quit()
				self.quitting[window.client.client_id] = 0
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quit' and len(tokens)>=2:
				tokens.pop(0)
				msg = ' '.join(tokens)
				msg = emoji.emojize(msg,use_aliases=True)
				window.client.quit(msg)
				self.quitting[window.client.client_id] = 0
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quit':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"quit [MESSAGE]")
				window.writeText(t)
				return True

		# |-------|
		# | /nick |
		# |-------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'nick' and len(tokens)==2:
				tokens.pop(0)
				newnick = tokens.pop(0)

				# Check to see if the user is trying to /join the
				# channel from the same channel they are in
				if window.client.nickname.lower()==newnick.lower():
					t = Message(ERROR_MESSAGE,'',"You are currently using \""+newnick+"\" as a nickname")
					window.writeText(t)
					return True

				window.client.setNick(newnick)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'nick':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"nick NEW_NICKNAME")
				window.writeText(t)
				return True

		# |-------|
		# | /part |
		# |-------|
		if len(tokens)>1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)==2:
				tokens.pop(0)
				channel = tokens.pop(0)
				window.client.leave(channel,config.DEFAULT_QUIT_MESSAGE)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)>=3:
				tokens.pop(0)
				channel = tokens.pop(0)
				msg = ' '.join(tokens)
				msg = emoji.emojize(msg,use_aliases=True)
				window.client.leave(channel,msg)
				return True

		# |-------|
		# | /join |
		# |-------|
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'join' and len(tokens)==2:
				tokens.pop(0)
				channel = tokens.pop(0)

				# Check to see if the user is trying to /join the
				# channel from the same channel they are in
				if window.name.lower()==channel.lower():
					t = Message(ERROR_MESSAGE,'',"You have already joined "+window.name)
					window.writeText(t)
					return True

				# Check to see if the user has already joined
				# the channel, and switch to the window if they have
				w = self.getSubWindow(channel,window.client)
				if w:
					self.showSubWindow(w)
					return True

				window.client.join(channel)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'join' and len(tokens)==3:
				tokens.pop(0)
				channel = tokens.pop(0)
				key = tokens.pop(0)

				# Check to see if the user is trying to /join the
				# channel from the same channel they are in
				if window.name.lower()==channel.lower():
					t = Message(ERROR_MESSAGE,'',"You have already joined "+window.name)
					window.writeText(t)
					return True

				# Check to see if the user has already joined
				# the channel, and switch to the window if they have
				w = self.getSubWindow(channel,window.client)
				if w:
					self.showSubWindow(w)
					return True

				window.client.join(channel,key)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'join':
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]")
				window.writeText(t)
				return True

		return False

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

	def getAllSubWindows(self,client):
		retval = []
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				if c.client.client_id == client.client_id:
					retval.append(window)
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


	def buildWindowsMenu(self):

		self.windowsMenu.clear()

		entry1 = QAction(QIcon(CASCADE_ICON),"Cascade windows",self)
		entry1.triggered.connect(self.MDI.cascadeSubWindows)
		self.windowsMenu.addAction(entry1)

		entry2 = QAction(QIcon(TILE_ICON),"Tile windows",self)
		entry2.triggered.connect(self.MDI.tileSubWindows)
		self.windowsMenu.addAction(entry2)

		self.windowsMenu.addSeparator()

		if len(irc.CONNECTIONS)==0:
			entry1.setEnabled(False)
			entry2.setEnabled(False)

		if len(irc.CONNECTIONS)>0:

			for i in irc.CONNECTIONS:
				entry = irc.CONNECTIONS[i]
				if entry.hostname:
					name = entry.hostname
				else:
					name = entry.server+":"+str(entry.port)

				wl = self.getAllSubWindows(entry)

				if len(wl)>0:
					sm = self.windowsMenu.addMenu(QIcon(NETWORK_ICON),name)

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

	def subWindowActivated(self,subwindow):
		if subwindow==None: return

		w = subwindow.widget()
		if hasattr(w,"name"):
			# It's a named subwindow
			pass

		if hasattr(w,"input"):
			w.input.setFocus()

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

	def endEverything(self):
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				c.client.quit(config.DEFAULT_QUIT_MESSAGE)
			if window:
				self.MDI.removeSubWindow(window)

	def newChannelWindow(self,name,client):
		w = QMdiSubWindow(self)
		w.setWidget(widgets.Window(name,client,CHANNEL_WINDOW,self.app,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
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
		self.MDI.addSubWindow(w)
		w.show()
		self.buildWindowsMenu()

		return w

	# |---------------|
	# | EVENT METHODS |
	# |---------------|

	# closeEvent()
	# Triggered when the client window is closed, via
	# any method 
	def closeEvent(self, event):
		self.endEverything()
		self.app.quit()
