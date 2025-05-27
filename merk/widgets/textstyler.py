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

class MiniStyler(QWidget):

	qssChanged = pyqtSignal(list)

	def exportQss(self):
		gcode = f'color: {self.color};'
		if self.bold: gcode = gcode + ' font-weight: bold;'
		if self.italic: gcode = gcode + ' font-style: italic;'
		if self.underline: gcode = gcode + ' text-decoration: underline;'

		return gcode

	def parseQss(self):
		for line in self.qss.split(";"):
			e = line.split(':')
			if len(e)==2:
				key = e[0].strip()
				value = e[1].strip()

				if key.lower()=='color':
					self.color = value

				if key.lower()=='font-style':
					if value.lower()=='italic':
						self.italic = True

				if key.lower()=='font-weight':
					if value.lower()=='bold':
						self.bold = True

	def checkBold(self,state):
		if state==Qt.Checked:
			self.bold = True
			self.setBold.setCheckState(Qt.Checked)
		else:
			self.bold = False
			self.setBold.setCheckState(Qt.Unchecked)

		self.qssChanged.emit([self.name,self.exportQss()])

	def checkItalic(self,state):
		if state==Qt.Checked:
			self.italic = True
			self.setItalic.setCheckState(Qt.Checked)
		else:
			self.italic = False
			self.setItalic.setCheckState(Qt.Unchecked)

		self.qssChanged.emit([self.name,self.exportQss()])

	def buttonColor(self):

		self.newcolor = QColorDialog.getColor(QColor(self.color))

		if self.newcolor.isValid():
			self.ncolor = self.newcolor.name()
			self.color = self.ncolor

			self.setColor.setStyleSheet(f'background-color: {self.color};')

			self.qssChanged.emit([self.name,self.exportQss()])

	def setQss(self,newstyle):
		self.qss = newstyle
		self.italic = False
		self.bold = False

		self.parseQss()

		self.setColor.setStyleSheet(f'background-color: {self.color};')

		if self.bold:
			self.setBold.setCheckState(Qt.Checked)
		else:
			self.setBold.setCheckState(Qt.Unchecked)

		if self.italic:
			self.setItalic.setCheckState(Qt.Checked)
		else:
			self.setItalic.setCheckState(Qt.Unchecked)


	def __init__(self,name,description,qss,underline=False,parent=None):
		super(MiniStyler,self).__init__(parent)

		self.name = name
		self.description = description
		self.qss = qss
		self.default = qss
		self.underline = underline
		self.parent = parent

		self.color = None
		self.bold = False
		self.italic = False

		self.parseQss()

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
		controlsLayout.addWidget(self.descriptionLabel)
		controlsLayout.addWidget(QLabel(' '))
		controlsLayout.addWidget(self.setColor)
		controlsLayout.addWidget(self.setBold)
		controlsLayout.addWidget(self.setItalic)
		controlsLayout.setAlignment(Qt.AlignLeft)

		self.setLayout(controlsLayout)

