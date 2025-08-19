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
from .. import config
from .text_separator import textSeparatorLabel,textSeparator

import emoji

toolbar_button_style = '''
	QPushButton {
		border: 0px;
		color: $FOREGROUND;
	}
	QPushButton::menu-indicator{width:0px;}
	QPushButton::open{
		background-color: $BACKGROUND;
		color: $FOREGROUND;
		font: bold;
	}
'''

toolbar_button_style_hover = '''
	QPushButton {
		border: 0px;
		background-color: $BACKGROUND;
		color: $FOREGROUND;
		font: bold;
	}
	QPushButton::menu-indicator{width:0px;}
	QPushButton::open{
		background-color: $HIGH;
		color: $LOW;
		font: bold;
	}
'''

toolbar_menu_style = '''
	QMenu {
		margin: 2px;
	}
	QMenu::item:selected {
		background-color: $HIGH;
		color: $LOW;
	}
	QMenu::item {
		background-color: transparent;
		color: $FOREGROUND;
	}
	QMenu::item:disabled {
		background-color: transparent;
		color: grey;
	}
'''

def generate_menu_toolbar(self):

	toolbar = QToolBar(self)

	# Match menu colors to the host's desktop palette
	mbcolor = self.palette().color(QPalette.Window).name()
	mfcolor = self.palette().color(QPalette.WindowText).name()
	mhigh = self.palette().color(QPalette.Highlight).name()
	mlow = self.palette().color(QPalette.HighlightedText).name()

	global toolbar_button_style
	toolbar_button_style = toolbar_button_style.replace('$FOREGROUND',mfcolor)
	toolbar_button_style = toolbar_button_style.replace('$BACKGROUND',mbcolor)
	toolbar_button_style = toolbar_button_style.replace('$LOW',mlow)
	toolbar_button_style = toolbar_button_style.replace('$HIGH',mhigh)

	global toolbar_button_style_hover
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$FOREGROUND',mfcolor)
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$BACKGROUND',mbcolor)
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$LOW',mlow)
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$HIGH',mhigh)

	global toolbar_menu_style
	toolbar_menu_style = toolbar_menu_style.replace('$FOREGROUND',mfcolor)
	toolbar_menu_style = toolbar_menu_style.replace('$BACKGROUND',mbcolor)
	toolbar_menu_style = toolbar_menu_style.replace('$LOW',mlow)
	toolbar_menu_style = toolbar_menu_style.replace('$HIGH',mhigh)

	toolbar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
	toolbar.setStyleSheet(''' QToolBar { spacing: 8px; } ''')

	f = toolbar.font()
	fm = QFontMetrics(f)
	fheight = fm.height()
		
	toolbar.setFixedHeight(fheight+8)

	return toolbar

def add_toolbar_menu(toolbar,name,menu):

	menu.setStyleSheet(toolbar_menu_style)

	toolMenuButton = MenuButton(
			toolbar_button_style,
			toolbar_button_style_hover,
			" "+name+" "
			)

	toolMenuButton.setStyleSheet(toolbar_button_style)
	
	toolMenuButton.setMenu(menu)
	toolbar.addWidget(toolMenuButton)

def get_icon_toolbar_button(icon,name):

	toolMenuButton = IconMenuButton(
			icon,
			toolbar_button_style,
			toolbar_button_style_hover,
			" "+name+" "
			)

	toolMenuButton.setStyleSheet(toolbar_button_style)
	
	return toolMenuButton

def get_icon_only_toolbar_button(icon):

	toolMenuButton = wIconMenuButton(
			icon,
			toolbar_button_style,
			toolbar_button_style_hover
			)

	toolMenuButton.setStyleSheet(toolbar_button_style)
	
	return toolMenuButton

def get_toolbar_button(name):

	toolMenuButton = MenuButton(
			toolbar_button_style,
			toolbar_button_style_hover,
			" "+name+" "
			)

	toolMenuButton.setStyleSheet(toolbar_button_style)
	
	return toolMenuButton

def add_toolbar_spacer(toolbar):
	toolbar.addWidget(QLabel(' '))

def add_toolbar_stretch(toolbar):
	s = QWidget()
	s.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
	toolbar.addWidget(s)

