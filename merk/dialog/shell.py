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

		retval = [self.name.text(),self.command.text()]

		return retval

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Shell Command")
		self.setWindowIcon(QIcon(SCRIPT_ICON))

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("<b>Alias:</b>")
		self.name = QNoSpaceLineEdit()	# Spaces can't be typed into this QLineEdit, as
									    # spaces are forbidden in alias names

		self.commandLabel = QLabel("<b>Command:</b>")
		self.command = QLineEdit()
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDABCDEFGHIJ")
		self.command.setMinimumWidth(wwidth)

		self.shellDescription = QLabel(f'''
			<small>
			This command will be executed, with the results of the command stored in the
			alias set here. If the command fails, or has an error, the alias will not
			be set, and the error will be displayed.
			</small>
			<br>
			''')
		self.shellDescription.setWordWrap(True)
		self.shellDescription.setAlignment(Qt.AlignJustify)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		lay = QFormLayout()
		lay.addRow(self.nameLabel,self.name)
		lay.addRow(self.commandLabel,self.command)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.shellDescription)
		finalLayout.addLayout(lay)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.name.setFocus()
