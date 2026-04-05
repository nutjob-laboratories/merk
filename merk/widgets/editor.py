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

import uuid
import os
import fnmatch
import re
import os
from collections import Counter
from pathlib import Path
import shutil
import zipfile

from ..resources import *
from .. import dialog
from .. import config
from .. import syntax
from .. import commands
from .. import user
from .. import plugins
from .text_separator import textSeparatorLabel,textSeparator
from .extendedmenuitem import MenuLabel,menuHtml

class Window(QMainWindow):

	def show_context_menu(self,pos):

		menu = self.editor.createStandardContextMenu()

		menu.addSeparator()

		smenu = menu.addMenu(QIcon(PRIVATE_ICON),"Insert user info")

		entry = QAction(QIcon(PRIVATE_ICON),"Nickname",self)
		entry.triggered.connect(lambda state,u=f"{user.NICKNAME}": self.insertIntoEditor(u))
		smenu.addAction(entry)

		entry = QAction(QIcon(PRIVATE_ICON),"Alternate",self)
		entry.triggered.connect(lambda state,u=f"{user.ALTERNATE}": self.insertIntoEditor(u))
		smenu.addAction(entry)

		entry = QAction(QIcon(PRIVATE_ICON),"Username",self)
		entry.triggered.connect(lambda state,u=f"{user.USERNAME}": self.insertIntoEditor(u))
		smenu.addAction(entry)

		entry = QAction(QIcon(PRIVATE_ICON),"Realname",self)
		entry.triggered.connect(lambda state,u=f"{user.REALNAME}": self.insertIntoEditor(u))
		smenu.addAction(entry)

		servers = self.parent.getAllServerWindows()
		if len(servers)>0:
			smenu = menu.addMenu(QIcon(CONNECT_ICON),"Insert server name")
			for window in servers:
				c = window.widget()
				entry = QAction(QIcon(CONSOLE_ICON),c.name,self)
				entry.triggered.connect(lambda state,u=f"{c.name}": self.insertIntoEditor(u))
				smenu.addAction(entry)

				entry = QAction(QIcon(CONNECT_ICON),f"{c.client.server}:{c.client.port}",self)
				entry.triggered.connect(lambda state,u=f"{c.client.server}:{c.client.port}": self.insertIntoEditor(u))
				smenu.addAction(entry)

				smenu.addSeparator()

		channels = self.parent.getAllChannelWindows()
		if len(channels)>0:
			smenu = menu.addMenu(QIcon(CHANNEL_ICON),"Insert channel name")
			clist = []
			for window in channels:
				c = window.widget()
				clist.append(c.name)

			clist = list(set(clist))
			for c in clist:
				entry = QAction(QIcon(CHANNEL_ICON),c,self)
				entry.triggered.connect(lambda state,u=f"{c}": self.insertIntoEditor(u))
				smenu.addAction(entry)

		menu.exec_(self.editor.mapToGlobal(pos))

	def check_for_save(self):

		if config.EDITOR_PROMPT_SAVE:
			if self.changed:
				msgBox = QMessageBox()
				msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
				msgBox.setIconPixmap(QPixmap(SAVEFILE_ICON))
				if self.editing_user_script:
					msgBox.setText("Do you want to save this connection script?")
				else:
					msgBox.setText("Do you want to save this file?")
				msgBox.setWindowTitle("Save")
				msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

				rval = msgBox.exec()
				if rval == QMessageBox.Yes:
					if self.editing_user_script:
						self.doFileSave()
					else:
						if self.filename==None:
							self.doFileSaveAs()
						else:
							self.doFileSave()

	def closeEvent(self, event):

		if self.force_close:
			self.parent.closeSubWindow(self.subwindow_id)
			event.accept()
			self.close()
			return

		self.check_for_save()

		# Make sure the MDI window is closed
		self.parent.closeSubWindow(self.subwindow_id)

		event.accept()
		self.close()

	def readConnect(self,hostid,contents):

		self.check_for_save()

		self.editing_user_script = True
		self.current_user_script = hostid

		self.editor.setPlainText(contents)
		self.changed = False
		self.updateApplicationTitle()

	def toggleLine(self):
		if config.HIGHLIGHT_CURRENT_LINE_IN_EDITOR:
			config.HIGHLIGHT_CURRENT_LINE_IN_EDITOR = False
			self.hl_menu.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			config.HIGHLIGHT_CURRENT_LINE_IN_EDITOR = True
			self.hl_menu.setIcon(QIcon(self.parent.checked_icon))
		self.editor.setHighlightLine(config.HIGHLIGHT_CURRENT_LINE_IN_EDITOR)
		config.save_settings(config.CONFIG_FILE)

	def toggleWordwrap(self):
		if config.EDITOR_WORDWRAP:
			self.editor.setLineWrapMode(QTextEdit.NoWrap)
			config.EDITOR_WORDWRAP = False
			self.ww_menu.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			self.editor.setLineWrapMode(QTextEdit.WidgetWidth)
			config.EDITOR_WORDWRAP = True
			self.ww_menu.setIcon(QIcon(self.parent.checked_icon))
		config.save_settings(config.CONFIG_FILE)

	def toggleReload(self):
		if config.AUTO_RELOAD_ON_CLOSE:
			config.AUTO_RELOAD_ON_CLOSE = False
			self.ar_menu.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			config.AUTO_RELOAD_ON_CLOSE = True
			self.ar_menu.setIcon(QIcon(self.parent.checked_icon))
		config.save_settings(config.CONFIG_FILE)

	def toggleClose(self):
		if config.CLOSE_EDITOR_ON_UNINSTALL:
			config.CLOSE_EDITOR_ON_UNINSTALL = False
			self.ce_menu.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			config.CLOSE_EDITOR_ON_UNINSTALL = True
			self.ce_menu.setIcon(QIcon(self.parent.checked_icon))
		config.save_settings(config.CONFIG_FILE)

	def toggleIndent(self):
		if config.PYTHON_AUTOINDENT:
			config.PYTHON_AUTOINDENT = False
			self.ai_menu.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			config.PYTHON_AUTOINDENT = True
			self.ai_menu.setIcon(QIcon(self.parent.checked_icon))
		config.save_settings(config.CONFIG_FILE)

	def toggleWhitespace(self):
		if config.PYTHON_SHOW_WHITESPACE:
			config.PYTHON_SHOW_WHITESPACE = False
			self.sw_menu.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			config.PYTHON_SHOW_WHITESPACE = True
			self.sw_menu.setIcon(QIcon(self.parent.checked_icon))
		self.toggle_whitespace()
		config.save_settings(config.CONFIG_FILE)

	def toggle_whitespace(self):
		document = self.editor.document()
		option = document.defaultTextOption()
		if config.PYTHON_SHOW_WHITESPACE:
			option.setFlags(option.flags() | QTextOption.ShowTabsAndSpaces)
			option.setFlags(option.flags() | QTextOption.AddSpaceForLineAndParagraphSeparators)
		else:
			option.setFlags(option.flags() & ~QTextOption.ShowTabsAndSpaces)
			option.setFlags(option.flags() & ~QTextOption.AddSpaceForLineAndParagraphSeparators)
		document.setDefaultTextOption(option)

	def buildEditMenu(self):

		self.editMenu.clear()

		mefind = QAction(QIcon(WHOIS_ICON),"Find",self)
		mefind.triggered.connect(self.doFind)
		mefind.setShortcut("Ctrl+F")
		self.editMenu.addAction(mefind)

		mefind = QAction(QIcon(EDIT_ICON),"Find and replace",self)
		mefind.triggered.connect(self.doFindReplace)
		mefind.setShortcut("Ctrl+R")
		self.editMenu.addAction(mefind)

		self.editMenu.addSeparator()

		entry = QAction(QIcon(SELECTALL_ICON),"Select All",self)
		entry.triggered.connect(self.editor.selectAll)
		entry.setShortcut("Ctrl+A")
		self.editMenu.addAction(entry)

		self.editMenu.addSeparator()

		self.menuUndo = QAction(QIcon(UNDO_ICON),"Undo",self)
		self.menuUndo.triggered.connect(self.editor.undo)
		self.menuUndo.setShortcut("Ctrl+Z")
		self.editMenu.addAction(self.menuUndo)
		self.menuUndo.setEnabled(False)

		self.menuRedo = QAction(QIcon(REDO_ICON),"Redo",self)
		self.menuRedo.triggered.connect(self.editor.redo)
		self.menuRedo.setShortcut("Ctrl+Y")
		self.editMenu.addAction(self.menuRedo)
		self.menuRedo.setEnabled(False)

		self.editMenu.addSeparator()

		self.menuCut = QAction(QIcon(CUT_ICON),"Cut",self)
		self.menuCut.triggered.connect(self.editor.cut)
		self.menuCut.setShortcut("Ctrl+X")
		self.editMenu.addAction(self.menuCut)
		self.menuCut.setEnabled(False)

		self.menuCopy = QAction(QIcon(COPY_ICON),"Copy",self)
		self.menuCopy.triggered.connect(self.editor.copy)
		self.menuCopy.setShortcut("Ctrl+C")
		self.editMenu.addAction(self.menuCopy)
		self.menuCopy.setEnabled(False)

		self.menuPaste = QAction(QIcon(CLIPBOARD_ICON),"Paste",self)
		self.menuPaste.triggered.connect(self.editor.paste)
		self.menuPaste.setShortcut("Ctrl+V")
		self.editMenu.addAction(self.menuPaste)

		self.editMenu.addSeparator()

		self.menuZoomIn = QAction(QIcon(PLUS_ICON),"Zoom in",self)
		self.menuZoomIn.triggered.connect(self.editor.zoomIn)
		self.menuZoomIn.setShortcut("Ctrl++")
		self.editMenu.addAction(self.menuZoomIn)

		self.menuZoomOut = QAction(QIcon(MINUS_ICON),"Zoom out",self)
		self.menuZoomOut.triggered.connect(self.editor.zoomOut)
		self.menuZoomOut.setShortcut("Ctrl+-")
		self.editMenu.addAction(self.menuZoomOut)

		if self.python:
			self.editMenu.addSeparator()

			mefind = QAction(QIcon(BAN_ICON),"Strip all comments",self)
			mefind.triggered.connect(self.doStripPython)
			self.editMenu.addAction(mefind)

	def generateStylesheet(self,obj,fore,back):

		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def refreshHighlighter(self):
		reset = False
		if self.changed==False: reset = True
		if config.EDITOR_USES_SYNTAX_HIGHLIGHTING:
			if self.python:
				self.highlight = syntax.PythonHighlighter(self.editor.document())
			else:
				self.highlight = syntax.MerkScriptHighlighter(self.editor.document())
			self.editor.setStyleSheet(self.generateStylesheet('CodeEditor',config.SYNTAX_FOREGROUND,config.SYNTAX_BACKGROUND))
			self.editor.highlight_current_line(True)
			if reset:
				self.changed = False
				self.updateApplicationTitle()
		else:
			script = self.editor.toPlainText()
			self.highlight = None
			self.editor.setStyleSheet(self.generateStylesheet('CodeEditor','#000000','#FFFFFF'))
			self.editor.setPlainText(script)
			self.editor.highlight_current_line(True)
			if reset:
				self.changed = False
				self.updateApplicationTitle()

	def togglePrompt(self):
		if config.EDITOR_PROMPT_SAVE:
			config.EDITOR_PROMPT_SAVE = False
			self.menuPrompt.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			config.EDITOR_PROMPT_SAVE = True
			self.menuPrompt.setIcon(QIcon(self.parent.checked_icon))
		config.save_settings(config.CONFIG_FILE)

	def toggleHighlighting(self):
		if config.EDITOR_USES_SYNTAX_HIGHLIGHTING:
			config.EDITOR_USES_SYNTAX_HIGHLIGHTING = False
			self.menuSyntax.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			config.EDITOR_USES_SYNTAX_HIGHLIGHTING = True
			self.menuSyntax.setIcon(QIcon(self.parent.checked_icon))
		config.save_settings(config.CONFIG_FILE)
		self.refreshHighlighter()

	def toggleStatusBar(self):
		if config.SHOW_STATUS_BAR_ON_EDITOR_WINDOWS:
			self.status.show()
		else:
			self.status.hide()

	def doStripPython(self):
		s = self.editor.toPlainText()
		s = strip_comments_and_docstrings_ast(s)
		self.editor.setPlainText(s)

	def doFind(self):

		cursor = self.editor.textCursor()
		if cursor.hasSelection():
			selected_text = cursor.selectedText()
		else:
			selected_text = None

		if self.findWindow != None and self.findWindow.is_replace==False:
			ftext = self.findWindow.find.text()

			if ftext!=selected_text:
				ftext = selected_text
				icount = None
				self.findWindow.icount.setText('<small>Ready</small>')
				self.findWindow.find.setText(ftext)

			if self.findWindow.icount!=' ':
				icount = self.findWindow.icount.text()
			else:
				icount = None
		else:
			if self.findWindow!=None:
				winpos = self.findWindow.pos()
				self.findWindow.close()
			else:
				winpos = None
			ftext = selected_text
			icount = None

			self.findWindow = dialog.Find(self,False)
			if winpos!=None: self.findWindow.move(winpos)
			if ftext: self.findWindow.find.setText(ftext)
			if icount: self.findWindow.icount.setText(icount)

			if self.editing_user_script:
				self.findWindow.setFilenameLabel(self.current_user_script)
			elif self.filename:
				self.findWindow.setFilenameLabel(os.path.basename(self.filename))
			else:
				self.findWindow.setFilenameLabel("Untitled")

		self.findWindow.show()
		return

	def doFindReplace(self):

		cursor = self.editor.textCursor()
		if cursor.hasSelection():
			selected_text = cursor.selectedText()
		else:
			selected_text = None

		if self.findWindow != None and self.findWindow.is_replace==True:
			ftext = self.findWindow.find.text()

			if ftext!=selected_text:
				ftext = selected_text
				icount = None
				self.findWindow.icount.setText('<small>Ready</small>')
				self.findWindow.find.setText(ftext)

			if self.findWindow.icount!=' ':
				icount = self.findWindow.icount.text()
			else:
				icount = None
		else:
			if self.findWindow!=None:
				winpos = self.findWindow.pos()
				self.findWindow.close()
			else:
				winpos = None
			ftext = selected_text
			icount = None

			self.findWindow = dialog.Find(self,True)
			if winpos!=None: self.findWindow.move(winpos)
			if ftext: self.findWindow.find.setText(ftext)
			if icount: self.findWindow.icount.setText(icount)

			if self.editing_user_script:
				self.findWindow.setFilenameLabel(self.current_user_script)
			elif self.filename:
				self.findWindow.setFilenameLabel(os.path.basename(self.filename))
			else:
				self.findWindow.setFilenameLabel("Untitled")

		self.findWindow.show()
		return

	def update_line_number(self):
		cursor = self.editor.textCursor()
		line_number = cursor.blockNumber() + 1

		self.status_line.setText(f"<small>{line_number}</small>")

	def doImport(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Import Script", str(Path.home()), f"MERK Script (*.{SCRIPT_FILE_EXTENSION});;All Files (*)", options=options)
		if fileName:
			base = os.path.basename(fileName)
			imported_file = os.path.join(commands.SCRIPTS_DIRECTORY,base)

			do_overwrite = True
			if os.path.exists(imported_file) or os.path.isfile(imported_file):
				msgBox = QMessageBox()
				msgBox.setIconPixmap(QPixmap(SCRIPT_ICON))
				msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
				msgBox.setText(f"\"{base}\" already exists. Overwrite script?")
				msgBox.setWindowTitle("Overwrite File")
				msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

				rval = msgBox.exec()
				if rval == QMessageBox.Cancel:
					do_overwrite = False
			
			if do_overwrite:
				try:
					shutil.copy(fileName, imported_file)
				except FileNotFoundError:
					QMessageBox.critical(self, 'Error', f"Source file '{fileName}' not found.")
					return
				except Exception as e:
					QMessageBox.critical(self, 'Error', f'Error importing file: {e}')
					return

				self.filename = imported_file
				f = commands.find_file(self.filename,SCRIPT_FILE_EXTENSION)
				if f!=None:
					x = open(f,mode="r",encoding="utf-8",errors="ignore")
					source_code = str(x.read())
					x.close()
					self.editor.setPlainText(source_code)
					self.changed = False
					self.updateApplicationTitle()

	def write_file_to_zip(self,zip_file,filename):
		# Check to see if the file already exists
		# in the zip
		do_replace = False
		with zipfile.ZipFile(zip_file, 'r') as zf:
			for member in zf.infolist():
				if member.filename==filename: do_replace = True
		if not do_replace:
			# File does not already exist, so just write it
			# to the zip file and return
			with zipfile.ZipFile(zip_file, 'a') as zip_ref:
				zip_ref.writestr(filename, self.editor.toPlainText())
			return

		# Copy everything in the old zip to a temp zip
		# except for the file to replace
		temp_zip_filename = zip_file + str(uuid.uuid4())[:8]
		with zipfile.ZipFile(zip_file, 'r') as zin:
			with zipfile.ZipFile(temp_zip_filename, 'w') as zout:
				for item in zin.infolist():
					if item.filename != filename:
						buffer = zin.read(item.filename)
						zout.writestr(item, buffer)

		# Replace the original file with the new one
		os.remove(zip_file)
		os.rename(temp_zip_filename, zip_file)

		# Write the new file to the zip
		with zipfile.ZipFile(zip_file, 'a') as zip_ref:
			zip_ref.writestr(filename, self.editor.toPlainText())

	def doZip(self):
		if self.filename==None:
			e = dialog.SetFilenameDialog(self)

			if not e: return
			out_file = e
		else:
			out_file = os.path.basename(self.filename)

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Write to ZIP", str(Path.home()), f"ZIP File (*.zip);;All Files (*)", options=options)
		if fileName:
			self.write_file_to_zip(fileName,out_file)
			QMessageBox.information(self, 'Success', f'File written to "{os.path.basename(fileName)}"!')

	def doInsertCallMethod(self,method):
		self.editor.insertPlainText(f"def {method}(self,window,arguments):")
		self.insert_raw_indent()
		self.editor.insertPlainText(f"pass")
		self.updateApplicationTitle()

	def doInsertEventMethod(self,method,vals=[]):
		self.editor.insertPlainText(f"def {method}(self,**arguments):")
		if len(vals)==0:
			self.insert_raw_indent()
			self.editor.insertPlainText(f"pass")
		else:
			for v in vals:
				self.insert_raw_indent()
				self.editor.insertPlainText(f"{v} = arguments[\"{v}\"]")
			self.insert_raw_indent()

	def doInsertInitMethod(self):
		self.editor.insertPlainText(f"def init(self):")
		self.insert_raw_indent()
		self.editor.insertPlainText(f"pass")
		self.updateApplicationTitle()

	def doInsertUninstallMethod(self):
		self.editor.insertPlainText(f"def uninstall(self):")
		self.insert_raw_indent()
		self.editor.insertPlainText(f"pass")
		self.updateApplicationTitle()

	def doInsertUnloadMethod(self):
		self.editor.insertPlainText(f"def unload(self):")
		self.insert_raw_indent()
		self.editor.insertPlainText(f"pass")
		self.updateApplicationTitle()

	def doInsertPauseMethod(self):
		self.editor.insertPlainText(f"def pause(self):")
		self.insert_raw_indent()
		self.editor.insertPlainText(f"pass")
		self.updateApplicationTitle()

	def doInsertUnPauseMethod(self):
		self.editor.insertPlainText(f"def unpause(self):")
		self.insert_raw_indent()
		self.editor.insertPlainText(f"pass")
		self.updateApplicationTitle()

	def doInsertCallMethod(self):
		m = dialog.SetMethodNameDialog('',self.parent)
		if m:
			self.editor.insertPlainText(f"def {m}(self,window,arguments):")
			self.insert_raw_indent()
			self.editor.insertPlainText(f"pass")
			self.updateApplicationTitle()

	def is_in_plugin_directory(self):
		if self.filename==None: return False

		known_dir = os.path.realpath(plugins.PLUGIN_DIRECTORY)
		target_file = os.path.realpath(self.filename)

		if os.path.commonpath([known_dir, target_file]) == known_dir:
			name_without_extension, extension = os.path.splitext(self.filename)
			if extension.lower()=='.py':
				return True
			else:
				return False
		else:
			return False

	def __init__(self,filename=None,parent=None,subwindow=None,python=False,blank=False,contents=None):
		super(Window, self).__init__(parent)

		self.filename = filename
		self.parent = parent
		self.changed = False
		self.cscript_menu = None
		self.window_type = EDITOR_WINDOW
		self.subwindow = subwindow
		self.python = python
		self.force_close = False
		self.blank = blank
		self.contents = contents

		self.editing_user_script = False
		self.current_user_script = None
		self.findWindow = None

		self.name = "Untitled"

		# Load in user settings
		user.load_user(user.USER_FILE)

		self.subwindow_id = str(uuid.uuid4())

		self.editor = CodeEditor()

		self.editor.setHighlightLine(config.HIGHLIGHT_CURRENT_LINE_IN_EDITOR)

		self.editor.cursorPositionChanged.connect(self.update_line_number)

		if config.EDITOR_USES_SYNTAX_HIGHLIGHTING:
			if self.python:
				self.highlight = syntax.PythonHighlighter(self.editor.document())
			else:
				self.highlight = syntax.MerkScriptHighlighter(self.editor.document())
			self.editor.setStyleSheet(self.generateStylesheet('CodeEditor',config.SYNTAX_FOREGROUND,config.SYNTAX_BACKGROUND))
			self.editor.highlight_current_line(True)
		else:
			self.highlight = None

		if self.python:
			self.toggle_whitespace()

		if config.EDITOR_WORDWRAP:
			self.editor.setLineWrapMode(QTextEdit.WidgetWidth)
		else:
			self.editor.setLineWrapMode(QTextEdit.NoWrap)

		self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
		self.editor.customContextMenuRequested.connect(self.show_context_menu)

		self.setWindowIcon(QIcon(SCRIPT_ICON))

		self.editor.textChanged.connect(self.docModified)
		self.editor.redoAvailable.connect(self.hasRedo)
		self.editor.undoAvailable.connect(self.hasUndo)
		self.editor.copyAvailable.connect(self.hasCopy)

		self.editor.installEventFilter(self)

		self.status = self.statusBar()
		self.status.setStyleSheet("QStatusBar::item { border: none; }")

		self.status_file = QLabel("<small><b>Untitled script</b></small>")
		self.status.addPermanentWidget(self.status_file,1)

		self.status_line = QLabel("<small>1</small>")
		self.status.addPermanentWidget(self.status_line,0)

		if not config.SHOW_STATUS_BAR_ON_EDITOR_WINDOWS:
			self.status.hide()

		if self.filename:
			if self.python:
				if not self.blank:
					f = commands.find_plugin(self.filename,"py")
				else:
					f = commands.find_plugin(self.filename,"py")
					if f==None: f = commands.find_file(self.filename,"py")
			else:
				f = commands.find_file(self.filename,SCRIPT_FILE_EXTENSION)
			if f!=None:
				x = open(f,mode="r",encoding="utf-8",errors="ignore")
				source_code = str(x.read())
				x.close()
				self.editor.setPlainText(source_code)
				self.changed = False
				self.updateApplicationTitle()

		if self.contents!=None:
			self.editor.setPlainText(self.contents)
			self.changed = True
			self.updateApplicationTitle()

		self.menubar = self.menuBar()

		self.fileMenu = self.menubar.addMenu("File")

		entry = QAction(QIcon(OPENFILE_ICON),"Open file",self)
		entry.triggered.connect(self.doFileOpen)
		entry.setShortcut("Ctrl+O")
		self.fileMenu.addAction(entry)

		if not self.python:
			if len(user.COMMANDS)>0:
				self.cscript_menu = self.fileMenu.addMenu(QIcon(OPENFILE_ICON),"Open connection script")

				for host in user.COMMANDS:
					entry = QAction(QIcon(SCRIPT_ICON),f"{host}",self)
					entry.triggered.connect(lambda state,x=host,f=user.COMMANDS[host]: self.readConnect(x,f))
					self.cscript_menu.addAction(entry)

			entry = QAction(QIcon(NEWFILE_ICON),"New script",self)
			entry.triggered.connect(self.doNewFile)
			entry.setShortcut("Ctrl+N")
			self.fileMenu.addAction(entry)

			entry = QAction(QIcon(SCRIPT_ICON),"New connection script",self)
			entry.triggered.connect(self.doNewScript)
			self.fileMenu.addAction(entry)

			entry = QAction(QIcon(SCRIPT_ICON),"New script editor window",self)
			entry.triggered.connect(self.parent.newEditorWindow)
			self.fileMenu.addAction(entry)

			entry = QAction(QIcon(PYTHON_ICON),"New Python editor window",self)
			entry.triggered.connect((lambda : self.parent.newEditorPluginFileBlank(None)))
			self.fileMenu.addAction(entry)

			self.fileMenu.addSeparator()

			entry = QAction(QIcon(FOLDER_ICON),"Scripts directory",self)
			entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+commands.SCRIPTS_DIRECTORY))))
			self.fileMenu.addAction(entry)

			entry = QAction(QIcon(IMPORT_ICON),"Import script",self)
			entry.triggered.connect(self.doImport)
			self.fileMenu.addAction(entry)

			self.zip = QAction(QIcon(EXPORT_ICON),"Write file to ZIP",self)
			self.zip.triggered.connect(self.doZip)
			self.fileMenu.addAction(self.zip)
		else:
			entry = QAction(QIcon(PLUGIN_ICON),"New plugin",self)
			entry.triggered.connect(self.doNewPlugin)
			entry.setShortcut("Ctrl+N")
			self.fileMenu.addAction(entry)

			entry = QAction(QIcon(PLUGIN_ICON),"New plugin (no comments)",self)
			entry.triggered.connect(self.doNewPluginComments)
			self.fileMenu.addAction(entry)

			entry = QAction(QIcon(NEWFILE_ICON),"New file",self)
			entry.triggered.connect(self.doNewFile)
			self.fileMenu.addAction(entry)

			entry = QAction(QIcon(SCRIPT_ICON),"New script editor window",self)
			entry.triggered.connect(self.parent.newEditorWindow)
			self.fileMenu.addAction(entry)

			entry = QAction(QIcon(PYTHON_ICON),"New Python editor window",self)
			entry.triggered.connect((lambda : self.parent.newEditorPluginFileBlank(None)))
			self.fileMenu.addAction(entry)

			self.fileMenu.addSeparator()

			entry = QAction(QIcon(FOLDER_ICON),"Plugins directory",self)
			entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+plugins.PLUGIN_DIRECTORY))))
			self.fileMenu.addAction(entry)

		self.fileMenu.addSeparator()

		self.menuSave = QAction(QIcon(SAVEFILE_ICON),"Save",self)
		self.menuSave.triggered.connect(self.doFileSave)
		self.menuSave.setShortcut("Ctrl+S")
		self.fileMenu.addAction(self.menuSave)

		self.menuSaveAs = QAction(QIcon(SAVEASFILE_ICON),"Save as...",self)
		self.menuSaveAs.triggered.connect(self.doFileSaveAs)
		if not self.filename: self.menuSaveAs.setShortcut("Ctrl+Shift+S")
		self.fileMenu.addAction(self.menuSaveAs)

		self.fileMenu.addSeparator()

		menuSyntaxText = "Syntax highlighting"
		if config.EDITOR_USES_SYNTAX_HIGHLIGHTING:
			self.menuSyntax = QAction(QIcon(self.parent.checked_icon),menuSyntaxText,self)
		else:
			self.menuSyntax = QAction(QIcon(self.parent.unchecked_icon),menuSyntaxText,self)
		self.menuSyntax.triggered.connect(self.toggleHighlighting)
		self.fileMenu.addAction(self.menuSyntax)

		if config.HIGHLIGHT_CURRENT_LINE_IN_EDITOR:
			self.hl_menu = QAction(QIcon(self.parent.checked_icon),"Highlight current line",self)
		else:
			self.hl_menu = QAction(QIcon(self.parent.unchecked_icon),"Highlight current line",self)
		self.hl_menu.triggered.connect(self.toggleLine)
		self.fileMenu.addAction(self.hl_menu)

		menuPromptText = "Ask to save changed files"
		if config.EDITOR_PROMPT_SAVE:
			self.menuPrompt = QAction(QIcon(self.parent.checked_icon),menuPromptText,self)
		else:
			self.menuPrompt = QAction(QIcon(self.parent.unchecked_icon),menuPromptText,self)
		self.menuPrompt.triggered.connect(self.togglePrompt)
		self.fileMenu.addAction(self.menuPrompt)

		if config.EDITOR_WORDWRAP:
			self.ww_menu = QAction(QIcon(self.parent.checked_icon),"Word wrap",self)
		else:
			self.ww_menu = QAction(QIcon(self.parent.unchecked_icon),"Word wrap",self)
		self.ww_menu.triggered.connect(self.toggleWordwrap)
		self.fileMenu.addAction(self.ww_menu)

		if self.python:
			if config.PYTHON_SHOW_WHITESPACE:
				self.sw_menu = QAction(QIcon(self.parent.checked_icon),"Show whitespace",self)
			else:
				self.sw_menu = QAction(QIcon(self.parent.unchecked_icon),"Show whitespace",self)
			self.sw_menu.triggered.connect(self.toggleWhitespace)
			self.fileMenu.addAction(self.sw_menu)

			if config.PYTHON_AUTOINDENT:
				self.ai_menu = QAction(QIcon(self.parent.checked_icon),"Auto-indent",self)
			else:
				self.ai_menu = QAction(QIcon(self.parent.unchecked_icon),"Auto-indent",self)
			self.ai_menu.triggered.connect(self.toggleIndent)
			self.fileMenu.addAction(self.ai_menu)

			if config.AUTO_RELOAD_ON_CLOSE:
				self.ar_menu = QAction(QIcon(self.parent.checked_icon),"Auto-reload plugins on close",self)
			else:
				self.ar_menu = QAction(QIcon(self.parent.unchecked_icon),"Auto-reload plugins on close",self)
			self.ar_menu.triggered.connect(self.toggleReload)
			self.fileMenu.addAction(self.ar_menu)

			if config.CLOSE_EDITOR_ON_UNINSTALL:
				self.ce_menu = QAction(QIcon(self.parent.checked_icon),"Close editor on plugin uninstall",self)
			else:
				self.ce_menu = QAction(QIcon(self.parent.unchecked_icon),"Close editor on plugin uninstall",self)
			self.ce_menu.triggered.connect(self.toggleClose)
			self.fileMenu.addAction(self.ce_menu)
		
		self.fileMenu.addSeparator()

		entry = QAction(QIcon(CLOSE_ICON),"Close",self)
		entry.triggered.connect(self.close)
		self.fileMenu.addAction(entry)

		self.editMenu = self.menubar.addMenu("Edit")

		self.buildEditMenu()

		if self.python:
			self.pInsertMenu = self.menubar.addMenu("Insert")

			self.menv = self.pInsertMenu.addMenu(QIcon(APPLICATION_ICON),f"{APPLICATION_NAME} Events")

			entry = QAction(QIcon(APPLICATION_ICON),"init",self)
			entry.triggered.connect(self.doInsertInitMethod)
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"uninstall",self)
			entry.triggered.connect(self.doInsertUninstallMethod)
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"unload",self)
			entry.triggered.connect(self.doInsertUnloadMethod)
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"pause",self)
			entry.triggered.connect(self.doInsertPauseMethod)
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"unpause",self)
			entry.triggered.connect(self.doInsertUnPauseMethod)
			self.menv.addAction(entry)
			
			entry = QAction(QIcon(WINDOW_ICON),"activate",self)
			entry.triggered.connect(lambda state,u="activate",v=["window"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"close",self)
			entry.triggered.connect(lambda state,u="close",v=["name"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(TIMESTAMP_ICON),"ctick",self)
			entry.triggered.connect(lambda state,u="ctick",v=["uptime"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"line_in",self)
			entry.triggered.connect(lambda state,u="line_in",v=["client","line"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"line_out",self)
			entry.triggered.connect(lambda state,u="line_out",v=["client","line"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"me",self)
			entry.triggered.connect(lambda state,u="me",v=["window","client","target","message"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"subwindow",self)
			entry.triggered.connect(lambda state,u="subwindow",v=["window"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(TIMESTAMP_ICON),"tick",self)
			entry.triggered.connect(lambda state,u="tick",v=["client","uptime"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"uptime",self)
			entry.triggered.connect(lambda state,u="uptime",v=["window","uptime"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			self.messenv = self.pInsertMenu.addMenu(QIcon(PRIVATE_ICON),f"Message Events")

			entry = QAction(QIcon(PRIVATE_ICON),"action",self)
			entry.triggered.connect(lambda state,u="action",v=["window","client","channel","user","nickname","hostmask","message"]: self.doInsertEventMethod(u,v))
			self.messenv.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"message",self)
			entry.triggered.connect(lambda state,u="message",v=["window","client","channel","user","nickname","hostmask","message"]: self.doInsertEventMethod(u,v))
			self.messenv.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"notice",self)
			entry.triggered.connect(lambda state,u="notice",v=["window","client","channel","user","nickname","hostmask","message"]: self.doInsertEventMethod(u,v))
			self.messenv.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"server",self)
			entry.triggered.connect(lambda state,u="server",v=["client","message"]: self.doInsertEventMethod(u,v))
			self.messenv.addAction(entry)

			self.conenv = self.pInsertMenu.addMenu(QIcon(CONNECT_ICON),f"Connection Events")

			entry = QAction(QIcon(CONNECT_ICON),"connected",self)
			entry.triggered.connect(lambda state,u="connected",v=["window","client"]: self.doInsertEventMethod(u,v))
			self.conenv.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"connecting",self)
			entry.triggered.connect(lambda state,u="connecting",v=["client"]: self.doInsertEventMethod(u,v))
			self.conenv.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"disconnect",self)
			entry.triggered.connect(lambda state,u="disconnect",v=["client","message"]: self.doInsertEventMethod(u,v))
			self.conenv.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"error",self)
			entry.triggered.connect(lambda state,u="error",v=["client","message"]: self.doInsertEventMethod(u,v))
			self.conenv.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"isupport",self)
			entry.triggered.connect(lambda state,u="isupport",v=["client","options"]: self.doInsertEventMethod(u,v))
			self.conenv.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"lost",self)
			entry.triggered.connect(lambda state,u="lost",v=["client"]: self.doInsertEventMethod(u,v))
			self.conenv.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"motd",self)
			entry.triggered.connect(lambda state,u="motd",v=["client","text"]: self.doInsertEventMethod(u,v))
			self.conenv.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"ping",self)
			entry.triggered.connect(lambda state,u="ping",v=["client"]: self.doInsertEventMethod(u,v))
			self.conenv.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"quit",self)
			entry.triggered.connect(lambda state,u="quit",v=["client","user","message"]: self.doInsertEventMethod(u,v))
			self.conenv.addAction(entry)

			self.statenv = self.pInsertMenu.addMenu(QIcon(OP_USER),f"Status Events")

			entry = QAction(QIcon(GO_AWAY_ICON),"away",self)
			entry.triggered.connect(lambda state,u="away",v=["client","user","message"]: self.doInsertEventMethod(u,v))
			self.statenv.addAction(entry)

			entry = QAction(QIcon(GO_AWAY_ICON),"back",self)
			entry.triggered.connect(lambda state,u="back",v=["client","user"]: self.doInsertEventMethod(u,v))
			self.statenv.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"ison",self)
			entry.triggered.connect(lambda state,u="ison",v=["client","users"]: self.doInsertEventMethod(u,v))
			self.statenv.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"mode",self)
			entry.triggered.connect(lambda state,u="mode",v=["client","user","target","mode","arguments"]: self.doInsertEventMethod(u,v))
			self.statenv.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"unmode",self)
			entry.triggered.connect(lambda state,u="unmode",v=["client","user","target","mode","arguments"]: self.doInsertEventMethod(u,v))
			self.statenv.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"nick",self)
			entry.triggered.connect(lambda state,u="nick",v=["client","nickname"]: self.doInsertEventMethod(u,v))
			self.statenv.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"rename",self)
			entry.triggered.connect(lambda state,u="rename",v=["client","old","new"]: self.doInsertEventMethod(u,v))
			self.statenv.addAction(entry)

			self.chanenv = self.pInsertMenu.addMenu(QIcon(CHANNEL_ICON),f"Channel Events")

			entry = QAction(QIcon(CHANNEL_ICON),"invite",self)
			entry.triggered.connect(lambda state,u="invite",v=["client","user","channel"]: self.doInsertEventMethod(u,v))
			self.chanenv.addAction(entry)

			entry = QAction(QIcon(CHANNEL_ICON),"join",self)
			entry.triggered.connect(lambda state,u="join",v=["window","channel","client","user"]: self.doInsertEventMethod(u,v))
			self.chanenv.addAction(entry)

			entry = QAction(QIcon(CHANNEL_ICON),"joined",self)
			entry.triggered.connect(lambda state,u="joined",v=["window","channel","client"]: self.doInsertEventMethod(u,v))
			self.chanenv.addAction(entry)

			entry = QAction(QIcon(KICK_ICON),"kick",self)
			entry.triggered.connect(lambda state,u="kick",v=["window","channel","client","user","target","message"]: self.doInsertEventMethod(u,v))
			self.chanenv.addAction(entry)

			entry = QAction(QIcon(KICK_ICON),"kicked",self)
			entry.triggered.connect(lambda state,u="kicked",v=["client","channel","user","message"]: self.doInsertEventMethod(u,v))
			self.chanenv.addAction(entry)

			entry = QAction(QIcon(CHANNEL_ICON),"left",self)
			entry.triggered.connect(lambda state,u="left",v=["client","channel"]: self.doInsertEventMethod(u,v))
			self.chanenv.addAction(entry)

			entry = QAction(QIcon(CHANNEL_ICON),"part",self)
			entry.triggered.connect(lambda state,u="part",v=["window","channel","client","user"]: self.doInsertEventMethod(u,v))
			self.chanenv.addAction(entry)

			entry = QAction(QIcon(CHANNEL_ICON),"topic",self)
			entry.triggered.connect(lambda state,u="topic",v=["window","channel","client","user","topic"]: self.doInsertEventMethod(u,v))
			self.chanenv.addAction(entry)

			self.pInsertMenu.addSeparator()

			entry = QAction(QIcon(PYTHON_ICON),"Callable method",self)
			entry.triggered.connect(self.doInsertCallMethod)
			self.pInsertMenu.addAction(entry)

		if not self.python:
			if config.ENABLE_ALIASES:
				self.aliasMenu = self.menubar.addMenu("Aliases")

				self.buildAliasMenu(self.aliasMenu)

			self.runMenu = self.menubar.addMenu("Run")

			self.runMenu.aboutToShow.connect(self.buildRunMenu)

		self.setCentralWidget(self.editor)

		if self.python and not self.filename and not self.blank:
			self.doNewPlugin()
			self.changed = True

		self.updateApplicationTitle()
		self.editor.setFocus()

	def buildAliasMenu(self,menu):

		# User information submenu

		sub = menu.addMenu(QIcon(PRIVATE_ICON),"User information")

		entry = QAction("Nickname",self)
		entry.triggered.connect(lambda state,u="$_NICKNAME": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Username",self)
		entry.triggered.connect(lambda state,u="$_USERNAME": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Realname",self)
		entry.triggered.connect(lambda state,u="$_REALNAME": self.insertIntoEditor(u))
		sub.addAction(entry)

		# Current server submenu

		sub = menu.addMenu(QIcon(CONNECT_ICON),"Current server")

		entry = QAction("Host",self)
		entry.triggered.connect(lambda state,u="$_HOST": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Server",self)
		entry.triggered.connect(lambda state,u="$_SERVER": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Port",self)
		entry.triggered.connect(lambda state,u="$_PORT": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("HostID",self)
		entry.triggered.connect(lambda state,u="$_HOSTID": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Server uptime",self)
		entry.triggered.connect(lambda state,u="$_SUPTIME": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("User mode",self)
		entry.triggered.connect(lambda state,u="$_MODE": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Connection type",self)
		entry.triggered.connect(lambda state,u="$_CONNECTION": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Network",self)
		entry.triggered.connect(lambda state,u="$_NETWORK": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Number of channels",self)
		entry.triggered.connect(lambda state,u="$_SCHANNELS": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Number of hidden channels",self)
		entry.triggered.connect(lambda state,u="$_HCHANNELS": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("User count",self)
		entry.triggered.connect(lambda state,u="$_SCOUNT": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Server software",self)
		entry.triggered.connect(lambda state,u="$_SOFTWARE": self.insertIntoEditor(u))
		sub.addAction(entry)

		# Current channel submenu

		sub = menu.addMenu(QIcon(CHANNEL_ICON),"Current channel")

		entry = QAction("User status",self)
		entry.triggered.connect(lambda state,u="$_STATUS": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Topic",self)
		entry.triggered.connect(lambda state,u="$_TOPIC": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Present in channel",self)
		entry.triggered.connect(lambda state,u="$_PRESENT": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Uptime",self)
		entry.triggered.connect(lambda state,u="$_UPTIME": self.insertIntoEditor(u))
		sub.addAction(entry)

		# Date and time submenu

		sub = menu.addMenu(QIcon(TIMESTAMP_ICON),"Date and time")


		entry = QAction("Day of the week",self)
		entry.triggered.connect(lambda state,u="$_MONTH": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Day of the month",self)
		entry.triggered.connect(lambda state,u="$_ORDINAL": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Month name",self)
		entry.triggered.connect(lambda state,u="$_MONTH": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Year",self)
		entry.triggered.connect(lambda state,u="$_YEAR": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Date",self)
		entry.triggered.connect(lambda state,u="$_DATE": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("European date",self)
		entry.triggered.connect(lambda state,u="$_EDATE": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Unix epoch",self)
		entry.triggered.connect(lambda state,u="$_EPOCH": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Time (24hr format)",self)
		entry.triggered.connect(lambda state,u="$_TIME": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Timestamp",self)
		entry.triggered.connect(lambda state,u="$_STAMP": self.insertIntoEditor(u))
		sub.addAction(entry)

		# Client submenu

		sub = menu.addMenu(QIcon(APPLICATION_ICON),"Client")

		entry = QAction("Name",self)
		entry.triggered.connect(lambda state,u="$_CLIENT": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Uptime",self)
		entry.triggered.connect(lambda state,u="$_CUPTIME": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Version",self)
		entry.triggered.connect(lambda state,u="$_VERSION": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Source code URL",self)
		entry.triggered.connect(lambda state,u="$_SOURCE": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Current release URL",self)
		entry.triggered.connect(lambda state,u="$_RELEASE": self.insertIntoEditor(u))
		sub.addAction(entry)

		entry = QAction("Current release version",self)
		entry.triggered.connect(lambda state,u="$_RVERSION": self.insertIntoEditor(u))
		sub.addAction(entry)

		# Non-submenu entries

		entry = QAction("Script name",self)
		entry.triggered.connect(lambda state,u="$_SCRIPT": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction("Filename",self)
		entry.triggered.connect(lambda state,u="$_FILE": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction("Current window",self)
		entry.triggered.connect(lambda state,u="$_WINDOW": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction("Window type",self)
		entry.triggered.connect(lambda state,u="$_WINDOW_TYPE": self.insertIntoEditor(u))
		menu.addAction(entry)

	def executeScript(self,window):
		script = self.editor.toPlainText()
		if self.filename==None:
			window.executeScript(script,None)
		else:
			window.executeScript(script,self.filename)
		self.runMenu.close()

	def executeScriptOnAll(self):
		servers = self.parent.getAllServerWindows()
		if len(servers)>0:
			for window in servers:
				c = window.widget()
				self.executeScript(c)

	def executeScriptOnChannels(self):
		servers = self.parent.getAllChannelWindows()
		if len(servers)>0:
			for window in servers:
				c = window.widget()
				self.executeScript(c)

	def executeScriptOnPrivates(self):
		servers = self.parent.getAllPrivateWindows()
		if len(servers)>0:
			for window in servers:
				c = window.widget()
				self.executeScript(c)

	def insertIntoEditor(self,value):
		self.editor.insertPlainText(f"{value}")
		self.updateApplicationTitle()

	def buildRunMenu(self):
		self.runMenu.clear()

		servers = self.parent.getAllConnectedServerWindows()
		channels = 0
		privates = 0

		if len(servers)>0:
			for window in servers:
				c = window.widget()
				if hasattr(c.client,"network"):
					network = c.client.network
				else:
					network = config.UNKNOWN_NETWORK_NAME+" network"
				if hasattr(c.client,"server"):
					if hasattr(c.client,"port"):
						cname = f"{c.client.server}:{c.client.port}"
					else:
						cname = f"{c.client.server}"
				else:
					cname = c.name
				runmenuLabel = MenuLabel( menuHtml(RUN_MENU_ICON,"Run on "+cname+"&nbsp;","<b>Host:</b> "+c.name+" ("+network+")<br>Execute on server window",CUSTOM_MENU_ICON_SIZE) )
				runmenuAction = QWidgetAction(self)
				runmenuAction.setDefaultWidget(runmenuLabel)
				runmenuLabel.clicked.connect(lambda u=c: self.executeScript(u))
				self.runMenu.addAction(runmenuAction)

				chats = self.parent.getAllConnectedChatWindows(c.client)
				for window in chats:
					c = window.widget()
					if hasattr(c.client,"network"):
						network = c.client.network
					else:
						network = config.UNKNOWN_NETWORK_NAME+" network"
					if hasattr(c.client,"hostname"):
						cname = c.client.hostname
					else:
						cname = f"{c.client.server}:{c.client.port}"
					if c.window_type==CHANNEL_WINDOW:
						ctype = "channel"
						channels = channels + 1
					else:
						ctype = "private chat"
						privates = privates + 1
					runmenuLabel = MenuLabel( menuHtml(RUN_MENU_ICON,"Run on "+c.name+"&nbsp;","<b>Host:</b> "+cname+" ("+network+")<br>Execute on "+ctype+" window",CUSTOM_MENU_ICON_SIZE) )
					runmenuAction = QWidgetAction(self)
					runmenuAction.setDefaultWidget(runmenuLabel)
					runmenuLabel.clicked.connect(lambda u=c: self.executeScript(u))
					self.runMenu.addAction(runmenuAction)

				self.runMenu.addSeparator()


			if len(servers)>1 or channels>1 or privates>1:
				self.runMenu.addSeparator()

			if len(servers)>1:

				entry = QAction(QIcon(RUN_ICON),"Run script on all servers",self)
				entry.triggered.connect(self.executeScriptOnAll)
				self.runMenu.addAction(entry)

			if channels>1:

				entry = QAction(QIcon(RUN_ICON),"Run script on all channels",self)
				entry.triggered.connect(self.executeScriptOnChannels)
				self.runMenu.addAction(entry)

			if privates>1:

				entry = QAction(QIcon(RUN_ICON),"Run script on all private chats",self)
				entry.triggered.connect(self.executeScriptOnPrivates)
				self.runMenu.addAction(entry)

			return

		# If there's no connected servers...
		entry = QAction(QIcon(DISCONNECT_ICON),"No connected servers",self)
		entry.setEnabled(False)
		self.runMenu.addAction(entry)

	def doNewPlugin(self):

		self.filename = None
		self.editor.clear()
		self.editor.insertPlainText(EXAMPLE_PLUGIN)
		self.changed = True
		self.menuSave.setShortcut("Ctrl+S")
		self.menuSaveAs.setShortcut(QKeySequence())
		self.editing_user_script = False
		self.current_user_script = None
		self.updateApplicationTitle()

		cursor = self.editor.textCursor()
		cursor.movePosition(QTextCursor.Start)
		self.editor.setTextCursor(cursor)

	def doNewPluginComments(self):
		self.filename = None
		self.editor.clear()
		self.editor.insertPlainText(strip_comments_and_docstrings_ast(EXAMPLE_PLUGIN))
		self.changed = True
		self.menuSave.setShortcut("Ctrl+S")
		self.menuSaveAs.setShortcut(QKeySequence())
		self.editing_user_script = False
		self.current_user_script = None
		self.updateApplicationTitle()

		cursor = self.editor.textCursor()
		cursor.movePosition(QTextCursor.Start)
		self.editor.setTextCursor(cursor)

	def doNewScript(self):

		self.check_for_save()

		x = dialog.NewConnectScript(self)
		e = x.get_server_information(self)

		if not e: return

		if e[0]=="": return
		if e[1]=="": e[1] = "6667"

		cscript = f"{e[0]}:{e[1]}"

		# If the connection script already exists, open it
		if cscript in user.COMMANDS:
			self.readConnect(cscript,user.COMMANDS[cscript])
			return

		self.filename = None
		self.editor.clear()
		self.changed = False
		self.menuSave.setShortcut("Ctrl+S")
		self.menuSaveAs.setShortcut(QKeySequence())
		self.editing_user_script = True
		self.current_user_script = cscript
		self.updateApplicationTitle()

	def openScript(self,hostid):

		# If the connection script already exists, open it
		if hostid in user.COMMANDS:
			self.readConnect(hostid,user.COMMANDS[hostid])
			return

		self.filename = None
		self.editor.clear()
		self.changed = False
		self.menuSave.setShortcut(QKeySequence())
		self.menuSaveAs.setShortcut("Ctrl+S")
		self.editing_user_script = True
		self.current_user_script = hostid
		self.updateApplicationTitle()

	def show_error_message(self,title, message):
		msg_box = QMessageBox()
		msg_box.setIcon(QMessageBox.Critical)
		msg_box.setWindowTitle(title)
		msg_box.setWindowIcon(QIcon(APPLICATION_ICON))
		msg_box.setText(message)
		msg_box.setStandardButtons(QMessageBox.Ok)
		msg_box.exec_()

	def updateApplicationTitle(self):

		if self.editing_user_script:
			if self.changed:
				self.setWindowTitle("Connection script for "+self.current_user_script+"*")
				self.status_file.setText(f"<small><b>Connection script for {self.current_user_script} - Changed</b></small>")
			else:
				self.setWindowTitle("Connection script for "+self.current_user_script)
				self.status_file.setText(f"<small><b>Connection script for {self.current_user_script}</b></small>")
			self.name = f"{self.current_user_script}"
			self.parent.buildWindowsMenu()

			if self.findWindow!=None: self.findWindow.setFilenameLabel(self.current_user_script)

			w = self.parent.getEditorWindow(self.subwindow_id)
			a = self.parent.MDI.activeSubWindow()
			if w==a: self.parent.merk_subWindowActivated(w)

			return

		if self.filename!=None:
			base = os.path.basename(self.filename)
			if self.changed:
				self.setWindowTitle(base+"*")
				self.status_file.setText(f"<small><b>{self.filename} - Changed</b></small>")
			else:
				self.setWindowTitle(base)
				self.status_file.setText(f"<small><b>{self.filename}</b></small>")
			self.name = f"{base}"
			if self.findWindow!=None: self.findWindow.setFilenameLabel(base)
		else:
			if self.changed:
				self.setWindowTitle(f"Untitled*")
				self.status_file.setText(f"<small><b>{self.name} - Changed</b></small>")
			else:
				self.setWindowTitle(f"Untitled")
				self.status_file.setText(f"<small><b>{self.name}</b></small>")
			self.name = "Untitled"
			if self.findWindow!=None: self.findWindow.setFilenameLabel("Untitled")
		
		self.parent.buildWindowsMenu()

		w = self.parent.getEditorWindow(self.subwindow_id)
		a = self.parent.MDI.activeSubWindow()
		if w==a: self.parent.merk_subWindowActivated(w)

	def doFileSaveAs(self):
		fname = f"{APPLICATION_NAME} Script"
		exten = f"{SCRIPT_FILE_EXTENSION}"
		direc = commands.SCRIPTS_DIRECTORY
		if self.python:
			fname = f"Python Module"
			exten = f"py"
			direc = plugins.PLUGIN_DIRECTORY
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save as...",direc,f"{fname} (*.{exten});;All Files (*)", options=options)
		if fileName:
			_, file_extension = os.path.splitext(fileName)
			if file_extension=='':
				efl = len(exten)+1
				if fileName[-efl:].lower()!=f".{exten}": fileName = fileName+f".{exten}"
			self.filename = fileName
			code = open(self.filename,"w",encoding="utf-8",errors="ignore")
			code.write(self.editor.toPlainText())
			code.close()
			self.changed = False
			self.updateApplicationTitle()
			self.menuSave.setShortcut("Ctrl+S")
			self.menuSaveAs.setShortcut(QKeySequence())

	def doNewFile(self):

		self.check_for_save()

		self.filename = None
		self.editor.clear()
		self.changed = False
		self.menuSave.setShortcut(QKeySequence())
		self.menuSaveAs.setShortcut("Ctrl+S")
		self.editing_user_script = False
		self.current_user_script = None
		self.updateApplicationTitle()

	def doFileOpen(self):

		self.check_for_save()

		fname = f"{APPLICATION_NAME} Script"
		exten = f"{SCRIPT_FILE_EXTENSION}"
		direc = commands.SCRIPTS_DIRECTORY
		if self.python:
			fname = f"Python Module"
			exten = f"py"
			direc = plugins.PLUGIN_DIRECTORY

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open File", direc, f"{fname} (*.{exten});;Text Files (*.txt);;All Files (*)", options=options)
		if fileName:
			script = open(fileName,"r",encoding="utf-8",errors="ignore")
			self.editor.setPlainText(script.read())
			script.close()
			self.filename = fileName
			self.changed = False
			self.menuSave.setShortcut("Ctrl+S")
			self.menuSaveAs.setShortcut(QKeySequence())
			self.editing_user_script = False
			self.current_user_script = None
			self.updateApplicationTitle()

	def doFileSave(self):

		if self.editing_user_script:
			contents = self.editor.toPlainText()
			if len(contents)==0:
				del user.COMMANDS[self.current_user_script]
			else:
				user.COMMANDS[self.current_user_script] = contents
			user.save_user(user.USER_FILE)

			self.cscript_menu.clear()

			for host in user.COMMANDS:
				entry = QAction(QIcon(SCRIPT_ICON),f"{host}",self)
				entry.triggered.connect(lambda state,x=host,f=user.COMMANDS[host]: self.readConnect(x,f))
				self.cscript_menu.addAction(entry)


			self.changed = False
			self.updateApplicationTitle()
			return

		if self.filename==None: return self.doFileSaveAs()

		code = open(self.filename,"w",encoding="utf-8",errors="ignore")
		code.write(self.editor.toPlainText())
		code.close()
		self.changed = False
		self.updateApplicationTitle()

	def _infer_indent_style(self):
		text = self.editor.toPlainText()
		lines = text.split('\n')
		
		space_indents = []
		tab_indents = []
		mixed_indents = []

		for line in lines:
			stripped = line.lstrip()
			if line != stripped and stripped:
				indent = line[:len(line) - len(stripped)]
				if '\t' in indent and ' ' in indent:
					mixed_indents.append(indent)
				elif '\t' in indent:
					tab_indents.append(indent)
				elif ' ' in indent:
					space_indents.append(indent)
		
		if len(tab_indents) > len(space_indents):
			return '\t'
		elif len(space_indents) > 0:
			space_counts = [len(indent) for indent in space_indents]
			common_size = Counter(space_counts).most_common(1)[0][0]

			smaller_sizes = [size for size in set(space_counts) if size < common_size]
			if smaller_sizes:
				min_size = min(smaller_sizes)
				if common_size % min_size == 0:
					common_size = min_size

			return ' ' * common_size
		elif mixed_indents:
			return config.DEFAULT_PYTHON_INDENT
		else:
			return config.DEFAULT_PYTHON_INDENT

	def eventFilter(self, watched: QObject, event: QEvent) -> bool:
		if not self.python: return super().eventFilter(watched, event)
		if not config.PYTHON_AUTOINDENT: return super().eventFilter(watched, event)

		# If we're working on a Python file, like a plugin, this event
		# will handle auto-indentation, trying to match the indent
		# style (either space or tab) of the overall document

		if watched is self.editor and event.type() == QEvent.KeyPress:
			key_event: QKeyEvent = event
			if key_event.key() in (Qt.Key_Return, Qt.Key_Enter):
				return self.insert_indent(watched,event)

			if key_event.key() == Qt.Key_Tab:
				return self.insert_indent(watched,event,True)
	
		return super().eventFilter(watched, event)

	def insert_raw_indent(self,no_newline=False):
		cursor = self.editor.textCursor()

		cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
		cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
		current_line_text = cursor.selectedText()
		
		cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.MoveAnchor)

		base_indentation = ""
		for char in current_line_text:
			if char in (' ', '\t'):
				base_indentation += char
			else:
				break
		
		new_line_indent = base_indentation
		stripped_line = current_line_text.strip()
		
		if stripped_line.endswith(':'):
			extra_indent_unit = self._infer_indent_style()
			new_line_indent += extra_indent_unit

		if no_newline:
			cursor.insertText(config.DEFAULT_PYTHON_INDENT)
			return True
		else:
			cursor.insertText('\n' + new_line_indent)
			return True

	def insert_indent(self,watched,event,no_newline=False):
		cursor = self.editor.textCursor()

		# If the cursor is in the "middle" of a line
		# and not at the end, we don't need to do any
		# of the indent calculation stuff, we can just
		# go ahead and do the enter key event
		block = cursor.block()
		block_length = block.length()
		cursor_pos_in_block = cursor.positionInBlock()
		if cursor_pos_in_block < block_length - 1:
			return super().eventFilter(watched, event)

		cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
		cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
		current_line_text = cursor.selectedText()
		
		cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.MoveAnchor)

		base_indentation = ""
		for char in current_line_text:
			if char in (' ', '\t'):
				base_indentation += char
			else:
				break
		
		new_line_indent = base_indentation
		stripped_line = current_line_text.strip()
		
		if stripped_line.endswith(':'):
			extra_indent_unit = self._infer_indent_style()
			new_line_indent += extra_indent_unit

		if no_newline:
			cursor.insertText(config.DEFAULT_PYTHON_INDENT)
			return True
		else:
			cursor.insertText('\n' + new_line_indent)
			return True

	def docModified(self):
		if not self.parent.at_least_one_window_has_spawned:
			self.parent.at_least_one_window_has_spawned = True
			return
		if self.changed: return
		self.changed = True
		self.updateApplicationTitle()

	def hasUndo(self,avail):
		if avail:
			self.menuUndo.setEnabled(True)
		else:
			self.menuUndo.setEnabled(False)

	def hasRedo(self,avail):
		if avail:
			self.menuRedo.setEnabled(True)
		else:
			self.menuRedo.setEnabled(False)

	def hasCopy(self,avail):
		if avail:
			self.menuCopy.setEnabled(True)
			self.menuCut.setEnabled(True)
		else:
			self.menuCopy.setEnabled(False)
			self.menuCut.setEnabled(False)

