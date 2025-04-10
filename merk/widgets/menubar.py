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
from .. import config
from .text_separator import textSeparatorLabel,textSeparator

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

	def __init__(self,normal_style,hover_style,parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

		self.normal_style = normal_style
		self.hover_style = hover_style

		self.timer = QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.clicked.emit)
		super().clicked.connect(self.checkDoubleClick)

	@pyqtSlot()
	def checkDoubleClick(self):
		if self.timer.isActive():
			self.doubleClicked.emit()
			self.timer.stop()
		else:
			self.timer.start(250)

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			self.setStyleSheet(self.hover_style)
			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet(self.normal_style)
		return False

class wIconMenuButton(QPushButton):
	doubleClicked = pyqtSignal()
	clicked = pyqtSignal()

	def __init__(self,icon,normal_style,hover_style,parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

		self.setIcon(QIcon(icon))

		self.normal_style = normal_style
		self.hover_style = hover_style

		self.timer = QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.clicked.emit)
		super().clicked.connect(self.checkDoubleClick)

	@pyqtSlot()
	def checkDoubleClick(self):
		if self.timer.isActive():
			self.doubleClicked.emit()
			self.timer.stop()
		else:
			self.timer.start(250)

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			self.setStyleSheet(self.hover_style)
			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet(self.normal_style)
		return False

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
			entry = QAction(QIcon(CHECKED_ICON),"Can float", self)
		else:
			entry = QAction(QIcon(UNCHECKED_ICON),"Can float", self)
		entry.triggered.connect(self.float)
		menu.addAction(entry)

		self.justifyMenu = QMenu("Alignment")
		self.justifyMenu.setIcon(QIcon(JUSTIFY_ICON))

		if config.MENUBAR_JUSTIFY=='left':
			entry = QAction(QIcon(ROUND_CHECKED_ICON),"Left",self)
		else:
			entry = QAction(QIcon(ROUND_UNCHECKED_ICON),"Left",self)
		entry.triggered.connect(lambda state,u="left": self.setJustify(u))
		self.justifyMenu.addAction(entry)

		if config.MENUBAR_JUSTIFY=='center':
			entry = QAction(QIcon(ROUND_CHECKED_ICON),"Center",self)
		else:
			entry = QAction(QIcon(ROUND_UNCHECKED_ICON),"Center",self)
		entry.triggered.connect(lambda state,u="center": self.setJustify(u))
		self.justifyMenu.addAction(entry)

		if config.MENUBAR_JUSTIFY=='right':
			entry = QAction(QIcon(ROUND_CHECKED_ICON),"Right",self)
		else:
			entry = QAction(QIcon(ROUND_UNCHECKED_ICON),"Right",self)
		entry.triggered.connect(lambda state,u="right": self.setJustify(u))
		self.justifyMenu.addAction(entry)
	
		menu.addMenu(self.justifyMenu)

		menu.exec_(self.mapToGlobal(event.pos()))

	def setJustify(self,justify):
		config.MENUBAR_JUSTIFY = justify
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildMenu()

	def float(self):
		if config.MENUBAR_CAN_FLOAT:
			config.MENUBAR_CAN_FLOAT = False
		else:
			config.MENUBAR_CAN_FLOAT = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildMenu()

