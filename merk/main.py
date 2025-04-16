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
import sys

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

from .widgets import menubar

class Merk(QMainWindow):

	# ===========
	# Constructor
	# ===========

	def __init__(
			self,
			app,
			configuration_location=None,
			configuration_directory_name=".merk",
			connection_info=None,
			application_font=None,
			no_commands=False,
			channels=[],
			dark_mode = False,
			default_palette=None,
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
		self.dark_mode = dark_mode
		self.default_palette = default_palette

		if self.dark_mode:
			self.checked_icon = DARK_CHECKED_ICON
			self.unchecked_icon = DARK_UNCHECKED_ICON
			self.round_checked_icon = DARK_ROUND_CHECKED_ICON
			self.round_unchecked_icon = DARK_ROUND_UNCHECKED_ICON
			self.options_icon = DARK_OPTIONS_ICON
			self.bold_icon = DARK_BOLD_ICON
			self.italic_icon = DARK_ITALIC_ICON
			self.spellcheck_icon = DARK_SPELLCHECK_ICON
			self.menu_icon = DARK_MENU_ICON
			self.window_icon = DARK_WINDOW_ICON
			self.systray_icon = DARK_SYSTRAY_ICON
		else:
			self.checked_icon = CHECKED_ICON
			self.unchecked_icon = UNCHECKED_ICON
			self.round_checked_icon = ROUND_CHECKED_ICON
			self.round_unchecked_icon = ROUND_UNCHECKED_ICON
			self.options_icon = OPTIONS_ICON
			self.bold_icon = BOLD_ICON
			self.italic_icon = ITALIC_ICON
			self.spellcheck_icon = SPELLCHECK_ICON
			self.menu_icon = MENU_ICON
			self.window_icon = WINDOW_ICON
			self.systray_icon = SYSTRAY_ICON

		# Set the application font
		self.app.setFont(self.application_font)

		# Set the widget font
		self.setFont(self.application_font)

		# Internal attributes
		self.quitting = {}
		self.hiding = {}
		self.scripts = {}
		self.reconnecting = {}
		self.is_hidden = False
		self.was_maximized = False
		self.maximized_window = None

		self.resize_timer = QTimer(self)
		self.resize_timer.timeout.connect(self.on_resize_complete)
		self.resize_delay = 200

		# Create the central object of the client,
		# the MDI widget
		self.MDI = QMdiArea()
		self.setCentralWidget(self.MDI)
		self.MDI.subWindowActivated.connect(self.subWindowActivated)

		# Set the background image of the MDI widget
		if self.dark_mode:
			backgroundPix = QPixmap(DARK_MDI_BACKGROUND)
		else:
			backgroundPix = QPixmap(MDI_BACKGROUND)
		backgroundBrush = QBrush(backgroundPix)
		self.MDI.setBackground(backgroundBrush)

		# Set the window title
		self.setWindowTitle(APPLICATION_NAME)
		self.setWindowIcon(QIcon(APPLICATION_ICON))

		# Systray

		self.flash = QTimer(self)
		self.flash.timeout.connect(self.blink)
		self.alternate = config.FLASH_SYSTRAY_SPEED
		self.flash_time = 500
		self.notifications = False

		self.tray_blank_icon = QIcon(NORMAL_USER)
		self.tray_icon = QIcon(APPLICATION_ICON)

		self.tray = QSystemTrayIcon() 
		self.tray.setIcon(self.tray_icon)
		if config.SHOW_SYSTRAY_ICON==False:
			self.tray.setVisible(False)
		else:
			self.tray.setVisible(True)
		self.tray.setToolTip(APPLICATION_NAME+" IRC client")

		self.tray_notifications = []
		self.tray_width = self.width()
		self.tray_height = self.height()

		self.trayMenu = QMenu()
		self.tray.setContextMenu(self.trayMenu)
		self.buildSystrayMenu()

		self.tray.activated.connect(self.systray_clicked)

		if config.SHOW_SYSTRAY_ICON==False:
			self.tray.hide()

		# Build the main menu
		self.buildMenu()

		# Windowbar
		self.initWindowbar()

		if connection_info:
			self.connectToIrc(connection_info)

	# Windowbar
	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.resize_timer.start(self.resize_delay)

	def on_resize_complete(self):
		self.resize_timer.stop()

		self.buildWindowbar()

	def initWindowbar(self):

		# Build the main menu
		self.buildMenu()

		if hasattr(self,"windowbar"): self.removeToolBar(self.windowbar)

		if hasattr(self,"menuTool"):
			self.insertToolBarBreak(self.menuTool)

		self.addToolBarBreak(Qt.TopToolBarArea)

		self.windowbar = menubar.generate_window_toolbar(self)
		self.windowbar.setMovable(config.WINDOWBAR_CAN_FLOAT)
		if config.WINDOWBAR_TOP_OF_SCREEN:
			self.addToolBar(Qt.TopToolBarArea,self.windowbar)
		else:
			self.addToolBar(Qt.BottomToolBarArea,self.windowbar)
		self.windowbar.hide()
		self.MDI.subWindowActivated.connect(self.buildWindowbar)

		self.buildWindowbar()

	def size_of_list(self,wl):
		window_titles = []
		for window in wl:
			if hasattr(window,"widget"):
				c = window.widget()
				window_titles.append(c.name)
		all_windows = ' '.join(window_titles)
		fm = QFontMetrics(self.font())
		window_width = fm.horizontalAdvance(all_windows) + (len(wl) * 20)
		if config.WINDOWBAR_SHOW_ICONS: window_width = window_width + (len(wl)*16)

		return window_width

	def raw_size_of_list(self,wl):
		all_windows = ' '.join(wl)
		fm = QFontMetrics(self.font())
		window_width = fm.horizontalAdvance(all_windows) + (len(wl) * 20)
		if config.WINDOWBAR_SHOW_ICONS: window_width = window_width + (len(wl)*16)

		return window_width

	def split_up_windowbar(self,windows):
		# Get length of entries
		window_width = self.size_of_list(windows)
		if self.width()>window_width:
			return [ windows, [] ]

		full = []
		abbv = []
		window_titles = []
		for window in windows:
			if hasattr(window,"widget"):
				c = window.widget()
				window_titles.append(c.name)

				if self.raw_size_of_list(window_titles)<(self.width()*0.75):
					full.append(window)
				else:
					abbv.append(window)
		return [full,abbv]

	def buildWindowbar(self):

		if not hasattr(self,"windowbar"): return

		if config.SHOW_WINDOWBAR==False:
			self.windowbar.hide()
			return

		self.windowbar.clear()

		self.windowbar.setMovable(config.WINDOWBAR_CAN_FLOAT)

		listOfConnections = {}
		for i in irc.CONNECTIONS:
			add_to_list = True
			for j in self.hiding:
				if self.hiding[j] is irc.CONNECTIONS[i]: add_to_list = False
			if add_to_list: listOfConnections[i] = irc.CONNECTIONS[i]

		window_list = []
		for i in listOfConnections:
			entry = listOfConnections[i]

			if config.WINDOWBAR_INCLUDE_SERVERS:
				window_list.append(self.getServerSubWindow(entry))

			for window in self.getAllSubChatWindows(entry):
				window_list.append(window)

		if config.WINDOWBAR_INCLUDE_EDITORS:
			for window in self.getAllEditorWindows():
				window_list.append(window)

		if len(window_list)>0:
			self.windowbar.show()
		else:
			self.windowbar.hide()
			return

		if config.WINDOWBAR_JUSTIFY.lower()=='center' or config.WINDOWBAR_JUSTIFY.lower()=='right':
			menubar.add_toolbar_stretch(self.windowbar)

		# Rearrange the windowlist so that the current
		# window is always first
		if config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST:
			x = self.MDI.activeSubWindow()
			rearranged = []
			for w in window_list:
				if w==x:
					rearranged.insert(0,w)
				else:
					rearranged.append(w)
			window_list = rearranged

		te = self.split_up_windowbar(window_list)
		
		full_display = te[0]
		partial_display = te[1]

		# Make sure the current active window is
		# in the full display list if it's not first
		if not config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST:
			x = self.MDI.activeSubWindow()
			aw = 0
			domove = False
			for w in partial_display:
				if w==x:
					full_display.append(partial_display.pop(aw))
					domove = True
				aw = aw + 1
			if domove: partial_display.append(full_display.pop(0))
		
		button_list = []

		for window in full_display:
			if hasattr(window,"widget"):
				c = window.widget()

				if c.window_type==CHANNEL_WINDOW:
					icon = CHANNEL_ICON
					wname = c.name
					if c.client.hostname:
						serv_name = name = c.client.hostname
					else:
						serv_name = c.client.server+":"+str(entry.port)

					if c.client.network:
						serv_name = serv_name + " ("+c.client.network+")"
				elif c.window_type==PRIVATE_WINDOW:
					icon = PRIVATE_ICON
					wname = c.name
					if c.client.hostname:
						serv_name = name = c.client.hostname
					else:
						serv_name = c.client.server+":"+str(entry.port)

					if c.client.network:
						serv_name = serv_name + " ("+c.client.network+")"
				elif c.window_type==SERVER_WINDOW:
					icon = CONSOLE_ICON
					wname = c.name
					if c.client.hostname:
						serv_name = name = c.client.hostname
					else:
						serv_name = c.client.server+":"+str(entry.port)

					if hasattr(c.client,"network"):
						if c.client.network:
							serv_name = serv_name + " ("+c.client.network+")"
				elif c.window_type==EDITOR_WINDOW:
					icon = SCRIPT_ICON
					if c.editing_user_script:
						wname = c.current_user_script
						serv_name = c.current_user_script
					else:
						if c.filename==None:
							wname = "Untitled script"
							serv_name = "Unsaved"
						else:
							wname = os.path.basename(c.filename)
							serv_name = c.filename

				if config.WINDOWBAR_SHOW_ICONS:
					button = menubar.get_icon_windowbar_button(icon,wname)
				else:
					button = menubar.get_windowbar_button(wname)
				button.clicked.connect(lambda u=window: self.showSubWindow(u))
				if config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED:
					button.doubleClicked.connect(lambda u=window: self.showSubWindowMaximized(u))
				else:
					button.doubleClicked.connect(lambda u=window: self.showSubWindow(u))
				if c.window_type==CHANNEL_WINDOW:
					button.setToolTip(serv_name)
				if c.window_type==PRIVATE_WINDOW:
					button.setToolTip(serv_name)
				if c.window_type==EDITOR_WINDOW:
					button.setToolTip(serv_name)
				if c.window_type==SERVER_WINDOW:
					button.setToolTip(serv_name)
				if c.window_type==EDITOR_WINDOW:
					button.setToolTip(wname)

				if not config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST:
					if window == self.MDI.activeSubWindow():
						font = QFont()
						font.setBold(True)
						font.setUnderline(True)
						button.setFont(font)

				button.setFixedHeight(18)
				button_list.append(button)


		for window in partial_display:
			if hasattr(window,"widget"):
				c = window.widget()

				if c.window_type==CHANNEL_WINDOW:
					icon = CHANNEL_ICON
					wname = c.name
					if c.client.hostname:
						serv_name = name = c.client.hostname
					else:
						serv_name = c.client.server+":"+str(entry.port)

					if c.client.network:
						serv_name = serv_name + " ("+c.client.network+")"
				elif c.window_type==PRIVATE_WINDOW:
					icon = PRIVATE_ICON
					wname = c.name
					if c.client.hostname:
						serv_name = name = c.client.hostname
					else:
						serv_name = c.client.server+":"+str(entry.port)

					if c.client.network:
						serv_name = serv_name + " ("+c.client.network+")"
				elif c.window_type==SERVER_WINDOW:
					icon = CONSOLE_ICON
					wname = c.name
					if c.client.hostname:
						serv_name = name = c.client.hostname
					else:
						serv_name = c.client.server+":"+str(entry.port)

					if c.client.network:
						serv_name = serv_name + " ("+c.client.network+")"
				elif c.window_type==EDITOR_WINDOW:
					icon = SCRIPT_ICON
					if c.editing_user_script:
						wname = c.current_user_script
						serv_name = c.current_user_script
					else:
						if c.filename==None:
							wname = "Untitled script"
							serv_name = "Unsaved"
						else:
							wname = os.path.basename(c.filename)
							serv_name = c.filename

				button = menubar.get_icon_only_toolbar_button(icon)
				button.clicked.connect(lambda u=window: self.showSubWindow(u))
				if config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED:
					button.doubleClicked.connect(lambda u=window: self.showSubWindowMaximized(u))
				else:
					button.doubleClicked.connect(lambda u=window: self.showSubWindow(u))
				if c.window_type==CHANNEL_WINDOW:
					button.setToolTip(c.name + "\n" + serv_name)
				if c.window_type==PRIVATE_WINDOW:
					button.setToolTip(serv_name)
					button.setToolTip(c.name + "\n" + serv_name)
				if c.window_type==EDITOR_WINDOW:
					button.setToolTip(c.name + "\n" + serv_name)
				if c.window_type==SERVER_WINDOW:
					button.setToolTip(serv_name)
				if c.window_type==EDITOR_WINDOW:
					button.setToolTip(wname)

				button.setFixedHeight(18)
				button_list.append(button)
		
		if config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST:
			if len(button_list)>0:
				font = QFont()
				font.setBold(True)
				font.setUnderline(True)
				button_list[0].setFont(font)

		for b in button_list:
			self.windowbar.addWidget(b)

		if config.WINDOWBAR_JUSTIFY.lower()=='center':
			menubar.add_toolbar_stretch(self.windowbar)

		self.windowbar.topLevelChanged.connect(self.windowDocked)

	def windowDocked(self,is_floating):
		if not is_floating:
			p = self.toolBarArea(self.windowbar)
			if p == Qt.TopToolBarArea:
				# it's at the top
				config.WINDOWBAR_TOP_OF_SCREEN = True
				config.save_settings(config.CONFIG_FILE)
			else:
				# it's at the bottom
				config.WINDOWBAR_TOP_OF_SCREEN = False
				config.save_settings(config.CONFIG_FILE)

	# SYSTRAY MENU

	def show_notifications(self,note=''):
		if config.FLASH_SYSTRAY_NOTIFICATION:
			if self.is_hidden:
				self.notifications = True
				if config.FLASH_SYSTRAY_LIST:
					if note!='':
						self.tray_notifications.append(note)
					if len(self.tray_notifications)>0:
						self.tray.setToolTip("\n".join(self.tray_notifications))
				if not self.flash.isActive():
					self.flash.start(self.flash_time)
			else:
				self.notifications = False
		else:
			self.notifications = False

	def hide_notifications(self):
		self.notifications = False
		self.tray.setIcon(self.tray_icon)
		self.tray_notifications = []
		self.tray.setToolTip(APPLICATION_NAME+" IRC client")

	def blink(self):
		if self.notifications==False:
			self.flash.stop()
			self.tray.setIcon(self.tray_icon)
			return
		if self.alternate:
			self.tray.setIcon(self.tray_blank_icon)
			self.flash.start(self.flash_time)
			self.alternate = False
		else:
			self.tray.setIcon(self.tray_icon)
			self.flash.start(self.flash_time)
			self.alternate = True

	def systray_clicked(self,reason):
		if reason == QSystemTrayIcon.ActivationReason.Trigger:
			#print("Single click")
			pass
		elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
			if self.is_hidden:
				self.toggleHide()
				self.showNormal()

	def changeEvent(self, event):
		if event.type() == QEvent.WindowStateChange:
			if self.windowState() & Qt.WindowMinimized:
				if config.MINIMIZE_TO_SYSTRAY==True:
					if config.SHOW_SYSTRAY_ICON==True:
						self.toggleHide()
		super().changeEvent(event)

	def toggleHide(self):
		if self.is_hidden:
			self.show()
			self.resize(self.tray_width,self.tray_height)
			self.is_hidden = False
			self.hide_notifications()

			if self.maximized_window!=None:
				self.maximized_window.showMaximized()
				if self.was_maximized:
					self.showNormal()
					self.showMaximized()
		else:
			if self.isMaximized():
				self.was_maximized = True
			if self.isMinimized():
				self.was_maximized = False
			active_subwindow = self.MDI.activeSubWindow()
			if active_subwindow:
				if active_subwindow.windowState() & QtCore.Qt.WindowMaximized:
					self.maximized_window = active_subwindow
				else:
					self.maximized_window = None
			else:
				self.maximized_window = None

			self.tray_width = self.width()
			self.tray_height = self.height()

			self.hide()
			self.is_hidden = True
		self.buildSystrayMenu()

	def buildSystrayMenu(self):

		if config.SYSTRAY_MENU==False:
			self.trayMenu.clear()
			self.tray.setContextMenu(None)
			return

		self.tray.setContextMenu(self.trayMenu)

		self.trayMenu.clear()

		entry = widgets.ExtendedMenuItemNoAction(self,APPLICATION_MENU_ICON,APPLICATION_NAME,APPLICATION_VERSION,25)
		self.trayMenu.addAction(entry)

		windows = self.getAllServerWindows()
		clean = []
		for w in windows:
			c = w.widget()
			if c.client.client_id in self.quitting: continue
			clean.append(w)
		windows = clean

		listOfConnections = {}
		for i in irc.CONNECTIONS:
			add_to_list = True
			for j in self.hiding:
				if self.hiding[j] is irc.CONNECTIONS[i]: add_to_list = False
			if add_to_list: listOfConnections[i] = irc.CONNECTIONS[i]

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
					sm = self.trayMenu.addMenu(QIcon(CONNECT_ICON),name)

					entry = QAction(QIcon(CONSOLE_ICON),name,self)
					entry.triggered.connect(lambda state,u=sw: self.systrayShowWindow(u))
					sm.addAction(entry)

					if len(wl)>0: sm.addSeparator()

					for w in wl:
						c = w.widget()

						if c.window_type==CHANNEL_WINDOW:
							icon = CHANNEL_ICON
						elif c.window_type==SERVER_WINDOW:
							icon = CONSOLE_ICON
						elif c.window_type==PRIVATE_WINDOW:
							icon = PRIVATE_ICON

						entry = QAction(QIcon(icon),c.name,self)
						entry.triggered.connect(lambda state,u=w: self.systrayShowWindow(u))
						sm.addAction(entry)

		self.trayMenu.addSeparator()

		self.trayFolder = self.trayMenu.addMenu(QIcon(FOLDER_ICON),"Folders")

		entry = QAction(QIcon(APPLICATION_ICON),APPLICATION_NAME,self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+INSTALL_DIRECTORY))))
		self.trayFolder.addAction(entry)

		entry = QAction(QIcon(FOLDER_ICON),"Settings",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+config.CONFIG_DIRECTORY))))
		self.trayFolder.addAction(entry)

		entry = QAction(QIcon(FOLDER_ICON),"Styles",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+styles.STYLE_DIRECTORY))))
		self.trayFolder.addAction(entry)

		entry = QAction(QIcon(FOLDER_ICON),"Logs",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+logs.LOG_DIRECTORY))))
		self.trayFolder.addAction(entry)

		entry = QAction(QIcon(FOLDER_ICON),"Scripts",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+commands.SCRIPTS_DIRECTORY))))
		self.trayFolder.addAction(entry)


		self.trayLinks = self.trayMenu.addMenu(QIcon(LINK_ICON),"Links")

		entry = QAction(QIcon(LINK_ICON),"Source code",self)
		entry.triggered.connect(lambda state,u=APPLICATION_SOURCE: self.openLinkInBrowser(u))
		self.trayLinks.addAction(entry)

		entry = QAction(QIcon(LINK_ICON),"GPL v3",self)
		entry.triggered.connect(lambda state,u="https://www.gnu.org/licenses/gpl-3.0.en.html": self.openLinkInBrowser(u))
		self.trayLinks.addAction(entry)

		entry = QAction(QIcon(LINK_ICON),"Emoji shortcodes",self)
		entry.triggered.connect(lambda state,u="https://carpedm20.github.io/emoji/all.html?enableList=enable_list_alias": self.openLinkInBrowser(u))
		self.trayLinks.addAction(entry)

		self.trayMenu.addSeparator()

		entry = QAction(QIcon(QUIT_ICON),"Exit",self)
		entry.triggered.connect(self.close)
		self.trayMenu.addAction(entry)

	def systrayShowWindow(self,window):
		self.toggleHide()
		self.showNormal()
		self.showSubWindow(window)
		window.showMaximized()

	def menuMax(self):

		if self.windowState() == Qt.WindowMaximized:
			self.setWindowState(Qt.WindowNoState)
		else:
			self.setWindowState(Qt.WindowMaximized)

	def menuMin(self):

		if self.windowState() == Qt.WindowMinimized:
			self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
		else:
			self.setWindowState(Qt.WindowMinimized)

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

		# If the flash doesn't work, just ignore the error
		try:
			if config.FLASH_SYSTRAY_DISCONNECT: self.show_notifications("Connection to "+client.hostname+" lost")
		except:
			pass

		# Update all editor run menus
		e = self.getAllEditorWindows()
		for w in e:
			c = w.widget()
			c.buildRunMenu()

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
			w.script_button.setEnabled(True)

			self.buildWindowsMenu()
		
		self.nickChanged(client)

		if not self.no_commands:
			w = self.getServerWindow(client)
			if w:
				hostid = client.server+":"+str(client.port)
				if hostid in user.COMMANDS:
					commands.executeScript(self,w,user.COMMANDS[hostid])

		if len(self.join_channels)>0:
			for e in self.join_channels:
				client.join(e[0],e[1])
			self.join_channels = []

		# Update all editor run menus
		e = self.getAllEditorWindows()
		for w in e:
			c = w.widget()
			c.buildRunMenu()

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
		
	def away(self,client,msg):
		w = self.getServerWindow(client)
		if w:
			t = Message(SYSTEM_MESSAGE,'',f"You are marked as being away")
			w.writeText(t)

	def back(self,client):
		w = self.getServerWindow(client)
		if w:
			t = Message(SYSTEM_MESSAGE,'',f"You are marked as being back")
			w.writeText(t)

	def gotVersion(self,client,server,version):
		w = self.getServerWindow(client)
		if w:
			t = Message(SYSTEM_MESSAGE,'',f"{server} VERSION: {version}")
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

			# Notify if the message has the user's nick
			# in it
			if client.nickname in msg:
				if config.FLASH_SYSTRAY_NICKNAME:
					self.show_notifications("Mentioned by "+nickname+" in "+target)

			# Channel message
			w = self.getWindow(target,client)
			if w:
				t = Message(CHAT_MESSAGE,user,msg)
				w.writeText(t)
				return

		if target==client.nickname:
			displayed_private_message = False

			if config.FLASH_SYSTRAY_PRIVATE: self.show_notifications("Received private message from "+nickname)

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

		if config.FLASH_SYSTRAY_NOTICE: self.show_notifications("Received a notice from "+nickname)

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

	def gotTime(self,client,server,time):
		w = self.getServerWindow(client)
		if w:
			t = Message(SYSTEM_MESSAGE,"",f"{server} reports time {time}")
			w.writeText(t)

	def gotBanlist(self,client,channel,banlist):
		w = self.getWindow(channel,client)
		if w:
			w.banlist = banlist.copy()
			w.refreshBanMenu()
			return

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

		p = user.split("!")
		if len(p)==2:
			nickname = p[0]
			hostmask = p[1]
		else:
			nickname = user
			hostmask = None

		if client.nickname in argument:
			if config.FLASH_SYSTRAY_MODE: self.show_notifications(nickname+" set mode +"+mode+" "+' '.join(argument)+" on "+target)

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

		p = user.split("!")
		if len(p)==2:
			nickname = p[0]
			hostmask = p[1]
		else:
			nickname = user
			hostmask = None

		if client.nickname in argument:
			if config.FLASH_SYSTRAY_MODE: self.show_notifications(nickname+" set mode -"+mode+" "+' '.join(argument)+" on "+target)

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
		
		if config.FLASH_SYSTRAY_KICK: self.show_notifications("Kicked from "+channel+" by "+kicker+": "+message)


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

		if not client.registered: return

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

		if config.FLASH_SYSTRAY_INVITE: self.show_notifications("Invited to "+channel+" by "+user)

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
		connection = ConnectDialogNoLogo(self.app,self,message,reason,self.no_commands,self.dark_mode)

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
			connection = ConnectDialogNoLogo(self.app,self,'','',self.no_commands,self.dark_mode)
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
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"client"):
				if c.client.client_id == client.client_id:
					c.refreshModeDisplay()
		self.MDI.setActiveSubWindow(w)

	def setAllFont(self,newfont):
		w = self.MDI.activeSubWindow()
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
		self.MDI.setActiveSubWindow(w)

	def rerenderUserlists(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"userlist"):
				c.rerenderUserlist()
		self.MDI.setActiveSubWindow(w)

	def toggleNickDisplay(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"nick_display"):
				c.toggleNickDisplay()
		self.MDI.setActiveSubWindow(w)

	def setAllLanguage(self,newlang):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"menuSetLanguage"):
				c.menuSetLanguage(newlang)
		self.MDI.setActiveSubWindow(w)

	def reRenderAll(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"rerenderChatLog"):
				c.rerenderChatLog()
			if hasattr(c,"rerenderEditor"):
				c.rerenderEditor()
		self.MDI.setActiveSubWindow(w)

	def reApplyStyle(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"applyStyle"):
				c.applyStyle()
		self.MDI.setActiveSubWindow(w)

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

	def hideAllTopic(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if c.window_type==CHANNEL_WINDOW:
					c.hideTopic()
		self.MDI.setActiveSubWindow(w)

	def showAllTopic(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if c.window_type==CHANNEL_WINDOW:
					c.showTopic()
		self.MDI.setActiveSubWindow(w)

	def refreshAllTopic(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if c.window_type==CHANNEL_WINDOW:

					if config.CHANNEL_TOPIC_BOLD:
						font = QFont()
						font.setBold(True)
						c.topic.setFont(font)
					else:
						font = QFont()
						font.setBold(False)
						c.topic.setFont(font)

					c.topic.refresh()
		self.MDI.setActiveSubWindow(w)

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

	def showSubWindowMaximized(self,window):
		if window.isMaximized():
			window.showNormal()
		else:
			window.showMaximized()
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

	def newEditorWindow(self):
		w = QMdiSubWindow(self)
		w.setWidget(widgets.ScriptEditor(None,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		w.setWindowIcon(QIcon(SCRIPT_ICON))
		self.MDI.addSubWindow(w)
		self.settingsMenu.close()
		self.buildWindowsMenu()
		w.show()

		return w

	def newEditorWindowFile(self,filename):
		w = QMdiSubWindow(self)
		w.setWidget(widgets.ScriptEditor(filename,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		w.setWindowIcon(QIcon(SCRIPT_ICON))
		self.MDI.addSubWindow(w)
		self.settingsMenu.close()
		self.buildWindowsMenu()
		w.show()

		return w

	def newEditorWindowConnect(self,hostid):
		w = QMdiSubWindow(self)
		w.setWidget(widgets.ScriptEditor(None,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		w.setWindowIcon(QIcon(SCRIPT_ICON))
		self.MDI.addSubWindow(w)
		self.settingsMenu.close()
		self.buildWindowsMenu()
		w.show()

		c = w.widget()
		c.openScript(hostid)

		return w

	def openLinkInBrowser(self,url):
		u = QUrl()
		u.setUrl(url)
		QDesktopServices.openUrl(u)

	def swapAllUserlists(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if c.window_type==CHANNEL_WINDOW:
					c.swapUserlist()
		self.MDI.setActiveSubWindow(w)

	def toggleAllUserlists(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if c.window_type==CHANNEL_WINDOW:
					c.showHideUserlist()
		self.MDI.setActiveSubWindow(w)

	def toggleSpellcheck(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if hasattr(c,"buildInputOptionsMenu"):
					c.buildInputOptionsMenu()
		self.MDI.setActiveSubWindow(w)

	def toggleInputMenu(self):
		w = self.MDI.activeSubWindow()
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if hasattr(c,"toggleInputMenu"):
					c.toggleInputMenu()
		self.MDI.setActiveSubWindow(w)


	# |--------------|
	# | MENU METHODS |
	# |--------------|

	def buildSettingsMenu(self):

		self.settingsMenu.clear()

		entry = widgets.ExtendedMenuItem(self,SETTINGS_MENU_ICON,'Settings','Configure '+APPLICATION_NAME+' preferences&nbsp;&nbsp;',25,self.openSettings)
		self.settingsMenu.addAction(entry)

		entry = widgets.ExtendedMenuItem(self,STYLE_MENU_ICON,'Style','Edit default text style&nbsp;&nbsp;',25,self.menuEditStyle)
		self.settingsMenu.addAction(entry)

		entry = widgets.ExtendedMenuItem(self,SCRIPT_MENU_ICON,'Script Editor','Edit '+APPLICATION_NAME+' scripts&nbsp;&nbsp;',25,self.newEditorWindow)
		self.settingsMenu.addAction(entry)

		entry = widgets.ExtendedMenuItem(self,LOG_MENU_ICON,'Export Logs','Export logs to text or JSON&nbsp;&nbsp;',25,self.menuExportLog)
		self.settingsMenu.addAction(entry)

		self.settingsMenu.addSeparator()

		sm = self.settingsMenu.addMenu(QIcon(FOLDER_ICON),"Application folders")

		entry = QAction(QIcon(APPLICATION_ICON),APPLICATION_NAME+" installation",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+INSTALL_DIRECTORY))))
		sm.addAction(entry)

		entry = QAction(QIcon(SETTINGS_ICON),"Settings directory",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+config.CONFIG_DIRECTORY))))
		sm.addAction(entry)

		entry = QAction(QIcon(STYLE_ICON),"Styles directory",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+styles.STYLE_DIRECTORY))))
		sm.addAction(entry)

		entry = QAction(QIcon(LOG_ICON),"Logs directory",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+logs.LOG_DIRECTORY))))
		sm.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Scripts directory",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+commands.SCRIPTS_DIRECTORY))))
		sm.addAction(entry)

	def buildHelpMenu(self):

		self.helpMenu.clear()

		entry = widgets.ExtendedMenuItem(self,APPLICATION_MENU_ICON,'About '+APPLICATION_NAME,"Version "+APPLICATION_VERSION,25,self.showAbout)
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

	def buildWindowsMenu(self):

		# Rebuild systray menu
		self.buildSystrayMenu()

		# Rebuild windowbar
		self.buildWindowbar()

		self.windowsMenu.clear()

		listOfConnections = {}
		for i in irc.CONNECTIONS:
			add_to_list = True
			for j in self.hiding:
				if self.hiding[j] is irc.CONNECTIONS[i]: add_to_list = False
			if add_to_list: listOfConnections[i] = irc.CONNECTIONS[i]

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
					sm = self.windowsMenu.addMenu(QIcon(CONNECT_ICON),name)

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

		edwins = self.getAllEditorWindows()
		if len(edwins)>0:

			for win in edwins:
				c = win.widget()
				entry = QAction(QIcon(SCRIPT_ICON),c.name,self)
				entry.triggered.connect(lambda state,u=win: self.showSubWindow(u))
				self.windowsMenu.addAction(entry)

		self.windowsMenu.addSeparator()

		entry3 = QAction(QIcon(NEXT_ICON),"Next window",self)
		entry3.setShortcut('Ctrl++')
		entry3.triggered.connect(self.MDI.activateNextSubWindow)
		self.windowsMenu.addAction(entry3)

		entry4 = QAction(QIcon(PREVIOUS_ICON),"Previous window",self)
		entry4.setShortcut('Ctrl+-')
		entry4.triggered.connect(self.MDI.activatePreviousSubWindow)
		self.windowsMenu.addAction(entry4)

		entry1 = QAction("Cascade windows",self)
		entry1.triggered.connect(self.MDI.cascadeSubWindows)
		self.windowsMenu.addAction(entry1)

		entry2 = QAction("Tile windows",self)
		entry2.triggered.connect(self.MDI.tileSubWindows)
		self.windowsMenu.addAction(entry2)

		if len(self.MDI.subWindowList())==0:
			entry1.setEnabled(False)
			entry2.setEnabled(False)
			entry3.setEnabled(False)
			entry4.setEnabled(False)

	def buildMainMenu(self):

		# Rebuild systray menu
		self.buildSystrayMenu()

		self.mainMenu.clear()

		entry = widgets.ExtendedMenuItem(self,CONNECT_ICON,'Connect','Connect to a server  ',25,self.connectMainMenu)
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

		if len(windows)==1:
			self.mainMenu.addSeparator()

		if len(windows)>0:
			if len(windows)==1:
				c = windows[0].widget()
				sname = c.client.server+":"+str(c.client.port)
				title = 'Disconnect from ' + sname
				entry = QAction(QIcon(CLOSE_ICON),title,self)
				entry.triggered.connect(self.disconnectAll)
				self.mainMenu.addAction(entry)
			else:
				title = "Disconnect from all servers"
				entry = widgets.ExtendedMenuItem(self,DISCONNECT_ICON,"Disconnect","Disconnect from all servers",25,self.disconnectAllMainMenu)
				self.mainMenu.addAction(entry)

				self.mainMenu.addSeparator()

			if len(windows)>1:
				for w in windows:
					c = w.widget()
					sname = c.client.server+":"+str(c.client.port)
					entry = QAction(QIcon(CLOSE_ICON),"Disconnect from "+sname,self)
					entry.triggered.connect(lambda state,u=c: u.disconnect())
					self.mainMenu.addAction(entry)

		self.mainMenu.addSeparator()

		entry = QAction(QIcon(QUIT_ICON),"Quit",self)
		entry.triggered.connect(self.close)
		self.mainMenu.addAction(entry)

	def menuDocked(self,is_floating):
		if not is_floating:
			p = self.toolBarArea(self.menuTool)
			if p == Qt.TopToolBarArea:
				# it's at the top
				config.MENUBAR_DOCKED_AT_TOP = True
				config.save_settings(config.CONFIG_FILE)
			else:
				# it's at the bottom
				config.MENUBAR_DOCKED_AT_TOP = False
				config.save_settings(config.CONFIG_FILE)

	def buildMenu(self):

		if hasattr(self,"menuTool"):
			self.removeToolBar(self.menuTool)
			self.addToolBarBreak()

		if not config.USE_MENUBAR:
			if hasattr(self,"menubar"):
				self.menubar.clear()
				self.menubar.show()
			else:
				self.menubar = self.menuBar()
			self.mainMenu = self.menubar.addMenu(config.MAIN_MENU_IRC_NAME)
			self.settingsMenu = self.menubar.addMenu(config.MAIN_MENU_TOOLS_NAME)
			self.windowsMenu = self.menubar.addMenu(config.MAIN_MENU_WINDOWS_NAME)
			self.helpMenu = self.menubar.addMenu(config.MAIN_MENU_HELP_NAME)
		else:
			if hasattr(self,"menubar"):
				self.menubar.clear()
				self.menubar.hide()
			self.mainMenu = QMenu()
			self.settingsMenu = QMenu()
			self.windowsMenu = QMenu()
			self.helpMenu = QMenu()

			self.menuTool = menubar.generate_menubar(self)
			if config.MENUBAR_DOCKED_AT_TOP:
				self.addToolBar(Qt.TopToolBarArea,self.menuTool)
			else:
				self.addToolBar(Qt.BottomToolBarArea,self.menuTool)
			self.menuTool.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
			self.menuTool.topLevelChanged.connect(self.menuDocked)
			self.menuTool.setMovable(config.MENUBAR_CAN_FLOAT)

			if config.MENUBAR_JUSTIFY.lower()=='center' or config.MENUBAR_JUSTIFY.lower()=='right':
				menubar.add_toolbar_stretch(self.menuTool)

			menubar.add_toolbar_menu(self.menuTool,config.MAIN_MENU_IRC_NAME,self.mainMenu)
			menubar.add_toolbar_menu(self.menuTool,config.MAIN_MENU_TOOLS_NAME,self.settingsMenu)
			menubar.add_toolbar_menu(self.menuTool,config.MAIN_MENU_WINDOWS_NAME,self.windowsMenu)
			menubar.add_toolbar_menu(self.menuTool,config.MAIN_MENU_HELP_NAME,self.helpMenu)

			if config.MENUBAR_JUSTIFY.lower()=='center':
				menubar.add_toolbar_stretch(self.menuTool)


		self.buildMainMenu()
		self.buildSettingsMenu()
		self.buildWindowsMenu()
		self.buildHelpMenu()

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

		self.mainMenu.close()

	def connectMainMenu(self):
		self.connectToIrc()
		self.mainMenu.close()

	def disconnectAllMainMenu(self):
		self.disconnectAll()
		self.mainMenu.close()

	def askDisconnect(self,client):

		no_hostname = False
		if not hasattr(client,"hostname"): no_hostname = True
		if not client.hostname: no_hostname = True

		do_disconnect = True

		if config.ASK_BEFORE_DISCONNECT:
			msgBox = QMessageBox()
			msgBox.setIconPixmap(QPixmap(DISCONNECT_DIALOG_IMAGE))
			msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
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
			msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
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

	def getAllEditorWindows(self):
		retval = []
		for window in self.MDI.subWindowList():
			c = window.widget()
			if hasattr(c,"window_type"):
				if c.window_type==EDITOR_WINDOW:
					retval.append(window)
		return retval

			
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
		self.setWindowTitle(APPLICATION_NAME)

		if subwindow==None: return

		w = subwindow.widget()
		if hasattr(w,"name"):
			# It's a named subwindow
			if config.DISPLAY_ACTIVE_CHAT_IN_TITLE:
				if hasattr(w,"client"):
					if w.client.hostname:
						server = w.client.hostname
					else:
						server = w.client.server+":"+str(w.client.port)
					if w.window_type==SERVER_WINDOW:
						self.setWindowTitle(APPLICATION_NAME+" - "+server)
					else:
						self.setWindowTitle(APPLICATION_NAME+" - "+w.name+" ("+server+")")
			pass

		if hasattr(w,"input"):
			w.input.setFocus()