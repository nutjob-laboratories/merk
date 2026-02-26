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

import uuid
import os
import fnmatch

from ..resources import *
from .. import config
from .. import render

class Window(QMainWindow):

	def closeEvent(self, event):

		# Make sure the MDI window is closed
		self.parent.closeSubWindow(self.subwindow_id)
		self.client.channel_list_window = None

		event.accept()
		self.close()

	def __init__(self,client=None,channel_data=None,parent=None):
		super(Window, self).__init__(parent)

		self.client = client
		self.data = channel_data
		self.parent = parent

		if self.client.hostname:
			self.server_name = self.client.hostname
		else:
			self.server_name = self.client.server+":"+str(self.client.port)

		self.name = self.server_name + " channels"

		if hasattr(self.client,"network"):
			self.network = self.client.network
		else:
			self.network = config.UNKNOWN_NETWORK_NAME.capitalize()+" network"

		self.window_title = f"Channels on {self.server_name} ({self.network})"

		self.setWindowTitle(self.window_title)

		self.window_type = LIST_WINDOW
		self.subwindow_id = str(uuid.uuid4())

		self.table_widget = QListWidget()

		self.table_widget.setAlternatingRowColors(True)
		self.table_widget.setTextElideMode(Qt.ElideRight)
		self.table_widget.itemDoubleClicked.connect(self.on_double_click)

		self.search_terms = QLineEdit('')
		self.search_terms.returnPressed.connect(self.doSearch)
		self.search_terms.setPlaceholderText("Enter search terms here")

		self.search_button = QPushButton('')
		self.search_button.setIcon(QIcon(LIST_ICON))
		self.search_button.setToolTip("Search channel list")
		self.search_button.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.search_button.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.search_button.clicked.connect(self.doSearch)
		self.search_button.setFlat(True)

		self.refresh_button = QPushButton('')
		self.refresh_button.setIcon(QIcon(REFRESH_ICON))
		self.refresh_button.setToolTip("Refresh channel list")
		self.refresh_button.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.refresh_button.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.refresh_button.clicked.connect(lambda state: self.client.sendLine('LIST'))
		self.refresh_button.setFlat(True)

		self.moreFive	= QRadioButton("5+",self)
		self.moreTen	= QRadioButton("10+",self)
		self.moreTwenty = QRadioButton("20+",self)
		self.moreFifty	= QRadioButton("50+",self)
		self.moreAny	= QRadioButton("1+",self)
		self.moreAny.setChecked(True)
		self.moreFive.toggled.connect(self.doReset)
		self.moreTen.toggled.connect(self.doReset)
		self.moreTwenty.toggled.connect(self.doReset)
		self.moreAny.toggled.connect(self.doReset)
		self.moreFifty.toggled.connect(self.doReset)

		self.reset_button = QPushButton("Reset")
		self.reset_button.clicked.connect(self.doResetButton)

		self.searchTopic = QCheckBox("Search topics",self)
		if config.EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH: self.searchTopic.setChecked(True)
		self.searchTopic.stateChanged.connect(self.changedSearchTopic)

		self.allTerms = QCheckBox("Search all terms",self)
		if config.SEARCH_ALL_TERMS_IN_CHANNEL_LIST: self.allTerms.setChecked(True)
		self.allTerms.stateChanged.connect(self.changedAllTerms)

		self.status = self.statusBar()
		self.status.setStyleSheet("QStatusBar::item { border: none; }")
		self.status_counts = QLabel(self.format_status_count(client.server_channel_count,client.server_user_count))
		self.status.addPermanentWidget(self.status_counts,0)
		self.status.addPermanentWidget(QLabel(),1)
		self.lastFetch = QLabel("<small>List received at "+self.client.last_list_fetch+"</small>")
		self.status.addPermanentWidget(self.lastFetch,0)

		if not config.SHOW_STATUS_BAR_ON_LIST_WINDOWS:
			self.status.hide()

		self.cLayout = QHBoxLayout()
		
		self.cLayout.addStretch()

		self.sLayout = QHBoxLayout()
		self.sLayout.addWidget(self.search_terms)
		self.sLayout.addWidget(self.search_button)
		self.sLayout.addWidget(QLabel(' '))
		self.sLayout.addWidget(self.refresh_button)
		self.sLayout.addWidget(QLabel(' '))
		self.sLayout.addWidget(self.reset_button)
		self.sLayout.setContentsMargins(1,1,1,1)

		self.oLayout = QHBoxLayout()
		self.oLayout.addWidget(QLabel("<b>Users:</b> "))
		self.oLayout.addWidget(self.moreAny)
		self.oLayout.addWidget(self.moreFive)
		self.oLayout.addWidget(self.moreTen)
		self.oLayout.addWidget(self.moreTwenty)
		self.oLayout.addWidget(self.moreFifty)
		self.oLayout.addStretch()
		self.oLayout.addWidget(self.allTerms)
		self.oLayout.addWidget(self.searchTopic)
		

		if config.SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS:
			if config.SHOW_CHANNEL_LIST_IN_WINDOWS_MENU:
				extra = f"""A new channel list can be requested from the server with the <b>{config.ISSUE_COMMAND_SYMBOL}refresh</b>
					command, or by clicking the <b>Refresh channel list</b> button on server window toolbars on in the <b>{config.MAIN_MENU_WINDOWS_NAME}</b>
					menu. This window will automatically update to use the new list."""
			else:
				extra = f"""A new channel list can be requested from the server with the <b>{config.ISSUE_COMMAND_SYMBOL}refresh</b>
					command, or by clicking the <b>Refresh channel list</b> button on server window toolbars. This window will automatically update
					to use the new list."""
		else:
			if config.SHOW_CHANNEL_LIST_IN_WINDOWS_MENU:
				extra = f"""A new channel list can be requested from the server with the <b>{config.ISSUE_COMMAND_SYMBOL}refresh</b>
					command, or by clicking <b>Refresh channel list</b> in the <b>{config.MAIN_MENU_WINDOWS_NAME}</b>
					menu. This window will automatically update to use the new list."""
			else:
				extra = f"""A new channel list can be requested from the server with the <b>{config.ISSUE_COMMAND_SYMBOL}refresh</b>
					command; this window will automatically update to use the new list."""

		if not config.SIMPLIFIED_DIALOGS:
			self.windowDescription = QLabel(f"""
				<small>
				This is a list of channels on <b>{self.server_name} ({self.network})</b>. To join a channel in the
				list, double click on the line the channel appears on. To search the
				list, enter search terms below, using <b>*</b> for multi-character wildcards,
				and <b>?</b> for single character wildcards, and press enter or the <b>Search</b> button.
				To reset the list after a search, press the <b>Reset</b> button to re-display all channels.
				{extra}
				</small>
				""")
			self.windowDescription.setWordWrap(True)
			self.windowDescription.setAlignment(Qt.AlignJustify)

		self.layout = QVBoxLayout()
		self.layout.setSpacing(2)
		if not config.SIMPLIFIED_DIALOGS:
			self.layout.addWidget(self.windowDescription)
		self.layout.addLayout(self.sLayout)
		self.layout.addLayout(self.oLayout)
		self.layout.addWidget(self.table_widget)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(self.layout)
		self.setCentralWidget(self.centralWidget)

		self.populate_table(self.data)

	def toggleStatusBar(self):
		if config.SHOW_STATUS_BAR_ON_LIST_WINDOWS:
			self.status.show()
		else:
			self.status.hide()

	def changedAllTerms(self,i):
		if self.allTerms.isChecked():
			config.SEARCH_ALL_TERMS_IN_CHANNEL_LIST = True
		else:
			config.SEARCH_ALL_TERMS_IN_CHANNEL_LIST = False
		config.save_settings(config.CONFIG_FILE)
		self.refresh_list()

	def changedSearchTopic(self,i):
		if self.searchTopic.isChecked():
			config.EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH = True
		else:
			config.EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH = False
		config.save_settings(config.CONFIG_FILE)
		self.refresh_list()

	def doExternalSearch(self,search_terms):
		self.search_terms.setText(search_terms)
		self.doSearch()

	def doSearch(self):

		QApplication.setOverrideCursor(Qt.WaitCursor)

		self.table_widget.clear()

		target = self.search_terms.text()

		self.setWindowTitle(self.window_title+" - "+target)

		if config.SEARCH_ALL_TERMS_IN_CHANNEL_LIST:
			target = "*"+"*".join(target.split())+"*"

		results = []
		for entry in self.client.server_channel_list:
			channel_name = entry[0]
			channel_count = entry[1]
			channel_topic = entry[2]

			if fnmatch.fnmatch(channel_name,f"{target}"):
				results.append(entry)
			if config.EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH:
				if fnmatch.fnmatch(channel_topic,f"{target}"):
					results.append(entry)

		results = remove_duplicate_sublists(results)

		data_count = 0
		user_count = 0
		for entry in results:
			try:
				if int(entry[1])==1:
					count = "(1 user)"
				else:
					count = f"({entry[1]} users)"
				icount = int(entry[1])
			except:
				count = ""
				icount = 0

			add_entry = True
			if self.moreFive.isChecked():
				if icount<5:
					add_entry = False
			if self.moreTen.isChecked():
				if icount<10:
					add_entry = False
			if self.moreTwenty.isChecked():
				if icount<20:
					add_entry = False
			if self.moreFifty.isChecked():
				if icount<50:
					add_entry = False

			if add_entry:
				if len(entry[2])==0:
					e = f"{entry[0]} {count}"
				else:
					if string_has_irc_formatting_codes(entry[2]):
						topic = strip_color(entry[2])
					else:
						topic = entry[2]
					e = f"{entry[0]} {count} - {topic}"
				
				i = QListWidgetItem(e)
				f = i.font()
				f.setBold(True)
				i.setFont(f)
				self.table_widget.addItem(i)

				i.channel = entry[0]
				data_count = data_count + 1
				user_count = user_count + icount

		self.table_widget.sortItems()

		self.status_counts.setText(self.format_status_count(data_count,user_count))

		if self.table_widget.count()==0:
			i = QListWidgetItem("No channels found.")
			f = i.font()
			f.setBold(True)
			i.setFont(f)
			self.table_widget.addItem(i)

		QApplication.restoreOverrideCursor()

	def doReset(self):
		self.refresh_list()

	def doResetButton(self):
		self.search_terms.setText('')
		self.setWindowTitle(self.window_title)
		self.refresh_list()

	def refresh_list(self):
		if len(self.search_terms.text().strip())>0:
			self.data = self.client.server_channel_list
			self.doSearch()
		else:
			self.table_widget.clear()
			self.data = self.client.server_channel_list
			self.populate_table(self.data)
		if self.client.last_list_fetch=='':
			self.lastFetch.setText("<small>List received at an unknown time</small>")
		else:
			self.lastFetch.setText("<small>List received at "+self.client.last_list_fetch+"</small>")

	def on_double_click(self,item):
		self.client.join(item.channel)

	def format_status_count(self,channels,users):
		return f"<small><i>{channels:,} channels with {users:,} users</i></small>"

	def populate_table(self, data):
		data_count = 0
		user_count = 0
		for entry in data:
			try:
				if int(entry[1])==1:
					count = "(1 user)"
				else:
					count = f"({entry[1]} users)"
				icount = int(entry[1])
			except:
				count = ""
				icount = 0

			add_entry = True
			if self.moreFive.isChecked():
				if icount<5:
					add_entry = False
			if self.moreTen.isChecked():
				if icount<10:
					add_entry = False
			if self.moreTwenty.isChecked():
				if icount<20:
					add_entry = False
			if self.moreFifty.isChecked():
				if icount<50:
					add_entry = False

			if add_entry:
				if len(entry[2])==0:
					e = f"{entry[0]} {count}"
				else:
					if string_has_irc_formatting_codes(entry[2]):
						topic = strip_color(entry[2])
					else:
						topic = entry[2]
					e = f"{entry[0]} {count} - {topic}"

				i = QListWidgetItem(e)
				f = i.font()
				f.setBold(True)
				i.setFont(f)
				self.table_widget.addItem(i)

				i.channel = entry[0]

				data_count = data_count + 1
				user_count = user_count + icount

		self.table_widget.sortItems()

		self.status_counts.setText(self.format_status_count(data_count,user_count))

		if self.table_widget.count()==0:
			i = QListWidgetItem("No channels found.")
			f = i.font()
			f.setBold(True)
			i.setFont(f)
			self.table_widget.addItem(i)

	