def add_toolbar_image(toolbar,icon):

	f = toolbar.font()
	f.setBold(True)

	toolMenuButton = QPushButton()
	toolMenuButton.setIcon(QIcon(icon))

	toolMenuButton.setStyleSheet("border: 0px;")

	toolbar.addWidget(toolMenuButton)

	return toolMenuButton

class MenuButton(QPushButton):

	def __init__(self,normal_style,hover_style,parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

		self.normal_style = normal_style
		self.hover_style = hover_style

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			self.setStyleSheet(self.hover_style)
			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet(self.normal_style)
		return False

class IconMenuButton(QPushButton):

	def __init__(self,icon,normal_style,hover_style,parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

		self.setIcon(QIcon(icon))

		self.normal_style = normal_style
		self.hover_style = hover_style

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			self.setStyleSheet(self.hover_style)
			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet(self.normal_style)
		return False

def get_icon_windowbar_button(icon,name):

	toolMenuButton = wIconMenuButton(
			icon,
			toolbar_button_style,
			toolbar_button_style_hover,
			" "+name+" "
			)

	toolMenuButton.setStyleSheet(toolbar_button_style)
	
	return toolMenuButton

def get_windowbar_button(name):

	toolMenuButton = wMenuButton(
			toolbar_button_style,
			toolbar_button_style_hover,
			" "+name+" "
			)

	toolMenuButton.setStyleSheet(toolbar_button_style)
	
	return toolMenuButton

class wMenuButton(QPushButton):
	doubleClicked = pyqtSignal()
	clicked = pyqtSignal()

	def setWindow(self,window):
		self.window = window.widget()

	def __init__(self,normal_style,hover_style,parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

		self.window = None

		self.normal_style = normal_style
		self.hover_style = hover_style

		self.timer = QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.clicked.emit)
		super().clicked.connect(self.checkDoubleClick)

		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.show_context_menu)

	def show_context_menu(self,position):

		if not config.WINDOWBAR_ENTRY_MENU: return

		menu = QMenu(self)

		if self.window.window_type==SERVER_WINDOW or self.window.window_type==CHANNEL_WINDOW or self.window.window_type==PRIVATE_WINDOW:
			if config.ENABLE_STYLE_EDITOR:
				if not config.FORCE_DEFAULT_STYLE:
					entry = QAction(QIcon(STYLE_ICON),"Edit text style",self)
					entry.triggered.connect(self.window.pressedStyleButton)
					menu.addAction(entry)
		
		if self.window.window_type==SERVER_WINDOW:

			self.contextNick = QAction(QIcon(PRIVATE_ICON),"Change nickname",self)
			self.contextNick.triggered.connect(self.window.changeNick)
			menu.addAction(self.contextNick)

			self.contextJoin = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
			self.contextJoin.triggered.connect(self.window.joinChannel)
			menu.addAction(self.contextJoin)

			if config.SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS:
				self.contextList = QAction(QIcon(LIST_ICON),"Server channel list",self)
				self.contextList.triggered.connect(self.window.showChannelList)
				menu.addAction(self.contextList)

			if config.SCRIPTING_ENGINE_ENABLED:
				hostid = self.window.client.server+":"+str(self.window.client.port)
				entry = QAction(QIcon(EDIT_ICON),"Edit connection script",self)
				entry.triggered.connect(lambda state,h=hostid: self.window.parent.newEditorWindowConnect(h))
				menu.addAction(entry)

			menu.addSeparator()

			entry = QAction(QIcon(CLOSE_ICON),"Disconnect from server",self)
			entry.triggered.connect(self.window.disconnect)
			menu.addAction(entry)

			if not self.window.client.registered:
				self.contextNick.setEnabled(False)
				self.contextJoin.setEnabled(False)
				self.contextList.setEnabled(False)

		if self.window.window_type==CHANNEL_WINDOW or self.window.window_type==PRIVATE_WINDOW:

			if config.WINDOWBAR_SHOW_UNREAD_MESSAGES:
				if self.window.parent.has_unread_messages(self.window.client,self.window.name):
					entry = QAction(QIcon(HIDE_ICON),"Clear unread messages",self)
					entry.triggered.connect(lambda state,i=self.window.client,h=self.window.name: self.window.parent.remove_unread_message(i,h))
					menu.addAction(entry)

			entry = QAction(QIcon(CLEAR_ICON),"Clear chat",self)
			entry.triggered.connect(self.window.clearChat)
			menu.addAction(entry)

			entry = QAction(QIcon(LOG_ICON),"Save log to file",self)
			entry.triggered.connect(self.window.menuSaveLogs)
			menu.addAction(entry)

		if self.window.window_type==CHANNEL_WINDOW:

			menu.addSeparator()

			entry = QAction(QIcon(CHANNEL_ICON),"Leave channel",self)
			if config.ENABLE_EMOJI_SHORTCODES:
				msg = emoji.emojize(config.DEFAULT_QUIT_MESSAGE,language=config.EMOJI_LANGUAGE)
			else:
				msg = config.DEFAULT_QUIT_MESSAGE
			entry.triggered.connect(lambda state,u=self.window.name,w=msg: self.window.client.leave(u,w))
			menu.addAction(entry)

		if self.window.window_type==LIST_WINDOW:

			entry = QAction(QIcon(REFRESH_ICON),"Refresh channel list",self)
			entry.triggered.connect(lambda state,h='LIST': self.window.client.sendLine(h))
			menu.addAction(entry)

		if self.window.window_type!=CHANNEL_WINDOW and self.window.window_type!=SERVER_WINDOW:

			menu.addSeparator()

			entry = QAction(QIcon(CLOSE_ICON),"Close window",self)
			entry.triggered.connect(self.window.close)
			menu.addAction(entry)

		menu.exec_(self.mapToGlobal(position))

	@pyqtSlot()
	def checkDoubleClick(self):
		if self.timer.isActive():
			self.doubleClicked.emit()
			self.timer.stop()
		else:
			self.timer.start(250)

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			if config.WINDOWBAR_HOVER_EFFECT:
				self.setStyleSheet(self.hover_style)
			else:
				self.setStyleSheet(self.normal_style)
			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet(self.normal_style)
		return False

	def pulse(self):
		self.effect = QGraphicsOpacityEffect(self)
		self.setGraphicsEffect(self.effect)

		self.animation = QPropertyAnimation(self.effect, b"opacity")
		self.animation.setDuration(config.WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH)
		self.animation.setStartValue(1.0) # Fully visible
		self.animation.setEndValue(0.2)   # Nearly transparent
		self.animation.setEasingCurve(QEasingCurve.InOutQuad) # Smooth in/out transition
		self.animation.setDirection(QAbstractAnimation.Forward) # Start with fade out
		self.animation.setLoopCount(-1) # Loop indefinitely

		# Start the animation
		self.animation.start()

class wIconMenuButton(QPushButton):
	doubleClicked = pyqtSignal()
	clicked = pyqtSignal()

	def setWindow(self,window):
		self.window = window.widget()

	def __init__(self,icon,normal_style,hover_style,parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

		self.window = None

		self.setIcon(QIcon(icon))

		self.normal_style = normal_style
		self.hover_style = hover_style

		self.timer = QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.clicked.emit)
		super().clicked.connect(self.checkDoubleClick)

		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.show_context_menu)

	def show_context_menu(self,position):

		if not config.WINDOWBAR_ENTRY_MENU: return

		menu = QMenu(self)

		if self.window.window_type==SERVER_WINDOW or self.window.window_type==CHANNEL_WINDOW or self.window.window_type==PRIVATE_WINDOW:
			if config.ENABLE_STYLE_EDITOR:
				if not config.FORCE_DEFAULT_STYLE:
					entry = QAction(QIcon(STYLE_ICON),"Edit text style",self)
					entry.triggered.connect(self.window.pressedStyleButton)
					menu.addAction(entry)
		
		if self.window.window_type==SERVER_WINDOW:

			self.contextNick = QAction(QIcon(PRIVATE_ICON),"Change nickname",self)
			self.contextNick.triggered.connect(self.window.changeNick)
			menu.addAction(self.contextNick)

			self.contextJoin = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
			self.contextJoin.triggered.connect(self.window.joinChannel)
			menu.addAction(self.contextJoin)

			if config.SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS:
				self.contextList = QAction(QIcon(LIST_ICON),"Server channel list",self)
				self.contextList.triggered.connect(self.window.showChannelList)
				menu.addAction(self.contextList)

			if config.SCRIPTING_ENGINE_ENABLED:
				hostid = self.window.client.server+":"+str(self.window.client.port)
				entry = QAction(QIcon(EDIT_ICON),"Edit connection script",self)
				entry.triggered.connect(lambda state,h=hostid: self.window.parent.newEditorWindowConnect(h))
				menu.addAction(entry)

			menu.addSeparator()

			entry = QAction(QIcon(CLOSE_ICON),"Disconnect from server",self)
			entry.triggered.connect(self.window.disconnect)
			menu.addAction(entry)

			if not self.window.client.registered:
				self.contextNick.setEnabled(False)
				self.contextJoin.setEnabled(False)
				self.contextList.setEnabled(False)

		if self.window.window_type==CHANNEL_WINDOW or self.window.window_type==PRIVATE_WINDOW:

			if config.WINDOWBAR_SHOW_UNREAD_MESSAGES:
				if self.window.parent.has_unread_messages(self.window.client,self.window.name):
					entry = QAction(QIcon(HIDE_ICON),"Clear unread messages",self)
					entry.triggered.connect(lambda state,i=self.window.client,h=self.window.name: self.window.parent.remove_unread_message(i,h))
					menu.addAction(entry)

			entry = QAction(QIcon(CLEAR_ICON),"Clear chat",self)
			entry.triggered.connect(self.window.clearChat)
			menu.addAction(entry)

			entry = QAction(QIcon(LOG_ICON),"Save log to file",self)
			entry.triggered.connect(self.window.menuSaveLogs)
			menu.addAction(entry)

		if self.window.window_type==CHANNEL_WINDOW:

			menu.addSeparator()

			entry = QAction(QIcon(CHANNEL_ICON),"Leave channel",self)
			if config.ENABLE_EMOJI_SHORTCODES:
				msg = emoji.emojize(config.DEFAULT_QUIT_MESSAGE,language=config.EMOJI_LANGUAGE)
			else:
				msg = config.DEFAULT_QUIT_MESSAGE
			entry.triggered.connect(lambda state,u=self.window.name,w=msg: self.window.client.leave(u,w))
			menu.addAction(entry)

		if self.window.window_type==LIST_WINDOW:

			entry = QAction(QIcon(REFRESH_ICON),"Refresh channel list",self)
			entry.triggered.connect(lambda state,h='LIST': self.window.client.sendLine(h))
			menu.addAction(entry)

		if self.window.window_type!=CHANNEL_WINDOW and self.window.window_type!=SERVER_WINDOW:

			menu.addSeparator()

			entry = QAction(QIcon(CLOSE_ICON),"Close window",self)
			entry.triggered.connect(self.window.close)
			menu.addAction(entry)

		menu.exec_(self.mapToGlobal(position))

	@pyqtSlot()
	def checkDoubleClick(self):
		if self.timer.isActive():
			self.doubleClicked.emit()
			self.timer.stop()
		else:
			self.timer.start(250)

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			if config.WINDOWBAR_HOVER_EFFECT:
				self.setStyleSheet(self.hover_style)
			else:
				self.setStyleSheet(self.normal_style)
			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet(self.normal_style)
		return False

	def pulse(self):
		self.effect = QGraphicsOpacityEffect(self)
		self.setGraphicsEffect(self.effect)

		self.animation = QPropertyAnimation(self.effect, b"opacity")
		self.animation.setDuration(config.WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH)
		self.animation.setStartValue(1.0) # Fully visible
		self.animation.setEndValue(0.2)   # Nearly transparent
		self.animation.setEasingCurve(QEasingCurve.InOutQuad) # Smooth in/out transition
		self.animation.setDirection(QAbstractAnimation.Forward) # Start with fade out
		self.animation.setLoopCount(-1) # Loop indefinitely

		# Start the animation
		self.animation.start()

