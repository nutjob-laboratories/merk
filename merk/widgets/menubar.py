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

def get_toolbar_button(icon,name):

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