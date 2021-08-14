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
from . import widgets

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

		entry = QAction("Quit",self)
		entry.triggered.connect(self.close)
		self.mainMenu.addAction(entry)

		# Windows menu
		self.windowsMenu = self.menubar.addMenu("Windows")

		entry = QAction("Next",self)
		entry.triggered.connect(self.MDI.activateNextSubWindow)
		self.windowsMenu.addAction(entry)

		entry = QAction("Previous",self)
		entry.triggered.connect(self.MDI.activatePreviousSubWindow)
		self.windowsMenu.addAction(entry)

		self.windowsMenu.addSeparator()

		entry = QAction("Cascade",self)
		entry.triggered.connect(self.MDI.cascadeSubWindows)
		self.windowsMenu.addAction(entry)

		entry = QAction("Tile",self)
		entry.triggered.connect(self.MDI.tileSubWindows)
		self.windowsMenu.addAction(entry)

		self.newChannelWindow("#flarp",None)
		self.newPrivateWindow("Bob",None)
		self.newPrivateWindow("Joe",None)
		self.newServerWindow("Bob",None)

	def subWindowActivated(self,subwindow):
		if subwindow==None: return
		
		w = subwindow.widget()
		if hasattr(w,"name"): print(w.name)

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

	def newChannelWindow(self,name,client):
		w = QMdiSubWindow()
		w.setWidget(widgets.Window(name,client,CHANNEL_WINDOW,self.app,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		self.MDI.addSubWindow(w)
		w.show()

	def newServerWindow(self,name,client):
		w = QMdiSubWindow()
		w.setWidget(widgets.Window(name,client,SERVER_WINDOW,self.app,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		self.MDI.addSubWindow(w)
		w.show()

	def newPrivateWindow(self,name,client):
		w = QMdiSubWindow()
		w.setWidget(widgets.Window(name,client,PRIVATE_WINDOW,self.app,self))
		w.resize(config.DEFAULT_SUBWINDOW_WIDTH,config.DEFAULT_SUBWINDOW_HEIGHT)
		self.MDI.addSubWindow(w)
		w.show()

	# |---------------|
	# | EVENT METHODS |
	# |---------------|

	# closeEvent()
	# Triggered when the client window is closed, via
	# any method 
	def closeEvent(self, event):
		self.app.quit()
