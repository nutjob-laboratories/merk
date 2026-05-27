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

		retval = [ self.script_name, self.args.text() ]

		return retval

	def getFilename(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Select script", commands.SCRIPTS_DIRECTORY, f"{APPLICATION_NAME} Script (*.{SCRIPT_FILE_EXTENSION});;All Files (*)", options=options)
		if fileName:
			if fileName.startswith(commands.SCRIPTS_DIRECTORY):
				self.add_and_select(os.path.basename(fileName))
			else:
				self.add_and_select(fileName)

	def add_and_select(self,new_item):
		if self.name.findText(new_item) == -1:
			self.name.addItem(new_item)
			index = self.name.count() - 1
		else:
			index = self.name.findText(new_item)
		self.name.setCurrentIndex(index)

	def on_script_changed(self, text):
		self.script_name = text

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.script_name = ''

		self.setWindowTitle("Execute script")
		self.setWindowIcon(QIcon(COMMAND_ICON))

		nameLayout = QHBoxLayout()
		self.nameLabel = QLabel("<b>Filename:&nbsp;</b>")

		scripts = []
		for f in commands.list_scripts():
			scripts.append(f'{f}')

		self.name = QComboBox(self)
		self.name.currentTextChanged.connect(self.on_script_changed)
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEF")
		self.name.setMinimumWidth(wwidth)
		self.name.addItem('')
		for e in scripts:
			self.name.addItem(e)

		self.file_button = QPushButton("")
		self.file_button.setIcon(QIcon(EDIT_ICON))
		self.file_button.clicked.connect(self.getFilename)
		self.file_button.setToolTip("Select a script")

		nameLayout.addWidget(self.nameLabel)
		nameLayout.addWidget(self.name)
		nameLayout.addWidget(self.file_button)

		self.argsLabel = QLabel("<b>Arguments:</b>")
		
		self.args = QLineEdit()
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEF")
		self.args.setMinimumWidth(wwidth)

		argsLayout = QHBoxLayout()
		argsLayout.addWidget(self.argsLabel)
		argsLayout.addWidget(self.args)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(nameLayout)
		finalLayout.addLayout(argsLayout)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())

		self.name.setFocus()