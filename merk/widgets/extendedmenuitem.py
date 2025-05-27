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

def menuHtml(icon,text,description,icon_size):
	return f'''
<table style="width: 100%" border="0" cellspacing="2" cellpadding="0">
	  <tbody>
		<tr>
		  <td style="text-align: center; vertical-align: middle;">&nbsp;<img src="{icon}" width="{icon_size}" height="{icon_size}">&nbsp;</td>
		  <td>
			<table style="width: 100%" border="0">
			  <tbody>
				<tr>
				  <td style="font-weight: bold;"><big>{text}</big></td>
				</tr>
				<tr>
				  <td style="font-style: normal; font-weight: normal;"><small>{description}</small></td>
				</tr>
			  </tbody>
			</table>
		  </td>
		</tr>
	  </tbody>
	</table>
	'''

def menuHtmlSpaced(icon,text,description,icon_size):
	return f'''
<table style="width: 100%" border="0" cellspacing="2" cellpadding="2">
	  <tbody>
		<tr>
		  <td style="text-align: center; vertical-align: middle;">&nbsp;<img src="{icon}" width="{icon_size}" height="{icon_size}"></td>
		  <td>
			<table style="width: 100%" border="0">
			  <tbody>
				<tr>
				  <td style="font-weight: bold;"><big>{text}</big></td>
				</tr>
				<tr>
				  <td style="font-style: normal; font-weight: normal;"><small>{description}&nbsp;&nbsp;</small></td>
				</tr>
			  </tbody>
			</table>
		  </td>
		</tr>
	  </tbody>
	</table>
	'''

class MenuLabel(QLabel):
	clicked=pyqtSignal()

	def __init__(self, parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

	def mousePressEvent(self, ev):
		self.clicked.emit()

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			col = self.palette().highlight().color().name()
			highlight = QColor(col).name()

			col = self.palette().highlightedText().color().name()
			highlight_text = QColor(col).name()
			
			self.setStyleSheet(f"background-color: {highlight}; color: {highlight_text};")
			return True
		elif event.type() == QEvent.Leave:
			self.setStyleSheet('')
			return True
		return False

class DisabledMenuLabel(QLabel):
	clicked=pyqtSignal()

	def __init__(self, parent=None):
		QLabel.__init__(self, parent)
		self.installEventFilter(self)

	def mousePressEvent(self, ev):
		self.clicked.emit()

	def eventFilter(self, object, event):
		
		return False

def ExtendedMenuItem(self,icon,title,description,icon_size,func):

	erkmenuLabel = MenuLabel( menuHtml(icon,title,description,icon_size) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)
	erkmenuLabel.clicked.connect(func)

	return erkmenuAction

def DisabledExtendedMenuItem(self,icon,title,description,icon_size,func):

	erkmenuLabel = DisabledMenuLabel( menuHtml(icon,title,description,icon_size) )
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)
	erkmenuLabel.clicked.connect(func)

	return erkmenuAction

def ExtendedMenuItemNoAction(self,icon,title,description,icon_size):

	erkmenuLabel = QLabel( menuHtmlSpaced(icon,title,description,icon_size) )
	erkmenuLabel.setOpenExternalLinks(True)
	erkmenuAction = QWidgetAction(self)
	erkmenuAction.setDefaultWidget(erkmenuLabel)

	return erkmenuAction