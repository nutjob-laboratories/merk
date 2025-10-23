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
		x = SetBind(self)
		e = x.get_script_information(self)
		if e:
			seq = e[0]
			cmd = e[1]

			if is_valid_shortcut_sequence(seq):
				r = self.parent.add_shortcut(seq,cmd)
				if r==GOOD_SHORTCUT:
					pass
					# t = Message(SYSTEM_MESSAGE,'',f"Bind for \"{seq}\" added (executes \"{cmd}\")")
				elif r==SHORTCUT_IN_USE:
					pass
					# t = Message(ERROR_MESSAGE,'',f"\"{seq}\" is already in use as a shortcut")
				else:
					pass
					# t = Message(ERROR_MESSAGE,'',f"\"{seq}\" is not a valid key sequence")
				# self.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				pass
				# t = Message(ERROR_MESSAGE,'',f"\"{seq}\" is not a valid key sequence or is already in use")
				# self.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			self.keys.clear()
			for e in self.parent.shortcuts:
				item = QListWidgetItem(f"{e[0]} - {e[2]}")
				item.seq = f"{e[0]}"
				item.cmd = f"{e[2]}"
				self.keys.addItem(item)

	def remove_key(self):
		selected_item = self.keys.currentItem()
		if selected_item:
			self.parent.remove_shortcut(selected_item.seq)

			self.keys.clear()
			for e in self.parent.shortcuts:
				item = QListWidgetItem(f"{e[0]} - {e[2]}")
				item.seq = f"{e[0]}"
				item.cmd = f"{e[2]}"
				self.keys.addItem(item)

	def refresh(self):
		self.keys.clear()
		for e in self.parent.shortcuts:
			item = QListWidgetItem(f"{e[0]} - {e[2]}")
			item.seq = f"{e[0]}"
			item.cmd = f"{e[2]}"
			self.keys.addItem(item)

	def closeEvent(self, event):

		self.parent.hotkey_manager = None

		event.accept()
		self.close()

	def save_keys(self):
		config.HOTKEYS = {}
		for e in self.parent.shortcuts:
			config.HOTKEYS[e[0]]=e[2]
		config.save_settings(config.CONFIG_FILE)

	def __init__(self,parent=None):
		super(Window,self).__init__(parent)

		self.parent = parent
		
		self.window_type = HOTKEY_WINDOW
		self.subwindow_id = str(uuid.uuid4())
		self.setWindowIcon(QIcon(INPUT_ICON))

		self.name = f"Hotkeys"
		self.setWindowTitle(f"Hotkeys")

		self.keys = QListWidget(self)
		self.keys.setTextElideMode(Qt.ElideRight)
		self.keys.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		for e in self.parent.shortcuts:
			item = QListWidgetItem(f"{e[0]} - {e[2]}")
			item.seq = f"{e[0]}"
			item.cmd = f"{e[2]}"
			self.keys.addItem(item)

		self.add = QPushButton("")
		self.add.setIcon(QIcon(PLUS_ICON))
		self.add.setToolTip("Add hotkey")
		self.add.clicked.connect(self.add_key)
		self.add.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.add.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.add.setFlat(True)

		self.remove = QPushButton("")
		self.remove.setIcon(QIcon(MINUS_ICON))
		self.remove.setToolTip("Remove hotkey")
		self.remove.clicked.connect(self.remove_key)
		self.remove.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.remove.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.remove.setFlat(True)

		self.save = QPushButton("")
		self.save.setIcon(QIcon(SAVEFILE_ICON))
		self.save.setToolTip("Save hotkeys")
		self.save.clicked.connect(self.save_keys)
		self.save.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.save.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.save.setFlat(True)

		self.exit = QPushButton("Close")
		self.exit.clicked.connect(self.close)

		buttonLayout = QHBoxLayout()
		buttonLayout.addWidget(self.save)
		buttonLayout.addWidget(self.add)
		buttonLayout.addWidget(self.remove)
		buttonLayout.addStretch()
		buttonLayout.addWidget(self.exit)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.keys)
		finalLayout.addLayout(buttonLayout)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(finalLayout)
		self.setCentralWidget(self.centralWidget)

		# self.setFixedSize(self.sizeHint())