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

import emoji
import fnmatch

class EmojiAutocomplete(QPlainTextEdit):

	def __init__(self, *args):
		QPlainTextEdit.__init__(self, *args)

		self.parent = args[0]

	def keyPressEvent(self,event):

		# BUGFIX: the user can "drag" the view "down"
		# with the mouse; this resets the widget to
		# "normal" every time the user presses a key
		# Man, I wish Qt had a rich-text-enabled QLineEdit :-(
		sb = self.verticalScrollBar()
		sb.setValue(sb.minimum())
		self.ensureCursorVisible()

		if event.key() == Qt.Key_Tab:

			if not config.ENABLE_EMOJI_SHORTCODES and not config.ENABLE_ASCIIMOJI_SHORTCODES:
				pass
			elif not self.parent.autocomplete.isChecked():
				pass
			else:

				cursor = self.textCursor()

				if self.toPlainText().strip()=='': return

				if config.ENABLE_EMOJI_SHORTCODES:
					# Autocomplete emojis
					cursor.select(QTextCursor.WordUnderCursor)
					oldpos = cursor.position()
					cursor.select(QTextCursor.WordUnderCursor)
					newpos = cursor.selectionStart() - 1
					cursor.setPosition(newpos,QTextCursor.MoveAnchor)
					cursor.setPosition(oldpos,QTextCursor.KeepAnchor)
					self.setTextCursor(cursor)
					if self.textCursor().hasSelection():
						text = self.textCursor().selectedText()

						for c in EMOJI_AUTOCOMPLETE:

							if fnmatch.fnmatchcase(c.lower(),f"{text.lower()}*"):
								cursor.beginEditBlock()
								cursor.insertText(c)
								cursor.endEditBlock()
								return

				if config.ENABLE_ASCIIMOJI_SHORTCODES:
					# Autocomplete emojis
					cursor.select(QTextCursor.WordUnderCursor)
					oldpos = cursor.position()
					cursor.select(QTextCursor.WordUnderCursor)
					newpos = cursor.selectionStart() - 1
					cursor.setPosition(newpos,QTextCursor.MoveAnchor)
					cursor.setPosition(oldpos,QTextCursor.KeepAnchor)
					self.setTextCursor(cursor)
					if self.textCursor().hasSelection():
						text = self.textCursor().selectedText()

						for c in ASCIIMOIJI:

							if fnmatch.fnmatchcase(c.lower(),f"{text.lower()}*"):
								cursor.beginEditBlock()
								cursor.insertText(c)
								cursor.endEditBlock()
								self.ensureCursorVisible()
								return

				cursor.movePosition(QTextCursor.End)
				self.setTextCursor(cursor)

		else:
			return super().keyPressEvent(event)

	def text(self):
		return self.toPlainText()

	def setText(self,text):
		self.setPlainText(text)

class Dialog(QDialog):

	@staticmethod
	def get_away_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		retval = self.away.text()

		if self.save_as_default:

			config.DEFAULT_AWAY_MESSAGE = retval
			config.save_settings(config.CONFIG_FILE)

		return retval

	def clickSave(self,state):
		if state == Qt.Checked:
			self.save_as_default = True
		else:
			self.save_as_default = False

	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		self.save_as_default = False

		self.setWindowTitle("Away")
		self.setWindowIcon(QIcon(GO_AWAY_ICON))

		awayLayout = QHBoxLayout()
		self.awayLabel = QLabel("<b>Away Message:</b>")


		self.away = EmojiAutocomplete(self)
		self.away.setText(config.DEFAULT_AWAY_MESSAGE)

		fm = self.away.fontMetrics()
		self.away.setFixedHeight(fm.height()+10)
		self.away.setWordWrapMode(QTextOption.NoWrap)
		self.away.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.away.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		wwidth = fm.horizontalAdvance("ABCDEFGHIJKLMNOPQRSTUVWXYZABCD")
		self.away.setMinimumWidth(wwidth)


		awayLayout.addWidget(self.awayLabel)
		awayLayout.addStretch()
		awayLayout.addWidget(self.away)

		self.saveaway = QCheckBox("Save away message as default",self)
		self.saveaway.stateChanged.connect(self.clickSave)

		self.autocomplete = QCheckBox("Autocomplete shortcodes",self)
		self.autocomplete.setChecked(True)

		if not config.ENABLE_EMOJI_SHORTCODES and not config.ENABLE_ASCIIMOJI_SHORTCODES:
			self.autocomplete.setEnabled(False)

		if not config.ENABLE_EMOJI_SHORTCODES:
			self.autocomplete.setChecked(False)
			self.autocomplete.setVisible(False)

		# Buttons
		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		awayInfoBox = QGroupBox("",self)
		awayInfoBox.setLayout(awayLayout)
		awayInfoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(awayInfoBox)
		finalLayout.addWidget(self.autocomplete)
		finalLayout.addWidget(self.saveaway)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
                    ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.away.setFocus()