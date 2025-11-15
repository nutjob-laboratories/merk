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
from .. import dialog

import uuid

class Window(QMainWindow):

	def add_key(self):
		x = dialog.SetBind(self)
		e = x.get_script_information(self)
		if e:
			seq = e[0]
			cmd = e[1]

			if is_valid_shortcut_sequence(seq):
				r = self.parent.add_shortcut(seq,cmd)
				if r==GOOD_SHORTCUT:
					self.statusBar.showMessage("Hotkey added")
				elif r==SHORTCUT_IN_USE:
					self.statusBar.showMessage(f"\"{seq}\" is already in use")
				else:
					self.statusBar.showMessage(f"\"{seq}\" is not valid")
			else:
				self.statusBar.showMessage(f"\"{seq}\" was not added")

			self.show_status = False
			self.refresh()

	def remove_key(self):
		selected_item = self.keys.currentItem()
		if hasattr(selected_item,'dummy'):
			if selected_item.dummy: return
		else:
			return
		if selected_item:
			self.parent.remove_shortcut(selected_item.seq)
			self.refresh()
			self.statusBar.showMessage("Hotkey removed")

	def refresh(self):
		self.keys.clear()
		for e in self.parent.shortcuts:
			item = QListWidgetItem(f"{e[0]} - {e[2]}")
			item.seq = f"{e[0]}"
			item.cmd = f"{e[2]}"
			item.dummy = False
			self.keys.addItem(item)
		if self.show_status:
			self.statusBar.showMessage(f"Displaying {len(self.parent.shortcuts)} hotkeys")
		else:
			self.show_status = True

		if len(self.parent.shortcuts)==0:
			item = QListWidgetItem(f"No hotkeys found")
			item.dummy = True
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
		self.statusBar.showMessage("Saved hotkeys")

	def on_item_clicked(self, item):
		if hasattr(item,'dummy'):
			if item.dummy: return
		else:
			return
		x = dialog.SetBind(self,item.seq,item.cmd)
		e = x.get_script_information(self,item.seq,item.cmd)
		if e:
			seq = e[0]
			cmd = e[1]

			self.parent.remove_shortcut(seq)

			if is_valid_shortcut_sequence(seq):
				r = self.parent.add_shortcut(seq,cmd)
				if r==GOOD_SHORTCUT:
					self.statusBar.showMessage("Hotkey edited")
				elif r==SHORTCUT_IN_USE:
					self.statusBar.showMessage(f"\"{seq}\" is already in use")
				else:
					self.statusBar.showMessage(f"\"{seq}\" is not valid")
			else:
				self.statusBar.showMessage(f"\"{seq}\" was not added")

			self.show_status = False
			self.refresh()

	def __init__(self,parent=None):
		super(Window,self).__init__(parent)

		self.parent = parent
		self.show_status = True
		
		self.window_type = HOTKEY_WINDOW
		self.subwindow_id = str(uuid.uuid4())
		self.setWindowIcon(QIcon(HOTKEY_ICON))

		self.name = f"Hotkeys"
		self.setWindowTitle(f"Hotkeys")

		self.keys = QListWidget(self)
		self.keys.setTextElideMode(Qt.ElideRight)
		self.keys.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.keys.itemDoubleClicked.connect(self.on_item_clicked)

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

		self.statusBar = QStatusBar(self)
		self.statusBar.showMessage(f"Displaying {len(self.parent.shortcuts)} hotkeys")

		self.refresh()

		buttonLayout = QHBoxLayout()
		buttonLayout.addWidget(self.save)
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