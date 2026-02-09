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

import uuid
import random

TIPS = [
 f'You can make a message bold by surrounding it with double asterisks!',
 f'You can send a message in italics by surrounding it with single asterisks!',
 f'To underline a word in a message, place two underscores before and after it!',
 f'Closing a channel window automatically leaves that channel!',
 f'You can change your nickname by double clicking the nickname display on chat windows!',
 f'To see a list of commands, type <nobr><b>{config.ISSUE_COMMAND_SYMBOL}help</b></nobr> in any chat window!',
 f'Click on the topic in channel windows to edit it, and press enter to send your changes to the server!',
 f'IRC was created by <b>Jarkko Oikarinen</b> in August 1988 to replace a program called MUT (MultiUser Talk)!',
 f"IRC was used to report on the 1991 Soviet coup d'état attempt throughout a media blackout!",
 f'As of December 2025, the top 5 IRC networks have total participation of around 88,000 users per day!',
 f'You can insert <b>emojis</b> into your messages using shortcodes!',
 f'You can insert <b>ASCIImojis</b> into your messages using shortcodes!',
 f'<b>{APPLICATION_NAME}</b> is open source! Check out the source code at <b><a href=\"{APPLICATION_SOURCE}\">{APPLICATION_SOURCE}</a></b>',
 f'Color in IRC messages was first introduced by <b>mIRC</b> in 1996, with version 4.5!',
 f'IRC has inspired many modern protocols, like <b>Slack</b> and <b>Discord</b>!',
 f'Use the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}list</b></nobr> command to find a channel to join!',
 f'Right click on any user in a channel user list for more options!',
 f'You can <b>{config.ISSUE_COMMAND_SYMBOL}ignore</b> annoying users to stop hearing from them!',
 f'You can create hotkeys to send commands to any server, channel, or private chat window instantly!',
 f'The <b>{APPLICATION_NAME}</b> User Guide has all the information you need to get the most out of <b>{APPLICATION_NAME}</b>!',
 f'To send a message in a command or script, use the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}msg</b></nobr> command!',
 f'You can search your channel and private chat logs with the <b>Log Manager</b>!',
 f"The <b>Style Editor</b> allows you to set each chat window's text styles!",
 f'Right click on the windowbar to see configuration options!',
 f'Right click on the menu bar to see configuration options!',
 f'<b>{APPLICATION_NAME}</b> can connect to multiple servers at one time!',
 f'To hide a server, channel, or private chat window, use the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}hide</b></nobr> command!',
 f'Use the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}maximize</b></nobr> command to maximize a chat window!',
 f'Use the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}minimize</b></nobr> command to minimize a chat window!',
 f'Connect to another server with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}connect</b></nobr> command!',
 f'<b>{APPLICATION_NAME}</b> can connect to IRC servers via <b>TCP/IP</b> or <b>SSL/TLS</b>!',
 f'Nicknames and channel names are unique on an IRC network!',
 f'The default server port for IRC is <b>6667</b> (<b>6697</b> for SSL/TLS)!',
 f'Unlike <b>Discord</b> or <b>Slack</b>, no single company owns IRC. Anyone can run their own server!',
 f'The first IRC server was <b>tolsun.oulu.fi</b>!',
 f'In early 1991, IRC was used for real-time reporting on the Gulf War!',
 f'A single IRC message is strictly capped at 512 characters, including the line-ending characters!',
 f'Much of early "internet slang" and leetspeak evolved or was popularized in IRC channels!',
 f'<b>{APPLICATION_NAME}</b> supports spellchecking in eight different languages!',
 f'<b>{APPLICATION_NAME}</b> can be configured with the <b>Settings</b> dialog, with over 300 different settings!',
 f'<b>{APPLICATION_NAME}</b> converts URLs in chat into clickable links, automatically!',
 f'<b>{APPLICATION_NAME}</b> is licensed under the <b>GNU General Public License 3.0</b>!',
 f"<b>{APPLICATION_NAME}</b> has <b>Windows</b> and <b>Linux</b> executables that don't require a Python installation!",
 f'<b>{APPLICATION_NAME}</b> uses a "multi-document interface", inspired by <b>mIRC</b> in 1995!',
 f'Right click on the chat display of any chat window for more options!',
 f'For more information about using <b>{APPLICATION_NAME}</b>, check out the <b>Help</b> menu!',
 f'To see a list of connected servers and windows, check out the <b>Windows</b> menu!',
 f'The <b>Tools</b> menu has a list of all the additional utilities you can use in <b>{APPLICATION_NAME}</b>!',
 f'The <b>Libera IRC network</b> is the biggest IRC network in 2026, with over 20,000 channels!',
 f'<b>{APPLICATION_NAME}</b> features over 70 commands, and even more that can be used in scripts!',
 f'Join a channel with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}join</b></nobr> command!',
 f'Change your nickname with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}nick</b></nobr> command!',
 f"Send a message describing what you're doing with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}me</b></nobr> command!",
 f'Disconnect from a server with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}quit</b></nobr> command!',
 f'Disconnect from all connected servers with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}quitall</b></nobr> command!',
 f'Set your status to "away" with the\u00A0<nobr><b>{config.ISSUE_COMMAND_SYMBOL}away</b></nobr> command!',
 f'Send a notice with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}notice</b></nobr> command!',
 f'Force <b>{APPLICATION_NAME}</b> to be "on top" of all other windows in Settings!',
 f'<b>{APPLICATION_NAME}</b> will always be free, but donations are welcome. <a href=\"https://buymeacoffee.com/danhetrick\">Donate today!</a>',
 f'Become a <a href=\"https://buymeacoffee.com/danhetrick\">patron of <b>{APPLICATION_NAME}</b></a> today, and help keep IRC going in the 21st century!',
 f'<b>UnrealIRCd</b> is the most popular and widely deployed IRC server software!',
 f'<b>{APPLICATION_NAME}</b> can notify you with a sound when your nickname is mentioned!',
 f'<b>{APPLICATION_NAME}</b> can be "minimized" to the system tray!',
 f'Leave a channel with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}part</b></nobr> command!',
 f'See the <b>{APPLICATION_NAME} User Guide</b> for how to send colored messages in your chat!',
 f'IRC is completely free and open source for anyone to use!',
 f'Set a channel topic with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}topic</b></nobr> command!',
 f'Invite someone to a channel with <nobr><b>{config.ISSUE_COMMAND_SYMBOL}invite</b></nobr>!',
 f'Open a private chat to a user by double-clicking their nickname in the user list!',
 f'Logs can be exported to JSON or your own custom format with the <b>Log Manager</b>!',
 f'<b>{APPLICATION_NAME}</b> saves a history of the servers it has connected to automatically!',
 f'<b>{APPLICATION_NAME}</b> features a list of over 80 servers to connect to, built in!',
 f'Right click on entries in the windowbar to see more options!',
 f'<b>{APPLICATION_NAME}</b> features autocomplete for commands, nicknames, channels, and more!',
 f'<b>{APPLICATION_NAME}</b> has been in active development since 2019, all by a single person!',
 f'<b>{APPLICATION_NAME}</b> logs all channel and private chat by default!',
 f'Set your status to "back" with the\u00A0<nobr><b>{config.ISSUE_COMMAND_SYMBOL}back</b></nobr> command!',
 f'<b>{APPLICATION_NAME}</b> is written in Python, using PyQt5, Twisted, and OpenSSL!',
 f'Nearly every aspect of <b>{APPLICATION_NAME}</b> can be configured with the <b>Settings</b> dialog!',
 f'<b>{APPLICATION_NAME}</b> can be ran full-screen! Turn this option on in <b>Settings</b>, or in the <b>Settings</b> menu!',
 f'<b>{APPLICATION_NAME}</b> features a complex set of command-line flags!',
 f'<b>{APPLICATION_NAME}</b> can run in "dark mode", so you don\'t hurt your eyes!',
 f'<b>{APPLICATION_NAME}</b> and the source code will always be free, but donations will always be welcome. <a href=\"https://buymeacoffee.com/danhetrick\">Donate today!</a>',
 f'Change the displayed names of the menus in the <b>Settings</b> dialog!',
 f'IRC lets people all over the world talk to each other in real-time, completely free!',
 f'<b>{APPLICATION_NAME}</b> can run completely from a USB thumb drive. Check out the <b>README</b> for how!',
 f'Join us on the official <b>#merk</b> channel, on <a href=\"https://libera.chat/\">Libera.chat</a>!',
 f'IRC nicknames can\'t have !, @, $, %, &, *, (, ), ., ,, /, ?, <, >, +, = characters or spaces in them!',
 f'IRC nicknames can\'t start with numbers!',
 f'IRC channel names can\'t contain spaces, control characters (like colors), or commas!',
 f'At its peak, IRC had 10,000,000 daily users!',
 f'<b>{APPLICATION_NAME}</b> runs on both <b>Windows</b> and <b>Linux</b> identically!',
 f'There are <b>{APPLICATION_NAME}</b> users all over the world, like Germany, Spain, Serbia, and the United States!',
 f'You can turn off timestamp display in settings, but timestamps are still saved to logs!',
 f'Logs can be automatically saved every once in awhile, so you don\'t lose anything from a system crash!',
 f'<b>NickServ</b> and <b>ChanServ</b> are IRC service bots that provide persistent management for user nicknames and channels, ensuring ownership and security!',
 f'As of 2021, there were 481 known operational IRC networks, with major networks like Libera supporting thousands of channels and users!',
 f'If you want to know how IRC works, take a look at RFC 1459 and RFC 2812 in the <b>Help</b> menu!',
 f'There are over 1,400 open source IRC clients. Thank you for choosing <b>{APPLICATION_NAME}</b>!',
 f'Open source refers to software with source code that anyone can inspect, modify, enhance, and redistribute freely!',
 f'Channel user lists can be configured in the Settings dialog!',
 f'Almost every aspect of <b>{APPLICATION_NAME}</b>\'s interface can be changed or modified!',
 f'Check the official <b><a href=\"{APPLICATION_SOURCE}\">{APPLICATION_NAME} homepage</a></b>. <b>{APPLICATION_NAME}</b> is updated often!',
]

