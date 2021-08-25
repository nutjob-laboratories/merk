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

class TextStyler(QWidget):

	def loadQss(self,style,default):
		self.qss = style
		self.default = default

		self.parseQss()

		self.example.setStyleSheet(self.qss)
		self.setColor.setStyleSheet(f'background-color: {self.color};')

		if self.show_styles:

			if self.bold:
				self.setBold.setCheckState(Qt.Checked)
			else:
				self.setBold.setCheckState(Qt.Unchecked)

			if self.italic:
				self.setItalic.setCheckState(Qt.Checked)
			else:
				self.setItalic.setCheckState(Qt.Unchecked)


	def exportQss(self):
		gcode = f'color: {self.color};'
		if self.bold: gcode = gcode + ' font-weight: bold;'
		if self.italic: gcode = gcode + ' font-style: italic;'
		if self.underline: gcode = gcode + ' text-decoration: underline;'

		return gcode

	def generateQss(self):
		gcode = f'color: {self.color};'
		if self.bold: gcode = gcode + ' font-weight: bold;'
		if self.italic:
			gcode = gcode + ' font-style: italic;'
		else:
			gcode = gcode + ' font-style: normal;'

		gcode = gcode + f' background-color: {self.bgcolor}'
		#if self.underline: gcode = gcode + ' text-decoration: underline;'

		self.qss = gcode

	def doReset(self):

		self.color = self.first_color
		self.bold = self.first_bold
		self.italic = self.first_italic
		self.underline = self.first_underline

		self.generateQss()
		self.parseQss()

		self.example.setStyleSheet(self.qss)
		self.setColor.setStyleSheet(f'background-color: {self.color};')

		if self.show_styles:

			if self.bold:
				self.setBold.setCheckState(Qt.Checked)
			else:
				self.setBold.setCheckState(Qt.Unchecked)

			if self.italic:
				self.setItalic.setCheckState(Qt.Checked)
			else:
				self.setItalic.setCheckState(Qt.Unchecked)

	def buttonColor(self):

		self.newcolor = QColorDialog.getColor(QColor(self.color))

		if self.newcolor.isValid():
			self.ncolor = self.newcolor.name()
			self.color = self.ncolor
			self.generateQss()
			self.example.setStyleSheet(self.qss)
			self.setColor.setStyleSheet(f'background-color: {self.color};')

	def checkBold(self,state):
		if state==Qt.Checked:
			self.bold = True
			self.setBold.setCheckState(Qt.Checked)
		else:
			self.bold = False
			self.setBold.setCheckState(Qt.Unchecked)
		self.generateQss()
		self.example.setStyleSheet(self.qss)

	def checkItalic(self,state):
		if state==Qt.Checked:
			self.italic = True
			self.setItalic.setCheckState(Qt.Checked)
		else:
			self.italic = False
			self.setItalic.setCheckState(Qt.Unchecked)
		self.generateQss()
		self.example.setStyleSheet(self.qss)

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

	def __init__(self,name,text,qss,show_styles=True,underline=False,parent=None):
		super(TextStyler,self).__init__(parent)
		self.name = name
		self.text = text
		self.parent = parent
		self.qss = qss
		self.show_styles = show_styles

		self.color = None
		self.bold = False
		self.italic = False
		self.underline = underline
		self.bgcolor = None

		self.parseQss()

		self.first_color = self.color
		self.first_bold = self.bold
		self.first_italic = self.italic
		self.first_underline = self.underline

		if self.underline:
			self.example = QLabel(f"<u>{self.text}</u>")
		else:
			self.example = QLabel(f"{self.text}")

		#self.parseQss()
		self.example.setStyleSheet(self.qss)

		self.setColor = QPushButton("")
		self.setColor.clicked.connect(self.buttonColor)
		self.setColor.setStyleSheet(f'background-color: {self.color};')

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setColor.setFixedSize(fheight+8,fheight+8)


		self.setReset = QPushButton("")
		self.setReset.clicked.connect(self.doReset)
		self.setReset.setIcon(QIcon(RESET_ICON))
		self.setReset.setFixedSize(fheight+8,fheight+8)

		# br = fm.boundingRect('Reset')
		# self.setReset.setFixedHeight(br.height())

		if self.show_styles:

			self.setBold = QCheckBox("",self)
			self.setBold.setIcon(QIcon(BOLD_ICON))
			self.setBold.stateChanged.connect(self.checkBold)
			if self.bold:
				self.setBold.setCheckState(Qt.Checked)
			else:
				self.setBold.setCheckState(Qt.Unchecked)

			self.setItalic = QCheckBox("",self)
			self.setItalic.setIcon(QIcon(ITALIC_ICON))
			self.setItalic.stateChanged.connect(self.checkItalic)
			if self.italic:
				self.setItalic.setCheckState(Qt.Checked)
			else:
				self.setItalic.setCheckState(Qt.Unchecked)

			controlsLayout = QHBoxLayout()
			controlsLayout.addWidget(self.example)
			controlsLayout.addWidget(QLabel(' '))
			controlsLayout.addWidget(self.setBold)
			controlsLayout.addWidget(self.setItalic)
			controlsLayout.addWidget(self.setColor)
			controlsLayout.addWidget(self.setReset)
			controlsLayout.setAlignment(Qt.AlignLeft)

		else:

			controlsLayout = QHBoxLayout()
			controlsLayout.addWidget(self.example)
			controlsLayout.addWidget(QLabel(' '))
			controlsLayout.addWidget(self.setReset)
			controlsLayout.addWidget(self.setColor)
			controlsLayout.setAlignment(Qt.AlignLeft)

		finale = QVBoxLayout()
		finale.addLayout(controlsLayout)

		self.setLayout(finale)
