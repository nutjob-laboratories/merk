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

class PlainIconTextAction(QWidgetAction):
	def __init__(self, icon, text, parent=None):
		super().__init__(parent)
		
		widget = QWidget()
		layout = QHBoxLayout()
		layout.setContentsMargins(2, 2, 2, 2)

		font_metrics = QFontMetrics(self.font())
		icon_size = font_metrics.height()
		
		icon_label = QLabel()
		icon_label.setPixmap(icon.pixmap(icon_size, icon_size))
		layout.addWidget(icon_label)
		
		data_label = QLabel()
		data_label.setText("<small>&nbsp;</small>"+text+"&nbsp;")
		layout.addWidget(data_label)

		layout.addStretch()
		
		widget.setLayout(layout)
		self.setDefaultWidget(widget)

PLAIN_TEXT = f'''
<table width="100%" border="0" cellspacing="1" cellpadding="1">
	<tbody>
		<tr>
			<td>&nbsp;&nbsp;!TEXT!&nbsp;&nbsp;</td>
		</tr>
	</tbody>
</table>'''

def plainTextAction(self,text):
		
	tsLabel = QLabel( PLAIN_TEXT.replace("!TEXT!",text) )
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)

	return tsAction

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

def plainTextClickable(self,text,func):
	tsLabel = MenuLabel( PLAIN_TEXT.replace("!TEXT!",text) )
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)
	tsLabel.clicked.connect(func)

	return tsAction

NS_PLAIN_TEXT = f'''
<table width="100%" border="0" cellspacing="1" cellpadding="1">
	<tbody>
		<tr>
			<td>!TEXT!</td>
		</tr>
	</tbody>
</table>'''

NSB_PLAIN_TEXT = f'''
<table width="100%" border="0" cellspacing="1" cellpadding="1">
	<tbody>
		<tr>
			<td><small>!TEXT!</small></td>
		</tr>
	</tbody>
</table>'''

def noSpacePlainTextAction(self,text):
		
	tsLabel = QLabel( NS_PLAIN_TEXT.replace("!TEXT!",text) )
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)

	return tsAction

def noSpacePlainTextActionBorder(self,text,darkmode):

	if darkmode:
		border_color = "darkGray"
	else:
		border_color = "lightGray"
		
	tsLabel = QLabel( NSB_PLAIN_TEXT.replace("!TEXT!",text) )
	tsLabel.setStyleSheet(f"border: 1px solid {border_color}; padding: -1px;")
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)

	return tsAction

def BoxPlainTextAction(self,title,text):
		
	tsLabel = QLabel( NS_PLAIN_TEXT.replace("!TEXT!",text) )

	alayout = QHBoxLayout()
	alayout.addWidget(tsLabel)
	alayout.setContentsMargins(3,3,3,3)

	aBox = QGroupBox(title)
	aBox.setLayout(alayout)
	aBox.setAlignment(Qt.AlignCenter)

	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(aBox)

	return tsAction




	