def generate_window_toolbar(self):

	toolbar = Windowbar(self)

	# Match menu colors to the host's desktop palette
	mbcolor = self.palette().color(QPalette.Window).name()
	mfcolor = self.palette().color(QPalette.WindowText).name()
	mhigh = self.palette().color(QPalette.Highlight).name()
	mlow = self.palette().color(QPalette.HighlightedText).name()

	global toolbar_button_style
	toolbar_button_style = toolbar_button_style.replace('$FOREGROUND',mfcolor)
	toolbar_button_style = toolbar_button_style.replace('$BACKGROUND',mbcolor)
	toolbar_button_style = toolbar_button_style.replace('$LOW',mlow)
	toolbar_button_style = toolbar_button_style.replace('$HIGH',mhigh)

	global toolbar_button_style_hover
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$FOREGROUND',mfcolor)
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$BACKGROUND',mbcolor)
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$LOW',mlow)
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$HIGH',mhigh)

	global toolbar_menu_style
	toolbar_menu_style = toolbar_menu_style.replace('$FOREGROUND',mfcolor)
	toolbar_menu_style = toolbar_menu_style.replace('$BACKGROUND',mbcolor)
	toolbar_menu_style = toolbar_menu_style.replace('$LOW',mlow)
	toolbar_menu_style = toolbar_menu_style.replace('$HIGH',mhigh)

	toolbar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
	toolbar.setStyleSheet(''' QToolBar { spacing: 8px; } ''')

	f = toolbar.font()
	fm = QFontMetrics(f)
	fheight = fm.height()
		
	toolbar.setFixedHeight(fheight+8)

	return toolbar

