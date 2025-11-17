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

from ..resources import *

class Window(QMainWindow):

	def view_export(self):
		item = self.packlist.currentItem()
		if item==None: return ''

		elog = item.file
		channel = item.channel
		dlog = self.delimiter
		llog = self.linedelim
		do_json = self.do_json
		do_epoch = self.epoch

		if not do_json:
			return logs.dumpLog(elog,dlog,llog,do_epoch)
		else:
			return logs.dumpLogJson(elog,do_epoch)

	def update_sample(self):
		if not hasattr(self,"sample"): return
		self.sample.setPlainText(self.view_export())

	def do_export(self):

		item = self.packlist.currentItem()

		elog = item.file
		channel = item.channel
		dlog = self.delimiter
		llog = self.linedelim
		do_json = self.do_json
		do_epoch = self.epoch
		if not do_json:
			options = QFileDialog.Options()
			options |= QFileDialog.DontUseNativeDialog
			fileName, _ = QFileDialog.getSaveFileName(self,f"Export {channel} log as...",INSTALL_DIRECTORY,"Text File (*.txt);;All Files (*)", options=options)
			if fileName:
				_, file_extension = os.path.splitext(fileName)
				if file_extension=='':
					efl = len("txt")+1
					if fileName[-efl:].lower()!=f".txt": fileName = fileName+f".txt"
				dump = logs.dumpLog(elog,dlog,llog,do_epoch)
				code = open(fileName,mode="w",encoding="utf-8")
				code.write(dump)
				code.close()
		else:
			options = QFileDialog.Options()
			options |= QFileDialog.DontUseNativeDialog
			fileName, _ = QFileDialog.getSaveFileName(self,f"Export {channel} log as...",INSTALL_DIRECTORY,"JSON File (*.json);;All Files (*)", options=options)
			if fileName:
				_, file_extension = os.path.splitext(fileName)
				if file_extension=='':
					efl = len("json")+1
					if fileName[-efl:].lower()!=f".json": fileName = fileName+f".json"
				dump = logs.dumpLogJson(elog,do_epoch)
				code = open(fileName,mode="w",encoding="utf-8")
				code.write(dump)
				code.close()

	def clickTime(self,state):
		if state == Qt.Checked:
			self.epoch = True
			self.update_sample()
		else:
			self.epoch = False
			self.update_sample()

	def setLine(self):

		dtype = self.line.itemText(self.line.currentIndex())
		if dtype=='Newline': self.linedelim = "\n"
		if dtype=='CRLF': self.linedelim = "\r\n"
		if dtype=='Tab': self.linedelim = "\t"
		if dtype=='Comma': self.linedelim = ","
		if dtype=='Pipe': self.linedelim = "|"

		self.update_sample()

	def setType(self):

		dtype = self.type.itemText(self.type.currentIndex())
		if dtype=='Space': self.delimiter = ' '
		if dtype=='Double Space': self.delimiter = '  '
		if dtype=='Tab': self.delimiter = "\t"
		if dtype=='Comma': self.delimiter = ','
		if dtype=='Colon': self.delimiter = ':'
		if dtype=='Double Colon': self.delimiter = '::'
		if dtype=='Pipe': self.delimiter = '|'
		if dtype=='Double Pipe': self.delimiter = '||'

		self.update_sample()

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

			channel_action = QAction(QIcon(CLIPBOARD_ICON),"Copy channel name to clipboard", self)
			channel_action.triggered.connect(lambda: self.copy_channel_to_clipboard(item))
			menu.addAction(channel_action)

			menu.addSeparator()

			delete_action = QAction(QIcon(CLOSE_ICON),"Delete log file", self)
			delete_action.triggered.connect(lambda: self.delete_log(item))
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

	def delete_log(self, item):
		msgBox = QMessageBox()
		if item.channel[:1]!='#' and item.channel[:1]!='&' and item.channel[:1]!='!' and item.channel[:1]!='+':
			msgBox.setIconPixmap(QPixmap(PRIVATE_WINDOW_ICON))
		else:
			msgBox.setIconPixmap(QPixmap(CHANNEL_WINDOW_ICON))
		msgBox.setWindowIcon(QIcon(LOG_ICON))
		msgBox.setText("Are you sure you want to delete this log?")
		msgBox.setWindowTitle("Delete log for "+item.channel+" ("+item.network+")")
		msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

		rval = msgBox.exec()
		if rval != QMessageBox.Cancel:
			self.packlist.takeItem(self.packlist.row(item))
			os.remove(item.file)

		self.chat.clear()
		self.status_details.setText(f"<small><b>Click a log to view its contents</b></small>")
		self.filestats.setText(' ')
		self.filesize.setText(' ')
		self.filetype.setText('<b>to export</b>')
		self.filename.setText('<b>Select a log</b>')
		self.packlist.clearSelection()
		self.menubar.setEnabled(False)
		self.format.setEnabled(False)
		self.typeLabel.setEnabled(False)
		self.type.setEnabled(False)
		self.lineLabel.setEnabled(False)
		self.line.setEnabled(False)
		self.time.setEnabled(False)
		self.button_export.setEnabled(False)
		self.file_icon.setPixmap(self.blank_file)

		self.sample.setPlainText('')

	def closeEvent(self, event):

		# Make sure the MDI window is closed
		self.parent.closeSubWindow(self.subwindow_id)
		self.parent.log_manager = None

		event.accept()
		self.close()

	def linkClicked(self,url):
		if url.host():
			# It's an internet link, so open it
			# in the default browser
			sb = self.chat.verticalScrollBar()
			og_value = sb.value()

			QDesktopServices.openUrl(url)
			self.chat.setSource(QUrl())
			sb.setValue(og_value)

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
		self.chat.clear()
		self.search.clear()
		self.log = []

		self.status_details.setText(f"<small><b>Select a log to view or export</b></small>")
		self.filesize.setText(' ')
		self.filestats.setText(" ")
		self.filetype.setText('<b>to export</b>')
		self.file_icon.setPixmap(self.blank_file)
		self.log_render_status.setText(' ')
		self.filename.setText('<b>Select a log</b>')

		self.menubar.setEnabled(False)
		self.format.setEnabled(False)
		self.typeLabel.setEnabled(False)
		self.type.setEnabled(False)
		self.lineLabel.setEnabled(False)
		self.line.setEnabled(False)
		self.time.setEnabled(False)
		self.button_export.setEnabled(False)

		self.update_sample()

		servers = []
		others = []

		for x in os.listdir(self.logdir):
			if x.endswith(".json"):
				log = os.path.join(self.logdir, x)
				if os.path.isfile(log):
					p = os.path.basename(log).replace('.json','')

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
							item.setToolTip(f"{channel} on {netname} network")

							if channel[:1]!='#' and channel[:1]!='&' and channel[:1]!='!' and channel[:1]!='+':
								item.setIcon(QIcon(PRIVATE_WINDOW_ICON))
								item.type = PRIVATE_WINDOW
							else:
								item.setIcon(QIcon(CHANNEL_WINDOW_ICON))
								item.type = CHANNEL_WINDOW

							item.file = log
							item.network = netname
							item.channel = channel
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

		self.do_json = True
		self.epoch = False
		self.log = []
		self.export_format = 'json'

		self.window_type = LOG_MANAGER_WINDOW
		self.subwindow_id = str(uuid.uuid4())
		self.setWindowIcon(QIcon(LOG_ICON))

		if target!=None:
			self.name = f"Log Manager ({self.target})"
			self.setWindowTitle(f"Log Manager ({self.target})")
		else:
			self.name = "Log Manager"
			self.setWindowTitle("Log Manager")

		self.channel_file = QPixmap(CHANNEL_ICON)
		self.private_file = QPixmap(PRIVATE_ICON)
		self.blank_file = QPixmap(LOG_ICON)

		icon_size = QSize(35, 35)
		self.channel_file = self.channel_file.scaled(icon_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
		self.private_file = self.private_file.scaled(icon_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
		self.blank_file = self.blank_file.scaled(icon_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

		self.style = styles.loadDefault()

		self.packlist = QListWidget(self)

		self.packlist.setContextMenuPolicy(Qt.CustomContextMenu)
		self.packlist.customContextMenuRequested.connect(self.show_context_menu)
		self.packlist.itemClicked.connect(self.on_item_selected)
		self.packlist.itemDoubleClicked.connect(self.on_item_clicked)

		self.chat = QTextBrowser(self)
		self.chat.setFocusPolicy(Qt.NoFocus)
		self.chat.anchorClicked.connect(self.linkClicked)
		self.chat.setReadOnly(True)

		delimLayout = QFormLayout()

		self.type = QComboBox(self)
		self.type.activated.connect(self.setType)
		self.type.addItem("Tab")
		self.type.addItem("Space")
		self.type.addItem("Double Space")
		self.type.addItem("Comma")
		self.type.addItem("Colon")
		self.type.addItem("Double Colon")
		self.type.addItem("Pipe")
		self.type.addItem("Double Pipe")
		f = self.type.font()
		f.setBold(True)
		self.type.setFont(f)

		self.typeLabel = QLabel("Field Delimiter:")
		delimLayout.addRow(self.typeLabel, self.type)

		self.line = QComboBox(self)
		self.line.activated.connect(self.setLine)
		self.line.addItem("Newline")
		self.line.addItem("CRLF")
		self.line.addItem("Tab")
		self.line.addItem("Comma")
		self.line.addItem("Pipe")
		f = self.line.font()
		f.setBold(True)
		self.line.setFont(f)

		self.lineLabel = QLabel("Entry Delimiter:")
		delimLayout.addRow(self.lineLabel, self.line)

		self.button_export=QPushButton("  Save Export  ")
		self.button_export.clicked.connect(self.do_export)

		self.button_close = QPushButton("Close")
		self.button_close.clicked.connect(self.close)

		self.time = QCheckBox("Epoch format for date/time ",self)
		self.time.stateChanged.connect(self.clickTime)
		self.time.toggle()

		self.time.setLayoutDirection(Qt.RightToLeft)

		self.menubar = QMenuBar(self)
		BOLD_FONT = self.font()
		BOLD_FONT.setBold(True)

		fileMenu = self.menubar.addMenu ("Export log as...")

		self.menuJson = QAction(QIcon(self.parent.round_checked_icon),"JSON",self)
		self.menuJson.triggered.connect(lambda state,s="json": self.toggleSetting(s))
		fileMenu.addAction(self.menuJson)

		self.menuText = QAction(QIcon(self.parent.round_unchecked_icon),"Text",self)
		self.menuText.triggered.connect(lambda state,s="text": self.toggleSetting(s))
		fileMenu.addAction(self.menuText)

		self.format = QLabel("JSON file")
		self.format.setFont(BOLD_FONT)

		self.type.setEnabled(False)
		self.typeLabel.setEnabled(False)
		self.line.setEnabled(False)
		self.lineLabel.setEnabled(False)

		formatLayout = QHBoxLayout()
		formatLayout.addWidget(self.menubar)
		formatLayout.addWidget(self.format)

		exportLayout = QVBoxLayout()
		exportLayout.addLayout(formatLayout)
		exportLayout.addLayout(delimLayout)
		exportLayout.addWidget(self.time)
		exportLayout.setSizeConstraint(QLayout.SetFixedSize)

		self.menubar.setEnabled(False)
		self.format.setEnabled(False)
		self.typeLabel.setEnabled(False)
		self.type.setEnabled(False)
		self.lineLabel.setEnabled(False)
		self.line.setEnabled(False)
		self.time.setEnabled(False)
		self.button_export.setEnabled(False)

		self.status = self.statusBar()
		self.status.setStyleSheet("QStatusBar::item { border: none; }")
		self.status_details = QLabel(f"<small><b>Select a log to view or export</b></small>")
		self.status.addPermanentWidget(self.status_details,1)

		background,foreground = styles.parseBackgroundAndForegroundColor(self.style["all"])

		self.chat.setStyleSheet(self.generateStylesheet('QTextBrowser',foreground,background))

		self.filestats = QLabel(' ')
		self.filesize = QLabel(' ')
		self.filetype = QLabel('<b>to export</b>')
		self.filename = QLabel('<b>Select a log</b>')

		self.file_icon = QLabel()
		self.file_icon.setPixmap(self.blank_file)

		buttons = QHBoxLayout()
		buttons.addStretch()
		buttons.addWidget(self.button_export)
		buttons.addStretch()
		
		mainLayout = QHBoxLayout()
		mainLayout.addWidget(self.chat)

		sideLayout = QVBoxLayout()
		sideLayout.addLayout(exportLayout)
		sideLayout.addStretch()

		detailsLayout = QVBoxLayout()
		detailsLayout.addWidget(self.filename)
		detailsLayout.addWidget(self.filetype)
		detailsLayout.addWidget(self.filesize)

		iconLayout = QVBoxLayout()
		iconLayout.addWidget(self.file_icon)

		self.sample = QPlainTextEdit(self)
		self.sample.setReadOnly(True)

		size_policy = self.sample.sizePolicy()
		size_policy.setVerticalPolicy(QSizePolicy.Expanding)
		self.sample.setSizePolicy(size_policy)

		self.update_sample()

		fileinfoLayout = QHBoxLayout()
		fileinfoLayout.addLayout(iconLayout)
		fileinfoLayout.addLayout(detailsLayout)
		fileinfoLayout.addStretch()
		fileinfoLayout.setSizeConstraint(QLayout.SetFixedSize)

		otherLayout = QHBoxLayout()
		otherLayout.addLayout(sideLayout)

		bottomLayout2 = QVBoxLayout()
		bottomLayout2.addLayout(fileinfoLayout)
		bottomLayout2.addLayout(otherLayout)

		file_info = QWidget()
		file_info.setLayout(bottomLayout2)
		
		bottomLayout4 = QVBoxLayout()
		bottomLayout4.addWidget(self.sample)

		file_display = QWidget()
		file_display.setLayout(bottomLayout4)

		self.verticalSplitter = QSplitter(Qt.Vertical)
		self.verticalSplitter.addWidget(file_info)
		self.verticalSplitter.addWidget(file_display)
		self.verticalSplitter.setStretchFactor(0, 0)
		self.verticalSplitter.setStretchFactor(1, 1)
		self.verticalSplitter.setHandleWidth(3)

		if self.parent.dark_mode:
			self.verticalSplitter.setStyleSheet("QSplitter::handle{background-color: lightGray;}")
		else:
			self.verticalSplitter.setStyleSheet("QSplitter::handle{background-color: darkGray;}")

		bottomLayout3 = QVBoxLayout()
		bottomLayout3.addWidget(self.verticalSplitter)
		bottomLayout3.addLayout(buttons)

		bottomLayout=QHBoxLayout()
		bottomLayout.addLayout(bottomLayout3)

		if not self.simplified:
			self.windowDescription = QLabel(f"""
				<small>
				Here, you can manage all installed logs. <b>Double click on a log name</b> to open that log for viewing
				in the log display. <b>Hover the mouse</b> over the log name to see what IRC network that log is
				from. <b>Right click on a log name</b> to view other options, like opening the log in a text editor,
				opening the log's location, copying information about the log to the clipboard, or deleting the log.
				To export a log, <b>click on a log name</b> to select the log, <b>click on the "Export" tab</b>,
				choose export options, and click the <b>Export</b> button. Click <b>Close</b> to close the manager.
				</small>
				""")
			self.windowDescription.setWordWrap(True)
			self.windowDescription.setAlignment(Qt.AlignJustify)

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

		self.log_display = QWidget()
		log_index = self.tabs.addTab(self.log_display, "View ")

		self.search = QLineEdit()
		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("AAAAAAAAAAAAAAAAAAAA")
		self.search.setFixedWidth(wwidth)
		self.search.returnPressed.connect(self.on_search)
		self.search.setPlaceholderText("Search terms...")

		self.forward = QPushButton("")
		self.forward.setIcon(QIcon(NEXT_ICON))
		self.forward.setToolTip("Next result")
		self.forward.clicked.connect(self.on_search)
		self.forward.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.forward.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))

		self.backward = QPushButton("")
		self.backward.setIcon(QIcon(BACK_ICON))
		self.backward.setToolTip("Previous result")
		self.backward.clicked.connect(self.on_back)
		self.backward.setFixedSize(QSize(config.INTERFACE_BUTTON_SIZE,config.INTERFACE_BUTTON_SIZE))
		self.backward.setIconSize(QSize(config.INTERFACE_BUTTON_ICON_SIZE,config.INTERFACE_BUTTON_ICON_SIZE))

		swlayout = QHBoxLayout()
		swlayout.addWidget(self.search)
		swlayout.addWidget(self.backward)
		swlayout.addWidget(self.forward)
		swlayout.setContentsMargins(0,0,0,0)
		
		self.swidget = QWidget()
		self.swidget.setLayout(swlayout)

		self.tabs.tabBar().setTabButton(log_index, QTabBar.RightSide, self.swidget)

		self.export_options = QWidget()
		self.tabs.addTab(self.export_options, "Export")

		self.log_display.setLayout(mainLayout)
		self.export_options.setLayout(bottomLayout)

		self.log_render_status = QLabel(" ")

		self.buildList()

		sbar = QVBoxLayout()
		sbar.addWidget(self.filestats)
		sbar.addWidget(self.log_render_status)

		buttonbar = QHBoxLayout()
		buttonbar.addLayout(sbar)
		buttonbar.addStretch()
		buttonbar.addWidget(self.button_close)

		managerLayout = QHBoxLayout()
		managerLayout.addWidget(self.horizontalSplitter)

		finalLayout = QVBoxLayout()
		if not self.simplified: finalLayout.addWidget(self.windowDescription)
		finalLayout.addLayout(managerLayout)
		finalLayout.addLayout(buttonbar)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(finalLayout)
		self.setCentralWidget(self.centralWidget)

		self.adjustSize()

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

	def on_search(self):
		search_text = self.search.text()

		if search_text:
			found = self.chat.find(search_text, QTextDocument.FindFlags())
			if not found:
				cursor = self.chat.textCursor()
				cursor.movePosition(QTextCursor.Start)
				self.chat.setTextCursor(cursor)
				self.chat.find(search_text, QTextDocument.FindFlags())

	def on_back(self):
		search_text = self.search.text()
		flags = QTextDocument.FindFlags() | QTextDocument.FindBackward

		if search_text:
			found = self.chat.find(search_text, flags)
			if not found:
				cursor = self.chat.textCursor()
				cursor.movePosition(QTextCursor.Start)
				self.chat.setTextCursor(cursor)
				self.chat.find(search_text, flags)

	def generateStylesheet(self,obj,fore,back):

		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def on_item_selected(self, item):

		loadLog = logs.readLog(item.network,item.channel,logs.LOG_DIRECTORY)
		self.log = loadLog

		chat_length = 0

		for line in self.log:
			if line.type!=DATE_MESSAGE: chat_length = chat_length + 1

		if len(self.log)>config.LOG_MANAGER_MAXIMUM_LOAD_SIZE:
			self.log_render_status.setText(f"<small>Double click to view last {config.LOG_MANAGER_MAXIMUM_LOAD_SIZE} lines of log</small>")
		else:
			self.log_render_status.setText(f"<small>Double click to view log</small>")

		size_bytes = os.path.getsize(item.file)

		self.status_details.setText(f'<small><b>{item.file}</b></small>')
		self.filesize.setText(f'<small><b>{convert_size(size_bytes)}</b></small>')
		self.filestats.setText(f"<small><b>{item.channel} ({item.network})</b> {chat_length} lines</b></small>")

		self.menubar.setEnabled(True)
		self.format.setEnabled(True)
		self.time.setEnabled(True)

		if self.export_format=='json':
			self.typeLabel.setEnabled(False)
			self.type.setEnabled(False)
			self.lineLabel.setEnabled(False)
			self.line.setEnabled(False)
		else:
			self.typeLabel.setEnabled(True)
			self.type.setEnabled(True)
			self.lineLabel.setEnabled(True)
			self.line.setEnabled(True)

		self.button_export.setEnabled(True)

		if item.type==CHANNEL_WINDOW:
			self.filetype.setText(f"<small><b>Channel log</b></small>")
			self.file_icon.setPixmap(self.channel_file)
		elif item.type==PRIVATE_WINDOW:
			self.filetype.setText(f"<small><b>Private chat log</b></small>")
			self.file_icon.setPixmap(self.private_file)

		self.filename.setText(f"<b>{item.channel}</b>")

		self.update_sample()

	def on_item_clicked(self, item):

		self.tabs.setCurrentWidget(self.log_display)

		start_time = time.time()
		QApplication.setOverrideCursor(Qt.WaitCursor)

		loadLog = logs.readLog(item.network,item.channel,logs.LOG_DIRECTORY)
		self.log = loadLog

		big_log = False

		if len(self.log)>config.LOG_MANAGER_MAXIMUM_LOAD_SIZE:
			big_log = True
			self.log_render_status.setText(f'<small>Rendering last {config.LOG_MANAGER_MAXIMUM_LOAD_SIZE} lines of log for viewing...</small>')
			self.log = self.log[-config.LOG_MANAGER_MAXIMUM_LOAD_SIZE:]
		else:
			self.log_render_status.setText(f'<small>Rendering log for viewing...</small>')

		QApplication.processEvents()

		chat_length = 0

		if config.SHOW_DATES_IN_LOGS:
			cdate = None
			marked = []
			for e in self.log:
				ndate = datetime.fromtimestamp(e.timestamp).strftime('%A %B %d, %Y')
				if cdate!=ndate:
					cdate = ndate
					m = Message(DATE_MESSAGE,'',cdate)
					marked.append(m)
				marked.append(e)
			self.log = marked

		self.chat.clear()
		for line in self.log:
			if line.type!=DATE_MESSAGE: chat_length = chat_length + 1
			t = render.render_message(line,self.style,None,True)
			self.chat.append(t)

		end_time = time.time()
		rendertime = end_time - start_time

		size_bytes = os.path.getsize(item.file)

		self.status_details.setText(f'<small><b>{item.file}</b></small>')
		self.filesize.setText(f'<small><b>{convert_size(size_bytes)}</b></small>')
		self.filestats.setText(f"<small><b>{item.channel} ({item.network})</b> {chat_length} lines, {rendertime:.4f} seconds</small>")
		if big_log:
			self.log_render_status.setText(f'<small>Viewing last {config.LOG_MANAGER_MAXIMUM_LOAD_SIZE} lines of log</small>')
		else:
			self.log_render_status.setText('<small>Viewing full log</small>')

		self.menubar.setEnabled(True)
		self.format.setEnabled(True)
		self.time.setEnabled(True)

		if self.export_format=='json':
			self.typeLabel.setEnabled(False)
			self.type.setEnabled(False)
			self.lineLabel.setEnabled(False)
			self.line.setEnabled(False)
		else:
			self.typeLabel.setEnabled(True)
			self.type.setEnabled(True)
			self.lineLabel.setEnabled(True)
			self.line.setEnabled(True)

		self.button_export.setEnabled(True)

		if item.type==CHANNEL_WINDOW:
			self.filetype.setText(f"<small><b>Channel log</b></small>")
			self.file_icon.setPixmap(self.channel_file)
		elif item.type==PRIVATE_WINDOW:
			self.filetype.setText(f"<small><b>Private chat log</b></small>")
			self.file_icon.setPixmap(self.private_file)

		self.filename.setText(f"<b>{item.channel}</b>")

		QApplication.restoreOverrideCursor()

		self.update_sample()

	def toggleSetting(self,setting):

		self.export_format = setting

		if setting=='json':
			self.menuJson.setIcon(QIcon(self.parent.round_checked_icon))
			self.menuText.setIcon(QIcon(self.parent.round_unchecked_icon))
			self.do_json = True
			self.type.setEnabled(False)
			self.typeLabel.setEnabled(False)
			self.line.setEnabled(False)
			self.lineLabel.setEnabled(False)
			self.format.setText("JSON file")
			self.update_sample()
			return

		if setting=='text':
			self.menuJson.setIcon(QIcon(self.parent.round_unchecked_icon))
			self.menuText.setIcon(QIcon(self.parent.round_checked_icon))
			self.do_json = False
			self.type.setEnabled(True)
			self.typeLabel.setEnabled(True)
			self.line.setEnabled(True)
			self.lineLabel.setEnabled(True)
			self.format.setText("ASCII text file")
			self.update_sample()
			return
