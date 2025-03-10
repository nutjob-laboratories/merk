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

class Dialog(QDialog):

	@staticmethod
	def get_channel_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		retval = [self.name.text(),self.key.text()]

		return retval

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Join channel")
		self.setWindowIcon(QIcon(CHANNEL_ICON))

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("<b>Channel:</b>")
		self.name = QNoSpaceLineEdit()	# Spaces can't be typed into this QLineEdit, as
									# spaces are forbidden in channel names
		nameLayout.addWidget(self.nameLabel)
		nameLayout.addStretch()
		nameLayout.addWidget(self.name)

		keyLayout = QHBoxLayout()
		self.keyLabel = QLabel("<b>Message:</b>")
		self.key = QLineEdit()
		keyLayout.addWidget(self.keyLabel)
		keyLayout.addStretch()
		keyLayout.addWidget(self.key)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		chanLayout = QVBoxLayout()
		chanLayout.addLayout(nameLayout)
		chanLayout.addLayout(keyLayout)

		chanInfoBox = QGroupBox("",self)
		chanInfoBox.setLayout(chanLayout)
		chanInfoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(chanInfoBox)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.name.setFocus()
