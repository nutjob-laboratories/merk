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
		self.menuSave.setEnabled(True)
		self.changed = False
		self.updateApplicationTitle()

	def toggleWordwrap(self):
		if config.EDITOR_WORDWRAP:
			self.editor.setLineWrapMode(QPlainTextEdit.NoWrap)
			config.EDITOR_WORDWRAP = False
			self.ww_menu.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			self.editor.setLineWrapMode(QPlainTextEdit.WidgetWidth)
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
			self.editor.setStyleSheet(self.generateStylesheet('QPlainTextEdit',config.SYNTAX_FOREGROUND,config.SYNTAX_BACKGROUND))
			if reset:
				self.changed = False
				self.updateApplicationTitle()
		else:
			script = self.editor.toPlainText()
			self.highlight = None
			self.editor.setStyleSheet(self.generateStylesheet('QPlainTextEdit','black','white'))
			self.editor.setPlainText(script)
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

		if self.findWindow != None:
			ftext = self.findWindow.find.text()
			winpos = self.findWindow.pos()
			if self.findWindow.icount!=' ':
				icount = self.findWindow.icount.text()
			else:
				icount = None
			self.findWindow.close()
		else:
			ftext = None
			winpos = None
			icount = None

		self.findWindow = Find(self,False)
		if self.filename:
			self.findWindow.setWindowTitle(self.filename)
		if ftext: self.findWindow.find.setText(ftext)

		if winpos:
			self.findWindow.move(winpos)

		if icount:
			self.findWindow.icount.setText(icount)

		self.findWindow.show()
		return

	def doFindReplace(self):

		if self.findWindow != None:
			ftext = self.findWindow.find.text()
			winpos = self.findWindow.pos()
			if self.findWindow.icount!=' ':
				icount = self.findWindow.icount.text()
			else:
				icount = None
			self.findWindow.close()
		else:
			ftext = None
			winpos = None
			icount = None

		self.findWindow = Find(self,True)
		if self.filename:
			self.findWindow.setWindowTitle(self.filename)
		if ftext: self.findWindow.find.setText(ftext)

		if winpos:
			self.findWindow.move(winpos)

		if icount:
			self.findWindow.icount.setText(icount)


		self.findWindow.show()
		return

	def update_line_number(self):
		cursor = self.editor.textCursor()
		line_number = cursor.blockNumber() + 1

		self.status_line.setText(f"<small>{line_number}</small>")

	def doImport(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Import Script", str(Path.home()), f"MERK Script (*.merk);;All Files (*)", options=options)
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

	def insertCallMethod(self):
		e = dialog.SetMethodDialog(self)

		if not e: return

		valid = True
		if e in plugins.EVENTS: valid = False
		if e in plugins.BUILT_IN: valid = False
		if e == '__init__': valid = False

		if not valid:
			QMessageBox.critical(self, 'Error', f"\"{e}\" is not a valid method name")
			return

		self.doInsertCallMethod(e)

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

	def __init__(self,filename=None,parent=None,subwindow=None,python=False,blank=False):
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

		self.editing_user_script = False
		self.current_user_script = None
		self.findWindow = None

		self.name = "Untitled"

		# Load in user settings
		user.load_user(user.USER_FILE)

		self.subwindow_id = str(uuid.uuid4())

		self.editor = QPlainTextEdit(self)

		self.editor.cursorPositionChanged.connect(self.update_line_number)

		if config.EDITOR_USES_SYNTAX_HIGHLIGHTING:
			if self.python:
				self.highlight = syntax.PythonHighlighter(self.editor.document())
			else:
				self.highlight = syntax.MerkScriptHighlighter(self.editor.document())
			self.editor.setStyleSheet(self.generateStylesheet('QPlainTextEdit',config.SYNTAX_FOREGROUND,config.SYNTAX_BACKGROUND))
		else:
			self.highlight = None

		if self.python:
			self.toggle_whitespace()

		if config.EDITOR_WORDWRAP:
			self.editor.setLineWrapMode(QPlainTextEdit.WidgetWidth)
		else:
			self.editor.setLineWrapMode(QPlainTextEdit.NoWrap)

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

		self.updateApplicationTitle()

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

			self.fileMenu.addSeparator()

			entry = QAction(QIcon(FOLDER_ICON),"Plugins directory",self)
			entry.triggered.connect((lambda : QDesktopServices.openUrl(QUrl("file:"+plugins.PLUGIN_DIRECTORY))))
			self.fileMenu.addAction(entry)

		self.fileMenu.addSeparator()

		self.menuSave = QAction(QIcon(SAVEFILE_ICON),"Save",self)
		self.menuSave.triggered.connect(self.doFileSave)
		self.menuSave.setShortcut("Ctrl+S")
		self.fileMenu.addAction(self.menuSave)

		if self.filename==None:
			self.menuSave.setEnabled(False)

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

			entry = QAction(QIcon(APPLICATION_ICON),"activate",self)
			entry.triggered.connect(lambda state,u="activate",v=["window"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"close",self)
			entry.triggered.connect(lambda state,u="close",v=["name"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"ctick",self)
			entry.triggered.connect(lambda state,u="ctick",v=["uptime"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"line_in",self)
			entry.triggered.connect(lambda state,u="line_in",v=["client","line"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"line_out",self)
			entry.triggered.connect(lambda state,u="line_out",v=["client","line"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"me",self)
			entry.triggered.connect(lambda state,u="me",v=["window","client","target","message"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"subwindow",self)
			entry.triggered.connect(lambda state,u="subwindow",v=["window"]: self.doInsertEventMethod(u,v))
			self.menv.addAction(entry)

			entry = QAction(QIcon(APPLICATION_ICON),"tick",self)
			entry.triggered.connect(lambda state,u="tick",v=["client","uptime"]: self.doInsertEventMethod(u,v))
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

			entry = QAction(QIcon(APPLICATION_ICON),f"{config.ISSUE_COMMAND_SYMBOL}call method",self)
			entry.triggered.connect(self.insertCallMethod)
			self.pInsertMenu.addAction(entry)

		if not self.python:
			self.commandMenu = self.menubar.addMenu("Commands")

			self.ircCommands = self.commandMenu.addMenu(QIcon(CONNECT_ICON),"IRC")

			entry = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
			entry.triggered.connect(self.insertJoin)
			self.ircCommands.addAction(entry)

			entry = QAction(QIcon(CHANNEL_ICON),"Part channel",self)
			entry.triggered.connect(self.insertPart)
			self.ircCommands.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"Send private message",self)
			entry.triggered.connect(self.insertPM)
			self.ircCommands.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"Send notice",self)
			entry.triggered.connect(self.insertNotice)
			self.ircCommands.addAction(entry)

			entry = QAction(QIcon(PRIVATE_ICON),"Set nickname",self)
			entry.triggered.connect(self.insertNick)
			self.ircCommands.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"Connect to server",self)
			entry.triggered.connect(self.insertConnect)
			self.ircCommands.addAction(entry)

			entry = QAction(QIcon(CONNECT_ICON),"Connect to server (reconnecting)",self)
			entry.triggered.connect(self.insertReConnect)
			self.ircCommands.addAction(entry)

			entry = QAction(QIcon(DISCONNECT_ICON),"Quit server",self)
			entry.triggered.connect(self.insertQuit)
			self.ircCommands.addAction(entry)

			entry = QAction(QIcon(DISCONNECT_ICON),"Quit all servers",self)
			entry.triggered.connect(self.insertAllQuit)
			self.ircCommands.addAction(entry)

			self.appCommands = self.commandMenu.addMenu(QIcon(APPLICATION_ICON),"Application")

			entry = QAction(QIcon(WINDOW_ICON),f"Set window size",self)
			entry.triggered.connect(self.insertAppSize)
			self.appCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),f"Move window",self)
			entry.triggered.connect(self.insertAppMove)
			self.appCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Minimize window",self)
			entry.triggered.connect(lambda state,u=f"{config.ISSUE_COMMAND_SYMBOL}window minimize": self.insertIntoEditor(u))
			self.appCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Maximize window",self)
			entry.triggered.connect(lambda state,u=f"{config.ISSUE_COMMAND_SYMBOL}window maximize": self.insertIntoEditor(u))
			self.appCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Restore window",self)
			entry.triggered.connect(lambda state,u=f"{config.ISSUE_COMMAND_SYMBOL}window restore": self.insertIntoEditor(u))
			self.appCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),f"Restart {APPLICATION_NAME}",self)
			entry.triggered.connect(lambda state,u=f"{config.ISSUE_COMMAND_SYMBOL}window restart": self.insertIntoEditor(u))
			self.appCommands.addAction(entry)

			entry = QAction(QIcon(QUIT_ICON),f"Exit {APPLICATION_NAME}",self)
			entry.triggered.connect(self.insertExit)
			self.appCommands.addAction(entry)

			self.winCommands = self.commandMenu.addMenu(QIcon(WINDOW_ICON),"Subwindows")

			entry = QAction(QIcon(WINDOW_ICON),"Focus window",self)
			entry.triggered.connect(self.insertFocus)
			self.winCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Maximize window",self)
			entry.triggered.connect(self.insertMax)
			self.winCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Minimize window",self)
			entry.triggered.connect(self.insertMin)
			self.winCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Restore window",self)
			entry.triggered.connect(self.insertRestore)
			self.winCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Show window",self)
			entry.triggered.connect(self.insertShow)
			self.winCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Hide window",self)
			entry.triggered.connect(self.insertHide)
			self.winCommands.addAction(entry)

			entry = QAction(QIcon(NEXT_ICON),"Next subwindow",self)
			entry.triggered.connect(self.insertNext)
			self.winCommands.addAction(entry)

			entry = QAction(QIcon(BACK_ICON),"Previous subwindow",self)
			entry.triggered.connect(self.insertPrevious)
			self.winCommands.addAction(entry)

			self.scriptCommands = self.commandMenu.addMenu(QIcon(SCRIPT_ICON),"Scripting")

			if config.ENABLE_INSERT_COMMAND:
				entry = QAction(QIcon(OPENFILE_ICON),"Insert script",self)
				entry.triggered.connect(self.insertScriptInsert)
				self.scriptCommands.addAction(entry)

			if config.ENABLE_ALIASES:
				entry = QAction(QIcon(EDIT_ICON),"Create alias",self)
				entry.triggered.connect(self.insertAlias)
				self.scriptCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Switch context",self)
			entry.triggered.connect(self.insertContext)
			self.scriptCommands.addAction(entry)

			entry = QAction(QIcon(TIMESTAMP_ICON),"Pause",self)
			entry.triggered.connect(self.insertPause)
			self.scriptCommands.addAction(entry)

			entry = QAction(QIcon(SCRIPT_ICON),"Set usage",self)
			entry.triggered.connect(self.insertUsage)
			self.scriptCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Restrict script",self)
			entry.triggered.connect(self.insertRestrict)
			self.scriptCommands.addAction(entry)

			entry = QAction(QIcon(QUIT_ICON),"End script",self)
			entry.triggered.connect(self.insertEnd)
			self.scriptCommands.addAction(entry)

			entry = QAction(QIcon(EDIT_ICON),f"If statement",self)
			entry.triggered.connect(self.insertIf)
			self.scriptCommands.addAction(entry)

			if config.ENABLE_DELAY_COMMAND:
				entry = QAction(QIcon(EXE_ICON),"Delay command",self)
				entry.triggered.connect(self.insertDelay)
				self.scriptCommands.addAction(entry)

			self.commentCommands = self.commandMenu.addMenu(QIcon(EDIT_ICON),"Comments")

			entry = QAction(QIcon(EDIT_ICON),"Insert multiline comment",self)
			entry.triggered.connect(self.insertMLComment)
			self.commentCommands.addAction(entry)

			entry = QAction(QIcon(EDIT_ICON),"Insert comment",self)
			entry.triggered.connect(self.insertComment)
			self.commentCommands.addAction(entry)

			self.displayCommands = self.commandMenu.addMenu(QIcon(EDIT_ICON),"Display")

			entry = QAction(QIcon(EDIT_ICON),"Print text",self)
			entry.triggered.connect(self.insertWrite)
			self.displayCommands.addAction(entry)

			entry = QAction(QIcon(EDIT_ICON),"Print system message",self)
			entry.triggered.connect(self.insertWriteSystem)
			self.displayCommands.addAction(entry)

			entry = QAction(QIcon(WINDOW_ICON),"Display message box",self)
			entry.triggered.connect(self.insertBox)
			self.displayCommands.addAction(entry)

			entry = QAction(QIcon(EXE_ICON),"Create macro",self)
			entry.triggered.connect(self.insertMacro)
			self.commandMenu.addAction(entry)

			entry = QAction(QIcon(EXE_ICON),"Execute script",self)
			entry.triggered.connect(self.insertScript)
			self.commandMenu.addAction(entry)

			if config.ENABLE_HOTKEYS:
				entry = QAction(QIcon(INPUT_ICON),"Bind hotkey",self)
				entry.triggered.connect(self.insertBind)
				self.commandMenu.addAction(entry)

			entry = QAction(QIcon(NOTIFICATION_ICON),"Play a sound",self)
			entry.triggered.connect(self.insertPlay)
			self.commandMenu.addAction(entry)

			if config.ENABLE_ALIASES:
				self.aliasMenu = self.menubar.addMenu("Aliases")

				self.buildAliasMenu(self.aliasMenu)

			self.runMenu = self.menubar.addMenu("Run")

			self.runMenu.aboutToShow.connect(self.buildRunMenu)

		self.setCentralWidget(self.editor)

		if self.python and not self.filename and not self.blank:
			self.doNewPlugin()
			self.changed = True

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

	def insertContext(self):
		e = dialog.SetWindowDialog("Context",self)

		if not e: return

		self.editor.insertPlainText("context "+str(e)+"\n")
		self.updateApplicationTitle()

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
		self.menuSave.setEnabled(True)
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
		self.menuSave.setEnabled(True)
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
		self.menuSave.setEnabled(True)
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
		self.menuSave.setEnabled(True)
		self.changed = False
		self.menuSave.setShortcut(QKeySequence())
		self.menuSaveAs.setShortcut("Ctrl+S")
		self.editing_user_script = True
		self.current_user_script = hostid
		self.updateApplicationTitle()

	def insertConnect(self):
		x = dialog.ConnectServer(self)
		e = x.get_server_information(self)

		if not e: return

		host = e[0]
		port = e[1]
		password = e[2]
		ssl = e[3]

		if e[4]==True:
			if ssl==True:
				my_command = config.ISSUE_COMMAND_SYMBOL+"xconnectssl"
			else:
				my_command = config.ISSUE_COMMAND_SYMBOL+"xconnect"
		else:
			if ssl==True:
				my_command = config.ISSUE_COMMAND_SYMBOL+"connectssl"
			else:
				my_command = config.ISSUE_COMMAND_SYMBOL+"connect"

		if len(port)==0: port = "6667"

		if len(password)==0:
			cmd = host+" "+port+"\n"
		else:
			cmd = host+" "+port+" "+password+"\n"

		self.editor.insertPlainText(my_command+" "+cmd)
		self.updateApplicationTitle()

	def insertReConnect(self):
		x = dialog.ConnectServer(self)
		e = x.get_server_information(self)

		if not e: return

		host = e[0]
		port = e[1]
		password = e[2]
		ssl = e[3]

		if e[4]==True:
			if ssl==True:
				my_command = config.ISSUE_COMMAND_SYMBOL+"xreconnectssl"
			else:
				my_command = config.ISSUE_COMMAND_SYMBOL+"xreconnect"
		else:
			if ssl==True:
				my_command = config.ISSUE_COMMAND_SYMBOL+"reconnectssl"
			else:
				my_command = config.ISSUE_COMMAND_SYMBOL+"reconnect"

		if len(port)==0: port = "6667"

		if len(password)==0:
			cmd = host+" "+port+"\n"
		else:
			cmd = host+" "+port+" "+password+"\n"

		self.editor.insertPlainText(my_command+" "+cmd)
		self.updateApplicationTitle()

	def insertAppMove(self):
		x = dialog.WindowInfo(self,"X Value","Y Value","pixels")
		if x:
			w = x[0]
			h = x[1]

			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+f"window move {w} {h}\n")
			self.updateApplicationTitle()

	def insertAppSize(self):
		x = dialog.WindowInfo(self,"Width","Height","pixels")
		if x:
			w = x[0]
			h = x[1]

			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+f"window size {w} {h}\n")
			self.updateApplicationTitle()

	def insertAllQuit(self):
		x = dialog.SetQuit(config.DEFAULT_QUIT_MESSAGE,self)
		e = x.get_message_information(config.DEFAULT_QUIT_MESSAGE,self)

		if e==None: return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"quitall "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertQuit(self):
		x = dialog.SetQuit(config.DEFAULT_QUIT_MESSAGE,self)
		e = x.get_message_information(config.DEFAULT_QUIT_MESSAGE,self)

		if e==None: return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"quit "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertNext(self):
		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"next\n")
		self.updateApplicationTitle()

	def insertPrevious(self):
		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"previous\n")
		self.updateApplicationTitle()

	def insertHide(self):
		e = dialog.SetWindowDialog("Hide",self)

		if not e:
			return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"hide "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertFocus(self):
		e = dialog.SetWindowDialog("Focus",self)

		if not e:
			return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"focus "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertShow(self):
		e = dialog.SetWindowDialog("Show",self)

		if not e:
			return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"show "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertRestore(self):
		e = dialog.SetWindowDialog("Restore",self)

		if not e:
			return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"restore "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertMin(self):
		e = dialog.SetWindowDialog("Minimize",self)

		if not e:
			return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"minimize "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertMax(self):
		e = dialog.SetWindowDialog("Maximize",self)

		if not e:
			return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"maximize "+str(e)+"\n")
		self.updateApplicationTitle()

	def show_error_message(self,title, message):
		msg_box = QMessageBox()
		msg_box.setIcon(QMessageBox.Critical)
		msg_box.setWindowTitle(title)
		msg_box.setWindowIcon(QIcon(APPLICATION_ICON))
		msg_box.setText(message)
		msg_box.setStandardButtons(QMessageBox.Ok)
		msg_box.exec_()

	def insertExit(self):
		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"exit\n")
		self.updateApplicationTitle()

	def insertEnd(self):
		self.editor.insertPlainText("end\n")
		self.updateApplicationTitle()

	def insertPlay(self):
		desktop =  os.path.join(os.path.expanduser("~"), "Desktop")
		if not os.path.isdir(desktop): desktop = os.path.expanduser("~")
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open WAV", desktop, f"WAV file (*.wav)", options=options)
		if fileName:
			if is_wav_file(fileName):
				self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"play "+fileName+"\n")
				self.updateApplicationTitle()
			else:
				self.show_error_message("Wrong file type","File is not a WAV file!\nOnly WAV files can be used with the "+config.ISSUE_COMMAND_SYMBOL+"play command.\nPlease select a valid file.")

	def insertAlias(self):
		x = dialog.SetAlias(self)
		e = x.get_alias_information(self)

		if not e: return

		aname = e[0]
		avalue = e[1]

		if len(aname)==0: return
		if len(avalue)==0: avalue = 'X'

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"alias "+aname+" "+avalue+"\n")
		self.updateApplicationTitle()

	def insertIf(self):
		x = dialog.SetIf(self)
		e = x.get_if_information(self)

		if not e: return

		val1 = str(e[0])
		operator = str(e[1])
		val2 = str(e[2])
		command = str(e[3])

		self.editor.insertPlainText(f"if {val1} {operator} {val2} {command}\n")
		self.updateApplicationTitle()

	def insertDelay(self):
		x = dialog.SetDelay(self)
		e = x.get_alias_information(self)

		if not e: return

		aname = str(e[0])
		avalue = str(e[1])

		if len(aname)==0: return
		if len(avalue)>0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"delay "+aname+" "+avalue+"\n")
			self.updateApplicationTitle()
		else:
			return

	def insertUsage(self):
		x = dialog.SetUsage(self)
		e = x.get_alias_information(self)

		if not e: return

		aname = str(e[0])
		avalue = str(e[1])

		if len(aname)==0: return
		if len(avalue)>0:
			self.editor.insertPlainText("usage "+aname+" "+avalue+"\n")
		else:
			self.editor.insertPlainText("usage "+aname+"\n")

		self.updateApplicationTitle()

	def insertPart(self):
		x = dialog.PartChannel(self)
		e = x.get_channel_information(self)

		if not e: return

		channel = e[0]
		msg = e[1]

		if len(msg)==0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"part "+channel+"\n")
			self.updateApplicationTitle()
		else:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"part "+channel+" "+msg+"\n")
			self.updateApplicationTitle()

	def insertNick(self):
		x = dialog.SetNick(self)
		e = x.get_nick_information(self)

		if not e: return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"nick "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertBind(self):
		x = dialog.SetBind(self)
		e = x.get_script_information(self)

		if not e: return
		if len(e[0].strip())==0: return
		if len(e[1].strip())==0: return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+f"bind {e[0]} {e[1]}\n")
		self.updateApplicationTitle()

	def insertScriptInsert(self):
		x = dialog.SetInsert(self)
		e = x.get_script_information(self)

		if not e: return

		self.editor.insertPlainText("insert "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertMacro(self):
		x = dialog.SetMacro(self)
		e = x.get_script_information(self)

		if not e: return

		name = e[0]
		script = e[1]
		usage = e[2]
		mhelp = e[3]

		if usage.strip()=='':
			if mhelp.strip()!='':
				usage = f"{config.ISSUE_COMMAND_SYMBOL}{name} ARGUMENTS"

		if ' ' in script:
			script = script.replace('"','\\"')
			script = f"\"{script}\""
		if ' ' in usage:
			usage = usage.replace('"','\\"')
			usage = f"\"{usage}\""
		if ' ' in mhelp:
			mhelp = mhelp.replace('"','\\"')
			mhelp = f"\"{mhelp}\""
		
		if usage.strip()!='' and mhelp.strip()=='':
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"macro "+str(name)+" "+str(script)+" "+str(usage)+"\n")
			self.updateApplicationTitle()
			return

		if usage.strip()!='' and mhelp.strip()!='':
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"macro "+str(name)+" "+str(script)+" "+str(usage)+" "+str(mhelp)+"\n")
			self.updateApplicationTitle()
			return


		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"macro "+str(name)+" "+str(script)+"\n")
		self.updateApplicationTitle()

	def insertScript(self):
		x = dialog.SetScript(self)
		e = x.get_script_information(self)

		if not e: return

		script = e[0]
		args = e[1]

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"script "+str(script)+" "+str(args)+"\n")
		self.updateApplicationTitle()

	def insertNotice(self):
		x = dialog.SendNotice(self)
		e = x.get_message_information(self)

		if not e: return

		target = e[0]
		msg = e[1]
		
		if len(target)>0 and len(msg)>0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"notice "+target+" "+msg+"\n")
			self.updateApplicationTitle()

	def insertWriteSystem(self):
		x = dialog.PrintMsg(self)
		e = x.get_message_information(self)

		if not e: return

		if len(e)>0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"prints "+e+"\n")
			self.updateApplicationTitle()

	def insertWrite(self):
		x = dialog.PrintMsg(self)
		e = x.get_message_information(self)

		if not e: return

		if len(e)>0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"print "+e+"\n")
			self.updateApplicationTitle()

	def insertBox(self):
		x = dialog.PrintMsg(self)
		e = x.get_message_information(self)

		if not e: return

		if len(e)>0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"msgbox "+e+"\n")
			self.updateApplicationTitle()

	def insertPM(self):
		x = dialog.SendPM(self)
		e = x.get_message_information(self)

		if not e: return

		target = e[0]
		msg = e[1]
		
		if len(target)>0 and len(msg)>0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"msg "+target+" "+msg+"\n")
			self.updateApplicationTitle()

	def insertPause(self):
		x = dialog.Pause(self)
		e = x.get_time_information(self)

		if not e: return

		self.editor.insertPlainText("wait "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertRestrict(self):
		x = dialog.SetRestrict(self)
		e = x.get_restrict_information(self)

		if not e: return

		self.editor.insertPlainText("restrict "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertMLComment(self):
		x = dialog.Comment(False,self)
		e = x.get_message_information(False,self)

		if not e: return

		if len(e)>0:
			for l in e.split("\n"):
				self.editor.insertPlainText(f"{config.ISSUE_COMMAND_SYMBOL}rem {l}\n")

			self.updateApplicationTitle()

	def insertComment(self):
		x = dialog.Comment(True,self)
		e = x.get_message_information(True,self)

		if not e: return

		if len(e)>0:
			self.editor.insertPlainText(f"{config.ISSUE_COMMAND_SYMBOL}rem {e}\n")
			self.updateApplicationTitle()

	def insertJoin(self):
		x = dialog.JoinChannel(self)
		e = x.get_channel_information(self)

		if not e: return

		channel = e[0]
		key = e[1]

		if len(key)==0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"join "+channel+"\n")
			self.updateApplicationTitle()
		else:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"join "+channel+" "+key+"\n")
			self.updateApplicationTitle()

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
		else:
			self.setWindowTitle(f"Untitled")
			self.name = "Untitled"
			self.status_file.setText(f"<small><b>{self.name}</b></small>")		
		
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
			self.menuSave.setEnabled(True)
			self.updateApplicationTitle()
			self.menuSave.setShortcut("Ctrl+S")
			self.menuSaveAs.setShortcut(QKeySequence())

	def doNewFile(self):

		self.check_for_save()

		self.filename = None
		self.editor.clear()
		self.menuSave.setEnabled(False)
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
			self.menuSave.setEnabled(True)
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
		indents = []
		
		for line in lines:
			stripped = line.lstrip()
			if line != stripped and stripped: 
				indent = line[:len(line) - len(stripped)]
				indents.append(indent)
		
		if indents:
			most_common = Counter(indents).most_common(1)[0][0]
			return most_common
			
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

