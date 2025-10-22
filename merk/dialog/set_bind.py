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

BLOCK_TAB = True

# From https://sl-alex.net/gui/2022/08/21/shortcutedit_capturing_shortcuts_in_pyqt/
class ShortcutEdit(QLineEdit):
	shortcutChanged = QtCore.pyqtSignal(int, list)

	keymap = {}
	modmap = {}
	modkeyslist = []

	current_modifiers = []
	current_key = 0

	def __init__(self, parent=None, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)

		self.parent = parent

		for key, value in vars(Qt).items():
			if isinstance(value, Qt.Key):
				self.keymap[value] = key.partition('_')[2]
				
		self.modmap = {
			Qt.ControlModifier:     'Ctrl',
			Qt.AltModifier:         'Alt',
			Qt.ShiftModifier:       'Shift',
			Qt.MetaModifier:        'Meta',
			Qt.GroupSwitchModifier: 'AltGr',
			Qt.KeypadModifier:      'Num',
			}

		self.modkeyslist = [
			Qt.Key_Control,
			Qt.Key_Alt,
			Qt.Key_Shift,
			Qt.Key_Meta,
			Qt.Key_AltGr,
			Qt.Key_NumLock,
			]

		self.installEventFilter(self)

	def focusInEvent(self, event):

		self.setText('')

		palette = self.parent.keyLabel.palette()
		palette.setColor(QPalette.WindowText, self.parent.default_text_color)  # Set text color to red
		self.parent.keyLabel.setPalette(palette)

		self.parent.status_label.setText("Enter key sequence.")

	def focusOutEvent(self, event):

		keys = self.text()
		is_valid = True
		if not is_valid_shortcut_sequence(keys): is_valid = False
		ks = QKeySequence(keys)
		if ks.isEmpty(): is_valid = False

		is_taken = False
		for w in QApplication.topLevelWidgets():
			for other in w.findChildren(QShortcut):
				if ks == other.key(): is_taken = True

		if not is_valid or is_taken:
			palette = self.parent.keyLabel.palette()
			palette.setColor(QPalette.WindowText, QColor("red"))  # Set text color to red
			self.parent.keyLabel.setPalette(palette)

		if not is_valid:
			self.parent.status_label.setText("Invalid key sequence.")
		elif is_taken:
			self.parent.status_label.setText("Hotkey is already in use.")
		else:
			self.parent.status_label.setText("Ready.")

		super().focusOutEvent(event)

	def eventFilter(self, object, event):
		if event.type() == QtCore.QEvent.KeyPress:
			if event.key() == 0 and int(event.modifiers()) == 0:
				return True

			self.current_modifiers = []
			self.current_key = 0

			key = event.key()
			modifiers = int(event.modifiers())

			if BLOCK_TAB:
				# Re-enable the tab key, so that users
				# can tab between text entries
				if event.key() == Qt.Key_Tab:
					super().keyPressEvent(event)
					return True
			
			modifiers_dict = {}
			for modifier in self.modmap.keys():
				if modifiers & modifier:
					modifiers_dict[modifier] = self.modmap[modifier]

			if key in self.modkeyslist:
				key = 0

			text = ''

			for modifier in modifiers_dict:
				if text != '':
					text = text + '+'
				text = text + modifiers_dict[modifier]
				self.current_modifiers.append(modifier)
			if Qt.KeypadModifier in modifiers_dict and key != 0:
				text = text + self.keymap[key]
				self.current_key = key
			elif key in self.keymap:
				if text != '':
					text = text + '+'
				text = text + self.keymap[key]
				self.current_key = key

			self.setText(text)
			self.shortcutChanged.emit(self.current_key, self.current_modifiers)

			return True
		elif event.type() == QtCore.QEvent.KeyRelease:
			return True

		return False

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

		retval = [ self.key_sequence.text(), self.command.text() ]

		return retval

	def clickTab(self):
		global BLOCK_TAB
		if self.allowTab.isChecked():
			BLOCK_TAB = True
		else:
			BLOCK_TAB = False

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.block_tab = True

		palette = self.palette()
		self.default_text_color = palette.color(QPalette.WindowText)

		self.setWindowTitle("Bind Hotkey")
		self.setWindowIcon(QIcon(INPUT_ICON))

		nameLayout = QHBoxLayout()
		self.keyLabel = QLabel("<b>Key Sequence:&nbsp;</b>")
		
		self.key_sequence = ShortcutEdit(self)
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJK")
		self.key_sequence.setMinimumWidth(wwidth)

		self.allowTab = QCheckBox("Block tab key",self)
		self.allowTab.stateChanged.connect(self.clickTab)
		self.allowTab.setChecked(True)

		nameLayout.addWidget(self.keyLabel)
		nameLayout.addWidget(self.key_sequence)
		nameLayout.addWidget(self.allowTab)

		self.commandLabel = QLabel("<b>Command:</b>")
		
		self.command = QLineEdit(self)
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQR")
		self.command.setMinimumWidth(wwidth)

		argsLayout = QHBoxLayout()
		argsLayout.addWidget(self.commandLabel)
		argsLayout.addWidget(self.command)

		self.status_label = QLabel("Enter key sequence.")

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(nameLayout)
		finalLayout.addLayout(argsLayout)
		finalLayout.addWidget(self.status_label)
		finalLayout.addWidget(buttons)
		
		self.setTabOrder(self.key_sequence, self.command)
		self.setTabOrder(self.command, buttons)
		self.setTabOrder(buttons, self.key_sequence)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(self.sizeHint())

		self.key_sequence.setFocus()