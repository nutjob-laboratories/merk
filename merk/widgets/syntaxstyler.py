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

class SyntaxColor(QWidget):

	syntaxChanged = pyqtSignal(list)

	def exportSettings(self):

		style = []
		if self.bold: style.append("bold")
		if self.italic: style.append("italic")
		flatstyle = ' '.join(style)

		gcode = [ f"{self.color}",flatstyle]

		return gcode

	def checkBold(self,state):
		if state==Qt.Checked:
			self.bold = True
			self.setBold.setCheckState(Qt.Checked)
		else:
			self.bold = False
			self.setBold.setCheckState(Qt.Unchecked)

		self.syntaxChanged.emit([self.name,self.exportSettings()])

	def checkItalic(self,state):
		if state==Qt.Checked:
			self.italic = True
			self.setItalic.setCheckState(Qt.Checked)
		else:
			self.italic = False
			self.setItalic.setCheckState(Qt.Unchecked)

		self.syntaxChanged.emit([self.name,self.exportSettings()])

	def buttonColor(self):

		self.newcolor = QColorDialog.getColor(QColor(self.color))

		if self.newcolor.isValid():
			self.ncolor = self.newcolor.name()
			self.color = self.ncolor

			self.setColor.setStyleSheet(f'background-color: {self.color};')

			self.syntaxChanged.emit([self.name,self.exportSettings()])


	def __init__(self,name,description,color,style,parent=None):
		super(SyntaxColor,self).__init__(parent)

		self.name = name
		self.description = description
		self.color = color
		self.style = style
		self.parent = parent

		self.bold = False
		self.italic = False

		if "bold" in self.style: self.bold = True
		if "italic" in self.style: self.italic = True

		self.descriptionLabel = QLabel(self.description)

		self.setColor = QPushButton("")
		self.setColor.clicked.connect(self.buttonColor)
		self.setColor.setToolTip("Set color")
		self.setColor.setStyleSheet(f'background-color: {self.color};')
		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setColor.setFixedSize(fheight+8,fheight+8)

		self.setBold = QCheckBox("",self)
		self.setBold.setIcon(QIcon(self.parent.parent.bold_icon))
		self.setBold.setToolTip("Bold")
		self.setBold.stateChanged.connect(self.checkBold)
		if self.bold:
			self.setBold.setCheckState(Qt.Checked)
		else:
			self.setBold.setCheckState(Qt.Unchecked)

		self.setItalic = QCheckBox("",self)
		self.setItalic.setIcon(QIcon(self.parent.parent.italic_icon))
		self.setItalic.setToolTip("Italic")
		self.setItalic.stateChanged.connect(self.checkItalic)
		if self.italic:
			self.setItalic.setCheckState(Qt.Checked)
		else:
			self.setItalic.setCheckState(Qt.Unchecked)

		

		controlsLayout = QHBoxLayout()
		controlsLayout.addWidget(self.setColor)
		controlsLayout.addWidget(self.setBold)
		controlsLayout.addWidget(self.setItalic)
		controlsLayout.setAlignment(Qt.AlignLeft)

		mainLayout = QVBoxLayout()
		mainLayout.addWidget(self.descriptionLabel)
		mainLayout.addLayout(controlsLayout)

		self.setLayout(mainLayout)

class SyntaxTextColor(QWidget):

	syntaxChanged = pyqtSignal(list)

	def exportSettings(self):

		return self.color

	def buttonColor(self):

		self.newcolor = QColorDialog.getColor(QColor(self.color))

		if self.newcolor.isValid():
			self.ncolor = self.newcolor.name()
			self.color = self.ncolor

			self.setColor.setStyleSheet(f'background-color: {self.color};')

			self.syntaxChanged.emit([self.name,self.exportSettings()])


	def __init__(self,name,description,color,parent=None):
		super(SyntaxTextColor,self).__init__(parent)

		self.name = name
		self.description = description
		self.color = color
		self.parent = parent

		self.descriptionLabel = QLabel(self.description)

		self.setColor = QPushButton("")
		self.setColor.clicked.connect(self.buttonColor)
		self.setColor.setStyleSheet(f'background-color: {self.color};')
		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setColor.setFixedSize(fheight+8,fheight+8)

		controlsLayout = QHBoxLayout()
		controlsLayout.addWidget(self.descriptionLabel)
		controlsLayout.addWidget(self.setColor)
		controlsLayout.setAlignment(Qt.AlignLeft)

		self.setLayout(controlsLayout)