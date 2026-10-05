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

import sys
import os
from pathlib import Path
import operator
import datetime
import time
from .. import logs
import uuid

from .. import config
from .. import styles
from .. import render
from .. import syntax

from ..resources import *

class Window(QMainWindow):

	def do_export_csv(self):

		item = self.packlist.currentItem()
		elog = item.file
		channel = item.channel
		if channel[0]=='#' or channel[0]=='&' or channel[0]=='+' or channel[0]=='!':
			def_filename = os.path.join(os.path.expanduser("~"),f"{channel[1:]}.csv")
		else:
			def_filename = os.path.join(os.path.expanduser("~"),f"{channel}.csv")

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,f"Export {channel} log as...",def_filename,"CSV File (*.csv);;All Files (*)", options=options)
		if fileName:
			_, file_extension = os.path.splitext(fileName)
			if file_extension=='':
				efl = len("csv")+1
				if fileName[-efl:].lower()!=f".csv": fileName = fileName+f".csv"
			dump = logs.dumpLogCSV(elog)
			code = open(fileName,mode="w",encoding="utf-8")
			code.write(dump)
			code.close()

	def do_export_human(self):

		item = self.packlist.currentItem()
		elog = item.file
		channel = item.channel
		if channel[0]=='#' or channel[0]=='&' or channel[0]=='+' or channel[0]=='!':
			def_filename = os.path.join(os.path.expanduser("~"),f"{channel[1:]}.txt")
		else:
			def_filename = os.path.join(os.path.expanduser("~"),f"{channel}.txt")

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,f"Export {channel} log as...",def_filename,"Text File (*.txt);;All Files (*)", options=options)
		if fileName:
			_, file_extension = os.path.splitext(fileName)
			if file_extension=='':
				efl = len("txt")+1
				if fileName[-efl:].lower()!=f".txt": fileName = fileName+f".txt"
			dump = logs.dumpLogHuman(elog,False,False)
			code = open(fileName,mode="w",encoding="utf-8")
			code.write(dump)
			code.close()

	def do_export_json(self):

		item = self.packlist.currentItem()
		elog = item.file
		channel = item.channel
		if channel[0]=='#' or channel[0]=='&' or channel[0]=='+' or channel[0]=='!':
			def_filename = os.path.join(os.path.expanduser("~"),f"{channel[1:]}.json")
		else:
			def_filename = os.path.join(os.path.expanduser("~"),f"{channel}.json")

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,f"Export {channel} log as...",def_filename,"JSON File (*.json);;All Files (*)", options=options)
		if fileName:
			_, file_extension = os.path.splitext(fileName)
			if file_extension=='':
				efl = len("json")+1
				if fileName[-efl:].lower()!=f".json": fileName = fileName+f".json"
			dump = logs.dumpLogJson(elog,True)
			code = open(fileName,mode="w",encoding="utf-8")
			code.write(dump)
			code.close()

	def closeEvent(self, event):

		self.parent.closeSubWindow(self.subwindow_id)
		self.parent.log_manager = None

		event.accept()
		self.close()

	def show_context_menu(self, position: QPoint):
		menu = QMenu(self)
		item = self.packlist.itemAt(position)

		if item is not None:

			open_action = QAction(QIcon(OPENFILE_ICON),"Open native JSON log", self)
			open_action.triggered.connect(lambda: self.open_item(item))
			menu.addAction(open_action)

			dir_action = QAction(QIcon(FOLDER_ICON),"Open log location", self)
			dir_action.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+logs.LOG_DIRECTORY))))
			menu.addAction(dir_action)

			file_action = QAction(QIcon(CLIPBOARD_ICON),"Copy file name to clipboard", self)
			file_action.triggered.connect(lambda: self.copy_file_to_clipboard(item))
			menu.addAction(file_action)

			channel_action = QAction(QIcon(CLIPBOARD_ICON),"Copy chat name to clipboard", self)
			channel_action.triggered.connect(lambda: self.copy_channel_to_clipboard(item))
			menu.addAction(channel_action)

			expMenu = menu.addMenu(QIcon(SAVEFILE_ICON),f"Export log to...")

			backup_action = QAction("Text", self)
			backup_action.triggered.connect(self.do_export_human)
			expMenu.addAction(backup_action)

			backup_action = QAction("JSON", self)
			backup_action.triggered.connect(self.do_export_json)
			expMenu.addAction(backup_action)

			backup_action = QAction("CSV", self)
			backup_action.triggered.connect(self.do_export_csv)
			expMenu.addAction(backup_action)

			backup_action = QAction(QIcon(SAVEFILE_ICON),"Back up log file", self)
			backup_action.triggered.connect(lambda: self.backup_log(item))
			menu.addAction(backup_action)

			if item.large_log==False:
				backup_action.setEnabled(False)
			else:
				f = backup_action.font()
				f.setBold(True)
				backup_action.setFont(f)

			menu.addSeparator()

			delete_action = QAction(QIcon(CLOSE_ICON),"Delete log file", self)
			delete_action.triggered.connect(lambda: self.delete_log(item))
			f = delete_action.font()
			f.setBold(True)
			delete_action.setFont(f)
			menu.addAction(delete_action)

			menu.exec_(self.packlist.mapToGlobal(position))

	def open_item(self,item):
		file_url = QUrl.fromLocalFile(item.file)
		QDesktopServices.openUrl(file_url)

	def copy_channel_to_clipboard(self,item):
		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard)
		cb.setText(f"{item.channel}", mode=cb.Clipboard)

	def copy_file_to_clipboard(self,item):
		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard)
		cb.setText(f"{item.file}", mode=cb.Clipboard)

	def backup_log(self,item):
		msgBox = QMessageBox()
		if item.channel[:1]!='#' and item.channel[:1]!='&' and item.channel[:1]!='!' and item.channel[:1]!='+':
			msgBox.setIconPixmap(QPixmap(PRIVATE_WINDOW_ICON))
		else:
			msgBox.setIconPixmap(QPixmap(CHANNEL_WINDOW_ICON))
		msgBox.setWindowIcon(QIcon(LOG_MENU_ICON))
		msgBox.setText("Are you sure you want to back up this log?")
		msgBox.setWindowTitle("Back up log for "+item.channel+" ("+item.network+")")

		default_button = msgBox.addButton(" Back up log ", QMessageBox.AcceptRole)
		msgBox.addButton(" Cancel ", QMessageBox.RejectRole)
		msgBox.setDefaultButton(default_button)

		f = default_button.font()
		f.setBold(True)
		default_button.setFont(f)

		rval = msgBox.exec()
		if rval != QMessageBox.RejectRole:

			options = QFileDialog.Options()
			options |= QFileDialog.DontUseNativeDialog
			fileName, _ = QFileDialog.getSaveFileName(self,f"Back up log as...",os.path.expanduser("~"),"Text File (*.txt);;All Files (*)", options=options)
			if fileName:
				_, file_extension = os.path.splitext(fileName)
				if file_extension=='':
					efl = len("txt")+1
					if fileName[-efl:].lower()!=f".txt": fileName = fileName+f".txt"

				QApplication.setOverrideCursor(Qt.WaitCursor)
				logs.backup_log_direct(item.file,fileName)
				QApplication.restoreOverrideCursor()
				self.buildList()

	def delete_log(self, item):
		msgBox = QMessageBox()
		if item.channel[:1]!='#' and item.channel[:1]!='&' and item.channel[:1]!='!' and item.channel[:1]!='+':
			msgBox.setIconPixmap(QPixmap(PRIVATE_WINDOW_ICON))
		else:
			msgBox.setIconPixmap(QPixmap(CHANNEL_WINDOW_ICON))
		msgBox.setWindowIcon(QIcon(LOG_MENU_ICON))
		msgBox.setText("Are you sure you want to delete this log?")
		msgBox.setWindowTitle("Delete log for "+item.channel+" ("+item.network+")")

		default_button = msgBox.addButton(" Delete log ", QMessageBox.AcceptRole)
		cancel_button = msgBox.addButton(" Cancel ", QMessageBox.RejectRole)
		msgBox.setDefaultButton(cancel_button)

		f = cancel_button.font()
		f.setBold(True)
		default_button.setFont(f)

		rval = msgBox.exec()
		if rval != QMessageBox.RejectRole:
			self.packlist.takeItem(self.packlist.row(item))
			os.remove(item.file)

		self.status_details.setText(f"<small><b>Click a log to view its contents</b></small>")

		self.dump.setText('')

	def closeEvent(self, event):

		# Make sure the MDI window is closed
		self.parent.closeSubWindow(self.subwindow_id)
		self.parent.log_manager = None

		event.accept()
		self.close()

	def setNewTarget(self,target):
		self.target = target

		if target!=None:
			self.name = f"Log Manager ({self.target})"
			self.setWindowTitle(f"Log Manager ({self.target})")
		else:
			self.name = "Log Manager"
			self.setWindowTitle("Log Manager")

		self.buildList()

	def buildList(self):

		self.packlist.clear()
		self.log = []

		self.status_details.setText(f"<small><b>Select a log</b></small>")

		servers = []
		others = []

		for x in os.listdir(self.logdir):
			if x.endswith(".json"):
				log = os.path.join(self.logdir, x)
				if os.path.isfile(log):
					p = os.path.basename(log).replace('.json','')
					p_size = convert_size(os.path.getsize(log))

					p = p.split(LOG_AND_STYLE_FILENAME_DELIMITER,1)
					if len(p)==2:
						netname = deescape_for_filename(p[0])
						channel = deescape_for_filename(p[1])

						is_a_server_log = False
						if len(netname)>1:
							if netname[0]=='#':
								is_a_server_log = True
								netname = netname[1:]

						add_to_list = True
						if self.target!=None:
							if self.target.lower()!=netname.lower(): add_to_list = False
							if self.target.lower() in channel.lower(): add_to_list = True

						if is_a_server_log:
							item = QListWidgetItem(netname+":"+channel+" (SERVER)")
							item.file = log
							if add_to_list: servers.append(item)
						else:
							netname = netname.upper()

							item = QListWidgetItem(channel)
							item.size = p_size
							item.setToolTip(f"{channel} on {netname} network ({item.size})")

							if channel[:1]!='#' and channel[:1]!='&' and channel[:1]!='!' and channel[:1]!='+':
								item.setIcon(QIcon(PRIVATE_WINDOW_ICON))
								item.type = PRIVATE_WINDOW
							else:
								item.setIcon(QIcon(CHANNEL_WINDOW_ICON))
								item.type = CHANNEL_WINDOW

							item.file = log
							item.network = netname
							item.channel = channel

							# Display large log files in red
							if os.path.getsize(log) >= config.LOG_WARNING_SIZE * 1024 * 1024:
								item.setForeground(QBrush(QColor('red')))
								f = item.font()
								f.setBold(True)
								item.setFont(f)
								item.large_log = True
							else:
								item.large_log = False

							if add_to_list: others.append(item)

		# Sort channel/chat logs by network, THEN chat name
		others = sorted(others,key=operator.attrgetter("network","channel"))
		# Sort servers by name
		servers = sorted(servers, key=lambda obj: obj.text())

		# Add the now sorted logs to the list widget
		for e in others:
			self.packlist.addItem(e)

		for e in servers:
			self.packlist.addItem(e)

	def __init__(self,logdir,parent=None,simplified=False,app=None,target=None):
		super(Window,self).__init__(parent)

		self.parent = parent
		self.logdir = logdir
		self.app = app
		self.delimiter = "\t"
		self.linedelim = "\n"
		self.simplified = simplified
		self.target = target

		self.log = []

		self.window_type = LOG_MANAGER_WINDOW
		self.subwindow_id = str(uuid.uuid4())
		self.setWindowIcon(QIcon(LOG_MENU_ICON))

		if target!=None:
			self.name = f"Log Manager ({self.target})"
			self.setWindowTitle(f"Log Manager ({self.target})")
		else:
			self.name = "Log Manager"
			self.setWindowTitle("Log Manager")

		if self.parent.dark_mode:
			self.style = styles.loadDarkDefault()
		else:
			self.style = styles.loadDefault()

		self.packlist = QListWidget(self)

		self.packlist.setContextMenuPolicy(Qt.CustomContextMenu)
		self.packlist.customContextMenuRequested.connect(self.show_context_menu)
		self.packlist.itemClicked.connect(self.on_item_clicked)

		delimLayout = QFormLayout()

		self.status = self.statusBar()
		self.status.setStyleSheet("QStatusBar::item { border: none; }")
		self.status_details = QLabel(f"<small><b>Select a log</b></small>")
		self.status.addPermanentWidget(self.status_details,1)

		self.dump = LogViewer()
		self.dump.setReadOnly(True)
		self.dump.setContextMenuPolicy(Qt.CustomContextMenu)
		self.dump.customContextMenuRequested.connect(self.dumpMenu)

		size_policy = self.dump.sizePolicy()
		size_policy.setVerticalPolicy(QSizePolicy.Expanding)
		self.dump.setSizePolicy(size_policy)

		# Highlight the log viewer display
		self.highlighter = syntax.IRCFullHighlighter(self.dump.document())

		dumpLayout = QVBoxLayout()
		dumpLayout.setSpacing(0)
		dumpLayout.addWidget(self.dump)

		self.tabs = QTabWidget()
		self.tabs.setStyleSheet("QTabBar::tab { font-weight: bold; }")

		self.horizontalSplitter = QSplitter(Qt.Horizontal)
		self.horizontalSplitter.addWidget(self.packlist)
		self.horizontalSplitter.addWidget(self.tabs)

		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("AAAAAAAAAAAAAAAAAAAAAAAAA")
		mwidth = self.tabs.width()
		self.horizontalSplitter.setSizes([wwidth,mwidth])

		self.horizontalSplitter.setStretchFactor(0, 0)
		self.horizontalSplitter.setStretchFactor(1, 1)

		self.dump_view = QWidget()
		log_index = self.tabs.addTab(self.dump_view, "")
		
		self.search = QLineEdit()
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("A"*30)
		self.search.setFixedWidth(wwidth)
		self.search.returnPressed.connect(self.on_search)
		self.search.setPlaceholderText("Search terms...")

		search_icon = QLabel()
		pixmap = QPixmap(LIST_ICON)
		pixmap = pixmap.scaled(config.INTERFACE_BUTTON_SIZE, config.INTERFACE_BUTTON_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		search_icon.setPixmap(pixmap)
		search_icon.setAlignment(Qt.AlignCenter)

		self.forward = QPushButton("")
		self.forward.setIcon(QIcon(NEXT_ICON))
		self.forward.setToolTip("Next result")
		self.forward.clicked.connect(self.on_search)
		self.forward.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.forward.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.forward.setFlat(True)
		self.forward.setStyleSheet("QPushButton:focus { border: none; outline: none; }")

		self.backward = QPushButton("")
		self.backward.setIcon(QIcon(PREVIOUS_ICON))
		self.backward.setToolTip("Previous result")
		self.backward.clicked.connect(self.on_back)
		self.backward.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.backward.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))
		self.backward.setFlat(True)
		self.backward.setStyleSheet("QPushButton:focus { border: none; outline: none; }")

		swlayout = QHBoxLayout()
		swlayout.addWidget(search_icon)
		swlayout.addWidget(self.search)
		swlayout.addWidget(self.backward)
		swlayout.addWidget(self.forward)
		swlayout.setContentsMargins(0,0,0,0)

		self.swidget = QWidget()
		self.swidget.setLayout(swlayout)

		self.tabs.tabBar().setTabButton(log_index, QTabBar.RightSide, self.swidget)

		self.dump_view.setLayout(dumpLayout)

		self.buildList()

		self.shortcut = QShortcut(QKeySequence("Ctrl+X"), self.dump)
		self.shortcut.activated.connect(self.copy_modified)

		managerLayout = QHBoxLayout()
		managerLayout.addWidget(self.horizontalSplitter)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(managerLayout)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(finalLayout)
		self.setCentralWidget(self.centralWidget)

		self.adjustSize()

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

	def dumpMenu(self,location):
		menu = QMenu(self.dump)

		cursor = self.dump.textCursor()
		has_selection = cursor.hasSelection()

		copy_action = QAction(QIcon(COPY_ICON),"Copy", menu)
		copy_action.setShortcut("Ctrl+C")
		copy_action.setEnabled(has_selection)

		copy_action.triggered.connect(self.copy)
		menu.addAction(copy_action)

		copy_action = QAction(QIcon(HIDE_MENU_ICON),"Copy plain text", menu)
		copy_action.setShortcut("Ctrl+X")
		copy_action.setEnabled(has_selection)

		copy_action.triggered.connect(self.copy_modified)
		menu.addAction(copy_action)

		menu.addSeparator()

		# Select all
		select_all_action = QAction(QIcon(SELECTALL_ICON),"Select All", menu)
		select_all_action.setShortcut("Ctrl+A")
		select_all_action.triggered.connect(self.dump.selectAll)
		menu.addAction(select_all_action)

		action = menu.exec_(self.dump.mapToGlobal(location))

	def copy(self):
		cursor = self.dump.textCursor()

		if not cursor.hasSelection():
			return

		text = cursor.selectedText()

		QApplication.clipboard().setText(text)

	def copy_modified(self):
		cursor = self.dump.textCursor()

		if not cursor.hasSelection():
			return

		text = cursor.selectedText()

		text = strip_color(text)

		QApplication.clipboard().setText(text)

	def generateStylesheet(self,obj,fore,back):

		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def on_search(self):
		search_text = self.search.text()

		if search_text:
			found = self.dump.find(search_text, QTextDocument.FindFlags())
			if not found:
				cursor = self.dump.textCursor()
				cursor.movePosition(QTextCursor.Start)
				self.dump.setTextCursor(cursor)
				self.dump.find(search_text, QTextDocument.FindFlags())

	def on_back(self):
		search_text = self.search.text()
		flags = QTextDocument.FindFlags() | QTextDocument.FindBackward

		if search_text:
			found = self.dump.find(search_text, flags)
			if not found:
				cursor = self.dump.textCursor()
				cursor.movePosition(QTextCursor.Start)
				self.dump.setTextCursor(cursor)
				self.dump.find(search_text, flags)

	def on_item_clicked(self, item):

		QApplication.setOverrideCursor(Qt.WaitCursor)

		# Notify the user that we're loading the log
		self.status_details.setText(f'<small><b>Loading log for viewing...</b></small>')
		self.repaint()

		if item.type==PRIVATE_WINDOW:
			det = f"Private chat with <b>{item.channel}</b> on <b>{item.network}</b>"
		else:
			det = f"Channel chat in <b>{item.channel}</b> on <b>{item.network}</b>"

		if item.large_log:
			self.status_details.setText(f'<small>{det} - <b>{item.file}</b> (<span style="color: red;">{item.size}</span>)</small>')
		else:
			self.status_details.setText(f'<small>{det} - <b>{item.file}</b> ({item.size})</small>')

		self.dump.setText(logs.dumpLogHuman(item.file,True))

		QApplication.restoreOverrideCursor()