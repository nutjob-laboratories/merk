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

from ..resources import *
from .. import config

class Dialog(QDialog):

	@staticmethod
	def get_sasl_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		retval = [self.name.text(),self.key.text()]

		return retval

	def clickEye(self,state):
		if self.eye.isChecked():
			self.key.setEchoMode(QLineEdit.Normal)
		else:
			self.key.setEchoMode(QLineEdit.Password)

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		config.load_settings(config.CONFIG_FILE)

		self.setWindowTitle("SASL Login")
		self.setWindowIcon(QIcon(CHANNEL_ICON))

		self.nameLabel = QLabel("<b>Username:</b>")

		self.name = QNoSpaceLineEdit()
	
		self.keyLabel = QLabel("<b>Password:</b>")
		self.key = QNoSpaceLineEdit()
		self.key.setEchoMode(QLineEdit.Password)

		self.eye = QCheckBox("View password",self)
		self.eye.stateChanged.connect(self.clickEye)

		inputLayout = QFormLayout()
		inputLayout.addRow(self.nameLabel,self.name)
		inputLayout.addRow(self.keyLabel,self.key)
		inputLayout.addRow(self.eye)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		chanInfoBox = QGroupBox("",self)
		chanInfoBox.setLayout(inputLayout)
		chanInfoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(chanInfoBox)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.name.setFocus()