if config.ENABLE_PLUGINS:
	p = [
		f'<b>{APPLICATION_NAME}</b> plugins are written in Python, just like <b>{APPLICATION_NAME}</b>!',
		f'You can install, edit, and create plugins with the <b>Plugin Manager</b>!',
		f'<b>{APPLICATION_NAME}</b> plugins can join channels, send messages, and even execute scripts!',
		f'<b>{APPLICATION_NAME}</b> plugins can use any library in the Python standard library!',
		f'<b>{APPLICATION_NAME}</b> features a Python editor for plugins, complete with syntax highlighting!',
		f'<b>{APPLICATION_NAME}</b> can directly execute plugin methods with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}call</b> command!',
	]
	TIPS = TIPS + p

if config.SCRIPTING_ENGINE_ENABLED:
	s = [
		f'You can write, edit, and execute scripts with the <b>Script Editor</b>!',
		f'Connection scripts allow you to automatically send commands as soon as you connect!',
		f'<b>{APPLICATION_NAME}</b> scripts can do almost everything you can do with a keyboard and mouse!',
		f'Want to automate your server connections? Start writing connections scripts!',
		f'Scripts can use special script-only commands, allowing them to "pause" or prevent execution in certain windows!',
		f'Create your own commands with the <nobr><b>{config.ISSUE_COMMAND_SYMBOL}macro</b></nobr> command!',
	]
	TIPS = TIPS + s

