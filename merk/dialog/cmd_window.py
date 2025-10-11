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

class Dialog(QDialog):

	@staticmethod
	def get_window_information(parent=None,xval=None,yval=None,measure='pixels'):
		dialog = Dialog(parent,xval,yval,measure)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		retval = [ self.width.value(),self.height.value() ]

		return retval

	def __init__(self,parent=None,xval=None,yval=None,measure='pixels'):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.xval = xval
		self.yval = yval
		self.measure=measure

		self.setWindowTitle("Window")
		self.setWindowIcon(QIcon(RESIZE_ICON))

		widthLayout = QHBoxLayout()
		self.widthLabel = QLabel(self.xval)
		self.width = QSpinBox()
		self.width.setRange(1,5000)
		self.width.setValue(1)
		widthLayout.addWidget(self.widthLabel)
		#widthLayout.addStretch()
		widthLayout.addWidget(self.width)
		widthLayout.addWidget(QLabel(self.measure))

		heightLayout = QHBoxLayout()
		self.heightLabel = QLabel(self.yval)
		self.height = QSpinBox()
		self.height.setRange(1,5000)
		self.height.setValue(1)
		heightLayout.addWidget(self.heightLabel)
		#heightLayout.addStretch()
		heightLayout.addWidget(self.height)
		heightLayout.addWidget(QLabel(self.measure))

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(widthLayout)
		finalLayout.addLayout(heightLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)