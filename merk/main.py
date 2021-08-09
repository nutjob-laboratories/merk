
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
	#	configuration_file (string: config filename, default: none)
	# 	parent (parent window, default: None)

	def __init__(
			self,
			app,
			configuration_location=None,
			configuration_file=None,
			parent=None,
		):
		super(Merk, self).__init__(parent)

		# Save any arguments passed to the class
		self.app = app
		self.parent = parent
		self.configuration_location = configuration_location

		# Initialize the config system
		config.initialize(self.configuration_location)

		# Set and save the configuration filename
		if configuration_file==None:
			self.configuration_file = config.CONFIG_FILE
		else:
			self.configuration_file = configuration_file

		# Load the config file
		config.load_settings(self.configuration_file)

		# Set the application font, if the user has
		# set a one that differs from the default
		if config.APPLICATION_FONT!=None:
			f = QFont()
			f.fromString(config.APPLICATION_FONT)
			self.app.setFont(f)

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