def generate_menubar(self):

	toolbar = Menubar(self)

	# Match menu colors to the host's desktop palette
	mbcolor = self.palette().color(QPalette.Window).name()
	mfcolor = self.palette().color(QPalette.WindowText).name()
	mhigh = self.palette().color(QPalette.Highlight).name()
	mlow = self.palette().color(QPalette.HighlightedText).name()

	global toolbar_button_style
	toolbar_button_style = toolbar_button_style.replace('$FOREGROUND',mfcolor)
	toolbar_button_style = toolbar_button_style.replace('$BACKGROUND',mbcolor)
	toolbar_button_style = toolbar_button_style.replace('$LOW',mlow)
	toolbar_button_style = toolbar_button_style.replace('$HIGH',mhigh)

	global toolbar_button_style_hover
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$FOREGROUND',mfcolor)
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$BACKGROUND',mbcolor)
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$LOW',mlow)
	toolbar_button_style_hover = toolbar_button_style_hover.replace('$HIGH',mhigh)

	global toolbar_menu_style
	toolbar_menu_style = toolbar_menu_style.replace('$FOREGROUND',mfcolor)
	toolbar_menu_style = toolbar_menu_style.replace('$BACKGROUND',mbcolor)
	toolbar_menu_style = toolbar_menu_style.replace('$LOW',mlow)
	toolbar_menu_style = toolbar_menu_style.replace('$HIGH',mhigh)

	toolbar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
	toolbar.setStyleSheet(''' QToolBar { spacing: 8px; } ''')

	f = toolbar.font()
	fm = QFontMetrics(f)
	fheight = fm.height()
		
	toolbar.setFixedHeight(fheight+8)

	return toolbar

