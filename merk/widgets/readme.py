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

import uuid
import os

from ..resources import *

class Window(QMainWindow):

	def closeEvent(self, event):

		# Make sure the MDI window is closed
		self.parent.closeSubWindow(self.subwindow_id)
		self.parent.readme_window = None

		event.accept()
		self.close()

	def __init__(self,parent=None):
		super(Window, self).__init__(parent)
	
		self.parent = parent

		self.window_type = README_WINDOW
		self.subwindow_id = str(uuid.uuid4())

		self.setWindowTitle("README")

		filename = resource_path("./merk/resources/README.html")

		f = open(filename,"r",encoding='utf-8')
		readme = f.read()
		f.close()

		self.README = QTextBrowser(self)
		self.README.anchorClicked.connect(self.linkClicked)
		self.README.setReadOnly(True)

		self.README.setHtml(readme)

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.README)
		self.layout.setContentsMargins(1,1,1,1)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(self.layout)
		self.setCentralWidget(self.centralWidget)

	def linkClicked(self,url):
		if url.host():
			# It's an internet link, so open it
			# in the default browser
			sb = self.README.verticalScrollBar()
			og_value = sb.value()

			QDesktopServices.openUrl(url)
			self.README.setSource(QUrl())
			sb.setValue(og_value)