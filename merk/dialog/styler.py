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

from ..resources import *
from .. import widgets
from .. import styles
from .. import render
from .. import config

class Dialog(QDialog):

	@staticmethod
	def get_style_information(client,chat,parent=None,simple=False,default=False):
		dialog = Dialog(client,chat,parent,simple,default)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def generateStylesheet(self,obj,fore,back):
		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def return_info(self):

		self.style['system'] = self.system_style.exportQss()
		self.style['action'] = self.action_style.exportQss()
		self.style['error'] = self.error_style.exportQss()
		self.style['hyperlink'] = self.link_style.exportQss()
		self.style['self'] = self.self_style.exportQss()
		self.style['username'] = self.user_style.exportQss()
		self.style['notice'] = self.notice_style.exportQss()
		self.style['server'] = self.server_style.exportQss()

		if self.default:
			styles.saveDefault(self.style)
			self.parent.reApplyStyle()
		else:
			self.saveStyle()

		return self.style

	def saveStyle(self):

		self.style['system'] = self.system_style.exportQss()
		self.style['action'] = self.action_style.exportQss()
		self.style['error'] = self.error_style.exportQss()
		self.style['hyperlink'] = self.link_style.exportQss()
		self.style['self'] = self.self_style.exportQss()
		self.style['username'] = self.user_style.exportQss()
		self.style['notice'] = self.notice_style.exportQss()
		self.style['server'] = self.server_style.exportQss()

		if self.default:
			styles.saveDefault(self.style)
		else:
			if self.wchat.window_type==SERVER_WINDOW:
				styles.saveStyle(self.client,self.wchat.name,self.style,True)
			else:
				styles.saveStyle(self.client,self.wchat.name,self.style,False)

	def qssChanged(self,data):
		style_name = data[0]
		qss = data[1]

		self.style[style_name] = qss

		self.chat.clear()

		for line in self.messages:
			t = render.render_message(line,self.style)
			self.chat.append(t)

	def syntaxChanged(self,data):
		name = data[0]

		if name=="fore":
			color = data[1]
			self.fgcolor = color
		elif name=="back":
			color = data[1]
			self.bgcolor = color

		gcode = f'color: {self.fgcolor};'
		gcode = gcode + f' background-color: {self.bgcolor};'

		self.style["all"] = gcode

		self.chat.setStyleSheet(self.generateStylesheet('QTextBrowser',self.fgcolor,self.bgcolor))
		self.userlist.setStyleSheet(self.generateStylesheet('QListWidget',self.fgcolor,self.bgcolor))

	def saveAsStyle(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save style as...","","Style File (*.style);;All Files (*)", options=options)
		if fileName:
			efl = len("style")+1
			if fileName[-efl:].lower()!=f".style": fileName = fileName+f".style"

			self.style['system'] = self.system_style.exportQss()
			self.style['action'] = self.action_style.exportQss()
			self.style['error'] = self.error_style.exportQss()
			self.style['hyperlink'] = self.link_style.exportQss()
			self.style['self'] = self.self_style.exportQss()
			self.style['username'] = self.user_style.exportQss()
			self.style['notice'] = self.notice_style.exportQss()
			self.style['server'] = self.server_style.exportQss()

			styles.write_style_file(self.style,fileName)

	def loadStyle(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Select Style File", styles.STYLE_DIRECTORY,"Style File (*.style);;All Files (*)", options=options)
		if fileName:
			self.style = styles.read_style_file(fileName)

			self.bgcolor,self.fgcolor = styles.parseBackgroundAndForegroundColor(self.style["all"])
			self.system_style.setQss(self.style['system'])
			self.link_style.setQss(self.style['hyperlink'])
			self.action_style.setQss(self.style['action'])
			self.error_style.setQss(self.style['error'])
			self.notice_style.setQss(self.style['notice'])
			self.self_style.setQss(self.style['self'])
			self.user_style.setQss(self.style['username'])
			self.server_style.setQss(self.style['server'])

			self.fore.applyColor(self.fgcolor)
			self.back.applyColor(self.bgcolor)

			self.chat.setStyleSheet(self.generateStylesheet('QTextBrowser',self.fgcolor,self.bgcolor))
			self.userlist.setStyleSheet(self.generateStylesheet('QListWidget',self.fgcolor,self.bgcolor))

			self.chat.clear()

			for line in self.messages:
				t = render.render_message(line,self.style)
				self.chat.append(t)

	def loadDefault(self):
		self.style = styles.read_style_file('',DEFAULT_STYLE)

		self.bgcolor,self.fgcolor = styles.parseBackgroundAndForegroundColor(self.style["all"])
		self.system_style.setQss(self.style['system'])
		self.link_style.setQss(self.style['hyperlink'])
		self.action_style.setQss(self.style['action'])
		self.error_style.setQss(self.style['error'])
		self.notice_style.setQss(self.style['notice'])
		self.self_style.setQss(self.style['self'])
		self.user_style.setQss(self.style['username'])
		self.server_style.setQss(self.style['server'])

		self.fore.applyColor(self.fgcolor)
		self.back.applyColor(self.bgcolor)

		self.chat.setStyleSheet(self.generateStylesheet('QTextBrowser',self.fgcolor,self.bgcolor))

		self.chat.clear()

		for line in self.messages:
			t = render.render_message(line,self.style)
			self.chat.append(t)

	def __init__(self,client,chat,parent=None,simple=False,default=False):
		super(Dialog,self).__init__(parent)

		self.client = client
		self.wchat = chat
		self.parent = parent
		self.default = default
		self.simple = simple

		if default:
			self.style = styles.loadDefault()
			self.setWindowTitle("Edit default text style")
		else:
			self.style = self.wchat.style
			self.setWindowTitle("Edit text style for "+self.wchat.name)

		self.setWindowIcon(QIcon(STYLE_ICON))

		self.bgcolor,self.fgcolor = styles.parseBackgroundAndForegroundColor(self.style["all"])

		self.system_style = widgets.MiniStyler('system', "System messages    ",self.style['system'],False,self)
		self.link_style = widgets.MiniStyler('hyperlink','Hyperlinks         ',self.style['hyperlink'],True,self)
		self.action_style = widgets.MiniStyler('action', 'CTCP Action message',self.style['action'],False,self)
		self.error_style = widgets.MiniStyler('error',   'Error message      ',self.style['error'],False,self)
		self.notice_style = widgets.MiniStyler('notice', 'Notice nicknames   ',self.style['notice'],False,self)
		self.self_style = widgets.MiniStyler('self',     'Your nickname      ',self.style['self'],False,self)
		self.user_style = widgets.MiniStyler('username', 'Other nicknames    ',self.style['username'],False,self)
		self.server_style = widgets.MiniStyler('server', 'Server message     ',self.style['server'],False,self)

		self.system_style.qssChanged.connect(self.qssChanged)
		self.link_style.qssChanged.connect(self.qssChanged)
		self.action_style.qssChanged.connect(self.qssChanged)
		self.error_style.qssChanged.connect(self.qssChanged)
		self.notice_style.qssChanged.connect(self.qssChanged)
		self.self_style.qssChanged.connect(self.qssChanged)
		self.user_style.qssChanged.connect(self.qssChanged)
		self.server_style.qssChanged.connect(self.qssChanged)

		self.chat = QTextBrowser(self)
		self.chat.setFocusPolicy(Qt.NoFocus)

		self.chat.setStyleSheet(self.generateStylesheet('QTextBrowser',self.fgcolor,self.bgcolor))

		fm = QFontMetrics(self.font())
		fheight = fm.height()

		self.chat.setFixedHeight((fheight*9)+10)

		self.messages = [
			Message(SERVER_MESSAGE,'','This is a server message'),
			Message(SYSTEM_MESSAGE,'','This is a system message'),
			Message(ERROR_MESSAGE,'','This is an error message'),
			Message(NOTICE_MESSAGE,'nickname','This is a notice message'),
			Message(CHAT_MESSAGE,'other_nicks',"Here's a link: http://google.com"),
			Message(SELF_MESSAGE,'your_nick',"Here's a message without a link!"),
			Message(ACTION_MESSAGE,'nickname','sends a CTCP action message'),
		]

		for line in self.messages:
			t = render.render_message(line,self.style)
			self.chat.append(t)

		self.fore = widgets.SyntaxTextColor('fore', "Text Color",self.fgcolor,self)
		self.back = widgets.SyntaxTextColor('back', "Background Color",self.bgcolor,self)

		self.fore.syntaxChanged.connect(self.syntaxChanged)
		self.back.syntaxChanged.connect(self.syntaxChanged)

		self.userlist = QListWidget(self)
		self.userlist.setStyleSheet(self.generateStylesheet('QListWidget',self.fgcolor,self.bgcolor))
		f = self.userlist.font()
		f.setBold(True)
		self.userlist.setFont(f)

		fm = self.chat.fontMetrics()
		ulwidth = (fm.averageCharWidth() + 2) + (fm.averageCharWidth()*10)

		self.userlist.setFixedHeight((fheight*9)+10)
		self.userlist.setFixedWidth(ulwidth)

		if not config.SHOW_USERLIST:
			self.userlist.hide()

		ui = QListWidgetItem()
		if config.PLAIN_USER_LISTS:
			ui.setText('~ '+'owner')
		else:
			ui.setIcon(QIcon(OWNER_USER))
			ui.setText('owner')
		self.userlist.addItem(ui)

		ui = QListWidgetItem()
		if config.PLAIN_USER_LISTS:
			ui.setText('% '+'admin')
		else:
			ui.setIcon(QIcon(ADMIN_USER))
			ui.setText('admin')
		self.userlist.addItem(ui)

		ui = QListWidgetItem()
		if config.PLAIN_USER_LISTS:
			ui.setText('@ '+'chanop')
		else:
			ui.setIcon(QIcon(OP_USER))
			ui.setText('chanop')
		self.userlist.addItem(ui)

		ui = QListWidgetItem()
		if config.PLAIN_USER_LISTS:
			ui.setText('% '+'halfop')
		else:
			ui.setIcon(QIcon(HALFOP_USER))
			ui.setText('halfop')
		self.userlist.addItem(ui)

		ui = QListWidgetItem()
		if config.PLAIN_USER_LISTS:
			ui.setText('+ '+'voiced')
		else:
			ui.setIcon(QIcon(VOICE_USER))
			ui.setText('voiced')
		self.userlist.addItem(ui)

		ui = QListWidgetItem()
		if config.PLAIN_USER_LISTS:
			ui.setText('  '+'user1')
		else:
			ui.setIcon(QIcon(NORMAL_USER))
			ui.setText('user1')
		self.userlist.addItem(ui)

		ui = QListWidgetItem()
		if config.PLAIN_USER_LISTS:
			ui.setText('  '+'user2')
		else:
			ui.setIcon(QIcon(NORMAL_USER))
			ui.setText('user2')
		self.userlist.addItem(ui)

		self.userlist.update()

		ln1 = QHBoxLayout()
		ln1.addWidget(self.system_style)
		ln1.addWidget(self.error_style)
		ln1.setContentsMargins(1,1,1,1)

		ln2 = QHBoxLayout()
		ln2.addWidget(self.link_style)
		ln2.addWidget(self.server_style)
		ln2.setContentsMargins(1,1,1,1)

		ln3 = QHBoxLayout()
		ln3.addWidget(self.self_style)
		ln3.addWidget(self.user_style)
		ln3.setContentsMargins(1,1,1,1)

		ln4 = QHBoxLayout()
		ln4.addWidget(self.action_style)
		ln4.addWidget(self.notice_style)
		ln4.setContentsMargins(1,1,1,1)

		ln5 = QHBoxLayout()
		ln5.addStretch()
		ln5.addWidget(self.fore)
		ln5.addStretch()
		ln5.addWidget(self.back)
		ln5.addStretch()
		ln5.setContentsMargins(1,1,1,1)

		editstyleLayout = QVBoxLayout()
		editstyleLayout.addLayout(ln5)
		editstyleLayout.addLayout(ln1)
		editstyleLayout.addLayout(ln2)
		editstyleLayout.addLayout(ln3)
		editstyleLayout.addLayout(ln4)

		dispLayout = QHBoxLayout()
		if config.SHOW_USERLIST_ON_LEFT:
			dispLayout.addWidget(self.userlist)
			dispLayout.addWidget(self.chat)
		else:
			dispLayout.addWidget(self.chat)
			dispLayout.addWidget(self.userlist)
		dispLayout.setContentsMargins(CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING)
		
		styleLayout = QVBoxLayout()
		styleLayout.addLayout(dispLayout)
		styleLayout.addLayout(editstyleLayout)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Save")

		saveAsButton = QPushButton("Save as...")
		saveAsButton.clicked.connect(self.saveAsStyle)

		loadButton = QPushButton("Open style")
		loadButton.clicked.connect(self.loadStyle)

		defaultButton = QPushButton("Set default")
		defaultButton.clicked.connect(self.loadDefault)

		buttonLayout = QHBoxLayout()
		buttonLayout.addWidget(defaultButton)
		buttonLayout.addWidget(loadButton)
		buttonLayout.addWidget(saveAsButton)
		buttonLayout.addWidget(buttons)
		buttonLayout.setAlignment(Qt.AlignRight)
		buttonLayout.setContentsMargins(1,1,1,1)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(styleLayout)
		finalLayout.addLayout(buttonLayout)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())
