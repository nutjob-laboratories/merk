#
# ███╗   ███╗██████╗ ██████╗ ██╗  ██╗
# ████╗ ████║╚═══╗██╗██╔══██╗██║ ██╔╝
# ██╔████╔██║███████║██████╔╝█████╔╝
# ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗
# ██║ ╚═╝ ██║ █████╔╝██║  ██║██║  ██╗
# ╚═╝     ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
# Copyright (C) 2026  Daniel Hetrick
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

from ..resources import *

class Window(QMainWindow):

	def closeEvent(self, event):

		# Make sure the MDI window is closed
		self.parent.closeSubWindow(self.subwindow_id)
		self.parent.log_dump_window = None

		event.accept()
		self.close()

	def __init__(self,parent=None,source=None,title=None):
		super(Window, self).__init__(parent)
	
		self.parent = parent
		self.source = source
		self.title = title

		self.window_type = LOGDUMP_WINDOW
		self.subwindow_id = str(uuid.uuid4())
		self.name = "LOGDUMP"

		self.setWindowTitle("Log Dump")

		if self.title!=None:
			self.name = self.title
			self.setWindowTitle(f"Server log for {self.title}")

		self.log = QTextBrowser(self)
		self.log.anchorClicked.connect(self.linkClicked)
		self.log.setReadOnly(True)

		self.log.setHtml(self.source)

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.log)
		self.layout.setContentsMargins(1,1,1,1)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(self.layout)
		self.setCentralWidget(self.centralWidget)

	def linkClicked(self,url):
		if url.host():
			# It's an internet link, so open it
			# in the default browser
			sb = self.log.verticalScrollBar()
			og_value = sb.value()

			QDesktopServices.openUrl(url)
			self.log.setSource(QUrl())
			sb.setValue(og_value)
