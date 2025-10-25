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

import os
import pathlib

from ..resources import *
from .. import commands
from .. import config

class Dialog(QDialog):

	@staticmethod
	def get_script_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		retval = [ self.name.text(), self.script.text(), self.usage.text(), self.mhelp.text() ]

		return retval

	def getFilename(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Select script", commands.SCRIPTS_DIRECTORY, f"{APPLICATION_NAME} Script (*.{SCRIPT_FILE_EXTENSION});;All Files (*)", options=options)
		if fileName:

			scriptDir = pathlib.Path(commands.SCRIPTS_DIRECTORY)
			configDir = pathlib.Path(config.CONFIG_DIRECTORY)
			fileDir = pathlib.Path(os.path.dirname(fileName))

			if scriptDir.resolve() == fileDir.resolve():
				# Script is in the script directory, no need
				# to keep the path, MERK will find the file
				self.script.setText(os.path.basename(fileName))
			elif configDir.resolve() == fileDir.resolve():
				self.script.setText(os.path.basename(fileName))
			else:
				self.script.setText(fileName)

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.setWindowTitle("Create Macro")
		self.setWindowIcon(QIcon(EXE_ICON))

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("<b>Name:&nbsp;</b>")
		
		self.name = QLineEdit()
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDABCDEFGHIJ")
		self.name.setMinimumWidth(wwidth)

		nameLayout.addWidget(self.nameLabel)
		nameLayout.addWidget(self.name)

		scriptLayout = QHBoxLayout()
		self.scriptLabel = QLabel("<b>Script:&nbsp;</b>")
		
		self.script = QLineEdit()
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDABCDEFGHIJ")
		self.script.setMinimumWidth(wwidth)
		

		self.file_button = QPushButton("")
		self.file_button.setIcon(QIcon(SCRIPT_ICON))
		self.file_button.clicked.connect(self.getFilename)
		self.file_button.setToolTip("Select a script")

		scriptLayout.addWidget(self.scriptLabel)
		scriptLayout.addWidget(self.script)
		scriptLayout.addWidget(self.file_button)

		self.usageLabel = QLabel("<b>Usage:</b>")
		
		self.usage = QLineEdit()
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDABCDEFGHIJ")
		self.usage.setMinimumWidth(wwidth)

		usageLayout = QHBoxLayout()
		usageLayout.addWidget(self.usageLabel)
		usageLayout.addWidget(self.usage)

		self.mhelpLabel = QLabel("<b>Help:</b>")
		
		self.mhelp = QLineEdit()
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDABCDEFGHIJ")
		self.mhelp.setMinimumWidth(wwidth)

		mhelpLayout = QHBoxLayout()
		mhelpLayout.addWidget(self.mhelpLabel)
		mhelpLayout.addWidget(self.mhelp)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(nameLayout)
		finalLayout.addLayout(scriptLayout)
		finalLayout.addLayout(usageLayout)
		finalLayout.addLayout(mhelpLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.script.setFocus()