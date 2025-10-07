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
from PyQt5.QtMultimedia import QSound

from ..resources import *
from .. import config
from .. import dialog
from .. import widgets
from .. import user
from .. import irc
from .. import commands

import emoji

import os,sys,subprocess

import fnmatch

class EmojiQuitAutocomplete(QPlainTextEdit):

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

			if not self.parent.autocompleteEmojisInQuit:
				self.parent.autoEmojiQuit.setFocus()

			elif not config.ENABLE_EMOJI_SHORTCODES:
				self.parent.autoEmojiQuit.setFocus()

			elif not self.parent.enableEmojis.isChecked():
				self.parent.autoEmojiQuit.setFocus()
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

							# Case sensitive
							if fnmatch.fnmatchcase(c,f"{text}*"):
								cursor.beginEditBlock()
								cursor.insertText(c)
								cursor.endEditBlock()
								self.ensureCursorVisible()
								return

							# Case insensitive
							if fnmatch.fnmatch(c,f"{text}*"):
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

class EmojiAwayAutocomplete(QPlainTextEdit):

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

			if not self.parent.autocompleteEmojisInAway:
				self.parent.autoEmojiAway.setFocus()

			elif not config.ENABLE_EMOJI_SHORTCODES:
				self.parent.autoEmojiAway.setFocus()

			elif not self.parent.enableEmojis.isChecked():
				self.parent.autoEmojiAway.setFocus()

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

							# Case sensitive
							if fnmatch.fnmatchcase(c,f"{text}*"):
								cursor.beginEditBlock()
								cursor.insertText(c)
								cursor.endEditBlock()
								self.ensureCursorVisible()
								return

							# Case insensitive
							if fnmatch.fnmatch(c,f"{text}*"):
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

	def boldApply(self):
		font = QFont()
		font.setBold(True)
		if hasattr(self,"saveButton"):
			self.saveButton.setFont(font)

	def selectorClick(self,item):
		self.stack.setCurrentWidget(item.widget)

	def menuFont(self):
		font, ok = QFontDialog.getFont()
		if ok:

			self.newfont = font

			f = font.toString()
			pfs = f.split(',')
			font_name = pfs[0]
			font_size = pfs[1]

			self.fontLabel.setText(f"Font: <b>{font_name}, {font_size} pt</b>")
			self.changed.show()
			self.boldApply()
		self.selector.setFocus()

	def setWinsize(self):
		
		x = dialog.SizeDialog(self)
		if x:
			self.subWidth = x[0]
			self.subHeight = x[1]
			self.sizeLabel.setText(f"Initial subwindow size: <b>{str(self.subWidth)}x{str(self.subHeight)}</b>")
			self.changed.show()
			self.boldApply()
		self.selector.setFocus()

	def setLogSize(self):

		x = dialog.LogSizeDialog(self)
		if x:
			self.logsize = x
			self.logLabel.setText(f"<b>{str(self.logsize)} lines</b>")
			self.changed.show()
			self.boldApply()
		self.selector.setFocus()

	def setHistorySize(self):

		x = dialog.HistorySizeDialog(self)
		if x:
			self.historysize = x
			self.historyLabel.setText(f"History size: <b>{str(self.historysize)} lines</b>")
			self.changed.show()
			self.boldApply()
		self.selector.setFocus()

	def selEnglish(self):
		self.spellLang = "en"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def selFrench(self):
		self.spellLang = "fr"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def selRussian(self):
		self.spellLang = "ru"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def selDutch(self):
		self.spellLang = "nl"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def selItalian(self):
		self.spellLang = "it"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def selPortuguese(self):
		self.spellLang = "pt"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def selGerman(self):
		self.spellLang = "de"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def selSpanish(self):
		self.spellLang = "es"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def selCreation(self):
		self.SET_SUBWINDOW_ORDER = "creation"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def selStacking(self):
		self.SET_SUBWINDOW_ORDER = "stacking"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def selActivation(self):
		self.SET_SUBWINDOW_ORDER = "activation"
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedLoadLogs(self,state):
		if self.loadChanLogs.isChecked() or self.loadPrivLogs.isChecked():
			self.markLog.setEnabled(True)
			self.logsizeButton.setEnabled(True)
			self.logLabel.setEnabled(True)
		else:
			self.markLog.setEnabled(False)
			self.logsizeButton.setEnabled(False)
			self.logLabel.setEnabled(False)

	def changedPrivLogs(self,state):
		if self.savePrivLogs.isChecked() or self.saveChanLogs.isChecked():
			self.intermittentLog.setEnabled(True)
			self.logInterval.setEnabled(True)
		else:
			self.intermittentLog.setEnabled(False)
			self.logInterval.setEnabled(False)

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedChanLogs(self,state):
		if self.saveChanLogs.isChecked():
			self.topicLog.setEnabled(True)
			self.joinLog.setEnabled(True)
			self.partLog.setEnabled(True)
			self.quitLog.setEnabled(True)
			self.nickLog.setEnabled(True)
			self.noticeLog.setEnabled(True)
		else:
			self.topicLog.setEnabled(False)
			self.joinLog.setEnabled(False)
			self.partLog.setEnabled(False)
			self.quitLog.setEnabled(False)
			self.nickLog.setEnabled(False)
			self.noticeLog.setEnabled(False)

		if self.savePrivLogs.isChecked() or self.saveChanLogs.isChecked():
			self.intermittentLog.setEnabled(True)
			self.logInterval.setEnabled(True)
		else:
			self.intermittentLog.setEnabled(False)
			self.logInterval.setEnabled(False)

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedSettingContext(self,state):
		if self.showUserlists.isChecked():
			if self.ulistContext.isChecked():
				self.elideAway.setEnabled(True)
				self.elideHostmask.setEnabled(True)
			else:
				self.elideAway.setEnabled(False)
				self.elideHostmask.setEnabled(False)
		else:
			self.elideAway.setEnabled(False)
			self.elideHostmask.setEnabled(False)

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()


	def changedSetting(self,state):
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedSettingEditor(self,state):
		self.syntax_did_change = True
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedSettingEditorIf(self,state):
		if self.enableIf.isChecked():
			self.syntaxop.setEnabled(True)
		else:
			self.syntaxop.setEnabled(False)

		self.syntax_did_change = True
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedSettingEditorConfig(self,state):
		if self.enableConfig.isChecked():
			self.autocompleteSettings.setEnabled(True)
		else:
			self.autocompleteSettings.setEnabled(False)
		if self.enableUser.isChecked():
			self.autocompleteUser.setEnabled(True)
		else:
			self.autocompleteUser.setEnabled(False)

		self.syntax_did_change = True
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedAutoAway(self,state):
		if self.autoAway.isChecked():
			self.autoawayInterval.setEnabled(True)
			self.typeCancelInput.setEnabled(True)
			self.windowCancelAway.setEnabled(True)
			self.appCancelAway.setEnabled(True)
			self.autoawayInterval.setEnabled(True)
		else:
			self.autoawayInterval.setEnabled(False)
			self.typeCancelInput.setEnabled(False)
			self.windowCancelAway.setEnabled(False)
			self.appCancelAway.setEnabled(False)
			self.autoawayInterval.setEnabled(False)
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedAutocomplete(self,state):
		if self.enableAutocomplete.isChecked():
			self.autocompleteCommands.setEnabled(True)
			self.autocompleteNicks.setEnabled(True)
			self.autocompleteChans.setEnabled(True)
			if self.enableEmojis.isChecked():
				self.autocompleteEmojis.setEnabled(True)
			else:
				self.autocompleteEmojis.setEnabled(False)
			if self.enableAlias.isChecked():
				self.autocompleteAlias.setEnabled(True)
			else:
				self.autocompleteAlias.setEnabled(False)
			self.autocompleteScripts.setEnabled(True)
			self.autocompleteSettings.setEnabled(True)
			self.autocompleteUser.setEnabled(True)
		else:
			self.autocompleteCommands.setEnabled(False)
			self.autocompleteNicks.setEnabled(False)
			self.autocompleteChans.setEnabled(False)
			self.autocompleteEmojis.setEnabled(False)
			self.autocompleteAlias.setEnabled(False)
			self.autocompleteScripts.setEnabled(False)
			self.autocompleteSettings.setEnabled(False)
			self.autocompleteUser.setEnabled(False)

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedHistory(self,state):
		if self.enableHistory.isChecked():
			self.historyButton.setEnabled(True)
			self.historyLabel.setEnabled(True)
		else:
			self.historyButton.setEnabled(False)
			self.historyLabel.setEnabled(False)

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedSettingAdvancedSymbol(self,state):
		self.changed_alias_symbol = True
		self.syntax_did_change = True
		self.changed.show()
		self.restart.show()
		self.boldApply()

	def changedSettingAdvanced(self,state):
		self.changed.show()
		self.restart.show()
		self.boldApply()
		self.selector.setFocus()

	def changedAlias(self,state):
		if self.enableAlias.isChecked():
			self.autocompleteAlias.setEnabled(True)
			self.interpolateAlias.setEnabled(True)
			self.syntaxalias.setEnabled(True)
			self.alias_symbol_label.setEnabled(True)
			self.alias_symbol.setEnabled(True)
			self.autoAliasAway.setEnabled(True)
			self.autoAliasQuit.setEnabled(True)
			self.enableShell.setEnabled(True)
			self.enableBuiltin.setEnabled(True)
		else:
			self.autocompleteAlias.setEnabled(False)
			self.interpolateAlias.setEnabled(False)
			self.syntaxalias.setEnabled(False)
			self.alias_symbol_label.setEnabled(False)
			self.alias_symbol.setEnabled(False)
			self.autoAliasAway.setEnabled(False)
			self.autoAliasQuit.setEnabled(False)
			self.enableShell.setEnabled(False)
			self.enableBuiltin.setEnabled(False)
		self.changed.show()
		self.syntax_did_change = True
		self.boldApply()
		self.selector.setFocus()

	def changedScripting(self,state):
		if self.enableScripts.isChecked():
			self.showErrors.setEnabled(True)
			self.restrictError.setEnabled(True)
			self.haltError.setEnabled(True)
			self.enableInsert.setEnabled(True)
			self.requireArgs.setEnabled(True)
			self.promptScript.setEnabled(True)
			self.enableGoto.setEnabled(True)
			self.enableIf.setEnabled(True)
			self.syntaxop.setEnabled(True)
			self.syntaxscript.setEnabled(True)
			self.enableWait.setEnabled(True)
			self.enableUser.setEnabled(True)
		else:
			self.showErrors.setEnabled(False)
			self.restrictError.setEnabled(False)
			self.haltError.setEnabled(False)
			self.enableInsert.setEnabled(False)
			self.requireArgs.setEnabled(False)
			self.promptScript.setEnabled(False)
			self.enableGoto.setEnabled(False)
			self.enableIf.setEnabled(False)
			self.syntaxop.setEnabled(False)
			self.syntaxscript.setEnabled(False)
			self.enableWait.setEnabled(False)
			self.enableUser.setEnabled(False)
		self.changed.show()
		#self.restart.show()
		self.boldApply()
		self.selector.setFocus()

	def changedInterpolate(self,state):
		if self.interpolateAlias.isChecked():
			self.autocompleteAlias.setEnabled(True)
		else:
			self.autocompleteAlias.setEnabled(False)
		self.syntax_did_change = True
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def setDarkMode(self,state):
		self.changed.show()
		self.restart.show()
		self.boldApply()
		self.selector.setFocus()

	def swapUserlistSetting(self,state):
		self.changed.show()
		self.boldApply()
		self.swapUserlists = True
		self.selector.setFocus()

	def changedSettingRerender(self,state):
		self.changed.show()
		self.boldApply()
		self.rerender = True
		self.selector.setFocus()

	def changedSettingRerenderUserlists(self,state):
		self.changed.show()
		self.boldApply()
		self.rerenderUsers = True
		self.selector.setFocus()

	def changedSettingRerenderNick(self,state):
		self.changed.show()
		self.boldApply()
		self.rerenderNick = True
		self.selector.setFocus()

	def changedSettingRerenderPad(self,state):
		if self.noPadding.isChecked():
			self.padLengthLabel.setEnabled(False)
			self.padLength.setEnabled(False)
			self.padLengthLabelSpec.setEnabled(False)
		else:
			self.padLengthLabel.setEnabled(True)
			self.padLength.setEnabled(True)
			self.padLengthLabelSpec.setEnabled(True)
		self.changed.show()
		self.boldApply()
		self.rerender = True
		self.selector.setFocus()

	def updatePadLength(self,state):
		self.nicknamePadLength = self.padLength.value()
		self.changed.show()
		self.boldApply()
		self.rerender = True
		self.selector.setFocus()

	def changedSettingHostmask(self,state):
		if self.autoHostmasks.isChecked():
			self.fetchFreqLabel.setEnabled(True)
			self.fetchFreq.setEnabled(True)
			self.fetchFreqLabelSpec.setEnabled(True)
		else:
			self.fetchFreqLabel.setEnabled(False)
			self.fetchFreq.setEnabled(False)
			self.fetchFreqLabelSpec.setEnabled(False)
		self.changed.show()
		self.boldApply()
		self.rerender = True
		self.selector.setFocus()

	def updateFreq(self,state):
		self.HOSTMASK_FETCH_FREQUENCY = self.fetchFreq.value()
		self.changed.show()
		self.boldApply()
		self.rerender = True
		self.selector.setFocus()

	def updateDelay(self,state):
		self.RECONNECTION_DELAY = self.delayTime.value()
		self.changed.show()
		self.boldApply()
		self.rerender = True
		self.selector.setFocus()

	def updateinputCursor(self,state):
		self.INPUT_CURSOR_WIDTH = self.inputCursor.value()
		self.changed.show()
		self.boldApply()
		self.rerender = True
		self.selector.setFocus()

	def updateMaxChat(self,state):
		self.IRC_MAX_PAYLOAD_LENGTH = self.maxChat.value()
		self.changed.show()
		self.boldApply()
		self.rerender = True
		self.selector.setFocus()

	def updateHeartbeat(self,state):
		self.heartbeat = self.heartbeatLength.value()
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changeTimestamp(self,state):
		if self.showTimestamps.isChecked():
			self.timestamp24hour.setEnabled(True)
			self.timestampSeconds.setEnabled(True)
		else:
			self.timestamp24hour.setEnabled(False)
			self.timestampSeconds.setEnabled(False)

		self.changed.show()
		self.boldApply()
		self.rerenderNick = True
		self.selector.setFocus()
		
	def changeEmojiAuto(self,state):
		if self.autoEmojiAway.isChecked():
			self.autocompleteEmojisInAway = True
		else:
			self.autocompleteEmojisInAway = False

		self.changed.show()
		self.boldApply()
		self.awayMsg.setFocus()

	def changeEmojiQuit(self,state):
		if self.autoEmojiQuit.isChecked():
			self.autocompleteEmojisInQuit = True
		else:
			self.autocompleteEmojisInQuit = False

		self.changed.show()
		self.boldApply()
		self.awayMsg.setFocus()

	def changedMenuOption(self,state):
		self.changed.show()
		self.boldApply()
		self.windowbar_change = True
		self.selector.setFocus()

	def changeUser(self,state):
		self.user_changed = True
		self.changed.show()
		self.boldApply()

	def setAwayMsg(self):

		self.default_away = self.awayMsg.text()

		self.changed.show()
		self.boldApply()

	def setQuitMsg(self):
		
		self.default_quit_part = self.partMsg.text()

		self.changed.show()
		self.boldApply()

	def underlineChanged(self,data):
		name = data[0]
		if name=="underline":
			color = data[1]
			self.SPELLCHECK_UNDERLINE_COLOR = color
			self.changed.show()
			self.boldApply()
			self.selector.setFocus()

	def syntaxChanged(self,data):
		name = data[0]
		
		if name=="comment":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_COMMENT_COLOR = color
			self.SYNTAX_COMMENT_STYLE = style
			self.changed.show()
			self.boldApply()
		elif name=="command":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_COMMAND_COLOR = color
			self.SYNTAX_COMMAND_STYLE = style
			self.changed.show()
			self.boldApply()
		elif name=="channel":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_CHANNEL_COLOR = color
			self.SYNTAX_CHANNEL_STYLE = style
			self.changed.show()
			self.boldApply()
		elif name=="alias":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_ALIAS_COLOR = color
			self.SYNTAX_ALIAS_STYLE = style
			self.changed.show()
			self.boldApply()
		elif name=="fore":
			color = data[1]
			self.SYNTAX_FOREGROUND = color
			self.changed.show()
			self.boldApply()
		elif name=="back":
			color = data[1]
			self.SYNTAX_BACKGROUND = color
			self.changed.show()
			self.boldApply()
		elif name=="nick":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_NICKNAME_COLOR = color
			self.SYNTAX_NICKNAME_STYLE = style
			self.changed.show()
			self.boldApply()
		elif name=="emoji":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_EMOJI_COLOR = color
			self.SYNTAX_EMOJI_STYLE = style
			self.changed.show()
			self.boldApply()
		elif name=="script":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_SCRIPT_COLOR = color
			self.SYNTAX_SCRIPT_STYLE = style
			self.changed.show()
			self.boldApply()
		elif name=="operator":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_OPERATOR_COLOR = color
			self.SYNTAX_OPERATOR_STYLE = style
			self.changed.show()
			self.boldApply()
		
		self.syntax_did_change = True
		self.selector.setFocus()

	def changedNotifications(self,state):
		if not self.audioNotifications.isChecked():
			self.notifyDisco.setEnabled(False)
			self.notifyNickname.setEnabled(False)
			self.notifyPrivate.setEnabled(False)
			self.notifyNotice.setEnabled(False)
			self.notifyKick.setEnabled(False)
			self.notifyInvite.setEnabled(False)
			self.notifyMode.setEnabled(False)
			self.soundLabel.setEnabled(False)
			self.soundButton.setEnabled(False)
			self.playButton.setEnabled(False)
			self.soundDefaultButton.setEnabled(False)
		else:
			self.notifyDisco.setEnabled(True)
			self.notifyNickname.setEnabled(True)
			self.notifyPrivate.setEnabled(True)
			self.notifyNotice.setEnabled(True)
			self.notifyKick.setEnabled(True)
			self.notifyInvite.setEnabled(True)
			self.notifyMode.setEnabled(True)
			self.soundLabel.setEnabled(True)
			self.soundButton.setEnabled(True)
			self.playButton.setEnabled(True)
			self.soundDefaultButton.setEnabled(True)
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedSystrayMin(self,state):
		if self.showSystray.isChecked():
			self.showSystrayMenu.setEnabled(True)
			if self.showSystrayMenu.isChecked():
				self.stmConnections.setEnabled(True)
				self.stmSettings.setEnabled(True)
				self.stmDirs.setEnabled(True)
				self.stmLinks.setEnabled(True)
				self.stmList.setEnabled(True)
				self.stmLogs.setEnabled(True)
				if not self.stmConnections.isChecked():
					self.stmList.setEnabled(False)
					self.stmLogs.setEnabled(False)
				else:
					self.stmList.setEnabled(True)
					self.stmLogs.setEnabled(True)
			else:
				self.stmConnections.setEnabled(False)
				self.stmSettings.setEnabled(False)
				self.stmDirs.setEnabled(False)
				self.stmLinks.setEnabled(False)
				self.stmList.setEnabled(False)
				self.stmLogs.setEnabled(False)
			self.minSystray.setEnabled(True)
			if self.minSystray.isChecked():
				self.systrayNotify.setEnabled(True)
				self.listSystray.setEnabled(True)
				self.systrayDisconnect.setEnabled(True)
				self.systrayNickname.setEnabled(True)
				self.systrayPrivate.setEnabled(True)
				self.systrayKick.setEnabled(True)
				self.systrayInvite.setEnabled(True)
				self.systrayNotice.setEnabled(True)
				self.systrayMode.setEnabled(True)
				self.systrayMinOnClose.setEnabled(True)
				self.setFlashInterval.setEnabled(True)
				self.flashInterval.setEnabled(True)
				self.doubleclickRestore.setEnabled(True)
				self.clickToMinimize.setEnabled(True)
			else:
				self.systrayNotify.setEnabled(False)
				self.listSystray.setEnabled(False)
				self.systrayDisconnect.setEnabled(False)
				self.systrayNickname.setEnabled(False)
				self.systrayPrivate.setEnabled(False)
				self.systrayKick.setEnabled(False)
				self.systrayInvite.setEnabled(False)
				self.systrayNotice.setEnabled(False)
				self.systrayMode.setEnabled(False)
				self.systrayMinOnClose.setEnabled(False)
				self.setFlashInterval.setEnabled(False)
				self.flashInterval.setEnabled(False)
				self.doubleclickRestore.setEnabled(False)
				self.clickToMinimize.setEnabled(False)
		else:
			self.showSystrayMenu.setEnabled(False)
			self.minSystray.setEnabled(False)
			self.systrayNotify.setEnabled(False)
			self.listSystray.setEnabled(False)
			self.systrayDisconnect.setEnabled(False)
			self.systrayNickname.setEnabled(False)
			self.systrayPrivate.setEnabled(False)
			self.systrayKick.setEnabled(False)
			self.systrayInvite.setEnabled(False)
			self.systrayNotice.setEnabled(False)
			self.systrayMode.setEnabled(False)
			self.systrayMinOnClose.setEnabled(False)
			self.setFlashInterval.setEnabled(False)
			self.flashInterval.setEnabled(False)
			self.doubleclickRestore.setEnabled(False)
			self.clickToMinimize.setEnabled(False)
			self.stmConnections.setEnabled(False)
			self.stmSettings.setEnabled(False)
			self.stmDirs.setEnabled(False)
			self.stmLinks.setEnabled(False)
			self.stmList.setEnabled(False)
			self.stmLogs.setEnabled(False)
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def changedSettingConnections(self,state):
		if not self.stmConnections.isChecked():
			self.stmList.setEnabled(False)
			self.stmLogs.setEnabled(False)
		else:
			self.stmList.setEnabled(True)
			self.stmLogs.setEnabled(True)


	def changedSystrayNotification(self,state):
		if self.systrayNotify.isChecked():
			self.listSystray.setEnabled(True)
			self.systrayDisconnect.setEnabled(True)
			self.systrayNickname.setEnabled(True)
			self.systrayPrivate.setEnabled(True)
			self.systrayKick.setEnabled(True)
			self.systrayInvite.setEnabled(True)
			self.systrayNotice.setEnabled(True)
			self.systrayMode.setEnabled(True)
			self.setFlashInterval.setEnabled(True)
			self.flashInterval.setEnabled(True)
		else:
			self.listSystray.setEnabled(False)
			self.systrayDisconnect.setEnabled(False)
			self.systrayNickname.setEnabled(False)
			self.systrayPrivate.setEnabled(False)
			self.systrayKick.setEnabled(False)
			self.systrayInvite.setEnabled(False)
			self.systrayNotice.setEnabled(False)
			self.systrayMode.setEnabled(False)
			self.setFlashInterval.setEnabled(False)
			self.flashInterval.setEnabled(False)
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def changedMenubarSetting(self,state):
		if self.menubar.isChecked():
			self.menubarFloat.setEnabled(True)
			self.menubarJustify.setEnabled(True)
			self.menubarMenu.setEnabled(True)
			self.alignLabel.setEnabled(True)
			self.menubarTop.setEnabled(True)
			self.menubarBold.setEnabled(True)
		else:
			self.menubarFloat.setEnabled(False)
			self.menubarJustify.setEnabled(False)
			self.menubarMenu.setEnabled(False)
			self.alignLabel.setEnabled(False)
			self.menubarTop.setEnabled(False)
			self.menubarBold.setEnabled(False)
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def changedEmoji(self,state):
		if self.enableEmojis.isChecked():
			self.autocompleteEmojis.setEnabled(True)
			self.syntaxemoji.setEnabled(True)
			self.autoEmojiAway.setEnabled(True)
			self.autoEmojiQuit.setEnabled(True)
		else:
			self.autocompleteEmojis.setEnabled(False)
			self.syntaxemoji.setEnabled(False)
			self.autoEmojiAway.setEnabled(False)
			self.autoEmojiQuit.setEnabled(False)

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def clickedAdvanced(self,state):
		if self.advancedEnable.isChecked():
			self.logEverything.setEnabled(True)
			self.writeConsole.setEnabled(True)
			self.writeFile.setEnabled(True)
			self.enablePing.setEnabled(True)
			self.serverHeartbeatLabel.setEnabled(True)
			self.heartbeatLength.setEnabled(True)
			self.heartbeatLabelSpec.setEnabled(True)
			self.maxChatLabel.setEnabled(True)
			self.maxChat.setEnabled(True)
			self.maxChatLabelSpec.setEnabled(True)
			self.floodProtection.setEnabled(True)
		else:
			self.logEverything.setEnabled(False)
			self.writeConsole.setEnabled(False)
			self.writeFile.setEnabled(False)
			self.enablePing.setEnabled(False)
			self.serverHeartbeatLabel.setEnabled(False)
			self.heartbeatLength.setEnabled(False)
			self.heartbeatLabelSpec.setEnabled(False)
			self.maxChatLabel.setEnabled(False)
			self.maxChat.setEnabled(False)
			self.maxChatLabelSpec.setEnabled(False)
			self.floodProtection.setEnabled(False)

			if config.FLOOD_PROTECTION_FOR_LONG_MESSAGES:
				self.floodProtection.setChecked(True)
			else:
				self.floodProtection.setChecked(False)

			self.maxChat.setValue(config.IRC_MAX_PAYLOAD_LENGTH)
			self.IRC_MAX_PAYLOAD_LENGTH = config.IRC_MAX_PAYLOAD_LENGTH

			self.heartbeatLength.setValue(config.TWISTED_CLIENT_HEARTBEAT)
			self.heartbeat = config.TWISTED_CLIENT_HEARTBEAT

			if config.SHOW_PINGS_IN_CONSOLE:
				self.enablePing.setChecked(True)
			else:
				self.enablePing.setChecked(False)

			self.alias_symbol.setText(config.ALIAS_INTERPOLATION_SYMBOL)

			if config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE: 
				self.logEverything.setChecked(True)
			else:
				self.logEverything.setChecked(False)

			if config.WRITE_INPUT_AND_OUTPUT_TO_CONSOLE:
				self.writeConsole.setChecked(True)
			else:
				self.writeConsole.setChecked(False)

			if config.WRITE_INPUT_AND_OUTPUT_TO_FILE:
				self.writeFile.setChecked(True)
			else:
				self.writeFile.setChecked(False)

		self.selector.setFocus()

	def prependChange(self,i):
		self.system_prepend = self.sysPrepend.itemText(i)

		self.setSystemPrepend.setText(f"Prefix system messages with: <big>{self.system_prepend}</big>")

		if self.system_prepend=="Nothing": self.system_prepend = ''

		self.rerender = True

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def styleChange(self, i):
		self.qt_style = self.qtStyle.itemText(i)

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def flashChange(self,i):
		newInterval = self.flashInterval.itemText(i)
		if newInterval=="250 ms": self.flash = 250
		if newInterval=="500 ms": self.flash = 500
		if newInterval=="750 ms": self.flash = 750
		if newInterval=="1 second": self.flash = 1000

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def intervalChange(self,i):
		newInterval = self.logInterval.itemText(i)
		if newInterval=="30 minutes": self.interval = 1800000
		if newInterval=="hour": self.interval = 3600000
		if newInterval=="15 minutes": self.interval = 900000
		if newInterval=="2 hours": self.interval = 7200000
		if newInterval=="3 hours": self.interval = 10800000

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def topicChange(self, i):
		self.refreshTopics = True

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def titleChange(self, i):
		self.refreshTitles = True

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def mainTopicChange(self, i):
		self.refreshTopics = True

		if self.topicDisplay.isChecked():
			self.topicBold.setEnabled(True)
			self.channelName.setEnabled(True)
			self.showBanlist.setEnabled(True)
			self.showChanMenu.setEnabled(True)
			self.channelCount.setEnabled(True)
		else:
			self.topicBold.setEnabled(False)
			self.channelName.setEnabled(False)
			self.showBanlist.setEnabled(False)
			self.showChanMenu.setEnabled(False)
			self.channelCount.setEnabled(False)

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def changedUserlistVisibility(self,i):
		self.toggleUserlist = True

		if self.showUserlists.isChecked():
			self.plainUserLists.setEnabled(True)
			self.showUserlistLeft.setEnabled(True)
			self.hideScroll.setEnabled(True)
			self.noSelectUserlists.setEnabled(True)
			self.ignoreUserlist.setEnabled(True)
			self.showAwayStatus.setEnabled(True)
			self.dcPrivate.setEnabled(True)
			self.ulistContext.setEnabled(True)

			if self.ulistContext.isChecked():
				self.elideAway.setEnabled(True)
				self.elideHostmask.setEnabled(True)
			else:
				self.elideAway.setEnabled(False)
				self.elideHostmask.setEnabled(False)
		else:
			self.plainUserLists.setEnabled(False)
			self.showUserlistLeft.setEnabled(False)
			self.hideScroll.setEnabled(False)
			self.noSelectUserlists.setEnabled(False)
			self.ignoreUserlist.setEnabled(False)
			self.showAwayStatus.setEnabled(False)
			self.dcPrivate.setEnabled(False)
			self.elideAway.setEnabled(False)
			self.elideHostmask.setEnabled(False)
			self.ulistContext.setEnabled(False)

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def changedSpellcheck(self,i):
		if self.enableSpellcheck.isChecked():
			self.englishSC.setEnabled(True)
			self.frenchSC.setEnabled(True)
			self.spanishSC.setEnabled(True)
			self.germanSC.setEnabled(True)
			self.portugueseSC.setEnabled(True)
			self.italianSC.setEnabled(True)
			self.dutchSC.setEnabled(True)
			self.russianSC.setEnabled(True)
			self.spellcheckDistance.setEnabled(True)
			self.distanceLabel.setEnabled(True)
			self.allowSpellcheck.setEnabled(True)
			self.spellcheckColor.setEnabled(True)
			self.spellcheckBold.setEnabled(True)
			self.spellcheckItalics.setEnabled(True)
			self.spellcheckStrikout.setEnabled(True)
			self.spellcheckMissColor.setEnabled(True)
		else:
			self.englishSC.setEnabled(False)
			self.frenchSC.setEnabled(False)
			self.spanishSC.setEnabled(False)
			self.germanSC.setEnabled(False)
			self.portugueseSC.setEnabled(False)
			self.italianSC.setEnabled(False)
			self.dutchSC.setEnabled(False)
			self.russianSC.setEnabled(False)
			self.spellcheckDistance.setEnabled(False)
			self.distanceLabel.setEnabled(False)
			self.allowSpellcheck.setEnabled(False)
			self.spellcheckColor.setEnabled(False)
			self.spellcheckBold.setEnabled(False)
			self.spellcheckItalics.setEnabled(False)
			self.spellcheckStrikout.setEnabled(False)
			self.spellcheckMissColor.setEnabled(False)

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def changedWindowbarSetting(self,i):
		if self.windowBar.isChecked():
			self.windowBarFloat.setEnabled(True)
			self.windowBarTop.setEnabled(True)
			self.windowBarServers.setEnabled(True)
			self.windowbarJustify.setEnabled(True)
			self.windowBarIcons.setEnabled(True)
			self.windowbarClick.setEnabled(True)
			self.windowBarEditor.setEnabled(True)
			self.windowBarFirst.setEnabled(True)
			self.windowbarMenu.setEnabled(True)
			self.windowbarPrivate.setEnabled(True)
			self.windowbarChannels.setEnabled(True)
			self.windowbarLists.setEnabled(True)
			self.windowBarUnderline.setEnabled(True)
			self.windowBarHover.setEnabled(True)
			self.windowbarLabel.setEnabled(True)
			self.windowbarManager.setEnabled(True)
			self.windowbarUnread.setEnabled(True)
			self.windowbarEntryMenu.setEnabled(True)
			self.serverHidden.setEnabled(True)
			self.windowbarItalics.setEnabled(True)
			self.channelHidden.setEnabled(True)
			self.privateHidden.setEnabled(True)
			self.autoHide.setEnabled(True)
			self.windowbarReadme.setEnabled(True)
			self.windowBarBold.setEnabled(True)
		else:
			self.windowBarFloat.setEnabled(False)
			self.windowBarTop.setEnabled(False)
			self.windowBarServers.setEnabled(False)
			self.windowbarJustify.setEnabled(False)
			self.windowBarIcons.setEnabled(False)
			self.windowbarClick.setEnabled(False)
			self.windowBarEditor.setEnabled(False)
			self.windowBarFirst.setEnabled(False)
			self.windowbarMenu.setEnabled(False)
			self.windowbarPrivate.setEnabled(False)
			self.windowbarChannels.setEnabled(False)
			self.windowbarLists.setEnabled(False)
			self.windowBarUnderline.setEnabled(False)
			self.windowBarHover.setEnabled(False)
			self.windowbarLabel.setEnabled(False)
			self.windowbarManager.setEnabled(False)
			self.windowbarUnread.setEnabled(False)
			self.windowbarEntryMenu.setEnabled(False)
			self.serverHidden.setEnabled(False)
			self.windowbarItalics.setEnabled(False)
			self.channelHidden.setEnabled(False)
			self.privateHidden.setEnabled(False)
			self.autoHide.setEnabled(False)
			self.windowbarReadme.setEnabled(False)
			self.windowBarBold.setEnabled(False)

		self.windowbar_change = True
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def distanceChange(self,i):
		self.spellcheck_distance = int(self.spellcheckDistance.itemText(i))

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def justifyChange(self, i):
		self.windowbar_justify = self.windowbarJustify.itemText(i)

		self.windowbar_change = True
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def menuJustifyChange(self,i):

		self.menubar_justify = self.menubarJustify.itemText(i)

		self.windowbar_change = True
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def menuChange(self,i):

		self.windowbar_change = True
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def setMainMenu(self):
		info = dialog.SetMenuNameDialog(self.default_main_menu,self)

		if not info: return None

		self.default_main_menu = info
		self.mainName.setText("<b>"+str(info)+"</b>")

		self.windowbar_change = True

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def setSettingsMenu(self):
		info = dialog.SetMenuNameDialog(self.default_settings_menu,self)

		if not info: return None

		self.default_settings_menu = info
		self.settingsName.setText("<b>"+str(info)+"</b>")

		self.windowbar_change = True

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def setToolsMenu(self):
		info = dialog.SetMenuNameDialog(self.default_tools_menu,self)

		if not info: return None

		self.default_tools_menu = info
		self.toolsName.setText("<b>"+str(info)+"</b>")

		self.windowbar_change = True

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def setWindowsMenu(self):
		info = dialog.SetMenuNameDialog(self.default_windows_menu,self)

		if not info: return None

		self.default_windows_menu = info
		self.windowsName.setText("<b>"+str(info)+"</b>")

		self.windowbar_change = True

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changeSettingStyle(self,state):
		self.rerenderStyle = True

		if self.forceDefault.isChecked():
			self.notInputWidget.setEnabled(False)
			self.notUserlist.setEnabled(False)
		else:
			self.notInputWidget.setEnabled(True)
			self.notUserlist.setEnabled(True)

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def setHelpMenu(self):
		info = dialog.SetMenuNameDialog(self.default_help_menu,self)

		if not info: return None

		self.default_help_menu = info
		self.helpName.setText("<b>"+str(info)+"</b>")

		self.windowbar_change = True

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def do_restart(self, link):
		self.save()

		if is_running_from_pyinstaller():
			subprocess.Popen([sys.executable])
			self.parent.close()
			self.parent.app.exit()
		else:
			os.execl(sys.executable, sys.executable, *sys.argv)
			sys.exit()

	def playSound(self):
		QSound.play(self.sound)
		self.selector.setFocus()
	
	def soundDefault(self):
		self.sound = BELL_NOTIFICATION

		bname = os.path.basename(self.sound)
		self.soundLabel.setText("<b>"+bname+"</b>")

		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def show_error_message(self,title, message):
		msg_box = QMessageBox()
		msg_box.setIcon(QMessageBox.Critical)
		msg_box.setWindowTitle(title)
		msg_box.setWindowIcon(QIcon(APPLICATION_ICON))
		msg_box.setText(message)
		msg_box.setStandardButtons(QMessageBox.Ok)
		msg_box.exec_()

	def setSound(self):
		desktop =  os.path.join(os.path.expanduser("~"), "Desktop")
		if not os.path.isdir(desktop): desktop = os.path.expanduser("~")
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open WAV", desktop, f"WAV file (*.wav)", options=options)
		if fileName:
			if is_wav_file(fileName):
				self.sound = fileName
				bname = os.path.basename(self.sound)
				self.soundLabel.setText("<b>"+bname+"</b>")

				self.changed.show()
				self.boldApply()
			else:
				self.show_error_message("Wrong file type","File is not a WAV file!\nOnly WAV files can be used as a notification.\nPlease select a valid file.")
		self.selector.setFocus()

	def autoawayChange(self,i):
		newInterval = self.autoawayInterval.itemText(i)
		if newInterval=="5 minutes": self.awayInterval = 300
		if newInterval=="30 minutes": self.awayInterval = 1800
		if newInterval=="1 hour": self.awayInterval = 3600
		if newInterval=="15 minutes": self.awayInterval = 900
		if newInterval=="2 hours": self.awayInterval = 7200
		if newInterval=="3 hours": self.awayInterval = 10800

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def eventFilter(self, source, event):
		if source == self.selector.viewport() and event.type() == QEvent.Wheel:
			return True
		return super().eventFilter(source, event)

	def __init__(self,app=None,parent=None):
		super(Dialog,self).__init__(parent)

		self.app = app
		self.parent = parent

		self.setFont(self.parent.application_font)

		# Load in user settings
		user.load_user(user.USER_FILE)

		# Load in config settings
		config.load_settings(config.CONFIG_FILE)

		self.newfont = None
		self.subWidth = config.DEFAULT_SUBWINDOW_WIDTH
		self.subHeight = config.DEFAULT_SUBWINDOW_HEIGHT
		self.logsize = config.MAXIMUM_LOADED_LOG_SIZE
		self.historysize = config.COMMAND_HISTORY_LENGTH
		self.spellLang = config.DEFAULT_SPELLCHECK_LANGUAGE
		self.rerender = False
		self.default_quit_part = config.DEFAULT_QUIT_MESSAGE
		self.rerenderUsers = False
		self.rerenderNick = False
		self.default_away = config.DEFAULT_AWAY_MESSAGE
		self.SYNTAX_COMMENT_COLOR = config.SYNTAX_COMMENT_COLOR
		self.SYNTAX_COMMENT_STYLE = config.SYNTAX_COMMENT_STYLE
		self.SYNTAX_COMMAND_COLOR = config.SYNTAX_COMMAND_COLOR
		self.SYNTAX_COMMAND_STYLE = config.SYNTAX_COMMAND_STYLE
		self.SYNTAX_CHANNEL_COLOR = config.SYNTAX_CHANNEL_COLOR
		self.SYNTAX_CHANNEL_STYLE = config.SYNTAX_CHANNEL_STYLE
		self.SYNTAX_BACKGROUND = config.SYNTAX_BACKGROUND
		self.SYNTAX_FOREGROUND = config.SYNTAX_FOREGROUND
		self.SYNTAX_ALIAS_COLOR = config.SYNTAX_ALIAS_COLOR
		self.SYNTAX_ALIAS_STYLE = config.SYNTAX_ALIAS_STYLE
		self.SYNTAX_NICKNAME_COLOR = config.SYNTAX_NICKNAME_COLOR
		self.SYNTAX_NICKNAME_STYLE = config.SYNTAX_NICKNAME_STYLE
		self.SYNTAX_EMOJI_COLOR = config.SYNTAX_EMOJI_COLOR
		self.SYNTAX_EMOJI_STYLE = config.SYNTAX_EMOJI_STYLE
		self.SYNTAX_SCRIPT_COLOR = config.SYNTAX_SCRIPT_COLOR
		self.SYNTAX_SCRIPT_STYLE = config.SYNTAX_SCRIPT_STYLE
		self.SYNTAX_OPERATOR_COLOR = config.SYNTAX_OPERATOR_COLOR
		self.SYNTAX_OPERATOR_STYLE = config.SYNTAX_OPERATOR_STYLE
		self.SPELLCHECK_UNDERLINE_COLOR = config.SPELLCHECK_UNDERLINE_COLOR
		self.qt_style = config.QT_WINDOW_STYLE
		self.windowbar_justify = config.WINDOWBAR_JUSTIFY
		self.menubar_justify = config.MENUBAR_JUSTIFY
		self.system_prepend = config.SYSTEM_MESSAGE_PREFIX
		self.autocompleteEmojisInAway = config.AUTOCOMPLETE_EMOJIS_IN_AWAY_MESSAGE_WIDGET
		self.autocompleteEmojisInQuit = config.AUTOCOMPLETE_EMOJIS_IN_QUIT_MESSAGE_WIDGET
		self.user_changed = False
		self.refreshTopics = False
		self.refreshTitles = False
		self.swapUserlists = False
		self.toggleUserlist = False
		self.rerenderStyle = False
		self.windowbar_change = False
		self.changed_alias_symbol = False
		self.default_main_menu = config.MAIN_MENU_IRC_NAME
		self.default_tools_menu = config.MAIN_MENU_TOOLS_NAME
		self.default_windows_menu = config.MAIN_MENU_WINDOWS_NAME
		self.default_help_menu = config.MAIN_MENU_HELP_NAME
		self.default_settings_menu = config.MAIN_MENU_SETTINGS_NAME
		self.interval = config.LOG_SAVE_INTERVAL
		self.awayInterval = config.AUTOAWAY_TIME
		self.flash = config.FLASH_SYSTRAY_SPEED
		self.sound = config.SOUND_NOTIFICATION_FILE
		self.syntax_did_change = False
		self.spellcheck_distance = config.SPELLCHECKER_DISTANCE
		self.nicknamePadLength = config.NICKNAME_PAD_LENGTH
		self.heartbeat = config.TWISTED_CLIENT_HEARTBEAT
		self.SET_SUBWINDOW_ORDER = config.SET_SUBWINDOW_ORDER
		self.INPUT_CURSOR_WIDTH = config.INPUT_CURSOR_WIDTH
		self.HOSTMASK_FETCH_FREQUENCY = config.HOSTMASK_FETCH_FREQUENCY
		self.RECONNECTION_DELAY = config.RECONNECTION_DELAY
		self.IRC_MAX_PAYLOAD_LENGTH = config.IRC_MAX_PAYLOAD_LENGTH

		self.setWindowTitle(f"Settings")
		self.setWindowIcon(QIcon(SETTINGS_ICON))

		self.selector = QListWidget(self)
		self.stack = QStackedWidget(self)

		# Prevent users from scrolling the selector with the
		# mouse wheel, or anything else
		self.selector.viewport().installEventFilter(self)
		self.selector.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.selector.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		f = self.selector.font()
		f.setBold(True)
		self.selector.setFont(f)

		self.changed = QLabel("<b>Settings changed.</b>&nbsp;&nbsp;")

		fm = QFontMetrics(self.font())
		fwidth = fm.width('X') * 22
		self.selector.setMaximumWidth(fwidth)

		add_factor = 13
		self.selector.setIconSize(QSize(fm.height()+add_factor,fm.height()+add_factor))

		self.selector.itemClicked.connect(self.selectorClick)

		self.selector.setStyleSheet("background-color: transparent; border-width: 0px; border-color: transparent;")

		# BEGIN PAGES

		# Application page

		self.applicationPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Application")
		entry.widget = self.applicationPage
		entry.setIcon(QIcon(APPLICATION_ICON))
		self.selector.addItem(entry)
		self.selector.setCurrentItem(entry)

		self.stack.addWidget(self.applicationPage)
		self.stack.setCurrentWidget(self.applicationPage)

		f = self.font()
		fs = f.toString()
		pfs = fs.split(',')
		font_name = pfs[0]
		font_size = pfs[1]

		self.fontLabel = QLabel(f"Font: <b>{font_name}, {font_size} pt</b>",self)

		fontButton = QPushButton("")
		fontButton.clicked.connect(self.menuFont)
		fontButton.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		fontButton.setFixedSize(fheight +10,fheight + 10)
		fontButton.setIcon(QIcon(FONT_ICON))
		fontButton.setToolTip("Change font")

		fontLayout = QHBoxLayout()
		fontLayout.addWidget(fontButton)
		fontLayout.addWidget(self.fontLabel)

		self.sizeLabel = QLabel(f"Initial subwindow size: <b>{str(self.subWidth)}x{str(self.subHeight)}</b>",self)

		sizeButton = QPushButton("")
		sizeButton.clicked.connect(self.setWinsize)
		sizeButton.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		sizeButton.setFixedSize(fheight +10,fheight + 10)
		sizeButton.setIcon(QIcon(EDIT_ICON))
		sizeButton.setToolTip("Change default window size")

		sizeLayout = QHBoxLayout()
		sizeLayout.addWidget(sizeButton)
		sizeLayout.addWidget(self.sizeLabel)

		self.simpleConnect = QCheckBox("Simplified dialogs",self)
		if config.SIMPLIFIED_DIALOGS: self.simpleConnect.setChecked(True)
		self.simpleConnect.stateChanged.connect(self.changedSetting)
		
		self.maxOnStart = QCheckBox("Maximize on startup",self)
		if config.MAXIMIZE_ON_STARTUP: self.maxOnStart.setChecked(True)
		self.maxOnStart.stateChanged.connect(self.changedSetting)

		self.alwaysOnTop = QCheckBox("Always on top",self)
		if config.ALWAYS_ON_TOP: self.alwaysOnTop.setChecked(True)
		self.alwaysOnTop.stateChanged.connect(self.changedSetting)

		self.askBeforeExit = QCheckBox("Ask before closing app",self)
		if config.ASK_BEFORE_CLOSE: self.askBeforeExit.setChecked(True)
		self.askBeforeExit.stateChanged.connect(self.changedSetting)

		self.noAppNameTitle = QCheckBox("Do not show application name in\napplication title",self)
		if config.DO_NOT_SHOW_APPLICATION_NAME_IN_TITLE: self.noAppNameTitle.setChecked(True)
		self.noAppNameTitle.stateChanged.connect(self.changedSetting)
		self.noAppNameTitle.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.noConnectLogo = QCheckBox(f"Hide {APPLICATION_NAME} logo on the initial\nconnection dialog",self)
		if config.HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG: self.noConnectLogo.setChecked(True)
		self.noConnectLogo.stateChanged.connect(self.changedSetting)
		self.noConnectLogo.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showConnect = QCheckBox("Show connection dialog on startup",self)
		if config.ASK_FOR_SERVER_ON_STARTUP: self.showConnect.setChecked(True)
		self.showConnect.stateChanged.connect(self.changedSetting)

		self.fullScreen = QCheckBox("Full screen",self)
		if config.SHOW_FULL_SCREEN: self.fullScreen.setChecked(True)
		self.fullScreen.stateChanged.connect(self.changedSetting)

		self.showTopicInTitle = QCheckBox("Show current channel topic in\napplication title",self)
		if config.SHOW_CHANNEL_TOPIC_IN_APPLICATION_TITLE: self.showTopicInTitle.setChecked(True)
		self.showTopicInTitle.stateChanged.connect(self.changedSetting)
		self.showTopicInTitle.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.noShowServerTitle = QCheckBox("Do not show server in application\ntitle",self)
		if config.DO_NOT_SHOW_SERVER_IN_TITLE: self.noShowServerTitle.setChecked(True)
		self.noShowServerTitle.stateChanged.connect(self.changedSetting)
		self.noShowServerTitle.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showChatInTitle = QCheckBox("Show active subwindow title in\napplication title",self)
		if config.DISPLAY_ACTIVE_CHAT_IN_TITLE: self.showChatInTitle.setChecked(True)
		self.showChatInTitle.stateChanged.connect(self.changedSetting)
		self.showChatInTitle.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		screenLayout2 = QHBoxLayout()
		screenLayout2.addStretch()
		screenLayout2.addWidget(self.alwaysOnTop)
		screenLayout2.addWidget(self.fullScreen)
		screenLayout2.addStretch()

		screenLayout = QHBoxLayout()
		screenLayout.addStretch()
		screenLayout.addWidget(self.maxOnStart)
		screenLayout.addStretch()

		screenLayout3 = QHBoxLayout()
		screenLayout3.addStretch()
		screenLayout3.addWidget(self.askBeforeExit)
		screenLayout3.addStretch()

		applicationLayout = QVBoxLayout()
		applicationLayout.addWidget(widgets.textSeparatorLabel(self,"<b>application settings</b>"))
		applicationLayout.addLayout(fontLayout)
		applicationLayout.addLayout(sizeLayout)
		applicationLayout.addWidget(QLabel(' '))
		applicationLayout.addWidget(widgets.textSeparatorLabel(self,"<b>main window</b>"))
		applicationLayout.addLayout(screenLayout)
		applicationLayout.addLayout(screenLayout2)
		applicationLayout.addLayout(screenLayout3)
		applicationLayout.addWidget(QLabel(' '))
		applicationLayout.addWidget(widgets.textSeparatorLabel(self,"<b>application title</b>"))
		applicationLayout.addWidget(self.noAppNameTitle)
		applicationLayout.addWidget(self.noShowServerTitle)
		applicationLayout.addWidget(self.showTopicInTitle)
		applicationLayout.addWidget(self.showChatInTitle)
		applicationLayout.addWidget(QLabel(' '))
		applicationLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous</b>"))
		applicationLayout.addWidget(self.simpleConnect)
		applicationLayout.addWidget(self.showConnect)
		applicationLayout.addWidget(self.noConnectLogo)
		applicationLayout.addStretch()

		self.applicationPage.setLayout(applicationLayout)

		# Widget page

		self.appearancePage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Appearance")
		entry.widget = self.appearancePage
		entry.setIcon(QIcon(STYLE_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.appearancePage)

		self.styleDescription = QLabel("""
			<small>
			This setting controls how <b>subwindows</b> and <b>widgets</b> look. Different <b>styles</b>
			use different sets of <b>widgets</b>. Qt comes with a number of them
			pre-installed, and you can select which one to use here. The selected
			<b>widget style</b> will be applied immediately without having
			to restart the application.
			</small>
			<br>
			""")
		self.styleDescription.setWordWrap(True)
		self.styleDescription.setAlignment(Qt.AlignJustify)

		self.qtStyle = QComboBox(self)
		self.qtStyle.addItem(config.QT_WINDOW_STYLE)
		for s in QStyleFactory.keys():
			if s==config.QT_WINDOW_STYLE: continue
			self.qtStyle.addItem(s)
		self.qtStyle.currentIndexChanged.connect(self.styleChange)

		styleLayout = QHBoxLayout()
		styleLayout.addWidget(QLabel("Widget Style "))
		styleLayout.addWidget(self.qtStyle)
		styleLayout.addStretch()

		self.darkDescription = QLabel("""
			<small>
			<b>Dark mode</b> changes the application palette to darker colors, which
			is supposed to decrease eye strain. Text display colors are unchanged,
			as those are set and controlled by the text style system.
			<br><br>
			<b>If dark mode is enabled or disabled, the application must be restarted to use the
			new palette.</b>
			</small>
			
			""")
		self.darkDescription.setWordWrap(True)
		self.darkDescription.setAlignment(Qt.AlignJustify)

		self.darkMode = QCheckBox("Enable dark mode",self)
		if config.DARK_MODE: self.darkMode.setChecked(True)
		self.darkMode.stateChanged.connect(self.setDarkMode)

		self.forceDefault = QCheckBox("Chat windows",self)
		if config.FORCE_DEFAULT_STYLE: self.forceDefault.setChecked(True)
		self.forceDefault.stateChanged.connect(self.changeSettingStyle)

		self.notInputWidget = QCheckBox("Text input widgets",self)
		if config.DO_NOT_APPLY_STYLE_TO_INPUT_WIDGET: self.notInputWidget.setChecked(True)
		self.notInputWidget.stateChanged.connect(self.changeSettingStyle)

		self.notUserlist = QCheckBox("Userlists",self)
		if config.DO_NOT_APPLY_STYLE_TO_USERLIST: self.notUserlist.setChecked(True)
		self.notUserlist.stateChanged.connect(self.changeSettingStyle)

		if config.FORCE_DEFAULT_STYLE:
			self.notInputWidget.setEnabled(False)
			self.notUserlist.setEnabled(False)

		self.noStyles = QCheckBox("Do not apply text styles",self)
		if config.DO_NOT_APPLY_STYLES_TO_TEXT: self.noStyles.setChecked(True)
		self.noStyles.stateChanged.connect(self.changedSettingRerender)
	
		app1Layout = QHBoxLayout()
		app1Layout.addStretch()
		app1Layout.addLayout(styleLayout)
		app1Layout.addStretch()

		app2Layout = QHBoxLayout()
		app2Layout.addStretch()
		app2Layout.addWidget(self.darkMode)
		app2Layout.addStretch()

		forceLayout = QFormLayout()
		forceLayout.addRow(self.forceDefault,self.notInputWidget)
		forceLayout.addRow(self.notUserlist)

		self.forceMono = QCheckBox("Force monospace rendering\nof all message text",self)
		if config.FORCE_MONOSPACE_RENDERING: self.forceMono.setChecked(True)
		self.forceMono.stateChanged.connect(self.changedSettingRerender)
		self.forceMono.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.inputCursorLabel = QLabel("Input cursor width:")
		self.inputCursorLabelSpec = QLabel("pixels")
		self.inputCursor = QSpinBox()
		self.inputCursor.setRange(1,99)
		self.inputCursor.setValue(self.INPUT_CURSOR_WIDTH)
		self.inputCursor.valueChanged.connect(self.updateinputCursor)

		cursorLayout = QHBoxLayout()
		cursorLayout.addWidget(self.inputCursorLabel)
		cursorLayout.addWidget(self.inputCursor)
		cursorLayout.addWidget(self.inputCursorLabelSpec)
		cursorLayout.addStretch()

		self.enableStyle = QCheckBox("Enable text style editor",self)
		if config.ENABLE_STYLE_EDITOR: self.enableStyle.setChecked(True)
		self.enableStyle.stateChanged.connect(self.changedSettingAdvanced)

		appearanceLayout = QVBoxLayout()
		appearanceLayout.addWidget(widgets.textSeparatorLabel(self,"<b>dark mode</b>"))
		appearanceLayout.addWidget(self.darkDescription)
		appearanceLayout.addLayout(app2Layout)
		appearanceLayout.addWidget(widgets.textSeparatorLabel(self,"<b>widget style</b>"))
		appearanceLayout.addWidget(self.styleDescription)
		appearanceLayout.addLayout(app1Layout)
		appearanceLayout.addWidget(QLabel(' '))
		appearanceLayout.addWidget(widgets.textSeparatorLabel(self,"<b>force default text style on...</b>"))
		appearanceLayout.addLayout(forceLayout)
		appearanceLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous</b>"))
		appearanceLayout.addWidget(self.enableStyle)
		appearanceLayout.addWidget(self.noStyles)
		appearanceLayout.addWidget(self.forceMono)
		appearanceLayout.addLayout(cursorLayout)
		appearanceLayout.addStretch()

		self.appearancePage.setLayout(appearanceLayout)

		# Menubar page

		self.menuPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Menus & Menubar")
		entry.widget = self.menuPage
		entry.setIcon(QIcon(MENU_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.menuPage)

		self.menubarDescription = QLabel("""
			<small>
			The <b>menubar</b> is a toolbar widget that takes the place of the menus of a
			"normal" application. The <b>menubar</b> can be moved to either the <b>top</b>
			of the main window, the <b>bottom</b> of the main window, or can be optionally
			<b>movable</b>. The <b>menubar</b> is turned on by default,
			but can be turned off if normal application menus are desired.
			</small>
			""")
		self.menubarDescription.setWordWrap(True)
		self.menubarDescription.setAlignment(Qt.AlignJustify)

		self.menubar = QCheckBox("Enable menubar",self)
		if config.USE_MENUBAR: self.menubar.setChecked(True)
		self.menubar.stateChanged.connect(self.changedMenubarSetting)

		self.menubarFloat = QCheckBox("Movable",self)
		if config.MENUBAR_CAN_FLOAT: self.menubarFloat.setChecked(True)
		self.menubarFloat.stateChanged.connect(self.menuChange)

		self.menubarJustify = QComboBox(self)
		self.menubarJustify.addItem(config.MENUBAR_JUSTIFY)
		if config.MENUBAR_JUSTIFY!='center': self.menubarJustify.addItem('center')
		if config.MENUBAR_JUSTIFY!='left': self.menubarJustify.addItem('left')
		if config.MENUBAR_JUSTIFY!='right': self.menubarJustify.addItem('right')
		self.menubarJustify.currentIndexChanged.connect(self.menuJustifyChange)

		self.menubarMenu = QCheckBox("Context menu",self)
		if config.MENUBAR_MENU: self.menubarMenu.setChecked(True)
		self.menubarMenu.stateChanged.connect(self.menuChange)

		self.alignLabel = QLabel("Menubar alignment ")

		if not config.USE_MENUBAR:
			self.menubarFloat.setEnabled(False)
			self.menubarJustify.setEnabled(False)
			self.menubarMenu.setEnabled(False)
			self.alignLabel.setEnabled(False)

		justifyLayout = QHBoxLayout()
		justifyLayout.addStretch()
		justifyLayout.addWidget(self.alignLabel)
		justifyLayout.addWidget(self.menubarJustify)
		justifyLayout.addStretch()

		self.mainName = QLabel("<b>"+self.default_main_menu+"</b>")

		self.setMainName = QPushButton("")
		self.setMainName.clicked.connect(self.setMainMenu)
		self.setMainName.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setMainName.setFixedSize(fheight +10,fheight + 10)
		self.setMainName.setIcon(QIcon(EDIT_ICON))
		self.setMainName.setToolTip("Set main menu name")

		setMainLayout = QHBoxLayout()
		
		setMainLayout.addWidget(self.setMainName)
		setMainLayout.addWidget(self.mainName)
		setMainLayout.addStretch()

		self.toolsName = QLabel("<b>"+self.default_tools_menu+"</b>")

		self.setToolsName = QPushButton("")
		self.setToolsName.clicked.connect(self.setToolsMenu)
		self.setToolsName.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setToolsName.setFixedSize(fheight +10,fheight + 10)
		self.setToolsName.setIcon(QIcon(EDIT_ICON))
		self.setToolsName.setToolTip("Set tools menu name")

		setToolsLayout = QHBoxLayout()
		
		setToolsLayout.addWidget(self.setToolsName)
		setToolsLayout.addWidget(self.toolsName)
		setToolsLayout.addStretch()

		self.windowsName = QLabel("<b>"+self.default_windows_menu+"</b>")

		self.setWindowsName = QPushButton("")
		self.setWindowsName.clicked.connect(self.setWindowsMenu)
		self.setWindowsName.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setWindowsName.setFixedSize(fheight +10,fheight + 10)
		self.setWindowsName.setIcon(QIcon(EDIT_ICON))
		self.setWindowsName.setToolTip("Set windows menu name")

		setWindowsLayout = QHBoxLayout()
		
		setWindowsLayout.addWidget(self.setWindowsName)
		setWindowsLayout.addWidget(self.windowsName)
		setWindowsLayout.addStretch()

		self.helpName = QLabel("<b>"+self.default_help_menu+"</b>")

		self.setHelpName = QPushButton("")
		self.setHelpName.clicked.connect(self.setHelpMenu)
		self.setHelpName.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setHelpName.setFixedSize(fheight +10,fheight + 10)
		self.setHelpName.setIcon(QIcon(EDIT_ICON))
		self.setHelpName.setToolTip("Set help menu name")

		setHelpLayout = QHBoxLayout()
		
		setHelpLayout.addWidget(self.setHelpName)
		setHelpLayout.addWidget(self.helpName)
		setHelpLayout.addStretch()

		mainMenuEntry = QVBoxLayout()
		mainMenuEntry.addWidget(QLabel("<b>Main menu</b>"))
		mainMenuEntry.addLayout(setMainLayout)
		
		toolsMenuEntry = QVBoxLayout()
		toolsMenuEntry.addWidget(QLabel("<b>Tools menu</b>"))
		toolsMenuEntry.addLayout(setToolsLayout)

		windowsMenuEntry = QVBoxLayout()
		windowsMenuEntry.addWidget(QLabel("<b>Windows menu</b>"))
		windowsMenuEntry.addLayout(setWindowsLayout)

		helpMenuEntry = QVBoxLayout()
		helpMenuEntry.addWidget(QLabel("<b>Help menu</b>"))
		helpMenuEntry.addLayout(setHelpLayout)

		self.settingsName = QLabel("<b>"+self.default_settings_menu+"</b>")

		self.setSettingsName = QPushButton("")
		self.setSettingsName.clicked.connect(self.setSettingsMenu)
		self.setSettingsName.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setSettingsName.setFixedSize(fheight +10,fheight + 10)
		self.setSettingsName.setIcon(QIcon(EDIT_ICON))
		self.setSettingsName.setToolTip("Set settings menu name")

		setMainLayout = QHBoxLayout()
		
		setMainLayout.addWidget(self.setSettingsName)
		setMainLayout.addWidget(self.settingsName)
		setMainLayout.addStretch()

		settingsMenuEntry = QVBoxLayout()
		settingsMenuEntry.addWidget(QLabel("<b>Settings menu</b>"))
		settingsMenuEntry.addLayout(setMainLayout)

		menuLineOne = QHBoxLayout()
		menuLineOne.addLayout(mainMenuEntry)
		menuLineOne.addLayout(settingsMenuEntry)

		menuLineTwo = QHBoxLayout()
		menuLineTwo.addLayout(toolsMenuEntry)
		menuLineTwo.addLayout(windowsMenuEntry)

		menuLineThree = QHBoxLayout()
		menuLineThree.addLayout(helpMenuEntry)

		nameMenuEntries = QFormLayout()
		nameMenuEntries.addRow(menuLineOne)
		nameMenuEntries.addRow(menuLineTwo)
		nameMenuEntries.addRow(menuLineThree)

		self.menuNameDescription = QLabel("""
			<small>
			Here, you can set the names used to display the main application
			<b>menus</b>. These are purely cosmetic, and don't change functionality at
			all. These names will be displayed even if the <b>menubar</b> is disabled,
			and normal menus are used.
			</small>
			""")
		self.menuNameDescription.setWordWrap(True)
		self.menuNameDescription.setAlignment(Qt.AlignJustify)

		menu1Layout = QHBoxLayout()
		menu1Layout.addStretch()
		menu1Layout.addWidget(self.menubar)
		menu1Layout.addStretch()

		self.menubarTop = QCheckBox("Display at top",self)
		if config.MENUBAR_DOCKED_AT_TOP: self.menubarTop.setChecked(True)
		self.menubarTop.stateChanged.connect(self.menuChange)

		self.menubarBold = QCheckBox("Bold entries on mouse hover",self)
		if config.MENUBAR_HOVER_EFFECT: self.menubarBold.setChecked(True)
		self.menubarBold.stateChanged.connect(self.menuChange)

		if not config.USE_MENUBAR:
			self.menubarFloat.setEnabled(False)
			self.menubarJustify.setEnabled(False)
			self.menubarMenu.setEnabled(False)
			self.alignLabel.setEnabled(False)
			self.menubarTop.setEnabled(False)
			self.menubarBold.setEnabled(False)

		menu2Layout = QHBoxLayout()
		menu2Layout.addStretch()
		menu2Layout.addWidget(self.menubarFloat)
		menu2Layout.addWidget(self.menubarTop)
		menu2Layout.addStretch()

		self.showChannelList = QCheckBox(f"Channel list options",self)
		if config.SHOW_CHANNEL_LIST_IN_WINDOWS_MENU: self.showChannelList.setChecked(True)
		self.showChannelList.stateChanged.connect(self.changedSetting)
		
		self.showLogsInWindows = QCheckBox(f"Network logs",self)
		if config.SHOW_LOGS_IN_WINDOWS_MENU: self.showLogsInWindows.setChecked(True)
		self.showLogsInWindows.stateChanged.connect(self.changedSetting)

		self.showServerInfo = QCheckBox(f"Server information",self)
		if config.SHOW_SERVER_INFO_IN_WINDOWS_MENU: self.showServerInfo.setChecked(True)
		self.showServerInfo.stateChanged.connect(self.changedSetting)

		menu3Layout = QHBoxLayout()
		menu3Layout.addWidget(self.showChannelList)
		menu3Layout.addWidget(self.showLogsInWindows)

		menuLayout = QVBoxLayout()
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>menubar settings</b>"))
		menuLayout.addWidget(self.menubarDescription)
		menuLayout.addLayout(menu1Layout)
		menuLayout.addLayout(menu2Layout)
		menuLayout.addLayout(justifyLayout)
		menuLayout.addWidget(self.menubarBold)
		menuLayout.addWidget(self.menubarMenu)
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>menu display names</b>"))
		menuLayout.addWidget(self.menuNameDescription)
		menuLayout.addLayout(nameMenuEntries)
		menuLayout.addWidget(widgets.textSeparatorLabel(self,f"<b>\"{config.MAIN_MENU_WINDOWS_NAME}\" menu includes...</b>"))
		menuLayout.addLayout(menu3Layout)
		menuLayout.addWidget(self.showServerInfo)
		menuLayout.addStretch()

		self.menuPage.setLayout(menuLayout)

		# Windowbar page

		self.windowbarPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Windowbar")
		entry.widget = self.windowbarPage
		entry.setIcon(QIcon(WINDOW_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.windowbarPage)

		self.windowbarDescription = QLabel("""
			<small>
			The <b>windowbar</b> is a toolbar widget that lists all (or some) of the open
			subwindows and allows you to switch between them by clicking on
			the subwindow's name.
			</small>
			""")
		self.windowbarDescription.setWordWrap(True)
		self.windowbarDescription.setAlignment(Qt.AlignJustify)

		self.windowBar = QCheckBox("Enable windowbar",self)
		if config.SHOW_WINDOWBAR: self.windowBar.setChecked(True)
		self.windowBar.stateChanged.connect(self.changedWindowbarSetting)

		self.windowBarTop = QCheckBox("Display at top",self)
		if config.WINDOWBAR_TOP_OF_SCREEN: self.windowBarTop.setChecked(True)
		self.windowBarTop.stateChanged.connect(self.menuChange)

		self.windowBarServers = QCheckBox("Server windows",self)
		if config.WINDOWBAR_INCLUDE_SERVERS: self.windowBarServers.setChecked(True)
		self.windowBarServers.stateChanged.connect(self.menuChange)

		self.windowBarIcons = QCheckBox("Shows window icons",self)
		if config.WINDOWBAR_SHOW_ICONS: self.windowBarIcons.setChecked(True)
		self.windowBarIcons.stateChanged.connect(self.menuChange)

		self.windowBarFloat = QCheckBox("Movable",self)
		if config.WINDOWBAR_CAN_FLOAT: self.windowBarFloat.setChecked(True)
		self.windowBarFloat.stateChanged.connect(self.menuChange)

		self.windowbarJustify = QComboBox(self)
		self.windowbarJustify.addItem(config.WINDOWBAR_JUSTIFY)
		if config.WINDOWBAR_JUSTIFY!='center': self.windowbarJustify.addItem('center')
		if config.WINDOWBAR_JUSTIFY!='left': self.windowbarJustify.addItem('left')
		if config.WINDOWBAR_JUSTIFY!='right': self.windowbarJustify.addItem('right')
		self.windowbarJustify.currentIndexChanged.connect(self.justifyChange)

		self.windowbarLabel = QLabel("Windowbar alignment ")

		justifyLayout = QHBoxLayout()
		justifyLayout.addStretch()
		justifyLayout.addWidget(self.windowbarLabel)
		justifyLayout.addWidget(self.windowbarJustify)
		justifyLayout.addStretch()

		self.windowbarClick = QCheckBox("Double click to maximize subwindow",self)
		if config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED: self.windowbarClick.setChecked(True)
		self.windowbarClick.stateChanged.connect(self.menuChange)

		self.windowBarEditor = QCheckBox("Editor windows",self)
		if config.WINDOWBAR_INCLUDE_EDITORS: self.windowBarEditor.setChecked(True)
		self.windowBarEditor.stateChanged.connect(self.menuChange)

		self.windowBarFirst = QCheckBox("Always show active window first",self)
		if config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST: self.windowBarFirst.setChecked(True)
		self.windowBarFirst.stateChanged.connect(self.menuChange)

		self.windowbarMenu = QCheckBox("Context menu",self)
		if config.WINDOWBAR_MENU: self.windowbarMenu.setChecked(True)
		self.windowbarMenu.stateChanged.connect(self.menuChange)

		self.windowbarChannels = QCheckBox("Channels",self)
		if config.WINDOWBAR_INCLUDE_CHANNELS: self.windowbarChannels.setChecked(True)
		self.windowbarChannels.stateChanged.connect(self.menuChange)

		self.windowbarPrivate = QCheckBox("Private chats",self)
		if config.WINDOWBAR_INCLUDE_PRIVATE: self.windowbarPrivate.setChecked(True)
		self.windowbarPrivate.stateChanged.connect(self.menuChange)

		self.windowbarLists = QCheckBox("Channel lists",self)
		if config.WINDOWBAR_INCLUDE_LIST: self.windowbarLists.setChecked(True)
		self.windowbarLists.stateChanged.connect(self.menuChange)

		self.windowBarUnderline = QCheckBox("Underlined text",self)
		if config.WINDOWBAR_UNDERLINE_ACTIVE_WINDOW: self.windowBarUnderline.setChecked(True)
		self.windowBarUnderline.stateChanged.connect(self.menuChange)

		self.windowBarHover = QCheckBox("Bold entries on mouse hover",self)
		if config.WINDOWBAR_HOVER_EFFECT: self.windowBarHover.setChecked(True)
		self.windowBarHover.stateChanged.connect(self.menuChange)

		self.windowbarManager = QCheckBox("Log manager",self)
		if config.WINDOWBAR_INCLUDE_MANAGER: self.windowbarManager.setChecked(True)
		self.windowbarManager.stateChanged.connect(self.menuChange)

		self.windowbarUnread = QCheckBox("Flash on unread chat messages",self)
		if config.WINDOWBAR_SHOW_UNREAD_MESSAGES: self.windowbarUnread.setChecked(True)
		self.windowbarUnread.stateChanged.connect(self.menuChange)

		self.windowbarEntryMenu = QCheckBox("Entry context menu",self)
		if config.WINDOWBAR_ENTRY_MENU: self.windowbarEntryMenu.setChecked(True)
		self.windowbarEntryMenu.stateChanged.connect(self.menuChange)

		self.serverHidden = QCheckBox("Server",self)
		if config.SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR: self.serverHidden.setChecked(True)
		self.serverHidden.stateChanged.connect(self.menuChange)

		self.windowbarItalics = QCheckBox("Show connecting server windows\nin italics",self)
		if config.WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS: self.windowbarItalics.setChecked(True)
		self.windowbarItalics.stateChanged.connect(self.menuChange)
		self.windowbarItalics.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.channelHidden = QCheckBox("Channel",self)
		if config.SHOW_HIDDEN_CHANNEL_WINDOWS_IN_WINDOWBAR: self.channelHidden.setChecked(True)
		self.channelHidden.stateChanged.connect(self.menuChange)

		self.privateHidden = QCheckBox("Private chats",self)
		if config.SHOW_HIDDEN_PRIVATE_WINDOWS_IN_WINDOWBAR: self.privateHidden.setChecked(True)
		self.privateHidden.stateChanged.connect(self.menuChange)

		self.autoHide = QCheckBox("Auto-hide",self)
		if config.HIDE_WINDOWBAR_IF_EMPTY: self.autoHide.setChecked(True)
		self.autoHide.stateChanged.connect(self.menuChange)

		self.windowbarReadme = QCheckBox("README",self)
		if config.WINDOWBAR_INCLUDE_README: self.windowbarReadme.setChecked(True)
		self.windowbarReadme.stateChanged.connect(self.menuChange)

		self.windowBarBold = QCheckBox("Bold text",self)
		if config.WINDOWBAR_BOLD_ACTIVE_WINDOW: self.windowBarBold.setChecked(True)
		self.windowBarBold.stateChanged.connect(self.menuChange)

		if not config.SHOW_WINDOWBAR:
			self.windowBarFloat.setEnabled(False)
			self.windowBarTop.setEnabled(False)
			self.windowBarServers.setEnabled(False)
			self.windowbarJustify.setEnabled(False)
			self.windowBarIcons.setEnabled(False)
			self.windowbarClick.setEnabled(False)
			self.windowBarEditor.setEnabled(False)
			self.windowBarFirst.setEnabled(False)
			self.windowbarMenu.setEnabled(False)
			self.windowbarPrivate.setEnabled(False)
			self.windowbarChannels.setEnabled(False)
			self.windowbarLists.setEnabled(False)
			self.windowBarUnderline.setEnabled(False)
			self.windowBarHover.setEnabled(False)
			self.windowbarLabel.setEnabled(False)
			self.windowbarManager.setEnabled(False)
			self.windowbarUnread.setEnabled(False)
			self.windowbarEntryMenu.setEnabled(False)
			self.serverHidden.setEnabled(False)
			self.windowbarItalics.setEnabled(False)
			self.channelHidden.setEnabled(False)
			self.privateHidden.setEnabled(False)
			self.autoHide.setEnabled(False)
			self.windowbarReadme.setEnabled(False)
			self.windowBarBold.setEnabled(False)

		includesLayout = QFormLayout()
		includesLayout.addRow(self.windowbarChannels,self.windowbarPrivate)
		includesLayout.addRow(self.windowBarServers,self.windowBarEditor)
		includesLayout.addRow(self.windowbarLists,self.windowbarManager)
		includesLayout.addRow(self.windowbarReadme)

		windowbar1Layout = QHBoxLayout()
		windowbar1Layout.addStretch()
		windowbar1Layout.addWidget(self.windowBar)
		windowbar1Layout.addStretch()

		wbMenuLayout = QFormLayout()
		wbMenuLayout.addRow(self.windowbarMenu,self.windowbarEntryMenu)

		windowbar2Layout = QHBoxLayout()
		windowbar2Layout.addWidget(self.windowBarFloat)
		windowbar2Layout.addWidget(self.windowBarTop)
		windowbar2Layout.addWidget(self.autoHide)

		hiddenLayout = QHBoxLayout()
		hiddenLayout.addWidget(self.serverHidden)
		hiddenLayout.addWidget(self.channelHidden)
		hiddenLayout.addWidget(self.privateHidden)

		wbAppearLayout = QHBoxLayout()
		wbAppearLayout.addStretch()
		wbAppearLayout.addWidget(self.windowBarBold)
		wbAppearLayout.addWidget(self.windowBarUnderline)
		wbAppearLayout.addStretch()

		windowbarLayout = QVBoxLayout()
		windowbarLayout.addWidget(widgets.textSeparatorLabel(self,"<b>windowbar settings</b>"))
		windowbarLayout.addWidget(self.windowbarDescription)
		windowbarLayout.addLayout(windowbar1Layout)
		windowbarLayout.addLayout(windowbar2Layout)
		windowbarLayout.addLayout(justifyLayout)
		windowbarLayout.addWidget(self.windowBarFirst)
		windowbarLayout.addWidget(self.windowBarHover)
		windowbarLayout.addWidget(self.windowBarIcons)
		windowbarLayout.addWidget(self.windowbarClick)
		windowbarLayout.addWidget(self.windowbarUnread)
		windowbarLayout.addWidget(self.windowbarItalics)
		windowbarLayout.addLayout(wbMenuLayout)
		windowbarLayout.addWidget(widgets.textSeparatorLabel(self,"<b>show active window in...</b>"))
		windowbarLayout.addLayout(wbAppearLayout)
		windowbarLayout.addWidget(widgets.textSeparatorLabel(self,"<b>windowbar includes</b>"))
		windowbarLayout.addLayout(includesLayout)
		windowbarLayout.addWidget(widgets.textSeparatorLabel(self,"<b>show hidden windows</b>"))
		windowbarLayout.addLayout(hiddenLayout)
		windowbarLayout.addStretch()

		self.windowbarPage.setLayout(windowbarLayout)

		# Subwindows

		self.subwindowPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Subwindows")
		entry.widget = self.subwindowPage
		entry.setIcon(QIcon(SUBWINDOW_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.subwindowPage)

		self.showInfo = QCheckBox("Show nickname display on all chat\nwindows",self)
		if config.SHOW_USER_INFO_ON_CHAT_WINDOWS: self.showInfo.setChecked(True)
		self.showInfo.stateChanged.connect(self.changedSettingRerenderNick)
		self.showInfo.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showInputMenu = QCheckBox("Show input menu button",self)
		if config.SHOW_INPUT_MENU: self.showInputMenu.setChecked(True)
		self.showInputMenu.stateChanged.connect(self.changedSetting)

		self.showContext = QCheckBox("Context menus on channel, private,\nand server text displays",self)
		if config.SHOW_CHAT_CONTEXT_MENUS: self.showContext.setChecked(True)
		self.showContext.stateChanged.connect(self.changedSetting)
		self.showContext.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showStatusServer = QCheckBox("Server windows",self)
		if config.SHOW_STATUS_BAR_ON_SERVER_WINDOWS: self.showStatusServer.setChecked(True)
		self.showStatusServer.stateChanged.connect(self.changedSetting)

		self.showStatusChat = QCheckBox("Chat windows",self)
		if config.SHOW_STATUS_BAR_ON_CHAT_WINDOWS: self.showStatusChat.setChecked(True)
		self.showStatusChat.stateChanged.connect(self.changedSetting)

		self.displayServNicks = QCheckBox("Show nickname display on server\nwindows",self)
		if config.DISPLAY_NICK_ON_SERVER_WINDOWS: self.displayServNicks.setChecked(True)
		self.displayServNicks.stateChanged.connect(self.changedSetting)
		self.displayServNicks.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showServToolbar = QCheckBox("Show toolbar on server windows",self)
		if config.SHOW_SERVER_WINDOW_TOOLBAR: self.showServToolbar.setChecked(True)
		self.showServToolbar.stateChanged.connect(self.changedSetting)

		self.showServRefresh = QCheckBox("Show channel list refresh button\non server window toolbars and menus",self)
		if config.SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS: self.showServRefresh.setChecked(True)
		self.showServRefresh.stateChanged.connect(self.changedSetting)

		self.showServRefresh.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showServList = QCheckBox("Show channel list button\non server window toolbars and menus",self)
		if config.SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS: self.showServList.setChecked(True)
		self.showServList.stateChanged.connect(self.changedSetting)

		self.showServList.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showStatusList = QCheckBox("Channel lists",self)
		if config.SHOW_STATUS_BAR_ON_LIST_WINDOWS: self.showStatusList.setChecked(True)
		self.showStatusList.stateChanged.connect(self.changedSetting)

		self.showStatusEditor = QCheckBox("Editor windows",self)
		if config.SHOW_STATUS_BAR_ON_EDITOR_WINDOWS: self.showStatusEditor.setChecked(True)
		self.showStatusEditor.stateChanged.connect(self.changedSetting)

		statusLayout = QFormLayout()
		statusLayout.addRow(self.showStatusServer,self.showStatusChat)
		statusLayout.addRow(self.showStatusList,self.showStatusEditor)

		self.enableDisconnect = QCheckBox("Closing server window disconnects\nfrom server",self)
		if config.CLOSING_SERVER_WINDOW_DISCONNECTS: self.enableDisconnect.setChecked(True)
		self.enableDisconnect.stateChanged.connect(self.changedSetting)
		self.enableDisconnect.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.hideServer = QCheckBox("Hide server windows when\nregistration is complete",self)
		if config.HIDE_SERVER_WINDOWS_ON_SIGNON: self.hideServer.setChecked(True)
		self.hideServer.stateChanged.connect(self.changedSetting)
		self.hideServer.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.autoMaxSubwindow = QCheckBox("Maximize new subwindows",self)
		if config.MAXIMIZE_SUBWINDOWS_ON_CREATION: self.autoMaxSubwindow.setChecked(True)
		self.autoMaxSubwindow.stateChanged.connect(self.changedSetting)

		self.mdiCreation = QRadioButton("Creation")
		self.mdiCreation.toggled.connect(self.selCreation)

		self.mdiStacking = QRadioButton("Stack")
		self.mdiStacking.toggled.connect(self.selStacking)

		self.mdiActivation = QRadioButton("Activation")
		self.mdiActivation.toggled.connect(self.selActivation)

		if config.SET_SUBWINDOW_ORDER=="creation": self.mdiCreation.setChecked(True)
		if config.SET_SUBWINDOW_ORDER=="stacking": self.mdiStacking.setChecked(True)
		if config.SET_SUBWINDOW_ORDER=="activation": self.mdiActivation.setChecked(True)

		orderLayout = QHBoxLayout()
		orderLayout.addWidget(self.mdiCreation)
		orderLayout.addWidget(self.mdiStacking)
		orderLayout.addWidget(self.mdiActivation)

		self.windowRubberSize = QCheckBox("Rubber band resize",self)
		if config.RUBBER_BAND_RESIZE: self.windowRubberSize.setChecked(True)
		self.windowRubberSize.stateChanged.connect(self.changedSetting)

		self.windowRubberMove = QCheckBox("Rubber band move",self)
		if config.RUBBER_BAND_MOVE: self.windowRubberMove.setChecked(True)
		self.windowRubberMove.stateChanged.connect(self.changedSetting)

		rbLayout = QHBoxLayout()
		rbLayout.addWidget(self.windowRubberSize)
		rbLayout.addWidget(self.windowRubberMove)

		subwindowLayout = QVBoxLayout()
		subwindowLayout.addWidget(widgets.textSeparatorLabel(self,"<b>subwindow settings</b>"))
		subwindowLayout.addWidget(self.showContext)
		subwindowLayout.addWidget(self.showInputMenu)
		subwindowLayout.addWidget(self.autoMaxSubwindow)
		subwindowLayout.addWidget(self.showInfo)
		subwindowLayout.addLayout(rbLayout)
		subwindowLayout.addWidget(widgets.textSeparatorLabel(self,"<b>order subwindows on...</b>"))
		subwindowLayout.addLayout(orderLayout)
		subwindowLayout.addWidget(widgets.textSeparatorLabel(self,"<b>subwindow status bars</b>"))
		subwindowLayout.addLayout(statusLayout)
		subwindowLayout.addWidget(widgets.textSeparatorLabel(self,"<b>server subwindows</b>"))
		subwindowLayout.addWidget(self.showServToolbar)
		subwindowLayout.addWidget(self.showServList)
		subwindowLayout.addWidget(self.showServRefresh)
		subwindowLayout.addWidget(self.displayServNicks)
		subwindowLayout.addWidget(self.enableDisconnect)
		subwindowLayout.addWidget(self.hideServer)
		
		subwindowLayout.addStretch()

		self.subwindowPage.setLayout(subwindowLayout)

		# Systray page

		self.systrayPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("System Tray")
		entry.widget = self.systrayPage
		entry.setIcon(QIcon(SYSTRAY_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.systrayPage)

		self.showSystrayMenu = QCheckBox("Show right click menu",self)
		if config.SYSTRAY_MENU: self.showSystrayMenu.setChecked(True)
		self.showSystrayMenu.stateChanged.connect(self.changedSystrayMin)

		self.minSystray = QCheckBox("Minimize to system tray",self)
		if config.MINIMIZE_TO_SYSTRAY: self.minSystray.setChecked(True)
		self.minSystray.stateChanged.connect(self.changedSystrayMin)

		self.systrayNotify = QCheckBox("Show system tray notifications\nwhen minimized to system tray",self)
		if config.FLASH_SYSTRAY_NOTIFICATION: self.systrayNotify.setChecked(True)
		self.systrayNotify.stateChanged.connect(self.changedSystrayNotification)
		self.systrayNotify.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.listSystray = QCheckBox("List notifications in tooltip",self)
		if config.FLASH_SYSTRAY_LIST: self.listSystray.setChecked(True)
		self.listSystray.stateChanged.connect(self.changedSetting)

		self.systrayDisconnect = QCheckBox("Disconnection from server",self)
		if config.FLASH_SYSTRAY_DISCONNECT: self.systrayDisconnect.setChecked(True)
		self.systrayDisconnect.stateChanged.connect(self.changedSetting)

		self.systrayNickname = QCheckBox("Nickname\nmentions",self)
		if config.FLASH_SYSTRAY_NICKNAME: self.systrayNickname.setChecked(True)
		self.systrayNickname.stateChanged.connect(self.changedSetting)
		self.systrayNickname.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.systrayPrivate = QCheckBox("Private\nmessages",self)
		if config.FLASH_SYSTRAY_PRIVATE: self.systrayPrivate.setChecked(True)
		self.systrayPrivate.stateChanged.connect(self.changedSetting)
		self.systrayPrivate.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.systrayKick = QCheckBox("Channel kick",self)
		if config.FLASH_SYSTRAY_KICK: self.systrayKick.setChecked(True)
		self.systrayKick.stateChanged.connect(self.changedSetting)

		self.systrayInvite = QCheckBox("Channel\ninvitation",self)
		if config.FLASH_SYSTRAY_INVITE: self.systrayInvite.setChecked(True)
		self.systrayInvite.stateChanged.connect(self.changedSetting)
		self.systrayInvite.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.systrayNotice = QCheckBox("Notice",self)
		if config.FLASH_SYSTRAY_NOTICE: self.systrayNotice.setChecked(True)
		self.systrayNotice.stateChanged.connect(self.changedSetting)

		self.systrayMode = QCheckBox("Mode set on\nuser",self)
		if config.FLASH_SYSTRAY_MODE: self.systrayMode.setChecked(True)
		self.systrayMode.stateChanged.connect(self.changedSetting)
		self.systrayMode.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.systrayMinOnClose = QCheckBox("Closing main window with window\ncontrols minimizes to tray",self)
		if config.CLOSING_WINDOW_MINIMIZES_TO_TRAY: self.systrayMinOnClose.setChecked(True)
		self.systrayMinOnClose.stateChanged.connect(self.changedSetting)
		self.systrayMinOnClose.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showSystray = QCheckBox("Show system tray icon",self)
		if config.SHOW_SYSTRAY_ICON: self.showSystray.setChecked(True)
		self.showSystray.stateChanged.connect(self.changedSystrayMin)

		discLay = QHBoxLayout()
		discLay.addWidget(self.systrayDisconnect)
		discLay.addStretch()

		nickPriv = QHBoxLayout()
		nickPriv.addWidget(self.systrayNickname)
		nickPriv.addWidget(self.systrayPrivate)

		kickInvite = QHBoxLayout()
		kickInvite.addWidget(self.systrayKick)
		kickInvite.addWidget(self.systrayInvite)

		noticeMode = QHBoxLayout()
		noticeMode.addWidget(self.systrayNotice)
		noticeMode.addWidget(self.systrayMode)

		self.setFlashInterval = QLabel("Flash icon every ")

		self.flashInterval = QComboBox(self)
		added = False
		if config.FLASH_SYSTRAY_SPEED==250:
			self.flashInterval.addItem("250ms")
			added = True
		if config.FLASH_SYSTRAY_SPEED==500:
			self.flashInterval.addItem("500 ms")
			added = True
		if config.FLASH_SYSTRAY_SPEED==750:
			self.flashInterval.addItem("750 ms")
			added = True
		if config.FLASH_SYSTRAY_SPEED==1000:
			self.flashInterval.addItem("1 second")
			added = True
		if added==False: self.flashInterval.addItem(f"{config.FLASH_SYSTRAY_SPEED} ms")
		if config.FLASH_SYSTRAY_SPEED!=250: self.flashInterval.addItem("250 ms")
		if config.FLASH_SYSTRAY_SPEED!=500: self.flashInterval.addItem("500 ms")
		if config.FLASH_SYSTRAY_SPEED!=750: self.flashInterval.addItem("750 ms")
		if config.FLASH_SYSTRAY_SPEED!=1000: self.flashInterval.addItem("1 second")
		self.flashInterval.currentIndexChanged.connect(self.flashChange)

		flashBox = QHBoxLayout()
		flashBox.addWidget(self.setFlashInterval)
		flashBox.addWidget(self.flashInterval)
		flashBox.addStretch()

		self.doubleclickRestore = QCheckBox("Double click to restore window\nfrom system tray",self)
		if config.DOUBLECLICK_TO_RESTORE_WINDOW_FROM_SYSTRAY: self.doubleclickRestore.setChecked(True)
		self.doubleclickRestore.stateChanged.connect(self.changedSetting)
		self.doubleclickRestore.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.clickToMinimize = QCheckBox("Click systray icon to minimize\nto system tray",self)
		if config.CLICK_SYSTRAY_ICON_TO_MINIMIZE_TO_TRAY: self.clickToMinimize.setChecked(True)
		self.clickToMinimize.stateChanged.connect(self.changedSetting)
		self.clickToMinimize.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.stmConnections = QCheckBox("Connections",self)
		if config.SHOW_CONNECTIONS_IN_SYSTRAY_MENU: self.stmConnections.setChecked(True)
		self.stmConnections.stateChanged.connect(self.changedSettingConnections)

		self.stmSettings = QCheckBox("Settings",self)
		if config.SHOW_SETTINGS_IN_SYSTRAY_MENU: self.stmSettings.setChecked(True)
		self.stmSettings.stateChanged.connect(self.changedSetting)

		self.stmDirs = QCheckBox("Directories",self)
		if config.SHOW_DIRECTORIES_IN_SYSTRAY_MENU: self.stmDirs.setChecked(True)
		self.stmDirs.stateChanged.connect(self.changedSetting)

		self.stmLinks = QCheckBox("Links ",self)
		if config.SHOW_LINKS_IN_SYSTRAY_MENU: self.stmLinks.setChecked(True)
		self.stmLinks.stateChanged.connect(self.changedSetting)

		self.stmList = QCheckBox("Channel list",self)
		if config.SHOW_LIST_IN_SYSTRAY_MENU: self.stmList.setChecked(True)
		self.stmList.stateChanged.connect(self.changedSetting)

		self.stmLogs = QCheckBox("Network logs",self)
		if config.SHOW_LOGS_IN_SYSTRAY_MENU: self.stmLogs.setChecked(True)
		self.stmLogs.stateChanged.connect(self.changedSetting)

		menuRow1 = QHBoxLayout()
		menuRow1.addStretch()
		menuRow1.addWidget(self.stmConnections)
		menuRow1.addWidget(self.stmSettings)
		menuRow1.addWidget(self.stmDirs)
		menuRow1.addStretch()

		menuRow2 = QHBoxLayout()
		menuRow2.addStretch()
		menuRow2.addWidget(self.stmLinks)
		menuRow2.addWidget(self.stmList)
		menuRow2.addWidget(self.stmLogs)
		menuRow2.addStretch()

		menuBox = QVBoxLayout()
		menuBox.addLayout(menuRow1)
		menuBox.addLayout(menuRow2)

		if not config.SYSTRAY_MENU:
			self.stmConnections.setEnabled(False)
			self.stmSettings.setEnabled(False)
			self.stmDirs.setEnabled(False)
			self.stmLinks.setEnabled(False)
			self.stmList.setEnabled(False)
			self.stmLogs.setEnabled(False)

		if not config.SHOW_CONNECTIONS_IN_SYSTRAY_MENU:
			self.stmList.setEnabled(False)
			self.stmLogs.setEnabled(False)

		systrayLayout = QVBoxLayout()
		systrayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>system tray settings</b>"))
		systrayLayout.addWidget(self.showSystray)
		systrayLayout.addWidget(self.showSystrayMenu)
		systrayLayout.addWidget(self.minSystray)
		systrayLayout.addWidget(self.systrayMinOnClose)
		systrayLayout.addWidget(self.doubleclickRestore)
		systrayLayout.addWidget(self.clickToMinimize)
		systrayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>notification settings</b>"))
		systrayLayout.addWidget(self.systrayNotify)
		systrayLayout.addWidget(self.listSystray)
		systrayLayout.addLayout(flashBox)
		systrayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>notifications</b>"))
		systrayLayout.addLayout(nickPriv)
		systrayLayout.addLayout(kickInvite)
		systrayLayout.addLayout(noticeMode)
		systrayLayout.addLayout(discLay)
		systrayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>system tray menu includes...</b>"))
		systrayLayout.addLayout(menuBox)
		systrayLayout.addStretch()

		self.systrayPage.setLayout(systrayLayout)

		if config.SHOW_SYSTRAY_ICON:
			self.showSystrayMenu.setEnabled(True)
			self.minSystray.setEnabled(True)
			if config.MINIMIZE_TO_SYSTRAY:
				self.systrayNotify.setEnabled(True)
				self.listSystray.setEnabled(True)
				self.systrayDisconnect.setEnabled(True)
				self.systrayNickname.setEnabled(True)
				self.systrayPrivate.setEnabled(True)
				self.systrayKick.setEnabled(True)
				self.systrayInvite.setEnabled(True)
				self.systrayNotice.setEnabled(True)
				self.systrayMode.setEnabled(True)
				self.systrayMinOnClose.setEnabled(True)
				self.setFlashInterval.setEnabled(True)
				self.flashInterval.setEnabled(True)
				self.doubleclickRestore.setEnabled(True)
				self.clickToMinimize.setEnabled(True)
			else:
				self.systrayNotify.setEnabled(False)
				self.listSystray.setEnabled(False)
				self.systrayDisconnect.setEnabled(False)
				self.systrayNickname.setEnabled(False)
				self.systrayPrivate.setEnabled(False)
				self.systrayKick.setEnabled(False)
				self.systrayInvite.setEnabled(False)
				self.systrayNotice.setEnabled(False)
				self.systrayMode.setEnabled(False)
				self.systrayMinOnClose.setEnabled(False)
				self.setFlashInterval.setEnabled(False)
				self.flashInterval.setEnabled(False)
				self.doubleclickRestore.setEnabled(False)
				self.clickToMinimize.setEnabled(False)
		else:
			self.showSystrayMenu.setEnabled(False)
			self.minSystray.setEnabled(False)
			self.systrayNotify.setEnabled(False)
			self.listSystray.setEnabled(False)
			self.systrayDisconnect.setEnabled(False)
			self.systrayNickname.setEnabled(False)
			self.systrayPrivate.setEnabled(False)
			self.systrayKick.setEnabled(False)
			self.systrayInvite.setEnabled(False)
			self.systrayNotice.setEnabled(False)
			self.systrayMode.setEnabled(False)
			self.systrayMinOnClose.setEnabled(False)
			self.setFlashInterval.setEnabled(False)
			self.flashInterval.setEnabled(False)
			self.doubleclickRestore.setEnabled(False)
			self.clickToMinimize.setEnabled(False)
			self.stmConnections.setEnabled(False)
			self.stmSettings.setEnabled(False)
			self.stmDirs.setEnabled(False)
			self.stmLinks.setEnabled(False)
			self.stmList.setEnabled(False)
			self.stmLogs.setEnabled(False)

		# Notifications

		self.notificationsPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Notifications")
		entry.widget = self.notificationsPage
		entry.setIcon(QIcon(NOTIFICATION_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.notificationsPage)

		self.audioNotifications = QCheckBox("Play audio notifications",self)
		if config.SOUND_NOTIFICATIONS: self.audioNotifications.setChecked(True)
		self.audioNotifications.stateChanged.connect(self.changedNotifications)

		self.notifyDisco = QCheckBox("Disconnection from server",self)
		if config.SOUND_NOTIFICATION_DISCONNECT: self.notifyDisco.setChecked(True)
		self.notifyDisco.stateChanged.connect(self.changedSetting)

		self.notifyNickname = QCheckBox("Nickname\nmention",self)
		if config.SOUND_NOTIFICATION_NICKNAME: self.notifyNickname.setChecked(True)
		self.notifyNickname.stateChanged.connect(self.changedSetting)
		self.notifyNickname.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.notifyPrivate = QCheckBox("Private\nmessage",self)
		if config.SOUND_NOTIFICATION_PRIVATE: self.notifyPrivate.setChecked(True)
		self.notifyPrivate.stateChanged.connect(self.changedSetting)
		self.notifyPrivate.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.notifyNotice = QCheckBox("Notice",self)
		if config.SOUND_NOTIFICATION_NOTICE: self.notifyNotice.setChecked(True)
		self.notifyNotice.stateChanged.connect(self.changedSetting)

		self.notifyKick = QCheckBox("Kick",self)
		if config.SOUND_NOTIFICATION_KICK: self.notifyKick.setChecked(True)
		self.notifyKick.stateChanged.connect(self.changedSetting)

		self.notifyInvite = QCheckBox("Invite",self)
		if config.SOUND_NOTIFICATION_INVITE: self.notifyInvite.setChecked(True)
		self.notifyInvite.stateChanged.connect(self.changedSetting)

		self.notifyMode = QCheckBox("Channel mode\nchange",self)
		if config.SOUND_NOTIFICATION_MODE: self.notifyMode.setChecked(True)
		self.notifyMode.stateChanged.connect(self.changedSetting)
		self.notifyMode.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")
		
		self.notifyDescription = QLabel("""
			<small>
			<b>Audio notifications</b>, when enabled, play a sound (by default, a bell) every time
			one of the listed <b>events</b> occur. Any file of any length can be used for the notification
			sound; the only limitation is that the file <b><i>must</i> be a WAV file</b>.
			</small>
			<br>
			""")
		self.notifyDescription.setWordWrap(True)
		self.notifyDescription.setAlignment(Qt.AlignJustify)

		adiscLay = QHBoxLayout()
		adiscLay.addWidget(self.notifyDisco)
		adiscLay.addStretch()

		anickPriv = QHBoxLayout()
		anickPriv.addWidget(self.notifyNickname)
		anickPriv.addWidget(self.notifyPrivate)

		akickInvite = QHBoxLayout()
		akickInvite.addWidget(self.notifyKick)
		akickInvite.addWidget(self.notifyInvite)

		anoticeMode = QHBoxLayout()
		anoticeMode.addWidget(self.notifyNotice)
		anoticeMode.addWidget(self.notifyMode)

		bname = os.path.basename(self.sound)
		self.soundLabel = QLabel("<b>"+bname+"</b>")

		self.soundButton = QPushButton("")
		self.soundButton.clicked.connect(self.setSound)
		self.soundButton.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.soundButton.setFixedSize(fheight +10,fheight + 10)
		self.soundButton.setIcon(QIcon(EDIT_ICON))
		self.soundButton.setToolTip("Set notification sound file")

		self.playButton = QPushButton(" Play")
		self.playButton.clicked.connect(self.playSound)
		self.playButton.setAutoDefault(False)
		self.playButton.setIcon(QIcon(RUN_ICON))
		self.playButton.setToolTip("Play sound")

		self.soundDefaultButton = QPushButton("Set to default")
		self.soundDefaultButton.clicked.connect(self.soundDefault)
		self.soundDefaultButton.setAutoDefault(False)
		self.soundDefaultButton.setToolTip("Set to default")

		if not config.SOUND_NOTIFICATIONS:
			self.notifyDisco.setEnabled(False)
			self.notifyNickname.setEnabled(False)
			self.notifyPrivate.setEnabled(False)
			self.notifyNotice.setEnabled(False)
			self.notifyKick.setEnabled(False)
			self.notifyInvite.setEnabled(False)
			self.notifyMode.setEnabled(False)
			self.soundLabel.setEnabled(False)
			self.soundButton.setEnabled(False)
			self.playButton.setEnabled(False)
			self.soundDefaultButton.setEnabled(False)

		sbLayout = QHBoxLayout()
		sbLayout.addStretch()
		sbLayout.addWidget(self.soundButton)
		sbLayout.addWidget(self.soundLabel)
		sbLayout.addStretch()

		sbLayout2 = QHBoxLayout()
		sbLayout2.addStretch()
		sbLayout2.addWidget(self.playButton)
		sbLayout2.addWidget(self.soundDefaultButton)
		sbLayout2.addStretch()

		audioMaster = QHBoxLayout()
		audioMaster.addStretch()
		audioMaster.addWidget(self.audioNotifications)
		audioMaster.addStretch()

		audioLayout = QVBoxLayout()
		audioLayout.addWidget(widgets.textSeparatorLabel(self,"<b>audio notifications</b>"))
		audioLayout.addWidget(self.notifyDescription)
		audioLayout.addLayout(audioMaster)
		audioLayout.addWidget(QLabel(' '))
		audioLayout.addWidget(widgets.textSeparatorLabel(self,"<b>events</b>"))
		audioLayout.addLayout(anickPriv)
		audioLayout.addLayout(akickInvite)
		audioLayout.addLayout(anoticeMode)
		audioLayout.addLayout(adiscLay)
		audioLayout.addWidget(widgets.textSeparatorLabel(self,"<b>sound file</b>"))
		audioLayout.addLayout(sbLayout)
		audioLayout.addLayout(sbLayout2)
		audioLayout.addStretch()

		self.notificationsPage.setLayout(audioLayout)

		# User page

		self.userPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("User")
		entry.widget = self.userPage
		entry.setIcon(QIcon(PRIVATE_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.userPage)

		self.nick = QNoSpaceLineEdit(user.NICKNAME)
		self.alternative = QNoSpaceLineEdit(user.ALTERNATE)
		self.username = QNoSpaceLineEdit(user.USERNAME)
		self.realname = QLineEdit(user.REALNAME)
		self.userinfo = QLineEdit(user.USERINFO)
		self.finger = QLineEdit(user.FINGER)

		self.nick.textChanged.connect(self.changeUser)
		self.alternative.textChanged.connect(self.changeUser)
		self.username.textChanged.connect(self.changeUser)
		self.realname.textChanged.connect(self.changeUser)
		self.userinfo.textChanged.connect(self.changeUser)
		self.finger.textChanged.connect(self.changeUser)

		nickLayout = QFormLayout()
		nickLayout.addRow(self.nick)
		nickLayout.addRow(QLabel("<center><small>The nickname you wish to use on the server</small></center>"))
		nickBox = QGroupBox("Nickname")
		nickBox.setAlignment(Qt.AlignLeft)
		nickBox.setLayout(nickLayout)

		font = nickBox.font()
		font.setBold(True)
		nickBox.setFont(font)
		
		alternateLayout = QFormLayout()
		alternateLayout.addRow(self.alternative)
		alternateLayout.addRow(QLabel("<center><small>Alternate nickname if your first<br>choice is already taken</small></center>"))
		alternateBox = QGroupBox("Alternate (optional)")
		alternateBox.setAlignment(Qt.AlignLeft)
		alternateBox.setLayout(alternateLayout)

		alternateBox.setFont(font)
		
		userLayout = QFormLayout()
		userLayout.addRow(self.username)
		userLayout.addRow(QLabel("<center><small>The username you wish to use</small></center>"))
		userBox = QGroupBox("Username")
		userBox.setAlignment(Qt.AlignLeft)
		userBox.setLayout(userLayout)

		userBox.setFont(font)
		
		realnameLayout = QFormLayout()
		realnameLayout.addRow(self.realname)
		realnameLayout.addRow(QLabel("<center><small>Your real name or other descriptive text</small></center>"))
		realnameBox = QGroupBox("Real Name")
		realnameBox.setAlignment(Qt.AlignLeft)
		realnameBox.setLayout(realnameLayout)

		realnameBox.setFont(font)

		userinfoLayout = QFormLayout()
		userinfoLayout.addRow(self.userinfo)
		userinfoLayout.addRow(QLabel("<center><small>Reply for CTCP USERINFO queries</small></center>"))
		userinfoBox = QGroupBox("USERINFO (optional)")
		userinfoBox.setAlignment(Qt.AlignLeft)
		userinfoBox.setLayout(userinfoLayout)

		userinfoBox.setFont(font)

		fingerLayout = QFormLayout()
		fingerLayout.addRow(self.finger)
		fingerLayout.addRow(QLabel("<center><small>Reply for CTCP FINGER queries</small></center>"))
		fingerBox = QGroupBox("FINGER (optional)")
		fingerBox.setAlignment(Qt.AlignLeft)
		fingerBox.setLayout(fingerLayout)

		fingerBox.setFont(font)

		userLayout = QVBoxLayout()
		userLayout.addWidget(widgets.textSeparatorLabel(self,"<b>user information</b>"))
		userLayout.addWidget(nickBox)
		userLayout.addWidget(alternateBox)
		userLayout.addWidget(userBox)
		userLayout.addWidget(realnameBox)
		userLayout.addWidget(userinfoBox)
		userLayout.addWidget(fingerBox)
		userLayout.addStretch()

		self.userPage.setLayout(userLayout)

		# Channels

		self.channelInfoPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Channels")
		entry.widget = self.channelInfoPage
		entry.setIcon(QIcon(CHANNEL_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.channelInfoPage)

		self.topicDisplay = QCheckBox("Show channel information display",self)
		if config.SHOW_CHANNEL_TOPIC: self.topicDisplay.setChecked(True)
		self.topicDisplay.stateChanged.connect(self.mainTopicChange)

		self.topicBold = QCheckBox("Show topic in bold",self)
		if config.CHANNEL_TOPIC_BOLD: self.topicBold.setChecked(True)
		self.topicBold.stateChanged.connect(self.titleChange)

		self.channelName = QCheckBox("Channel name/modes",self)
		if config.SHOW_CHANNEL_NAME_AND_MODES: self.channelName.setChecked(True)
		self.channelName.stateChanged.connect(self.topicChange)

		self.showBanlist = QCheckBox("Banlist button",self)
		if config.SHOW_BANLIST_MENU: self.showBanlist.setChecked(True)
		self.showBanlist.stateChanged.connect(self.topicChange)

		self.showChanMenu = QCheckBox("Set modes button",self)
		if config.SHOW_CHANNEL_MENU: self.showChanMenu.setChecked(True)
		self.showChanMenu.stateChanged.connect(self.topicChange)

		self.channelCount = QCheckBox("User count",self)
		if config.SHOW_USER_COUNT_DISPLAY: self.channelCount.setChecked(True)
		self.channelCount.stateChanged.connect(self.topicChange)

		if not config.SHOW_CHANNEL_TOPIC:
			self.topicBold.setEnabled(False)
			self.channelName.setEnabled(False)
			self.showBanlist.setEnabled(False)
			self.showChanMenu.setEnabled(False)
			self.channelCount.setEnabled(False)

		self.channelDescription = QLabel("""
			<small>
			The <b>channel information display</b> is a bar shown at the top of
			every channel window that displays the channel <b>name</b>, any <b>modes</b> set
			on the channel, the channel
			<b>topic</b>, and the channel <b>banlist</b>. The channel <b>topic</b> can be changed
			or edited with it (if you have the right permissions) by clicking
			on the <b>topic</b> and editing it. Here, the
			<b>channel information display</b> can be customized or turned off.
			</small>
			""")
		self.channelDescription.setWordWrap(True)
		self.channelDescription.setAlignment(Qt.AlignJustify)

		self.topicTitleDisplay = QCheckBox("Show channel topic in subwindow title",self)
		if config.SHOW_CHANNEL_TOPIC_IN_WINDOW_TITLE: self.topicTitleDisplay.setChecked(True)
		self.topicTitleDisplay.stateChanged.connect(self.titleChange)

		self.showUserlistLeft = QCheckBox("Display on left",self)
		if config.SHOW_USERLIST_ON_LEFT: self.showUserlistLeft.setChecked(True)
		self.showUserlistLeft.stateChanged.connect(self.swapUserlistSetting)

		self.plainUserLists = QCheckBox("Plain text only",self)
		if config.PLAIN_USER_LISTS: self.plainUserLists.setChecked(True)
		self.plainUserLists.stateChanged.connect(self.changedSettingRerenderUserlists)

		self.showUserlists = QCheckBox("Show user lists",self)
		if config.SHOW_USERLIST: self.showUserlists.setChecked(True)
		self.showUserlists.stateChanged.connect(self.changedUserlistVisibility)

		self.autoJoin = QCheckBox("Automatically join channel on invite",self)
		if config.JOIN_ON_INVITE: self.autoJoin.setChecked(True)
		self.autoJoin.stateChanged.connect(self.changedSetting)

		self.hideScroll = QCheckBox("Hide horizontal scrollbars",self)
		if config.HIDE_USERLIST_HORIZONTAL_SCROLLBAR: self.hideScroll.setChecked(True)
		self.hideScroll.stateChanged.connect(self.changedSetting)

		self.noSelectUserlists = QCheckBox("Forbid item selection",self)
		if config.USERLIST_ITEMS_NON_SELECTABLE: self.noSelectUserlists.setChecked(True)
		self.noSelectUserlists.stateChanged.connect(self.changedSettingRerenderUserlists)

		self.ignoreUserlist = QCheckBox("Mark ignored users",self)
		if config.SHOW_IGNORE_STATUS_IN_USERLISTS: self.ignoreUserlist.setChecked(True)
		self.ignoreUserlist.stateChanged.connect(self.changedSettingRerenderUserlists)

		self.showAwayStatus = QCheckBox("Mark away users",self)
		if config.SHOW_AWAY_STATUS_IN_USERLISTS: self.showAwayStatus.setChecked(True)
		self.showAwayStatus.stateChanged.connect(self.changedSettingRerenderUserlists)

		self.dcPrivate = QCheckBox("Double click user for private chat",self)
		if config.DOUBLECLICK_TO_OPEN_PRIVATE_CHAT: self.dcPrivate.setChecked(True)
		self.dcPrivate.stateChanged.connect(self.changedSetting)

		self.elideAway = QCheckBox("Elide away message ",self)
		if config.ELIDE_AWAY_MSG_IN_USERLIST_CONTEXT: self.elideAway.setChecked(True)
		self.elideAway.stateChanged.connect(self.changedSetting)

		self.elideHostmask = QCheckBox("Elide hostmask",self)
		if config.ELIDE_HOSTMASK_IN_USERLIST_CONTEXT: self.elideHostmask.setChecked(True)
		self.elideHostmask.stateChanged.connect(self.changedSetting)

		self.ulistContext = QCheckBox("Context menu",self)
		if config.USERLIST_CONTEXT_MENU: self.ulistContext.setChecked(True)
		self.ulistContext.stateChanged.connect(self.changedSettingContext)

		if not config.SHOW_USERLIST:
			self.plainUserLists.setEnabled(False)
			self.showUserlistLeft.setEnabled(False)
			self.hideScroll.setEnabled(False)
			self.noSelectUserlists.setEnabled(False)
			self.ignoreUserlist.setEnabled(False)
			self.showAwayStatus.setEnabled(False)
			self.dcPrivate.setEnabled(False)
			self.elideAway.setEnabled(False)
			self.elideHostmask.setEnabled(False)
			self.ulistContext.setEnabled(False)

		if not config.USERLIST_CONTEXT_MENU:
			if config.SHOW_USERLIST:
				self.elideAway.setEnabled(False)
				self.elideHostmask.setEnabled(False)

		chanButtonLayout = QFormLayout()
		chanButtonLayout.addRow(self.channelName,self.channelCount)
		chanButtonLayout.addRow(self.showChanMenu,self.showBanlist)

		ulistDisplay = QFormLayout()
		ulistDisplay.addRow(self.showUserlists,self.showUserlistLeft)
		ulistDisplay.addRow(self.plainUserLists,self.ulistContext)
		ulistDisplay.addRow(self.elideAway,self.elideHostmask)
		ulistDisplay.addRow(self.ignoreUserlist,self.showAwayStatus)
		
		ulistDisplay2 = QHBoxLayout()
		ulistDisplay2.addStretch()
		ulistDisplay2.addLayout(ulistDisplay)
		ulistDisplay2.addStretch()

		infoExist = QHBoxLayout()
		infoExist.addStretch()
		infoExist.addWidget(self.topicDisplay)
		infoExist.addStretch()

		self.nameTitleDisplay = QCheckBox("Show channel name in subwindow title",self)
		if config.SHOW_CHANNEL_NAME_IN_SUBWINDOW_TITLE: self.nameTitleDisplay.setChecked(True)
		self.nameTitleDisplay.stateChanged.connect(self.titleChange)

		menuLayout = QVBoxLayout()
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>channel information display</b>"))
		menuLayout.addWidget(self.channelDescription)
		menuLayout.addLayout(infoExist)
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>display settings</b>"))
		menuLayout.addLayout(chanButtonLayout)
		menuLayout.addWidget(self.topicBold)
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>user list settings</b>"))
		menuLayout.addLayout(ulistDisplay2)
		menuLayout.addWidget(self.noSelectUserlists)
		menuLayout.addWidget(self.hideScroll)
		menuLayout.addWidget(self.dcPrivate)
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous</b>"))
		menuLayout.addWidget(self.nameTitleDisplay)
		menuLayout.addWidget(self.topicTitleDisplay)
		menuLayout.addWidget(self.autoJoin)
		menuLayout.addStretch()

		self.channelInfoPage.setLayout(menuLayout)

		# Time

		self.timestampPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Time")
		entry.widget = self.timestampPage
		entry.setIcon(QIcon(TIMESTAMP_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.timestampPage)

		self.showTimestamps = QCheckBox("Show timestamps",self)
		if config.DISPLAY_TIMESTAMP: self.showTimestamps.setChecked(True)
		self.showTimestamps.stateChanged.connect(self.changeTimestamp)

		self.timestamp24hour = QCheckBox("Use 24-hour time for timestamps",self)
		if config.TIMESTAMP_24_HOUR: self.timestamp24hour.setChecked(True)
		self.timestamp24hour.stateChanged.connect(self.changedSettingRerender)

		self.timestampSeconds = QCheckBox("Show seconds in timestamps",self)
		if config.TIMESTAMP_SHOW_SECONDS: self.timestampSeconds.setChecked(True)
		self.timestampSeconds.stateChanged.connect(self.changedSettingRerender)

		if not config.DISPLAY_TIMESTAMP:
			self.timestamp24hour.setEnabled(False)
			self.timestampSeconds.setEnabled(False)

		self.showUptime = QCheckBox("Show connection uptime",self)
		if config.SHOW_CONNECTION_UPTIME: self.showUptime.setChecked(True)
		self.showUptime.stateChanged.connect(self.changedSetting)

		self.showChanUptime = QCheckBox("Show channel uptime",self)
		if config.SHOW_CHANNEL_UPTIME: self.showChanUptime.setChecked(True)
		self.showChanUptime.stateChanged.connect(self.changedSetting)

		self.timestampDescription = QLabel("""
			<small>
			<b>Timestamps</b>, if turned on, are shown as the beginning of all displayed
			messages in the chat display. They are saved to the log regardless of whether
			they are visible or not.
			</small>
			<br>
			""")
		self.timestampDescription.setWordWrap(True)
		self.timestampDescription.setAlignment(Qt.AlignJustify)

		self.uptimeDescription = QLabel("""
			<small>
			<b>Uptimes</b> (that is, the length of time you have been connected to a
			<b>server</b> or been in a <b>channel</b>) are generally displayed in the subwindow's
			<b>status bar</b>. For <b>server</b> windows, if the <b>status bar</b>
			is turned off, the connection <b>uptime</b> is displayed in the toolbar.
			</small>
			<br>
			""")
		self.uptimeDescription.setWordWrap(True)
		self.uptimeDescription.setAlignment(Qt.AlignJustify)

		self.showDates = QCheckBox("Show dates in logs",self)
		if config.SHOW_DATES_IN_LOGS: self.showDates.setChecked(True)
		self.showDates.stateChanged.connect(self.changedSettingRerender)

		timestampLayout = QVBoxLayout()
		timestampLayout.addWidget(widgets.textSeparatorLabel(self,"<b>timestamp settings</b>"))
		timestampLayout.addWidget(self.timestampDescription)
		timestampLayout.addWidget(self.showTimestamps)
		timestampLayout.addWidget(self.timestamp24hour)
		timestampLayout.addWidget(self.timestampSeconds)
		timestampLayout.addWidget(QLabel(' '))
		timestampLayout.addWidget(widgets.textSeparatorLabel(self,"<b>uptime displays</b>"))
		timestampLayout.addWidget(self.uptimeDescription)
		timestampLayout.addWidget(self.showUptime)
		timestampLayout.addWidget(self.showChanUptime)
		timestampLayout.addWidget(QLabel(' '))
		timestampLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous settings</b>"))
		timestampLayout.addWidget(self.showDates)
		timestampLayout.addStretch()

		self.timestampPage.setLayout(timestampLayout)

		# Connection page

		self.connectionsPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Connection")
		entry.widget = self.connectionsPage
		entry.setIcon(QIcon(NETWORK_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.connectionsPage)

		self.askBeforeDisconnect = QCheckBox("Ask before disconnecting",self)
		if config.ASK_BEFORE_DISCONNECT: self.askBeforeDisconnect.setChecked(True)
		self.askBeforeDisconnect.stateChanged.connect(self.changedSetting)

		self.askBeforeReconnect = QCheckBox("Ask before reconnecting",self)
		if config.ASK_BEFORE_RECONNECT: self.askBeforeReconnect.setChecked(True)
		self.askBeforeReconnect.stateChanged.connect(self.changedSetting)

		self.notifyOnLostConnection = QCheckBox("Notify on lost/failed connection",self)
		if config.NOTIFY_ON_LOST_OR_FAILED_CONNECTION: self.notifyOnLostConnection.setChecked(True)
		self.notifyOnLostConnection.stateChanged.connect(self.changedSetting)

		self.promptFail = QCheckBox("Prompt for new server on\nconnection failure",self)
		if config.PROMPT_ON_FAILED_CONNECTION: self.promptFail.setChecked(True)
		self.promptFail.stateChanged.connect(self.changedSetting)

		self.promptFail.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.requestList = QCheckBox("Fetch channel list from server on\nconnection",self)
		if config.REQUEST_CHANNEL_LIST_ON_CONNECTION: self.requestList.setChecked(True)
		self.requestList.stateChanged.connect(self.changedSetting)
		self.requestList.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.autoHostmasks = QCheckBox("Fetch user hostmasks on channel join",self)
		if config.GET_HOSTMASKS_ON_CHANNEL_JOIN: self.autoHostmasks.setChecked(True)
		self.autoHostmasks.stateChanged.connect(self.changedSettingHostmask)

		self.showNetLinks = QCheckBox("Show known links to network\nhomepages",self)
		if config.SHOW_LINKS_TO_NETWORK_WEBPAGES: self.showNetLinks.setChecked(True)
		self.showNetLinks.stateChanged.connect(self.changedSetting)
		self.showNetLinks.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.fetchFreqLabel = QLabel("Fetch hostmask every")
		self.fetchFreqLabelSpec = QLabel("seconds")
		self.fetchFreq = QSpinBox()
		self.fetchFreq.setRange(1,99)
		self.fetchFreq.setValue(self.HOSTMASK_FETCH_FREQUENCY)
		self.fetchFreq.valueChanged.connect(self.updateFreq)

		freqLayout = QHBoxLayout()
		freqLayout.addWidget(self.fetchFreqLabel)
		freqLayout.addWidget(self.fetchFreq)
		freqLayout.addWidget(self.fetchFreqLabelSpec)
		freqLayout.addStretch()

		if not config.GET_HOSTMASKS_ON_CHANNEL_JOIN:
			self.fetchFreqLabel.setEnabled(False)
			self.fetchFreq.setEnabled(False)
			self.fetchFreqLabelSpec.setEnabled(False)

		self.delayReconnect = QCheckBox("Delay reconnection by",self)
		if config.DELAY_AUTO_RECONNECTION: self.delayReconnect.setChecked(True)
		self.delayReconnect.stateChanged.connect(self.changedSetting)

		self.delayTimeLabelSpec = QLabel("seconds")
		self.delayTime = QSpinBox()
		self.delayTime.setRange(1,99)
		self.delayTime.setValue(self.RECONNECTION_DELAY)
		self.delayTime.valueChanged.connect(self.updateDelay)

		delayLayout = QHBoxLayout()
		delayLayout.addWidget(self.delayReconnect)
		delayLayout.addWidget(self.delayTime)
		delayLayout.addWidget(self.delayTimeLabelSpec)
		delayLayout.addStretch()

		connectionsLayout = QVBoxLayout()
		connectionsLayout.addWidget(widgets.textSeparatorLabel(self,"<b>connection settings</b>"))
		connectionsLayout.addWidget(self.askBeforeDisconnect)
		connectionsLayout.addWidget(self.notifyOnLostConnection)
		connectionsLayout.addWidget(self.promptFail)
		connectionsLayout.addWidget(self.showNetLinks)
		connectionsLayout.addWidget(QLabel(' '))
		connectionsLayout.addWidget(widgets.textSeparatorLabel(self,"<b>automatic reconnection</b>"))
		connectionsLayout.addWidget(self.askBeforeReconnect)
		connectionsLayout.addLayout(delayLayout)
		connectionsLayout.addWidget(QLabel(' '))
		connectionsLayout.addWidget(widgets.textSeparatorLabel(self,"<b>automatically fetch from server</b>"))
		connectionsLayout.addWidget(self.requestList)
		connectionsLayout.addWidget(self.autoHostmasks)
		connectionsLayout.addLayout(freqLayout)
		connectionsLayout.addStretch()
		self.connectionsPage.setLayout(connectionsLayout)

		# Away

		self.awayPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Away")
		entry.widget = self.awayPage
		entry.setIcon(QIcon(GO_AWAY_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.awayPage)

		self.promptAway = QCheckBox(f"Prompt for away message if one is\nnot provided with the {config.ISSUE_COMMAND_SYMBOL}away command\nor when pressing the \"Set status to\naway\" button on the server window\ntoolbar",self)
		if config.PROMPT_FOR_AWAY_MESSAGE: self.promptAway.setChecked(True)
		self.promptAway.stateChanged.connect(self.changedSetting)
		self.promptAway.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.autoAway = QCheckBox("Auto-away after",self)
		if config.USE_AUTOAWAY: self.autoAway.setChecked(True)
		self.autoAway.stateChanged.connect(self.changedAutoAway)

		self.autoawayInterval = QComboBox(self)
		added = False
		if config.AUTOAWAY_TIME==300:
			self.autoawayInterval.addItem("5 minutes")
			added = True
		if config.AUTOAWAY_TIME==900:
			self.autoawayInterval.addItem("15 minutes")
			added = True
		if config.AUTOAWAY_TIME==1800:
			self.autoawayInterval.addItem("30 minutes")
			added = True
		if config.AUTOAWAY_TIME==3600:
			self.autoawayInterval.addItem("1 hour")
			added = True
		if config.AUTOAWAY_TIME==7200:
			self.autoawayInterval.addItem("2 hours")
			added = True
		if config.AUTOAWAY_TIME==10800:
			self.autoawayInterval.addItem("3 hours")
			added = True
		if added==False: self.autoawayInterval.addItem(f"{config.AUTOAWAY_TIME} sec")
		if config.AUTOAWAY_TIME!=300: self.autoawayInterval.addItem("5 minutes")
		if config.AUTOAWAY_TIME!=900: self.autoawayInterval.addItem("15 minutes")
		if config.AUTOAWAY_TIME!=1800: self.autoawayInterval.addItem("30 minutes")
		if config.AUTOAWAY_TIME!=3600: self.autoawayInterval.addItem("1 hour")
		if config.AUTOAWAY_TIME!=7200: self.autoawayInterval.addItem("2 hours")
		if config.AUTOAWAY_TIME!=10800: self.autoawayInterval.addItem("3 hours")
		self.autoawayInterval.currentIndexChanged.connect(self.autoawayChange)

		intervalBox = QHBoxLayout()
		intervalBox.addWidget(self.autoAway)
		intervalBox.addWidget(self.autoawayInterval)
		intervalBox.addStretch()

		self.showAwayBack = QCheckBox("Show user away and back\nnotification messages",self)
		if config.SHOW_AWAY_AND_BACK_MESSAGES: self.showAwayBack.setChecked(True)
		self.showAwayBack.stateChanged.connect(self.changedSettingRerender)
		self.showAwayBack.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showAwayNick = QCheckBox("Show away status in nickname\ndisplay",self)
		if config.SHOW_AWAY_STATUS_IN_NICK_DISPLAY: self.showAwayNick.setChecked(True)
		self.showAwayNick.stateChanged.connect(self.changedSettingRerenderNick)
		self.showAwayNick.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")
	
		self.typeCancelInput = QCheckBox("Interacting with the text\ninput widget cancels autoaway",self)
		if config.TYPING_INPUT_CANCELS_AUTOAWAY: self.typeCancelInput.setChecked(True)
		self.typeCancelInput.stateChanged.connect(self.changedSetting)
		self.typeCancelInput.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")
	
		self.windowCancelAway = QCheckBox("Interacting with subwindows\ncancels autoaway",self)
		if config.WINDOW_INTERACTION_CANCELS_AUTOAWAY: self.windowCancelAway.setChecked(True)
		self.windowCancelAway.stateChanged.connect(self.changedSetting)
		self.windowCancelAway.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")
	
		self.appCancelAway = QCheckBox("Interacting with application\ncancels autoaway",self)
		if config.APP_INTERACTION_CANCELS_AUTOAWAY: self.appCancelAway.setChecked(True)
		self.appCancelAway.stateChanged.connect(self.changedSetting)
		self.appCancelAway.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")
	
		if not config.USE_AUTOAWAY:
			self.autoawayInterval.setEnabled(False)
			self.typeCancelInput.setEnabled(False)
			self.windowCancelAway.setEnabled(False)
			self.appCancelAway.setEnabled(False)
			self.autoawayInterval.setEnabled(False)

		self.awayMsg = EmojiAwayAutocomplete(self)
		self.awayMsg.setText(self.default_away)

		fm = self.awayMsg.fontMetrics()
		self.awayMsg.setFixedHeight(fm.height()+10)
		self.awayMsg.setWordWrapMode(QTextOption.NoWrap)
		self.awayMsg.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.awayMsg.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.awayMsg.textChanged.connect(self.setAwayMsg)

		self.autoEmojiAway = QCheckBox(f"Autocomplete emoji shortcodes",self)
		if config.AUTOCOMPLETE_EMOJIS_IN_AWAY_MESSAGE_WIDGET: self.autoEmojiAway.setChecked(True)
		self.autoEmojiAway.stateChanged.connect(self.changeEmojiAuto)

		if not config.ENABLE_EMOJI_SHORTCODES:
			self.autoEmojiAway.setEnabled(False)

		self.autoAliasAway = QCheckBox(f"Interpolate aliases into message",self)
		if config.INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE: self.autoAliasAway.setChecked(True)
		self.autoAliasAway.stateChanged.connect(self.changedSetting)

		if not config.ENABLE_ALIASES:
			self.autoAliasAway.setEnabled(False)

		awayLayout = QVBoxLayout()
		awayLayout.addWidget(self.awayMsg)
		awayLayout.addWidget(self.autoEmojiAway)
		awayLayout.addWidget(self.autoAliasAway)
		awayBox = QGroupBox("")
		awayBox.setAlignment(Qt.AlignLeft)
		awayBox.setLayout(awayLayout)

		awayLayout = QVBoxLayout()
		awayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>away settings</b>"))
		awayLayout.addWidget(self.promptAway)
		awayLayout.addWidget(self.showAwayBack)
		awayLayout.addWidget(self.showAwayNick)
		awayLayout.addWidget(QLabel(' '))
		awayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>autoaway settiings</b>"))
		awayLayout.addLayout(intervalBox)
		awayLayout.addWidget(self.typeCancelInput)
		awayLayout.addWidget(self.windowCancelAway)
		awayLayout.addWidget(self.appCancelAway)
		awayLayout.addWidget(QLabel(' '))
		awayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>default away message</b>"))
		awayLayout.addWidget(awayBox)
		awayLayout.addStretch()

		self.awayPage.setLayout(awayLayout)

		# Input page

		self.inputPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Input")
		entry.widget = self.inputPage
		entry.setIcon(QIcon(INPUT_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.inputPage)

		self.historyLabel = QLabel(f"History size: <b>{str(self.historysize)} lines</b>",self)

		self.historyButton = QPushButton("")
		self.historyButton.clicked.connect(self.setHistorySize)
		self.historyButton.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.historyButton.setFixedSize(fheight +10,fheight + 10)
		self.historyButton.setIcon(QIcon(EDIT_ICON))
		self.historyButton.setToolTip("Change command history size")

		historyLayout = QHBoxLayout()
		historyLayout.addWidget(self.historyButton)
		historyLayout.addWidget(self.historyLabel)
		historyLayout.addStretch()

		self.historyDescription = QLabel("""
			<small>
			If enabled, any text typed into the text input widget is saved to the <b>command history</b>.
			Use the <b>arrow keys</b> to move backwards (<b>&uarr;</b>) and forwards (<b>&darr;</b>) in the 
			<b>command history</b> to issue any previously issued commands.
			</small>
			<br>
			""")
		self.historyDescription.setWordWrap(True)
		self.historyDescription.setAlignment(Qt.AlignJustify)

		self.autocompleteDescription = QLabel("""
			<small>
			To use autocomplete, type the first few characters of a <b>command</b>,
			<b>nickname</b>, <b>channel</b>, <b>emoji shortcode</b>, <b>script filename</b>, or <b>alias</b>
			and then hit <b>tab</b> to complete the entry.
			</small>
			<br>
			""")
		self.autocompleteDescription.setWordWrap(True)
		self.autocompleteDescription.setAlignment(Qt.AlignJustify)

		self.autocompleteCommands = QCheckBox("Commands",self)
		if config.AUTOCOMPLETE_COMMANDS: self.autocompleteCommands.setChecked(True)
		self.autocompleteCommands.stateChanged.connect(self.changedSetting)

		self.autocompleteNicks = QCheckBox("Nicknames",self)
		if config.AUTOCOMPLETE_NICKS: self.autocompleteNicks.setChecked(True)
		self.autocompleteNicks.stateChanged.connect(self.changedSetting)

		self.autocompleteChans = QCheckBox("Channels",self)
		if config.AUTOCOMPLETE_CHANNELS: self.autocompleteChans.setChecked(True)
		self.autocompleteChans.stateChanged.connect(self.changedSetting)

		self.autocompleteEmojis = QCheckBox("Emoji shortcodes",self)
		if config.AUTOCOMPLETE_EMOJIS: self.autocompleteEmojis.setChecked(True)
		self.autocompleteEmojis.stateChanged.connect(self.changedSetting)

		if config.ENABLE_EMOJI_SHORTCODES:
			self.autocompleteEmojis.setEnabled(True)
		else:
			self.autocompleteEmojis.setEnabled(False)

		self.autocompleteAlias = QCheckBox("Aliases",self)
		if config.AUTOCOMPLETE_ALIAS: self.autocompleteAlias.setChecked(True)
		self.autocompleteAlias.stateChanged.connect(self.changedSetting)

		self.enableHistory = QCheckBox("Enable command history",self)
		if config.ENABLE_COMMAND_INPUT_HISTORY: self.enableHistory.setChecked(True)
		self.enableHistory.stateChanged.connect(self.changedHistory)

		if not config.ENABLE_COMMAND_INPUT_HISTORY:
			self.historyButton.setEnabled(False)
			self.historyLabel.setEnabled(False)

		self.enableAutocomplete = QCheckBox("Enable autocomplete",self)
		if config.ENABLE_AUTOCOMPLETE: self.enableAutocomplete.setChecked(True)
		self.enableAutocomplete.stateChanged.connect(self.changedAutocomplete)

		self.autocompleteScripts = QCheckBox("Script filenames",self)
		if config.AUTOCOMPLETE_SCRIPTS: self.autocompleteScripts.setChecked(True)
		self.autocompleteScripts.stateChanged.connect(self.changedSetting)

		self.autocompleteSettings = QCheckBox("Settings",self)
		if config.AUTOCOMPLETE_SETTINGS: self.autocompleteSettings.setChecked(True)
		self.autocompleteSettings.stateChanged.connect(self.changedSetting)

		self.autocompleteUser = QCheckBox("User settings",self)
		if config.AUTOCOMPLETE_USER: self.autocompleteUser.setChecked(True)
		self.autocompleteUser.stateChanged.connect(self.changedSetting)

		if not config.ENABLE_AUTOCOMPLETE:
			self.autocompleteCommands.setEnabled(False)
			self.autocompleteNicks.setEnabled(False)
			self.autocompleteChans.setEnabled(False)
			self.autocompleteEmojis.setEnabled(False)
			self.autocompleteAlias.setEnabled(False)
			self.autocompleteScripts.setEnabled(False)
			self.autocompleteSettings.setEnabled(False)
			self.autocompleteUser.setEnabled(False)

		if not config.ENABLE_ALIASES:
			self.autocompleteAlias.setEnabled(False)

		if not config.ENABLE_USER_COMMAND:
			self.autocompleteUser.setEnabled(False)

		if not config.ENABLE_CONFIG_COMMAND:
			self.autocompleteSettings.setEnabled(False)

		autoMaster = QHBoxLayout()
		autoMaster.addStretch()
		autoMaster.addWidget(self.enableAutocomplete)
		autoMaster.addStretch()

		historyMaster = QHBoxLayout()
		historyMaster.addStretch()
		historyMaster.addWidget(self.enableHistory)
		historyMaster.addStretch()

		autoSettingsLayout = QFormLayout()
		autoSettingsLayout.addRow(self.autocompleteCommands,self.autocompleteNicks)
		autoSettingsLayout.addRow(self.autocompleteChans,self.autocompleteEmojis)
		autoSettingsLayout.addRow(self.autocompleteScripts,self.autocompleteAlias)
		autoSettingsLayout.addRow(self.autocompleteSettings,self.autocompleteUser)

		inputLayout = QVBoxLayout()
		inputLayout.addWidget(widgets.textSeparatorLabel(self,"<b>command history</b>"))
		inputLayout.addWidget(self.historyDescription)
		inputLayout.addLayout(historyMaster)
		inputLayout.addLayout(historyLayout)
		inputLayout.addWidget(QLabel(' '))
		inputLayout.addWidget(widgets.textSeparatorLabel(self,"<b>autocomplete</b>"))
		inputLayout.addWidget(self.autocompleteDescription)
		inputLayout.addLayout(autoMaster)
		inputLayout.addWidget(QLabel(' '))
		inputLayout.addWidget(widgets.textSeparatorLabel(self,"<b>autocomplete enabled for...</b>"))
		inputLayout.addLayout(autoSettingsLayout)
		inputLayout.addStretch()

		self.inputPage.setLayout(inputLayout)

		# Spellcheck page

		self.spellcheckPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Spellcheck")
		entry.widget = self.spellcheckPage
		entry.setIcon(QIcon(SPELLCHECK_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.spellcheckPage)

		self.enableSpellcheck = QCheckBox("Enable spellcheck",self)
		if config.ENABLE_SPELLCHECK: self.enableSpellcheck.setChecked(True)
		self.enableSpellcheck.stateChanged.connect(self.changedSpellcheck)

		self.englishSC = QRadioButton("English")
		self.englishSC.toggled.connect(self.selEnglish)

		self.frenchSC = QRadioButton("Française")
		self.frenchSC.toggled.connect(self.selFrench)

		self.spanishSC = QRadioButton("Español")
		self.spanishSC.toggled.connect(self.selSpanish)

		self.germanSC = QRadioButton("Deutsche")
		self.germanSC.toggled.connect(self.selGerman)

		self.portugueseSC = QRadioButton("Português")
		self.portugueseSC.toggled.connect(self.selPortuguese)

		self.italianSC = QRadioButton("Italiano")
		self.italianSC.toggled.connect(self.selItalian)

		self.dutchSC = QRadioButton("Nederlands")
		self.dutchSC.toggled.connect(self.selDutch)

		self.russianSC = QRadioButton("Русский")
		self.russianSC.toggled.connect(self.selRussian)

		if config.DEFAULT_SPELLCHECK_LANGUAGE=="en": self.englishSC.setChecked(True)
		if config.DEFAULT_SPELLCHECK_LANGUAGE=="fr": self.frenchSC.setChecked(True)
		if config.DEFAULT_SPELLCHECK_LANGUAGE=="es": self.spanishSC.setChecked(True)
		if config.DEFAULT_SPELLCHECK_LANGUAGE=="de": self.germanSC.setChecked(True)
		if config.DEFAULT_SPELLCHECK_LANGUAGE=="pt": self.portugueseSC.setChecked(True)
		if config.DEFAULT_SPELLCHECK_LANGUAGE=="it": self.italianSC.setChecked(True)
		if config.DEFAULT_SPELLCHECK_LANGUAGE=="nl": self.dutchSC.setChecked(True)
		if config.DEFAULT_SPELLCHECK_LANGUAGE=="ru": self.russianSC.setChecked(True)

		self.allowSpellcheck = QCheckBox("Show spellcheck settings in menus",self)
		if config.ALLOW_MENUS_TO_CHANGE_SPELLCHECK_SETTINGS: self.allowSpellcheck.setChecked(True)
		self.allowSpellcheck.stateChanged.connect(self.changedSpellcheck)

		self.spellcheckDistance = QComboBox(self)
		self.spellcheckDistance.addItem(str(config.SPELLCHECKER_DISTANCE))
		if config.SPELLCHECKER_DISTANCE!=1: self.spellcheckDistance.addItem('1')
		if config.SPELLCHECKER_DISTANCE!=2: self.spellcheckDistance.addItem('2')
		if config.SPELLCHECKER_DISTANCE!=2: self.spellcheckDistance.addItem('3')
		self.spellcheckDistance.currentIndexChanged.connect(self.distanceChange)

		self.distanceLabel = QLabel("Levenshtein distance ")

		self.spellcheckColor = widgets.SyntaxTextColor('underline', "<b>Underline Color</b>",self.SPELLCHECK_UNDERLINE_COLOR,self)
		self.spellcheckColor.syntaxChanged.connect(self.underlineChanged)

		distanceLayout = QHBoxLayout()
		distanceLayout.addWidget(self.distanceLabel)
		distanceLayout.addWidget(self.spellcheckDistance)
		distanceLayout.addStretch()

		self.spellcheckBold = QCheckBox("Bold",self)
		if config.SHOW_MISSPELLED_WORDS_IN_BOLD: self.spellcheckBold.setChecked(True)
		self.spellcheckBold.stateChanged.connect(self.changedSpellcheck)

		self.spellcheckItalics = QCheckBox("Italics",self)
		if config.SHOW_MISSPELLED_WORDS_IN_ITALICS: self.spellcheckItalics.setChecked(True)
		self.spellcheckItalics.stateChanged.connect(self.changedSpellcheck)

		self.spellcheckStrikout = QCheckBox("Strikeout",self)
		if config.SHOW_MISSPELLED_WORDS_IN_STRIKEOUT: self.spellcheckStrikout.setChecked(True)
		self.spellcheckStrikout.stateChanged.connect(self.changedSpellcheck)

		self.spellcheckMissColor = QCheckBox("In underline color",self)
		if config.SHOW_MISSPELLED_WORDS_IN_COLOR: self.spellcheckMissColor.setChecked(True)
		self.spellcheckMissColor.stateChanged.connect(self.changedSpellcheck)

		if not config.ENABLE_SPELLCHECK:
			self.englishSC.setEnabled(False)
			self.frenchSC.setEnabled(False)
			self.spanishSC.setEnabled(False)
			self.germanSC.setEnabled(False)
			self.portugueseSC.setEnabled(False)
			self.italianSC.setEnabled(False)
			self.dutchSC.setEnabled(False)
			self.russianSC.setEnabled(False)
			self.allowSpellcheck.setEnabled(False)
			self.distanceLabel.setEnabled(False)
			self.spellcheckDistance.setEnabled(False)
			self.spellcheckColor.setEnabled(False)
			self.spellcheckBold.setEnabled(False)
			self.spellcheckItalics.setEnabled(False)
			self.spellcheckStrikout.setEnabled(False)
			self.spellcheckMissColor.setEnabled(False)

		langLayout = QFormLayout()
		langLayout.addRow(self.englishSC, self.frenchSC)
		langLayout.addRow(self.spanishSC, self.germanSC)
		langLayout.addRow(self.portugueseSC, self.italianSC)
		langLayout.addRow(self.dutchSC,self.russianSC)

		lanSubLayout = QHBoxLayout()
		lanSubLayout.addStretch()
		lanSubLayout.addLayout(langLayout)
		lanSubLayout.addStretch()

		spColorLayout = QHBoxLayout()
		spColorLayout.addStretch()
		spColorLayout.addWidget(self.spellcheckColor)
		spColorLayout.addStretch()

		spFormatLayout = QHBoxLayout()
		spFormatLayout.addStretch()
		spFormatLayout.addWidget(self.spellcheckBold)
		spFormatLayout.addWidget(self.spellcheckItalics)
		spFormatLayout.addWidget(self.spellcheckStrikout)
		spFormatLayout.addStretch()

		spFormatLayout2 = QHBoxLayout()
		spFormatLayout2.addStretch()
		spFormatLayout2.addWidget(self.spellcheckMissColor)
		spFormatLayout2.addStretch()


		self.spellcheckDescription = QLabel(f"""
			<small>
			Misspelled words in the input widget are marked with a <b><span style='text-decoration: underline; color: {self.SPELLCHECK_UNDERLINE_COLOR};'>
			colored underline</span></b>. <b>Right click</b> on a <b>marked word</b> to get <b>suggestions to replace
			the word with</b> or to <b>add that word to the built-in dictionary</b>. The <b>Levenshtein distance</b> setting sets
			how the spellchecker finds suggestions to replace misspelled words; lower numbers are better for
			longer words.
			</small>
			
			""")
		self.spellcheckDescription.setWordWrap(True)
		self.spellcheckDescription.setAlignment(Qt.AlignJustify)

		spellMaster = QHBoxLayout()
		spellMaster.addStretch()
		spellMaster.addWidget(self.enableSpellcheck)
		spellMaster.addStretch()

		spellcheckLayout = QVBoxLayout()
		spellcheckLayout.addWidget(widgets.textSeparatorLabel(self,"<b>spellcheck</b>"))
		spellcheckLayout.addWidget(self.spellcheckDescription)
		spellcheckLayout.addLayout(spellMaster)
		spellcheckLayout.addWidget(QLabel(' '))
		spellcheckLayout.addWidget(widgets.textSeparatorLabel(self,"<b>spellcheck settings</b>"))
		spellcheckLayout.addWidget(self.allowSpellcheck)
		spellcheckLayout.addLayout(distanceLayout)
		spellcheckLayout.addWidget(QLabel(' '))
		spellcheckLayout.addWidget(widgets.textSeparatorLabel(self,"<b>misspelled word appearance</b>"))
		spellcheckLayout.addLayout(spColorLayout)
		spellcheckLayout.addLayout(spFormatLayout)
		spellcheckLayout.addLayout(spFormatLayout2)
		spellcheckLayout.addWidget(QLabel(' '))
		spellcheckLayout.addWidget(widgets.textSeparatorLabel(self,"<b>default spellcheck language</b>"))
		spellcheckLayout.addLayout(lanSubLayout)
		spellcheckLayout.addStretch()

		self.spellcheckPage.setLayout(spellcheckLayout)

		# Log page

		self.logPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Logs")
		entry.widget = self.logPage
		entry.setIcon(QIcon(LOG_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.logPage)

		self.saveChanLogs = QCheckBox("Save logs",self)
		if config.SAVE_CHANNEL_LOGS: self.saveChanLogs.setChecked(True)
		self.saveChanLogs.stateChanged.connect(self.changedChanLogs)

		self.loadChanLogs = QCheckBox("Load logs",self)
		if config.LOAD_CHANNEL_LOGS: self.loadChanLogs.setChecked(True)
		self.loadChanLogs.stateChanged.connect(self.changedLoadLogs)

		self.savePrivLogs = QCheckBox("Save logs",self)
		if config.SAVE_PRIVATE_LOGS: self.savePrivLogs.setChecked(True)
		self.savePrivLogs.stateChanged.connect(self.changedPrivLogs)

		self.loadPrivLogs = QCheckBox("Load logs",self)
		if config.LOAD_PRIVATE_LOGS: self.loadPrivLogs.setChecked(True)
		self.loadPrivLogs.stateChanged.connect(self.changedLoadLogs)

		self.markLog = QCheckBox("Mark end of loaded log",self)
		if config.MARK_END_OF_LOADED_LOG: self.markLog.setChecked(True)
		self.markLog.stateChanged.connect(self.changedSetting)
		
		self.logLabel = QLabel(f"<b>{str(self.logsize)} lines</b>",self)

		self.logsizeButton = QPushButton("")
		self.logsizeButton.clicked.connect(self.setLogSize)
		self.logsizeButton.setAutoDefault(False)

		self.intermittentLog = QCheckBox("Save logs every",self)
		if config.DO_INTERMITTENT_LOG_SAVES: self.intermittentLog.setChecked(True)
		self.intermittentLog.stateChanged.connect(self.changedSetting)

		self.logInterval = QComboBox(self)
		added = False
		if config.LOG_SAVE_INTERVAL==900000:
			self.logInterval.addItem("15 minutes")
			added = True
		if config.LOG_SAVE_INTERVAL==1800000:
			self.logInterval.addItem("30 minutes")
			added = True
		if config.LOG_SAVE_INTERVAL==3600000:
			self.logInterval.addItem("hour")
			added = True
		if config.LOG_SAVE_INTERVAL==7200000:
			self.logInterval.addItem("2 hours")
			added = True
		if config.LOG_SAVE_INTERVAL==10800000:
			self.logInterval.addItem("3 hours")
			added = True
		if added==False: self.logInterval.addItem(f"{config.LOG_SAVE_INTERVAL} ms")
		if config.LOG_SAVE_INTERVAL!=900000: self.logInterval.addItem("15 minutes")
		if config.LOG_SAVE_INTERVAL!=1800000: self.logInterval.addItem("30 minutes")
		if config.LOG_SAVE_INTERVAL!=3600000: self.logInterval.addItem("hour")
		if config.LOG_SAVE_INTERVAL!=7200000: self.logInterval.addItem("2 hours")
		if config.LOG_SAVE_INTERVAL!=10800000: self.logInterval.addItem("3 hours")
		self.logInterval.currentIndexChanged.connect(self.intervalChange)

		intervalBox = QHBoxLayout()
		intervalBox.addWidget(self.intermittentLog)
		intervalBox.addWidget(self.logInterval)
		intervalBox.addStretch()

		if config.SAVE_PRIVATE_LOGS or config.SAVE_CHANNEL_LOGS:
			self.intermittentLog.setEnabled(True)
			self.logInterval.setEnabled(True)
		else:
			self.intermittentLog.setEnabled(False)
			self.logInterval.setEnabled(False)

		self.logDescription = QLabel("""
			<small>
			Full <b>logs</b> are not loaded for display. The below settings
			controls how much of the <b>log</b> is loaded into the application
			for display.
			</small>
			<br>
			""")
		self.logDescription.setWordWrap(True)
		self.logDescription.setAlignment(Qt.AlignJustify)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.logsizeButton.setFixedSize(fheight +10,fheight + 10)
		self.logsizeButton.setIcon(QIcon(EDIT_ICON))
		self.logsizeButton.setToolTip("Change log load size")

		logsizeLayout = QHBoxLayout()
		logsizeLayout.addWidget(self.logsizeButton)
		logsizeLayout.addWidget(self.logLabel)
		logsizeLayout.addStretch()

		if config.LOAD_CHANNEL_LOGS or config.LOAD_PRIVATE_LOGS:
			self.markLog.setEnabled(True)
			self.logsizeButton.setEnabled(True)
			self.logLabel.setEnabled(True)
		else:
			self.markLog.setEnabled(False)
			self.logsizeButton.setEnabled(False)
			self.logLabel.setEnabled(False)

		self.logFullDescription = QLabel(f"""
			<small>
			<b>Logs</b> are saved in JavaScript Object Notation (<b>JSON</B>), and use a format that can
			be read and displayed easily by <b>{APPLICATION_NAME}</b>. If you want to use other
			software to read or parse your IRC <b>logs</b>, a <b>log</b> export tool is built into
			<b>{APPLICATION_NAME}</b>. The tool is located in the "<b>{self.default_tools_menu}</b>"
			menu, under "<b>Export Logs</b>".
			</small>
			<br>
			""")
		self.logFullDescription.setWordWrap(True)
		self.logFullDescription.setAlignment(Qt.AlignJustify)

		self.topicLog = QCheckBox("Topics",self)
		if config.LOG_CHANNEL_TOPICS: self.topicLog.setChecked(True)
		self.topicLog.stateChanged.connect(self.changedSetting)

		self.joinLog = QCheckBox("Joins",self)
		if config.LOG_CHANNEL_JOIN: self.joinLog.setChecked(True)
		self.joinLog.stateChanged.connect(self.changedSetting)

		self.partLog = QCheckBox("Parts",self)
		if config.LOG_CHANNEL_PART: self.partLog.setChecked(True)
		self.partLog.stateChanged.connect(self.changedSetting)

		self.quitLog = QCheckBox("Quits",self)
		if config.LOG_CHANNEL_QUIT: self.quitLog.setChecked(True)
		self.quitLog.stateChanged.connect(self.changedSetting)

		self.nickLog = QCheckBox("Nickname changes",self)
		if config.LOG_CHANNEL_NICKNAME_CHANGE: self.nickLog.setChecked(True)
		self.nickLog.stateChanged.connect(self.changedSetting)

		self.noticeLog = QCheckBox("Channel notices",self)
		if config.LOG_CHANNEL_NOTICE: self.noticeLog.setChecked(True)
		self.noticeLog.stateChanged.connect(self.changedSetting)

		if config.SAVE_CHANNEL_LOGS:
			self.topicLog.setEnabled(True)
			self.joinLog.setEnabled(True)
			self.partLog.setEnabled(True)
			self.quitLog.setEnabled(True)
			self.nickLog.setEnabled(True)
			self.noticeLog.setEnabled(True)
		else:
			self.topicLog.setEnabled(False)
			self.joinLog.setEnabled(False)
			self.partLog.setEnabled(False)
			self.quitLog.setEnabled(False)
			self.nickLog.setEnabled(False)
			self.noticeLog.setEnabled(False)

		chanLayout = QHBoxLayout()
		chanLayout.addStretch()
		chanLayout.addWidget(self.saveChanLogs)
		chanLayout.addStretch()
		chanLayout.addWidget(self.loadChanLogs)
		chanLayout.addStretch()

		privLayout = QHBoxLayout()
		privLayout.addStretch()
		privLayout.addWidget(self.savePrivLogs)
		privLayout.addStretch()
		privLayout.addWidget(self.loadPrivLogs)
		privLayout.addStretch()

		contLayout = QHBoxLayout()
		contLayout.addStretch()
		contLayout.addWidget(self.topicLog)
		contLayout.addWidget(self.joinLog)
		contLayout.addWidget(self.partLog)
		contLayout.addWidget(self.quitLog)
		contLayout.addStretch()

		cont2Layout = QHBoxLayout()
		cont2Layout.addStretch()
		cont2Layout.addWidget(self.nickLog)
		cont2Layout.addWidget(self.noticeLog)
		cont2Layout.addStretch()

		logLayout = QVBoxLayout()
		logLayout.addWidget(widgets.textSeparatorLabel(self,"<b>log settings</b>"))
		logLayout.addWidget(self.logFullDescription)
		logLayout.addWidget(widgets.textSeparatorLabel(self,"<b>channel logs</b>"))
		logLayout.addLayout(chanLayout)
		logLayout.addWidget(widgets.textSeparatorLabel(self,"<b>channel log includes...</b>"))
		logLayout.addLayout(contLayout)
		logLayout.addLayout(cont2Layout)
		logLayout.addWidget(widgets.textSeparatorLabel(self,"<b>private chat logs</b>"))
		logLayout.addLayout(privLayout)
		logLayout.addWidget(QLabel(' '))
		logLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous</b>"))
		logLayout.addWidget(self.markLog)
		logLayout.addLayout(intervalBox)
		logLayout.addWidget(QLabel(' '))
		logLayout.addWidget(widgets.textSeparatorLabel(self,"<b>log load size</b>"))
		logLayout.addWidget(self.logDescription)
		logLayout.addLayout(logsizeLayout)
		logLayout.addStretch()

		self.logPage.setLayout(logLayout)

		# Messages

		self.messagePage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Messages")
		entry.widget = self.messagePage
		entry.setIcon(QIcon(MESSAGE_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.messagePage)

		self.showColors = QCheckBox("Show IRC colors",self)
		if config.DISPLAY_IRC_COLORS: self.showColors.setChecked(True)
		self.showColors.stateChanged.connect(self.changedSettingRerender)

		self.showLinks = QCheckBox("Convert URLs to hyperlinks",self)
		if config.CONVERT_URLS_TO_LINKS: self.showLinks.setChecked(True)
		self.showLinks.stateChanged.connect(self.changedSettingRerender)

		self.createWindow = QCheckBox("Create windows for incoming\nprivate chat",self)
		if config.CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES: self.createWindow.setChecked(True)
		self.createWindow.stateChanged.connect(self.changedSetting)
		self.createWindow.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.createWindowOut = QCheckBox("Create windows for outgoing\nprivate chat",self)
		if config.CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES: self.createWindowOut.setChecked(True)
		self.createWindowOut.stateChanged.connect(self.changedSetting)
		self.createWindowOut.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.writePrivate = QCheckBox("Write private messages to\nserver window",self)
		if config.WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW: self.writePrivate.setChecked(True)
		self.writePrivate.stateChanged.connect(self.changedSetting)
		self.writePrivate.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.writeScroll = QCheckBox("Always scroll chat to bottom\nwhen displaying text",self)
		if config.ALWAYS_SCROLL_TO_BOTTOM: self.writeScroll.setChecked(True)
		self.writeScroll.stateChanged.connect(self.changedSetting)

		self.writeScroll.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.sysPrepend = QComboBox(self)
		if config.SYSTEM_MESSAGE_PREFIX=='':
			current = "Nothing"
		else:
			current = config.SYSTEM_MESSAGE_PREFIX
		self.sysPrepend.addItem(current)
		for s in SYSTEM_PREPEND_OPTIONS:
			if s==current: continue
			self.sysPrepend.addItem(s)
		self.sysPrepend.currentIndexChanged.connect(self.prependChange)

		self.setSystemPrepend = QLabel(f"Prefix system messages with: <big>{current}</big>")

		prepSel = QHBoxLayout()
		prepSel.addWidget(QLabel("Select a symbol:"))
		prepSel.addWidget(self.sysPrepend)

		prepLayout = QVBoxLayout()
		prepLayout.addWidget(self.setSystemPrepend)
		prepLayout.addLayout(prepSel)

		self.linkChannel = QCheckBox("Convert channel names to links",self)
		if config.CONVERT_CHANNELS_TO_LINKS: self.linkChannel.setChecked(True)
		self.linkChannel.stateChanged.connect(self.changedSettingRerender)

		self.noPadding = QCheckBox("Do not pad nicknames in chat\ndisplay",self)
		if config.STRIP_NICKNAME_PADDING_FROM_DISPLAY: self.noPadding.setChecked(True)
		self.noPadding.stateChanged.connect(self.changedSettingRerenderPad)
		self.noPadding.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")
	
		self.ignoreCreateWindow = QCheckBox("Do not create windows for\nmessages from ignored users",self)
		if config.DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS: self.ignoreCreateWindow.setChecked(True)
		self.ignoreCreateWindow.stateChanged.connect(self.changedSetting)
		self.ignoreCreateWindow.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.createNotice = QCheckBox("Create windows for incoming\nprivate notices",self)
		if config.CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES: self.createNotice.setChecked(True)
		self.createNotice.stateChanged.connect(self.changedSetting)
		self.createNotice.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.padLengthLabel = QLabel("Nickname padding:")
		self.padLengthLabelSpec = QLabel("characters")
		self.padLength = QSpinBox()
		self.padLength.setRange(1,99)
		self.padLength.setValue(self.nicknamePadLength)
		self.padLength.valueChanged.connect(self.updatePadLength)

		padLayout = QHBoxLayout()
		padLayout.addWidget(self.padLengthLabel)
		padLayout.addWidget(self.padLength)
		padLayout.addWidget(self.padLengthLabelSpec)
		padLayout.addStretch()

		if config.STRIP_NICKNAME_PADDING_FROM_DISPLAY:
			self.padLengthLabel.setEnabled(False)
			self.padLength.setEnabled(False)
			self.padLengthLabelSpec.setEnabled(False)

		self.writeMessageOut = QCheckBox("Write outgoing private messages\nto the current window",self)
		if config.WRITE_OUTGOING_PRIVATE_MESSAGES_TO_CURRENT_WINDOW: self.writeMessageOut.setChecked(True)
		self.writeMessageOut.stateChanged.connect(self.changedSetting)
		self.writeMessageOut.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		messageLayout = QVBoxLayout()
		messageLayout.addWidget(widgets.textSeparatorLabel(self,"<b>message settings</b>"))
		messageLayout.addWidget(self.showColors)
		messageLayout.addWidget(self.showLinks)
		messageLayout.addWidget(self.linkChannel)
		messageLayout.addWidget(self.writeScroll)
		messageLayout.addWidget(self.noPadding)
		messageLayout.addLayout(padLayout)
		messageLayout.addWidget(QLabel(' '))
		messageLayout.addWidget(widgets.textSeparatorLabel(self,"<b>private messages</b>"))
		messageLayout.addWidget(self.createWindow)
		messageLayout.addWidget(self.createNotice)
		messageLayout.addWidget(self.ignoreCreateWindow)
		messageLayout.addWidget(self.createWindowOut)
		messageLayout.addWidget(self.writePrivate)
		messageLayout.addWidget(self.writeMessageOut)
		messageLayout.addWidget(QLabel(' '))
		messageLayout.addWidget(widgets.textSeparatorLabel(self,"<b>system message prefix</b>"))
		messageLayout.addLayout(prepLayout)
		messageLayout.addStretch()

		self.messagePage.setLayout(messageLayout)

		# Scripting

		self.scriptingPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Scripting")
		entry.widget = self.scriptingPage
		entry.setIcon(QIcon(SCRIPT_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.scriptingPage)

		self.interpolateAlias = QCheckBox("Interpolate aliases into input\nfrom the text input widget",self)
		if config.INTERPOLATE_ALIASES_INTO_INPUT: self.interpolateAlias.setChecked(True)
		self.interpolateAlias.stateChanged.connect(self.changedInterpolate)
		if not config.INTERPOLATE_ALIASES_INTO_INPUT: self.autocompleteAlias.setEnabled(False)
		self.interpolateAlias.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.enableAlias = QCheckBox("Enable aliases",self)
		if config.ENABLE_ALIASES: self.enableAlias.setChecked(True)
		self.enableAlias.stateChanged.connect(self.changedAlias)

		self.enableScripts = QCheckBox("Enable scripting",self)
		if config.SCRIPTING_ENGINE_ENABLED: self.enableScripts.setChecked(True)
		self.enableScripts.stateChanged.connect(self.changedScripting)

		self.showErrors = QCheckBox("Show error messages when\nexecuting scripts",self)
		if config.DISPLAY_SCRIPT_ERRORS: self.showErrors.setChecked(True)
		self.showErrors.stateChanged.connect(self.changedSetting)
		self.showErrors.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("AA")

		self.alias_symbol = QNoSpaceLineEdit(config.ALIAS_INTERPOLATION_SYMBOL)
		self.alias_symbol.setMaximumWidth(wwidth)
		self.alias_symbol.textChanged.connect(self.changedSettingAdvancedSymbol)
		self.alias_symbol_label = QLabel("Alias interpolation symbol")

		aliasLayout = QHBoxLayout()
		aliasLayout.addWidget(self.alias_symbol)
		aliasLayout.addWidget(self.alias_symbol_label)
		aliasLayout.addStretch()

		self.enableShell = QCheckBox(f"{config.ISSUE_COMMAND_SYMBOL}shell",self)
		if config.ENABLE_SHELL_COMMAND: self.enableShell.setChecked(True)
		self.enableShell.stateChanged.connect(self.changedSettingEditor)

		if not config.ENABLE_ALIASES:
			self.enableShell.setEnabled(False)

		self.scriptingDescription = QLabel(f"""
			<small><b>Scripting</b> allows <b>{APPLICATION_NAME}</b> to automate commands upon connection, as well
			as for multiple commands to be executed in sequence. Turning off <b>scripting</b> will
			prevent scripts and connection scripts from being executed or edited in <b>{APPLICATION_NAME}</b>,
			but it will not turn off commands entered in the input widget.
			</small>
			
			""")
		self.scriptingDescription.setWordWrap(True)
		self.scriptingDescription.setAlignment(Qt.AlignJustify)

		seLayout = QHBoxLayout()
		seLayout.addStretch()
		seLayout.addWidget(self.enableScripts)
		seLayout.addStretch()

		self.haltError = QCheckBox("Halt execution on error",self)
		if config.HALT_SCRIPT_EXECUTION_ON_ERROR: self.haltError.setChecked(True)
		self.haltError.stateChanged.connect(self.changedSetting)

		self.requireArgs = QCheckBox(f"Exact argument count with \"usage\"",self)
		if config.REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS: self.requireArgs.setChecked(True)
		self.requireArgs.stateChanged.connect(self.changedSetting)

		self.enableInsert = QCheckBox(f"insert",self)
		if config.ENABLE_INSERT_COMMAND: self.enableInsert.setChecked(True)
		self.enableInsert.stateChanged.connect(self.changedSettingEditor)

		self.promptScript = QCheckBox(f"Prompt for file when calling\n{config.ISSUE_COMMAND_SYMBOL}script with no arguments",self)
		if config.PROMPT_FOR_SCRIPT_FILE: self.promptScript.setChecked(True)
		self.promptScript.stateChanged.connect(self.changedSetting)
		self.promptScript.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.enableDelay = QCheckBox(f"{config.ISSUE_COMMAND_SYMBOL}delay",self)
		if config.ENABLE_DELAY_COMMAND: self.enableDelay.setChecked(True)
		self.enableDelay.stateChanged.connect(self.changedSettingEditor)

		self.enableConfig = QCheckBox(f"{config.ISSUE_COMMAND_SYMBOL}config",self)
		if config.ENABLE_CONFIG_COMMAND: self.enableConfig.setChecked(True)
		self.enableConfig.stateChanged.connect(self.changedSettingEditorConfig)

		self.restrictError = QCheckBox(f"Display error for violations of\nonly and restrict commands",self)
		if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION: self.restrictError.setChecked(True)
		self.restrictError.stateChanged.connect(self.changedSetting)
		self.restrictError.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.enableBuiltin = QCheckBox("Built-in aliases",self)
		if config.ENABLE_BUILT_IN_ALIASES: self.enableBuiltin.setChecked(True)
		self.enableBuiltin.stateChanged.connect(self.changedSettingEditor)

		self.enableGoto = QCheckBox(f"goto",self)
		if config.ENABLE_GOTO_COMMAND: self.enableGoto.setChecked(True)
		self.enableGoto.stateChanged.connect(self.changedSettingEditor)

		self.enableIf = QCheckBox(f"if",self)
		if config.ENABLE_IF_COMMAND: self.enableIf.setChecked(True)
		self.enableIf.stateChanged.connect(self.changedSettingEditorIf)

		self.enableWait = QCheckBox(f"wait",self)
		if config.ENABLE_WAIT_COMMAND: self.enableWait.setChecked(True)
		self.enableWait.stateChanged.connect(self.changedSettingEditor)

		self.enableUser = QCheckBox(f"{config.ISSUE_COMMAND_SYMBOL}user",self)
		if config.ENABLE_USER_COMMAND: self.enableUser.setChecked(True)
		self.enableUser.stateChanged.connect(self.changedSettingEditorConfig)

		if not config.ENABLE_ALIASES:
			self.interpolateAlias.setEnabled(False)
			self.alias_symbol.setEnabled(False)
			self.alias_symbol_label.setEnabled(False)
			self.enableBuiltin.setEnabled(False)

		if not config.SCRIPTING_ENGINE_ENABLED:
			self.restrictError.setEnabled(False)
			self.haltError.setEnabled(False)
			self.enableInsert.setEnabled(False)
			self.showErrors.setEnabled(False)
			self.requireArgs.setEnabled(False)
			self.promptScript.setEnabled(False)
			self.enableGoto.setEnabled(False)
			self.enableIf.setEnabled(False)
			self.enableWait.setEnabled(False)
			self.enableUser.setEnabled(False)

		cmdLayout = QHBoxLayout()
		cmdLayout.addStretch()
		cmdLayout.addWidget(self.enableShell)
		cmdLayout.addWidget(self.enableDelay)
		cmdLayout.addWidget(self.enableConfig)
		cmdLayout.addWidget(self.enableUser)
		cmdLayout.addStretch()

		cmdLayout2 = QHBoxLayout()
		cmdLayout2.addStretch()
		cmdLayout2.addWidget(self.enableInsert)
		cmdLayout2.addWidget(self.enableGoto)
		cmdLayout2.addWidget(self.enableIf)
		cmdLayout2.addWidget(self.enableWait)
		cmdLayout2.addStretch()

		self.escapeHTML = QCheckBox(f"Escape HTML in {config.ISSUE_COMMAND_SYMBOL}print and {config.ISSUE_COMMAND_SYMBOL}prints",self)
		if config.ESCAPE_HTML_FROM_RAW_SYSTEM_MESSAGE: self.escapeHTML.setChecked(True)
		self.escapeHTML.stateChanged.connect(self.changedSettingRerender)

		aliLayout = QHBoxLayout()
		aliLayout.addWidget(self.enableAlias)
		aliLayout.addWidget(self.enableBuiltin)

		scriptingLayout = QVBoxLayout()
		scriptingLayout.addWidget(widgets.textSeparatorLabel(self,"<b>scripting</b>"))
		scriptingLayout.addWidget(self.scriptingDescription)
		scriptingLayout.addLayout(seLayout)
		scriptingLayout.addWidget(widgets.textSeparatorLabel(self,"<b>alias settings</b>"))
		scriptingLayout.addLayout(aliLayout)
		scriptingLayout.addWidget(self.interpolateAlias)
		scriptingLayout.addLayout(aliasLayout)
		scriptingLayout.addWidget(widgets.textSeparatorLabel(self,"<b>error settings</b>"))
		scriptingLayout.addWidget(self.showErrors)
		scriptingLayout.addWidget(self.haltError)
		scriptingLayout.addWidget(self.restrictError)
		scriptingLayout.addWidget(widgets.textSeparatorLabel(self,"<b>command settings</b>"))
		scriptingLayout.addWidget(self.requireArgs)
		scriptingLayout.addWidget(self.promptScript)
		scriptingLayout.addWidget(self.escapeHTML)
		scriptingLayout.addWidget(widgets.textSeparatorLabel(self,"<b>enable/disable commands</b>"))
		scriptingLayout.addLayout(cmdLayout)
		scriptingLayout.addWidget(widgets.textSeparatorLabel(self,"<b>enable/disable script-only commands</b>"))
		scriptingLayout.addLayout(cmdLayout2)
		scriptingLayout.addStretch()

		self.scriptingPage.setLayout(scriptingLayout)

		# Highlighting

		self.syntaxPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Highlighting")
		entry.widget = self.syntaxPage
		entry.setIcon(QIcon(HIGHLIGHT_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.syntaxPage)

		self.syntaxcomment = widgets.SyntaxColor('comment', "<b>Comments</b>",self.SYNTAX_COMMENT_COLOR,self.SYNTAX_COMMENT_STYLE,self)
		self.syntaxcommand = widgets.SyntaxColor('command', "<b>Commands</b>",self.SYNTAX_COMMAND_COLOR,self.SYNTAX_COMMAND_STYLE,self)
		self.syntaxchannel = widgets.SyntaxColor('channel', "<b>Channels</b>",self.SYNTAX_CHANNEL_COLOR,self.SYNTAX_CHANNEL_STYLE,self)
		self.syntaxalias = widgets.SyntaxColor('alias', "<b>Aliases</b>",self.SYNTAX_ALIAS_COLOR,self.SYNTAX_ALIAS_STYLE,self)
		self.syntaxscript = widgets.SyntaxColor('script', "<b>Script-Only Commands</b>",self.SYNTAX_SCRIPT_COLOR,self.SYNTAX_SCRIPT_STYLE,self)
		self.syntaxop = widgets.SyntaxColor('operator', "<b>\"if\" Operators</b>",self.SYNTAX_OPERATOR_COLOR,self.SYNTAX_OPERATOR_STYLE,self)
		self.syntaxfore = widgets.SyntaxTextColor('fore', "<b>Text Color</b>",self.SYNTAX_FOREGROUND,self)
		self.syntaxback = widgets.SyntaxTextColor('back', "<b>Background</b>",self.SYNTAX_BACKGROUND,self)
		self.syntaxnick = widgets.SyntaxColor('nick', "<b>Nicknames</b>",self.SYNTAX_NICKNAME_COLOR,self.SYNTAX_NICKNAME_STYLE,self)
		self.syntaxemoji = widgets.SyntaxColor('emoji', "<b>Emoji Shortcodes</b>",self.SYNTAX_EMOJI_COLOR,self.SYNTAX_EMOJI_STYLE,self)

		self.syntaxcomment.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxcommand.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxchannel.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxalias.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxscript.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxop.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxnick.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxemoji.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxfore.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxback.syntaxChanged.connect(self.syntaxChanged)

		if not config.ENABLE_EMOJI_SHORTCODES:
			self.syntaxemoji.setEnabled(False)

		self.syntaxDescription = QLabel("""
			<small>
			<b>Syntax highlighting</b> is applied to both the script section of the
			connection dialog, and the built-in script editor.
			</small>
			""")
		self.syntaxDescription.setWordWrap(True)
		self.syntaxDescription.setAlignment(Qt.AlignJustify)

		self.syntaxInput = QLabel("""
			<small>
			<b>Syntax highlighting</b> can also be applied to the input widget in
			all server and chat windows. They will use the same color and
			format settings as the script highlighting. <b>Nicknames</b> from the
			current chat and <b>emoji shortcodes</b> will be highlighted using the
			colors and format settings below.
			</small>
			<br>
			""")
		self.syntaxInput.setWordWrap(True)
		self.syntaxInput.setAlignment(Qt.AlignJustify)

		self.toggleSyntaxInput = QCheckBox("Apply syntax highlighting to input",self)
		if config.APPLY_SYNTAX_STYLES_TO_INPUT_WIDGET: self.toggleSyntaxInput.setChecked(True)
		self.toggleSyntaxInput.stateChanged.connect(self.changedSetting)

		tbLay = QFormLayout()
		tbLay.addRow(self.syntaxfore, self.syntaxback)
		tbLay.addRow(self.syntaxcomment, self.syntaxcommand)
		tbLay.addRow(self.syntaxchannel, self.syntaxalias)
		tbLay.addRow(self.syntaxscript,self.syntaxop)

		sbLay = QFormLayout()
		sbLay.addRow(self.syntaxnick, self.syntaxemoji)

		if not config.ENABLE_ALIASES:
			self.syntaxalias.setEnabled(False)

		if not config.SCRIPTING_ENGINE_ENABLED:
			self.syntaxop.setEnabled(False)
			self.syntaxscript.setEnabled(False)

		inputMaster = QHBoxLayout()
		inputMaster.addStretch()
		inputMaster.addWidget(self.toggleSyntaxInput)
		inputMaster.addStretch()

		syntaxLayout = QVBoxLayout()
		syntaxLayout.addWidget(widgets.textSeparatorLabel(self,"<b>syntax highlighting</b>"))
		syntaxLayout.addWidget(self.syntaxDescription)
		syntaxLayout.addLayout(tbLay)
		syntaxLayout.addWidget(QLabel(' '))
		syntaxLayout.addWidget(widgets.textSeparatorLabel(self,"<b>input highlighting</b>"))
		syntaxLayout.addWidget(self.syntaxInput)
		syntaxLayout.addLayout(inputMaster)
		syntaxLayout.addLayout(sbLay)
		syntaxLayout.addStretch()

		self.syntaxPage.setLayout(syntaxLayout)

		# Miscellaneous page

		self.miscPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Miscellaneous")
		entry.widget = self.miscPage
		entry.setIcon(QIcon(MISC_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.miscPage)

		self.enableEmojis = QCheckBox("Enable emoji shortcodes",self)
		if config.ENABLE_EMOJI_SHORTCODES: self.enableEmojis.setChecked(True)
		self.enableEmojis.stateChanged.connect(self.changedEmoji)

		url = bytearray(QUrl.fromLocalFile(resource_path("./merk/resources/emoji_shortcode_list.pdf")).toEncoded()).decode()

		self.emojiDescription = QLabel(f"""
			<small>
			If <b>emoji shortcodes</b> are enabled, you can insert <b>emojis</b> into
			your chat, quit, part, and away messages by using <a href="https://emojibase.dev/docs/shortcodes/"><b>shortcodes</b></a>.
			You can find a complete list of supported <b>shortcodes</b> <a href="{url}">
			here</a>, or a searchable online list <a href="https://carpedm20.github.io/emoji/all.html?enableList=enable_list_alias">here</a>.
			</small>
			<br>
			""")
		self.emojiDescription.setWordWrap(True)
		self.emojiDescription.setAlignment(Qt.AlignJustify)
		self.emojiDescription.setOpenExternalLinks(True)

		escLayout = QHBoxLayout()
		escLayout.addStretch()
		escLayout.addWidget(self.enableEmojis)
		escLayout.addStretch()

		self.partMsg = EmojiQuitAutocomplete(self)
		self.partMsg.setText(self.default_quit_part)

		fm = self.partMsg.fontMetrics()
		self.partMsg.setFixedHeight(fm.height()+10)
		self.partMsg.setWordWrapMode(QTextOption.NoWrap)
		self.partMsg.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.partMsg.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.partMsg.textChanged.connect(self.setQuitMsg)

		self.autoEmojiQuit = QCheckBox(f"Autocomplete emoji shortcodes",self)
		if config.AUTOCOMPLETE_EMOJIS_IN_QUIT_MESSAGE_WIDGET: self.autoEmojiQuit.setChecked(True)
		self.autoEmojiQuit.stateChanged.connect(self.changeEmojiQuit)

		if not config.ENABLE_EMOJI_SHORTCODES:
			self.autoEmojiQuit.setEnabled(False)

		self.autoAliasQuit = QCheckBox(f"Interpolate aliases into message",self)
		if config.INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE: self.autoAliasQuit.setChecked(True)
		self.autoAliasQuit.stateChanged.connect(self.changedSetting)

		if not config.ENABLE_ALIASES:
			self.autoAliasQuit.setEnabled(False)

		qfLayout = QVBoxLayout()
		qfLayout.addWidget(self.partMsg)
		qfLayout.addWidget(self.autoEmojiQuit)
		qfLayout.addWidget(self.autoAliasQuit)

		quitBox = QGroupBox("")
		quitBox.setAlignment(Qt.AlignLeft)
		quitBox.setLayout(qfLayout)

		size_policy = quitBox.sizePolicy()
		size_policy.setHorizontalPolicy(QSizePolicy.Expanding)
		size_policy.setVerticalPolicy(QSizePolicy.Fixed)
		quitBox.setSizePolicy(size_policy)

		self.searchAllTerms = QCheckBox("Search for all terms in\nchannel list searches",self)
		if config.SEARCH_ALL_TERMS_IN_CHANNEL_LIST: self.searchAllTerms.setChecked(True)
		self.searchAllTerms.stateChanged.connect(self.changedSetting)
		self.searchAllTerms.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.examineTopic = QCheckBox("Examine topics in channel\nlist searches",self)
		if config.EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH: self.examineTopic.setChecked(True)
		self.examineTopic.stateChanged.connect(self.changedSetting)
		self.examineTopic.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.searchInstall = QCheckBox(f"Search install directory for files",self)
		if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES: self.searchInstall.setChecked(True)
		self.searchInstall.stateChanged.connect(self.changedSetting)

		miscLayout = QVBoxLayout()
		miscLayout.addWidget(widgets.textSeparatorLabel(self,"<b>default quit/part message</b>"))
		miscLayout.addWidget(quitBox)
		miscLayout.addWidget(QLabel(' '))
		miscLayout.addWidget(widgets.textSeparatorLabel(self,"<b>emoji shortcodes</b>"))
		miscLayout.addWidget(self.emojiDescription)
		miscLayout.addLayout(escLayout)
		miscLayout.addWidget(QLabel(' '))
		miscLayout.addWidget(widgets.textSeparatorLabel(self,"<b>channel list settings</b>"))
		miscLayout.addWidget(self.searchAllTerms)
		miscLayout.addWidget(self.examineTopic)
		miscLayout.addWidget(QLabel(' '))
		miscLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous</b>"))
		miscLayout.addWidget(self.searchInstall)
		miscLayout.addStretch()
		self.miscPage.setLayout(miscLayout)

		# Advanced

		self.advancedPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Advanced")
		entry.widget = self.advancedPage
		entry.setIcon(QIcon(ADVANCED_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.advancedPage)

		self.advancedEnable = QCheckBox("Enable advanced settings",self)
		self.advancedEnable.stateChanged.connect(self.clickedAdvanced)

		self.logEverything = QCheckBox("Save all system messages to log",self)
		if config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE: self.logEverything.setChecked(True)
		self.logEverything.stateChanged.connect(self.changedSettingAdvanced)
		self.logEverything.setEnabled(False)

		self.advancedDescription = QLabel(f"""
			<center><b><span style='color: red;'>WARNING!</b></span> <b>Changing these settings may break your installation,
			break existing scripts, or fill up your hard drive!</b></center><small><br>
			If changing these settings causes the application to no longer function, please run
			<b>{APPLICATION_NAME}</b> with the <b><code>--reset</code></b> command-line flag. This will reset all your
			settings to the default, and should fix any fatal problems.
			</small>
			
			""")
		self.advancedDescription.setWordWrap(True)
		self.advancedDescription.setAlignment(Qt.AlignJustify)

		self.writeConsole = QCheckBox("Write all network input and\noutput to STDOUT",self)
		if config.WRITE_INPUT_AND_OUTPUT_TO_CONSOLE: self.writeConsole.setChecked(True)
		self.writeConsole.stateChanged.connect(self.changedSettingAdvanced)
		self.writeConsole.setEnabled(False)
		self.writeConsole.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.writeFile = QCheckBox("Write all network input and\noutput to a file in the user's\nsettings directory",self)
		if config.WRITE_INPUT_AND_OUTPUT_TO_FILE: self.writeFile.setChecked(True)
		self.writeFile.stateChanged.connect(self.changedSettingAdvanced)
		self.writeFile.setEnabled(False)
		self.writeFile.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.enablePing = QCheckBox("Show server pings in server windows",self)
		if config.SHOW_PINGS_IN_CONSOLE: self.enablePing.setChecked(True)
		self.enablePing.stateChanged.connect(self.changedSettingAdvanced)
		self.enablePing.setEnabled(False)

		aoLayout = QHBoxLayout()
		aoLayout.addStretch()
		aoLayout.addWidget(self.advancedEnable)
		aoLayout.addStretch()

		self.serverHeartbeatLabel = QLabel("Connection heartbeat:")
		self.heartbeatLabelSpec = QLabel("seconds")
		self.heartbeatLength = QSpinBox()
		self.heartbeatLength.setRange(1,300)
		self.heartbeatLength.setValue(self.heartbeat)
		self.heartbeatLength.valueChanged.connect(self.updateHeartbeat)

		hbLayout = QHBoxLayout()
		hbLayout.addWidget(self.serverHeartbeatLabel)
		hbLayout.addWidget(self.heartbeatLength)
		hbLayout.addWidget(self.heartbeatLabelSpec)
		hbLayout.addStretch()

		self.serverHeartbeatLabel.setEnabled(False)
		self.heartbeatLength.setEnabled(False)
		self.heartbeatLabelSpec.setEnabled(False)

		self.maxChatLabel = QLabel("Max message length:")
		self.maxChatLabelSpec = QLabel("characters")
		self.maxChat = QSpinBox()
		self.maxChat.setRange(1,512)
		self.maxChat.setValue(self.IRC_MAX_PAYLOAD_LENGTH)
		self.maxChat.valueChanged.connect(self.updateMaxChat)

		maxLayout = QHBoxLayout()
		maxLayout.addWidget(self.maxChatLabel)
		maxLayout.addWidget(self.maxChat)
		maxLayout.addWidget(self.maxChatLabelSpec)
		maxLayout.addStretch()

		self.maxChatLabel.setEnabled(False)
		self.maxChat.setEnabled(False)
		self.maxChatLabelSpec.setEnabled(False)

		self.floodProtection = QCheckBox("Flood protection for long messages",self)
		if config.FLOOD_PROTECTION_FOR_LONG_MESSAGES: self.floodProtection.setChecked(True)
		self.floodProtection.stateChanged.connect(self.changedSettingAdvanced)
		self.floodProtection.setEnabled(False)

		advancedLayout = QVBoxLayout()
		advancedLayout.addWidget(widgets.textSeparatorLabel(self,"<b>advanced</b>"))
		advancedLayout.addWidget(self.advancedDescription)
		advancedLayout.addLayout(aoLayout)
		advancedLayout.addWidget(QLabel(' '))
		advancedLayout.addWidget(widgets.textSeparatorLabel(self,"<b>advanced settings</b>"))
		advancedLayout.addLayout(hbLayout)
		advancedLayout.addLayout(maxLayout)
		advancedLayout.addWidget(self.floodProtection)
		advancedLayout.addWidget(self.enablePing)
		advancedLayout.addWidget(self.logEverything)
		advancedLayout.addWidget(self.writeConsole)
		advancedLayout.addWidget(self.writeFile)
		advancedLayout.addStretch()

		self.advancedPage.setLayout(advancedLayout)

		# End settings pages

		self.changed.hide()

		# Buttons

		self.restart = QPushButton(" Apply && Restart ")
		self.restart.clicked.connect(self.do_restart)
		self.restart.setAutoDefault(False)
		font = self.restart.font()
		font.setBold(True)
		self.restart.setFont(font)

		self.saveButton = QPushButton("Apply")
		self.saveButton.clicked.connect(self.save)
		self.saveButton.setAutoDefault(False)

		self.cancelButton = QPushButton("Cancel")
		self.cancelButton.clicked.connect(self.close)

		self.restart.hide()

		# Finalize layout

		dialogButtonsLayout = QHBoxLayout()
		dialogButtonsLayout.addStretch()
		dialogButtonsLayout.addWidget(self.changed)
		dialogButtonsLayout.addStretch()
		dialogButtonsLayout.addWidget(self.restart)
		dialogButtonsLayout.addWidget(self.saveButton)
		dialogButtonsLayout.addWidget(self.cancelButton)

		leftLayout = QVBoxLayout()
		# leftLayout.addWidget(QLabel(' '))
		leftLayout.addWidget(self.selector)

		mainLayout = QHBoxLayout()
		mainLayout.addLayout(leftLayout)
		mainLayout.addWidget(self.stack)
		mainLayout.setContentsMargins(1,1,1,1)

		self.finalLayout = QVBoxLayout()
		self.finalLayout.addLayout(mainLayout)
		self.finalLayout.addLayout(dialogButtonsLayout)
		self.finalLayout.setContentsMargins(4,4,4,4)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(self.finalLayout)

		self.setFixedSize(self.finalLayout.sizeHint())

	def save(self):

		got_errors = False
		errors = []

		# Check to make sure the user doesn't try
		# to save blank user information
		if self.nick.text()=='':
			got_errors = True
			errors.append("Nickname is blank")
		if self.username.text()=='':
			got_errors = True
			errors.append("Username is blank")
		if self.realname.text().strip()=='':
			got_errors = True
			errors.append("Realname is blank")

		# Check to make sure the user isn't trying to
		# save blank menu names
		if self.default_main_menu.strip()=='':
			got_errors = True
			errors.append("Main menu name is blank or only contains whitespace")
		if self.default_settings_menu.strip()=='':
			got_errors = True
			errors.append("Settings menu name is blank or only contains whitespace")
		if self.default_tools_menu.strip()=='':
			got_errors = True
			errors.append("Tools menu name is blank or only contains whitespace")
		if self.default_windows_menu.strip()=='':
			got_errors = True
			errors.append("Windows menu name is blank or only contains whitespace")
		if self.default_help_menu.strip()=='':
			got_errors = True
			errors.append("Help menu name is blank or only contains whitespace")

		if got_errors:

			detailed = ''
			for e in errors:
				detailed = detailed + "* "+e+"\n"

			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setWindowIcon(QIcon(APPLICATION_ICON))
			msg.setText("<big><b>Bad or Missing Settings</b></big>")
			msg.setInformativeText("Please correct these settings and try again.")
			msg.setDetailedText(detailed)
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			return

		# Now that we know the settings are "sane", let's
		# apply the settings
		QApplication.setOverrideCursor(Qt.WaitCursor)

		# Save the current focused window
		current_open_window = self.parent.MDI.activeSubWindow()

		reset_built_in = False
		if config.ENABLE_BUILT_IN_ALIASES:
			if not self.enableBuiltin.isChecked():
				reset_built_in = True

		config.DISPLAY_ACTIVE_CHAT_IN_TITLE = self.showChatInTitle.isChecked()
		config.PROMPT_ON_FAILED_CONNECTION = self.promptFail.isChecked()
		config.ALWAYS_SCROLL_TO_BOTTOM = self.writeScroll.isChecked()
		config.NOTIFY_ON_LOST_OR_FAILED_CONNECTION = self.notifyOnLostConnection.isChecked()
		config.ASK_BEFORE_RECONNECT = self.askBeforeReconnect.isChecked()
		config.ENABLE_SPELLCHECK = self.enableSpellcheck.isChecked()
		config.ENABLE_EMOJI_SHORTCODES = self.enableEmojis.isChecked()
		config.DEFAULT_SPELLCHECK_LANGUAGE = self.spellLang
		config.WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW = self.writePrivate.isChecked()
		config.CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES = self.createWindow.isChecked()
		config.SHOW_CONNECTION_UPTIME = self.showUptime.isChecked()
		config.SHOW_CHANNEL_UPTIME = self.showChanUptime.isChecked()
		config.DISPLAY_TIMESTAMP = self.showTimestamps.isChecked()
		config.DISPLAY_IRC_COLORS = self.showColors.isChecked()
		config.CONVERT_URLS_TO_LINKS = self.showLinks.isChecked()
		config.COMMAND_HISTORY_LENGTH = self.historysize
		config.MAXIMUM_LOADED_LOG_SIZE = self.logsize
		config.SAVE_CHANNEL_LOGS = self.saveChanLogs.isChecked()
		config.LOAD_CHANNEL_LOGS = self.loadChanLogs.isChecked()
		config.SAVE_PRIVATE_LOGS = self.savePrivLogs.isChecked()
		config.LOAD_PRIVATE_LOGS = self.loadPrivLogs.isChecked()
		config.AUTOCOMPLETE_COMMANDS = self.autocompleteCommands.isChecked()
		config.AUTOCOMPLETE_NICKS = self.autocompleteNicks.isChecked()
		config.AUTOCOMPLETE_EMOJIS = self.autocompleteEmojis.isChecked()
		config.ASK_BEFORE_DISCONNECT = self.askBeforeDisconnect.isChecked()
		config.DEFAULT_SUBWINDOW_WIDTH = self.subWidth
		config.DEFAULT_SUBWINDOW_HEIGHT = self.subHeight
		config.DEFAULT_QUIT_MESSAGE = self.default_quit_part
		config.TIMESTAMP_24_HOUR = self.timestamp24hour.isChecked()
		config.TIMESTAMP_SHOW_SECONDS = self.timestampSeconds.isChecked()
		config.PLAIN_USER_LISTS = self.plainUserLists.isChecked()
		config.SHOW_USER_INFO_ON_CHAT_WINDOWS = self.showInfo.isChecked()
		config.AUTOCOMPLETE_CHANNELS = self.autocompleteChans.isChecked()
		config.SYNTAX_COMMENT_COLOR = self.SYNTAX_COMMENT_COLOR
		config.SYNTAX_COMMENT_STYLE = self.SYNTAX_COMMENT_STYLE
		config.SYNTAX_COMMAND_COLOR = self.SYNTAX_COMMAND_COLOR
		config.SYNTAX_COMMAND_STYLE = self.SYNTAX_COMMAND_STYLE
		config.SYNTAX_CHANNEL_COLOR = self.SYNTAX_CHANNEL_COLOR
		config.SYNTAX_CHANNEL_STYLE = self.SYNTAX_CHANNEL_STYLE
		config.SYNTAX_BACKGROUND = self.SYNTAX_BACKGROUND
		config.SYNTAX_FOREGROUND = self.SYNTAX_FOREGROUND
		config.SHOW_SYSTRAY_ICON = self.showSystray.isChecked()
		config.SHOW_USERLIST_ON_LEFT = self.showUserlistLeft.isChecked()
		config.FLASH_SYSTRAY_NOTIFICATION = self.systrayNotify.isChecked()
		config.FLASH_SYSTRAY_NICKNAME = self.systrayNickname.isChecked()
		config.FLASH_SYSTRAY_DISCONNECT = self.systrayDisconnect.isChecked()
		config.FLASH_SYSTRAY_PRIVATE = self.systrayPrivate.isChecked()
		config.FLASH_SYSTRAY_KICK = self.systrayKick.isChecked()
		config.FLASH_SYSTRAY_INVITE = self.systrayInvite.isChecked()
		config.FLASH_SYSTRAY_NOTICE = self.systrayNotice.isChecked()
		config.FLASH_SYSTRAY_MODE = self.systrayMode.isChecked()
		config.FLASH_SYSTRAY_LIST = self.listSystray.isChecked()
		config.SYSTRAY_MENU = self.showSystrayMenu.isChecked()
		config.SYNTAX_ALIAS_COLOR = self.SYNTAX_ALIAS_COLOR
		config.SYNTAX_ALIAS_STYLE = self.SYNTAX_ALIAS_STYLE
		config.MENUBAR_CAN_FLOAT = self.menubarFloat.isChecked()
		config.USE_MENUBAR = self.menubar.isChecked()
		config.QT_WINDOW_STYLE = self.qt_style
		config.SHOW_CHANNEL_TOPIC = self.topicDisplay.isChecked()
		config.SHOW_CHANNEL_TOPIC_IN_WINDOW_TITLE = self.topicTitleDisplay.isChecked()
		config.CHANNEL_TOPIC_BOLD = self.topicBold.isChecked()
		config.SHOW_CHANNEL_NAME_AND_MODES = self.channelName.isChecked()
		config.SHOW_BANLIST_MENU = self.showBanlist.isChecked()
		config.SHOW_USERLIST = self.showUserlists.isChecked()
		config.SHOW_INPUT_MENU = self.showInputMenu.isChecked()
		config.SHOW_WINDOWBAR = self.windowBar.isChecked()
		config.WINDOWBAR_TOP_OF_SCREEN = self.windowBarTop.isChecked()
		config.WINDOWBAR_INCLUDE_SERVERS = self.windowBarServers.isChecked()
		config.WINDOWBAR_CAN_FLOAT = self.windowBarFloat.isChecked()
		config.WINDOWBAR_JUSTIFY = self.windowbar_justify
		config.WINDOWBAR_SHOW_ICONS = self.windowBarIcons.isChecked()
		config.WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED = self.windowbarClick.isChecked()
		config.WINDOWBAR_INCLUDE_EDITORS = self.windowBarEditor.isChecked()
		config.SHOW_CHAT_CONTEXT_MENUS = self.showContext.isChecked()
		config.ALWAYS_SHOW_CURRENT_WINDOW_FIRST = self.windowBarFirst.isChecked()
		config.MENUBAR_JUSTIFY = self.menubar_justify
		config.MENUBAR_MENU = self.menubarMenu.isChecked()
		config.WINDOWBAR_MENU = self.windowbarMenu.isChecked()
		config.MAIN_MENU_IRC_NAME = self.default_main_menu
		config.MAIN_MENU_TOOLS_NAME = self.default_tools_menu
		config.MAIN_MENU_WINDOWS_NAME = self.default_windows_menu
		config.MAIN_MENU_HELP_NAME = self.default_help_menu
		config.DARK_MODE = self.darkMode.isChecked()
		config.SIMPLIFIED_DIALOGS = self.simpleConnect.isChecked()
		config.SYSTEM_MESSAGE_PREFIX = self.system_prepend
		config.WINDOWBAR_INCLUDE_CHANNELS = self.windowbarChannels.isChecked()
		config.WINDOWBAR_INCLUDE_PRIVATE = self.windowbarPrivate.isChecked()
		config.JOIN_ON_INVITE = self.autoJoin.isChecked()
		config.GET_HOSTMASKS_ON_CHANNEL_JOIN = self.autoHostmasks.isChecked()
		config.MAIN_MENU_SETTINGS_NAME = self.default_settings_menu
		config.DO_INTERMITTENT_LOG_SAVES = self.intermittentLog.isChecked()
		config.SHOW_STATUS_BAR_ON_SERVER_WINDOWS = self.showStatusServer.isChecked()
		config.SHOW_STATUS_BAR_ON_CHAT_WINDOWS = self.showStatusChat.isChecked()
		config.MAXIMIZE_ON_STARTUP = self.maxOnStart.isChecked()
		config.SHOW_LINKS_TO_NETWORK_WEBPAGES = self.showNetLinks.isChecked()
		config.DISPLAY_NICK_ON_SERVER_WINDOWS = self.displayServNicks.isChecked()
		config.SOUND_NOTIFICATIONS = self.audioNotifications.isChecked()
		config.SOUND_NOTIFICATION_DISCONNECT = self.notifyDisco.isChecked()
		config.SOUND_NOTIFICATION_NICKNAME = self.notifyNickname.isChecked()
		config.SOUND_NOTIFICATION_PRIVATE = self.notifyPrivate.isChecked()
		config.SOUND_NOTIFICATION_NOTICE = self.notifyNotice.isChecked()
		config.SOUND_NOTIFICATION_KICK = self.notifyKick.isChecked()
		config.SOUND_NOTIFICATION_INVITE = self.notifyInvite.isChecked()
		config.SOUND_NOTIFICATION_MODE = self.notifyMode.isChecked()
		config.SOUND_NOTIFICATION_FILE = self.sound
		config.FORCE_MONOSPACE_RENDERING = self.forceMono.isChecked()
		config.FORCE_DEFAULT_STYLE = self.forceDefault.isChecked()
		config.ASK_BEFORE_CLOSE = self.askBeforeExit.isChecked()
		config.AUTOCOMPLETE_ALIAS = self.autocompleteAlias.isChecked()
		config.INTERPOLATE_ALIASES_INTO_INPUT = self.interpolateAlias.isChecked()
		config.REQUEST_CHANNEL_LIST_ON_CONNECTION = self.requestList.isChecked()
		config.EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH = self.examineTopic.isChecked()
		config.WINDOWBAR_INCLUDE_LIST = self.windowbarLists.isChecked()
		config.SHOW_CHANNEL_LIST_IN_WINDOWS_MENU = self.showChannelList.isChecked()
		config.SEARCH_ALL_TERMS_IN_CHANNEL_LIST = self.searchAllTerms.isChecked()
		config.SHOW_SERVER_INFO_IN_WINDOWS_MENU = self.showServerInfo.isChecked()
		config.SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS = self.showServRefresh.isChecked()
		config.SHOW_SERVER_WINDOW_TOOLBAR = self.showServToolbar.isChecked()
		config.SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS = self.showServList.isChecked()
		config.SHOW_STATUS_BAR_ON_LIST_WINDOWS = self.showStatusList.isChecked()
		config.WINDOWBAR_UNDERLINE_ACTIVE_WINDOW = self.windowBarUnderline.isChecked()
		config.WINDOWBAR_HOVER_EFFECT = self.windowBarHover.isChecked()
		config.SHOW_CHANNEL_TOPIC_IN_APPLICATION_TITLE = self.showTopicInTitle.isChecked()
		config.DO_NOT_APPLY_STYLE_TO_INPUT_WIDGET = self.notInputWidget.isChecked()
		config.DO_NOT_APPLY_STYLE_TO_USERLIST = self.notUserlist.isChecked()
		config.DO_NOT_SHOW_APPLICATION_NAME_IN_TITLE = self.noAppNameTitle.isChecked()
		config.APPLY_SYNTAX_STYLES_TO_INPUT_WIDGET = self.toggleSyntaxInput.isChecked()
		config.SYNTAX_NICKNAME_COLOR = self.SYNTAX_NICKNAME_COLOR
		config.SYNTAX_NICKNAME_STYLE = self.SYNTAX_NICKNAME_STYLE
		config.SYNTAX_EMOJI_COLOR = self.SYNTAX_EMOJI_COLOR
		config.SYNTAX_EMOJI_STYLE = self.SYNTAX_EMOJI_STYLE
		config.HIDE_USERLIST_HORIZONTAL_SCROLLBAR = self.hideScroll.isChecked()
		config.SHOW_AWAY_AND_BACK_MESSAGES = self.showAwayBack.isChecked()
		config.SHOW_AWAY_STATUS_IN_USERLISTS = self.showAwayStatus.isChecked()
		config.SHOW_AWAY_STATUS_IN_NICK_DISPLAY = self.showAwayNick.isChecked()
		config.PROMPT_FOR_AWAY_MESSAGE = self.promptAway.isChecked()
		config.CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES = self.createWindowOut.isChecked()
		config.CONVERT_CHANNELS_TO_LINKS = self.linkChannel.isChecked()
		config.DO_NOT_APPLY_STYLES_TO_TEXT = self.noStyles.isChecked()
		config.TYPING_INPUT_CANCELS_AUTOAWAY = self.typeCancelInput.isChecked()
		config.WINDOW_INTERACTION_CANCELS_AUTOAWAY = self.windowCancelAway.isChecked()
		config.APP_INTERACTION_CANCELS_AUTOAWAY = self.appCancelAway.isChecked()
		config.DEFAULT_AWAY_MESSAGE = self.default_away
		config.AUTOCOMPLETE_EMOJIS_IN_AWAY_MESSAGE_WIDGET = self.autocompleteEmojisInAway
		config.DOUBLECLICK_TO_RESTORE_WINDOW_FROM_SYSTRAY = self.doubleclickRestore.isChecked()
		config.LOG_CHANNEL_TOPICS = self.topicLog.isChecked()
		config.LOG_CHANNEL_JOIN = self.joinLog.isChecked()
		config.LOG_CHANNEL_PART = self.partLog.isChecked()
		config.LOG_CHANNEL_QUIT = self.quitLog.isChecked()
		config.LOG_CHANNEL_NICKNAME_CHANGE = self.nickLog.isChecked()
		config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE = self.logEverything.isChecked()
		config.SPELLCHECKER_DISTANCE = self.spellcheck_distance
		config.SHOW_CHANNEL_MENU = self.showChanMenu.isChecked()
		config.WRITE_INPUT_AND_OUTPUT_TO_CONSOLE = self.writeConsole.isChecked()
		config.WRITE_INPUT_AND_OUTPUT_TO_FILE = self.writeFile.isChecked()
		config.AUTOCOMPLETE_EMOJIS_IN_QUIT_MESSAGE_WIDGET = self.autoEmojiQuit.isChecked()
		config.SHOW_STATUS_BAR_ON_EDITOR_WINDOWS = self.showStatusEditor.isChecked()
		config.ENABLE_ALIASES = self.enableAlias.isChecked()
		config.ENABLE_AUTOCOMPLETE = self.enableAutocomplete.isChecked()
		config.ENABLE_STYLE_EDITOR = self.enableStyle.isChecked()
		config.DISPLAY_SCRIPT_ERRORS = self.showErrors.isChecked()
		config.STRIP_NICKNAME_PADDING_FROM_DISPLAY = self.noPadding.isChecked()
		config.WINDOWBAR_INCLUDE_MANAGER = self.windowbarManager.isChecked()
		config.USERLIST_ITEMS_NON_SELECTABLE = self.noSelectUserlists.isChecked()
		config.SHOW_USER_COUNT_DISPLAY = self.channelCount.isChecked()
		config.ALLOW_MENUS_TO_CHANGE_SPELLCHECK_SETTINGS = self.allowSpellcheck.isChecked()
		config.SPELLCHECK_UNDERLINE_COLOR = self.SPELLCHECK_UNDERLINE_COLOR
		config.SHOW_MISSPELLED_WORDS_IN_BOLD = self.spellcheckBold.isChecked()
		config.SHOW_MISSPELLED_WORDS_IN_ITALICS = self.spellcheckItalics.isChecked()
		config.SHOW_MISSPELLED_WORDS_IN_STRIKEOUT = self.spellcheckStrikout.isChecked()
		config.SCRIPTING_ENGINE_ENABLED = self.enableScripts.isChecked()
		config.SHOW_PINGS_IN_CONSOLE = self.enablePing.isChecked()
		config.CLOSING_SERVER_WINDOW_DISCONNECTS = self.enableDisconnect.isChecked()
		config.SHOW_IGNORE_STATUS_IN_USERLISTS = self.ignoreUserlist.isChecked()
		config.WINDOWBAR_SHOW_UNREAD_MESSAGES = self.windowbarUnread.isChecked()
		config.WINDOWBAR_ENTRY_MENU = self.windowbarEntryMenu.isChecked()
		config.DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS = self.ignoreCreateWindow.isChecked()
		config.CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES = self.createNotice.isChecked()
		config.HALT_SCRIPT_EXECUTION_ON_ERROR = self.haltError.isChecked()
		config.REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS = self.requireArgs.isChecked()
		config.ENABLE_INSERT_COMMAND = self.enableInsert.isChecked()
		config.LOG_CHANNEL_NOTICE = self.noticeLog.isChecked()
		config.SHOW_DATES_IN_LOGS = self.showDates.isChecked()
		config.INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE = self.autoAliasAway.isChecked()
		config.INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE = self.autoAliasQuit.isChecked()
		config.HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG = self.noConnectLogo.isChecked()
		config.ASK_FOR_SERVER_ON_STARTUP = self.showConnect.isChecked()
		config.PROMPT_FOR_SCRIPT_FILE = self.promptScript.isChecked()
		config.SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR = self.serverHidden.isChecked()
		config.HIDE_SERVER_WINDOWS_ON_SIGNON = self.hideServer.isChecked()
		config.ENABLE_DELAY_COMMAND = self.enableDelay.isChecked()
		config.WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS = self.windowbarItalics.isChecked()
		config.DOUBLECLICK_TO_OPEN_PRIVATE_CHAT = self.dcPrivate.isChecked()
		config.AUTOCOMPLETE_SCRIPTS = self.autocompleteScripts.isChecked()
		config.MAXIMIZE_SUBWINDOWS_ON_CREATION = self.autoMaxSubwindow.isChecked()
		config.SHOW_CHANNEL_NAME_IN_SUBWINDOW_TITLE = self.nameTitleDisplay.isChecked()
		config.SHOW_HIDDEN_CHANNEL_WINDOWS_IN_WINDOWBAR = self.channelHidden.isChecked()
		config.SHOW_HIDDEN_PRIVATE_WINDOWS_IN_WINDOWBAR = self.privateHidden.isChecked()
		config.SYNTAX_SCRIPT_COLOR = self.SYNTAX_SCRIPT_COLOR
		config.SYNTAX_SCRIPT_STYLE = self.SYNTAX_SCRIPT_STYLE
		config.AUTOCOMPLETE_SETTINGS = self.autocompleteSettings.isChecked()
		config.ENABLE_CONFIG_COMMAND = self.enableConfig.isChecked()
		config.ENABLE_SHELL_COMMAND = self.enableShell.isChecked()
		config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION = self.restrictError.isChecked()
		config.MENUBAR_DOCKED_AT_TOP = self.menubarTop.isChecked()
		config.NICKNAME_PAD_LENGTH = self.nicknamePadLength
		config.TWISTED_CLIENT_HEARTBEAT = self.heartbeat
		config.ESCAPE_HTML_FROM_RAW_SYSTEM_MESSAGE = self.escapeHTML.isChecked()
		config.HIDE_WINDOWBAR_IF_EMPTY = self.autoHide.isChecked()
		config.WINDOWBAR_INCLUDE_README = self.windowbarReadme.isChecked()
		config.WINDOWBAR_BOLD_ACTIVE_WINDOW = self.windowBarBold.isChecked()
		config.MENUBAR_HOVER_EFFECT = self.menubarBold.isChecked()
		config.ENABLE_BUILT_IN_ALIASES = self.enableBuiltin.isChecked()
		config.SYNTAX_OPERATOR_COLOR = self.SYNTAX_OPERATOR_COLOR
		config.SYNTAX_OPERATOR_STYLE = self.SYNTAX_OPERATOR_STYLE
		config.ENABLE_GOTO_COMMAND = self.enableGoto.isChecked()
		config.ENABLE_IF_COMMAND = self.enableIf.isChecked()
		config.WRITE_OUTGOING_PRIVATE_MESSAGES_TO_CURRENT_WINDOW = self.writeMessageOut.isChecked()
		config.RUBBER_BAND_RESIZE = self.windowRubberSize.isChecked()
		config.RUBBER_BAND_MOVE = self.windowRubberMove.isChecked()
		config.INPUT_CURSOR_WIDTH = self.INPUT_CURSOR_WIDTH
		config.ENABLE_WAIT_COMMAND = self.enableWait.isChecked()
		config.ELIDE_AWAY_MSG_IN_USERLIST_CONTEXT = self.elideAway.isChecked()
		config.ELIDE_HOSTMASK_IN_USERLIST_CONTEXT = self.elideHostmask.isChecked()
		config.USERLIST_CONTEXT_MENU = self.ulistContext.isChecked()
		config.HOSTMASK_FETCH_FREQUENCY = self.HOSTMASK_FETCH_FREQUENCY
		config.DO_NOT_SHOW_SERVER_IN_TITLE = self.noShowServerTitle.isChecked()
		config.SHOW_CONNECTIONS_IN_SYSTRAY_MENU = self.stmConnections.isChecked()
		config.SHOW_SETTINGS_IN_SYSTRAY_MENU = self.stmSettings.isChecked()
		config.SHOW_DIRECTORIES_IN_SYSTRAY_MENU = self.stmDirs.isChecked()
		config.SHOW_LINKS_IN_SYSTRAY_MENU = self.stmLinks.isChecked()
		config.SHOW_LIST_IN_SYSTRAY_MENU = self.stmList.isChecked()
		config.SHOW_LOGS_IN_SYSTRAY_MENU = self.stmLogs.isChecked()
		config.SHOW_LOGS_IN_WINDOWS_MENU = self.showLogsInWindows.isChecked()
		config.DELAY_AUTO_RECONNECTION = self.delayReconnect.isChecked()
		config.RECONNECTION_DELAY = self.RECONNECTION_DELAY
		config.AUTOCOMPLETE_USER = self.autocompleteUser.isChecked()
		config.ENABLE_USER_COMMAND = self.enableUser.isChecked()
		config.IRC_MAX_PAYLOAD_LENGTH = self.IRC_MAX_PAYLOAD_LENGTH
		config.FLOOD_PROTECTION_FOR_LONG_MESSAGES = self.floodProtection.isChecked()
		config.SEARCH_INSTALL_DIRECTORY_FOR_FILES = self.searchInstall.isChecked()

		if self.SET_SUBWINDOW_ORDER.lower()=='creation':
			self.parent.MDI.setActivationOrder(QMdiArea.CreationOrder)
		elif self.SET_SUBWINDOW_ORDER.lower()=='stacking':
			self.parent.MDI.setActivationOrder(QMdiArea.StackingOrder)
		elif self.SET_SUBWINDOW_ORDER.lower()=='activation':
			self.parent.MDI.setActivationOrder(QMdiArea.ActivationHistoryOrder)
		else:
			self.parent.MDI.setActivationOrder(QMdiArea.CreationOrder)
		config.SET_SUBWINDOW_ORDER = self.SET_SUBWINDOW_ORDER

		if self.fullScreen.isChecked():
			if not config.SHOW_FULL_SCREEN:
				config.SHOW_FULL_SCREEN = True
				if not self.parent.fullscreen:
					self.parent.showFullScreen()
		else:
			if config.SHOW_FULL_SCREEN:
				config.SHOW_FULL_SCREEN = False
				if not self.parent.fullscreen:
					self.parent.showNormal()
		
		if config.MINIMIZE_TO_SYSTRAY==True:
			if not self.minSystray.isChecked():
				if self.parent.is_hidden:
					self.parent.toggleHide()
					self.parent.showNormal()
		config.MINIMIZE_TO_SYSTRAY = self.minSystray.isChecked()

		if self.changed_alias_symbol:
			config.ALIAS_INTERPOLATION_SYMBOL = self.alias_symbol.text()

		if not self.enableHistory.isChecked():
			if config.ENABLE_COMMAND_INPUT_HISTORY:
				self.parent.clearCommandHistory()

		config.ENABLE_COMMAND_INPUT_HISTORY = self.enableHistory.isChecked()

		if config.FLASH_SYSTRAY_SPEED!=self.flash:
			config.FLASH_SYSTRAY_SPEED = self.flash

		if self.autoAway.isChecked()!= config.USE_AUTOAWAY:
			self.parent.resetAllAutoawayTimers()

		config.USE_AUTOAWAY = self.autoAway.isChecked()

		if self.awayInterval!=config.AUTOAWAY_TIME:
			config.AUTOAWAY_TIME = self.awayInterval
			self.parent.resetAllAutoawayTimers()

		if config.DO_NOT_SHOW_APPLICATION_NAME_IN_TITLE:
			self.parent.setWindowTitle(' ')
		else:
			self.parent.setWindowTitle(APPLICATION_NAME)

		if self.alwaysOnTop.isChecked():
			if not config.ALWAYS_ON_TOP:
				config.ALWAYS_ON_TOP = True
				if not self.parent.ontop:
					self.parent.setWindowFlags(self.parent.windowFlags() | Qt.WindowStaysOnTopHint)
					if not self.parent.is_hidden:
						self.parent.show()
		else:
			if config.ALWAYS_ON_TOP:
				config.ALWAYS_ON_TOP = False
				if not self.parent.ontop:
					self.parent.setWindowFlags(self.parent.windowFlags() & ~Qt.WindowStaysOnTopHint)
					if not self.parent.is_hidden:
						self.parent.show()

		if self.interval!=config.LOG_SAVE_INTERVAL:
			config.LOG_SAVE_INTERVAL = self.interval
			self.parent.updateInterval()

		if self.user_changed:
			user.NICKNAME = self.nick.text()
			user.ALTERNATE = self.alternative.text()
			user.USERNAME = self.username.text()
			user.REALNAME = self.realname.text()
			user.USERINFO = self.userinfo.text().strip()
			user.FINGER = self.finger.text().strip()
			user.save_user(user.USER_FILE)

		if config.TIMESTAMP_24_HOUR:
			ts = '%H:%M'
		else:
			ts = '%I:%M'
		if config.TIMESTAMP_SHOW_SECONDS: ts = ts + ':%S'

		config.TIMESTAMP_FORMAT = ts

		if self.newfont!=None:
			config.APPLICATION_FONT = self.newfont.toString()
			self.parent.app.setFont(self.newfont)
			self.parent.setAllFont(self.newfont)

		# Save new settings to the config file
		config.save_settings(config.CONFIG_FILE)

		self.parent.buildSettingsMenu()
		self.parent.buildWindowsMenu()

		self.parent.app.setStyle(self.qt_style)
		font = self.parent.app.font()
		self.parent.app.setFont(font)
		self.parent.setAllFont(font)

		self.parent.setAllLanguage(config.DEFAULT_SPELLCHECK_LANGUAGE)
		if self.rerender: self.parent.reRenderAll()
		if self.rerenderUsers: self.parent.rerenderUserlists()
		if self.rerenderStyle: self.parent.reApplyStyle()

		if self.rerenderNick:
			self.parent.rerenderAllNickDisplays()
			self.parent.toggleNickDisplay()
			if not self.rerenderUsers: self.parent.rerenderUserlists()

		if config.SHOW_SYSTRAY_ICON:
			self.parent.tray.setVisible(True)
			self.parent.tray.show()
			self.parent.buildSystrayMenu()
		else:
			self.parent.tray.setVisible(False)
			self.parent.tray.hide()

		if self.windowbar_change:
			# Build menubar/menus
			self.parent.buildMenu()

			# Set the windowbar
			self.parent.initWindowbar()

		if self.swapUserlists: self.parent.swapAllUserlists()

		if self.toggleUserlist: self.parent.toggleAllUserlists()

		self.parent.toggleSpellcheck()

		self.parent.toggleInputMenu()

		self.parent.toggleServNickDisplay()

		self.parent.toggleRefreshButton()

		self.parent.updateStatusBar()

		self.parent.toggleServerToolbar()

		self.parent.toggleRubberbanding()

		self.parent.toggleScrollbar()

		self.parent.toggleCursorWidth()

		self.parent.toggleUserinfo()

		self.parent.refreshAllTopic()
		if config.SHOW_CHANNEL_TOPIC:
			self.parent.showAllTopic()
		else:
			self.parent.hideAllTopic()

		if reset_built_in: commands.clearTemporaryAliases()
		commands.build_help_and_autocomplete()

		# Refresh editor windows with any changes to syntax highlighting
		if self.syntax_did_change:
			for window in self.parent.getAllEditorWindows():
				if hasattr(window,"widget"):
					c = window.widget()
					if hasattr(c,"refreshHighlighter"):
						c.refreshHighlighter()

		w = self.parent.MDI.activeSubWindow()
		self.parent.merk_subWindowActivated(w)

		self.parent.MDI.setActiveSubWindow(current_open_window)
		self.parent.merk_subWindowActivated(current_open_window)

		QApplication.restoreOverrideCursor()

		# Close the dialog
		self.close()