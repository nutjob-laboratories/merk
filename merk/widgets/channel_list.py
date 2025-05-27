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

		self.name = "CHANNEL_LIST_WINDOW"

		if self.client.hostname:
			self.server_name = self.client.hostname
		else:
			self.server_name = self.client.server+":"+str(self.client.port)

		if hasattr(self.client,"network"):
			self.network = self.client.network
		else:
			self.network = "Unknown network"

		self.setWindowTitle(f"Channels on {self.server_name} ({self.network}) - {len(self.data)} channels")

		self.window_type = LIST_WINDOW
		self.subwindow_id = str(uuid.uuid4())

		self.table_widget = QListWidget()

		self.table_widget.setAlternatingRowColors(True)
		# self.table_widget.setWordWrap(True)
		self.table_widget.setTextElideMode(Qt.ElideRight)

		self.table_widget.itemDoubleClicked.connect(self.on_double_click)

		self.search_terms = QLineEdit('')
		self.search_button = QPushButton("Search")
		self.reset_button = QPushButton("Filter/Reset")
		self.refresh = QPushButton("Fetch List")

		self.moreFive = QCheckBox("5+",self)
		self.moreFive.stateChanged.connect(self.moreFiveClick)

		self.moreTwo = QCheckBox("2+",self)
		self.moreTen = QCheckBox("10+",self)
		self.moreTwenty = QCheckBox("20+",self)

		self.search_terms.setPlaceholderText("Enter search terms here")
		self.search_button.setDefault(True) 

		self.search_button.clicked.connect(self.doSearch)
		self.refresh.clicked.connect(self.doRefresh)
		self.reset_button.clicked.connect(self.doReset)

		self.sLayout = QHBoxLayout()
		self.sLayout.addWidget(self.search_terms)
		self.sLayout.addWidget(self.search_button)
		self.sLayout.addWidget(self.reset_button)
		self.sLayout.addWidget(self.refresh)

		self.cLayout = QHBoxLayout()
		self.cLayout.addWidget(QLabel('<b>Channel user count:</b>'))
		self.cLayout.addWidget(self.moreTwo)
		self.cLayout.addWidget(self.moreFive)
		self.cLayout.addWidget(self.moreTen)
		self.cLayout.addWidget(self.moreTwenty)
		self.cLayout.addStretch()

		self.windowDescription = QLabel(f"""
			<small>
			This is a list of channels on <b>{self.server_name} ({self.network})</b>. To join a channel in the
			list, double click on the line the channel appears on. To search the
			list, enter search terms below, using <b>*</b> for multi-character wildcards,
			and <b>?</b> for single character wildcards, and press the <b>Search</b> button.
			To reset the list after a search, press <b>Filter/Reset</b> to re-display all channels or
			to filter list on channel user count.
			Press <b>Fetch List</b> to request a fresh channel list from the server.
			</small>
			""")
		self.windowDescription.setWordWrap(True)
		self.windowDescription.setAlignment(Qt.AlignJustify)

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.windowDescription)
		self.layout.addLayout(self.sLayout)
		self.layout.addLayout(self.cLayout)
		self.layout.addWidget(self.table_widget)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(self.layout)
		self.setCentralWidget(self.centralWidget)

		self.populate_table(self.data)

	def moreFiveClick(self):
		#self.refresh_list()
		pass

	def doExternalSearch(self,search_terms):
		self.search_terms.setText(search_terms)
		self.doSearch()

	def doSearch(self):

		self.table_widget.clear()

		target = self.search_terms.text()

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
			if self.moreTwo.isChecked():
				if icount<2:
					add_entry = False
			if self.moreFive.isChecked():
				if icount<5:
					add_entry = False
			if self.moreTen.isChecked():
				if icount<10:
					add_entry = False
			if self.moreTwenty.isChecked():
				if icount<20:
					add_entry = False
			if len(entry[2])==0:
				e = f"{entry[0]} ({count})"
			else:
				e = f"{entry[0]} ({count}) - {entry[2]}"
			i = QListWidgetItem()
			i.setText(e)
			font = QFont()
			font.setBold(True)
			i.setFont(font)
			i.channel = entry[0]
			if add_entry:
				self.table_widget.addItem(i)
				data_count = data_count + 1

		self.setWindowTitle(f"Channels on {self.server_name} ({self.network}) - {data_count} channels")

	def doRefresh(self):
		self.client.doing_list_refresh = True
		self.client.sendLine('LIST')

	def doReset(self):
		self.search_terms.setText('')
		self.refresh_list()

	def refresh_list(self):
		self.table_widget.clear()
		self.data = self.client.server_channel_list
		self.populate_table(self.data)

	def on_double_click(self,item):
		self.client.join(item.channel)

	def populate_table(self, data):
		data_count = 0
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
			if self.moreTwo.isChecked():
				if icount<2:
					add_entry = False
			if self.moreFive.isChecked():
				if icount<5:
					add_entry = False
			if self.moreTen.isChecked():
				if icount<10:
					add_entry = False
			if self.moreTwenty.isChecked():
				if icount<20:
					add_entry = False
			if len(entry[2])==0:
				e = f"{entry[0]} {count}"
			else:
				e = f"{entry[0]} {count} - {entry[2]}"
			i = QListWidgetItem()
			i.setText(e)
			font = QFont()
			font.setBold(True)
			i.setFont(font)
			i.channel = entry[0]
			if add_entry:
				self.table_widget.addItem(i)
				data_count = data_count + 1

		self.setWindowTitle(f"Channels on {self.server_name} ({self.network}) - {data_count} channels")

	