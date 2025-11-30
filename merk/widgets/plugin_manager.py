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
from . import extendedmenuitem

import emoji

HAS_CONSOLE = emoji.emojize(config.PLUGIN_HAS_CONSOLE_MARKER,language="alias")

import uuid
import operator
import shutil
from pathlib import Path
import zipfile

class Window(QMainWindow):

	def do_export(self,item):
		if hasattr(item,"dummy"):
			if item.dummy: return
		else:
			return

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,f"Export {item.NAME} {item.VERSION}",str(Path.home()),f"ZIP Files (*.zip);;All Files (*)", options=options)
		if fileName:
			_, file_extension = os.path.splitext(fileName)
			if file_extension=='':
				efl = len("zip")+1
				if fileName[-efl:].lower()!=f".zip": fileName = fileName+f".zip"

				with zipfile.ZipFile(fileName, "w") as zipf:
					zipf.write(item.filename, arcname=os.path.basename(item.filename))
					if item.icon!=None: zipf.write(item.icon, arcname=os.path.basename(item.icon))

				QMessageBox.information(self, 'Success', f'Plugin archive "{os.path.basename(fileName)}" exported.')

	def export_plugin(self):
		item = self.plugin_list.currentItem()
		self.do_export(item)

	def import_zip(self,filename):

		if not config.OVERWRITE_PLUGINS_ON_IMPORT:
			overwrite = False
			ofiles = []
			try:
				with zipfile.ZipFile(filename, 'r') as zf:
					for member in zf.infolist():
						file_path = os.path.join(plugins.PLUGIN_DIRECTORY, member.filename)

						extract_file = False
						name_without_extension, extension = os.path.splitext(file_path)
						if extension.lower()=='.py' or extension.lower()=='.png': extract_file = True

						if config.IMPORT_SCRIPTS_IN_PLUGINS:
							sfile_path = os.path.join(commands.SCRIPTS_DIRECTORY, member.filename)
							name_without_extension, extension = os.path.splitext(sfile_path)
							if extension.lower()=='.merk': extract_file = True


						if extract_file:
							if os.path.exists(file_path):
								overwrite = True
								ofiles.append(file_path)
							if os.path.exists(sfile_path):
								overwrite = True
								ofiles.append(sfile_path)
			except zipfile.BadZipFile:
				QMessageBox.critical(self, 'Error', f"\"{filename}\" is not a valid zip file")
				return
			except FileNotFoundError:
				QMessageBox.critical(self, 'Error', f"Plugin archive \"{filename}\" not found.")
				return
			except Exception as e:
				QMessageBox.critical(self, 'Error', f'Error importing file: {e}')
				return
		else:
			overwrite = False
			ofiles = []

		if not config.OVERWRITE_PLUGINS_ON_IMPORT and overwrite==True:
			msgBox = QMessageBox()
			msgBox.setIconPixmap(QPixmap(PLUGIN_ICON))
			msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
			msgBox.setText("The following files already exist. Overwrite?")
			msgBox.setInformativeText("\n".join(ofiles))
			msgBox.setWindowTitle("Overwrite")
			msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

			rval = msgBox.exec()
			if rval == QMessageBox.Cancel:
				pass
			else:
				overwrite = False

		if not overwrite:
			try:
				with zipfile.ZipFile(filename, 'r') as zf:
					for member in zf.infolist():
						file_path = os.path.join(plugins.PLUGIN_DIRECTORY, member.filename)

						extract_file = False
						name_without_extension, extension = os.path.splitext(file_path)
						if extension.lower()=='.py' or extension.lower()=='.png': extract_file = True

						if extract_file: zf.extract(member, plugins.PLUGIN_DIRECTORY)

						if config.IMPORT_SCRIPTS_IN_PLUGINS:
							file_path = os.path.join(commands.SCRIPTS_DIRECTORY, member.filename)

							extract_file = False
							name_without_extension, extension = os.path.splitext(file_path)
							if extension.lower()=='.merk': extract_file = True

							if extract_file: zf.extract(member, commands.SCRIPTS_DIRECTORY)

			except zipfile.BadZipFile:
				QMessageBox.critical(self, 'Error', f"\"{filename}\" is not a valid zip file")
			except FileNotFoundError:
				QMessageBox.critical(self, 'Error', f"Plugin archive \"{filename}\" not found.")
			except Exception as e:
				QMessageBox.critical(self, 'Error', f'Error importing file: {e}')

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
		else:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Critical)
			msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
			msgBox.setText(f"Import failed! The following files in \"{os.path.basename(filename)}\" will overwrite existing files:")
			msgBox.setInformativeText("\n".join(ofiles))
			msgBox.setWindowTitle("Plugin import error")
			msgBox.setStandardButtons(QMessageBox.Ok)
			msgBox.exec()

	def add_plugin(self):
		if not config.ENABLE_PLUGIN_EDITOR: return
		self.parent.newEditorPlugin()

	def delete_plugin(self,item):
		multiple = []
		for obj in plugins.PLUGINS:
			if item.filename==obj._filename:
				multiple.append(f"{obj.NAME} {obj.VERSION}")

		if len(multiple)>1:
			pid = "plugins"
		else:
			pid = "plugin"

		msgBox = QMessageBox()
		msgBox.setIconPixmap(QPixmap(PLUGIN_ICON))
		msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
		msgBox.setText(f"Are you sure you want to delete \"{item.basename}\"?\nThis will remove the following {pid}:")
		if len(multiple)>0:
			msgBox.setInformativeText("\n".join(multiple))
		msgBox.setWindowTitle("Delete plugin")
		msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

		rval = msgBox.exec()
		if rval == QMessageBox.Cancel:
			pass
		else:
			if os.path.exists(item.filename):
				try:
					os.remove(item.filename)
					self.parent.closeConsole(item.plugin)
				except OSError as e:
					QMessageBox.critical(self, 'Error', f'Error deleting file: {e}')
			else:
				QMessageBox.warning(self, 'Warning', f'File "{item.basename}" not found.')

			if item.icon!=None:
				try:
					os.remove(item.icon)
				except OSError as e:
					QMessageBox.critical(self, 'Error', f'Error deleting file: {e}')

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

	def remove_plugin(self):

		item = self.plugin_list.currentItem()
		if hasattr(item,"dummy"):
			if item.dummy: return
		else:
			return

		self.delete_plugin(item)

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

	def update_console(self,plugin):
		for i in range(self.plugin_list.count()):
			item = self.plugin_list.item(i)

			if hasattr(item,"dummy"):
				if item.dummy: continue

			if item.plugin==plugin:

				subwindow,widget = self.parent.getConsole(plugin)
				if subwindow==None:
					console_tag = ''
				else:
					console_tag = f" {HAS_CONSOLE}"

				if is_url(item.SOURCE):
					author_tag = f"<b><a href=\"{item.SOURCE}\">{item.AUTHOR}</a></b>{console_tag}"
				else:
					author_tag = f"<b>{item.AUTHOR}</b>{console_tag}"

				name_tag = f"{item.NAME} {item.VERSION}"
				class_tag = f"<b>{item.classname}</b> in {item.basename}"

				widget = extendedmenuitem.pluginItem(
					name_tag,
					class_tag,
					author_tag,
					icon,48
				)
				self.plugin_list.setItemWidget(item, widget)

	def refresh(self):
		self.plugin_list.clear()
		for obj in plugins.PLUGINS:
			filename = obj._filename
			basename = obj._basename
			events = obj._events
			event_list = obj._event_list
			methods = obj._methods
			NAME = obj.NAME
			VERSION = obj.VERSION
			AUTHOR = obj.AUTHOR
			SOURCE = obj.SOURCE
			classname = obj._class
			icon = obj._icon
			uuid = obj._id
			size = prettySize(get_memory_size(obj))
			calls = obj._calls

			item = QListWidgetItem()
			item.setToolTip(f"Filename: {basename}\nEvents: {events}\nMethods: {methods}\nCallable methods: {calls}\nMemory: {size}")
			item.filename = obj._filename
			item.basename = obj._basename
			item.events = obj._events
			item.event_list = obj._event_list
			item.NAME = obj.NAME
			item.VERSION = obj.VERSION
			item.AUTHOR = obj.AUTHOR
			item.SOURCE = obj.SOURCE
			item.classname = classname
			item.methods = methods
			item.dummy = False
			item.icon = icon
			item.plugin = obj
			item.size = size

			subwindow,widget = self.parent.getConsole(item.plugin)
			if subwindow==None:
				console_tag = ''
			else:
				console_tag = f" {HAS_CONSOLE}"

			if is_url(SOURCE):
				author_tag = f"<b><a href=\"{SOURCE}\">{AUTHOR}</a></b>{console_tag}"
			else:
				author_tag = f"<b>{AUTHOR}</b>{console_tag}"

			name_tag = f"{NAME} {VERSION}"
			class_tag = f"<b>{classname}</b> in {basename}"

			widget = extendedmenuitem.pluginItem(
				name_tag,
				class_tag,
				author_tag,
				icon,48
			)

			item.setSizeHint(widget.sizeHint())

			self.plugin_list.addItem(item)
			self.plugin_list.setItemWidget(item, widget)

		if self.plugin_list.count()==0:
			item = QListWidgetItem()
			item.dummy = True
			item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

			widget = extendedmenuitem.ignoreItem("No plugins installed")
			item.setSizeHint(widget.sizeHint())
			self.plugin_list.addItem(item)
			self.plugin_list.setItemWidget(item, widget)

			self.plugin_list.clearSelection()

	def on_item_double_clicked(self, item):
		if not config.ENABLE_PLUGIN_EDITOR: return
		if item.dummy: return

		subwindow,widget = self.parent.getConsole(item.plugin)
		if subwindow!=None:
			if subwindow.isVisible():
				subwindow.close()
			else:
				subwindow.show()

	def import_plugin(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Import File", str(Path.home()), f"Zip Files (*.zip);;MERK Plugin (*.py);;All Files (*)", options=options)
		if fileName:
			base = os.path.basename(fileName)
			imported_file = os.path.join(plugins.PLUGIN_DIRECTORY,base)

			name_without_extension, extension = os.path.splitext(fileName)
			if extension.lower()=='.zip':
				self.import_zip(fileName)
			else:

				if not config.OVERWRITE_PLUGINS_ON_IMPORT:
					import_file = True
					if os.path.exists(imported_file) or os.path.isfile(imported_file):
						import_file = False

						msgBox = QMessageBox()
						msgBox.setIcon(QMessageBox.Critical)
						msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
						msgBox.setText(f"Import failed! \"{os.path.basename(fileName)}\" already exists in the plugin directory.")
						msgBox.setWindowTitle("Plugin import error")
						msgBox.setStandardButtons(QMessageBox.Ok)
						msgBox.exec()
				else:
					import_file = True

				if import_file:
					try:
						shutil.copy(fileName, imported_file)
						self.reload_plugins()
					except FileNotFoundError:
						QMessageBox.critical(self, 'Error', f"Source file '{fileName}' not found.")
					except Exception as e:
						QMessageBox.critical(self, 'Error', f'Error importing file: {e}')

	def closeEvent(self, event):

		self.parent.plugin_manager = None

		event.accept()
		self.close()

	def show_context_menu(self, position: QPoint):
		menu = QMenu(self)
		item = self.plugin_list.itemAt(position)

		if item is not None:
				if hasattr(item,"dummy"):
					if item.dummy==False:

						subwindow,widget = self.parent.getConsole(item.plugin)
						if subwindow!=None:
							edit_action = QAction(QIcon(WINDOW_ICON),"View console", self)
							edit_action.triggered.connect(lambda: self.on_item_double_clicked(item))
							menu.addAction(edit_action)

						edit_action = QAction(QIcon(SCRIPT_ICON),"Edit plugin", self)
						edit_action.triggered.connect(lambda: self.parent.openPythonEditor(item.filename))
						menu.addAction(edit_action)

						if not config.ENABLE_PLUGIN_EDITOR: edit_action.setVisible(False)

						export_action = QAction(QIcon(EXPORT_ICON),"Export plugin", self)
						export_action.triggered.connect(lambda: self.do_export(item))
						menu.addAction(export_action)

						menu.addSeparator()

						delete_action = QAction(QIcon(MINUS_ICON),"Uninstall plugin", self)
						delete_action.triggered.connect(lambda: self.delete_plugin(item))
						menu.addAction(delete_action)

						menu.exec_(self.plugin_list.mapToGlobal(position))

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

		config.load_settings(config.CONFIG_FILE)
		
		self.window_type = PLUGIN_WINDOW
		self.subwindow_id = str(uuid.uuid4())
		self.setWindowIcon(QIcon(PLUGIN_ICON))

		self.name = f"Plugins"
		self.setWindowTitle(f"Plugin Manager")

		self.plugin_list = QListWidget(self)
		self.plugin_list.setTextElideMode(Qt.ElideRight)
		self.plugin_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.plugin_list.setSelectionMode(QListWidget.SingleSelection)
		self.plugin_list.itemDoubleClicked.connect(self.on_item_double_clicked)
		self.plugin_list.setContextMenuPolicy(Qt.CustomContextMenu)
		self.plugin_list.customContextMenuRequested.connect(self.show_context_menu)

		if self.parent.dark_mode:
			self.plugin_list.setStyleSheet(f"""
				QListWidget::item:selected {{
					background: darkGray;
				}}
			""")
		else:
			self.plugin_list.setStyleSheet(f"""
				QListWidget::item:selected {{
					background: lightGray;
				}}
			""")

		self.menubar = self.menuBar()

		self.pluginMenu = self.menubar.addMenu("Plugins")

		self.menuNew = QAction(QIcon(PLUS_ICON),"Create new plugin",self)
		self.menuNew.triggered.connect(self.add_plugin)
		self.pluginMenu.addAction(self.menuNew)

		if not config.ENABLE_PLUGIN_EDITOR: self.menuNew.setVisible(False)

		self.menuImport = QAction(QIcon(IMPORT_ICON),"Install plugin",self)
		self.menuImport.triggered.connect(self.import_plugin)
		self.pluginMenu.addAction(self.menuImport)

		self.pluginMenu.addSeparator()

		entry = QAction(QIcon(FOLDER_ICON),"Plugins directory",self)
		entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+plugins.PLUGIN_DIRECTORY))))
		self.pluginMenu.addAction(entry)

		self.menuRefresh = QAction(QIcon(REFRESH_ICON),"Reload plugins",self)
		self.menuRefresh.triggered.connect(self.reload_plugins)
		self.pluginMenu.addAction(self.menuRefresh)

		self.pluginMenu.addSeparator()

		self.menuClose = QAction(QIcon(CLOSE_ICON),"Close",self)
		self.menuClose.triggered.connect(self.close)
		self.pluginMenu.addAction(self.menuClose)

		self.refresh()

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(self.plugin_list)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(finalLayout)
		self.setCentralWidget(self.centralWidget)

		self.resize(350,300)

		if bool(self.parent.windowFlags() & Qt.WindowStaysOnTopHint):
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
