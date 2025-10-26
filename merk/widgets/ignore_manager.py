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
from .. import commands
from .. import config
from ..dialog import *

import uuid

class Window(QMainWindow):

	def add_key(self):
		i = GetIgnore('',self)
		if i:

			config.IGNORE_LIST.append(i)
			config.save_settings(config.CONFIG_FILE)
			self.parent.buildSettingsMenu()
			self.parent.reRenderAll(True)
			self.parent.rerenderUserlists()

			self.keys.clear()
			for e in config.IGNORE_LIST:
				item = QListWidgetItem(f"{e}")
				item.ignore = f"{e}"
				self.keys.addItem(item)

			self.statusBar.showMessage("Ignore added")

	def remove_key(self):
		selected_item = self.keys.currentItem()
		if selected_item:
			i = selected_item.ignore
			config.IGNORE_LIST.remove(i)
			config.save_settings(config.CONFIG_FILE)
			self.parent.buildSettingsMenu()
			self.parent.reRenderAll(True)
			self.parent.rerenderUserlists()

			self.keys.clear()
			for e in config.IGNORE_LIST:
				item = QListWidgetItem(f"{e}")
				item.ignore = f"{e}"
				self.keys.addItem(item)

			self.statusBar.showMessage("Ignore removed")

	def refresh(self):
		self.keys.clear()
		for e in config.IGNORE_LIST:
			item = QListWidgetItem(f"{e}")
			item.ignore = f"{e}"
			self.keys.addItem(item)
		self.statusBar.showMessage(f"Displaying {len(config.IGNORE_LIST)} ignores")

	def closeEvent(self, event):

		self.parent.ignore_manager = None

		event.accept()
		self.close()

	def __init__(self,parent=None):
		super(Window,self).__init__(parent)

		self.parent = parent

		config.load_settings(config.CONFIG_FILE)
		
		self.window_type = IGNORE_WINDOW
		self.subwindow_id = str(uuid.uuid4())
		self.setWindowIcon(QIcon(HIDE_ICON))

		self.name = f"Ignores"
		self.setWindowTitle(f"Ignores")

		self.keys = QListWidget(self)
		self.keys.setTextElideMode(Qt.ElideRight)
		self.keys.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		for e in config.IGNORE_LIST:
			item = QListWidgetItem(f"{e}")
			item.ignore = f"{e}"
			self.keys.addItem(item)

		self.add = QPushButton("")
		self.add.setIcon(QIcon(PLUS_ICON))
		self.add.setToolTip("Add ignore")
		self.add.clicked.connect(self.add_key)
		self.add.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.add.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.add.setFlat(True)

		self.remove = QPushButton("")
		self.remove.setIcon(QIcon(MINUS_ICON))
		self.remove.setToolTip("Remove ignore")
		self.remove.clicked.connect(self.remove_key)
		self.remove.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.remove.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.remove.setFlat(True)

		self.exit = QPushButton("Close")
		self.exit.clicked.connect(self.close)

		self.statusBar = QStatusBar(self)
		self.statusBar.showMessage(f"Displaying {len(config.IGNORE_LIST)} ignores")

		buttonLayout = QHBoxLayout()
		buttonLayout.addWidget(self.add)
		buttonLayout.addWidget(self.remove)
		buttonLayout.addStretch()
		buttonLayout.addWidget(self.exit)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.keys)
		finalLayout.addLayout(buttonLayout)
		finalLayout.addWidget(self.statusBar)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(finalLayout)
		self.setCentralWidget(self.centralWidget)

		# self.setFixedSize(self.sizeHint())