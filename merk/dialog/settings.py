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
from .. import config
from .. import dialog
from .. import widgets

class Dialog(QDialog):

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
		self.selector.setFocus()

	def setWinsize(self):
		
		x = dialog.SizeDialog(self)
		if x:
			self.subWidth = x[0]
			self.subHeight = x[1]
			self.sizeLabel.setText(f"<b>{str(self.subWidth)}x{str(self.subHeight)} px</b>")
			self.changed.show()
		self.selector.setFocus()

	def setLogSize(self):

		x = dialog.LogSizeDialog(self)
		if x:
			self.logsize = x
			self.logLabel.setText(f"<b>{str(self.logsize)} lines</b>")
			self.changed.show()
		self.selector.setFocus()

	def setHistorySize(self):

		x = dialog.HistorySizeDialog(self)
		if x:
			self.historysize = x
			self.historyLabel.setText(f"<b>{str(self.historysize)} lines</b>")
			self.changed.show()
		self.selector.setFocus()

	def selEnglish(self):
		self.spellLang = "en"
		self.changed.show()
		self.selector.setFocus()

	def selFrench(self):
		self.spellLang = "fr"
		self.changed.show()
		self.selector.setFocus()

	def selGerman(self):
		self.spellLang = "de"
		self.changed.show()
		self.selector.setFocus()

	def selSpanish(self):
		self.spellLang = "es"
		self.changed.show()
		self.selector.setFocus()

	def changedSetting(self,state):
		self.changed.show()
		self.selector.setFocus()

	def swapUserlistSetting(self,state):
		self.changed.show()
		self.swapUserlists = True
		self.selector.setFocus()

	def changedSettingRerender(self,state):
		self.changed.show()
		self.rerender = True
		self.selector.setFocus()

	def changedSettingRerenderUserlists(self,state):
		self.changed.show()
		self.rerenderUsers = True
		self.selector.setFocus()

	def changedSettingRerenderNick(self,state):
		self.changed.show()
		self.rerenderNick = True
		self.selector.setFocus()

	def setQuitMsg(self):
		info = dialog.QuitPartDialog(self.default_quit_part,self)

		if not info: return None

		self.default_quit_part = info
		self.partMsg.setText("<b>"+str(info)+"</b>")

		self.changed.show()
		self.selector.setFocus()

	def syntaxChanged(self,data):
		name = data[0]
		
		if name=="comment":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_COMMENT_COLOR = color
			self.SYNTAX_COMMENT_STYLE = style
			self.changed.show()
		elif name=="command":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_COMMAND_COLOR = color
			self.SYNTAX_COMMAND_STYLE = style
			self.changed.show()
		elif name=="channel":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_CHANNEL_COLOR = color
			self.SYNTAX_CHANNEL_STYLE = style
			self.changed.show()
		elif name=="alias":
			color = data[1][0]
			style = data[1][1]
			self.SYNTAX_ALIAS_COLOR = color
			self.SYNTAX_ALIAS_STYLE = style
			self.changed.show()
		elif name=="fore":
			color = data[1]
			self.SYNTAX_FOREGROUND = color
			self.changed.show()
		elif name=="back":
			color = data[1]
			self.SYNTAX_BACKGROUND = color
			self.changed.show()
		
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
		self.selector.setFocus()
		self.changed.show()

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

	def changedMenubarSetting(self,state):
		if self.menubar.isChecked():
			self.menubarFloat.setEnabled(True)
		else:
			self.menubarFloat.setEnabled(False)
		self.selector.setFocus()
		self.changed.show()

	def changedEmoji(self,state):
		if self.enableEmojis.isChecked():
			self.autocompleteEmojis.setEnabled(True)
		else:
			self.autocompleteEmojis.setEnabled(False)
		self.selector.setFocus()
		self.changed.show()

	def styleChange(self, i):
		self.qt_style = self.qtStyle.itemText(i)

		self.selector.setFocus()
		self.changed.show()

	def topicChange(self, i):
		self.refreshTopics = True

		self.selector.setFocus()
		self.changed.show()

	def titleChange(self, i):
		self.refreshTitles = True

		self.selector.setFocus()
		self.changed.show()

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


	def __init__(self,app=None,parent=None):
		super(Dialog,self).__init__(parent)

		self.app = app
		self.parent = parent

		self.setFont(self.parent.application_font)

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

		self.qt_style = config.QT_WINDOW_STYLE

		self.refreshTopics = False
		self.refreshTitles = False
		self.swapUserlists = False

		self.setWindowTitle("Settings")
		self.setWindowIcon(QIcon(SETTINGS_ICON))

		self.selector = QListWidget(self)
		self.stack = QStackedWidget(self)

		f = self.selector.font()
		f.setBold(True)
		self.selector.setFont(f)

		self.changed = QLabel("<i>Settings changed.</i>")

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
		entry.setIcon(QIcon(APPLICATION_ICON))
		self.selector.addItem(entry)
		self.selector.setCurrentItem(entry)

		self.stack.addWidget(self.applicationPage)
		self.stack.setCurrentWidget(self.applicationPage)

		logo = QLabel()
		pixmap = QPixmap(SPLASH_LOGO)
		logo.setPixmap(pixmap)
		logo.setAlignment(Qt.AlignCenter)

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
		fontLayout.addStretch()

		self.sizeLabel = QLabel(f"<b>{str(config.DEFAULT_SUBWINDOW_WIDTH)}x{str(config.DEFAULT_SUBWINDOW_HEIGHT)} px</b>",self)

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
		sizeLayout.addStretch()

		self.showChatInTitle = QCheckBox("Show active chat in window title",self)
		if config.DISPLAY_ACTIVE_CHAT_IN_TITLE: self.showChatInTitle.setChecked(True)
		self.showChatInTitle.stateChanged.connect(self.changedSetting)

		self.showSystray = QCheckBox("Show system tray icon",self)
		if config.SHOW_SYSTRAY_ICON: self.showSystray.setChecked(True)
		self.showSystray.stateChanged.connect(self.changedSystrayMin)

		versionLabel = QLabel('<b>Version '+APPLICATION_VERSION+"</b>")
		versionLayout = QHBoxLayout()
		versionLayout.addStretch()
		versionLayout.addWidget(versionLabel)
		versionLayout.addStretch()

		self.showInfo = QCheckBox("Show user info on all chat windows",self)
		if config.SHOW_USER_INFO_ON_CHAT_WINDOWS: self.showInfo.setChecked(True)
		self.showInfo.stateChanged.connect(self.changedSettingRerenderNick)

		applicationLayout = QVBoxLayout()
		applicationLayout.addWidget(logo)
		applicationLayout.addLayout(versionLayout)
		applicationLayout.addWidget(QLabel(' '))
		applicationLayout.addWidget(widgets.textSeparatorLabel(self,"<b>application settings</b>"))
		applicationLayout.addWidget(self.showChatInTitle)
		applicationLayout.addWidget(self.showSystray)
		applicationLayout.addWidget(self.showInfo)
		applicationLayout.addWidget(widgets.textSeparatorLabel(self,"<b>default font</b>"))
		applicationLayout.addLayout(fontLayout)
		applicationLayout.addWidget(widgets.textSeparatorLabel(self,"<b>initial window size</b>"))
		applicationLayout.addLayout(sizeLayout)
		applicationLayout.addStretch()

		self.applicationPage.setLayout(applicationLayout)

		# Widget page

		self.appearancePage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Widgets")
		entry.widget = self.appearancePage
		entry.setIcon(QIcon(WIDGET_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.appearancePage)

		self.styleDescription = QLabel("""
			<small>
			This setting controls how subwindows and widgets look. Different styles
			use different sets of widgets. Qt comes with a number of them
			pre-installed, and you can select which one to use here. The selected
			widget style will be applied immediately without having
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

		appearanceLayout = QVBoxLayout()
		appearanceLayout.addWidget(widgets.textSeparatorLabel(self,"<b>widget style</b>"))
		appearanceLayout.addWidget(self.styleDescription)
		appearanceLayout.addLayout(styleLayout)
		appearanceLayout.addStretch()

		self.appearancePage.setLayout(appearanceLayout)

		# Menubar page

		self.menuPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Menubar")
		entry.widget = self.menuPage
		entry.setIcon(QIcon(MENU_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.menuPage)

		self.menubarDescription = QLabel("""
			<small>
			The menubar is a widget that takes the place of the menus of a
			"normal" application. The menubar can be moved to either the top
			of the main window, the bottom of the main window, or can optionally
			float above all the subwindows. The menubar is turned on by default,
			but can be turned off if normal application menus are desired.
			</small>
			<br>
			""")
		self.menubarDescription.setWordWrap(True)
		self.menubarDescription.setAlignment(Qt.AlignJustify)

		self.menubar = QCheckBox("Use menubar",self)
		if config.USE_MENUBAR: self.menubar.setChecked(True)
		self.menubar.stateChanged.connect(self.changedMenubarSetting)

		self.menubarFloat = QCheckBox("Menubar can \"float\"",self)
		if config.MENUBAR_CAN_FLOAT: self.menubarFloat.setChecked(True)
		self.menubarFloat.stateChanged.connect(self.changedSetting)

		if not config.USE_MENUBAR: self.menubarFloat.setEnabled(False)

		menuLayout = QVBoxLayout()
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>menubar settings</b>"))
		menuLayout.addWidget(self.menubarDescription)
		menuLayout.addWidget(self.menubar)
		menuLayout.addWidget(self.menubarFloat)
		menuLayout.addStretch()

		self.menuPage.setLayout(menuLayout)

		# Connection page

		self.connectionsPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Connection")
		entry.widget = self.connectionsPage
		entry.setIcon(QIcon(CONNECT_ICON))
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

		self.partMsg = QLabel("<b>"+str(config.DEFAULT_QUIT_MESSAGE)+"</b>")

		self.setPartMsg = QPushButton("")
		self.setPartMsg.clicked.connect(self.setQuitMsg)
		self.setPartMsg.setAutoDefault(False)

		fm = QFontMetrics(self.font())
		fheight = fm.height()
		self.setPartMsg.setFixedSize(fheight +10,fheight + 10)
		self.setPartMsg.setIcon(QIcon(EDIT_ICON))
		self.setPartMsg.setToolTip("Set quit/part message")

		cgbLayout = QHBoxLayout()
		cgbLayout.addWidget(self.setPartMsg)
		cgbLayout.addWidget(self.partMsg)
		cgbLayout.addStretch()

		self.quitpartDescription = QLabel("""
			<small>
			This is the default message used for channel parts or
			server quits if a message is not provided.
			</small>
			<br>
			""")
		self.quitpartDescription.setWordWrap(True)
		self.quitpartDescription.setAlignment(Qt.AlignJustify)

		connectionsLayout = QVBoxLayout()
		connectionsLayout.addWidget(widgets.textSeparatorLabel(self,"<b>connection settings</b>"))
		connectionsLayout.addWidget(self.askBeforeDisconnect)
		connectionsLayout.addWidget(self.askBeforeReconnect)
		connectionsLayout.addWidget(self.notifyOnLostConnection)
		connectionsLayout.addWidget(self.promptFail)
		connectionsLayout.addWidget(widgets.textSeparatorLabel(self,"<b>default quit/part message</b>"))
		connectionsLayout.addWidget(self.quitpartDescription)
		connectionsLayout.addLayout(cgbLayout)
		connectionsLayout.addStretch()

		self.connectionsPage.setLayout(connectionsLayout)

		# Channel info page

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
			The channel information display is a bar shown at the top of
			every channel window that displays the channel name, any modes set
			on the channel, the channel
			topic, and the channel banlist. The channel topic can be changed
			or edited with it (if you have the right permissions) by clicking
			on the topic and editing it. Here, the
			channel information display can be customized or turned off.
			</small>
			<br>
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

		menuLayout = QVBoxLayout()
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>channel information display</b>"))
		menuLayout.addWidget(self.channelDescription)
		menuLayout.addWidget(self.topicDisplay)
		menuLayout.addWidget(self.topicBold)
		menuLayout.addWidget(self.channelName)
		menuLayout.addWidget(self.showBanlist)
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>user lists</b>"))
		menuLayout.addWidget(self.plainUserLists)
		menuLayout.addWidget(self.showUserlistLeft)
		menuLayout.addWidget(widgets.textSeparatorLabel(self,"<b>miscellaneous</b>"))
		menuLayout.addWidget(self.topicTitleDisplay)
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

		self.historyLabel = QLabel(f"<b>{str(config.COMMAND_HISTORY_LENGTH)} lines</b>",self)

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
			Any text typed into the text input box is saved to the command history.
			Use the up and down arrow keys to move backwards and forwards in the 
			command history to issue any previously issued commands.
			</small>
			<br>
			""")
		self.historyDescription.setWordWrap(True)
		self.historyDescription.setAlignment(Qt.AlignJustify)

		inputLayout = QVBoxLayout()
		inputLayout.addWidget(widgets.textSeparatorLabel(self,"<b>text input settings</b>"))
		inputLayout.addWidget(self.enableEmojis)
		inputLayout.addWidget(widgets.textSeparatorLabel(self,"<b>command history size</b>"))
		inputLayout.addWidget(self.historyDescription)
		inputLayout.addLayout(historyLayout)
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
		self.enableSpellcheck.stateChanged.connect(self.changedSetting)

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

		langLayout = QFormLayout()
		langLayout.addRow(self.englishSC, self.frenchSC)
		langLayout.addRow(self.spanishSC, self.germanSC)

		lanSubLayout = QHBoxLayout()
		lanSubLayout.addStretch()
		lanSubLayout.addLayout(langLayout)
		lanSubLayout.addStretch()

		self.spellcheckDescription = QLabel("""
			<small>
			Misspelled words in the input box are marked with a red
			underline. Right click on a marked word to get suggestions to replace
			the word with or to add that word to the built-in dictionary.
			</small>
			<br>
			""")
		self.spellcheckDescription.setWordWrap(True)
		self.spellcheckDescription.setAlignment(Qt.AlignJustify)

		spellcheckLayout = QVBoxLayout()
		spellcheckLayout.addWidget(widgets.textSeparatorLabel(self,"<b>spellcheck</b>"))
		spellcheckLayout.addWidget(self.enableSpellcheck)
		spellcheckLayout.addWidget(self.spellcheckDescription)
		spellcheckLayout.addWidget(widgets.textSeparatorLabel(self,"<b>default spellcheck language</b>"))
		spellcheckLayout.addLayout(lanSubLayout)
		spellcheckLayout.addStretch()

		self.spellcheckPage.setLayout(spellcheckLayout)

		# Autocomplete page

		self.autocompletePage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Autocomplete")
		entry.widget = self.autocompletePage
		entry.setIcon(QIcon(AUTOCOMPLETE_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.autocompletePage)

		self.autocompleteDescription = QLabel("""
			<small>
			To use autocomplete, type the first few characters of a command,
			nickname, channel, or emoji shortcode, and then hit tab to complete
			the entry.
			</small>
			<br>
			""")
		self.autocompleteDescription.setWordWrap(True)
		self.autocompleteDescription.setAlignment(Qt.AlignJustify)

		self.autocompleteCommands = QCheckBox("Autocomplete commands",self)
		if config.AUTOCOMPLETE_COMMANDS: self.autocompleteCommands.setChecked(True)
		self.autocompleteCommands.stateChanged.connect(self.changedSetting)

		self.autocompleteNicks = QCheckBox("Autocomplete nicknames",self)
		if config.AUTOCOMPLETE_NICKS: self.autocompleteNicks.setChecked(True)
		self.autocompleteNicks.stateChanged.connect(self.changedSetting)

		self.autocompleteChans = QCheckBox("Autocomplete channels",self)
		if config.AUTOCOMPLETE_CHANNELS: self.autocompleteChans.setChecked(True)
		self.autocompleteChans.stateChanged.connect(self.changedSetting)

		self.autocompleteEmojis = QCheckBox("Autocomplete emoji shortcodes",self)
		if config.AUTOCOMPLETE_EMOJIS: self.autocompleteEmojis.setChecked(True)
		self.autocompleteEmojis.stateChanged.connect(self.changedSetting)

		if config.ENABLE_EMOJI_SHORTCODES:
			self.autocompleteEmojis.setEnabled(True)
		else:
			self.autocompleteEmojis.setEnabled(False)

		autocompleteLayout = QVBoxLayout()
		autocompleteLayout.addWidget(widgets.textSeparatorLabel(self,"<b>autocomplete settings</b>"))
		autocompleteLayout.addWidget(self.autocompleteDescription)
		autocompleteLayout.addWidget(self.autocompleteCommands)
		autocompleteLayout.addWidget(self.autocompleteNicks)
		autocompleteLayout.addWidget(self.autocompleteChans)
		autocompleteLayout.addWidget(self.autocompleteEmojis)
		autocompleteLayout.addStretch()

		self.autocompletePage.setLayout(autocompleteLayout)

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

		self.logLabel = QLabel(f"<b>{str(config.MAXIMUM_LOADED_LOG_SIZE)} lines</b>",self)

		logsizeButton = QPushButton("")
		logsizeButton.clicked.connect(self.setLogSize)
		logsizeButton.setAutoDefault(False)

		self.logDescription = QLabel("""
			<small>
			Full logs are not loaded for display. The below settings
			controls how much of the log is loaded into the application
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

		logLayout = QVBoxLayout()
		logLayout.addWidget(widgets.textSeparatorLabel(self,"<b>chat log settings</b>"))
		logLayout.addWidget(self.saveChanLogs)
		logLayout.addWidget(self.loadChanLogs)
		logLayout.addWidget(self.savePrivLogs)
		logLayout.addWidget(self.loadPrivLogs)
		logLayout.addWidget(self.markLog)
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

		messageLayout = QVBoxLayout()
		messageLayout.addWidget(widgets.textSeparatorLabel(self,"<b>message settings</b>"))
		messageLayout.addWidget(self.showColors)
		messageLayout.addWidget(self.showLinks)
		messageLayout.addWidget(self.createWindow)
		messageLayout.addWidget(self.writePrivate)
		messageLayout.addWidget(self.writeScroll)
		messageLayout.addStretch()

		self.messagePage.setLayout(messageLayout)

		# Timestamps

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

		timestampLayout = QVBoxLayout()
		timestampLayout.addWidget(widgets.textSeparatorLabel(self,"<b>timestamp settings</b>"))
		timestampLayout.addWidget(self.showTimestamps)
		timestampLayout.addWidget(self.timestamp24hour)
		timestampLayout.addWidget(self.timestampSeconds)
		timestampLayout.addWidget(widgets.textSeparatorLabel(self,"<b>uptime display</b>"))
		timestampLayout.addWidget(self.showUptime)
		timestampLayout.addWidget(self.showChanUptime)
		timestampLayout.addStretch()

		self.timestampPage.setLayout(timestampLayout)

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
		systrayLayout.addWidget(self.showSystrayMenu)
		systrayLayout.addWidget(self.minSystray)
		systrayLayout.addWidget(self.systrayNotify)
		systrayLayout.addWidget(self.listSystray)
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

		# Syntax

		self.syntaxPage = QWidget()

		entry = QListWidgetItem()
		entry.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
		entry.setText("Highlighting")
		entry.widget = self.syntaxPage
		entry.setIcon(QIcon(SCRIPT_ICON))
		self.selector.addItem(entry)

		self.stack.addWidget(self.syntaxPage)

		self.syntaxcomment = widgets.SyntaxColor('comment', "Comments   ",self.SYNTAX_COMMENT_COLOR,self.SYNTAX_COMMENT_STYLE,self)
		self.syntaxcommand = widgets.SyntaxColor('command', "Commands   ",self.SYNTAX_COMMAND_COLOR,self.SYNTAX_COMMAND_STYLE,self)
		self.syntaxchannel = widgets.SyntaxColor('channel', "Channels   ",self.SYNTAX_CHANNEL_COLOR,self.SYNTAX_CHANNEL_STYLE,self)
		self.syntaxalias = widgets.SyntaxColor('alias', "Aliases    ",self.SYNTAX_ALIAS_COLOR,self.SYNTAX_ALIAS_STYLE,self)

		self.syntaxfore = widgets.SyntaxTextColor('fore', "Text       ",self.SYNTAX_FOREGROUND,self)
		self.syntaxback = widgets.SyntaxTextColor('back', "Background ",self.SYNTAX_BACKGROUND,self)

		self.syntaxcomment.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxcommand.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxchannel.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxalias.syntaxChanged.connect(self.syntaxChanged)

		self.syntaxfore.syntaxChanged.connect(self.syntaxChanged)
		self.syntaxback.syntaxChanged.connect(self.syntaxChanged)

		self.syntaxDescription = QLabel("""
			<small>
			Syntax highlighting is applied to both the command section of the
			connection dialog, and the built-in script editor. Commands,
			channels, comments, and aliases appear in the colors and styles set below.
			Close and reopen any open editor windows to see changes.
			</small>
			<br>
			""")
		self.syntaxDescription.setWordWrap(True)
		self.syntaxDescription.setAlignment(Qt.AlignJustify)

		tbLay = QHBoxLayout()
		tbLay.addWidget(self.syntaxfore)
		tbLay.addWidget(self.syntaxback)

		scLine1 = QHBoxLayout()
		scLine1.addWidget(self.syntaxcomment)
		scLine1.addWidget(self.syntaxcommand)

		scLine2 = QHBoxLayout()
		scLine2.addWidget(self.syntaxchannel)
		scLine2.addWidget(self.syntaxalias)

		syntaxLayout = QVBoxLayout()
		syntaxLayout.addWidget(widgets.textSeparatorLabel(self,"<b>syntax highlighting</b>"))
		syntaxLayout.addWidget(self.syntaxDescription)
		syntaxLayout.addLayout(tbLay)
		syntaxLayout.addLayout(scLine1)
		syntaxLayout.addLayout(scLine2)
		syntaxLayout.addStretch()

		self.syntaxPage.setLayout(syntaxLayout)

		self.changed.hide()

		# Buttons

		saveButton = QPushButton("Apply")
		saveButton.clicked.connect(self.save)
		saveButton.setAutoDefault(False)

		cancelButton = QPushButton("Cancel")
		cancelButton.clicked.connect(self.close)

		# Finalize layout

		notificationLayout = QVBoxLayout()
		notificationLayout.addWidget(self.changed)

		dialogButtonsLayout = QHBoxLayout()
		dialogButtonsLayout.addLayout(notificationLayout)
		dialogButtonsLayout.addStretch()
		dialogButtonsLayout.addWidget(saveButton)
		dialogButtonsLayout.addWidget(cancelButton)

		mainLayout = QHBoxLayout()
		mainLayout.addWidget(self.selector)
		mainLayout.addWidget(self.stack)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(mainLayout)
		finalLayout.addLayout(dialogButtonsLayout)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())

	def save(self):

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

		# Save new settings to the config file
		config.save_settings(config.CONFIG_FILE)

		# Get current active window
		current_window = self.parent.MDI.activeSubWindow()

		self.parent.app.setStyle(self.qt_style)

		if config.TIMESTAMP_24_HOUR:
			ts = '%H:%M'
		else:
			ts = '%I:%M'
		if config.TIMESTAMP_SHOW_SECONDS: ts = ts + ':%S'

		config.TIMESTAMP_FORMAT = ts

		self.parent.setAllLanguage(config.DEFAULT_SPELLCHECK_LANGUAGE)
		if self.rerender: self.parent.reRenderAll()
		if self.rerenderUsers: self.parent.rerenderUserlists()

		if self.rerenderNick:
			self.parent.toggleNickDisplay()
			if not self.rerenderUsers: self.parent.rerenderUserlists()

		if self.newfont!=None:
			config.APPLICATION_FONT = self.newfont.toString()
			self.parent.app.setFont(self.newfont)
			self.parent.setAllFont(self.newfont)

		self.parent.subWindowActivated(None)

		if config.SHOW_SYSTRAY_ICON:
			self.parent.tray.setVisible(True)
			self.parent.tray.show()
			self.parent.buildSystrayMenu()
		else:
			self.parent.tray.setVisible(False)
			self.parent.tray.hide()

		self.parent.buildMenu()

		self.parent.refreshAllTopic()
		if config.SHOW_CHANNEL_TOPIC:
			self.parent.showAllTopic()
		else:
			self.parent.hideAllTopic()

		if self.swapUserlists: self.parent.swapAllUserlists()

		# Set the application font
		self.parent.app.setFont(self.parent.application_font)

		# Set the widget font
		self.parent.setFont(self.parent.application_font)

		# Set active window back
		self.parent.MDI.setActiveSubWindow(current_window)

		# Close the dialog
		self.close()