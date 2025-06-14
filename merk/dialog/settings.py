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

import os,sys

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

			self.fontLabel.setText(f"<b>{font_name}, {font_size} pt</b>")
			self.changed.show()
			self.boldApply()
		self.selector.setFocus()

	def setWinsize(self):
		
		x = dialog.SizeDialog(self)
		if x:
			self.subWidth = x[0]
			self.subHeight = x[1]
			self.sizeLabel.setText(f"<b>{str(self.subWidth)}x{str(self.subHeight)} px</b>")
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
			self.historyLabel.setText(f"<b>{str(self.historysize)} lines</b>")
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

	def changedSetting(self,state):
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()

	def changedInterpolate(self,state):
		if self.interpolateAlias.isChecked():
			self.autocompleteAlias.setEnabled(True)
		else:
			self.autocompleteAlias.setEnabled(False)
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
		else:
			self.notifyDisco.setEnabled(True)
			self.notifyNickname.setEnabled(True)
			self.notifyPrivate.setEnabled(True)
			self.notifyNotice.setEnabled(True)
			self.notifyKick.setEnabled(True)
			self.notifyInvite.setEnabled(True)
			self.notifyMode.setEnabled(True)
		self.changed.show()
		self.boldApply()
		self.selector.setFocus()
		

	def changedSystrayMin(self,state):
		if self.showSystray.isChecked():
			self.showSystrayMenu.setEnabled(True)
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
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

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
		else:
			self.listSystray.setEnabled(False)
			self.systrayDisconnect.setEnabled(False)
			self.systrayNickname.setEnabled(False)
			self.systrayPrivate.setEnabled(False)
			self.systrayKick.setEnabled(False)
			self.systrayInvite.setEnabled(False)
			self.systrayNotice.setEnabled(False)
			self.systrayMode.setEnabled(False)
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def changedMenubarSetting(self,state):
		if self.menubar.isChecked():
			self.menubarFloat.setEnabled(True)
			self.menubarJustify.setEnabled(True)
			self.menubarMenu.setEnabled(True)
		else:
			self.menubarFloat.setEnabled(False)
			self.menubarJustify.setEnabled(False)
			self.menubarMenu.setEnabled(False)
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def changedEmoji(self,state):
		if self.enableEmojis.isChecked():
			self.autocompleteEmojis.setEnabled(True)
		else:
			self.autocompleteEmojis.setEnabled(False)
		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

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
		else:
			self.topicBold.setEnabled(False)
			self.channelName.setEnabled(False)
			self.showBanlist.setEnabled(False)

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def changedUserlistVisibility(self,i):
		self.toggleUserlist = True

		if self.showUserlists.isChecked():
			self.plainUserLists.setEnabled(True)
			self.showUserlistLeft.setEnabled(True)
			self.hideScroll.setEnabled(True)
		else:
			self.plainUserLists.setEnabled(False)
			self.showUserlistLeft.setEnabled(False)
			self.hideScroll.setEnabled(False)

		self.selector.setFocus()
		self.changed.show()
		self.boldApply()

	def changedSpellcheck(self,i):
		if self.enableSpellcheck.isChecked():
			self.englishSC.setEnabled(True)
			self.frenchSC.setEnabled(True)
			self.spanishSC.setEnabled(True)
			self.germanSC.setEnabled(True)
		else:
			self.englishSC.setEnabled(False)
			self.frenchSC.setEnabled(False)
			self.spanishSC.setEnabled(False)
			self.germanSC.setEnabled(False)
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
		self.windowbar_change = True
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
		os.execl(sys.executable, sys.executable, *sys.argv)

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

		self.qt_style = config.QT_WINDOW_STYLE

		self.windowbar_justify = config.WINDOWBAR_JUSTIFY

		self.menubar_justify = config.MENUBAR_JUSTIFY

		self.system_prepend = config.SYSTEM_MESSAGE_PREFIX

		self.user_changed = False

		self.refreshTopics = False
		self.refreshTitles = False
		self.swapUserlists = False
		self.toggleUserlist = False
		self.rerenderStyle = False

		self.windowbar_change = False

		self.default_main_menu = config.MAIN_MENU_IRC_NAME
		self.default_tools_menu = config.MAIN_MENU_TOOLS_NAME
		self.default_windows_menu = config.MAIN_MENU_WINDOWS_NAME
		self.default_help_menu = config.MAIN_MENU_HELP_NAME
		self.default_settings_menu = config.MAIN_MENU_SETTINGS_NAME

		self.interval = config.LOG_SAVE_INTERVAL
		self.awayInterval = config.AUTOAWAY_TIME

		self.sound = config.SOUND_NOTIFICATION_FILE

		self.syntax_did_change = False

		self.setWindowTitle("Settings")
		self.setWindowIcon(QIcon(SETTINGS_ICON))

		self.selector = QListWidget(self)
		self.stack = QStackedWidget(self)

		f = self.selector.font()
		f.setBold(True)
		self.selector.setFont(f)

		self.changed = QLabel("<b>Settings changed.</b>&nbsp;&nbsp;")

		if is_running_from_pyinstaller():
			self.restart = QLabel("<b>Restart required.</b>")
		else:
			self.restart = QLabel(f"<b><a href=\"restart\">Apply & restart {APPLICATION_NAME}.</a></b>")
			self.restart.setOpenExternalLinks(False)
			self.restart.linkActivated.connect(self.do_restart)

		fm = QFontMetrics(self.font())
		fwidth = fm.width('X') * 27
		self.selector.setMaximumWidth(fwidth)

		add_factor = 10
		self.selector.setIconSize(QSize(fm.height()+add_factor,fm.height()+add_factor))

		self.selector.itemClicked.connect(self.selectorClick)

		self.selector.setStyleSheet("background-color: transparent; border-width: 0px; border-color: transparent;")

		# Application page

		self.applicationPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("General")
		entry.widget = self.applicationPage
		entry.setIcon(QIcon(SETTINGS_ICON))
		self.selector.addItem(entry)
		self.selector.setCurrentItem(entry)

		self.stack.addWidget(self.applicationPage)
		self.stack.setCurrentWidget(self.applicationPage)

		f = self.font()
		fs = f.toString()
		pfs = fs.split(',')
		font_name = pfs[0]
		font_size = pfs[1]

		self.fontLabel = QLabel(f"<b>{font_name}, {font_size} pt</b>",self)

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

		self.sizeLabel = QLabel(f"<b>{str(self.subWidth)}x{str(self.subHeight)} px</b>",self)

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
		
		self.maxOnStart = QCheckBox("Maximize window on startup",self)
		if config.MAXIMIZE_ON_STARTUP: self.maxOnStart.setChecked(True)
		self.maxOnStart.stateChanged.connect(self.changedSetting)

		self.alwaysOnTop = QCheckBox("Main window always on top",self)
		if config.ALWAYS_ON_TOP: self.alwaysOnTop.setChecked(True)
		self.alwaysOnTop.stateChanged.connect(self.changedSetting)

		self.askBeforeExit = QCheckBox("Ask before closing app",self)
		if config.ASK_BEFORE_CLOSE: self.askBeforeExit.setChecked(True)
		self.askBeforeExit.stateChanged.connect(self.changedSetting)

		self.examineTopic = QCheckBox("Examine topics in channel\nlist searches",self)
		if config.EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH: self.examineTopic.setChecked(True)
		self.examineTopic.stateChanged.connect(self.changedSetting)

		self.examineTopic.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showChannelList = QCheckBox(f"Show channel list options in\nthe \"{config.MAIN_MENU_WINDOWS_NAME}\" menu",self)
		if config.SHOW_CHANNEL_LIST_IN_WINDOWS_MENU: self.showChannelList.setChecked(True)
		self.showChannelList.stateChanged.connect(self.changedSetting)

		self.showChannelList.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.searchAllTerms = QCheckBox("Search for all terms in\nchannel list searches",self)
		if config.SEARCH_ALL_TERMS_IN_CHANNEL_LIST: self.searchAllTerms.setChecked(True)
		self.searchAllTerms.stateChanged.connect(self.changedSetting)

		self.searchAllTerms.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showServerInfo = QCheckBox(f"Show server information in\nthe \"{config.MAIN_MENU_WINDOWS_NAME}\" menu",self)
		if config.SHOW_SERVER_INFO_IN_WINDOWS_MENU: self.showServerInfo.setChecked(True)
		self.showServerInfo.stateChanged.connect(self.changedSetting)

		self.showServerInfo.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.noAppNameTitle = QCheckBox("Do not show application name in\nwindow title",self)
		if config.DO_NOT_SHOW_APPLICATION_NAME_IN_TITLE: self.noAppNameTitle.setChecked(True)
		self.noAppNameTitle.stateChanged.connect(self.changedSetting)

		self.noAppNameTitle.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		applicationLayout = QVBoxLayout()
		applicationLayout.addWidget(widgets.textSeparatorLabel(self,"<b>default font</b>"))
		applicationLayout.addLayout(fontLayout)
		applicationLayout.addWidget(QLabel(' '))
		applicationLayout.addWidget(widgets.textSeparatorLabel(self,"<b>initial window size</b>"))
		applicationLayout.addLayout(sizeLayout)
		applicationLayout.addWidget(QLabel(' '))
		applicationLayout.addWidget(widgets.textSeparatorLabel(self,"<b>application</b>"))
		applicationLayout.addWidget(self.maxOnStart)
		applicationLayout.addWidget(self.alwaysOnTop)
		applicationLayout.addWidget(self.askBeforeExit)
		applicationLayout.addWidget(self.simpleConnect)
		applicationLayout.addWidget(self.examineTopic)
		applicationLayout.addWidget(self.searchAllTerms)
		applicationLayout.addWidget(self.showChannelList)
		applicationLayout.addWidget(self.showServerInfo)
		applicationLayout.addWidget(self.noAppNameTitle)
		applicationLayout.addStretch()

		self.applicationPage.setLayout(applicationLayout)

		# Widget page

		self.appearancePage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Appearance")
		entry.widget = self.appearancePage
		entry.setIcon(QIcon(WIDGET_ICON))
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
		styleLayout.addWidget(QLabel("<b>Widget Style</b> "))
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
			<br>
			""")
		self.darkDescription.setWordWrap(True)
		self.darkDescription.setAlignment(Qt.AlignJustify)

		self.darkMode = QCheckBox("Enable dark mode",self)
		if config.DARK_MODE: self.darkMode.setChecked(True)
		self.darkMode.stateChanged.connect(self.setDarkMode)

		self.forceDefault = QCheckBox("Force all chat windows to use\nthe default text style",self)
		if config.FORCE_DEFAULT_STYLE: self.forceDefault.setChecked(True)
		self.forceDefault.stateChanged.connect(self.changeSettingStyle)

		self.forceDefault.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.notInputWidget = QCheckBox("Force default text style on\nthe text input widget",self)
		if config.DO_NOT_APPLY_STYLE_TO_INPUT_WIDGET: self.notInputWidget.setChecked(True)
		self.notInputWidget.stateChanged.connect(self.changeSettingStyle)

		self.notInputWidget.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.notUserlist = QCheckBox("Force default text style on\nthe userlist",self)
		if config.DO_NOT_APPLY_STYLE_TO_USERLIST: self.notUserlist.setChecked(True)
		self.notUserlist.stateChanged.connect(self.changeSettingStyle)

		self.notUserlist.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		if self.forceDefault.isChecked():
			self.notInputWidget.setEnabled(False)
			self.notUserlist.setEnabled(False)

		appearanceLayout = QVBoxLayout()
		appearanceLayout.addWidget(widgets.textSeparatorLabel(self,"<b>widget style</b>"))
		appearanceLayout.addWidget(self.styleDescription)
		appearanceLayout.addLayout(styleLayout)
		appearanceLayout.addWidget(QLabel(' '))
		appearanceLayout.addWidget(widgets.textSeparatorLabel(self,"<b>dark mode</b>"))
		appearanceLayout.addWidget(self.darkDescription)
		appearanceLayout.addWidget(self.darkMode)
		appearanceLayout.addWidget(QLabel(' '))
		appearanceLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous</b>"))
		appearanceLayout.addWidget(self.forceDefault)
		appearanceLayout.addWidget(self.notInputWidget)
		appearanceLayout.addWidget(self.notUserlist)
		appearanceLayout.addStretch()

		self.appearancePage.setLayout(appearanceLayout)

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

		self.showChatInTitle = QCheckBox("Show active subwindow information\nin application title",self)
		if config.DISPLAY_ACTIVE_CHAT_IN_TITLE: self.showChatInTitle.setChecked(True)
		self.showChatInTitle.stateChanged.connect(self.changedSetting)

		self.showChatInTitle.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")
	
		self.showTopicInTitle = QCheckBox("Show current channel topic in\napplication title",self)
		if config.SHOW_CHANNEL_TOPIC_IN_APPLICATION_TITLE: self.showTopicInTitle.setChecked(True)
		self.showTopicInTitle.stateChanged.connect(self.changedSetting)

		self.showTopicInTitle.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		statusLayout = QFormLayout()
		statusLayout.addRow(self.showStatusServer,self.showStatusChat)
		statusLayout.addRow(self.showStatusList)

		subwindowLayout = QVBoxLayout()
		subwindowLayout.addWidget(widgets.textSeparatorLabel(self,"<b>server windows</b>"))
		subwindowLayout.addWidget(self.showServToolbar)
		subwindowLayout.addWidget(self.showServList)
		subwindowLayout.addWidget(self.showServRefresh)
		subwindowLayout.addWidget(self.displayServNicks)
		subwindowLayout.addWidget(QLabel(' '))
		subwindowLayout.addWidget(widgets.textSeparatorLabel(self,"<b>chat windows</b>"))
		subwindowLayout.addWidget(self.showInfo)
		subwindowLayout.addWidget(self.showTopicInTitle)
		subwindowLayout.addWidget(QLabel(' '))
		subwindowLayout.addWidget(widgets.textSeparatorLabel(self,"<b>status bars</b>"))
		subwindowLayout.addLayout(statusLayout)
		subwindowLayout.addWidget(QLabel(' '))
		subwindowLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous</b>"))
		subwindowLayout.addWidget(self.showContext)
		subwindowLayout.addWidget(self.showInputMenu)
		subwindowLayout.addWidget(self.showChatInTitle)
		subwindowLayout.addStretch()

		self.subwindowPage.setLayout(subwindowLayout)

		# User page

		self.userPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("User")
		entry.widget = self.userPage
		entry.setIcon(QIcon(PRIVATE_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.userPage)

		self.userDescription = QLabel("""
			<small>
			You can set the default settings needed to connect to
			an IRC server here. These options can be set or changed
			in the server connection dialog. If both your <b>nickname</b> and <b>alternate</b>
			nickname are taken (or if you have not set an <b>alternate</b> nickname),
			a random number will be generated and attached to your <b>nickname</b> for use.
			<br>
			""")
		self.userDescription.setWordWrap(True)
		self.userDescription.setAlignment(Qt.AlignJustify)

		self.nick = QNoSpaceLineEdit(user.NICKNAME)
		self.alternative = QNoSpaceLineEdit(user.ALTERNATE)
		self.username = QNoSpaceLineEdit(user.USERNAME)
		self.realname = QLineEdit(user.REALNAME)

		self.nick.textChanged.connect(self.changeUser)
		self.alternative.textChanged.connect(self.changeUser)
		self.username.textChanged.connect(self.changeUser)
		self.realname.textChanged.connect(self.changeUser)

		nickl = QLabel("<b>Nickname:</b>")
		altl = QLabel("<b>Alternate:</b>")
		usrl = QLabel("<b>Username:</b>")
		reall = QLabel("<b>Real name:</b>")

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

		userLayout = QVBoxLayout()
		userLayout.addWidget(widgets.textSeparatorLabel(self,"<b>user defaults</b>"))
		userLayout.addWidget(self.userDescription)
		userLayout.addWidget(nickBox)
		userLayout.addWidget(alternateBox)
		userLayout.addWidget(userBox)
		userLayout.addWidget(realnameBox)
		userLayout.addStretch()

		self.userPage.setLayout(userLayout)

		# Menubar page

		self.menuPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Menus")
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

		if not config.USE_MENUBAR:
			self.menubarFloat.setEnabled(False)
			self.menubarJustify.setEnabled(False)
			self.menubarMenu.setEnabled(False)

		justifyLayout = QHBoxLayout()
		justifyLayout.addWidget(QLabel("<b>Menubar alignment</b> "))
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

		menuLayout = QVBoxLayout()
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>menubar settings</b>"))
		menuLayout.addWidget(self.menubarDescription)
		menuLayout.addWidget(self.menubar)
		menuLayout.addWidget(self.menubarFloat)
		menuLayout.addWidget(self.menubarMenu)
		menuLayout.addLayout(justifyLayout)
		menuLayout.addWidget(QLabel(' '))
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>menu display names</b>"))
		menuLayout.addWidget(self.menuNameDescription)
		menuLayout.addLayout(nameMenuEntries)
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
			the subwindow's name. The <b>windowbar</b> can show channel, private chat,
			server, or script editor windows. It can be displayed at the <b>top</b> of
			the main window or at the <b>bottom</b>, or can be optionally <b>movable</b>. The entries
			in the window bar can be <b>left</b>, <b>right</b>, or <b>center</b> justified. The
			<b>windowbar</b> is turned on by default.
			</small>
			""")
		self.windowbarDescription.setWordWrap(True)
		self.windowbarDescription.setAlignment(Qt.AlignJustify)

		self.windowBar = QCheckBox("Enable windowbar",self)
		if config.SHOW_WINDOWBAR: self.windowBar.setChecked(True)
		self.windowBar.stateChanged.connect(self.changedWindowbarSetting)

		self.windowBarTop = QCheckBox("Display at top of window",self)
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

		justifyLayout = QHBoxLayout()
		justifyLayout.addWidget(QLabel("<b>Windowbar alignment</b> "))
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

		self.windowBarUnderline = QCheckBox("Underline active window",self)
		if config.WINDOWBAR_UNDERLINE_ACTIVE_WINDOW: self.windowBarUnderline.setChecked(True)
		self.windowBarUnderline.stateChanged.connect(self.menuChange)

		self.windowBarHover = QCheckBox("Bold entries on mouse hover",self)
		if config.WINDOWBAR_HOVER_EFFECT: self.windowBarHover.setChecked(True)
		self.windowBarHover.stateChanged.connect(self.menuChange)

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

		includesLayout = QFormLayout()
		includesLayout.addRow(self.windowbarChannels,self.windowbarPrivate)
		includesLayout.addRow(self.windowBarServers,self.windowBarEditor)
		includesLayout.addRow(self.windowbarLists)

		windowbarLayout = QVBoxLayout()
		windowbarLayout.addWidget(widgets.textSeparatorLabel(self,"<b>windowbar settings</b>"))
		windowbarLayout.addWidget(self.windowbarDescription)
		windowbarLayout.addWidget(self.windowBar)
		windowbarLayout.addWidget(self.windowBarFloat)
		windowbarLayout.addWidget(self.windowBarTop)
		windowbarLayout.addWidget(self.windowBarFirst)
		windowbarLayout.addWidget(self.windowBarUnderline)
		windowbarLayout.addWidget(self.windowBarHover)
		windowbarLayout.addWidget(self.windowBarIcons)
		windowbarLayout.addWidget(self.windowbarClick)
		windowbarLayout.addWidget(self.windowbarMenu)
		windowbarLayout.addLayout(justifyLayout)
		windowbarLayout.addWidget(QLabel(' '))
		windowbarLayout.addWidget(widgets.textSeparatorLabel(self,"<b>windowbar includes</b>"))
		windowbarLayout.addLayout(includesLayout)
		windowbarLayout.addStretch()

		self.windowbarPage.setLayout(windowbarLayout)

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
		self.showTimestamps.stateChanged.connect(self.changedSettingRerender)

		self.timestamp24hour = QCheckBox("Use 24-hour time for timestamps",self)
		if config.TIMESTAMP_24_HOUR: self.timestamp24hour.setChecked(True)
		self.timestamp24hour.stateChanged.connect(self.changedSettingRerender)

		self.timestampSeconds = QCheckBox("Show seconds in timestamps",self)
		if config.TIMESTAMP_SHOW_SECONDS: self.timestampSeconds.setChecked(True)
		self.timestampSeconds.stateChanged.connect(self.changedSettingRerender)

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

		self.askBeforeReconnect = QCheckBox("Ask before automatically\nreconnecting",self)
		if config.ASK_BEFORE_RECONNECT: self.askBeforeReconnect.setChecked(True)
		self.askBeforeReconnect.stateChanged.connect(self.changedSetting)

		self.askBeforeReconnect.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.notifyOnLostConnection = QCheckBox("Notify on lost/failed connection",self)
		if config.NOTIFY_ON_LOST_OR_FAILED_CONNECTION: self.notifyOnLostConnection.setChecked(True)
		self.notifyOnLostConnection.stateChanged.connect(self.changedSetting)

		self.promptFail = QCheckBox("Prompt for new server on\nconnection failure",self)
		if config.PROMPT_ON_FAILED_CONNECTION: self.promptFail.setChecked(True)
		self.promptFail.stateChanged.connect(self.changedSetting)

		self.promptFail.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.requestList = QCheckBox("Fetch channel list from\nserver on connection",self)
		if config.REQUEST_CHANNEL_LIST_ON_CONNECTION: self.requestList.setChecked(True)
		self.requestList.stateChanged.connect(self.changedSetting)

		self.requestList.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.autoHostmasks = QCheckBox("Fetch hostmasks on channel join",self)
		if config.GET_HOSTMASKS_ON_CHANNEL_JOIN: self.autoHostmasks.setChecked(True)
		self.autoHostmasks.stateChanged.connect(self.changedSetting)

		self.showNetLinks = QCheckBox("Show known links to network\nhomepages",self)
		if config.SHOW_LINKS_TO_NETWORK_WEBPAGES: self.showNetLinks.setChecked(True)
		self.showNetLinks.stateChanged.connect(self.changedSetting)
		self.showNetLinks.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		connectionsLayout = QVBoxLayout()
		connectionsLayout.addWidget(widgets.textSeparatorLabel(self,"<b>connection settings</b>"))
		connectionsLayout.addWidget(self.askBeforeDisconnect)
		connectionsLayout.addWidget(self.askBeforeReconnect)
		connectionsLayout.addWidget(self.notifyOnLostConnection)
		connectionsLayout.addWidget(self.promptFail)
		connectionsLayout.addWidget(self.requestList)
		connectionsLayout.addWidget(self.autoHostmasks)
		connectionsLayout.addWidget(self.showNetLinks)
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

		self.awayMsg = QLineEdit(self.default_away)

		self.awayMsg.textChanged.connect(self.setAwayMsg)

		awayLayout = QVBoxLayout()
		awayLayout.addWidget(self.awayMsg)
		awayBox = QGroupBox("")
		awayBox.setAlignment(Qt.AlignLeft)
		awayBox.setLayout(awayLayout)

		self.promptAway = QCheckBox(f"Prompt for away message if one is\nnot provided with the {config.ISSUE_COMMAND_SYMBOL}away command\nor when pressing the \"Set status to\naway\" button on the server window\ntoolbar",self)
		if config.PROMPT_FOR_AWAY_MESSAGE: self.promptAway.setChecked(True)
		self.promptAway.stateChanged.connect(self.changedSetting)
		self.promptAway.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.autoAway = QCheckBox("Auto-away after",self)
		if config.USE_AUTOAWAY: self.autoAway.setChecked(True)
		self.autoAway.stateChanged.connect(self.changedSetting)

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

		self.showAwayStatus = QCheckBox("Show away status in userlists",self)
		if config.SHOW_AWAY_STATUS_IN_USERLISTS: self.showAwayStatus.setChecked(True)
		self.showAwayStatus.stateChanged.connect(self.changedSettingRerenderUserlists)

		self.showAwayBack = QCheckBox("Show user away and back\nnotification messages",self)
		if config.SHOW_AWAY_AND_BACK_MESSAGES: self.showAwayBack.setChecked(True)
		self.showAwayBack.stateChanged.connect(self.changedSetting)
		self.showAwayBack.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.showAwayNick = QCheckBox("Show away status in nickname\ndisplay",self)
		if config.SHOW_AWAY_STATUS_IN_NICK_DISPLAY: self.showAwayNick.setChecked(True)
		self.showAwayNick.stateChanged.connect(self.changedSettingRerenderNick)
		self.showAwayNick.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")
	
		awayLayout = QVBoxLayout()
		awayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>away settings</b>"))
		awayLayout.addLayout(intervalBox)
		awayLayout.addWidget(self.promptAway)
		awayLayout.addWidget(self.showAwayStatus)
		awayLayout.addWidget(self.showAwayBack)
		awayLayout.addWidget(self.showAwayNick)
		awayLayout.addWidget(QLabel(' '))
		awayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>default away message</b>"))
		awayLayout.addWidget(awayBox)
		awayLayout.addStretch()

		self.awayPage.setLayout(awayLayout)

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

		self.topicBold = QCheckBox("Show channel topic in bold",self)
		if config.CHANNEL_TOPIC_BOLD: self.topicBold.setChecked(True)
		self.topicBold.stateChanged.connect(self.titleChange)

		self.channelName = QCheckBox("Show channel name and modes",self)
		if config.SHOW_CHANNEL_NAME_AND_MODES: self.channelName.setChecked(True)
		self.channelName.stateChanged.connect(self.topicChange)

		self.showBanlist = QCheckBox("Show channel banlist",self)
		if config.SHOW_BANLIST_MENU: self.showBanlist.setChecked(True)
		self.showBanlist.stateChanged.connect(self.topicChange)

		if not config.SHOW_CHANNEL_TOPIC:
			self.topicBold.setEnabled(False)
			self.channelName.setEnabled(False)
			self.showBanlist.setEnabled(False)

		self.channelDescription = QLabel("""
			<small>
			The <b>channel information display</b> is a bar shown at the top of
			every channel window that displays the channel <b>name</b>, any <b>modes</b> set
			on the channel, the channel
			<b>topic</b>, and the channel <b>banlist</b>. The channel <b>topic</b> can be changed
			or edited with it (if you have the right permissions) by clicking
			on the <b>topic</b> and editing it. Here, the
			<b>channel information display</b> can be customized or turned off.
			<br>
			</small>
			""")
		self.channelDescription.setWordWrap(True)
		self.channelDescription.setAlignment(Qt.AlignJustify)

		self.topicTitleDisplay = QCheckBox("Show channel topic in subwindow title",self)
		if config.SHOW_CHANNEL_TOPIC_IN_WINDOW_TITLE: self.topicTitleDisplay.setChecked(True)
		self.topicTitleDisplay.stateChanged.connect(self.titleChange)

		self.showUserlistLeft = QCheckBox("Display user lists on the left\nhand side of channel windows",self)
		if config.SHOW_USERLIST_ON_LEFT: self.showUserlistLeft.setChecked(True)
		self.showUserlistLeft.stateChanged.connect(self.swapUserlistSetting)

		self.showUserlistLeft.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.plainUserLists = QCheckBox("Plain user lists",self)
		if config.PLAIN_USER_LISTS: self.plainUserLists.setChecked(True)
		self.plainUserLists.stateChanged.connect(self.changedSettingRerenderUserlists)

		self.showUserlists = QCheckBox("Show user lists",self)
		if config.SHOW_USERLIST: self.showUserlists.setChecked(True)
		self.showUserlists.stateChanged.connect(self.changedUserlistVisibility)

		self.autoJoin = QCheckBox("Automatically join channel on invite",self)
		if config.JOIN_ON_INVITE: self.autoJoin.setChecked(True)
		self.autoJoin.stateChanged.connect(self.changedSetting)

		self.hideScroll = QCheckBox("Hide horizontal scrollbars on\n all userlists",self)
		if config.HIDE_USERLIST_HORIZONTAL_SCROLLBAR: self.hideScroll.setChecked(True)
		self.hideScroll.stateChanged.connect(self.changedSetting)
		self.hideScroll.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		if not config.SHOW_USERLIST:
			self.plainUserLists.setEnabled(False)
			self.showUserlistLeft.setEnabled(False)
			self.hideScroll.setEnabled(False)

		menuLayout = QVBoxLayout()
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>channel information display</b>"))
		menuLayout.addWidget(self.channelDescription)
		menuLayout.addWidget(self.topicDisplay)
		menuLayout.addWidget(self.topicBold)
		menuLayout.addWidget(self.channelName)
		menuLayout.addWidget(self.showBanlist)
		menuLayout.addWidget(QLabel(' '))
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>user lists</b>"))
		menuLayout.addWidget(self.showUserlists)
		menuLayout.addWidget(self.plainUserLists)
		menuLayout.addWidget(self.showUserlistLeft)
		menuLayout.addWidget(self.hideScroll)
		menuLayout.addWidget(QLabel(' '))
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous</b>"))
		menuLayout.addWidget(self.topicTitleDisplay)
		menuLayout.addWidget(self.autoJoin)
		menuLayout.addStretch()

		self.channelInfoPage.setLayout(menuLayout)

		# Input page

		self.inputPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Input")
		entry.widget = self.inputPage
		entry.setIcon(QIcon(INPUT_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.inputPage)

		self.enableEmojis = QCheckBox("Enable emoji shortcodes",self)
		if config.ENABLE_EMOJI_SHORTCODES: self.enableEmojis.setChecked(True)
		self.enableEmojis.stateChanged.connect(self.changedEmoji)

		self.historyLabel = QLabel(f"<b>{str(self.historysize)} lines</b>",self)

		historyButton = QPushButton("")
		historyButton.clicked.connect(self.setHistorySize)
		historyButton.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		historyButton.setFixedSize(fheight +10,fheight + 10)
		historyButton.setIcon(QIcon(EDIT_ICON))
		historyButton.setToolTip("Change command history size")

		historyLayout = QHBoxLayout()
		historyLayout.addWidget(historyButton)
		historyLayout.addWidget(self.historyLabel)
		historyLayout.addStretch()

		self.historyDescription = QLabel("""
			<small>
			Any text typed into the text input widget is saved to the <b>command history</b>.
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
			<b>nickname</b>, <b>channel</b>, <b>alias</b>, or <b>emoji shortcode</b>, and then hit <b>tab</b> to complete
			the entry.
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

		self.interpolateAlias = QCheckBox("Interpolate aliases into input",self)
		if config.INTERPOLATE_ALIASES_INTO_INPUT: self.interpolateAlias.setChecked(True)
		self.interpolateAlias.stateChanged.connect(self.changedInterpolate)

		if not config.INTERPOLATE_ALIASES_INTO_INPUT: self.autocompleteAlias.setEnabled(False)

		autoLayout1 = QHBoxLayout()
		autoLayout1.addWidget(self.autocompleteCommands)
		autoLayout1.addWidget(self.autocompleteNicks)

		autoLayout2 = QHBoxLayout()
		autoLayout2.addWidget(self.autocompleteChans)
		autoLayout2.addWidget(self.autocompleteEmojis)

		self.emojiDescription = QLabel("""
			<small>
			If <b>emoji shortcodes</b> are enabled, you can insert <b>emojis</b> into
			your chat by using <a href="https://emojibase.dev/docs/shortcodes/"><b>shortcodes</b></a>.
			You can find a complete list of supported <b>shortcodes</b> <a href="https://carpedm20.github.io/emoji/all.html?enableList=enable_list_alias">
			here</a>.
			</small>
			<br>
			""")
		self.emojiDescription.setWordWrap(True)
		self.emojiDescription.setAlignment(Qt.AlignJustify)
		self.emojiDescription.setOpenExternalLinks(True)

		inputLayout = QVBoxLayout()
		inputLayout.addWidget(widgets.textSeparatorLabel(self,"<b>emoji shortcodes</b>"))
		inputLayout.addWidget(self.emojiDescription)
		inputLayout.addWidget(self.enableEmojis)
		inputLayout.addWidget(QLabel(' '))
		inputLayout.addWidget(widgets.textSeparatorLabel(self,"<b>command history size</b>"))
		inputLayout.addWidget(self.historyDescription)
		inputLayout.addLayout(historyLayout)
		inputLayout.addWidget(QLabel(' '))
		inputLayout.addWidget(widgets.textSeparatorLabel(self,"<b>autocomplete</b>"))
		inputLayout.addWidget(self.autocompleteDescription)
		inputLayout.addLayout(autoLayout1)
		inputLayout.addLayout(autoLayout2)
		inputLayout.addWidget(self.autocompleteAlias)
		inputLayout.addWidget(QLabel(' '))
		inputLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous</b>"))
		inputLayout.addWidget(self.interpolateAlias)
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

		if config.DEFAULT_SPELLCHECK_LANGUAGE=="en": self.englishSC.setChecked(True)
		if config.DEFAULT_SPELLCHECK_LANGUAGE=="fr": self.frenchSC.setChecked(True)
		if config.DEFAULT_SPELLCHECK_LANGUAGE=="es": self.spanishSC.setChecked(True)
		if config.DEFAULT_SPELLCHECK_LANGUAGE=="de": self.germanSC.setChecked(True)

		if not config.ENABLE_SPELLCHECK:
			self.englishSC.setEnabled(False)
			self.frenchSC.setEnabled(False)
			self.spanishSC.setEnabled(False)
			self.germanSC.setEnabled(False)

		langLayout = QFormLayout()
		langLayout.addRow(self.englishSC, self.frenchSC)
		langLayout.addRow(self.spanishSC, self.germanSC)

		lanSubLayout = QHBoxLayout()
		lanSubLayout.addStretch()
		lanSubLayout.addLayout(langLayout)
		lanSubLayout.addStretch()

		self.spellcheckDescription = QLabel("""
			<small>
			Misspelled words in the input widget are marked with a <b><span style='text-decoration: underline; color: red;'>red
			underline</span></b>. <b>Right click</b> on a <b>marked word</b> to get <b>suggestions to replace
			the word with</b> or to <b>add that word to the built-in dictionary</b>.
			</small>
			<br>
			""")
		self.spellcheckDescription.setWordWrap(True)
		self.spellcheckDescription.setAlignment(Qt.AlignJustify)

		spellcheckLayout = QVBoxLayout()
		spellcheckLayout.addWidget(widgets.textSeparatorLabel(self,"<b>spellcheck</b>"))
		spellcheckLayout.addWidget(self.spellcheckDescription)
		spellcheckLayout.addWidget(self.enableSpellcheck)
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

		self.saveChanLogs = QCheckBox("Save channel logs",self)
		if config.SAVE_CHANNEL_LOGS: self.saveChanLogs.setChecked(True)
		self.saveChanLogs.stateChanged.connect(self.changedSetting)

		self.loadChanLogs = QCheckBox("Load channel logs",self)
		if config.LOAD_CHANNEL_LOGS: self.loadChanLogs.setChecked(True)
		self.loadChanLogs.stateChanged.connect(self.changedSetting)

		self.savePrivLogs = QCheckBox("Save private chat logs",self)
		if config.SAVE_PRIVATE_LOGS: self.savePrivLogs.setChecked(True)
		self.savePrivLogs.stateChanged.connect(self.changedSetting)

		self.loadPrivLogs = QCheckBox("Load private chat logs",self)
		if config.LOAD_PRIVATE_LOGS: self.loadPrivLogs.setChecked(True)
		self.loadPrivLogs.stateChanged.connect(self.changedSetting)

		self.markLog = QCheckBox("Mark end of loaded log",self)
		if config.MARK_END_OF_LOADED_LOG: self.markLog.setChecked(True)
		self.markLog.stateChanged.connect(self.changedSetting)
		
		self.logLabel = QLabel(f"<b>{str(self.logsize)} lines</b>",self)

		logsizeButton = QPushButton("")
		logsizeButton.clicked.connect(self.setLogSize)
		logsizeButton.setAutoDefault(False)

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
		logsizeButton.setFixedSize(fheight +10,fheight + 10)
		logsizeButton.setIcon(QIcon(EDIT_ICON))
		logsizeButton.setToolTip("Change log load size")

		logsizeLayout = QHBoxLayout()
		logsizeLayout.addWidget(logsizeButton)
		logsizeLayout.addWidget(self.logLabel)
		logsizeLayout.addStretch()

		self.logFullDescription = QLabel(f"""
			<small>
			<b>Logs</b> are saved in JavaScript Object Notation (<b>JSON</B>), and use a format that can
			be read and displayed easily by <b>{APPLICATION_NAME}</b>. If you want to use other
			software to read or parse your IRC <b>logs</b>, a <b>log</b> export tool is built into
			<b>{APPLICATION_NAME}</b>. The tool is located in the "<b>{self.default_tools_menu}</b>"
			menu, under "<b>Export Logs</b>". Your <b>logs</b> can be exported in <b>JSON</b>, <b>CSV</b>, or your
			own custom <b>ASCII, character delimited format</b>.
			</small>
			<br>
			""")
		self.logFullDescription.setWordWrap(True)
		self.logFullDescription.setAlignment(Qt.AlignJustify)

		logLayout = QVBoxLayout()
		logLayout.addWidget(widgets.textSeparatorLabel(self,"<b>log settings</b>"))
		logLayout.addWidget(self.logFullDescription)
		logLayout.addWidget(self.saveChanLogs)
		logLayout.addWidget(self.loadChanLogs)
		logLayout.addWidget(self.savePrivLogs)
		logLayout.addWidget(self.loadPrivLogs)
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

		self.createWindow = QCheckBox("Create windows for private chat",self)
		if config.CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES: self.createWindow.setChecked(True)
		self.createWindow.stateChanged.connect(self.changedSetting)

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

		self.forceMono = QCheckBox("Force monospace rendering\nof all message text",self)
		if config.FORCE_MONOSPACE_RENDERING: self.forceMono.setChecked(True)
		self.forceMono.stateChanged.connect(self.changedSettingRerender)

		self.forceMono.setStyleSheet("QCheckBox { text-align: left top; } QCheckBox::indicator { subcontrol-origin: padding; subcontrol-position: left top; }")

		self.partMsg = QLineEdit(self.default_quit_part)

		self.partMsg.textChanged.connect(self.setQuitMsg)

		partLayout = QVBoxLayout()
		partLayout.addWidget(self.partMsg)
		partBox = QGroupBox("")
		partBox.setAlignment(Qt.AlignLeft)
		partBox.setLayout(partLayout)

		messageLayout = QVBoxLayout()
		messageLayout.addWidget(widgets.textSeparatorLabel(self,"<b>message settings</b>"))
		messageLayout.addWidget(self.showColors)
		messageLayout.addWidget(self.showLinks)
		messageLayout.addWidget(self.createWindow)
		messageLayout.addWidget(self.writePrivate)
		messageLayout.addWidget(self.writeScroll)
		messageLayout.addWidget(self.forceMono)
		messageLayout.addWidget(QLabel(' '))
		messageLayout.addWidget(widgets.textSeparatorLabel(self,"<b>system messages</b>"))
		messageLayout.addLayout(prepLayout)
		messageLayout.addWidget(QLabel(' '))
		messageLayout.addWidget(widgets.textSeparatorLabel(self,"<b>default quit/part message</b>"))
		messageLayout.addWidget(partBox)
		messageLayout.addStretch()

		self.messagePage.setLayout(messageLayout)

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

		systrayLayout = QVBoxLayout()
		systrayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>system tray settings</b>"))
		systrayLayout.addWidget(self.showSystray)
		systrayLayout.addWidget(self.showSystrayMenu)
		systrayLayout.addWidget(self.minSystray)
		systrayLayout.addWidget(self.systrayNotify)
		systrayLayout.addWidget(self.listSystray)
		systrayLayout.addWidget(self.systrayMinOnClose)
		systrayLayout.addWidget(QLabel(' '))
		systrayLayout.addWidget(widgets.textSeparatorLabel(self,"<b>notifications</b>"))
		systrayLayout.addLayout(nickPriv)
		systrayLayout.addLayout(kickInvite)
		systrayLayout.addLayout(noticeMode)
		systrayLayout.addLayout(discLay)
		systrayLayout.addStretch()

		self.systrayPage.setLayout(systrayLayout)

		if self.showSystray.isChecked():
			self.showSystrayMenu.setEnabled(True)
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

		# Syntax

		self.syntaxPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Highlighting")
		entry.widget = self.syntaxPage
		entry.setIcon(QIcon(SCRIPT_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.syntaxPage)

		self.syntaxcomment = widgets.SyntaxColor('comment', "<b>Comments</b>",self.SYNTAX_COMMENT_COLOR,self.SYNTAX_COMMENT_STYLE,self)
		self.syntaxcommand = widgets.SyntaxColor('command', "<b>Commands</b>",self.SYNTAX_COMMAND_COLOR,self.SYNTAX_COMMAND_STYLE,self)
		self.syntaxchannel = widgets.SyntaxColor('channel', "<b>Channels</b>",self.SYNTAX_CHANNEL_COLOR,self.SYNTAX_CHANNEL_STYLE,self)
		self.syntaxalias = widgets.SyntaxColor('alias', "<b>Aliases</b>",self.SYNTAX_ALIAS_COLOR,self.SYNTAX_ALIAS_STYLE,self)

		self.syntaxfore = widgets.SyntaxTextColor('fore', "<b>Text Color</b>",self.SYNTAX_FOREGROUND,self)
		self.syntaxback = widgets.SyntaxTextColor('back', "<b>Background</b>",self.SYNTAX_BACKGROUND,self)

		self.syntaxcomment.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxcommand.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxchannel.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxalias.syntaxChanged.connect(self.syntaxChanged)

		self.syntaxnick = widgets.SyntaxColor('nick', "<b>Nicknames</b>",self.SYNTAX_NICKNAME_COLOR,self.SYNTAX_NICKNAME_STYLE,self)
		self.syntaxemoji = widgets.SyntaxColor('emoji', "<b>Emoji Shortcodes</b>",self.SYNTAX_EMOJI_COLOR,self.SYNTAX_EMOJI_STYLE,self)

		self.syntaxnick.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxemoji.syntaxChanged.connect(self.syntaxChanged)

		self.syntaxfore.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxback.syntaxChanged.connect(self.syntaxChanged)

		self.syntaxDescription = QLabel("""
			<small>
			<b>Syntax highlighting</b> is applied to both the script section of the
			connection dialog, and the built-in script editor. <b>Commands</b>,
			<b>channels</b>, <b>comments</b>, and <b>aliases</b> appear in the colors and styles set below.
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
			colors and format settings below. Text color and background
			color will be set to the current window's text style.
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

		sbLay = QFormLayout()
		sbLay.addRow(self.syntaxnick, self.syntaxemoji)

		syntaxLayout = QVBoxLayout()
		syntaxLayout.addWidget(widgets.textSeparatorLabel(self,"<b>syntax highlighting</b>"))
		syntaxLayout.addWidget(self.syntaxDescription)
		syntaxLayout.addLayout(tbLay)
		syntaxLayout.addWidget(widgets.textSeparatorLabel(self,"<b>input highlighting</b>"))
		syntaxLayout.addWidget(self.syntaxInput)
		syntaxLayout.addWidget(self.toggleSyntaxInput)
		syntaxLayout.addLayout(sbLay)
		syntaxLayout.addStretch()

		self.syntaxPage.setLayout(syntaxLayout)

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

		if not self.audioNotifications.isChecked():
			self.notifyDisco.setEnabled(False)
			self.notifyNickname.setEnabled(False)
			self.notifyPrivate.setEnabled(False)
			self.notifyNotice.setEnabled(False)
			self.notifyKick.setEnabled(False)
			self.notifyInvite.setEnabled(False)
			self.notifyMode.setEnabled(False)
		
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

		soundButton = QPushButton("")
		soundButton.clicked.connect(self.setSound)
		soundButton.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		soundButton.setFixedSize(fheight +10,fheight + 10)
		soundButton.setIcon(QIcon(EDIT_ICON))
		soundButton.setToolTip("Set notification sound file")

		playButton = QPushButton(" Play")
		playButton.clicked.connect(self.playSound)
		playButton.setAutoDefault(False)
		playButton.setIcon(QIcon(RUN_ICON))
		playButton.setToolTip("Play sound")

		soundDefault = QPushButton("Set to default")
		soundDefault.clicked.connect(self.soundDefault)
		soundDefault.setAutoDefault(False)
		soundDefault.setToolTip("Set to default")

		sbLayout = QHBoxLayout()
		sbLayout.addStretch()
		sbLayout.addWidget(soundButton)
		sbLayout.addWidget(self.soundLabel)
		sbLayout.addStretch()

		sbLayout2 = QHBoxLayout()
		sbLayout2.addStretch()
		sbLayout2.addWidget(playButton)
		sbLayout2.addWidget(soundDefault)
		sbLayout2.addStretch()


		audioLayout = QVBoxLayout()
		audioLayout.addWidget(widgets.textSeparatorLabel(self,"<b>audio notifications</b>"))
		audioLayout.addWidget(self.notifyDescription)
		audioLayout.addWidget(self.audioNotifications)
		audioLayout.addWidget(QLabel(' '))
		audioLayout.addWidget(widgets.textSeparatorLabel(self,"<b>events</b>"))
		audioLayout.addLayout(anickPriv)
		audioLayout.addLayout(akickInvite)
		audioLayout.addLayout(anoticeMode)
		audioLayout.addLayout(adiscLay)
		audioLayout.addWidget(QLabel(' '))
		audioLayout.addWidget(widgets.textSeparatorLabel(self,"<b>sound file</b>"))
		audioLayout.addLayout(sbLayout)
		audioLayout.addLayout(sbLayout2)
		audioLayout.addStretch()

		self.notificationsPage.setLayout(audioLayout)

		self.changed.hide()
		self.restart.hide()

		# Buttons

		self.saveButton = QPushButton("Apply")
		self.saveButton.clicked.connect(self.save)
		self.saveButton.setAutoDefault(False)

		self.cancelButton = QPushButton("Cancel")
		self.cancelButton.clicked.connect(self.close)

		# Finalize layout

		logo = QLabel()
		pixmap = QPixmap(APPLICATION_ICON)
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

		dialogButtonsLayout = QHBoxLayout()
		dialogButtonsLayout.addStretch()
		dialogButtonsLayout.addWidget(self.changed)
		dialogButtonsLayout.addWidget(self.restart)
		dialogButtonsLayout.addStretch()
		dialogButtonsLayout.addWidget(self.saveButton)
		dialogButtonsLayout.addWidget(self.cancelButton)

		leftLayout = QVBoxLayout()
		leftLayout.addWidget(self.selector)
		leftLayout.addWidget(logo)

		mainLayout = QHBoxLayout()
		mainLayout.addLayout(leftLayout)
		mainLayout.addWidget(self.stack)

		self.finalLayout = QVBoxLayout()
		self.finalLayout.addLayout(mainLayout)
		self.finalLayout.addLayout(dialogButtonsLayout)

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
		config.MINIMIZE_TO_SYSTRAY = self.minSystray.isChecked()
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
		config.DEFAULT_AWAY_MESSAGE = self.default_away
		config.PROMPT_FOR_AWAY_MESSAGE = self.promptAway.isChecked()

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
			user.save_user(user.USER_FILE)

		if config.TIMESTAMP_24_HOUR:
			ts = '%H:%M'
		else:
			ts = '%I:%M'
		if config.TIMESTAMP_SHOW_SECONDS: ts = ts + ':%S'

		config.TIMESTAMP_FORMAT = ts

		# Save new settings to the config file
		config.save_settings(config.CONFIG_FILE)

		self.parent.buildSettingsMenu()
		self.parent.buildWindowsMenu()

		self.parent.app.setStyle(self.qt_style)

		self.parent.setAllLanguage(config.DEFAULT_SPELLCHECK_LANGUAGE)
		if self.rerender: self.parent.reRenderAll()
		if self.rerenderUsers: self.parent.rerenderUserlists()
		if self.rerenderStyle: self.parent.reApplyStyle()

		if self.rerenderNick:
			self.parent.rerenderAllNickDisplays()
			self.parent.toggleNickDisplay()
			if not self.rerenderUsers: self.parent.rerenderUserlists()

		if self.newfont!=None:
			config.APPLICATION_FONT = self.newfont.toString()
			self.parent.app.setFont(self.newfont)
			self.parent.setAllFont(self.newfont)

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

		self.parent.refreshAllTopic()
		if config.SHOW_CHANNEL_TOPIC:
			self.parent.showAllTopic()
		else:
			self.parent.hideAllTopic()

		if self.swapUserlists: self.parent.swapAllUserlists()

		if self.toggleUserlist: self.parent.toggleAllUserlists()

		self.parent.toggleSpellcheck()

		self.parent.toggleInputMenu()

		self.parent.toggleServNickDisplay()

		self.parent.toggleRefreshButton()

		self.parent.updateStatusBar()

		self.parent.toggleServerToolbar()

		self.parent.toggleScrollbar()

		# Set the application font
		self.parent.app.setFont(self.parent.application_font)

		# Set the widget font
		self.parent.setFont(self.parent.application_font)

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