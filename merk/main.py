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

from .resources import *
from . import config
from . import styles
from . import widgets
from . import render

# from .irc import(
# 	connect,
# 	connectSSL,
# 	reconnect,
# 	reconnectSSL,
# 	CONNECTIONS
# )

from . import irc

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
			configuration_file=None,
			parent=None,
		):
		super(Merk, self).__init__(parent)

		# Save any arguments passed to the class
		self.app = app
		self.parent = parent
		self.configuration_location = configuration_location
		self.configuration_directory_name = configuration_directory_name
		self.configuration_file = configuration_file

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

		entry = QAction(QIcon(QUIT_ICON),"Quit",self)
		entry.setShortcut('Ctrl+Q')
		entry.triggered.connect(self.close)
		self.mainMenu.addAction(entry)

		# Windows menu
		self.windowsMenu = self.menubar.addMenu("Windows")

		self.buildWindowsMenu()

		# c = self.newChannelWindow("#flarp",None)
		# self.newPrivateWindow("Bob",None)
		# self.newPrivateWindow("Joe",None)
		# self.newServerWindow("Bob",None)

		# w = c.widget()
		# w.writeUserlist(
		# 		[
		# 			"@flarple",
		# 			"joe",
		# 			"alfie",
		# 			"+sn00g",
		# 			"+clark",
		# 			"herb",
		# 			"@argyle"
		# 		]
		# 	)

		irc.reconnect(
			nickname="bob",
			server="localhost",
			port=6667,
			alternate="b0b",
			password=None,
			username="merk_test",
			realname="The Merk Test",
			ssl=False,
			gui=self,
			reconnect=False,
			failreconnect=True,
		)

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
		
		client.join("#themaxx")
		self.nickChanged(client)

	def receivedMOTD(self,client,motd):

		m = "<br>".join(motd)
		w = self.getServerWindow(client)
		if w:
			t = Message(SERVER_MESSAGE,'',m)
			w.writeText(t)

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
	# END IRC EVENTS

	def handleUserInput(self,window,user_input):

		# Handle chat commands
		if self.handleChatCommands(window,user_input): return

		# Handle common commands
		if self.handleCommonCommands(window,user_input): return
		
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
					window.client.leave(channel,msg)
					return True

		return False

	def handleCommonCommands(self,window,user_input):
		tokens = user_input.split()

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


	def buildWindowsMenu(self):

		self.windowsMenu.clear()

		entry = QAction(QIcon(CASCADE_ICON),"Cascade",self)
		entry.triggered.connect(self.MDI.cascadeSubWindows)
		self.windowsMenu.addAction(entry)

		entry = QAction(QIcon(TILE_ICON),"Tile",self)
		entry.triggered.connect(self.MDI.tileSubWindows)
		self.windowsMenu.addAction(entry)

		self.windowsMenu.addSeparator()

		entry = QAction(QIcon(NEXT_ICON),"Next window",self)
		entry.setShortcut('Ctrl++')
		entry.triggered.connect(self.MDI.activateNextSubWindow)
		self.windowsMenu.addAction(entry)

		entry = QAction(QIcon(PREVIOUS_ICON),"Previous window",self)
		entry.setShortcut('Ctrl+-')
		entry.triggered.connect(self.MDI.activatePreviousSubWindow)
		self.windowsMenu.addAction(entry)

		self.windowsMenu.addSeparator()

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

	def subWindowActivated(self,subwindow):
		if subwindow==None: return

		w = subwindow.widget()
		if hasattr(w,"name"):
			# It's a named subwindow
			pass

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
		w = QMdiSubWindow()
		w.setWidget(widgets.Window(name,client,CHANNEL_WINDOW,self.app,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		self.MDI.addSubWindow(w)
		w.show()
		self.buildWindowsMenu()

		return w

	def newServerWindow(self,name,client):
		w = QMdiSubWindow()
		w.setWidget(widgets.Window(name,client,SERVER_WINDOW,self.app,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		self.MDI.addSubWindow(w)
		w.show()
		self.buildWindowsMenu()

		return w

	def newPrivateWindow(self,name,client):
		w = QMdiSubWindow()
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
		self.app.quit()

	