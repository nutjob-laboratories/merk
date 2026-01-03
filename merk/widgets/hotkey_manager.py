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
from . import extendedmenuitem

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
					self.parent.save_shortcuts()
				elif r==SHORTCUT_IN_USE:
					QMessageBox.critical(self, 'Error', f'Hotkey \"{seq}\" is already in use.')
				else:
					QMessageBox.critical(self, 'Error', f'\"{seq}\" is not a valid hotkey.')
			else:
				QMessageBox.warning(self, 'Warning', f'Hotkey \"{seq}\" was not added.')

			self.refresh()

	def remove_key(self):
		selected_item = self.keys.currentItem()
		if hasattr(selected_item,'dummy'):
			if selected_item.dummy: return
		else:
			return
		if selected_item:
			self.parent.remove_shortcut(selected_item.seq)
			self.parent.save_shortcuts()
			self.refresh()

	def refresh(self):
		self.keys.clear()
		for e in self.parent.shortcuts:
			item = QListWidgetItem()
			item.seq = f"{e[0]}"
			item.cmd = f"{e[2]}"
			item.dummy = False

			widget = extendedmenuitem.hotkeyItem(f"{e[0]}",f"{e[2]}")
			item.setSizeHint(widget.sizeHint())

			self.keys.addItem(item)
			self.keys.setItemWidget(item, widget)

		if len(self.parent.shortcuts)==0:
			item = QListWidgetItem()
			item.dummy = True
			item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
			widget = extendedmenuitem.ignoreItem("No hotkeys set")
			item.setSizeHint(widget.sizeHint())
			self.keys.addItem(item)
			self.keys.setItemWidget(item, widget)
			self.remove.hide()
		else:
			self.remove.show()

	def closeEvent(self, event):

		self.parent.hotkey_manager = None

		event.accept()
		self.close()

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
					self.parent.save_shortcuts()
				elif r==SHORTCUT_IN_USE:
					QMessageBox.critical(self, 'Error', f'Hotkey \"{seq}\" is already in use.')
				else:
					QMessageBox.critical(self, 'Error', f'\"{seq}\" is not a valid hotkey.')
			else:
				QMessageBox.warning(self, 'Warning', f'Hotkey \"{seq}\" was not added.')

			self.refresh()

	def toggleTop(self):
		if bool(self.parent.windowFlags() & Qt.WindowStaysOnTopHint):
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
			self.show()
		else:
			self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
			self.show()
		
	def __init__(self,parent=None):
		super(Window,self).__init__(parent)

		self.parent = parent
		
		self.window_type = HOTKEY_WINDOW
		self.subwindow_id = str(uuid.uuid4())
		self.setWindowIcon(QIcon(HOTKEY_ICON))

		self.name = f"Hotkeys"
		self.setWindowTitle(f"Hotkey Manager")

		self.keys = QListWidget(self)
		self.keys.setTextElideMode(Qt.ElideRight)
		self.keys.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.keys.itemDoubleClicked.connect(self.on_item_clicked)

		if self.parent.dark_mode:
			self.keys.setStyleSheet(f"""
				QListWidget::item:selected {{
					background: darkGray;
				}}
			""")
		else:
			self.keys.setStyleSheet(f"""
				QListWidget::item:selected {{
					background: lightGray;
				}}
			""")

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
		self.remove.hide()

		self.refresh()

		buttonLayout = QHBoxLayout()
		buttonLayout.addWidget(self.add)
		buttonLayout.addWidget(self.remove)
		buttonLayout.addStretch()

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.keys)
		finalLayout.addLayout(buttonLayout)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(finalLayout)
		self.setCentralWidget(self.centralWidget)

		if config.MANAGERS_ALWAYS_ON_TOP:
			self.setWindowFlags(self.windowFlags() | Qt.WindowType.Dialog)

		if bool(self.parent.windowFlags() & Qt.WindowStaysOnTopHint):
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
