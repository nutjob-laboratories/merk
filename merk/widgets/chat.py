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

import re
import uuid
import fnmatch
import pathlib

import emoji

from spellchecker import SpellChecker

from ..resources import *
from .. import config
from .. import styles
from .. import render
from ..dialog import *
from .. import logs
from .plain_text import plainTextAction,noSpacePlainTextAction
from .text_separator import textSeparatorLabel,textSeparator
from .extendedmenuitem import ExtendedMenuItemNoAction

from .. import commands

from .. import syntax

class Window(QMainWindow):

	def reload_config(self):
		config.load_settings(config.CONFIG_FILE)

	def window_interacted_with(self):
		if config.USE_AUTOAWAY:
			if config.WINDOW_INTERACTION_CANCELS_AUTOAWAY:
				if self.client.autoaway:
					self.client.back()

				self.client.last_interaction = 0

	def __init__(self,name,client,window_type,app,parent=None):
		super(Window, self).__init__(parent)

		self.name = name
		self.client = client
		self.window_type = window_type
		self.app = app
		self.parent = parent

		self.subwindow_id = str(uuid.uuid4())
		self.default_style = styles.loadDefault()

		self.uptime = 0

		self.channel_topic = ""		# Channel topic
		self.userlist_width = 0		# Userlist width

		self.user_count = 0

		self.language = config.DEFAULT_SPELLCHECK_LANGUAGE

		self.history_buffer = ['']
		self.history_buffer_pointer = 0

		self.log = []
		self.new_log = []
		self.full_nicks = []

		self.users = []
		self.nicks = []
		self.hostmasks = {}
		self.operator = False
		self.voiced = False
		self.owner = False
		self.admin = False
		self.halfop = False
		self.protected = False

		self.banlist = []
		self.away = {}

		self.userlist_visible = True

		self.force_close = False

		self.current_date = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%A %B %d, %Y')

		self.dosave = QTimer(self)
		self.dosave.timeout.connect(self.saveLogs)
		self.dosave.start(config.LOG_SAVE_INTERVAL)

		self.setWindowTitle(self.name)

		if self.window_type==CHANNEL_WINDOW:
			icon = CHANNEL_ICON
		elif self.window_type==SERVER_WINDOW:
			icon = CONSOLE_ICON
		elif self.window_type==PRIVATE_WINDOW:
			icon = PRIVATE_ICON
		self.setWindowIcon(QIcon(icon))

		f = self.parent.app.font()
		self.setFont(f)

		# For nick autocomplete
		if self.window_type==PRIVATE_WINDOW: self.nicks = [ self.name ]

		if self.window_type==SERVER_WINDOW:

			if self.client.kwargs["ssl"]:
				name = "SSL/TLS"
			else:
				name = "TCP/IP "

			self.server_info_menu = buildServerSettingsMenu(self,self.client)

			self.info_button = QPushButton(name)
			self.info_button.setMenu(self.server_info_menu)
			self.info_button.setToolTip("IRC Server")
			self.info_button.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
			self.info_button.setFlat(True)
			f = self.info_button.font()
			f.setBold(True)
			self.info_button.setFont(f)

			serverBar = QHBoxLayout()
			serverBar.addWidget(self.info_button)

			self.join_button = QPushButton("")
			self.join_button.setIcon(QIcon(CHANNEL_ICON))
			self.join_button.clicked.connect(self.joinChannel)
			self.join_button.setToolTip("Join a channel")
			self.join_button.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
			self.join_button.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
			self.join_button.setFlat(True)
			serverBar.addWidget(self.join_button)

			self.nick_button = QPushButton("")
			self.nick_button.setIcon(QIcon(PRIVATE_ICON))
			self.nick_button.clicked.connect(self.changeNick)
			self.nick_button.setToolTip("Change your nickname")
			self.nick_button.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
			self.nick_button.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
			self.nick_button.setFlat(True)
			serverBar.addWidget(self.nick_button)

			self.away_button = QPushButton("")
			self.away_button.setIcon(QIcon(GO_AWAY_ICON))
			self.away_button.clicked.connect(self.changeAway)
			self.away_button.setToolTip("Set status to \"away\"")
			self.away_button.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
			self.away_button.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
			self.away_button.setFlat(True)
			serverBar.addWidget(self.away_button)

			self.script_button = QPushButton("")
			self.script_button.setIcon(QIcon(RUN_ICON))
			self.script_button.clicked.connect(lambda state,u=True: self.loadScript(u))
			self.script_button.setToolTip("Run a script")
			self.script_button.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
			self.script_button.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
			self.script_button.setFlat(True)
			serverBar.addWidget(self.script_button)

			if not config.SCRIPTING_ENGINE_ENABLED:
				self.script_button.hide()

			self.refresh_button = QPushButton("")
			self.refresh_button.setIcon(QIcon(REFRESH_ICON))
			self.refresh_button.clicked.connect(self.refreshChannelList)
			self.refresh_button.setToolTip("Refresh channel list")
			self.refresh_button.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
			self.refresh_button.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
			self.refresh_button.setFlat(True)
			serverBar.addWidget(self.refresh_button)

			if not config.SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS:
				self.refresh_button.hide()

			self.list_button = QPushButton("")
			self.list_button.setIcon(QIcon(LIST_ICON))
			self.list_button.clicked.connect(self.showChannelList)
			self.list_button.setToolTip("Server channel list")
			self.list_button.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
			self.list_button.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
			self.list_button.setFlat(True)
			serverBar.addWidget(self.list_button)

			if not config.SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS:
				self.list_button.hide()

			serverBar.addStretch()

			self.serverUptime = QLabel("<b>00:00:00</b>")
			serverBar.addWidget(self.serverUptime)

			if not config.SHOW_CONNECTION_UPTIME: self.serverUptime.hide()
			if config.SHOW_STATUS_BAR_ON_SERVER_WINDOWS: self.serverUptime.hide()

			sep1 = QFrame()
			sep1.setFrameShape(QFrame.VLine)
			sep1.setFrameShadow(QFrame.Sunken)
			sep1.setLineWidth(1)

			serverBar.addWidget(sep1)

			entry = QPushButton("")
			entry.setIcon(QIcon(DISCONNECT_WINDOW_ICON))
			entry.clicked.connect(self.disconnect)
			entry.setToolTip("Disconnect from server")
			entry.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
			entry.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
			entry.setFlat(True)
			serverBar.addWidget(entry)

			serverBar.setContentsMargins(1,1,1,1)
			self.server_window_toolbar = QWidget()
			self.server_window_toolbar.setLayout(serverBar)
			self.server_window_toolbar.setMinimumHeight(config.INTERFACE_BUTTON_SIZE)
			self.server_window_toolbar.setMaximumHeight(config.INTERFACE_BUTTON_SIZE)

			if not config.SHOW_SERVER_WINDOW_TOOLBAR: self.server_window_toolbar.hide()

			self.nick_button.setEnabled(False)
			self.join_button.setEnabled(False)
			self.info_button.setEnabled(False)
			self.script_button.setEnabled(False)
			self.list_button.setEnabled(False)
			self.refresh_button.setEnabled(False)
			self.away_button.setEnabled(False)

		if self.window_type==CHANNEL_WINDOW:

			if self.parent.dark_mode:
				border_color = "white"
			else:
				border_color = "black"

			# Channel name display
			self.channel_mode_display = QLabel("<b>"+self.name+"</b>")
			self.channel_mode_display.setStyleSheet(f"border: 1px solid {border_color}; padding: 0px;")

			# Channel name display
			self.channel_users_display = QLabel("<b><small>1 user</small></b>")
			self.channel_users_display.setStyleSheet(f"border: 1px solid {border_color}; padding: 0px;")
			self.channel_users_display.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
			
			# Create topic editor
			self.topic = TopicEdit(self)
			self.topic.returnPressed.connect(self.handleTopicInput)
			self.topic.setReadOnly(True)

			# Set topic editors color to the same as the
			# window background
			col = self.parent.palette().color(QPalette.Background).name()
			self.topic.setFrame(False)
			p = self.topic.palette()
			p.setColor(QPalette.Base, QColor(col))
			self.topic.setPalette(p)

			# Create the uselist
			self.userlist = QListWidget(self)
			self.userlist.setFocusPolicy(Qt.NoFocus)
			self.userlist.itemDoubleClicked.connect(self.handleDoubleClick)
			self.userlist.installEventFilter(self)
			self.userlist.setIconSize(QSize(config.USERLIST_ICON_SIZE, config.USERLIST_ICON_SIZE))

			if config.HIDE_USERLIST_HORIZONTAL_SCROLLBAR:
				self.userlist.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			else:
				self.userlist.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

			f = self.userlist.font()
			f.setBold(True)
			self.userlist.setFont(f)

			self.channelUptime = QLabel("<small>00:00:00</small>")

			if not config.SHOW_CHANNEL_UPTIME: self.channelUptime.hide()

			if not config.SHOW_USERLIST:
				self.userlist.hide()
				self.userlist_visible = False

			if not config.SHOW_USER_COUNT_DISPLAY:
				self.channel_users_display.hide()

		# Create chat display widget
		self.chat = QTextBrowser(self)
		self.chat.setFocusPolicy(Qt.NoFocus)
		self.chat.anchorClicked.connect(self.linkClicked)
		self.chat.setReadOnly(True)

		self.chat.setContextMenuPolicy(Qt.CustomContextMenu)
		self.chat.customContextMenuRequested.connect(self.chatMenu)

		# Create text input widget
		self.input = SpellTextEdit(self)
		self.input.returnPressed.connect(self.handleUserInput)
		self.input.keyUp.connect(self.keyPressUp)
		self.input.keyDown.connect(self.keyPressDown)

		# Text input widget should only be one line
		fm = self.input.fontMetrics()
		# self.input.setFixedHeight(fm.height()+12)
		self.input.setFixedHeight(fm.height()+10)
		self.input.setWordWrapMode(QTextOption.NoWrap)
		self.input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		# Set input language for spell checker
		self.input.changeLanguage(self.language)

		# Nickname display
		self.nick_display = QLabel("<b>"+self.client.nickname+"&nbsp;</b>")
		self.mode_display = QLabel("")

		self.nick_display.installEventFilter(self)

		if len(self.client.usermodes)>0:
			self.mode_display.setText("<small>+"+self.client.usermodes+"</small>")
		else:
			self.mode_display.hide()

		# Hide the nickname display on server windows
		if self.window_type==SERVER_WINDOW:
			if not config.DISPLAY_NICK_ON_SERVER_WINDOWS:
				self.nick_display.hide()
		if self.window_type==SERVER_WINDOW: self.mode_display.hide()


		self.settingsMenu = QMenu("")

		self.buildInputOptionsMenu()

		self.settingsButton = QPushButton(QIcon(self.parent.options_icon),"")
		self.settingsButton.setIconSize(QSize(self.input.height()-10,self.input.height()))
		self.settingsButton.setFixedSize(self.input.height()-10,self.input.height())
		self.settingsButton.setToolTip("Options")
		self.settingsButton.setMenu(self.settingsMenu)
		self.settingsButton.setFlat(True)
		self.settingsButton.setStyleSheet("""
			QPushButton::menu-indicator { image: none; }
			QPushButton:pressed { border: none;}
		""")

		if not config.SHOW_INPUT_MENU: self.settingsButton.hide()

		if self.window_type!=SERVER_WINDOW:

			fm = QFontMetrics(self.app.font())

			self.op_icon = QLabel(self)
			pixmap = QPixmap(OP_USER)
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.op_icon.setPixmap(pixmap)

			self.voice_icon = QLabel(self)
			pixmap = QPixmap(VOICE_USER)
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.voice_icon.setPixmap(pixmap)

			self.owner_icon = QLabel(self)
			pixmap = QPixmap(OWNER_USER)
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.owner_icon.setPixmap(pixmap)

			self.admin_icon = QLabel(self)
			pixmap = QPixmap(ADMIN_USER)
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.admin_icon.setPixmap(pixmap)

			self.halfop_icon = QLabel(self)
			pixmap = QPixmap(HALFOP_USER)
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.halfop_icon.setPixmap(pixmap)

			self.key_icon = QLabel(self)
			pixmap = QPixmap(KEY_ICON)
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.key_icon.setPixmap(pixmap)

			self.protected_icon = QLabel(self)
			pixmap = QPixmap(PROTECTED_USER)
			pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.protected_icon.setPixmap(pixmap)

			self.op_icon.hide()
			self.voice_icon.hide()
			self.owner_icon.hide()
			self.admin_icon.hide()
			self.halfop_icon.hide()
			self.key_icon.hide()
			self.protected_icon.hide()

			self.name_spacer = QLabel("")

		nickLayout = QHBoxLayout()
		if self.window_type!=SERVER_WINDOW:
			nickLayout.addWidget(self.op_icon)
			nickLayout.addWidget(self.voice_icon)
			nickLayout.addWidget(self.owner_icon)
			nickLayout.addWidget(self.admin_icon)
			nickLayout.addWidget(self.halfop_icon)
			nickLayout.addWidget(self.protected_icon)
			nickLayout.addWidget(self.name_spacer)
		nickLayout.addWidget(self.nick_display)
		nickLayout.addWidget(self.mode_display)
		
		if self.window_type!=SERVER_WINDOW:
			if not config.SHOW_USER_INFO_ON_CHAT_WINDOWS:
				if hasattr(self,"name_spacer"): self.name_spacer.hide()
				self.nick_display.hide()
				self.mode_display.hide()

		inputLayout = QHBoxLayout()
		inputLayout.addLayout(nickLayout)
		inputLayout.addWidget(self.input)
		inputLayout.addWidget(self.settingsButton)

		if self.window_type==CHANNEL_WINDOW:

			# Channel windows will have the chat display split with
			# the user list display
			self.horizontalSplitter = QSplitter(Qt.Horizontal)
			if config.SHOW_USERLIST_ON_LEFT:
				self.horizontalSplitter.addWidget(self.userlist)
				self.horizontalSplitter.addWidget(self.chat)
			else:
				self.horizontalSplitter.addWidget(self.chat)
				self.horizontalSplitter.addWidget(self.userlist)
			self.horizontalSplitter.splitterMoved.connect(self.splitterResize)

			# Set the initial splitter ratio
			ulwidth = (fm.averageCharWidth() + 2) + (fm.averageCharWidth()*15)
			mwidth = self.width()-ulwidth
			self.horizontalSplitter.setSizes([mwidth,ulwidth])

			# Set the starting width of the userlist
			self.userlist.resize(ulwidth,self.height())
			self.userlist_width = ulwidth

			# BANLIST BUTTON
			self.banlist_menu = QPushButton("")
			self.banlist_menu.setIcon(QIcon(BAN_ICON))
			self.banlist_menu.setMenu(buildBanMenu(self,self.client))
			self.banlist_menu.setStyleSheet("QPushButton::menu-indicator { image: none; }")
			self.banlist_menu.setToolTip("Channel bans")
			self.banlist_menu.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
			self.banlist_menu.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
			self.banlist_menu.setFlat(True)

			self.banlist_menu.hide()

			self.channel_menu = QPushButton("")
			self.channel_menu.setIcon(QIcon(MODES_ICON))
			self.channel_menu.setMenu(buildBanMenu(self,self.client))
			self.channel_menu.setStyleSheet("QPushButton::menu-indicator { image: none; }")
			self.channel_menu.setToolTip("Set channel modes")
			self.channel_menu.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
			self.channel_menu.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
			self.channel_menu.setFlat(True)

			self.channel_menu.hide()

			topicLayout = QHBoxLayout()
			topicLayout.addWidget(self.channel_menu)
			topicLayout.addWidget(self.banlist_menu)
			topicLayout.addWidget(self.channel_mode_display)
			topicLayout.addWidget(self.topic)
			topicLayout.addWidget(self.channel_users_display)

			if not config.SHOW_CHANNEL_TOPIC:
				self.hideTopic()

			if not config.SHOW_CHANNEL_NAME_AND_MODES:
				self.channel_mode_display.hide()

			if not config.SHOW_BANLIST_MENU:
				self.banlist_menu.hide()

			if not config.SHOW_CHANNEL_MENU:
				self.channel_menu.hide()

			finalLayout = QVBoxLayout()
			finalLayout.setSpacing(CHAT_WINDOW_WIDGET_SPACING)
			finalLayout.setContentsMargins(CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING)
			finalLayout.addLayout(topicLayout)
			finalLayout.addWidget(self.horizontalSplitter)
			finalLayout.addLayout(inputLayout)

		else:

			finalLayout = QVBoxLayout()
			finalLayout.setSpacing(CHAT_WINDOW_WIDGET_SPACING)
			finalLayout.setContentsMargins(CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING,CHAT_WINDOW_WIDGET_SPACING)
			if self.window_type==SERVER_WINDOW: finalLayout.addWidget(self.server_window_toolbar)
			finalLayout.addWidget(self.chat)
			finalLayout.addLayout(inputLayout)

		# Finalize the layout
		interface = QWidget()
		interface.setLayout(finalLayout)
		self.setCentralWidget(interface)

		self.input.setFocus()

		if self.window_type==SERVER_WINDOW:
			# Create the status bar, and give it a "flat" style
			self.status = self.statusBar()
			self.status.setStyleSheet("QStatusBar::item { border: none; }")

			# Here, we display the server the chat window is associated
			# with, as well as how the client is connected to it (using
			# SSL/TLS or not) and other information
			fm = QFontMetrics(self.app.font())
			if self.client.kwargs["ssl"]:
				self.secure_icon = QLabel(self)
				pixmap = QPixmap(VISITED_SECURE_ICON)
				pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
				self.secure_icon.setPixmap(pixmap)
				self.status.addPermanentWidget(self.secure_icon,0)
				self.status_server = QLabel(f"<small><b>{self.client.server}:{self.client.port}</b></small>")
				self.status_server.setOpenExternalLinks(True)
			else:
				self.secure_icon = QLabel(self)
				pixmap = QPixmap(VISITED_BOOKMARK_ICON)
				pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
				self.secure_icon.setPixmap(pixmap)
				self.status.addPermanentWidget(self.secure_icon,0)
				self.status_server = QLabel(f"<small><b>{self.client.server}:{self.client.port}</b></small>")
				self.status_server.setOpenExternalLinks(True)
			self.status.addPermanentWidget(self.status_server,0)

			# Spacer
			self.status.addPermanentWidget(QLabel(),1)

			self.statusServerUptime = QLabel("<small>00:00:00</small>")

			self.status.addPermanentWidget(self.statusServerUptime,0)
			self.status.addPermanentWidget(QLabel(' '),0)

			if not config.SHOW_STATUS_BAR_ON_SERVER_WINDOWS: self.status.hide()

		# Channel and private chat windows get a status bar
		if self.window_type==CHANNEL_WINDOW or self.window_type==PRIVATE_WINDOW:

			# Create the status bar, and give it a "flat" style
			self.status = self.statusBar()
			self.status.setStyleSheet("QStatusBar::item { border: none; }")

			# Here, we display the server the chat window is associated
			# with, as well as how the client is connected to it (using
			# SSL/TLS or not) and other information
			fm = QFontMetrics(self.app.font())
			if self.client.kwargs["ssl"]:
				self.secure_icon = QLabel(self)
				pixmap = QPixmap(VISITED_SECURE_ICON)
				pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
				self.secure_icon.setPixmap(pixmap)
				self.status.addPermanentWidget(self.secure_icon,0)
				if config.SHOW_LINKS_TO_NETWORK_WEBPAGES:
					netlink = get_network_link(self.client.network)
					if netlink!=None:
						self.status_server = QLabel("<small><b>"+self.client.hostname+"</b> (<a href=\""+netlink+"\">"+self.client.network+"</a>)</small>")
					else:
						self.status_server = QLabel("<small><b>"+self.client.hostname+"</b> ("+self.client.network+")</small>")
				else:
					self.status_server = QLabel("<small><b>"+self.client.hostname+"</b> ("+self.client.network+")</small>")
				self.status_server.setOpenExternalLinks(True)
			else:
				self.secure_icon = QLabel(self)
				pixmap = QPixmap(VISITED_BOOKMARK_ICON)
				pixmap = pixmap.scaled(fm.height(), fm.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
				self.secure_icon.setPixmap(pixmap)
				self.status.addPermanentWidget(self.secure_icon,0)
				if config.SHOW_LINKS_TO_NETWORK_WEBPAGES:
					netlink = get_network_link(self.client.network)
					if netlink!=None:
						self.status_server = QLabel("<small><b>"+self.client.hostname+"</b> (<a href=\""+netlink+"\">"+self.client.network+"</a>)</small>")
					else:
						self.status_server = QLabel("<small><b>"+self.client.hostname+"</b> ("+self.client.network+")</small>")
				else:
					self.status_server = QLabel("<small><b>"+self.client.hostname+"</b> ("+self.client.network+")</small>")
				self.status_server.setOpenExternalLinks(True)
			self.status.addPermanentWidget(self.status_server,0)

			# Spacer
			self.status.addPermanentWidget(QLabel(),1)

			# Channel windows will display the key for that
			# channel (if set) in the lower right corner
			if self.window_type==CHANNEL_WINDOW:
				self.status.addPermanentWidget(self.key_icon,0)
				self.key_value = QLabel("")
				self.status.addPermanentWidget(self.key_value,0)
				self.key_value.hide()

			if self.window_type==CHANNEL_WINDOW:
				self.key_spacer = QLabel("")
				self.status.addPermanentWidget(self.key_spacer,0)
				self.key_spacer.hide()
				self.status.addPermanentWidget(self.channelUptime,0)
				self.status.addPermanentWidget(QLabel(' '),0)

			if not config.SHOW_STATUS_BAR_ON_CHAT_WINDOWS: self.status.hide()

		# Load and apply default style
		self.applyStyle()

		# Decide whether to load logs or not
		load_logs = True

		if self.window_type==CHANNEL_WINDOW:
			if config.LOAD_CHANNEL_LOGS:
				load_logs=True
			else:
				load_logs=False

		if self.window_type==PRIVATE_WINDOW:
			if config.LOAD_PRIVATE_LOGS:
				load_logs=True
			else:
				load_logs=False

		# Only channel and private chat windows load logs
		if self.window_type==CHANNEL_WINDOW or self.window_type==PRIVATE_WINDOW:
			if load_logs:

				QApplication.setOverrideCursor(Qt.WaitCursor)

				# Load log from disk
				loadLog = logs.readLog(self.client.network,self.name,logs.LOG_DIRECTORY)
				# If the log is too long (which, after a while, it *will* be), we
				# trim it, so that the chat window doesn't take up 50GB of memory
				if len(loadLog)>config.MAXIMUM_LOADED_LOG_SIZE:
					loadLog = logs.trimLog(loadLog,config.MAXIMUM_LOADED_LOG_SIZE)
				# If there's been log data loaded, add it to the internal
				# log of the chat window
				if len(loadLog)>0:
					self.log = loadLog + self.log
					# Now, we insert day markers; starting with the first saved
					# log message, we will insert a separator before the first
					# message of a new day containing the date the following
					# messages will have taken place on. This makes reading
					# the loaded log a bit clearer. We step through the loaded
					# log data, checking the date of each message, placing
					# our markers whenever the date changes, the then replace
					# the loaded log data with our "altered" log.
					cdate = None
					marked = []
					for e in self.log:
						ndate = datetime.fromtimestamp(e.timestamp).strftime('%A %B %d, %Y')
						if cdate!=ndate:
							cdate = ndate
							m = Message(DATE_MESSAGE,'',cdate)
							marked.append(m)
						marked.append(e)
					self.log = marked
					# Mark end of loaded log
					if config.MARK_END_OF_LOADED_LOG:
						t = datetime.timestamp(datetime.now())
						pretty_timestamp = datetime.fromtimestamp(t).strftime('%m/%d/%Y, '+config.TIMESTAMP_FORMAT)
						self.log.append(Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',"Resumed on "+pretty_timestamp))
				# Now, rerender all text in the log, so that
				# the loaded log data is displayed
				self.rerenderChatLog()

				QApplication.restoreOverrideCursor()

	def showChannelList(self):
		if len(self.client.server_channel_list)==0:
			self.client.need_to_get_list = True
			self.client.sendLine("LIST")
			return
		if self.client.channel_list_window==None:
			self.parent.newListWindow(self.client,self)
		else:
			self.parent.showSubWindow(self.client.channel_list_window)

	def refreshChannelList(self):
		self.client.sendLine("LIST")

	def showChannelListSearch(self,search_terms,do_fresh_search=False):
		if do_fresh_search==True:
			self.client.need_to_get_list = True
			self.client.sendLine("LIST")
			self.client.list_search_terms = search_terms
			return
		if len(self.client.server_channel_list)==0:
			self.client.need_to_get_list = True
			self.client.sendLine("LIST")
			self.client.list_search_terms = search_terms
			return
		if self.client.channel_list_window==None:
			w = self.parent.newListWindow(self.client,self)
			c = w.widget()
			c.doExternalSearch(search_terms)
		else:
			self.parent.showSubWindow(self.client.channel_list_window)
			c = self.client.channel_list_window.widget()
			c.doExternalSearch(search_terms)

	def toggleRefreshButton(self):
		if self.window_type==SERVER_WINDOW:
			if config.SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS:
				self.refresh_button.show()
			else:
				self.refresh_button.hide()
			if config.SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS:
				self.list_button.show()
			else:
				self.list_button.hide()

	def toggleServerToolbar(self):
		if hasattr(self,"server_window_toolbar"):
			if config.SHOW_SERVER_WINDOW_TOOLBAR:
				self.server_window_toolbar.show()
			else:
				self.server_window_toolbar.hide()

	def toggleStatusBar(self):
		if self.window_type==SERVER_WINDOW:
			if not config.SHOW_STATUS_BAR_ON_SERVER_WINDOWS:
				self.status.hide()
			else:
				self.status.show()
			return
		if not config.SHOW_STATUS_BAR_ON_CHAT_WINDOWS:
			self.status.hide()
		else:
			self.status.show()

	def toggleServNicks(self):
		if self.window_type==SERVER_WINDOW:
			if not config.DISPLAY_NICK_ON_SERVER_WINDOWS:
				self.nick_display.hide()
			else:
				self.nick_display.show()

	def unset_mode(self,mode):
		self.client.mode(self.name,False,mode)

	def set_mode(self,mode):
		self.client.mode(self.name,True,mode)

	def lock_channel(self):

		my_key = SetKeyDialog(self)
		if my_key:
			self.client.mode(self.name,True,'k '+my_key)

	def is_privileged(self):
		if self.operator: return True
		if self.halfop: return True
		if self.owner: return True
		if self.admin: return True
		if self.protected: return True

	def is_operator(self):
		if self.operator: return True
		if self.owner: return True
		if self.admin: return True
		if self.protected: return True

	def buildOperatorMenu(self):

		opmenu = QMenu("Channel modes")

		try:
			channel_modes = self.client.channelmodes[self.name]
		except:
			channel_modes = ''

		e = textSeparator(self,"Channel modes")
		opmenu.addAction(e)

		if self.is_privileged():

			if self.name in self.client.channelkeys:
				entry = QAction(QIcon(MINUS_ICON),"Unlock channel",self)
				entry.triggered.connect(lambda state,h='k '+self.client.channelkeys[self.name]: self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Lock channel",self)
				entry.triggered.connect(self.lock_channel)
				opmenu.addAction(entry)

			if 'm' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Unmoderate channel",self)
				entry.triggered.connect(lambda state,h='m': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Moderate channel",self)
				entry.triggered.connect(lambda state,h='m': self.set_mode(h))
				opmenu.addAction(entry)

			if 'n' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Allow external messages",self)
				entry.triggered.connect(lambda state,h='n': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Forbid external messages",self)
				entry.triggered.connect(lambda state,h='n': self.set_mode(h))
				opmenu.addAction(entry)

			if 't' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Anyone can change topic",self)
				entry.triggered.connect(lambda state,h='t': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Protect channel topic",self)
				entry.triggered.connect(lambda state,h='t': self.set_mode(h))
				opmenu.addAction(entry)

		if self.is_operator():

			if 'c' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Allow IRC color",self)
				entry.triggered.connect(lambda state,h='c': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Forbid IRC color",self)
				entry.triggered.connect(lambda state,h='c': self.set_mode(h))
				opmenu.addAction(entry)

			if 'S' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Do not remove IRC color",self)
				entry.triggered.connect(lambda state,h='S': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Remove IRC color",self)
				entry.triggered.connect(lambda state,h='S': self.set_mode(h))
				opmenu.addAction(entry)

			if 'C' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Allow CTCP",self)
				entry.triggered.connect(lambda state,h='C': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Forbid CTCP",self)
				entry.triggered.connect(lambda state,h='C': self.set_mode(h))
				opmenu.addAction(entry)

			if 'KNOCK' in self.client.supports:
				if 'K' in channel_modes:
					entry = QAction(QIcon(MINUS_ICON),"Allow knocks",self)
					entry.triggered.connect(lambda state,h='K': self.unset_mode(h))
					opmenu.addAction(entry)
				else:
					entry = QAction(QIcon(PLUS_ICON),"Forbid knocks",self)
					entry.triggered.connect(lambda state,h='K': self.set_mode(h))
					opmenu.addAction(entry)

			if 'i' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Allow uninvited users",self)
				entry.triggered.connect(lambda state,h='i': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Only invited users",self)
				entry.triggered.connect(lambda state,h='i': self.set_mode(h))
				opmenu.addAction(entry)

			if 'p' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Make channel public",self)
				entry.triggered.connect(lambda state,h='p': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Make channel private",self)
				entry.triggered.connect(lambda state,h='p': self.set_mode(h))
				opmenu.addAction(entry)

			if 's' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Make channel unsecret",self)
				entry.triggered.connect(lambda state,h='s': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Make channel secret",self)
				entry.triggered.connect(lambda state,h='s': self.set_mode(h))
				opmenu.addAction(entry)

			if 'T' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Allow channel notices",self)
				entry.triggered.connect(lambda state,h='T': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Forbid channel notices",self)
				entry.triggered.connect(lambda state,h='T': self.set_mode(h))
				opmenu.addAction(entry)

			if 'V' in channel_modes:
				entry = QAction(QIcon(MINUS_ICON),"Allow invites",self)
				entry.triggered.connect(lambda state,h='V': self.unset_mode(h))
				opmenu.addAction(entry)
			else:
				entry = QAction(QIcon(PLUS_ICON),"Forbid invites",self)
				entry.triggered.connect(lambda state,h='V': self.set_mode(h))
				opmenu.addAction(entry)

		return opmenu

	def chatMenu(self,location):

		menu = self.chat.createStandardContextMenu()

		if config.SHOW_CHAT_CONTEXT_MENUS:

			if self.window_type==SERVER_WINDOW:

				menu.addSeparator()

				if config.ENABLE_STYLE_EDITOR:
					if not config.FORCE_DEFAULT_STYLE:
						entry = QAction(QIcon(STYLE_ICON),"Edit text style",self)
						entry.triggered.connect(self.pressedStyleButton)
						menu.addAction(entry)

				entry = QAction(QIcon(CLEAR_ICON),"Clear log",self)
				entry.triggered.connect(self.clearChat)
				menu.addAction(entry)

				self.contextNick = QAction(QIcon(PRIVATE_ICON),"Change nickname",self)
				self.contextNick.triggered.connect(self.changeNick)
				menu.addAction(self.contextNick)

				self.contextJoin = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
				self.contextJoin.triggered.connect(self.joinChannel)
				menu.addAction(self.contextJoin)

				if config.SCRIPTING_ENGINE_ENABLED:
					self.contextRun = QAction(QIcon(RUN_ICON),"Run script",self)
					self.contextRun.triggered.connect(self.loadScript)
					menu.addAction(self.contextRun)

					hostid = self.client.server+":"+str(self.client.port)
					entry = QAction(QIcon(EDIT_ICON),"Edit connection script",self)
					entry.triggered.connect(lambda state,h=hostid: self.parent.newEditorWindowConnect(h))
					menu.addAction(entry)

				if config.SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS:
					if config.SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS:
						menu.addSeparator()

				if config.SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS:
					self.contextList = QAction(QIcon(LIST_ICON),"Server channel list",self)
					self.contextList.triggered.connect(self.showChannelList)
					menu.addAction(self.contextList)

				if config.SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS:
					self.contextRefresh = QAction(QIcon(REFRESH_ICON),"Refresh channel list",self)
					self.contextRefresh.triggered.connect(self.refreshChannelList)
					menu.addAction(self.contextRefresh)

				menu.addSeparator()

				entry = QAction(QIcon(CLOSE_ICON),"Disconnect from server",self)
				entry.triggered.connect(self.disconnect)
				menu.addAction(entry)

				if self.client.hostname==None:
					self.contextNick.setEnabled(False)
					self.contextJoin.setEnabled(False)
					if config.SCRIPTING_ENGINE_ENABLED:
						self.contextRun.setEnabled(False)

			if self.window_type!=SERVER_WINDOW:

				menu.addSeparator()

				if config.ENABLE_STYLE_EDITOR:
					if not config.FORCE_DEFAULT_STYLE:
						entry = QAction(QIcon(STYLE_ICON),"Edit text style",self)
						entry.triggered.connect(self.pressedStyleButton)
						menu.addAction(entry)

				if config.SCRIPTING_ENGINE_ENABLED:
					self.contextRun = QAction(QIcon(RUN_ICON),"Run script",self)
					self.contextRun.triggered.connect(self.loadScript)
					menu.addAction(self.contextRun)

				entry = QAction(QIcon(CLEAR_ICON),"Clear chat",self)
				entry.triggered.connect(self.clearChat)
				menu.addAction(entry)

				entry = QAction(QIcon(LOG_ICON),"Save log to file",self)
				entry.triggered.connect(self.menuSaveLogs)
				menu.addAction(entry)

			if self.window_type==CHANNEL_WINDOW:

				menu.addSeparator()

				entry = QAction(QIcon(CHANNEL_ICON),"Leave channel",self)
				if config.ENABLE_EMOJI_SHORTCODES:
					msg = emoji.emojize(config.DEFAULT_QUIT_MESSAGE,language=config.EMOJI_LANGUAGE)
				else:
					msg = config.DEFAULT_QUIT_MESSAGE
				entry.triggered.connect(lambda state,u=self.name,w=msg: self.client.leave(u,w))
				menu.addAction(entry)

			if self.window_type==PRIVATE_WINDOW:

				menu.addSeparator()

				entry = QAction(QIcon(CLOSE_ICON),"Close window",self)
				entry.triggered.connect(self.close)
				menu.addAction(entry)


		action = menu.exec_(self.chat.mapToGlobal(location))

	def buildInputOptionsMenu(self):

		self.settingsMenu.clear()

		if config.ENABLE_STYLE_EDITOR:
			if not config.FORCE_DEFAULT_STYLE:
				entry = QAction(QIcon(STYLE_ICON),"Edit text style",self)
				entry.triggered.connect(self.pressedStyleButton)
				self.settingsMenu.addAction(entry)

		if self.window_type!=SERVER_WINDOW:

			entry = QAction(QIcon(CLEAR_ICON),"Clear chat",self)
			entry.triggered.connect(self.clearChat)
			self.settingsMenu.addAction(entry)

			entry = QAction(QIcon(LOG_ICON),"Save log to file",self)
			entry.triggered.connect(self.menuSaveLogs)
			self.settingsMenu.addAction(entry)

		if self.window_type==SERVER_WINDOW:
			entry = QAction(QIcon(CLEAR_ICON),"Clear log",self)
			entry.triggered.connect(self.clearChat)
			self.settingsMenu.addAction(entry)

		if config.SCRIPTING_ENGINE_ENABLED:
			entry = QAction(QIcon(RUN_ICON),"Run script",self)
			entry.triggered.connect(self.loadScript)
			self.settingsMenu.addAction(entry)

		if config.ENABLE_SPELLCHECK:
			# Spellcheck Button
			self.spellcheckMenu = QMenu("Spellcheck")
			self.spellcheckMenu.setIcon(QIcon(SPELLCHECK_ICON))

			self.languageEnglish = QAction(QIcon(self.parent.round_unchecked_icon),"English",self)
			self.languageEnglish.triggered.connect(lambda state,u="en": self.menuSetLanguage(u))
			self.spellcheckMenu.addAction(self.languageEnglish)

			self.languageFrench = QAction(QIcon(self.parent.round_unchecked_icon),"Française",self)
			self.languageFrench.triggered.connect(lambda state,u="fr": self.menuSetLanguage(u))
			self.spellcheckMenu.addAction(self.languageFrench)

			self.languageSpanish = QAction(QIcon(self.parent.round_unchecked_icon),"Español",self)
			self.languageSpanish.triggered.connect(lambda state,u="es": self.menuSetLanguage(u))
			self.spellcheckMenu.addAction(self.languageSpanish)

			self.languageGerman = QAction(QIcon(self.parent.round_unchecked_icon),"Deutsche",self)
			self.languageGerman.triggered.connect(lambda state,u="de": self.menuSetLanguage(u))
			self.spellcheckMenu.addAction(self.languageGerman)

			self.languagePortuguese = QAction(QIcon(self.parent.round_unchecked_icon),"Português",self)
			self.languagePortuguese.triggered.connect(lambda state,u="pt": self.menuSetLanguage(u))
			self.spellcheckMenu.addAction(self.languagePortuguese)

			self.languageItalian = QAction(QIcon(self.parent.round_unchecked_icon),"Italiano",self)
			self.languageItalian.triggered.connect(lambda state,u="it": self.menuSetLanguage(u))
			self.spellcheckMenu.addAction(self.languageItalian)

			self.languageDutch = QAction(QIcon(self.parent.round_unchecked_icon),"Nederlands",self)
			self.languageDutch.triggered.connect(lambda state,u="nl": self.menuSetLanguage(u))
			self.spellcheckMenu.addAction(self.languageDutch)

			self.languageRussian = QAction(QIcon(self.parent.round_unchecked_icon),"Русский",self)
			self.languageRussian.triggered.connect(lambda state,u="ru": self.menuSetLanguage(u))
			self.spellcheckMenu.addAction(self.languageRussian)

			if self.language=="en": self.languageEnglish.setIcon(QIcon(self.parent.round_checked_icon))
			if self.language=="fr": self.languageFrench.setIcon(QIcon(self.parent.round_checked_icon))
			if self.language=="es": self.languageSpanish.setIcon(QIcon(self.parent.round_checked_icon))
			if self.language=="de": self.languageGerman.setIcon(QIcon(self.parent.round_checked_icon))
			if self.language=="pt": self.languagePortuguese.setIcon(QIcon(self.parent.round_checked_icon))
			if self.language=="it": self.languageItalian.setIcon(QIcon(self.parent.round_checked_icon))
			if self.language=="nl": self.languageDutch.setIcon(QIcon(self.parent.round_checked_icon))
			if self.language=="ru": self.languageRussian.setIcon(QIcon(self.parent.round_checked_icon))

			if config.ALLOW_MENUS_TO_CHANGE_SPELLCHECK_SETTINGS: self.settingsMenu.addMenu(self.spellcheckMenu)

	def updateHostmask(self,nick,hostmask):
		if hostmask!=None:
			if nick in self.nicks:
				self.hostmasks[nick] = hostmask
		else:
			if nick in self.hostmasks:
				self.hostmasks.pop(nick)

	def swapHostmask(self,oldnick,newnick):
		if oldnick in self.hostmasks:
			hm =  self.hostmasks[oldnick]
			self.hostmasks.pop(oldnick)
			self.hostmasks[newnick] = hm

	def hasNickHostmask(self,nick):
		if nick in self.hostmasks: return True
		return False

	def hideTopic(self):
		self.banlist_menu.hide()
		self.channel_menu.hide()
		self.channel_mode_display.hide()
		self.topic.hide()
		self.channel_users_display.hide()

	def showTopic(self):
		if config.SHOW_BANLIST_MENU:
			if len(self.banlist)>0: self.banlist_menu.show()
		else:
			self.banlist_menu.hide()
		if config.SHOW_CHANNEL_MENU:
			if self.is_privileged():
				self.channel_menu.show()
		else:
			self.channel_menu.hide()
		self.channel_mode_display.show()
		if config.SHOW_CHANNEL_NAME_AND_MODES:
			self.channel_mode_display.show()
		else:
			self.channel_mode_display.hide()
		self.topic.show()
		if config.SHOW_USER_COUNT_DISPLAY:
			self.channel_users_display.show()
		else:
			self.channel_users_display.hide()

	def tickUptime(self,uptime):

		if config.SHOW_CHANNEL_UPTIME:
			if hasattr(self,"channelUptime"): 
				if not self.channelUptime.isVisible(): self.channelUptime.show()
		else:
			if hasattr(self,"channelUptime"):
				if self.channelUptime.isVisible(): self.channelUptime.hide()

		if config.SHOW_CONNECTION_UPTIME:
			if hasattr(self,"serverUptime"):
				if not self.serverUptime.isVisible(): self.serverUptime.show()
		else:
			if hasattr(self,"serverUptime"):
				if self.serverUptime.isVisible(): self.serverUptime.hide()

		if config.SHOW_CONNECTION_UPTIME:
			if hasattr(self,"statusServerUptime"):
				if not self.statusServerUptime.isVisible(): self.statusServerUptime.show()
		else:
			if hasattr(self,"statusServerUptime"):
				if self.statusServerUptime.isVisible(): self.statusServerUptime.hide()

		if config.SHOW_STATUS_BAR_ON_SERVER_WINDOWS:
			if hasattr(self,"serverUptime"):
				if self.serverUptime.isVisible(): self.serverUptime.hide()

		if self.window_type==SERVER_WINDOW:
			self.uptime = uptime
			self.serverUptime.setText("<b>"+prettyUptime(self.uptime)+"</b>")
			self.statusServerUptime.setText("<small>"+prettyUptime(self.uptime)+"</small>")
		else:
			self.uptime = self.uptime + 1
			if self.window_type==CHANNEL_WINDOW:
				self.channelUptime.setText("<small>"+prettyUptime(self.uptime)+"</small>")

			if self.window_type==CHANNEL_WINDOW or self.window_type==PRIVATE_WINDOW:
				# If the date has changed, add a date message to the chat to reflect that
				# But only do that on channel and private chat windows
				cdate = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%A %B %d, %Y')
				if cdate!=self.current_date:
					self.current_date = cdate
					# there's a new date; create a new date separator
					m = Message(DATE_MESSAGE,'',cdate)
					d2 = render.render_message(m,self.style,None,config.STRIP_NICKNAME_PADDING_FROM_DISPLAY)
					self.chat.append(d2)

	def refreshBanMenu(self):
		self.banlist_menu.setMenu(buildBanMenu(self,self.client))

		if len(self.banlist)>0:
			if config.SHOW_BANLIST_MENU: self.banlist_menu.show()
			if not config.SHOW_CHANNEL_TOPIC: self.banlist_menu.hide()
		else:
			self.banlist_menu.hide()

	def refreshChannelMenu(self):
		if hasattr(self,"channel_menu"):
			self.channel_menu.setMenu(self.buildOperatorMenu())
			if config.SHOW_CHANNEL_MENU:
				if not self.is_privileged():
					self.channel_menu.hide()
				else:
					self.channel_menu.show()
			else:
				self.channel_menu.hide()

	def refreshInfoMenu(self):
		self.server_info_menu = buildServerSettingsMenu(self,self.client)
		self.info_button.setMenu(self.server_info_menu)

	def toggleInputMenu(self):
		if config.SHOW_INPUT_MENU: 
			self.settingsButton.show()
		else:
			self.settingsButton.hide()

	def toggleNickDisplay(self):
		if config.SHOW_USER_INFO_ON_CHAT_WINDOWS:
			if self.window_type!=SERVER_WINDOW:
				if hasattr(self,"name_spacer"): self.name_spacer.show()
				self.nick_display.show()
				self.mode_display.show()
		else:
			if self.window_type!=SERVER_WINDOW:
				if hasattr(self,"name_spacer"): self.name_spacer.hide()
				self.nick_display.hide()
				self.mode_display.hide()

	def clearChat(self):
		self.log = []
		self.rerenderChatLog()

	def rerenderChatLog(self):

		self.chat.clear()
		for line in self.log:

			do_render = True
			if line.sender!='':
				p = line.sender.split("!")
				if len(p)==2:
					nickname = p[0].lower()
					hostmask = p[1].lower()
				else:
					nickname = line.sender.lower()
					hostmask = None

				if line.sender in config.IGNORE_LIST: do_render = False
				if self.is_ignored(nickname,hostmask): do_render = False

			if do_render:
				t = render.render_message(line,self.style,self.client,config.STRIP_NICKNAME_PADDING_FROM_DISPLAY)
				self.chat.append(t)

		self.chat.moveCursor(QTextCursor.End)
		self.input.setFocus()

	def refreshModeDisplay(self):
		if len(self.client.usermodes)==0:
			self.mode_display.setText("")
			self.mode_display.hide()
		else:
			self.mode_display.setText("<small>+"+self.client.usermodes+"</small>")
			if self.window_type!=SERVER_WINDOW:
				if config.SHOW_USER_INFO_ON_CHAT_WINDOWS:
					self.mode_display.show()
		self.updateTitle()
		self.refreshChannelMenu()

		if hasattr(self,"key_icon"):
			if self.name in self.client.channelkeys:
				self.key_icon.show()
				if hasattr(self,"key_value"):
					self.key_value.setText("<small>+k "+self.client.channelkeys[self.name]+"</small>")
					self.key_value.show()
					self.key_spacer.show()
			else:
				self.key_icon.hide()
				if hasattr(self,"key_value"):
					self.key_value.hide()
					self.key_spacer.hide()
		
	def updateTitle(self):

		if self.window_type==SERVER_WINDOW:

			if hasattr(self.client,"hostname"):
				self.name = self.client.hostname

			if hasattr(self.client,"network"):
				if config.SHOW_LINKS_TO_NETWORK_WEBPAGES:
					netlink = get_network_link(self.client.network)
					if netlink!=None:
						self.status_server.setText("<small><b>"+self.client.hostname+"</b> (<a href=\""+netlink+"\">"+self.client.network+"</a>)</small>")
					else:
						self.status_server.setText("<small><b>"+self.client.hostname+"</b> ("+self.client.network+")</small>")
				else:
					self.status_server.setText("<small><b>"+self.client.hostname+"</b> ("+self.client.network+")</small>")
			else:
				self.status_server.setText(f"<small><b>{self.client.hostname}</b></small>")

		if self.window_type==CHANNEL_WINDOW:
			if self.name in self.client.channelmodes:
				if len(self.client.channelmodes[self.name])>0:
					modes = " +"+self.client.channelmodes[self.name]
				else:
					modes = ''
			else:
				modes = ''

			if len(modes)>0:
				self.channel_mode_display.setText("<b>"+self.name+"</b> <small>"+modes+"</small>")
			else:
				self.channel_mode_display.setText("<b>"+self.name+"</b>")
		else:
			self.setWindowTitle(self.name)
			self.parent.buildWindowsMenu()

	def eventFilter(self, source, event):

		# Name click
		if (event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.nick_display):
			info = NewNickDialog(self.client.nickname,self)
			if info!=None:
				self.client.setNick(info)
				return True

		# User List Menu
		if (event.type() == QtCore.QEvent.ContextMenu and source is self.userlist):

			item = source.itemAt(event.pos())
			if item is None: return True

			user = item.text()

			user_nick = ''
			user_hostmask = None
			user_is_op = False
			user_is_voiced = False
			user_is_admin = False
			user_is_owner = False
			user_is_halfop = False
			user_is_protected = False

			raw_user = None

			for u in self.users:
				p = u.split('!')
				if len(p)==2:
					nick = p[0]
					hostmask = p[1]
				else:
					nick = u
					hostmask = None

				if '@' in nick:
					is_op = True
					nick = nick.replace('@','')
				else:
					is_op = False
				if '+' in nick:
					is_voiced = True
					nick = nick.replace('+','')
				else:
					is_voiced = False
				if '~' in nick:
					is_owner = True
					nick = nick.replace('~','')
				else:
					is_owner = False
				if '&' in nick:
					is_admin = True
					nick = nick.replace('&','')
				else:
					is_admin = False
				if '%' in nick:
					is_halfop = True
					nick = nick.replace('%','')
				else:
					is_halfop = False
				if '!' in nick:
					is_protected = True
					nick = nick.replace('!','')
				else:
					is_protected = False
				if nick==user:
					raw_user = u
					user_nick = nick
					if hostmask:
						user_hostmask = hostmask
					else:
						if nick in self.hostmasks:
							user_hostmask = self.hostmasks[nick]
					user_is_op = is_op
					user_is_voiced = is_voiced
					user_is_owner = is_owner
					user_is_admin = is_admin
					user_is_halfop = is_halfop
					user_is_protected = is_protected
					break

			if len(user_nick.strip())==0:
				if '@' in user:
					user_is_op = True
					user = user.replace('@','')
				if '+' in user:
					user_is_voiced = True
					user = user.replace('+','')
				if '~' in user:
					user_is_owner = True
					user = user.replace('~','')
				if '&' in user:
					user_is_admin = True
					user = user.replace('&','')
				if '%' in user:
					user_is_halfop = True
					user = user.replace('%','')
				if '!' in user:
					user_is_protected = True
					user = user.replace('!','')
				user_nick = user

				user_nick = self.clean_nick(user_nick)

				if user_nick in self.hostmasks:
					user_hostmask = self.hostmasks[user_nick]

			if user_nick==self.client.nickname:
				this_is_me = True
			else:
				this_is_me = False

			menu = QMenu(self)

			if user_hostmask:
				max_length = 25
				if len(user_hostmask)>max_length:
					if len(user_hostmask)>=max_length+3:
						offset = max_length-3
					elif len(user_hostmask)==max_length+2:
						offset = max_length-2
					elif len(user_hostmask)==max_length+1:
						offset = max_length-1
					else:
						offset = max_length
					display_hostmask = user_hostmask[0:offset]+"..."
				else:
					display_hostmask = user_hostmask

			statusLayout = QHBoxLayout()
			if user_is_op:
				ICON = OP_USER
				OTHER_TEXT = "Channel operator"
			elif user_is_voiced:
				ICON = VOICE_USER
				OTHER_TEXT = "Voiced user"
			elif user_is_owner:
				ICON = OWNER_USER
				OTHER_TEXT = "Channel owner"
			elif user_is_admin:
				ICON = ADMIN_USER
				OTHER_TEXT = "Channel admin"
			elif user_is_halfop:
				ICON = HALFOP_USER
				OTHER_TEXT = "Channel half-operator"
			elif user_is_protected:
				ICON = PROTECTED_USER
				OTHER_TEXT = "Protected user"
			else:
				ICON = PRIVATE_MENU_ICON
				OTHER_TEXT = "Normal user"
			statusLayout.addStretch()

			is_hidden = False
			if user_hostmask:
				is_hidden = self.is_ignored(user_nick,user_hostmask)
			else:
				is_hidden = self.is_ignored(user_nick,None)

			if user_nick==self.client.nickname:
				
				if config.SHOW_AWAY_STATUS_IN_USERLISTS:
					if self.client.is_away:
						entry = ExtendedMenuItemNoAction(self,ICON,user_nick,"You are away",CUSTOM_MENU_ICON_SIZE)
						menu.addAction(entry)

						e = noSpacePlainTextAction(self,f"<small><i>{self.client.away_msg}</i></small>")
						menu.addAction(e)
					else:
						entry = ExtendedMenuItemNoAction(self,ICON,user_nick,"This is you!",CUSTOM_MENU_ICON_SIZE)
						menu.addAction(entry)
				else:
					entry = ExtendedMenuItemNoAction(self,ICON,user_nick,"This is you!",CUSTOM_MENU_ICON_SIZE)
					menu.addAction(entry)

			else:
				if user_hostmask:
					entry = ExtendedMenuItemNoAction(self,ICON,user_nick,display_hostmask,CUSTOM_MENU_ICON_SIZE)
					menu.addAction(entry)

					if is_hidden:
						e = noSpacePlainTextAction(self,f"<small><i><center>User is ignored</center></i></small>")
						menu.addAction(e)

				else:
					entry = ExtendedMenuItemNoAction(self,ICON,user_nick,OTHER_TEXT,CUSTOM_MENU_ICON_SIZE)
					menu.addAction(entry)

					if is_hidden:
						e = noSpacePlainTextAction(self,f"<small><i><center>User is ignored</center></i></small>")
						menu.addAction(e)

			if config.SHOW_AWAY_STATUS_IN_USERLISTS:
				if user_nick in self.away:
					away_msg = self.away[user_nick]

					e = noSpacePlainTextAction(self,f"<small><i>{away_msg}</i></small>")
					menu.addAction(e)

			menu.addSeparator()

			if self.operator:

				opMenu = menu.addMenu(QIcon(OP_USER),"Operator actions")

				opMenu.addSeparator()

				if user_is_op: actDeop = opMenu.addAction(QIcon(MINUS_ICON),"Take operator status")
				if not user_is_op: actOp = opMenu.addAction(QIcon(PLUS_ICON),"Give operator status")

				if not user_is_op:
					if user_is_voiced: actDevoice = opMenu.addAction(QIcon(MINUS_ICON),"Take voiced status")
					if not user_is_voiced: actVoice = opMenu.addAction(QIcon(PLUS_ICON),"Give voiced status")

				opMenu.addSeparator()

				actKick = opMenu.addAction(QIcon(KICK_ICON),"Kick "+user_nick)
				actBan = opMenu.addAction(QIcon(BAN_ICON),"Ban "+user_nick)
				actKickBan = opMenu.addAction(QIcon(BAN_ICON),"Kick && Ban "+user_nick)

			actWhois = menu.addAction(QIcon(WHOIS_ICON),"WHOIS")

			if is_hidden:
				actIgnore = menu.addAction(QIcon(SHOW_ICON),"Unignore user")
			else:
				actIgnore = menu.addAction(QIcon(HIDE_ICON),"Ignore user")

			actPriv = menu.addAction(QIcon(PRIVATE_ICON),"Open private chat")

			clipMenu = menu.addMenu(QIcon(CLIPBOARD_ICON),"Copy to clipboard")
			actCopyNick = clipMenu.addAction(QIcon(PRIVATE_ICON),"User's nickname")
			if user_hostmask: actHostmask = clipMenu.addAction(QIcon(PRIVATE_ICON),"User's hostmask")

			action = menu.exec_(self.userlist.mapToGlobal(event.pos()))

			if action == actPriv:
				self.parent.openPrivate(self.client,user)
				return True

			if action == actIgnore:
				if is_hidden:
					if user_hostmask:
						if user_hostmask.lower() in config.IGNORE_LIST:
							config.IGNORE_LIST.remove(user_hostmask.lower())
					if user_nick.lower() in config.IGNORE_LIST:
						config.IGNORE_LIST.remove(user_nick.lower())
					config.save_settings(config.CONFIG_FILE)
					self.parent.buildSettingsMenu()
					self.parent.reRenderAll(True)
					self.parent.rerenderUserlists()
					return True
				else:
					if user_hostmask:
						config.IGNORE_LIST.append(user_hostmask.lower())
					else:
						config.IGNORE_LIST.append(user_nick.lower())
					config.save_settings(config.CONFIG_FILE)
					self.parent.buildSettingsMenu()
					self.parent.reRenderAll(True)
					self.parent.rerenderUserlists()
					return True

			if action == actWhois:
				self.client.sendLine("WHOIS "+user_nick)
				return True

			if action == actCopyNick:
				cb = QApplication.clipboard()
				cb.clear(mode=cb.Clipboard)
				cb.setText(f"{user_nick}", mode=cb.Clipboard)
				return True

			if user_hostmask:
				if action == actHostmask:
					cb = QApplication.clipboard()
					cb.clear(mode=cb.Clipboard)
					cb.setText(f"{user_hostmask}", mode=cb.Clipboard)
					return True

			if self.operator:

				if action == actKick:
					self.client.kick(self.name,user_nick)
					return True

				if action == actBan:
					if user_hostmask:
						h = user_hostmask.split('@')[1]
						banmask = "*@"+h
					else:
						banmask = user_nick
					self.client.mode(self.name,True,"b",None,None,banmask)
					return True

				if action == actKickBan:
					if user_hostmask:
						h = user_hostmask.split('@')[1]
						banmask = "*@"+h
					else:
						banmask = user_nick
					self.client.mode(self.name,True,"b",None,None,banmask)
					self.client.kick(self.name,user_nick)
					return True

				if user_is_op:
					if action == actDeop:
						self.client.mode(self.name,False,"o",None,user_nick)
						return True

				if not user_is_op:
					if user_is_voiced:
						if action == actDevoice:
							self.client.mode(self.name,False,"v",None,user_nick)
							return True

				if not user_is_op:
					if action == actOp:
						self.client.mode(self.name,True,"o",None,user_nick)
						return True

				if not user_is_op:
					if not user_is_voiced:
						if action == actVoice:
							self.client.mode(self.name,True,"v",None,user_nick)
							return True

			return True

		return super(Window, self).eventFilter(source, event)

	def loadScript(self,directly_execute=False):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Select Script", commands.SCRIPTS_DIRECTORY, f"{APPLICATION_NAME} Script (*.merk);;All Files (*)", options=options)
		if fileName:
			if directly_execute:
				# Function was called from the server toolbar, so
				# load and execute the script directly
				f = open(fileName,"r")
				script = f.read()
				f.close()
				commands.executeScript(self.parent,self,script,fileName)
			else:
				scriptDir = pathlib.Path(commands.SCRIPTS_DIRECTORY)
				configDir = pathlib.Path(config.CONFIG_DIRECTORY)
				fileDir = pathlib.Path(os.path.dirname(fileName))

				if scriptDir.resolve() == fileDir.resolve():
					# Script is in the script directory, no need
					# to keep the path, MERK will find the file
					self.input.setText(f"{config.ISSUE_COMMAND_SYMBOL}script {os.path.basename(fileName)} ")
				elif configDir.resolve() == fileDir.resolve():
					# Script is in the config directory
					self.input.setText(f"{config.ISSUE_COMMAND_SYMBOL}script {os.path.basename(fileName)} ")
				else:
					self.input.setText(f"{config.ISSUE_COMMAND_SYMBOL}script {fileName} ")
				self.input.setFocus()
				self.input.moveCursor(QTextCursor.End)

	def executeScript(self,script,filename=None):
		commands.executeScript(self.parent,self,script,filename)

	def generateStylesheet(self,obj,fore,back):

		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def pressedStyleButton(self):
		if config.SIMPLIFIED_DIALOGS:
			x = SimpleStylerDialog(self.client,self,self.parent)
		else:
			x = StylerDialog(self.client,self,self.parent)
		if x:
			self.applyStyle()

	def applyStyle(self,filename=None):
		if not config.FORCE_DEFAULT_STYLE:
			if filename == None:
				if self.window_type==SERVER_WINDOW:
					self.style = styles.loadStyleServer(self.client)
				else:
					self.style = styles.loadStyle(self.client,self.name)
			else:
				s = styles.loadStyleFile(filename)
				if s:
					self.style = s
				else:
					return False
		else:
			self.style = self.default_style

		# Apply style background and forground colors
		background,foreground = styles.parseBackgroundAndForegroundColor(self.style["all"])

		self.chat.setStyleSheet(self.generateStylesheet('QTextBrowser',foreground,background))

		if not config.DO_NOT_APPLY_STYLE_TO_INPUT_WIDGET:
			self.input.setStyleSheet(self.generateStylesheet('SpellTextEdit',foreground,background))
		else:
			b,f = styles.parseBackgroundAndForegroundColor(self.default_style["all"])
			self.input.setStyleSheet(self.generateStylesheet('SpellTextEdit',f,b))

		if self.window_type==CHANNEL_WINDOW:
			if not config.DO_NOT_APPLY_STYLE_TO_USERLIST:
				self.userlist.setStyleSheet(self.generateStylesheet('QListWidget',foreground,background))
			else:
				b,f = styles.parseBackgroundAndForegroundColor(self.default_style["all"])
				self.userlist.setStyleSheet(self.generateStylesheet('QListWidget',f,b))
				self.writeUserlist(self.full_nicks)


		self.rerenderChatLog()
		self.rerenderUserlist()

	def rerenderUserlist(self):
		self.writeUserlist(self.users)

	def change_to_away_display(self,w):
		if config.SHOW_AWAY_STATUS_IN_USERLISTS:
			font = QFont()
			font.setBold(False)
			w.setFont(font)

			background,foreground = styles.parseBackgroundAndForegroundColor(self.style["all"])
			c = QColor(foreground)
			if test_if_foreground_is_light(self.style["all"]):
				change = c.darker(150)
			else:
				change = c.lighter(150)
			w.setForeground(QBrush(QColor(change)))


	def change_to_back_display(self,w):
		if config.SHOW_AWAY_STATUS_IN_USERLISTS:
			font = QFont()
			font.setBold(True)
			w.setFont(font)

			background,foreground = styles.parseBackgroundAndForegroundColor(self.style["all"])
			w.setForeground(QBrush(QColor(foreground)))

	def got_away(self,username,message):

		p = username.split('!')
		if len(p)==2:
			nickname = p[0]
			hostmask = p[1]
		else:
			nickname = username

		self.away[nickname] = message

		for i in range(self.userlist.count()):
			item = self.userlist.item(i)
			
			target = item.text()
			target = target.replace('@','')
			target = target.replace('+','')
			target = target.replace('~','')
			target = target.replace('&','')
			target = target.replace('%','')
			target = target.replace('!','')

			if target==nickname:
				self.change_to_away_display(item)
				self.userlist.update()

	def got_back(self,username):

		p = username.split('!')
		if len(p)==2:
			nickname = p[0]
			hostmask = p[1]
		else:
			nickname = username

		if nickname in self.away:
			del self.away[nickname]

		for i in range(self.userlist.count()):
			item = self.userlist.item(i)
			
			target = item.text()
			target = target.replace('@','')
			target = target.replace('+','')
			target = target.replace('~','')
			target = target.replace('&','')
			target = target.replace('%','')
			target = target.replace('!','')

			if target==nickname:
				self.change_to_back_display(item)
				self.userlist.update()

	def clean_nick(self,nick):
		nick = nick.replace('@','')
		nick = nick.replace('+','')
		nick = nick.replace('~','')
		nick = nick.replace('&','')
		nick = nick.replace('%','')
		nick = nick.replace('!','')
		return nick

	def is_ignored(self,nick,hostmask):

		if nick in self.hostmasks:
			for i in config.IGNORE_LIST:
				if i.lower()==self.hostmasks[nick].lower(): return True

		for i in config.IGNORE_LIST:
			if i.lower()==nick.lower(): return True

		if hostmask!=None:
			for i in config.IGNORE_LIST:
				if i.lower()==hostmask.lower(): return True

		return False

	def change_to_ignore_display(self,w):
		if config.SHOW_IGNORE_STATUS_IN_USERLISTS:
			font = QFont()
			font.setBold(False)
			font.setStrikeOut(True)
			w.setFont(font)

	def writeUserlist(self,users):

		if not hasattr(self,"userlist"): return	

		self.users = []
		self.operator = False
		self.voiced = False
		self.owner = False
		self.admin = False
		self.halfop = False
		self.protected = False

		self.userlist.clear()

		self.user_count = 0
		self.full_nicks = users

		owners = []
		admins = []
		ops = []
		halfops = []
		voiced = []
		normal = []
		protected = []
		ignored = []

		for u in users:
			if len(u)<1: continue
			self.users.append(u)
			p = u.split("!")
			if len(p)==2:
				nickname = p[0]
				hostmask = p[1]
				self.hostmasks[self.clean_nick(nickname)] = hostmask
			else:
				nickname = u
				hostmask = None

			if self.is_ignored(self.clean_nick(nickname),hostmask): ignored.append(self.clean_nick(nickname))

			self.user_count = self.user_count + 1

			if '@' in nickname:
				ops.append(nickname.replace('@',''))
				if nickname.replace('@','')==self.client.nickname: self.operator = True
			elif '+' in nickname:
				voiced.append(nickname.replace('+',''))
				if nickname.replace('+','')==self.client.nickname: self.voiced = True
			elif '~' in nickname:
				owners.append(nickname.replace('~',''))
				if nickname.replace('~','')==self.client.nickname: self.owner = True
			elif '&' in nickname:
				admins.append(nickname.replace('&',''))
				if nickname.replace('&','')==self.client.nickname: self.admin = True
			elif '%' in nickname:
				halfops.append(nickname.replace('%',''))
				if nickname.replace('%','')==self.client.nickname: self.halfop = True
			elif '!' in nickname:
				protected.append(nickname.replace('!',''))
				if nickname.replace('!','')==self.client.nickname: self.protected = True
			else:
				normal.append(nickname)

		if self.user_count==1:
			self.channel_users_display.setText("<b><small>1 user</small></b>")
		else:
			self.channel_users_display.setText(f"<b><small>{self.user_count} users</small></b>")

		# Store a list of the nicks in this channel
		self.nicks = owners + admins + halfops + ops + voiced + normal

		# Alphabetize
		owners.sort(key=str.lower)
		admins.sort(key=str.lower)
		ops.sort(key=str.lower)
		halfops.sort(key=str.lower)
		voiced.sort(key=str.lower)
		normal.sort(key=str.lower)
		protected.sort(key=str.lower)

		# Add owners
		for u in owners:
			ui = QListWidgetItem()
			if config.PLAIN_USER_LISTS:
				ui.setText('~ '+u)
			else:
				ui.setIcon(QIcon(OWNER_USER))
				ui.setText(u)

			if config.USERLIST_ITEMS_NON_SELECTABLE:
				ui.setFlags(ui.flags() & ~Qt.ItemIsSelectable)
				
			self.change_to_back_display(ui)

			if u==self.client.nickname:
				if self.client.is_away:
					self.change_to_away_display(ui)

			if u in self.away:
				self.change_to_away_display(ui)

			if u in ignored: self.change_to_ignore_display(ui)

			self.userlist.addItem(ui)

		# Add admins
		for u in admins:
			ui = QListWidgetItem()
			if config.PLAIN_USER_LISTS:
				ui.setText('& '+u)
			else:
				ui.setIcon(QIcon(ADMIN_USER))
				ui.setText(u)

			if config.USERLIST_ITEMS_NON_SELECTABLE:
				ui.setFlags(ui.flags() & ~Qt.ItemIsSelectable)
				
			self.change_to_back_display(ui)

			if u==self.client.nickname:
				if self.client.is_away:
					self.change_to_away_display(ui)

			if u in self.away:
				self.change_to_away_display(ui)

			if u in ignored: self.change_to_ignore_display(ui)

			self.userlist.addItem(ui)

		# Add halfops
		for u in halfops:
			ui = QListWidgetItem()
			if config.PLAIN_USER_LISTS:
				ui.setText('% '+u)
			else:
				ui.setIcon(QIcon(HALFOP_USER))
				ui.setText(u)

			if config.USERLIST_ITEMS_NON_SELECTABLE:
				ui.setFlags(ui.flags() & ~Qt.ItemIsSelectable)
				
			self.change_to_back_display(ui)

			if u==self.client.nickname:
				if self.client.is_away:
					self.change_to_away_display(ui)

			if u in self.away:
				self.change_to_away_display(ui)

			if u in ignored: self.change_to_ignore_display(ui)

			self.userlist.addItem(ui)

		# Add ops
		for u in ops:
			ui = QListWidgetItem()
			if config.PLAIN_USER_LISTS:
				ui.setText('@ '+u)
			else:
				ui.setIcon(QIcon(OP_USER))
				ui.setText(u)

			if config.USERLIST_ITEMS_NON_SELECTABLE:
				ui.setFlags(ui.flags() & ~Qt.ItemIsSelectable)
				
			self.change_to_back_display(ui)

			if u==self.client.nickname:
				if self.client.is_away:
					self.change_to_away_display(ui)

			if u in self.away:
				self.change_to_away_display(ui)

			if u in ignored: self.change_to_ignore_display(ui)

			self.userlist.addItem(ui)

		# Add voiced
		for u in voiced:
			ui = QListWidgetItem()
			if config.PLAIN_USER_LISTS:
				ui.setText('+ '+u)
			else:
				ui.setIcon(QIcon(VOICE_USER))
				ui.setText(u)

			if config.USERLIST_ITEMS_NON_SELECTABLE:
				ui.setFlags(ui.flags() & ~Qt.ItemIsSelectable)
				
			self.change_to_back_display(ui)

			if u==self.client.nickname:
				if self.client.is_away:
					self.change_to_away_display(ui)

			if u in self.away:
				self.change_to_away_display(ui)

			if u in ignored: self.change_to_ignore_display(ui)

			self.userlist.addItem(ui)

		# Add protected
		for u in protected:
			ui = QListWidgetItem()
			if config.PLAIN_USER_LISTS:
				ui.setText('! '+u)
			else:
				ui.setIcon(QIcon(PROTECTED_USER))
				ui.setText(u)

			if config.USERLIST_ITEMS_NON_SELECTABLE:
				ui.setFlags(ui.flags() & ~Qt.ItemIsSelectable)

			self.change_to_back_display(ui)

			if u==self.client.nickname:
				if self.client.is_away:
					self.change_to_away_display(ui)

			if u in self.away:
				self.change_to_away_display(ui)

			if u in ignored: self.change_to_ignore_display(ui)

			self.userlist.addItem(ui)

		# Add normal
		for u in normal:
			ui = QListWidgetItem()
			if config.PLAIN_USER_LISTS:
				ui.setText('  '+u)
			else:
				ui.setIcon(QIcon(NORMAL_USER))
				ui.setText(u)

			if config.USERLIST_ITEMS_NON_SELECTABLE:
				ui.setFlags(ui.flags() & ~Qt.ItemIsSelectable)
			
			self.change_to_back_display(ui)

			if u==self.client.nickname:
				if self.client.is_away:
					self.change_to_away_display(ui)

			if u in self.away:
				self.change_to_away_display(ui)

			if u in ignored: self.change_to_ignore_display(ui)

			self.userlist.addItem(ui)

		self.userlist.update()

		self.op_icon.hide()
		self.voice_icon.hide()
		self.owner_icon.hide()
		self.admin_icon.hide()
		self.halfop_icon.hide()
		self.protected_icon.hide()

		if config.SHOW_USER_INFO_ON_CHAT_WINDOWS:
			need_spacer = True
			if self.operator:
				self.op_icon.show()
				need_spacer = False
			if self.voiced:
				self.voice_icon.show()
				need_spacer = False
			if self.owner:
				self.owner_icon.show()
				need_spacer = False
			if self.admin:
				self.admin_icon.show()
				need_spacer = False
			if self.halfop:
				self.halfop_icon.show()
				need_spacer = False
			if self.protected:
				self.protected_icon.show()
				need_spacer = False

			if need_spacer:
				self.name_spacer.show()
			else:
				self.name_spacer.hide()

		self.refreshChannelMenu()

		

	def disconnect(self):

		no_hostname = False
		if not hasattr(self.client,"hostname"): no_hostname = True
		if not self.client.hostname: no_hostname = True

		do_disconnect = self.parent.askDisconnect(self.client)

		if do_disconnect:
			if no_hostname:
				self.parent.quitting[self.client.client_id] = 0
				self.client.quit()
				self.parent.hideServerWindow(self.client)
			else:
				self.parent.quitting[self.client.client_id] = 0
				if config.ENABLE_EMOJI_SHORTCODES:
					msg = emoji.emojize(config.DEFAULT_QUIT_MESSAGE,language=config.EMOJI_LANGUAGE)
				else:
					msg = config.DEFAULT_QUIT_MESSAGE
				self.client.quit(msg)

	def changeNick(self):
		newnick = NewNickDialog(self.client.nickname,self.parent)
		if newnick:
			self.client.setNick(newnick)

	def changeAway(self):
		if self.client.is_away:
			self.away_button.setToolTip("Set status to \"away\"")
			self.away_button.setIcon(QIcon(GO_AWAY_ICON))
			self.client.back()
		else:
			if config.PROMPT_FOR_AWAY_MESSAGE:
				msg = AwayDialog(self)
				if msg:
					self.away_button.setToolTip("Set status to \"back\"")
					self.away_button.setIcon(QIcon(GO_BACK_ICON))
					if config.ENABLE_EMOJI_SHORTCODES:
						msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					self.client.away(msg)
					self.client.away_msg = msg
			else:
				self.away_button.setToolTip("Set status to \"back\"")
				self.away_button.setIcon(QIcon(GO_BACK_ICON))
				if config.ENABLE_EMOJI_SHORTCODES:
					msg = emoji.emojize(config.DEFAULT_AWAY_MESSAGE,language=config.EMOJI_LANGUAGE)
				else:
					msg = config.DEFAULT_AWAY_MESSAGE
				self.client.away(msg)
				self.client.away_msg = msg

	def joinChannel(self):
		channel_info = JoinChannelDialog(self.parent)
		if channel_info:
			if channel_info[0][:1]=='#' or channel_info[0][:1]=='&' or channel_info[0][:1]=='!' or channel_info[0][:1]=='+':
				self.client.join(channel_info[0],channel_info[1])
			else:
				self.client.join('#'+channel_info[0],channel_info[1])

	def refreshNickDisplay(self):
		if config.SHOW_AWAY_STATUS_IN_NICK_DISPLAY:
			if self.client.is_away:
				self.nick_display.setText(self.client.nickname+" ")
			else:
				self.nick_display.setText("<b>"+self.client.nickname+"&nbsp;</b>")
		else:
			self.nick_display.setText("<b>"+self.client.nickname+"&nbsp;</b>")

	def writeText(self,message,write_to_log=True):

		if self.client.client_id in self.parent.quitting: return

		try:
			if type(message)==type(str()):
				self.chat.append(message)
			else:

				do_render = True
				if message.sender!='':
					p = message.sender.split("!")
					if len(p)==2:
						nickname = p[0].lower()
						hostmask = p[1].lower()
					else:
						nickname = message.sender.lower()
						hostmask = None
				
					if message.sender in config.IGNORE_LIST: do_render = False
					if self.is_ignored(nickname,hostmask): do_render = False

				# Save entered text to the current log
				self.log.append(message)

				# Save entered text to the new log for saving
				if write_to_log: self.new_log.append(message)

				if do_render:
					t = render.render_message(message,self.style,self.client,config.STRIP_NICKNAME_PADDING_FROM_DISPLAY)
					self.chat.append(t)

			self.moveChatToBottom(config.ALWAYS_SCROLL_TO_BOTTOM)
		except:
			pass

	def closeEvent(self, event):

		# This will be true if the window is closed
		# with the window bar "X" button or if Alt-F4
		# is pressed
		if event.spontaneous():
			pass

		if self.force_close:
			# Let the parent know that this subwindow
			# has been closed by the user
			self.parent.closeSubWindow(self.subwindow_id)

			event.accept()
			self.close()
			return

		if self.client.client_id in self.parent.quitting:
			if self.window_type==SERVER_WINDOW:
				self.parent.closeSubWindow(self.subwindow_id)
				event.accept()
				self.close()
				return

		# Server windows are never closed unless
		# the server has been disconnected; they
		# are only hidden
		if self.window_type==SERVER_WINDOW:
			if config.CLOSING_SERVER_WINDOW_DISCONNECTS:
				self.disconnect()
				event.ignore()
			else:
				event.ignore()
				self.parent.hideSubWindow(self.subwindow_id)
				self.parent.MDI.activateNextSubWindow()
			return

		# If this is a channel window, sent a part command
		if self.window_type==CHANNEL_WINDOW:
			if config.ENABLE_EMOJI_SHORTCODES:
				msg = emoji.emojize(config.DEFAULT_QUIT_MESSAGE,language=config.EMOJI_LANGUAGE)
			else:
				msg = config.DEFAULT_QUIT_MESSAGE
			self.client.leave(self.name,msg)

		save_logs = True

		if self.window_type==CHANNEL_WINDOW:
			if config.SAVE_CHANNEL_LOGS:
				save_logs=True
			else:
				save_logs=False

		if self.window_type==PRIVATE_WINDOW:
			if config.SAVE_PRIVATE_LOGS:
				save_logs=True
			else:
				save_logs=False

		# Save logs
		if self.window_type==CHANNEL_WINDOW or self.window_type==PRIVATE_WINDOW:
			if save_logs:
				logs.saveLog(self.client.network,self.name,self.new_log,logs.LOG_DIRECTORY)
				self.parent.buildToolsMenu()


		# Let the parent know that this subwindow
		# has been closed by the user
		self.parent.closeSubWindow(self.subwindow_id)

		event.accept()
		self.close()

	def newLogInterval(self):
		self.dosave.stop()
		self.dosave.start(config.LOG_SAVE_INTERVAL)

	def saveLogs(self):
		if config.DO_INTERMITTENT_LOG_SAVES:
			save_logs = True

			if self.window_type==CHANNEL_WINDOW:
				if config.SAVE_CHANNEL_LOGS:
					save_logs=True
				else:
					save_logs=False

			if self.window_type==PRIVATE_WINDOW:
				if config.SAVE_PRIVATE_LOGS:
					save_logs=True
				else:
					save_logs=False

			# Save logs
			if self.window_type==CHANNEL_WINDOW or self.window_type==PRIVATE_WINDOW:
				if save_logs:
					if len(self.new_log)>0:
						logs.saveLog(self.client.network,self.name,self.new_log,logs.LOG_DIRECTORY)
						self.new_log = []
					self.parent.buildToolsMenu()

		self.dosave.start(config.LOG_SAVE_INTERVAL)

	def menuSaveLogs(self):
		# Save logs
		if self.window_type==CHANNEL_WINDOW or self.window_type==PRIVATE_WINDOW:
			options = QFileDialog.Options()
			options |= QFileDialog.DontUseNativeDialog
			fileName, _ = QFileDialog.getSaveFileName(self,"Save log as...","",f"{APPLICATION_NAME} Log (*.json);;All Files (*)", options=options)
			if fileName:
				_, file_extension = os.path.splitext(fileName)
				if file_extension=='':
					efl = len('json')+1
					if fileName[-efl:].lower()!=".json": fileName = fileName+".json"
				logs.saveLogFile(self.client.network,self.name,self.new_log,logs.LOG_DIRECTORY,fileName)

	def menuSetLanguage(self,language):
		self.changeSpellcheckLanguage(language)

		self.languageEnglish.setIcon(QIcon(self.parent.round_unchecked_icon))
		self.languageFrench.setIcon(QIcon(self.parent.round_unchecked_icon))
		self.languageSpanish.setIcon(QIcon(self.parent.round_unchecked_icon))
		self.languageGerman.setIcon(QIcon(self.parent.round_unchecked_icon))
		self.languageDutch.setIcon(QIcon(self.parent.round_unchecked_icon))
		self.languageItalian.setIcon(QIcon(self.parent.round_unchecked_icon))
		self.languageRussian.setIcon(QIcon(self.parent.round_unchecked_icon))
		self.languagePortuguese.setIcon(QIcon(self.parent.round_unchecked_icon))

		if self.language=="en": self.languageEnglish.setIcon(QIcon(self.parent.round_checked_icon))
		if self.language=="fr": self.languageFrench.setIcon(QIcon(self.parent.round_checked_icon))
		if self.language=="es": self.languageSpanish.setIcon(QIcon(self.parent.round_checked_icon))
		if self.language=="de": self.languageGerman.setIcon(QIcon(self.parent.round_checked_icon))
		if self.language=="nl": self.languageDutch.setIcon(QIcon(self.parent.round_checked_icon))
		if self.language=="it": self.languageItalian.setIcon(QIcon(self.parent.round_checked_icon))
		if self.language=="ru": self.languageRussian.setIcon(QIcon(self.parent.round_checked_icon))
		if self.language=="pt": self.languagePortuguese.setIcon(QIcon(self.parent.round_checked_icon))

		if config.ENABLE_SPELLCHECK:
			self.languageEnglish.setEnabled(True)
			self.languageFrench.setEnabled(True)
			self.languageSpanish.setEnabled(True)
			self.languageGerman.setEnabled(True)
			self.languageDutch.setEnabled(True)
			self.languageItalian.setEnabled(True)
			self.languageRussian.setEnabled(True)
			self.languagePortuguese.setEnabled(True)
		else:
			self.languageEnglish.setEnabled(False)
			self.languageFrench.setEnabled(False)
			self.languageSpanish.setEnabled(False)
			self.languageGerman.setEnabled(False)
			self.languageDutch.setEnabled(False)
			self.languageItalian.setEnabled(False)
			self.languageRussian.setEnabled(False)
			self.languagePortuguese.setEnabled(False)

	def linkClicked(self,url):
		if url.host():
			# It's an internet link, so open it
			# in the default browser
			sb = self.chat.verticalScrollBar()
			og_value = sb.value()

			QDesktopServices.openUrl(url)
			self.chat.setSource(QUrl())
			sb.setValue(og_value)
		else:
			# It's a link to a channel, so
			# join the channel
			sb = self.chat.verticalScrollBar()
			og_value = sb.value()
			
			chan = url.toString()
			self.client.join(chan)
			self.chat.setSource(QUrl())
			sb.setValue(og_value)
	

	def handleUserInput(self):
		user_input = self.input.text()
		self.input.setText('')

		# Discard empty input
		if len(user_input.strip())==0: return

		# ================================
		# BEGIN COMMAND HISTORY MANAGEMENT
		# ================================

		if config.ENABLE_COMMAND_INPUT_HISTORY:
			# Remove blank entries from history
			clean = []
			for c in self.history_buffer:
				if len(c.strip())==0: continue
				clean.append(c)
			self.history_buffer = clean

			# Insert current input into the history,
			# right at the beginning
			self.history_buffer.insert(0,user_input)

			# If history is larger than it's supposed to be,
			# remove the last entry
			if len(self.history_buffer)>config.COMMAND_HISTORY_LENGTH:
				self.history_buffer.pop()

			# "Zero" the history buffer pointer
			self.history_buffer_pointer = -1

			# Add a blank entry to the history;
			# this represents (to the user) the current
			# "blank" input
			self.history_buffer.append('')

			# Remove consecutive repeated commands
			self.history_buffer = [self.history_buffer[i] for i in range(len(self.history_buffer)) if (i==0) or self.history_buffer[i] != self.history_buffer[i-1]]

		# ==============================
		# END COMMAND HISTORY MANAGEMENT
		# ==============================

		# Pass the input (and window) to the parent
		# to process input
		if self.window_type!=SERVER_WINDOW:
			self.parent.handleUserInput(self,user_input)
		else:
			self.parent.handleConsoleInput(self,user_input)

		# Move chat display to the bottom
		self.moveChatToBottom(True)

	def changeSpellcheckLanguage(self,lang):

		# Set the new language
		self.language = lang
		self.input.changeLanguage(lang)

		# Rewrite whatever is in the input widget
		# so that it's spellchecked
		cursor = self.input.textCursor()
		user_input = self.input.text()
		self.input.setText('')
		self.input.setText(user_input)
		self.input.moveCursor(cursor.position())

	def resetInput(self):
		cursor = self.input.textCursor()
		user_input = self.input.text()
		self.input.setText('')
		self.input.setText(user_input)
		self.input.moveCursor(cursor.position())

	def handleTopicInput(self):
		entered_topic = self.topic.text()

		self.client.topic(self.name,entered_topic)
		self.input.setFocus()

	def setTopic(self,topic):

		if not hasattr(self,"topic"): return

		self.channel_topic = topic
		self.topic.setText(topic)
		self.topic.setCursorPosition(0)

		w = self.parent.getSubWindow(self.name,self.client)
		a = self.parent.MDI.activeSubWindow()
		if w==a:
			self.parent.merk_subWindowActivated(w)			


	def handleDoubleClick(self,item):
		item.setSelected(False)
		user = item.text()
		user = user.replace('@','')
		user = user.replace('+','')

		if user!=self.client.nickname:
			self.parent.openPrivate(self.client,user)

	def keyPressDown(self):
		if config.ENABLE_COMMAND_INPUT_HISTORY:
			if len(self.history_buffer) <= 1: return
			self.history_buffer_pointer = self.history_buffer_pointer - 1
			if self.history_buffer_pointer < 0:
				self.history_buffer_pointer = len(self.history_buffer) - 1
			self.input.setText(self.history_buffer[self.history_buffer_pointer])
			self.input.moveCursor(QTextCursor.End)

	def keyPressUp(self):
		if config.ENABLE_COMMAND_INPUT_HISTORY:
			if len(self.history_buffer) <= 1: return
			self.history_buffer_pointer = self.history_buffer_pointer + 1
			if len(self.history_buffer) - 1 < self.history_buffer_pointer:
				self.history_buffer_pointer = 0
			self.input.setText(self.history_buffer[self.history_buffer_pointer])
			self.input.moveCursor(QTextCursor.End)

	def moveChatToBottom(self,force=False):

		if force:
			sb = self.chat.verticalScrollBar()
			sb.setValue(sb.maximum())
			self.chat.ensureCursorVisible()

			self.chat.moveCursor(QTextCursor.End)

		fm = QFontMetrics(self.chat.font())
		fheight = fm.height() * 1.5
		sb = self.chat.verticalScrollBar()
		is_at_bottom = False
		if sb.value()>=sb.maximum()-fheight: is_at_bottom = True

		if is_at_bottom:
			sb.setValue(sb.maximum())
			self.chat.ensureCursorVisible()

			self.chat.moveCursor(QTextCursor.End)

	def changeEvent(self, event):
		if event.type() == QEvent.WindowStateChange:
			if event.oldState() and Qt.WindowMinimized:
				# Minimized

				# Make sure the topic displays correctly
				if hasattr(self,"topic"): self.topic.refresh()

			elif event.oldState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
				# Maximized

				# Make sure the topic displays correctly
				if hasattr(self,"topic"): self.topic.refresh()

	def splitterResize(self,position,index):
		# Save the width of the userlist for the resize event
		self.userlist_width = self.userlist.width()

	def resizeScroll(self):
		# Scroll the chat display down to the bottom
		self.moveChatToBottom(True)
		# Delete the timer
		del self.__resize_timer

	def resizeEvent(self, event):

		if config.SCROLL_CHAT_TO_BOTTOM_ON_RESIZE:
			# Set (or reset, if the resize is still on-going)
			# a timer, so that 100 milliseconds after the resize
			# is complete, the chat display is scrolled to the
			# bottom. Calling the scroll function every time
			# the resize event is triggered works, but it
			# slows the app down and makes it "jitter". This
			# speeds it up quite a bit.
			self.__resize_timer = QTimer()
			self.__resize_timer.timeout.connect(self.resizeScroll)
			self.__resize_timer.start(100)

		if self.window_type==CHANNEL_WINDOW:

			# Make sure the topic displays correctly
			self.topic.refresh()
	   
			# QSplitter dynamically changes widget sizes on a resize
			# event; this makes the userlist widget get wider or less wide
			# depending on the new widget size. This code makes sure that
			# the userlist maintains the same width during resize events

			# Calculate the width of the chat display widget
			chat_width = self.width() - self.userlist_width - (CHAT_WINDOW_WIDGET_SPACING * 3)

			# Resize the userlist widget with the width value saved in
			# the splitter resize event
			self.userlist.resize(self.userlist_width,self.userlist.height())

			# Resize the chat display to compensate for the changed
			# userlist size
			self.chat.resize(chat_width,self.chat.height())

			# Move the userlist so it's along side the chat display
			self.userlist.move(chat_width + 3,self.userlist.y())

			# Move the QSplitter handle to match the new widget sizes
			if config.SHOW_USERLIST_ON_LEFT:
				self.horizontalSplitter.setSizes([self.userlist.width(), self.chat.width()])
			else:
				self.horizontalSplitter.setSizes([self.chat.width(), self.userlist.width()])

			if not config.SHOW_USERLIST:
				self.userlist.hide()
				self.userlist_visible = False
				self.buildInputOptionsMenu()

			# Move focus back to the input widget
			self.input.setFocus()

		return super(Window, self).resizeEvent(event)

	def showHideUserlist(self):
		if config.SHOW_USERLIST:
			self.userlist.show()
			self.userlist_visible = True
			self.buildInputOptionsMenu()
		else:
			self.userlist.hide()
			self.userlist_visible = False
			self.buildInputOptionsMenu()
		self.moveChatToBottom(True)

	def swapUserlist(self):
		self.userlist.setParent(None)
		self.chat.setParent(None)
		if config.SHOW_USERLIST_ON_LEFT:
			self.horizontalSplitter.addWidget(self.userlist)
			self.horizontalSplitter.addWidget(self.chat)
		else:
			self.horizontalSplitter.addWidget(self.chat)
			self.horizontalSplitter.addWidget(self.userlist)

		# Calculate the width of the chat display widget
		chat_width = self.width() - self.userlist_width - (CHAT_WINDOW_WIDGET_SPACING * 3)

		# Resize the userlist widget with the width value saved in
		# the splitter resize event
		self.userlist.resize(self.userlist_width,self.userlist.height())

		# Resize the chat display to compensate for the changed
		# userlist size
		self.chat.resize(chat_width,self.chat.height())

		# Move the userlist so it's along side the chat display
		self.userlist.move(chat_width + 3,self.userlist.y())

		# Move the QSplitter handle to match the new widget sizes
		if config.SHOW_USERLIST_ON_LEFT:
			self.horizontalSplitter.setSizes([self.userlist.width(), self.chat.width()])
		else:
			self.horizontalSplitter.setSizes([self.chat.width(), self.userlist.width()])

		self.moveChatToBottom(True)

def buildBanMenu(self,client):

	banlist = self.banlist

	optionsMenu = QMenu("Banned Users")

	e = textSeparator(self,"Banned Users")
	optionsMenu.addAction(e)

	for b in banlist:
		e = plainTextAction(self,f"<b>{b[0]}</b>")
		optionsMenu.addAction(e)

	return optionsMenu

def buildServerSettingsMenu(self,client):

	supports = client.supports # list
	maxchannels = client.maxchannels
	maxnicklen = client.maxnicklen
	channellen = client.channellen
	topiclen = client.topiclen
	kicklen = client.kicklen
	awaylen = client.awaylen
	maxtargets = client.maxtargets
	modes = client.modes
	chanmodes = client.chanmodes #list
	prefix = client.prefix # list
	cmds = client.cmds # list
	casemapping = client.casemapping
	maxmodes = client.maxmodes

	optionsMenu = QMenu("Server information")

	e = textSeparator(self,"Server")
	optionsMenu.addAction(e)

	if client.hostname:
		name = client.hostname
	else:
		name = client.server+":"+str(client.port)

	if hasattr(client,"network"):
		mynet = client.network
	else:
		mynet = "Unknown"

	e = plainTextAction(self,"<b>Host"+f":</b> {name}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Port"+f":</b> {client.port}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Network"+f":</b> {mynet}")
	optionsMenu.addAction(e)

	if client.kwargs["ssl"]:
		e = plainTextAction(self,"<b>Connection:</b> SSL/TLS")
	else:
		e = plainTextAction(self,"<b>Connection:</b> TCP/IP")
	optionsMenu.addAction(e)

	if client.server_user_count==0:
		e = plainTextAction(self,"<b>Users"+f":</b> Unknown")
	else:
		e = plainTextAction(self,"<b>Users"+f":</b> {client.server_user_count:,}")
	optionsMenu.addAction(e)

	if client.server_op_count==0:
		e = plainTextAction(self,"<b>Operators"+f":</b> Unknown")
	else:
		e = plainTextAction(self,"<b>Operators"+f":</b> {client.server_op_count:,}")
	optionsMenu.addAction(e)

	if client.actual_server_channel_count==0:
		if client.server_channel_count==0:
			e = plainTextAction(self,"<b>Channels"+f":</b> Unknown")
		else:
			e = plainTextAction(self,"<b>Channels"+f":</b> {client.server_channel_count:,}")
		optionsMenu.addAction(e)
	else:
		diff = client.actual_server_channel_count - client.server_channel_count
		if client.server_channel_count==0:
			e = plainTextAction(self,"<b>Channels"+f":</b> {client.actual_server_channel_count:,}")
		else:
			e = plainTextAction(self,"<b>Channels"+f":</b> {client.server_channel_count:,} ({diff:,} hidden)")
		optionsMenu.addAction(e)

	e = textSeparator(self,"Limits")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum channels"+f":</b> {maxchannels}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum nickname length"+f":</b> {maxnicklen}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum channel length"+f":</b> {channellen}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum topic length"+f":</b> {topiclen}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum kick length"+f":</b> {kicklen}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum away length"+f":</b> {awaylen}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum message targets"+f":</b> {maxtargets}")
	optionsMenu.addAction(e)

	e = plainTextAction(self,"<b>Maximum modes per user"+f":</b> {modes}")
	optionsMenu.addAction(e)

	e = textSeparator(self,"Miscellaneous")
	optionsMenu.addAction(e)

	if len(maxmodes)>0:
		maxmodesmenu = QMenu("Maximum modes",self)
		for c in maxmodes:
			e = QAction(F"{c[0]}: {c[1]}", self) 
			maxmodesmenu.addAction(e)
		optionsMenu.addMenu(maxmodesmenu)

	if len(cmds)>0:
		cmdmenu = QMenu("Commands",self)
		for c in cmds:
			e = QAction(F"{c}", self) 
			cmdmenu.addAction(e)
		optionsMenu.addMenu(cmdmenu)

	if len(supports)>0:
		supportsmenu = QMenu("Supports",self)
		for c in supports:
			e = QAction(F"{c}", self) 
			supportsmenu.addAction(e)
		optionsMenu.addMenu(supportsmenu)

	if len(chanmodes)>0:
		chanmodemenu = QMenu("Channel modes",self)
		ct = 0
		for c in chanmodes:
			if ct==0:
				ctype = "A"
			elif ct==1:
				ctype = "B"
			elif ct==2:
				ctype = "C"
			elif ct==3:
				ctype = "D"
			e = QAction(F"{ctype}: {c}", self) 
			chanmodemenu.addAction(e)
			ct = ct + 1
		optionsMenu.addMenu(chanmodemenu)

	if len(prefix)>0:
		prefixmenu = QMenu("Status prefixes",self)
		for c in prefix:
			m = c[0]
			s = c[1]
			if s=="&": s="&&"
			e = QAction(F"{m}: {s}", self)
			if m=="o": e.setIcon(QIcon(OP_USER))
			if m=="v": e.setIcon(QIcon(VOICE_USER))
			if m=="a": e.setIcon(QIcon(ADMIN_USER))
			if m=="q": e.setIcon(QIcon(OWNER_USER))
			if m=="h": e.setIcon(QIcon(HALFOP_USER))
			if m=="Y": e.setIcon(QIcon(PROTECTED_USER))
			prefixmenu.addAction(e)
		optionsMenu.addMenu(prefixmenu)

	return optionsMenu

class TopicEdit(QLineEdit):
	def __init__(self, parent=None):
		super(QLineEdit, self).__init__(parent)
		self.readyToEdit = True
		self.parent = parent
		self.is_enabled = True

		if config.CHANNEL_TOPIC_BOLD:
			font = QFont()
			font.setBold(True)
			self.setFont(font)

	def refresh(self):
		self.setText(self.parent.channel_topic)

	def setText(self,text,elide=True):
		if elide:
			metrics = QFontMetrics(self.font())
			elided  = metrics.elidedText(text, Qt.ElideRight, self.width())
			QLineEdit.setText(self,elided)
			if len(elided)!=len(text):
				self.setToolTip(text)
			else:
				self.setToolTip('')
		else:
			QLineEdit.setText(self,text)

		# Handle window title
		if config.SHOW_CHANNEL_TOPIC_IN_WINDOW_TITLE:
			if len(text)>0:
				self.parent.setWindowTitle(self.parent.name+" - "+text)
			else:
				self.parent.setWindowTitle(self.parent.name)
		else:
			self.parent.setWindowTitle(self.parent.name)

	def mousePressEvent(self, e, Parent=None):
		super(QLineEdit, self).mousePressEvent(e) #required to deselect on 2e click
		if not self.is_enabled: return
		if self.readyToEdit:
			self.setText(self.parent.channel_topic,False)
			self.setReadOnly(False)
			self.selectAll()
			self.readyToEdit = False

	def focusOutEvent(self, e):
		super(QLineEdit, self).focusOutEvent(e) #required to remove cursor on focusOut
		self.setText(self.parent.channel_topic)

		self.deselect()
		self.readyToEdit = True
		self.setReadOnly(True)
		self.setCursorPosition(0)

class SpellTextEdit(QPlainTextEdit):

	returnPressed = pyqtSignal()
	keyUp = pyqtSignal()
	keyDown = pyqtSignal()

	def __init__(self, *args):
		QPlainTextEdit.__init__(self, *args)

		self.parent = args[0]

		self.dict = SpellChecker(language=self.parent.language,distance=config.SPELLCHECKER_DISTANCE)
		self.dict.word_frequency.load_words(config.DICTIONARY)

		self.highlighter = Highlighter(self.document())

		self.highlighter.setDict(self.dict)
		self.highlighter.setParent(self.parent)

		self.nicks = []

	def keyPressEvent(self,event):

		if config.USE_AUTOAWAY:
			if config.TYPING_INPUT_CANCELS_AUTOAWAY:
				if self.parent.client.autoaway:
					self.parent.client.back()

		self.parent.client.last_interaction = 0

		# BUGFIX: the user can "drag" the view "down"
		# with the mouse; this resets the widget to
		# "normal" every time the user presses a key
		# Man, I wish Qt had a rich-text-enabled QLineEdit :-(
		sb = self.verticalScrollBar()
		sb.setValue(sb.minimum())
		self.ensureCursorVisible()

		if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
			self.returnPressed.emit()
			return
		elif event.key() == Qt.Key_Up:
			self.keyUp.emit()
		elif event.key() == Qt.Key_Down:
			self.keyDown.emit()
		elif event.key() == Qt.Key_Tab:
			cursor = self.textCursor()

			if self.toPlainText().strip()=='': return

			if config.ENABLE_AUTOCOMPLETE:
				if config.ENABLE_ALIASES:
					if config.INTERPOLATE_ALIASES_INTO_INPUT:
						if config.AUTOCOMPLETE_ALIAS:
							# Auto-complete channel/server
							cursor.select(QTextCursor.WordUnderCursor)
							oldpos = cursor.position()
							cursor.select(QTextCursor.WordUnderCursor)
							newpos = cursor.selectionStart() - 1
							cursor.setPosition(newpos,QTextCursor.MoveAnchor)
							cursor.setPosition(oldpos,QTextCursor.KeepAnchor)
							self.setTextCursor(cursor)
							if self.textCursor().hasSelection():
								text = self.textCursor().selectedText()

								for a in commands.ALIAS:
									if fnmatch.fnmatch(config.ALIAS_INTERPOLATION_SYMBOL+a,f"{text}*"):
										cursor.beginEditBlock()
										cursor.insertText(f"{config.ALIAS_INTERPOLATION_SYMBOL+a}")
										cursor.endEditBlock()
										return

								for a in commands.TEMPORARY_ALIAS_AUTOCOMPLETE:
									if fnmatch.fnmatch(config.ALIAS_INTERPOLATION_SYMBOL+a,f"{text}*"):
										cursor.beginEditBlock()
										cursor.insertText(f"{config.ALIAS_INTERPOLATION_SYMBOL+a}")
										cursor.endEditBlock()
										return

				if config.AUTOCOMPLETE_COMMANDS:
					# Auto-complete commands
					cursor.select(QTextCursor.BlockUnderCursor)
					self.setTextCursor(cursor)
					if self.textCursor().hasSelection():
						text = self.textCursor().selectedText()

						self.COMMAND_LIST = commands.AUTOCOMPLETE

						for c in self.COMMAND_LIST:
							cmd = c
							rep = self.COMMAND_LIST[c]

							if fnmatch.fnmatch(cmd,f"{text}*"):
								cursor.beginEditBlock()
								cursor.insertText(rep)
								cursor.endEditBlock()
								return

				if config.AUTOCOMPLETE_NICKS:
					# Auto-complete nicks
					cursor.select(QTextCursor.WordUnderCursor)
					self.setTextCursor(cursor)
					if self.textCursor().hasSelection():
						text = self.textCursor().selectedText()

						# Nicks
						chan_nicks = self.parent.nicks
						for nick in chan_nicks:
							# Skip client's nickname
							if nick==self.parent.client.nickname:
								continue
							if fnmatch.fnmatch(nick,f"{text}*"):
								cursor.beginEditBlock()
								cursor.insertText(f"{nick}")
								cursor.endEditBlock()
								return

				if config.AUTOCOMPLETE_CHANNELS:
					# Auto-complete channel/server
					cursor.select(QTextCursor.WordUnderCursor)
					oldpos = cursor.position()
					cursor.select(QTextCursor.WordUnderCursor)
					newpos = cursor.selectionStart() - 1
					cursor.setPosition(newpos,QTextCursor.MoveAnchor)
					cursor.setPosition(oldpos,QTextCursor.KeepAnchor)
					self.setTextCursor(cursor)
					if self.textCursor().hasSelection():
						text = self.textCursor().selectedText()

						# Channel/server names
						for name in self.parent.parent.getAllChatNames():
							if fnmatch.fnmatch(name,f"{text}*"):
								cursor.beginEditBlock()
								cursor.insertText(f"{name}")
								cursor.endEditBlock()
								return

				if config.ENABLE_EMOJI_SHORTCODES:
					if config.AUTOCOMPLETE_EMOJIS:
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
									return

								# Case insensitive
								if fnmatch.fnmatch(c,f"{text}*"):
									cursor.beginEditBlock()
									cursor.insertText(c)
									cursor.endEditBlock()
									return

			cursor.movePosition(QTextCursor.End)
			self.setTextCursor(cursor)

		else:
			return super().keyPressEvent(event)

	def text(self):
		return self.toPlainText()

	def setText(self,text):
		self.setPlainText(text)

	def changeLanguage(self,lang):
		self.dict = SpellChecker(language=lang,distance=config.SPELLCHECKER_DISTANCE)
		self.highlighter.setDict(self.dict)
		self.dict.word_frequency.load_words(config.DICTIONARY)

	def mousePressEvent(self, event):
		if event.button() == Qt.RightButton:
			# Rewrite the mouse event to a left button event so the cursor is
			# moved to the location of the pointer.
			event = QMouseEvent(QEvent.MouseButtonPress, event.pos(),
				Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
		QPlainTextEdit.mousePressEvent(self, event)

	def addToDictionary(self,word):

		# Remove the dictionary from the spellchecker
		self.dict.word_frequency.remove_words(config.DICTIONARY)

		# Add the word to the internal dictionary
		config.DICTIONARY.append(word)

		# Save new settings to the config file
		config.save_settings(config.CONFIG_FILE)

		# Re-add the dictionary to the spellchecker
		self.dict.word_frequency.load_words(config.DICTIONARY)

		# Reset the input
		self.parent.resetInput()

	def removeFromDictionary(self,word):

		# Remove the dictionary from the spellchecker
		self.dict.word_frequency.remove_words(config.DICTIONARY)

		# Remove the word from the internal dictionary
		config.DICTIONARY.remove(word)

		# Save new settings to the config file
		config.save_settings(config.CONFIG_FILE)

		# Re-add the dictionary to the spellchecker
		self.dict.word_frequency.load_words(config.DICTIONARY)

		# Reset the input
		self.parent.resetInput()

	def contextMenuEvent(self, event):

		popup_menu = self.createStandardContextMenu()


		# Don't autoselect if the user has selected text
		# Don't offer spelling corrections if the user has selected text
		if self.textCursor().hasSelection():
			do_spellcheck = False
		else:
			# Select the word under the cursor.
			cursor = self.textCursor()
			cursor.select(QTextCursor.WordUnderCursor)
			self.setTextCursor(cursor)
			do_spellcheck = True
		
		counter = 0
		unknown_word = False

		# Check if the selected word is misspelled and offer spelling
		# suggestions if it is.
		if self.textCursor().hasSelection():
			text = self.textCursor().selectedText()

			# Make sure that words in the custom dictionary aren't flagged as misspelled
			#if not text in config.DICTIONARY:

			if config.ENABLE_SPELLCHECK:

				misspelled = self.dict.unknown([text])
				if len(misspelled)>0:
					unknown_word =True
					if self.dict.candidates(text)!=None:
						for word in self.dict.candidates(text):
							if word!=text:
								action = SpellAction(word, popup_menu)
								action.correct.connect(self.correctWord)
								if word==self.dict.correction(text):
									f = action.font()
									f.setBold(True)
									action.setFont(f)
								popup_menu.insertAction(popup_menu.actions()[0],action)
								counter = counter + 1
						if counter != 0:
							popup_menu.insertSeparator(popup_menu.actions()[counter])

			popup_menu.insertSeparator(popup_menu.actions()[counter])
			counter = counter + 1

			if not ' ' in text:
				if unknown_word:
					entry = QAction(QIcon(DICTIONARY_ICON),f"Add \"{text}\" to dictionary",self)
					entry.triggered.connect(lambda state,word=text: self.addToDictionary(word))
					popup_menu.insertAction(popup_menu.actions()[counter],entry)
					popup_menu.insertSeparator(popup_menu.actions()[counter+1])

				if text in config.DICTIONARY:
					entry = QAction(QIcon(DICTIONARY_ICON),f"Remove \"{text}\" from dictionary",self)
					entry.triggered.connect(lambda state,word=text: self.removeFromDictionary(word))
					popup_menu.insertAction(popup_menu.actions()[counter],entry)
					popup_menu.insertSeparator(popup_menu.actions()[counter+1])

		popup_menu.exec_(event.globalPos())

	def correctWord(self, word):
		'''
		Replaces the selected text with word.
		'''
		cursor = self.textCursor()
		cursor.beginEditBlock()

		cursor.removeSelectedText()
		cursor.insertText(word)

		cursor.endEditBlock()


class Highlighter(QSyntaxHighlighter):

	WORDS = u'(?iu)[\\w\']+'
	CHANNELS = r"#\w+"
	EMOJIS = r":\w+:"
	SPECIAL = ['\\','^','$','.','|','?','*','+','(',')','{']

	def __init__(self, *args):
		QSyntaxHighlighter.__init__(self, *args)

		self.dict = None
		self.ulist = []

	def setParent(self,parent):
		self.parent = parent

	def setDict(self, dict):
		self.dict = dict

	def escape_symbol(self,target):
		symbol = ''
		for c in target:
			if c in self.SPECIAL:
				c = '\\'+c
			symbol = symbol + c
		return fr"{symbol}\w+"

	def highlightBlock(self, text):

		do_not_spellcheck = []

		if config.APPLY_SYNTAX_STYLES_TO_INPUT_WIDGET:

			# Apply syntax style to emoji shortcodes
			if config.ENABLE_EMOJI_SHORTCODES:
				emojiformat = syntax.format(config.SYNTAX_EMOJI_COLOR,config.SYNTAX_EMOJI_STYLE)
				for word_object in re.finditer(self.EMOJIS, text):
					for code in EMOJI_AUTOCOMPLETE:
						if code==word_object.group():
							do_not_spellcheck.append(code[1:-1])
							self.setFormat(word_object.start(), word_object.end() - word_object.start(), emojiformat)

			# Apply syntax style to nicknames
			nickformat = syntax.format(config.SYNTAX_NICKNAME_COLOR,config.SYNTAX_NICKNAME_STYLE)
			for word_object in re.finditer(self.WORDS, text):
				for nick in self.parent.nicks:
					if nick==self.parent.client.nickname: continue
					if nick==word_object.group():
						do_not_spellcheck.append(nick)
						self.setFormat(word_object.start(), word_object.end() - word_object.start(), nickformat)

			# Apply syntax styles to channels
			channelformat = syntax.format(config.SYNTAX_CHANNEL_COLOR,config.SYNTAX_CHANNEL_STYLE)
			for word_object in re.finditer(self.CHANNELS, text):
				for name in self.parent.parent.getAllChatNames():
					if name==word_object.group():
						do_not_spellcheck.append(name)
						do_not_spellcheck.append(name[1:])
						self.setFormat(word_object.start(), word_object.end() - word_object.start(), channelformat)

			if config.ENABLE_ALIASES:
				# Apply syntax styles to aliases
				if config.INTERPOLATE_ALIASES_INTO_INPUT:
					# Make sure the alias interpolation symbol
					# is properly escaped
					ALIASES = self.escape_symbol(config.ALIAS_INTERPOLATION_SYMBOL)

					aliasformat = syntax.format(config.SYNTAX_ALIAS_COLOR,config.SYNTAX_ALIAS_STYLE)
					for word_object in re.finditer(ALIASES, text):
						for a in commands.ALIAS:
							if config.ALIAS_INTERPOLATION_SYMBOL+a==word_object.group():
								do_not_spellcheck.append(a)
								self.setFormat(word_object.start(), word_object.end() - word_object.start(), aliasformat)

						for a in commands.TEMPORARY_ALIAS_AUTOCOMPLETE:
							if config.ALIAS_INTERPOLATION_SYMBOL+a==word_object.group():
								do_not_spellcheck.append(a)
								self.setFormat(word_object.start(), word_object.end() - word_object.start(), aliasformat)

			# Apply syntax styles to commands
			
			# Make sure the command symbol is
			# properly escaped
			COMMANDS = self.escape_symbol(config.ISSUE_COMMAND_SYMBOL)

			cmdformat = syntax.format(config.SYNTAX_COMMAND_COLOR,config.SYNTAX_COMMAND_STYLE)
			for word_object in re.finditer(COMMANDS, text):
				for c in commands.AUTOCOMPLETE:
					if c==word_object.group():
						do_not_spellcheck.append(c)
						do_not_spellcheck.append(c[1:])
						self.setFormat(word_object.start(), word_object.end() - word_object.start(), cmdformat)

		# Highlight for spelling
		if self.dict:
			misspelled_format = QTextCharFormat()
			misspelled_format.setUnderlineColor(QColor(config.SPELLCHECK_UNDERLINE_COLOR))
			misspelled_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
			if config.SHOW_MISSPELLED_WORDS_IN_ITALICS: misspelled_format.setFontItalic(True)
			if config.SHOW_MISSPELLED_WORDS_IN_BOLD: misspelled_format.setFontWeight(QFont.Bold)
			if config.SHOW_MISSPELLED_WORDS_IN_STRIKEOUT: misspelled_format.setFontStrikeOut(True)
			if config.SHOW_MISSPELLED_WORDS_IN_COLOR: misspelled_format.setForeground(QColor(config.SPELLCHECK_UNDERLINE_COLOR))

			for word_object in re.finditer(self.WORDS, text):

				if config.ENABLE_SPELLCHECK:

					misspelled = self.dict.unknown([word_object.group()])
					if len(misspelled)>0:
						# Make sure that words in the custom dictionary aren't flagged as misspelled
						if not word_object.group() in config.DICTIONARY:
							if config.APPLY_SYNTAX_STYLES_TO_INPUT_WIDGET:
								if not word_object.group() in do_not_spellcheck:
									self.setFormat(word_object.start(), word_object.end() - word_object.start(), misspelled_format)
							else:
								self.setFormat(word_object.start(), word_object.end() - word_object.start(), misspelled_format)

class SpellAction(QAction):
	correct = pyqtSignal(str)

	def __init__(self, *args):
		QAction.__init__(self, *args)

		self.triggered.connect(lambda x: self.correct.emit(
			self.text()))