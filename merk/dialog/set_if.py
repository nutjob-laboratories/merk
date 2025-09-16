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
from .. import user

class Dialog(QDialog):

	@staticmethod
	def get_if_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		retval = [self.val1.text(),self.operator.currentText(),self.val2.text(),self.command.text()]

		return retval


	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("If statement")
		self.setWindowIcon(QIcon(SCRIPT_ICON))

		self.val1 = QLineEdit()
		self.val2 = QLineEdit()
		self.command = QLineEdit()

		self.val1.setPlaceholderText('VALUE1')
		self.val2.setPlaceholderText('VALUE2')
		self.command.setPlaceholderText('Command...')

		self.operator = QComboBox(self)
		self.operator.addItem('(is)')
		self.operator.addItem('(not)')
		self.operator.addItem('(in)')
		self.operator.addItem('(gt)')
		self.operator.addItem('(lt)')

		fline = QHBoxLayout()
		fline.addWidget(self.val1)
		fline.addWidget(self.operator)
		fline.addWidget(self.val2)

		sline = QHBoxLayout()
		sline.addWidget(QLabel("<b>Command:</b>"))
		sline.addWidget(self.command)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		# nickInfoBox = QGroupBox("",self)
		# nickInfoBox.setLayout(nameLayout)
		# nickInfoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(fline)
		finalLayout.addLayout(sline)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.val1.setFocus()