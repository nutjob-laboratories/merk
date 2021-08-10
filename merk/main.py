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

	# |---------------|
	# | EVENT METHODS |
	# |---------------|

	# closeEvent()
	# Triggered when the client window is closed, via
	# any method 
	def closeEvent(self, event):
		self.app.quit()
