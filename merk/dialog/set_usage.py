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
	def get_alias_information(parent=None):
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

		self.setWindowTitle("Usage")
		self.setWindowIcon(QIcon(SCRIPT_ICON))

		self.nameLabel = QLabel("<b>Number of arguments:</b>")
		self.name = QNoSpaceLineEdit()	# Spaces can't be typed into this QLineEdit, as
										# spaces are forbidden in channel names

		keyLayout = QHBoxLayout()
		self.keyLabel = QLabel("<b>Message:</b>")
		self.key = QLineEdit()
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDABCDEFGHIJ")
		self.key.setMinimumWidth(wwidth)

		self.aliasDescription = QLabel(f'''
			<small>
			Set <b>Number of arguments</b> to the number of arguments this script
			should expect; this must be a number. If the script is called with a different
			number of arguments, then <b>Message</b> is displayed. Setting a <b>Message</b>
			is optional.
			</small>
			<br>
			''')
		self.aliasDescription.setWordWrap(True)
		self.aliasDescription.setAlignment(Qt.AlignJustify)

		inputLayout = QFormLayout()
		inputLayout.addRow(self.nameLabel,self.name)
		inputLayout.addRow(self.keyLabel,self.key)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.aliasDescription)
		finalLayout.addLayout(inputLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.name.setFocus()
