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

from ..resources import *
from ..dialog import *
from .. import config
from .. import syntax
from .. import commands
from .. import user
from .text_separator import textSeparatorLabel,textSeparator
from .extendedmenuitem import MenuLabel,menuHtml

class Window(QMainWindow):

	def is_multi_line_selection_by_block(self):
		cursor = self.editor.textCursor()
		if cursor.hasSelection():
			start_position = cursor.selectionStart()
			end_position = cursor.selectionEnd()

			temp_cursor = self.editor.textCursor()

			temp_cursor.setPosition(start_position)
			start_block_number = temp_cursor.blockNumber()

			temp_cursor.setPosition(end_position)
			end_block_number = temp_cursor.blockNumber()

			return start_block_number != end_block_number
		return False

	def comment_selected(self):
		cursor = self.editor.textCursor()
		selected_text = cursor.selectedText()

		if selected_text:

			if self.is_multi_line_selection_by_block():
				selected_text = re.sub(os.linesep + r'\Z','',selected_text)
				text = "/*\n"+selected_text+"\n*/"
			else:
				text = "/* "+selected_text+" */"
			
			cursor.beginEditBlock()
			cursor.insertText(text)
			cursor.endEditBlock()

	def show_context_menu(self,pos):

		menu = self.editor.createStandardContextMenu()

		menu.addSeparator()

		commented = QAction(QIcon(SCRIPT_ICON),"Comment out selection", self)
		commented.triggered.connect(self.comment_selected)
		menu.addAction(commented)

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
		
		# smenu = menu.addMenu(QIcon(SETTINGS_ICON),"Config Values")
		# settings = config.build_settings()
		# for s in settings:
		# 	if s=="timestamp_format": continue
		# 	if s=="log_absolutely_all_messages_of_any_type": continue
		# 	if not type(settings[s]) is list:
		# 		if type(settings[s]).__name__=='bool':
		# 			dtype = "boolean"
		# 		elif type(settings[s]).__name__=='int':
		# 			dtype = "integer"
		# 		elif type(settings[s]).__name__=='str':
		# 			dtype = "string"
		# 		else:
		# 			dtype = "unknown"
		# 		entry = QAction(QIcon(SCRIPT_ICON),f"{s} ({dtype})",self)
		# 		entry.triggered.connect(lambda state,u=f"{s}": self.insertIntoEditor(u))
		# 		smenu.addAction(entry)

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

		selected_text = self.editor.textCursor().selectedText()
		commented.setEnabled(bool(selected_text))

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
		if self.wordwrap:
			self.editor.setLineWrapMode(QPlainTextEdit.NoWrap)
			self.wordwrap = False
			self.ww_menu.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			self.editor.setLineWrapMode(QPlainTextEdit.WidgetWidth)
			self.wordwrap = True
			self.ww_menu.setIcon(QIcon(self.parent.checked_icon))

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

		self.editMenu.addSeparator()

		mefind = QAction(QIcon(BAN_ICON),"Strip all comments",self)
		mefind.triggered.connect(self.doStrip)
		self.editMenu.addAction(mefind)

	def generateStylesheet(self,obj,fore,back):

		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def refreshHighlighter(self):
		reset = False
		if self.changed==False: reset = True
		if config.EDITOR_USES_SYNTAX_HIGHLIGHTING:
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

	def doStrip(self):
		s = self.editor.toPlainText()
		s = re.sub(re.compile("/\\*.*?\\*/",re.DOTALL ) ,"" ,s)
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

	def __init__(self,filename=None,parent=None,subwindow=None):
		super(Window, self).__init__(parent)

		self.filename = filename
		self.parent = parent
		self.changed = False
		self.cscript_menu = None
		self.window_type = EDITOR_WINDOW
		self.subwindow = subwindow

		self.editing_user_script = False
		self.current_user_script = None
		self.findWindow = None

		self.name = "Untitled script"

		# Load in user settings
		user.load_user(user.USER_FILE)

		self.subwindow_id = str(uuid.uuid4())

		self.editor = QPlainTextEdit(self)

		self.editor.cursorPositionChanged.connect(self.update_line_number)

		if config.EDITOR_USES_SYNTAX_HIGHLIGHTING:
			self.highlight = syntax.MerkScriptHighlighter(self.editor.document())
			self.editor.setStyleSheet(self.generateStylesheet('QPlainTextEdit',config.SYNTAX_FOREGROUND,config.SYNTAX_BACKGROUND))
		else:
			self.highlight = None

		self.wordwrap = True
		self.editor.setLineWrapMode(QPlainTextEdit.WidgetWidth)

		self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
		self.editor.customContextMenuRequested.connect(self.show_context_menu)

		self.setWindowIcon(QIcon(SCRIPT_ICON))

		self.editor.textChanged.connect(self.docModified)
		self.editor.redoAvailable.connect(self.hasRedo)
		self.editor.undoAvailable.connect(self.hasUndo)
		self.editor.copyAvailable.connect(self.hasCopy)

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

		if self.wordwrap:
			self.ww_menu = QAction(QIcon(self.parent.checked_icon),"Word wrap",self)
		else:
			self.ww_menu = QAction(QIcon(self.parent.unchecked_icon),"Word wrap",self)
		self.ww_menu.triggered.connect(self.toggleWordwrap)
		self.fileMenu.addAction(self.ww_menu)
		
		self.fileMenu.addSeparator()

		entry = QAction(QIcon(CLOSE_ICON),"Close",self)
		entry.triggered.connect(self.close)
		self.fileMenu.addAction(entry)

		self.editMenu = self.menubar.addMenu("Edit")

		self.buildEditMenu()

		self.commandMenu = self.menubar.addMenu("Commands")

		e = textSeparator(self,"IRC Commands")
		self.commandMenu.addAction(e)

		entry = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
		entry.triggered.connect(self.insertJoin)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(CHANNEL_ICON),"Part channel",self)
		entry.triggered.connect(self.insertPart)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(PRIVATE_ICON),"Send private message",self)
		entry.triggered.connect(self.insertPM)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(PRIVATE_ICON),"Send notice",self)
		entry.triggered.connect(self.insertNotice)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(PRIVATE_ICON),"Set nickname",self)
		entry.triggered.connect(self.insertNick)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(DISCONNECT_ICON),"Quit server",self)
		entry.triggered.connect(self.insertQuit)
		self.commandMenu.addAction(entry)

		e = textSeparator(self,"Script Commands")
		self.commandMenu.addAction(e)

		entry = QAction(QIcon(SCRIPT_ICON),"Multiline comment",self)
		entry.triggered.connect(self.insertMLComment)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Comment",self)
		entry.triggered.connect(self.insertComment)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Create alias",self)
		entry.triggered.connect(self.insertAlias)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(CONNECT_ICON),"Connect to server",self)
		entry.triggered.connect(self.insertConnect)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(EDIT_ICON),"Print to window",self)
		entry.triggered.connect(self.insertWrite)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(WINDOW_ICON),"Display message box",self)
		entry.triggered.connect(self.insertBox)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(WINDOW_ICON),"Switch context",self)
		entry.triggered.connect(self.insertContext)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Pause",self)
		entry.triggered.connect(self.insertPause)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Set usage",self)
		entry.triggered.connect(self.insertUsage)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Restrict script",self)
		entry.triggered.connect(self.insertRestrict)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(WINDOW_ICON),"Maximize window",self)
		entry.triggered.connect(self.insertMax)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(WINDOW_ICON),"Minimize window",self)
		entry.triggered.connect(self.insertMin)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(NEXT_ICON),"Next subwindow",self)
		entry.triggered.connect(self.insertNext)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(BACK_ICON),"Previous subwindow",self)
		entry.triggered.connect(self.insertPrevious)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Execute script",self)
		entry.triggered.connect(self.insertScript)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(NOTIFICATION_ICON),"Play a sound",self)
		entry.triggered.connect(self.insertPlay)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(EXE_ICON),"Insert shell command",self)
		entry.triggered.connect(self.insertShell)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(APPLICATION_ICON),"Exit application",self)
		entry.triggered.connect(self.insertExit)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"End script",self)
		entry.triggered.connect(self.insertEnd)
		self.commandMenu.addAction(entry)

		self.aliasMenu = self.menubar.addMenu("Aliases")

		self.buildAliasMenu(self.aliasMenu)

		self.runMenu = self.menubar.addMenu("Run")

		self.runMenu.aboutToShow.connect(self.buildRunMenu)

		self.setCentralWidget(self.editor)

		self.editor.setFocus()

	def buildAliasMenu(self,menu):

		entry = QAction(QIcon(SCRIPT_ICON),"Host",self)
		entry.triggered.connect(lambda state,u="$_HOST": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Filename",self)
		entry.triggered.connect(lambda state,u="$_FILE": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"User mode",self)
		entry.triggered.connect(lambda state,u="$_MODE": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Nickname",self)
		entry.triggered.connect(lambda state,u="$_NICKNAME": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Port",self)
		entry.triggered.connect(lambda state,u="$_PORT": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Present in channel",self)
		entry.triggered.connect(lambda state,u="$_PRESENT": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Realname",self)
		entry.triggered.connect(lambda state,u="$_REALNAME": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Script name",self)
		entry.triggered.connect(lambda state,u="$_SCRIPT": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Server",self)
		entry.triggered.connect(lambda state,u="$_SERVER": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"User status",self)
		entry.triggered.connect(lambda state,u="$_STATUS": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Channel topic",self)
		entry.triggered.connect(lambda state,u="$_TOPIC": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Uptime",self)
		entry.triggered.connect(lambda state,u="$_UPTIME": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Username",self)
		entry.triggered.connect(lambda state,u="$_USERNAME": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Current window",self)
		entry.triggered.connect(lambda state,u="$_WINDOW": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Window type",self)
		entry.triggered.connect(lambda state,u="$_WINDOW_TYPE": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Date",self)
		entry.triggered.connect(lambda state,u="$_DATE": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"European date",self)
		entry.triggered.connect(lambda state,u="$_EDATE": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Unix epoch",self)
		entry.triggered.connect(lambda state,u="$_EPOCH": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Client name",self)
		entry.triggered.connect(lambda state,u="$_CLIENT": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Client version",self)
		entry.triggered.connect(lambda state,u="$_VERSION": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Client source code URL",self)
		entry.triggered.connect(lambda state,u="$_SOURCE": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Client uptime",self)
		entry.triggered.connect(lambda state,u="$_CUPTIME": self.insertIntoEditor(u))
		menu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Timestamp",self)
		entry.triggered.connect(lambda state,u="$_TIMESTAMP": self.insertIntoEditor(u))
		menu.addAction(entry)

	def insertContext(self):
		e = SetWindowDialog("Context",self)

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
					network = "Unknown network"
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
						network = "Unknown network"
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

	def doNewScript(self):

		self.check_for_save()

		x = NewConnectScript(self)
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
		x = ConnectServer(self)
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


	def insertQuit(self):
		x = SetQuit(config.DEFAULT_QUIT_MESSAGE,self)
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

	def insertMin(self):
		e = SetWindowDialog("Minimize",self)

		if not e: return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"minimize "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertMax(self):
		e = SetWindowDialog("Maximize",self)

		if not e: return

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

	def insertShell(self):
		x = SetShell(self)
		e = x.get_alias_information(self)

		if not e: return

		aname = e[0]
		avalue = e[1]

		if len(aname)==0: return
		if len(avalue)==0: avalue = 'X'

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"shell "+aname+" "+avalue+"\n")
		self.updateApplicationTitle()

	def insertAlias(self):
		x = SetAlias(self)
		e = x.get_alias_information(self)

		if not e: return

		aname = e[0]
		avalue = e[1]

		if len(aname)==0: return
		if len(avalue)==0: avalue = 'X'

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"alias "+aname+" "+avalue+"\n")
		self.updateApplicationTitle()

	def insertUsage(self):
		x = SetUsage(self)
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
		x = PartChannel(self)
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
		x = SetNick(self)
		e = x.get_nick_information(self)

		if not e: return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"nick "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertScript(self):
		x = SetScript(self)
		e = x.get_script_information(self)

		if not e: return

		script = e[0]
		args = e[1]

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"script "+str(script)+" "+str(args)+"\n")
		self.updateApplicationTitle()

	def insertNotice(self):
		x = SendNotice(self)
		e = x.get_message_information(self)

		if not e: return

		target = e[0]
		msg = e[1]
		
		if len(target)>0 and len(msg)>0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"notice "+target+" "+msg+"\n")
			self.updateApplicationTitle()

	def insertWrite(self):
		x = PrintMsg(self)
		e = x.get_message_information(self)

		if not e: return

		if len(e)>0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"print "+e+"\n")
			self.updateApplicationTitle()

	def insertBox(self):
		x = PrintMsg(self)
		e = x.get_message_information(self)

		if not e: return

		if len(e)>0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"msgbox "+e+"\n")
			self.updateApplicationTitle()

	def insertPM(self):
		x = SendPM(self)
		e = x.get_message_information(self)

		if not e: return

		target = e[0]
		msg = e[1]
		
		if len(target)>0 and len(msg)>0:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"msg "+target+" "+msg+"\n")
			self.updateApplicationTitle()

	def insertPause(self):
		x = Pause(self)
		e = x.get_time_information(self)

		if not e: return

		self.editor.insertPlainText("wait "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertRestrict(self):
		x = SetRestrict(self)
		e = x.get_restrict_information(self)

		if not e: return

		self.editor.insertPlainText("restrict "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertMLComment(self):
		x = Comment(False,self)
		e = x.get_message_information(False,self)

		if not e: return

		if len(e)>0:
			self.editor.insertPlainText("/*\n"+e+"\n*/\n")
			self.updateApplicationTitle()

	def insertComment(self):
		x = Comment(True,self)
		e = x.get_message_information(True,self)

		if not e: return

		if len(e)>0:
			self.editor.insertPlainText("/* "+e+" */\n")
			self.updateApplicationTitle()

	def insertJoin(self):
		x = JoinChannel(self)
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
			self.setWindowTitle(f"Unnamed {APPLICATION_NAME} script")
			self.name = "Untitled script"
			self.status_file.setText(f"<small><b>{self.name}</b></small>")
		
		self.parent.buildWindowsMenu()

		w = self.parent.getEditorWindow(self.subwindow_id)
		a = self.parent.MDI.activeSubWindow()
		if w==a: self.parent.merk_subWindowActivated(w)


	def doFileSaveAs(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save script as...",commands.SCRIPTS_DIRECTORY,f"{APPLICATION_NAME} Script (*.{SCRIPT_FILE_EXTENSION});;All Files (*)", options=options)
		if fileName:
			_, file_extension = os.path.splitext(fileName)
			if file_extension=='':
				efl = len(SCRIPT_FILE_EXTENSION)+1
				if fileName[-efl:].lower()!=f".{SCRIPT_FILE_EXTENSION}": fileName = fileName+f".{SCRIPT_FILE_EXTENSION}"
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

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open Script", commands.SCRIPTS_DIRECTORY, f"{APPLICATION_NAME} Script (*.{SCRIPT_FILE_EXTENSION});;Text Files (*.txt);;All Files (*)", options=options)
		if fileName:
			script = open(fileName,"r",encoding="utf-8",errors="ignore")
			self.editor.setPlainText(script.read())
			script.close()
			self.filename = fileName
			self.changed = False
			self.updateApplicationTitle()
			self.menuSave.setEnabled(True)
			self.menuSave.setShortcut("Ctrl+S")
			self.menuSaveAs.setShortcut(QKeySequence())
			self.editing_user_script = False
			self.current_user_script = None

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

		code = open(self.filename,"w",encoding="utf-8",errors="ignore")
		code.write(self.editor.toPlainText())
		code.close()
		self.changed = False
		self.updateApplicationTitle()

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

