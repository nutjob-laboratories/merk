#
# ███╗   ███╗██████╗ ██████╗ ██╗  ██╗
# ████╗ ████║╚═══╗██╗██╔══██╗██║ ██╔╝
# ██╔████╔██║███████║██████╔╝█████╔╝
# ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗
# ██║ ╚═╝ ██║ █████╔╝██║  ██║██║  ██╗
# ╚═╝     ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
# Copyright (C) 2025  Daniel Hetrick
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

import platform
import twisted
import pkg_resources

from ..resources import *

def get_pyinstaller_version():
	try:
		return pkg_resources.get_distribution('pyinstaller').version
	except pkg_resources.DistributionNotFound:
		return None

class Dialog(QDialog):

	closed = pyqtSignal()

	def closeEvent(self, event):
		self.closed.emit()

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle(APPLICATION_NAME)
		self.setWindowIcon(QIcon(APPLICATION_ICON))

		BOLD_FONT = self.font()
		BOLD_FONT.setBold(True)

		self.tabs = QTabWidget()

		self.tabs.setFont(BOLD_FONT)

		self.tabs.setStyleSheet("""
			QTabWidget::tab-bar { alignment: center; font: bold; }
			""")

		self.about_tab = QWidget()
		self.tabs.addTab(self.about_tab, "About")

		self.credits_tab = QWidget()
		self.tabs.addTab(self.credits_tab, "Credits")

		logo = QLabel()
		pixmap = QPixmap(SPLASH_LOGO)
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

		nutjob = QLabel()
		pixmap = QPixmap(NUTJOB_LOGO)
		nutjob.setPixmap(pixmap)
		nutjob.setAlignment(Qt.AlignCenter)

		line2 = QLabel("<b>Free and Open Source IRC Client</b>")
		line2.setAlignment(Qt.AlignCenter)
		line3 = QLabel("<big><b>MERK "+APPLICATION_VERSION+"</b></big>")
		line3.setAlignment(Qt.AlignCenter)
		line4 = QLabel(f"<big><b><a href=\"https://github.com/nutjob-laboratories/merk\">Official Repository</a></b></big>")
		line4.setAlignment(Qt.AlignCenter)
		line4.setOpenExternalLinks(True)

		descriptionLayout = QVBoxLayout()
		descriptionLayout.addWidget(line3)
		descriptionLayout.addWidget(line2)
		descriptionLayout.addWidget(line4)

		qt_logo = QLabel()
		pixmap = QPixmap(QT_ICON)
		qt_logo.setPixmap(pixmap)
		qt_logo.setAlignment(Qt.AlignCenter)

		python_logo = QLabel()
		pixmap = QPixmap(PYTHON_ICON)
		python_logo.setPixmap(pixmap)
		python_logo.setAlignment(Qt.AlignCenter)

		twisted_logo = QLabel()
		pixmap = QPixmap(TWISTED_BUTTON_ICON)
		twisted_logo.setPixmap(pixmap)
		twisted_logo.setAlignment(Qt.AlignCenter)

		if is_running_from_pyinstaller():
			pyi_logo = QLabel()
			pixmap = QPixmap(PYINSTALLER_ICON)
			pyi_logo.setPixmap(pixmap)
			pyi_logo.setAlignment(Qt.AlignCenter)

		titleLayout = QVBoxLayout()
		titleLayout.addWidget(logo)
		titleLayout.addLayout(descriptionLayout)

		# https://github.com/elementary/icons/

		icons_credit = QLabel(f"<small><b>Icons by <a href=\"https://material.io/resources/icons/\">Google</a>, <a href=\"https://github.com/elementary/icons/\">elementaryOS</a>, and <a href=\"https://github.com/madmaxms/iconpack-obsidian\">Obsidian</a></small></b>")
		icons_credit.setAlignment(Qt.AlignCenter)
		icons_credit.setOpenExternalLinks(True)

		font_credit = QLabel(f"<small><b>Default font by <a href=\"http://www.carrois.com/\">Carrois Apostrophe</small></a> (<a href=\"https://bboxtype.com/typefaces/FiraSans/\">Fira Mono</a>)</small></b>")
		font_credit.setAlignment(Qt.AlignCenter)
		font_credit.setOpenExternalLinks(True)


		spellcheck_credit = QLabel(f"<b><small><a href=\"https://github.com/barrust/pyspellchecker\">pyspellchecker</a> by <a href=\"mailto:barrust@gmail.com\">Tyler Barrus</small></a></b>")
		spellcheck_credit.setAlignment(Qt.AlignCenter)
		spellcheck_credit.setOpenExternalLinks(True)

		emoji_credit = QLabel(f"<b><small><a href=\"https://github.com/carpedm20/emoji\">emoji</a> by <a href=\"http://carpedm20.github.io/about/\">Taehoon Kim</a> and <a href=\"http://twitter.com/geowurster/\">Kevin Wurster</a></small></b>")
		emoji_credit.setAlignment(Qt.AlignCenter)
		emoji_credit.setOpenExternalLinks(True)

		gnu_credit = QLabel(f"<big><b><a href=\"https://www.gnu.org/licenses/gpl-3.0.en.html\">Gnu General Public License 3.0</a></b></big>")
		gnu_credit.setAlignment(Qt.AlignCenter)
		gnu_credit.setOpenExternalLinks(True)

		qr_credit = QLabel(f"<b><small><a href=\"https://github.com/twisted/qt5reactor\">qt5reactor</a> by Twisted Matrix Labs</small></b>")
		qr_credit.setAlignment(Qt.AlignCenter)
		qr_credit.setOpenExternalLinks(True)

		if is_running_from_pyinstaller():
			pi_credit = QLabel(f"<b><small><a href=\"https://pyinstaller.org/\">PyInstaller</a> by David Cortesi</small></b>")
			pi_credit.setAlignment(Qt.AlignCenter)
			pi_credit.setOpenExternalLinks(True)

		platform_credit = QLabel(f"<small><b>Running on "+ platform.system().strip() + " " + platform.release().strip() +"</b></small>")
		platform_credit.setAlignment(Qt.AlignCenter)

		# QT_VERSION_STR

		tv = str(twisted.version)
		tv = tv.replace('[','',1)
		tv = tv.replace(']','',1)
		tv = tv.strip()

		tv = tv.split(',')[1].strip()
		tv = tv.replace('version ','',1)

		nutjob_credit = QLabel(f"<big><b><a href=\"https://github.com/nutjob-laboratories\">NUTJOB</a> <a href=\"https://github.com/nutjob-laboratories\">LABORATORIES</a></b></big>")
		nutjob_credit.setAlignment(Qt.AlignCenter)
		nutjob_credit.setOpenExternalLinks(True)

		me_credit = QLabel(f"<small>Created and written by <a href=\"https://github.com/danhetrick\">Dan Hetrick</a></small>")
		me_credit.setAlignment(Qt.AlignCenter)
		me_credit.setOpenExternalLinks(True)

		pyCred = QVBoxLayout()
		pyCred.addWidget(python_logo)
		pyCred.addWidget(QLabel("<small><b><a href=\"https://python.org\">Python</a> " + platform.python_version().strip() +"</b></small>"))

		twCred = QVBoxLayout()
		twCred.addWidget(twisted_logo)
		twCred.addWidget(QLabel("<small><b><a href=\"https://twistedmatrix.com/\">Twisted</a> " + tv +"</b></small>"))

		qtCred = QVBoxLayout()
		qtCred.addWidget(qt_logo)
		qtCred.addWidget(QLabel("<small><b><a href=\"https://www.qt.io/\">Qt</a> " + str(QT_VERSION_STR) +"</b></small>"))

		if is_running_from_pyinstaller():
			version = get_pyinstaller_version()
			if version != None:
				pyiCredit = QVBoxLayout()
				pyiCredit.addWidget(pyi_logo)
				pyiCredit.addWidget(QLabel("<center><small><b><a href=\"https://pyinstaller.org/\">PyInstaller</a> " + version +"</b></small></center>"))

		logoBar = QHBoxLayout()
		logoBar.addStretch()
		logoBar.addLayout(pyCred)
		logoBar.addStretch()
		logoBar.addLayout(qtCred)
		logoBar.addStretch()
		logoBar.addLayout(twCred)
		logoBar.addStretch()

		creditsBox = QGroupBox()
		creditsBox.setAlignment(Qt.AlignHCenter)

		creditsLayout = QVBoxLayout()
		creditsLayout.addWidget(icons_credit)
		creditsLayout.addWidget(font_credit)
		creditsLayout.addWidget(spellcheck_credit)
		creditsLayout.addWidget(emoji_credit)
		creditsLayout.addWidget(qr_credit)
		if is_running_from_pyinstaller():
			creditsLayout.addWidget(pi_credit)
		creditsBox.setLayout(creditsLayout)

		okButton = QPushButton("Ok")
		okButton.clicked.connect(self.close)

		aboutLayout = QVBoxLayout()
		aboutLayout.addStretch()
		aboutLayout.addLayout(titleLayout)
		aboutLayout.addWidget(gnu_credit)
		aboutLayout.addWidget(platform_credit)
		aboutLayout.addStretch()
		aboutLayout.addLayout(logoBar)
		if is_running_from_pyinstaller():
			aboutLayout.addLayout(pyiCredit)
		aboutLayout.addStretch()

		self.about_tab.setLayout(aboutLayout)

		credLayout = QVBoxLayout()
		credLayout.addStretch()
		credLayout.addWidget(nutjob)
		credLayout.addWidget(nutjob_credit)
		credLayout.addWidget(me_credit)
		credLayout.addStretch()
		credLayout.addWidget(creditsBox)
		credLayout.addStretch()
		
		self.credits_tab.setLayout(credLayout)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.tabs)
		finalLayout.addWidget(okButton)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())
