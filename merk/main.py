
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from merk.resources import *

class Merk(QMainWindow):

	# ===========
	# Constructor
	# ===========

	# Arguments:
	# 	app (QApplication)
	# 	parent (parent window, default: None)

	def __init__(
			self,
			app,
			parent=None,
		):
		super(Merk, self).__init__(parent)

		# Save any arguments passed to the class
		self.app = app
		self.parent = parent

		# Create the central object of the client,
		# the MDI widget
		self.MDI = QMdiArea()
		self.setCentralWidget(self.MDI)

		# Set the background image of the MDI widget
		backgroundPix = QPixmap(MDI_BACKGROUND)
		backgroundBrush = QBrush(backgroundPix)
		self.MDI.setBackground(backgroundBrush)

		


	# |---------------|
	# | EVENT METHODS |
	# |---------------|

	# closeEvent()
	# Triggered when the client window is closed, via
	# any method 
	def closeEvent(self, event):
		self.app.quit()
