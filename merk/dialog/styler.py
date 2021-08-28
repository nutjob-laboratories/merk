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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from ..resources import *
from .. import widgets
from .. import styles

class Dialog(QDialog):

	@staticmethod
	def get_style_information(client,chat,parent=None):
		dialog = Dialog(client,chat,parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		self.style['system'] = self.system_style.exportQss()
		self.style['action'] = self.action_style.exportQss()
		self.style['error'] = self.error_style.exportQss()
		self.style['hyperlink'] = self.link_style.exportQss()
		self.style['self'] = self.self_style.exportQss()
		self.style['username'] = self.user_style.exportQss()
		self.style['notice'] = self.notice_style.exportQss()
		self.style['all'] = self.all_style.exportQss()
		self.style['server'] = self.server_style.exportQss()

		return self.style

	def saveStyle(self):

		self.style['system'] = self.system_style.exportQss()
		self.style['action'] = self.action_style.exportQss()
		self.style['error'] = self.error_style.exportQss()
		self.style['hyperlink'] = self.link_style.exportQss()
		self.style['self'] = self.self_style.exportQss()
		self.style['username'] = self.user_style.exportQss()
		self.style['notice'] = self.notice_style.exportQss()
		self.style['all'] = self.all_style.exportQss()
		self.style['server'] = self.server_style.exportQss()
		
		# saveStyle(client,channel,style,is_server_window=False):
		if self.chat.window_type==SERVER_WINDOW:
			styles.saveStyle(self.client,self.chat.name,self.style,True)
		else:
			styles.saveStyle(self.client,self.chat.name,self.style,False)

	def __init__(self,client,chat,parent=None):
		super(Dialog,self).__init__(parent)

		self.client = client
		self.chat = chat
		self.parent = parent

		self.style = self.chat.style

		self.setWindowTitle("Edit text styles")
		self.setWindowIcon(QIcon(STYLE_ICON))

		bgcolor,fgcolor = styles.parseBackgroundAndForegroundColor(self.style["all"])

		self.system_style = widgets.TextStyler('system','This is a system message',self.style['system'],True,False,bgcolor,self)
		self.link_style = widgets.TextStyler('hyperlink','This is a link',self.style['hyperlink'],True,True,bgcolor,self)
		self.action_style = widgets.TextStyler('action','This is a CTCP Action message',self.style['action'],True,False,bgcolor,self)
		self.error_style = widgets.TextStyler('error','This is an error message',self.style['error'],True,False,bgcolor,self)
		self.notice_style = widgets.TextStyler('notice','Notice nicknames',self.style['notice'],True,False,bgcolor,self)
		self.self_style = widgets.TextStyler('self','Your nickname',self.style['self'],True,False,bgcolor,self)
		self.user_style = widgets.TextStyler('username','Other nicknames',self.style['username'],True,False,bgcolor,self)
		self.server_style = widgets.TextStyler('server','This is a server message',self.style['server'],True,False,bgcolor,self)

		self.all_style = widgets.AllStyler('all',self.style['all'],self)

		styleLayout = QVBoxLayout()
		styleLayout.addWidget(self.all_style)
		styleLayout.addWidget(self.system_style)
		styleLayout.addWidget(self.link_style)
		styleLayout.addWidget(self.action_style)
		styleLayout.addWidget(self.error_style)
		styleLayout.addWidget(self.notice_style)
		styleLayout.addWidget(self.self_style)
		styleLayout.addWidget(self.user_style)
		styleLayout.addWidget(self.server_style)
		styleLayout.addStretch()

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Apply")

		entry = QPushButton("Save")
		entry.clicked.connect(self.saveStyle)

		buttonLayout = QHBoxLayout()
		buttonLayout.addStretch()
		buttonLayout.addWidget(entry)
		buttonLayout.addWidget(buttons)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(styleLayout)
		finalLayout.addLayout(buttonLayout)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)