random.shuffle(TIPS)

class Window(QMainWindow):

	def closeEvent(self, event):

		self.parent.tips = None

		event.accept()
		self.close()

	def next_tip(self):
		self.pointer = self.pointer + 1
		if self.pointer > len(TIPS)-1:
			random.shuffle(TIPS)
			self.pointer = 0

		todays_tip = TIPS[self.pointer]
		self.trick.setText(todays_tip)

	def changedSetting(self,state):
		if config.SHOW_TIPS_AT_START:
			config.SHOW_TIPS_AT_START = False
		else:
			config.SHOW_TIPS_AT_START = True
		config.save_settings(config.CONFIG_FILE)

	def __init__(self,parent=None):
		super(Window,self).__init__(parent)

		self.parent = parent
		self.pointer = 0

		config.load_settings(config.CONFIG_FILE)
		
		self.window_type = TIPS_WINDOW
		self.subwindow_id = str(uuid.uuid4())
		self.setWindowIcon(QIcon(APPLICATION_ICON))

		self.name = f"Tip of the Day"
		self.setWindowTitle(f"Tip of the Day")

		todays_tip = TIPS[self.pointer]

		self.trick = QLabel(todays_tip)
		self.trick.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.trick.setWordWrap(True)
		self.trick.setAlignment(Qt.AlignCenter)
		if self.parent.dark_mode:
			self.trick.setStyleSheet(
				"border: 1px solid white; "
				"padding: 5px;"
				"background-color: #998e02; color: white;"
			)
		else:
			self.trick.setStyleSheet(
				"border: 1px solid black; "
				"padding: 5px;"
				"background-color: #fff49d; color: black;"
			)
		self.trick.setOpenExternalLinks(True)

		self.next = QPushButton(" Next Tip ")
		self.next.clicked.connect(self.next_tip)

		self.cbutton = QPushButton("Close")
		self.cbutton.clicked.connect(self.close)

		self.doTips = QCheckBox("Show at startup",self)
		if config.SHOW_TIPS_AT_START: self.doTips.setChecked(True)
		self.doTips.stateChanged.connect(self.changedSetting)

		self.donate = QLabel("<center><a href=\"https://buymeacoffee.com/danhetrick\">Donate to <b>MERK</b> today!</a></center>")
		self.donate.setOpenExternalLinks(True)

		buttons = QHBoxLayout()
		buttons.addWidget(self.doTips)
		buttons.addStretch()
		buttons.addWidget(self.next)
		buttons.addWidget(self.cbutton)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.trick)
		finalLayout.addWidget(self.donate)
		finalLayout.addLayout(buttons)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(finalLayout)
		self.setCentralWidget(self.centralWidget)

		self.resize(350,150)

		# Center dialog on the screen
		mouse_pos = QApplication.desktop().cursor().pos()
		screen_index = QApplication.desktop().screenNumber(mouse_pos)
		screen_geometry = QApplication.desktop().availableGeometry(screen_index)
		window_geometry = self.frameGeometry()
		center_point = screen_geometry.center()
		window_geometry.moveCenter(center_point)
		self.move(window_geometry.topLeft())

		self.setWindowFlags(self.windowFlags() | Qt.WindowType.Dialog)

		if bool(self.parent.windowFlags() & Qt.WindowStaysOnTopHint):
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

		self.cbutton.setFocus()
