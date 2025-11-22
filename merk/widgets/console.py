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
from .. import config
from .. import styles
from .. import render

class Window(QMainWindow):

	def closeEvent(self, event):

		if self.force_close:
			# Make sure the MDI window is closed
			self.parent.closeSubWindow(self.subwindow_id)
			self.parent.readme_window = None

			event.accept()
			self.close()
		else:
			event.ignore()
			self.parent.hideSubWindow(self.subwindow_id)
			self.parent.MDI.activateNextSubWindow()
			return

	def __init__(self,parent,plugin,title=None):
		super(Window, self).__init__(parent)
	
		self.parent = parent
		self.plugin = plugin
		self.title = title
		self.force_close = False

		self.style = styles.loadDefault()
		self.log = []

		self.window_type = PLUGIN_CONSOLE
		self.subwindow_id = str(uuid.uuid4())
		self.name = f"{self.plugin.NAME} {self.plugin.VERSION}"

		if self.title==None:
			self.setWindowTitle(f"{self.plugin.NAME} {self.plugin.VERSION}")
		else:
			self.setWindowTitle(f"{self.title}")

		if self.plugin._icon!=None:
			self.setWindowIcon(QIcon(self.plugin._icon))
		else:
			self.setWindowIcon(QIcon(PLUGIN_ICON))

		self.chat = QTextBrowser(self)
		self.chat.anchorClicked.connect(self.linkClicked)
		self.chat.setReadOnly(True)

		self.applyStyle()

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.chat)
		self.layout.setContentsMargins(1,1,1,1)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(self.layout)
		self.setCentralWidget(self.centralWidget)

	def linkClicked(self,url):
		if url.host():
			# It's an internet link, so open it
			# in the default browser
			sb = self.chat.verticalScrollBar()
			og_value = sb.value()

			QDesktopServices.openUrl(url)
			self.chat.setSource(QUrl())
			sb.setValue(og_value)

	def writeText(self,message):
		try:
			if type(message)==type(str()):
				self.chat.append(message)
				self.log.append(message)
			else:
				t = render.render_message(message,self.style,None,True)
				self.chat.append(t)
				self.log.append(message)

			self.moveChatToBottom(True)
		except:
			pass

	def moveChatToBottom(self,force=False):
		if force:
			sb = self.chat.verticalScrollBar()
			sb.setValue(sb.maximum())
			self.chat.ensureCursorVisible()

			self.chat.moveCursor(QTextCursor.End)

		fm = QFontMetrics(self.chat.font())
		fheight = fm.height() * 1.5
		sb = self.chat.verticalScrollBar()
		is_at_bottom = False
		if sb.value()>=sb.maximum()-fheight: is_at_bottom = True

		if is_at_bottom:
			sb.setValue(sb.maximum())
			self.chat.ensureCursorVisible()

			self.chat.moveCursor(QTextCursor.End)

	def applyStyle(self,filename=None):
		
		# Apply style background and forground colors
		background,foreground = styles.parseBackgroundAndForegroundColor(self.style["all"])

		self.chat.setStyleSheet(self.generateStylesheet('QTextBrowser',foreground,background))

		self.rerenderChatLog()

	def generateStylesheet(self,obj,fore,back):
		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def rerenderChatLog(self):

		self.chat.clear()
		for line in self.log:
			t = render.render_message(line,self.style,None,True)
			self.chat.append(t)

		self.chat.moveCursor(QTextCursor.End)
