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
	def get_nick_information(nick,parent=None):
		dialog = Dialog(nick,parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		retval = self.name.text()

		if self.save_as_default:
			user.NICKNAME = retval
			user.save_user(user.USER_FILE)

		return retval

	def clickSave(self,state):
		if state == Qt.Checked:
			self.save_as_default = True
		else:
			self.save_as_default = False

	def __init__(self,nick,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.nick = nick

		self.save_as_default = False

		self.setWindowTitle("Change nickname")
		self.setWindowIcon(QIcon(PRIVATE_ICON))

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("<b>New nickname:</b>")
		self.name = QNoSpaceLineEdit()
		nameLayout.addWidget(self.nameLabel)
		nameLayout.addStretch()
		nameLayout.addWidget(self.name)

		self.savenick = QCheckBox("Save nickname as default",self)
		self.savenick.stateChanged.connect(self.clickSave)

		self.name.setPlaceholderText(self.nick)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		nickInfoBox = QGroupBox("",self)
		nickInfoBox.setLayout(nameLayout)
		nickInfoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(nickInfoBox)
		finalLayout.addWidget(self.savenick)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.name.setFocus()