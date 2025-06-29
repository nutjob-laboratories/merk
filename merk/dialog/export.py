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

from .. import config
from .. import styles
from .. import render

from ..resources import *

class Dialog(QDialog):

	@staticmethod
	def get_name_information(logdir,parent=None,simplified=False,app=None):
		dialog = Dialog(logdir,parent,simplified,app)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

		self.close()

	def return_info(self):

		item = self.packlist.currentItem()
		if item:
			retval = [item.file,item.channel,self.delimiter,self.linedelim, self.do_json, self.epoch]
		else:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText("No log selected")
			msg.setWindowTitle("Error")
			msg.exec_()
			return None

		return retval

	def clickTime(self,state):
		if state == Qt.Checked:
			self.epoch = True
		else:
			self.epoch = False

	def setLine(self):

		dtype = self.line.itemText(self.line.currentIndex())
		if dtype=='Newline': self.linedelim = "\n"
		if dtype=='CRLF': self.linedelim = "\r\n"
		if dtype=='Tab': self.linedelim = "\t"
		if dtype=='Comma': self.linedelim = ","
		if dtype=='Pipe': self.linedelim = "|"

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

	def closeEvent(self, event):

		if self.app != None:
			self.app.quit()

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

		self.exportBox.setTitle("Select a log to export")
		self.chat.clear()
		self.status_details.setText(f"<small><b>Click a log to view its contents</b></small>")
		self.filestats.setText('<small><i>Right click on a log for more options</i></small>')
		self.filesize.setText('')
		self.packlist.clearSelection()
		self.menubar.setEnabled(False)
		self.format.setEnabled(False)
		self.typeLabel.setEnabled(False)
		self.type.setEnabled(False)
		self.lineLabel.setEnabled(False)
		self.line.setEnabled(False)
		self.time.setEnabled(False)
		self.exportBox.setEnabled(False)
		self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)

	def __init__(self,logdir,parent=None,simplified=False,app=None):
		super(Dialog,self).__init__(parent)

		self.parent = parent
		self.logdir = logdir
		self.app = app
		self.delimiter = "\t"
		self.linedelim = "\n"
		self.simplified = simplified

		self.do_json = True
		self.epoch = False
		self.log = []

		self.setWindowTitle("Log Manager")
		self.setWindowIcon(QIcon(LOG_ICON))

		self.style = styles.loadDefault()

		self.packlist = QListWidget(self)

		self.packlist.setContextMenuPolicy(Qt.CustomContextMenu)
		self.packlist.customContextMenuRequested.connect(self.show_context_menu)
		self.packlist.itemClicked.connect(self.on_item_clicked)

		fm = QFontMetrics(self.font())
		wwidth = fm.horizontalAdvance("AAAAAAAAAAAAAAAAAAAA")
		self.packlist.setMaximumWidth(wwidth)
		wwidth = fm.horizontalAdvance("AAAAAAAAAAAAAAA")
		self.packlist.setMinimumWidth(wwidth)

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

						if is_a_server_log:
							item = QListWidgetItem(netname+":"+channel+" (SERVER)")
							item.file = log
							servers.append(item)
						else:
							netname = netname.upper()

							#item = QListWidgetItem(channel+" ("+netname+")")
							item = QListWidgetItem(channel)
							item.setToolTip(netname+" network")

							if channel[:1]!='#' and channel[:1]!='&' and channel[:1]!='!' and channel[:1]!='+':
								item.setIcon(QIcon(PRIVATE_WINDOW_ICON))
							else:
								item.setIcon(QIcon(CHANNEL_WINDOW_ICON))

							item.file = log
							item.network = netname
							item.channel = channel
							others.append(item)

		# Sort channel/chat logs by network, THEN chat name
		others = sorted(others,key=operator.attrgetter("network","channel"))
		# Sort servers by name
		servers = sorted(servers, key=lambda obj: obj.text())

		# Add the now sorted logs to the list widget
		for e in others:
			self.packlist.addItem(e)

		for e in servers:
			self.packlist.addItem(e)

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

		# Buttons
		self.buttons = QDialogButtonBox(self)
		self.buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)

		self.buttons.button(QDialogButtonBox.Ok).setText("Export")
		self.buttons.button(QDialogButtonBox.Cancel).setText("Close")

		self.time = QCheckBox("Epoch format for date/time ",self)
		self.time.stateChanged.connect(self.clickTime)
		self.time.toggle()

		self.time.setLayoutDirection(Qt.RightToLeft)

		self.menubar = QMenuBar(self)
		BOLD_FONT = self.font()
		BOLD_FONT.setBold(True)

		fileMenu = self.menubar.addMenu ("Export log as...")

		self.menuJson = QAction(QIcon(ROUND_CHECKED_ICON),"JSON",self)
		self.menuJson.triggered.connect(lambda state,s="json": self.toggleSetting(s))
		fileMenu.addAction(self.menuJson)

		self.menuText = QAction(QIcon(ROUND_UNCHECKED_ICON),"Text",self)
		self.menuText.triggered.connect(lambda state,s="text": self.toggleSetting(s))
		fileMenu.addAction(self.menuText)

		self.format = QLabel("JSON file")
		self.format.setFont(BOLD_FONT)

		self.type.setVisible(False)
		self.typeLabel.setVisible(False)
		self.line.setVisible(False)
		self.lineLabel.setVisible(False)

		formatLayout = QHBoxLayout()
		formatLayout.addWidget(self.menubar)
		formatLayout.addWidget(self.format)

		exportLayout = QVBoxLayout()
		exportLayout.addLayout(formatLayout)
		exportLayout.addLayout(delimLayout)
		exportLayout.addWidget(self.time)
		exportLayout.addStretch()

		self.exportBox = QGroupBox("Select a log to export")
		self.exportBox.setAlignment(Qt.AlignHCenter)
		self.exportBox.setLayout(exportLayout)

		self.menubar.setEnabled(False)
		self.format.setEnabled(False)
		self.typeLabel.setEnabled(False)
		self.type.setEnabled(False)
		self.lineLabel.setEnabled(False)
		self.line.setEnabled(False)
		self.time.setEnabled(False)
		self.exportBox.setEnabled(False)
		self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)

		f = self.exportBox.font()
		f.setBold(True)
		self.exportBox.setFont(f)

		self.chat = QTextBrowser(self)
		self.chat.setFocusPolicy(Qt.NoFocus)
		# self.chat.anchorClicked.connect(self.linkClicked)
		self.chat.setReadOnly(True)
		self.chat.setMinimumWidth(600)

		self.status = QStatusBar()
		self.status.setStyleSheet("QStatusBar::item { border: none; }")
		self.status_details = QLabel(f"<small><b>Click a log to view its contents</b></small>")
		self.status.addPermanentWidget(self.status_details,1)

		background,foreground = styles.parseBackgroundAndForegroundColor(self.style["all"])

		self.chat.setStyleSheet(self.generateStylesheet('QTextBrowser',foreground,background))

		self.filestats = QLabel('<small><i>Right click on a log for more options</i></small>')
		self.filesize = QLabel('')

		mainLayout = QHBoxLayout()
		mainLayout.addWidget(self.packlist)
		mainLayout.addWidget(self.chat)

		labelLayout = QHBoxLayout()
		labelLayout.addStretch()
		labelLayout.addWidget(self.filestats)

		labelLayout2 = QHBoxLayout()
		labelLayout2.addStretch()
		labelLayout2.addWidget(self.filesize)

		buttonLayout = QVBoxLayout()
		buttonLayout.addLayout(labelLayout)
		buttonLayout.addLayout(labelLayout2)
		buttonLayout.addStretch()
		buttonLayout.addWidget(self.buttons)

		bottomLayout = QHBoxLayout()
		bottomLayout.addWidget(self.exportBox)
		bottomLayout.addLayout(buttonLayout)

		if not self.simplified:
			self.windowDescription = QLabel(f"""
				<small>
				Here, you can manage all installed logs. <b>Click on a log name</b> to open that log for viewing
				in the log display. <b>Hover the mouse</b> over the log name to see what IRC network that log is
				from. <b>Right click on a log name</b> to view other options, like opening the log in a text editor,
				opening the log's location, copying information about the log to the clipboard, or deleting the log.
				To export a log, <b>click on a log name</b> to select the log, choose export options in the
				box on the bottom left, and click the <b>Export</b> button. Click <b>Close</b> to close the manager.
				</small>
				""")
			self.windowDescription.setWordWrap(True)
			self.windowDescription.setAlignment(Qt.AlignJustify)

		finalLayout = QVBoxLayout()
		if not self.simplified: finalLayout.addWidget(self.windowDescription)
		finalLayout.addLayout(mainLayout)
		finalLayout.addLayout(bottomLayout)
		finalLayout.addWidget(self.status)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

	def generateStylesheet(self,obj,fore,back):

		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def on_item_clicked(self, item):
		start_time = time.time()
		QApplication.setOverrideCursor(Qt.WaitCursor)

		loadLog = logs.readLog(item.network,item.channel,logs.LOG_DIRECTORY)
		self.log = loadLog

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
			t = render.render_message(line,self.style,None)
			self.chat.append(t)

		end_time = time.time()
		rendertime = end_time - start_time

		size_bytes = os.path.getsize(item.file)

		self.exportBox.setTitle(item.text())
		self.status_details.setText(f'<small><b>{item.file}</b></small>')
		self.filesize.setText(f'<small><b>{convert_size(size_bytes)}</b></small>')
		self.filestats.setText(f"<small><b>{len(self.log)} lines, {rendertime:.4f} seconds</b></small>")

		self.menubar.setEnabled(True)
		self.format.setEnabled(True)
		self.typeLabel.setEnabled(True)
		self.type.setEnabled(True)
		self.lineLabel.setEnabled(True)
		self.line.setEnabled(True)
		self.time.setEnabled(True)
		self.exportBox.setEnabled(True)
		self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)

		QApplication.restoreOverrideCursor()

	def toggleSetting(self,setting):

		if setting=='json':
			self.menuJson.setIcon(QIcon(ROUND_CHECKED_ICON))
			self.menuText.setIcon(QIcon(ROUND_UNCHECKED_ICON))
			self.do_json = True
			self.type.setVisible(False)
			self.typeLabel.setVisible(False)
			self.line.setVisible(False)
			self.lineLabel.setVisible(False)
			self.format.setText("JSON file")
			return

		if setting=='text':
			self.menuJson.setIcon(QIcon(ROUND_UNCHECKED_ICON))
			self.menuText.setIcon(QIcon(ROUND_CHECKED_ICON))
			self.do_json = False
			self.type.setVisible(True)
			self.typeLabel.setVisible(True)
			self.line.setVisible(True)
			self.lineLabel.setVisible(True)
			self.format.setText("ASCII text file")
			return
