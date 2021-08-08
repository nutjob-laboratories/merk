from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

app = QApplication([])

import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

from merk.main import Merk
from merk.resources import *

if __name__ == '__main__':

	app = QApplication([])

	# Load in fonts from the resources file
	fid = QFontDatabase.addApplicationFont(BUNDLED_FONT)
	for f in OTHER_BUNDLED_FONTS:
		QFontDatabase.addApplicationFont(f)

	# Set the default font
	_fontstr = QFontDatabase.applicationFontFamilies(fid)[0]
	font = QFont(_fontstr,BUNDLED_FONT_SIZE)

	app.setFont(font)

	GUI = Merk(
			app,		# Application
			None,		# Parent
		)

	GUI.show()

	reactor.run()