class Menubar(QToolBar):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.parent = parent

	def contextMenuEvent(self, event):

		if config.MENUBAR_MENU==False: return

		menu = QMenu(self)

		e = textSeparator(self,"Menubar Settings")
		menu.addAction(e)

		if config.MENUBAR_CAN_FLOAT:
			entry = QAction(QIcon(self.parent.checked_icon),"Movable", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Movable", self)
		entry.triggered.connect(self.float)
		menu.addAction(entry)

		self.justifyMenu = QMenu("Alignment")
		self.justifyMenu.setIcon(QIcon(JUSTIFY_ICON))

		if config.MENUBAR_JUSTIFY=='left':
			entry = QAction(QIcon(self.parent.round_checked_icon),"Left",self)
		else:
			entry = QAction(QIcon(self.parent.round_unchecked_icon),"Left",self)
		entry.triggered.connect(lambda state,u="left": self.setJustify(u))
		self.justifyMenu.addAction(entry)

		if config.MENUBAR_JUSTIFY=='center':
			entry = QAction(QIcon(self.parent.round_checked_icon),"Center",self)
		else:
			entry = QAction(QIcon(self.parent.round_unchecked_icon),"Center",self)
		entry.triggered.connect(lambda state,u="center": self.setJustify(u))
		self.justifyMenu.addAction(entry)

		if config.MENUBAR_JUSTIFY=='right':
			entry = QAction(QIcon(self.parent.round_checked_icon),"Right",self)
		else:
			entry = QAction(QIcon(self.parent.round_unchecked_icon),"Right",self)
		entry.triggered.connect(lambda state,u="right": self.setJustify(u))
		self.justifyMenu.addAction(entry)
	
		menu.addMenu(self.justifyMenu)

		menu.exec_(self.mapToGlobal(event.pos()))

	def setJustify(self,justify):
		w = self.parent.MDI.activeSubWindow()
		config.MENUBAR_JUSTIFY = justify
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildMenu()
		self.parent.initWindowbar()
		if len(self.parent.MDI.subWindowList())>0:
			self.parent.MDI.setActiveSubWindow(w)

	def float(self):
		w = self.parent.MDI.activeSubWindow()
		if config.MENUBAR_CAN_FLOAT:
			config.MENUBAR_CAN_FLOAT = False
		else:
			config.MENUBAR_CAN_FLOAT = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildMenu()
		self.parent.initWindowbar()
		if len(self.parent.MDI.subWindowList())>0:
			self.parent.MDI.setActiveSubWindow(w)

class Windowbar(QToolBar):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.parent = parent

	def contextMenuEvent(self, event):

		if config.WINDOWBAR_MENU==False: return

		menu = QMenu(self)

		e = textSeparator(self,"Windowbar Settings")
		menu.addAction(e)

		if config.WINDOWBAR_CAN_FLOAT:
			entry = QAction(QIcon(self.parent.checked_icon),"Movable", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Movable", self)
		entry.triggered.connect(self.float)
		menu.addAction(entry)

		if config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST:
			entry = QAction(QIcon(self.parent.checked_icon),"Show active first", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Show active first", self)
		entry.triggered.connect(self.first)
		menu.addAction(entry)

		if config.WINDOWBAR_UNDERLINE_ACTIVE_WINDOW:
			entry = QAction(QIcon(self.parent.checked_icon),"Underline active window", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Underline active window", self)
		entry.triggered.connect(self.underline)
		menu.addAction(entry)
		
		if config.WINDOWBAR_SHOW_ICONS:
			entry = QAction(QIcon(self.parent.checked_icon),"Show icons", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Show icons", self)
		entry.triggered.connect(self.icons)
		menu.addAction(entry)

		if config.WINDOWBAR_INCLUDE_CHANNELS:
			entry = QAction(QIcon(self.parent.checked_icon),"Channel windows", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Channel windows", self)
		entry.triggered.connect(self.channels)
		menu.addAction(entry)

		if config.WINDOWBAR_INCLUDE_PRIVATE:
			entry = QAction(QIcon(self.parent.checked_icon),"Private windows", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Private windows", self)
		entry.triggered.connect(self.privates)
		menu.addAction(entry)
		
		if config.WINDOWBAR_INCLUDE_SERVERS:
			entry = QAction(QIcon(self.parent.checked_icon),"Server windows", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Server windows", self)
		entry.triggered.connect(self.servers)
		menu.addAction(entry)

		if config.WINDOWBAR_INCLUDE_EDITORS:
			entry = QAction(QIcon(self.parent.checked_icon),"Editor windows", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Editor windows", self)
		entry.triggered.connect(self.editors)
		menu.addAction(entry)

		if config.WINDOWBAR_INCLUDE_LIST:
			entry = QAction(QIcon(self.parent.checked_icon),"Channel lists", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Channel lists", self)
		entry.triggered.connect(self.list_window)
		menu.addAction(entry)

		if config.WINDOWBAR_INCLUDE_MANAGER:
			entry = QAction(QIcon(self.parent.checked_icon),"Log manager", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Log manager", self)
		entry.triggered.connect(self.list_manager)
		menu.addAction(entry)

		if config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED:
			entry = QAction(QIcon(self.parent.checked_icon),"Double click to maximize", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Double click to maximize", self)
		entry.triggered.connect(self.doubleclick)
		menu.addAction(entry)

		if config.WINDOWBAR_SHOW_UNREAD_MESSAGES:
			entry = QAction(QIcon(self.parent.checked_icon),"Show unread messages", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Show unread messages", self)
		entry.triggered.connect(self.showUnread)
		menu.addAction(entry)

		if config.WINDOWBAR_ENTRY_MENU:
			entry = QAction(QIcon(self.parent.checked_icon),"Entry context menu", self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Entry context menu", self)
		entry.triggered.connect(self.showMenu)
		menu.addAction(entry)

		self.justifyMenu = QMenu("Alignment")
		self.justifyMenu.setIcon(QIcon(JUSTIFY_ICON))

		if config.WINDOWBAR_JUSTIFY=='left':
			entry = QAction(QIcon(self.parent.round_checked_icon),"Left",self)
		else:
			entry = QAction(QIcon(self.parent.round_unchecked_icon),"Left",self)
		entry.triggered.connect(lambda state,u="left": self.setJustify(u))
		self.justifyMenu.addAction(entry)

		if config.WINDOWBAR_JUSTIFY=='center':
			entry = QAction(QIcon(self.parent.round_checked_icon),"Center",self)
		else:
			entry = QAction(QIcon(self.parent.round_unchecked_icon),"Center",self)
		entry.triggered.connect(lambda state,u="center": self.setJustify(u))
		self.justifyMenu.addAction(entry)

		if config.WINDOWBAR_JUSTIFY=='right':
			entry = QAction(QIcon(self.parent.round_checked_icon),"Right",self)
		else:
			entry = QAction(QIcon(self.parent.round_unchecked_icon),"Right",self)
		entry.triggered.connect(lambda state,u="right": self.setJustify(u))
		self.justifyMenu.addAction(entry)
	
		menu.addMenu(self.justifyMenu)

		menu.addSeparator()

		entry1 = QAction(QIcon(CASCADE_ICON),"Cascade windows",self)
		entry1.triggered.connect(self.parent.MDI.cascadeSubWindows)
		menu.addAction(entry1)

		entry2 = QAction(QIcon(TILE_ICON),"Tile windows",self)
		entry2.triggered.connect(self.parent.MDI.tileSubWindows)
		menu.addAction(entry2)

		menu.exec_(self.mapToGlobal(event.pos()))

	def setJustify(self,justify):
		w = self.parent.MDI.activeSubWindow()
		config.WINDOWBAR_JUSTIFY = justify
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def first(self):
		w = self.parent.MDI.activeSubWindow()
		if config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST:
			config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST = False
		else:
			config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def underline(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_UNDERLINE_ACTIVE_WINDOW:
			config.WINDOWBAR_UNDERLINE_ACTIVE_WINDOW = False
		else:
			config.WINDOWBAR_UNDERLINE_ACTIVE_WINDOW = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def float(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_CAN_FLOAT:
			config.WINDOWBAR_CAN_FLOAT = False
		else:
			config.WINDOWBAR_CAN_FLOAT = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def showUnread(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_SHOW_UNREAD_MESSAGES:
			config.WINDOWBAR_SHOW_UNREAD_MESSAGES = False
		else:
			config.WINDOWBAR_SHOW_UNREAD_MESSAGES = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def showMenu(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_ENTRY_MENU:
			config.WINDOWBAR_ENTRY_MENU = False
		else:
			config.WINDOWBAR_ENTRY_MENU = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def doubleclick(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED:
			config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED = False
		else:
			config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def editors(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_INCLUDE_EDITORS:
			config.WINDOWBAR_INCLUDE_EDITORS = False
		else:
			config.WINDOWBAR_INCLUDE_EDITORS = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def list_manager(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_INCLUDE_MANAGER:
			config.WINDOWBAR_INCLUDE_MANAGER = False
		else:
			config.WINDOWBAR_INCLUDE_MANAGER = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def list_window(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_INCLUDE_LIST:
			config.WINDOWBAR_INCLUDE_LIST = False
		else:
			config.WINDOWBAR_INCLUDE_LIST = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def servers(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_INCLUDE_SERVERS:
			config.WINDOWBAR_INCLUDE_SERVERS = False
		else:
			config.WINDOWBAR_INCLUDE_SERVERS = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)
		
	def icons(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_SHOW_ICONS:
			config.WINDOWBAR_SHOW_ICONS = False
		else:
			config.WINDOWBAR_SHOW_ICONS = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def channels(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_INCLUDE_CHANNELS:
			config.WINDOWBAR_INCLUDE_CHANNELS = False
		else:
			config.WINDOWBAR_INCLUDE_CHANNELS = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

	def privates(self):
		w = self.parent.MDI.activeSubWindow()
		if config.WINDOWBAR_INCLUDE_PRIVATE:
			config.WINDOWBAR_INCLUDE_PRIVATE = False
		else:
			config.WINDOWBAR_INCLUDE_PRIVATE = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.initWindowbar()
		self.parent.MDI.setActiveSubWindow(w)

