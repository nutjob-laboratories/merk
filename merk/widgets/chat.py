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

import re
import uuid
import fnmatch

from spellchecker import SpellChecker

from ..resources import *
from .. import config
from .. import styles
from .. import render
from ..dialog import *

class Window(QMainWindow):

	def __init__(self,name,client,window_type,app,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.client = client
		self.window_type = window_type
		self.app = app
		self.parent = parent

		self.subwindow_id = str(uuid.uuid4())

		self.channel_topic = ""		# Channel topic
		self.userlist_width = 0		# Userlist width

		self.language = config.DEFAULT_SPELLCHECK_LANGUAGE

		self.history_buffer = ['']
		self.history_buffer_pointer = 0

		self.spellcheck_enabled = True

		self.users = []
		self.nicks = []
		self.hostmasks = {}
		self.operator = False
		self.voiced = False
		self.owner = False
		self.admin = False
		self.halfop = False

		self.setWindowTitle(self.name)

		if self.window_type==CHANNEL_WINDOW:
			icon = CHANNEL_ICON
		elif self.window_type==SERVER_WINDOW:
			icon = CONSOLE_ICON
		elif self.window_type==PRIVATE_WINDOW:
			icon = PRIVATE_ICON
		self.setWindowIcon(QIcon(icon))

		f = self.parent.app.font()
		self.setFont(f)

		# For nick autocomplete
		if self.window_type==PRIVATE_WINDOW: self.nicks = [ self.name ]

		if self.window_type==CHANNEL_WINDOW:
			
			# Create topic editor
			self.topic = TopicEdit(self)
			self.topic.returnPressed.connect(self.handleTopicInput)
			self.topic.setReadOnly(True)

			# Set topic editors color to the same as the
			# window background
			col = self.parent.palette().color(QPalette.Background).name()
			self.topic.setFrame(False)
			p = self.topic.palette()
			p.setColor(QPalette.Base, QColor(col))
			self.topic.setPalette(p)

			# Create the uselist
			self.userlist = QListWidget(self)
			self.userlist.setFocusPolicy(Qt.NoFocus)
			self.userlist.itemDoubleClicked.connect(self.handleDoubleClick)
			self.userlist.installEventFilter(self)

		# Create chat display widget
		self.chat = QTextBrowser(self)
		self.chat.setFocusPolicy(Qt.NoFocus)
		self.chat.anchorClicked.connect(self.linkClicked)

		# Create text input widget
		self.input = SpellTextEdit(self)
		self.input.returnPressed.connect(self.handleUserInput)
		self.input.keyUp.connect(self.keyPressUp)
		self.input.keyDown.connect(self.keyPressDown)

		# Text input widget should only be one line
		fm = self.input.fontMetrics()
		self.input.setFixedHeight(fm.height()+9)
		self.input.setWordWrapMode(QTextOption.NoWrap)
		self.input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		# Set input language for spell checker
		self.input.changeLanguage(self.language)

		# Nickname display
		self.nick_display = QLabel("<b>"+self.client.nickname+"</b>")
		self.mode_display = QLabel("")

		self.nick_display.installEventFilter(self)

		if len(self.client.usermodes)>0:
			self.mode_display.setText("+"+self.client.usermodes)

		# Hide the nickname display on server windows
		if self.window_type==SERVER_WINDOW: self.nick_display.hide()
		if self.window_type==SERVER_WINDOW: self.mode_display.hide()

		# Spellcheck Button
		self.spellcheckMenu = QMenu("Spellcheck")

		self.languageEnabled = QAction(QIcon(TOGGLE_ON_ICON),"Enabled",self)
		self.languageEnabled.triggered.connect(self.setSpellcheckEnabled)
		self.spellcheckMenu.addAction(self.languageEnabled)

		self.spellcheckMenu.addSeparator()

		self.languageEnglish = QAction(QIcon(ROUND_UNCHECKED_ICON),"English",self)
		self.languageEnglish.triggered.connect(lambda state,u="en": self.menuSetLanguage(u))
		self.spellcheckMenu.addAction(self.languageEnglish)

		self.languageFrench = QAction(QIcon(ROUND_UNCHECKED_ICON),"Française",self)
		self.languageFrench.triggered.connect(lambda state,u="fr": self.menuSetLanguage(u))
		self.spellcheckMenu.addAction(self.languageFrench)

		self.languageSpanish = QAction(QIcon(ROUND_UNCHECKED_ICON),"Español",self)
		self.languageSpanish.triggered.connect(lambda state,u="es": self.menuSetLanguage(u))
		self.spellcheckMenu.addAction(self.languageSpanish)

		self.languageGerman = QAction(QIcon(ROUND_UNCHECKED_ICON),"Deutsche",self)
		self.languageGerman.triggered.connect(lambda state,u="de": self.menuSetLanguage(u))
		self.spellcheckMenu.addAction(self.languageGerman)

		if self.language=="en": self.languageEnglish.setIcon(QIcon(ROUND_CHECKED_ICON))
		if self.language=="fr": self.languageFrench.setIcon(QIcon(ROUND_CHECKED_ICON))
		if self.language=="es": self.languageSpanish.setIcon(QIcon(ROUND_CHECKED_ICON))
		if self.language=="de": self.languageGerman.setIcon(QIcon(ROUND_CHECKED_ICON))

		self.spellcheckMenuButton = QPushButton(QIcon(SPELLCHECK_ICON),"")
		self.spellcheckMenuButton.setMenu(self.spellcheckMenu)
		self.spellcheckMenuButton.setIconSize(QSize(self.input.height(),self.input.height()))
		self.spellcheckMenuButton.setFixedSize(self.input.height()+5,self.input.height())
		self.spellcheckMenuButton.setStyleSheet("QPushButton::menu-indicator { image: none; }")
		self.spellcheckMenuButton.setToolTip("Spellcheck")

		if self.window_type!=SERVER_WINDOW:

			self.op_icon = QLabel(self)
			pixmap = QPixmap(OP_USER)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.op_icon.setPixmap(pixmap)

			self.voice_icon = QLabel(self)
			pixmap = QPixmap(VOICE_USER)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.voice_icon.setPixmap(pixmap)

			self.owner_icon = QLabel(self)
			pixmap = QPixmap(OWNER_USER)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.owner_icon.setPixmap(pixmap)

			self.admin_icon = QLabel(self)
			pixmap = QPixmap(ADMIN_USER)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.admin_icon.setPixmap(pixmap)

			self.halfop_icon = QLabel(self)
			pixmap = QPixmap(HALFOP_USER)
			fm = QFontMetrics(self.app.font())
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.halfop_icon.setPixmap(pixmap)

			self.op_icon.hide()
			self.voice_icon.hide()
			self.owner_icon.hide()
			self.admin_icon.hide()
			self.halfop_icon.hide()


		nickLayout = QHBoxLayout()
		if self.window_type!=SERVER_WINDOW:
			nickLayout.addWidget(self.op_icon)
			nickLayout.addWidget(self.voice_icon)
			nickLayout.addWidget(self.owner_icon)
			nickLayout.addWidget(self.admin_icon)
			nickLayout.addWidget(self.halfop_icon)
		nickLayout.addWidget(self.nick_display)
		nickLayout.addWidget(self.mode_display)

		inputLayout = QHBoxLayout()
		inputLayout.addLayout(nickLayout)
		inputLayout.addWidget(self.input)
		inputLayout.addWidget(self.spellcheckMenuButton)

		if self.window_type==CHANNEL_WINDOW:

			# Channel windows will have the chat display split with
			# the user list display
			self.horizontalSplitter = QSplitter(Qt.Horizontal)
			self.horizontalSplitter.addWidget(self.chat)
			self.horizontalSplitter.addWidget(self.userlist)
			self.horizontalSplitter.splitterMoved.connect(self.splitterResize)

			# Set the initial splitter ratio
			ulwidth = (fm.averageCharWidth() + 2) + (fm.averageCharWidth()*15)
			mwidth = self.width()-ulwidth
			self.horizontalSplitter.setSizes([mwidth,ulwidth])

			# Set the starting width of the userlist
			self.userlist.resize(ulwidth,self.height())
			self.userlist_width = ulwidth

			topicLayout = QHBoxLayout()
			topicLayout.addWidget(self.topic)

			finalLayout = QVBoxLayout()
			finalLayout.setSpacing(CHAT_WINDOW_WIDGET_SPACING)
			finalLayout.setContentsMargins(CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING)
			finalLayout.addLayout(topicLayout)
			finalLayout.addWidget(self.horizontalSplitter)
			finalLayout.addLayout(inputLayout)

		else:

			finalLayout = QVBoxLayout()
			finalLayout.setSpacing(CHAT_WINDOW_WIDGET_SPACING)
			finalLayout.setContentsMargins(CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING)
			finalLayout.addWidget(self.chat)
			finalLayout.addLayout(inputLayout)

		# Finalize the layout
		interface = QWidget()
		interface.setLayout(finalLayout)
		self.setCentralWidget(interface)

		self.input.setFocus()

		# Load and apply default style
		self.applyStyle()

	def refreshModeDisplay(self):
		if len(self.client.usermodes)==0:
			self.mode_display.setText("")
		else:
			self.mode_display.setText("<small>+"+self.client.usermodes+"</small>")
		self.updateTitle()
		
	def updateTitle(self):

		if self.window_type==CHANNEL_WINDOW:
			if self.name in self.client.channelmodes:
				if len(self.client.channelmodes[self.name])>0:
					modes = " +"+self.client.channelmodes[self.name]
				else:
					modes = ''
			else:
				modes = ''
			self.setWindowTitle(self.name+modes)
		else:
			self.setWindowTitle(self.name)

	def eventFilter(self, source, event):

		# Name click
		if (event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.nick_display):
			info = NewNickDialog(self.client.nickname,self)
			if info!=None:
				self.client.setNick(info)
				return True


		return super(Window, self).eventFilter(source, event)

	def applyStyle(self,filename=None):
		if filename == None:
			self.style = styles.loadStyle(self.client,self.name)
		else:
			s = styles.loadStyleFile(filename)
			if s:
				self.style = s
			else:
				return False

		# Apply style background and forground colors
		background,foreground = styles.parseBackgroundAndForegroundColor(self.style["all"])

		p = self.chat.palette()
		p.setColor(QPalette.Base, QColor(background))
		p.setColor(QPalette.Text, QColor(foreground))
		self.chat.setPalette(p)

		p = self.input.palette()
		p.setColor(QPalette.Base, QColor(background))
		p.setColor(QPalette.Text, QColor(foreground))
		self.input.setPalette(p)

		if self.window_type==CHANNEL_WINDOW:
			p = self.userlist.palette()
			p.setColor(QPalette.Base, QColor(background))
			p.setColor(QPalette.Text, QColor(foreground))
			self.userlist.setPalette(p)

	def writeUserlist(self,users):

		if not hasattr(self,"userlist"): return

		self.users = []
		self.operator = False
		self.voiced = False
		self.owner = False
		self.admin = False
		self.halfop = False

		self.userlist.clear()

		# Sort the user list
		owners = []
		admins = []
		ops = []
		halfops = []
		voiced = []
		normal = []

		for u in users:
			if len(u)<1: continue
			self.users.append(u)
			p = u.split("!")
			if len(p)==2:
				nickname = p[0]
				hostmask = p[1]
				self.hostmasks[nickname] = hostmask
			else:
				nickname = u
				hostmask = None

			if '@' in nickname:
				ops.append(nickname.replace('@',''))
				if nickname.replace('@','')==self.client.nickname: self.operator = True
			elif '+' in nickname:
				voiced.append(nickname.replace('+',''))
				if nickname.replace('+','')==self.client.nickname: self.voiced = True
			elif '~' in nickname:
				owners.append(nickname.replace('~',''))
				if nickname.replace('~','')==self.client.nickname: self.owner = True
			elif '&' in nickname:
				admins.append(nickname.replace('&',''))
				if nickname.replace('&','')==self.client.nickname: self.admin = True
			elif '%' in nickname:
				halfops.append(nickname.replace('%',''))
				if nickname.replace('%','')==self.client.nickname: self.halfop = True
			else:
				normal.append(nickname)

		# Store a list of the nicks in this channel
		self.nicks = owners + admins + halfops + ops + voiced + normal

		# Alphabetize
		owners.sort()
		admins.sort()
		halfops.sort()
		ops.sort()
		voiced.sort()
		normal.sort()

		# Add owners
		for u in owners:
			ui = QListWidgetItem()
			ui.setIcon(QIcon(OWNER_USER))
			ui.setText(u)

			self.userlist.addItem(ui)

		# Add admins
		for u in admins:
			ui = QListWidgetItem()
			ui.setIcon(QIcon(ADMIN_USER))
			ui.setText(u)

			self.userlist.addItem(ui)

		# Add halfops
		for u in halfops:
			ui = QListWidgetItem()
			ui.setIcon(QIcon(HALFOP_USER))
			ui.setText(u)

			self.userlist.addItem(ui)

		# Add ops
		for u in ops:
			ui = QListWidgetItem()
			ui.setIcon(QIcon(OP_USER))
			ui.setText(u)

			self.userlist.addItem(ui)

		# Add voiced
		for u in voiced:
			ui = QListWidgetItem()
			ui.setIcon(QIcon(VOICE_USER))
			ui.setText(u)

			self.userlist.addItem(ui)

		# Add normal
		for u in normal:
			ui = QListWidgetItem()
			ui.setIcon(QIcon(NORMAL_USER))
			ui.setText(u)

			self.userlist.addItem(ui)

		self.userlist.update()

		self.op_icon.hide()
		self.voice_icon.hide()
		self.owner_icon.hide()
		self.admin_icon.hide()
		self.halfop_icon.hide()

		if self.operator: self.op_icon.show()
		if self.voiced: self.voice_icon.show()
		if self.owner: self.owner_icon.show()
		if self.admin: self.admin_icon.show()
		if self.halfop: self.halfop_icon.show()

	def refreshNickDisplay(self):
		self.nick_display.setText("<b>"+self.client.nickname+"</b>")

	def writeText(self,text):

		if type(text)==type(str()):
			self.chat.append(text)
		else:
			t = render.render_message(text,self.style)
			self.chat.append(t)
		self.moveChatToBottom()

	def closeEvent(self, event):

		# Server windows are never closed unless
		# the server has been disconnected; they
		# are only hidden
		if self.window_type==SERVER_WINDOW:
			event.ignore()
			self.parent.hideSubWindow(self.subwindow_id)
			return

		# If this is a channel window, sent a part command
		if self.window_type==CHANNEL_WINDOW:
			self.client.leave(self.name,config.DEFAULT_QUIT_MESSAGE)

		# Let the parent know that this subwindow
		# has been closed by the user
		self.parent.closeSubWindow(self.subwindow_id)

	def setSpellcheckEnabled(self):
		if self.spellcheck_enabled:
			self.spellcheck_enabled = False
			self.languageEnabled.setText("Disabled")
			self.languageEnabled.setIcon(QIcon(TOGGLE_OFF_ICON))
			self.languageEnglish.setEnabled(False)
			self.languageFrench.setEnabled(False)
			self.languageSpanish.setEnabled(False)
			self.languageGerman.setEnabled(False)
		else:
			self.spellcheck_enabled = True
			self.languageEnabled.setText("Enabled")
			self.languageEnabled.setIcon(QIcon(TOGGLE_ON_ICON))
			self.languageEnglish.setEnabled(True)
			self.languageFrench.setEnabled(True)
			self.languageSpanish.setEnabled(True)
			self.languageGerman.setEnabled(True)

		# Rewrite whatever is in the input widget
		cursor = self.input.textCursor()
		user_input = self.input.text()
		self.input.setText('')
		self.input.setText(user_input)
		self.input.moveCursor(cursor.position())

	def menuSetLanguage(self,language):
		self.changeSpellcheckLanguage(language)

		self.languageEnglish.setIcon(QIcon(ROUND_UNCHECKED_ICON))
		self.languageFrench.setIcon(QIcon(ROUND_UNCHECKED_ICON))
		self.languageSpanish.setIcon(QIcon(ROUND_UNCHECKED_ICON))
		self.languageGerman.setIcon(QIcon(ROUND_UNCHECKED_ICON))

		if self.language=="en": self.languageEnglish.setIcon(QIcon(ROUND_CHECKED_ICON))
		if self.language=="fr": self.languageFrench.setIcon(QIcon(ROUND_CHECKED_ICON))
		if self.language=="es": self.languageSpanish.setIcon(QIcon(ROUND_CHECKED_ICON))
		if self.language=="de": self.languageGerman.setIcon(QIcon(ROUND_CHECKED_ICON))

	def linkClicked(self,url):
		if url.host():

			sb = self.chat.verticalScrollBar()
			og_value = sb.value()

			QDesktopServices.openUrl(url)
			self.chat.setSource(QUrl())
			sb.setValue(og_value)

	def handleUserInput(self):
		user_input = self.input.text()
		self.input.setText('')

		# ================================
		# BEGIN COMMAND HISTORY MANAGEMENT
		# ================================

		# Remove blank entries from history
		clean = []
		for c in self.history_buffer:
			if c=='': continue
			clean.append(c)
		self.history_buffer = clean

		# Insert current input into the history,
		# right at the beginning
		self.history_buffer.insert(0,user_input)

		# If history is larger than it's supposed to be,
		# remove the last entry
		if len(self.history_buffer)>config.COMMAND_HISTORY_LENGTH:
			self.history_buffer.pop()

		# "Zero" the history buffer pointer
		self.history_buffer_pointer = -1

		# Add a blank entry to the history;
		# this represents (to the user) the current
		# "blank" input
		self.history_buffer.append('')

		# Remove consecutive repeated commands
		self.history_buffer = [self.history_buffer[i] for i in range(len(self.history_buffer)) if (i==0) or self.history_buffer[i] != self.history_buffer[i-1]]

		# ==============================
		# END COMMAND HISTORY MANAGEMENT
		# ==============================

		# Pass the input (and window) to the parent
		# to process input
		if self.window_type!=SERVER_WINDOW:
			self.parent.handleUserInput(self,user_input)
		else:
			self.parent.handleConsoleInput(self,user_input)

		# Move chat display to the bottom
		self.moveChatToBottom(True)

	def changeSpellcheckLanguage(self,lang):

		# Set the new language
		self.language = lang
		self.input.changeLanguage(lang)

		# Rewrite whatever is in the input widget
		# so that it's spellchecked
		cursor = self.input.textCursor()
		user_input = self.input.text()
		self.input.setText('')
		self.input.setText(user_input)
		self.input.moveCursor(cursor.position())

	def handleTopicInput(self):
		entered_topic = self.topic.text()

		self.client.topic(self.name,entered_topic)
		self.input.setFocus()

	def setTopic(self,topic):

		if not hasattr(self,"topic"): return

		self.channel_topic = topic
		self.topic.setText(topic)
		self.topic.setCursorPosition(0)

	def handleDoubleClick(self,item):
		item.setSelected(False)
		user = item.text()
		user = user.replace('@','')
		user = user.replace('+','')

		if user!=self.client.nickname:
			self.parent.openPrivate(self.client,user)

	def keyPressDown(self):
		if len(self.history_buffer) <= 1: return
		self.history_buffer_pointer = self.history_buffer_pointer - 1
		if self.history_buffer_pointer < 0:
			self.history_buffer_pointer = len(self.history_buffer) - 1
		self.input.setText(self.history_buffer[self.history_buffer_pointer])
		self.input.moveCursor(QTextCursor.End)

	def keyPressUp(self):
		if len(self.history_buffer) <= 1: return
		self.history_buffer_pointer = self.history_buffer_pointer + 1
		if len(self.history_buffer) - 1 < self.history_buffer_pointer:
			self.history_buffer_pointer = 0
		self.input.setText(self.history_buffer[self.history_buffer_pointer])
		self.input.moveCursor(QTextCursor.End)

	def moveChatToBottom(self,force=False):

		if force:
			sb = self.chat.verticalScrollBar()
			sb.setValue(sb.maximum())
			self.chat.ensureCursorVisible()

		fm = QFontMetrics(self.chat.font())
		fheight = fm.height() * 2
		sb = self.chat.verticalScrollBar()
		is_at_bottom = False
		if sb.value()>=sb.maximum()-fheight: is_at_bottom = True

		if is_at_bottom:
			sb.setValue(sb.maximum())
			self.chat.ensureCursorVisible()

	def splitterResize(self,position,index):
		# Save the width of the userlist for the resize event
		self.userlist_width = self.userlist.width()

	def resizeEvent(self, event):

		if self.window_type==CHANNEL_WINDOW:

			# Make sure the topic displays correctly
			self.topic.refresh()
	   
			# QSplitter dynamically changes widget sizes on a resize
			# event; this makes the userlist widget get wider or less wide
			# depending on the new widget size. This code makes sure that
			# the userlist maintains the same width during resize events

			# Calculate the width of the chat display widget
			chat_width = self.width() - self.userlist_width - (CHAT_WINDOW_WIDGET_SPACING * 3)

			# Resize the userlist widget with the width value saved in
			# the splitter resize event
			self.userlist.resize(self.userlist_width,self.userlist.height())

			# Resize the chat display to compensate for the changed
			# userlist size
			self.chat.resize(chat_width,self.chat.height())

			# Move the userlist so it's along side the chat display
			self.userlist.move(chat_width + 3,self.userlist.y())

			# Move the QSplitter handle to match the new widget sizes
			self.horizontalSplitter.setSizes([self.chat.width(), self.userlist.width()])

			# Move focus back to the input widget
			self.input.setFocus()

		return super(Window, self).resizeEvent(event)

class TopicEdit(QLineEdit):
	def __init__(self, parent=None):
		super(QLineEdit, self).__init__(parent)
		self.readyToEdit = True
		self.parent = parent
		self.is_enabled = True

	def refresh(self):
		self.setText(self.parent.channel_topic)

	def setText(self,text,elide=True):
		if elide:
			metrics = QFontMetrics(self.font())
			elided  = metrics.elidedText(text, Qt.ElideRight, self.width())
			QLineEdit.setText(self,elided)
			if len(elided)!=len(text):
				self.setToolTip(text)
			else:
				self.setToolTip('')
		else:
			QLineEdit.setText(self,text)

	def mousePressEvent(self, e, Parent=None):
		super(QLineEdit, self).mousePressEvent(e) #required to deselect on 2e click
		if not self.is_enabled: return
		if self.readyToEdit:
			self.setText(self.parent.channel_topic,False)
			self.setReadOnly(False)
			self.selectAll()
			self.readyToEdit = False

	def focusOutEvent(self, e):
		super(QLineEdit, self).focusOutEvent(e) #required to remove cursor on focusOut
		self.setText(self.parent.channel_topic)

		self.deselect()
		self.readyToEdit = True
		self.setReadOnly(True)
		self.setCursorPosition(0)

class SpellTextEdit(QPlainTextEdit):

	returnPressed = pyqtSignal()
	keyUp = pyqtSignal()
	keyDown = pyqtSignal()

	def __init__(self, *args):
		QPlainTextEdit.__init__(self, *args)

		self.parent = args[0]

		self.dict = SpellChecker(language=self.parent.language,distance=1)

		self.highlighter = Highlighter(self.document())

		self.highlighter.setDict(self.dict)
		self.highlighter.setParent(self.parent)

		self.nicks = []

	def keyPressEvent(self,event):

		# BUGFIX: the user can "drag" the view "down"
		# with the mouse; this resets the widget to
		# "normal" every time the user presses a key
		# Man, I wish Qt had a rich-text-enabled QLineEdit :-(
		sb = self.verticalScrollBar()
		sb.setValue(sb.minimum())
		self.ensureCursorVisible()

		if event.key() == Qt.Key_Return:
			self.returnPressed.emit()
		elif event.key() == Qt.Key_Up:
			self.keyUp.emit()
		elif event.key() == Qt.Key_Down:
			self.keyDown.emit()
		elif event.key() == Qt.Key_Tab:
			cursor = self.textCursor()

			if self.toPlainText().strip()=='': return

			if config.AUTOCOMPLETE_COMMANDS:
				# Auto-complete commands
				cursor.select(QTextCursor.BlockUnderCursor)
				self.setTextCursor(cursor)
				if self.textCursor().hasSelection():
					text = self.textCursor().selectedText()

					self.COMMAND_LIST = self.parent.parent.command_autocomplete_data

					for c in self.COMMAND_LIST:
						cmd = c
						rep = self.COMMAND_LIST[c]

						if fnmatch.fnmatch(cmd,f"{text}*"):
							cursor.beginEditBlock()
							cursor.insertText(rep)
							cursor.endEditBlock()
							return

			if config.AUTOCOMPLETE_NICKS:
				# Auto-complete nicks
				cursor.select(QTextCursor.WordUnderCursor)
				self.setTextCursor(cursor)
				if self.textCursor().hasSelection():
					text = self.textCursor().selectedText()

					# Nicks
					chan_nicks = self.parent.nicks
					for nick in chan_nicks:
						# Skip client's nickname
						if nick==self.parent.client.nickname:
							continue
						if fnmatch.fnmatch(nick,f"{text}*"):
							cursor.beginEditBlock()
							cursor.insertText(f"{nick}")
							cursor.endEditBlock()
							return

			if config.AUTOCOMPLETE_EMOJIS:
				# Autocomplete emojis
				cursor.select(QTextCursor.WordUnderCursor)
				oldpos = cursor.position()
				cursor.select(QTextCursor.WordUnderCursor)
				newpos = cursor.selectionStart() - 1
				cursor.setPosition(newpos,QTextCursor.MoveAnchor)
				cursor.setPosition(oldpos,QTextCursor.KeepAnchor)
				self.setTextCursor(cursor)
				if self.textCursor().hasSelection():
					text = self.textCursor().selectedText()

					for c in EMOJI_AUTOCOMPLETE:

						# Case sensitive
						if fnmatch.fnmatchcase(c,f"{text}*"):
							cursor.beginEditBlock()
							cursor.insertText(c)
							cursor.endEditBlock()
							return

						# Case insensitive
						if fnmatch.fnmatch(c,f"{text}*"):
							cursor.beginEditBlock()
							cursor.insertText(c)
							cursor.endEditBlock()
							return

			cursor.movePosition(QTextCursor.End)
			self.setTextCursor(cursor)

		else:
			return super().keyPressEvent(event)

	def text(self):
		return self.toPlainText()

	def setText(self,text):
		self.setPlainText(text)

	def changeLanguage(self,lang):
		self.dict = SpellChecker(language=lang,distance=1)
		self.highlighter.setDict(self.dict)

	def mousePressEvent(self, event):
		if event.button() == Qt.RightButton:
			# Rewrite the mouse event to a left button event so the cursor is
			# moved to the location of the pointer.
			event = QMouseEvent(QEvent.MouseButtonPress, event.pos(),
				Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
		QPlainTextEdit.mousePressEvent(self, event)

	def contextMenuEvent(self, event):

		popup_menu = self.createStandardContextMenu()


		# Don't autoselect if the user has selected text
		# Don't offer spelling corrections if the user has selected text
		if self.textCursor().hasSelection():
			do_spellcheck = False
		else:
			# Select the word under the cursor.
			cursor = self.textCursor()
			cursor.select(QTextCursor.WordUnderCursor)
			self.setTextCursor(cursor)
			do_spellcheck = True
		
		counter = 0

		# Check if the selected word is misspelled and offer spelling
		# suggestions if it is.
		if self.textCursor().hasSelection():
			text = self.textCursor().selectedText()

			# Make sure that words in the custom dictionary aren't flagged as misspelled
			if not text in config.DICTIONARY:

				if self.parent.spellcheck_enabled:

					misspelled = self.dict.unknown([text])
					if len(misspelled)>0:
						
						for word in self.dict.candidates(text):
							action = SpellAction(word, popup_menu)
							action.correct.connect(self.correctWord)
							popup_menu.insertAction(popup_menu.actions()[0],action)
							counter = counter + 1
						if counter != 0:
							popup_menu.insertSeparator(popup_menu.actions()[counter])

			popup_menu.insertSeparator(popup_menu.actions()[counter])
			counter = counter + 1

		popup_menu.exec_(event.globalPos())

	def correctWord(self, word):
		'''
		Replaces the selected text with word.
		'''
		cursor = self.textCursor()
		cursor.beginEditBlock()

		cursor.removeSelectedText()
		cursor.insertText(word)

		cursor.endEditBlock()


class Highlighter(QSyntaxHighlighter):

	WORDS = u'(?iu)[\w\']+'

	def __init__(self, *args):
		QSyntaxHighlighter.__init__(self, *args)

		self.dict = None
		self.ulist = []

	def setParent(self,parent):
		self.parent = parent

	def setDict(self, dict):
		self.dict = dict

	def highlightBlock(self, text):
		if not self.dict:
			return

		format = QTextCharFormat()
		format.setUnderlineColor(Qt.red)
		format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

		for word_object in re.finditer(self.WORDS, text):

			if self.parent.spellcheck_enabled:

				misspelled = self.dict.unknown([word_object.group()])
				if len(misspelled)>0:
					# Make sure that words in the custom dictionary aren't flagged as misspelled
					if not word_object.group() in config.DICTIONARY:
						self.setFormat(word_object.start(), word_object.end() - word_object.start(), format)

class SpellAction(QAction):
	correct = pyqtSignal(str)

	def __init__(self, *args):
		QAction.__init__(self, *args)

		self.triggered.connect(lambda x: self.correct.emit(
			self.text()))