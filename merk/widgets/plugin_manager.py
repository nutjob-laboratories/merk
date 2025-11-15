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
from .. import plugins

import uuid
import operator
import shutil
from pathlib import Path

class Window(QMainWindow):

	def add_plugin(self):
		if not config.ENABLE_PLUGIN_EDITOR: return
		self.parent.newEditorPlugin()

	def remove_plugin(self):

		item = self.plugin_list.currentItem()
		if hasattr(item,"dummy"):
			if item.dummy: return
		else:
			return

		msgBox = QMessageBox()
		msgBox.setIconPixmap(QPixmap(PLUGIN_ICON))
		msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
		msgBox.setText(f"Are you sure you want to delete {item.NAME} {item.VERSION}?")
		msgBox.setWindowTitle("Remove plugin")
		msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

		rval = msgBox.exec()
		if rval == QMessageBox.Cancel:
			pass
		else:
			if os.path.exists(item.filename):
				try:
					os.remove(item.filename)
					QMessageBox.information(self, 'Success', f'File "{item.filename}" deleted successfully.')
				except OSError as e:
					QMessageBox.critical(self, 'Error', f'Error deleting file: {e}')
			else:
				QMessageBox.warning(self, 'Warning', f'File "{item.filename}" not found.')

			errors = plugins.load_plugins(self.parent)
			if len(errors)>0:
				msgBox = QMessageBox()
				msgBox.setIconPixmap(QPixmap(PLUGIN_ICON))
				msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
				if len(errors)>1:
					msgBox.setText("There were errors loading plugins!")
				else:
					msgBox.setText("There was an error loading plugins!")
				msgBox.setInformativeText("\n".join(errors))
				msgBox.setWindowTitle("Plugin load error")
				msgBox.setStandardButtons(QMessageBox.Ok)
				msgBox.exec()
			self.refresh()

	def reload_plugins(self):
		errors = plugins.load_plugins(self.parent)
		if len(errors)>0:
			msgBox = QMessageBox()
			msgBox.setIconPixmap(QPixmap(PLUGIN_ICON))
			msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
			if len(errors)>1:
				msgBox.setText("There were errors loading plugins!")
			else:
				msgBox.setText("There was an error loading plugins!")
			msgBox.setInformativeText("\n".join(errors))
			msgBox.setWindowTitle("Plugin load error")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()
		self.refresh()

	def refresh(self):
		self.plugin_list.clear()
		others = []
		for obj in plugins.PLUGINS:
			filename = obj._filename
			basename = obj._basename
			events = obj._events
			event_list = obj._event_list
			size = prettySize(obj._size)
			NAME = obj.NAME
			VERSION = obj.VERSION
			AUTHOR = obj.AUTHOR
			SOURCE = obj.SOURCE

			item = QListWidgetItem(f"{NAME} {VERSION}")
			item.setToolTip(f"Author: {AUTHOR}\nURL: {SOURCE}\nFilename: {basename}\nEvents: {events}\nSize: {size}")
			item.filename = obj._filename
			item.basename = obj._basename
			item.events = obj._events
			item.event_list = obj._event_list
			item.size = obj._size
			item.NAME = obj.NAME
			item.VERSION = obj.VERSION
			item.AUTHOR = obj.AUTHOR
			item.SOURCE = obj.SOURCE
			item.dummy = False
			others.append(item)

			others = sorted(others,key=operator.attrgetter("NAME","VERSION"))
		for e in others:
			self.plugin_list.addItem(e)

		if len(others)==0:
			item = QListWidgetItem(f"No plugins installed")
			item.dummy = True
			self.plugin_list.addItem(item)

	def on_item_clicked(self, item):
		if not config.ENABLE_PLUGIN_EDITOR: return
		if item.dummy: return
		self.parent.newEditorPluginFile(item.filename)

	def import_plugin(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Import File", str(Path.home()), f"MERK Plugin (*.py);;All Files (*)", options=options)
		if fileName:
			base = os.path.basename(fileName)
			imported_file = os.path.join(plugins.PLUGIN_DIRECTORY,base)

			import_file = True
			if os.path.exists(imported_file) or os.path.isfile(imported_file):
				import_file = False

				msgBox = QMessageBox()
				msgBox.setIconPixmap(QPixmap(PLUGIN_ICON))
				msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
				msgBox.setText("Plugin file already exists! Overwrite?")
				msgBox.setWindowTitle("Overwrite File")
				msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

				rval = msgBox.exec()
				if rval == QMessageBox.Cancel:
					pass
				else:
					import_file = True

			if import_file:
				try:
					shutil.move(fileName, imported_file)
					self.reload_plugins()
				except FileNotFoundError:
					QMessageBox.critical(self, 'Error', f"Source file '{fileName}' not found.")
				except Exception as e:
					QMessageBox.critical(self, 'Error', f'Error importing file: {e}')

	def closeEvent(self, event):

		self.parent.plugin_manager = None

		event.accept()
		self.close()

	def toggleEnableEditor(self):
		if config.ENABLE_PLUGIN_EDITOR: 
			self.add.show()
		else:
			self.add.hide()

	def __init__(self,parent=None):
		super(Window,self).__init__(parent)

		self.parent = parent

		config.load_settings(config.CONFIG_FILE)
		
		self.window_type = PLUGIN_WINDOW
		self.subwindow_id = str(uuid.uuid4())
		self.setWindowIcon(QIcon(PLUGIN_ICON))

		self.name = f"Plugins"
		self.setWindowTitle(f"Plugins")

		self.plugin_list = QListWidget(self)
		self.plugin_list.setTextElideMode(Qt.ElideRight)
		self.plugin_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.plugin_list.setSelectionMode(QListWidget.SingleSelection)

		self.plugin_list.itemDoubleClicked.connect(self.on_item_clicked)

		self.refresh()

		self.add = QPushButton("")
		self.add.setIcon(QIcon(PLUS_ICON))
		self.add.setToolTip("Create new plugin")
		self.add.clicked.connect(self.add_plugin)
		self.add.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.add.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.add.setFlat(True)

		if not config.ENABLE_PLUGIN_EDITOR: self.add.hide()

		self.remove = QPushButton("")
		self.remove.setIcon(QIcon(MINUS_ICON))
		self.remove.setToolTip("Delete plugin")
		self.remove.clicked.connect(self.remove_plugin)
		self.remove.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.remove.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.remove.setFlat(True)

		self.plugImport = QPushButton("")
		self.plugImport.setIcon(QIcon(IMPORT_ICON))
		self.plugImport.setToolTip("Import plugin")
		self.plugImport.clicked.connect(self.import_plugin)
		self.plugImport.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.plugImport.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.plugImport.setFlat(True)

		self.brefresh = QPushButton("")
		self.brefresh.setIcon(QIcon(REFRESH_ICON))
		self.brefresh.setToolTip("Reload plugins")
		self.brefresh.clicked.connect(self.reload_plugins)
		self.brefresh.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.brefresh.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.brefresh.setFlat(True)

		self.exit = QPushButton("Close")
		self.exit.clicked.connect(self.close)

		buttonLayout = QHBoxLayout()
		buttonLayout.addWidget(self.add)
		buttonLayout.addWidget(self.remove)
		buttonLayout.addWidget(self.plugImport)
		buttonLayout.addWidget(self.brefresh)
		buttonLayout.addStretch()
		buttonLayout.addWidget(self.exit)

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.plugin_list)
		finalLayout.addLayout(buttonLayout)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(finalLayout)
		self.setCentralWidget(self.centralWidget)

		# self.setFixedSize(self.sizeHint())