class Windowbar(QToolBar):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.parent = parent

	def contextMenuEvent(self, event):

		if config.WINDOWBAR_MENU==False: return

		menu = QMenu(self)

		e = textSeparator(self,"Windowbar Settings")
		menu.addAction(e)

		if config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST:
			entry = QAction(QIcon(CHECKED_ICON),"Show active first", self)
		else:
			entry = QAction(QIcon(UNCHECKED_ICON),"Show active first", self)
		entry.triggered.connect(self.first)
		menu.addAction(entry)

		if config.WINDOWBAR_CAN_FLOAT:
			entry = QAction(QIcon(CHECKED_ICON),"Can float", self)
		else:
			entry = QAction(QIcon(UNCHECKED_ICON),"Can float", self)
		entry.triggered.connect(self.float)
		menu.addAction(entry)
		
		if config.WINDOWBAR_SHOW_ICONS:
			entry = QAction(QIcon(CHECKED_ICON),"Show icons", self)
		else:
			entry = QAction(QIcon(UNCHECKED_ICON),"Show icons", self)
		entry.triggered.connect(self.icons)
		menu.addAction(entry)
		
		if config.WINDOWBAR_INCLUDE_SERVERS:
			entry = QAction(QIcon(CHECKED_ICON),"Server windows", self)
		else:
			entry = QAction(QIcon(UNCHECKED_ICON),"Server windows", self)
		entry.triggered.connect(self.servers)
		menu.addAction(entry)

		if config.WINDOWBAR_INCLUDE_EDITORS:
			entry = QAction(QIcon(CHECKED_ICON),"Editor windows", self)
		else:
			entry = QAction(QIcon(UNCHECKED_ICON),"Editor windows", self)
		entry.triggered.connect(self.editors)
		menu.addAction(entry)

		if config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED:
			entry = QAction(QIcon(CHECKED_ICON),"Doubleclick to maximize", self)
		else:
			entry = QAction(QIcon(UNCHECKED_ICON),"Doubleclick to maximize", self)
		entry.triggered.connect(self.doubleclick)
		menu.addAction(entry)

		self.justifyMenu = QMenu("Alignment")
		self.justifyMenu.setIcon(QIcon(JUSTIFY_ICON))

		if config.WINDOWBAR_JUSTIFY=='left':
			entry = QAction(QIcon(ROUND_CHECKED_ICON),"Left",self)
		else:
			entry = QAction(QIcon(ROUND_UNCHECKED_ICON),"Left",self)
		entry.triggered.connect(lambda state,u="left": self.setJustify(u))
		self.justifyMenu.addAction(entry)

		if config.WINDOWBAR_JUSTIFY=='center':
			entry = QAction(QIcon(ROUND_CHECKED_ICON),"Center",self)
		else:
			entry = QAction(QIcon(ROUND_UNCHECKED_ICON),"Center",self)
		entry.triggered.connect(lambda state,u="center": self.setJustify(u))
		self.justifyMenu.addAction(entry)

		if config.WINDOWBAR_JUSTIFY=='right':
			entry = QAction(QIcon(ROUND_CHECKED_ICON),"Right",self)
		else:
			entry = QAction(QIcon(ROUND_UNCHECKED_ICON),"Right",self)
		entry.triggered.connect(lambda state,u="right": self.setJustify(u))
		self.justifyMenu.addAction(entry)
	
		menu.addMenu(self.justifyMenu)

		menu.exec_(self.mapToGlobal(event.pos()))

	def setJustify(self,justify):
		config.WINDOWBAR_JUSTIFY = justify
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildWindowbar()

	def first(self):
		if config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST:
			config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST = False
		else:
			config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildWindowbar()

	def float(self):
		if config.WINDOWBAR_CAN_FLOAT:
			config.WINDOWBAR_CAN_FLOAT = False
		else:
			config.WINDOWBAR_CAN_FLOAT = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildWindowbar()

	def doubleclick(self):
		if config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED:
			config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED = False
		else:
			config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildWindowbar()

	def editors(self):
		if config.WINDOWBAR_INCLUDE_EDITORS:
			config.WINDOWBAR_INCLUDE_EDITORS = False
		else:
			config.WINDOWBAR_INCLUDE_EDITORS = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildWindowbar()

	def servers(self):
		if config.WINDOWBAR_INCLUDE_SERVERS:
			config.WINDOWBAR_INCLUDE_SERVERS = False
		else:
			config.WINDOWBAR_INCLUDE_SERVERS = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildWindowbar()
		
	def icons(self):
		if config.WINDOWBAR_SHOW_ICONS:
			config.WINDOWBAR_SHOW_ICONS = False
		else:
			config.WINDOWBAR_SHOW_ICONS = True
		config.save_settings(config.CONFIG_FILE)
		self.parent.buildWindowbar()

