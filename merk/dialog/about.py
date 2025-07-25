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

from ..resources import *
from .. import widgets

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

		self.patrons_tab = QWidget()
		self.tabs.addTab(self.patrons_tab, "Patrons")

		logo = QLabel()
		pixmap = QPixmap(SPLASH_LOGO)
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

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

		icons_credit = QLabel(f"<small><b>Icons by <a href=\"https://material.io/resources/icons/\">Google</a>, <a href=\"https://github.com/elementary/icons/\">elementaryOS</a>, and <a href=\"https://github.com/madmaxms/iconpack-obsidian\">Obsidian</a></small></b>")
		icons_credit.setAlignment(Qt.AlignCenter)
		icons_credit.setOpenExternalLinks(True)

		font_credit = QLabel(f"<small><b>Default font by <a href=\"http://www.carrois.com/\">Carrois Apostrophe</a> (<a href=\"https://bboxtype.com/typefaces/FiraSans/\">Fira Mono</a>)</small></b>")
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

			upx_credit = QLabel(f"<b><small><a href=\"https://upx.github.io/\">UPX</a> by M. Oberhumer, L. Molnar & J. Reiser</small></b>")
			upx_credit.setAlignment(Qt.AlignCenter)
			upx_credit.setOpenExternalLinks(True)

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

		me_credit = QLabel(f"<small><b>Created and written by <a href=\"https://github.com/danhetrick\">Dan Hetrick</a></b></small>")
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
		qtCred.addWidget(QLabel("<center><small><b><a href=\"https://www.qt.io/\">Qt</a> " + str(QT_VERSION_STR) +"</b></small></center>"))
		qtCred.addWidget(QLabel("<center><small><b><a href=\"https://www.riverbankcomputing.com/software/pyqt/\">PyQt</a> " + str(PYQT_VERSION_STR) +"</b></small></center>"))

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
			creditsLayout.addWidget(upx_credit)
			creditsLayout.addWidget(pi_credit)
		creditsBox.setLayout(creditsLayout)

		okButton = QPushButton("Ok")
		okButton.clicked.connect(self.close)

		app_description = QLabel("<b>Free and Open Source IRC Client</b>")
		app_description.setAlignment(Qt.AlignCenter)
		app_version = QLabel("<big><b>Version "+APPLICATION_VERSION+"</b></big>")
		app_version.setAlignment(Qt.AlignCenter)
		app_repository = QLabel(f"<big><b><a href=\"{APPLICATION_SOURCE}\">Source Code Repository</a></b></big>")
		app_repository.setAlignment(Qt.AlignCenter)
		app_repository.setOpenExternalLinks(True)

		app_donations = QLabel(f"<big><b><a href=\"https://www.gofundme.com/f/keep-dans-opensource-projects-alive\">Donate To {APPLICATION_NAME}</a></b></big>")
		app_donations.setAlignment(Qt.AlignCenter)
		app_donations.setOpenExternalLinks(True)

		pyinstaller_no_version = QLabel("<center><small><b>Running with <a href=\"https://pyinstaller.org/\">PyInstaller</a></b></small></center>")
		pyinstaller_no_version.setOpenExternalLinks(True)

		aboutLayout = QVBoxLayout()
		aboutLayout.addStretch()
		aboutLayout.addWidget(logo)
		aboutLayout.addWidget(app_version)
		aboutLayout.addWidget(app_description)
		aboutLayout.addWidget(app_repository)
		aboutLayout.addWidget(app_donations)
		aboutLayout.addWidget(gnu_credit)
		aboutLayout.addWidget(platform_credit)
		if is_running_from_pyinstaller():
			version = get_pyinstaller_version()
			if version != None:
				pyinstaller_w_version = QLabel("<center><small><b>Running with <a href=\"https://pyinstaller.org/\">PyInstaller</a> " + version +"</b></small></center>")
				pyinstaller_w_version.setOpenExternalLinks(True)
				aboutLayout.addWidget(pyinstaller_w_version)
			else:
				aboutLayout.addWidget(pyinstaller_no_version)
		aboutLayout.addStretch()

		self.about_tab.setLayout(aboutLayout)

		credLayout = QVBoxLayout()
		credLayout.addStretch()
		credLayout.addLayout(logoBar)
		credLayout.addStretch()
		credLayout.addWidget(creditsBox)
		credLayout.addWidget(me_credit)
		credLayout.addStretch()
		
		self.credits_tab.setLayout(credLayout)

		patron_list = QLabel(f"""
			<small>Ilmari Lauhakangas, Boris, Michael, Jim Kost,<br>
			       Brian, Harry Oxnard, Vincent
			</small>
			""")
		patron_list.setAlignment(Qt.AlignJustify)
		patron_list.setOpenExternalLinks(True)

		patron_description = QLabel(f"""
			<small>These are the wonderful humans that help keep<br>
			    <b>{APPLICATION_NAME}</b> alive. Thank you for helping me keep IRC<br>
			    alive in the 21st century! If you want your<br>
			    name here, <b><a href=\"https://www.gofundme.com/f/keep-dans-opensource-projects-alive\">donate $50 or more today!</a></b></small><br>
			""")
		patron_description.setAlignment(Qt.AlignJustify)
		patron_description.setOpenExternalLinks(True)

		patDescLayout = QHBoxLayout()
		patDescLayout.addStretch()
		patDescLayout.addWidget(patron_description)
		patDescLayout.addStretch()

		patronLayout = QVBoxLayout()
		patronLayout.addLayout(patDescLayout)
		patronLayout.addWidget(widgets.textSeparatorLabel(self,"<b>patrons</b>"))
		patronLayout.addWidget(patron_list)
		patronLayout.addStretch()

		self.patrons_tab.setLayout(patronLayout)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.tabs)
		finalLayout.addWidget(okButton)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())
