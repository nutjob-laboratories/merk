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

	def settings_update_sample(self):
		if not hasattr(self,"sample"): return
		if self.sample.toPlainText()!='':
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
			self.settings_update_sample()
		else:
			self.epoch = False
			self.settings_update_sample()

	def setLine(self):

		dtype = self.line.itemText(self.line.currentIndex())
		if dtype=='Newline': self.linedelim = "\n"
		if dtype=='CRLF': self.linedelim = "\r\n"
		if dtype=='Tab': self.linedelim = "\t"
		if dtype=='Comma': self.linedelim = ","
		if dtype=='Pipe': self.linedelim = "|"

		self.settings_update_sample()

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

		self.settings_update_sample()

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

		self.status_details.setText(f"<small><b>Click a log to view its contents</b></small>")
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

		self.status_details.setText(f"<small><b>Select a log to export</b></small>")
		self.filesize.setText(' ')
		self.filetype.setText('<b>to export</b>')
		self.file_icon.setPixmap(self.blank_file)
		self.filename.setText('<b>Select a log</b>')

		self.menubar.setEnabled(False)
		self.format.setEnabled(False)
		self.typeLabel.setEnabled(False)
		self.type.setEnabled(False)
		self.lineLabel.setEnabled(False)
		self.line.setEnabled(False)
		self.time.setEnabled(False)
		self.button_export.setEnabled(False)

		self.sample.setPlainText('')

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

		if self.parent.dark_mode:
			self.style = styles.loadDarkDefault()
		else:
			self.style = styles.loadDefault()

		self.packlist = QListWidget(self)

		self.packlist.setContextMenuPolicy(Qt.CustomContextMenu)
		self.packlist.customContextMenuRequested.connect(self.show_context_menu)
		self.packlist.itemClicked.connect(self.on_item_selected)
		self.packlist.itemDoubleClicked.connect(self.on_item_clicked)

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
		self.button_export.setEnabled(False)

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
		self.status_details = QLabel(f"<small><b>Select a log to export</b></small>")
		self.status.addPermanentWidget(self.status_details,1)

		self.filesize = QLabel(' ')
		self.filetype = QLabel('<b>to export</b>')
		self.filename = QLabel('<b>Select a log</b>')

		self.file_icon = QLabel()
		self.file_icon.setPixmap(self.blank_file)

		buttons = QHBoxLayout()
		buttons.addStretch()
		buttons.addWidget(self.button_export)
		buttons.addStretch()

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
		self.verticalSplitter.setHandleWidth(2)

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
				<b>Click on a log name</b> to open that log for exporting.
				<b>Hover the mouse</b> over the log name to see what IRC network that log is
				from. <b>Right click on a log name</b> to view other options.
				To export a log, double click on a log, choose export options, and click the
				<b>Save Export</b> button. Click <b>Close</b> to close the manager.
				</small>
				""")
			self.windowDescription.setWordWrap(True)
			self.windowDescription.setAlignment(Qt.AlignJustify)

		self.tabs = QTabWidget()
		self.tabs.setStyleSheet("QTabBar::tab { font-weight: bold; }")
		self.tabs.tabBar().hide()

		self.horizontalSplitter = QSplitter(Qt.Horizontal)
		self.horizontalSplitter.addWidget(self.packlist)
		self.horizontalSplitter.addWidget(self.tabs)

		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("AAAAAAAAAAAAAAAAAAAAAAAAA")
		mwidth = self.tabs.width()
		self.horizontalSplitter.setSizes([wwidth,mwidth])

		self.horizontalSplitter.setStretchFactor(0, 0)
		self.horizontalSplitter.setStretchFactor(1, 1)

		self.export_options = QWidget()
		self.tabs.addTab(self.export_options, "Export")

		self.export_options.setLayout(bottomLayout)

		self.buildList()

		managerLayout = QHBoxLayout()
		managerLayout.addWidget(self.horizontalSplitter)

		finalLayout = QVBoxLayout()
		if not self.simplified: finalLayout.addWidget(self.windowDescription)
		finalLayout.addLayout(managerLayout)

		# Set the layout as the central widget
		self.centralWidget = QWidget()
		self.centralWidget.setLayout(finalLayout)
		self.setCentralWidget(self.centralWidget)

		self.adjustSize()

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

	def generateStylesheet(self,obj,fore,back):

		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def on_item_selected(self, item):

		loadLog = logs.readLog(item.network,item.channel,logs.LOG_DIRECTORY)
		self.log = loadLog

		size_bytes = os.path.getsize(item.file)

		self.status_details.setText(f'<small><b>{item.file}</b></small>')
		self.filesize.setText(f'<small><b>{convert_size(size_bytes)}</b></small>')

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

		self.sample.setPlainText('')
		self.button_export.setEnabled(False)

	def on_item_clicked(self, item):

		QApplication.setOverrideCursor(Qt.WaitCursor)

		size_bytes = os.path.getsize(item.file)

		self.status_details.setText(f'<small><b>{item.file}</b></small>')
		self.filesize.setText(f'<small><b>{convert_size(size_bytes)}</b></i></small>')

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
		self.button_export.setEnabled(True)

		QApplication.restoreOverrideCursor()

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
			self.settings_update_sample()
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
			self.settings_update_sample()
			return
