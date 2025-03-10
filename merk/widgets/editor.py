#
# ███╗   ███╗██████╗ ██████╗ ██╗  ██╗
# ████╗ ████║╚═══╗██╗██╔══██╗██║ ██╔╝
# ██╔████╔██║███████║██████╔╝█████╔╝
# ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗
# ██║ ╚═╝ ██║ █████╔╝██║  ██║██║  ██╗
# ╚═╝     ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
# Copyright (C) 2021  Daniel Hetrick
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

from ..resources import *
from ..dialog import *
from .. import config
from .. import syntax
from .. import commands
from .. import user
from .text_separator import textSeparatorLabel,textSeparator

class Window(QMainWindow):

	def closeEvent(self, event):

		# Make sure the MDI window is closed
		self.parent.closeSubWindow(self.subwindow_id)

		event.accept()
		self.close()

	def readConnect(self,hostid,contents):

		self.editing_user_script = True
		self.current_user_script = hostid

		self.editor.setPlainText(contents)
		self.menuSave.setEnabled(True)
		self.changed = False
		self.updateApplicationTitle()

	def __init__(self,filename=None,parent=None):
		super(Window, self).__init__(parent)

		self.filename = filename
		self.parent = parent
		self.changed = False

		self.editing_user_script = False
		self.current_user_script = None

		# Load in user settings
		user.load_user(user.USER_FILE)

		self.subwindow_id = str(uuid.uuid4())

		self.editor = QPlainTextEdit(self)
		self.highlight = syntax.MerkScriptHighlighter(self.editor.document())

		p = self.editor.palette()
		p.setColor(QPalette.Base, QColor(config.SYNTAX_BACKGROUND))
		p.setColor(QPalette.Text, QColor(config.SYNTAX_FOREGROUND))
		self.editor.setPalette(p)

		self.setWindowIcon(QIcon(SCRIPT_ICON))

		self.editor.textChanged.connect(self.docModified)
		self.editor.redoAvailable.connect(self.hasRedo)
		self.editor.undoAvailable.connect(self.hasUndo)
		self.editor.copyAvailable.connect(self.hasCopy)

		self.updateApplicationTitle()

		if self.filename:
			f = commands.find_script(self.filename)
			if f!=None:
				x = open(f,mode="r",encoding="utf-8",errors="ignore")
				source_code = str(x.read())
				x.close()
				self.editor.setPlainText(source_code)
				self.changed = False
				self.updateApplicationTitle()

		self.menubar = self.menuBar()

		self.fileMenu = self.menubar.addMenu("File")

		entry = QAction(QIcon(NEWFILE_ICON),"New file",self)
		entry.triggered.connect(self.doNewFile)
		entry.setShortcut("Ctrl+N")
		self.fileMenu.addAction(entry)

		entry = QAction(QIcon(OPENFILE_ICON),"Open file",self)
		entry.triggered.connect(self.doFileOpen)
		entry.setShortcut("Ctrl+O")
		self.fileMenu.addAction(entry)

		self.menuSave = QAction(QIcon(SAVEFILE_ICON),"Save",self)
		self.menuSave.triggered.connect(self.doFileSave)
		if self.filename: self.menuSave.setShortcut("Ctrl+S")
		self.fileMenu.addAction(self.menuSave)

		if self.filename==None:
			self.menuSave.setEnabled(False)

		self.menuSaveAs = QAction(QIcon(SAVEASFILE_ICON),"Save as...",self)
		self.menuSaveAs.triggered.connect(self.doFileSaveAs)
		if not self.filename: self.menuSaveAs.setShortcut("Ctrl+S")
		self.fileMenu.addAction(self.menuSaveAs)

		self.fileMenu.addSeparator()

		if len(user.COMMANDS)>0:

			sm = self.fileMenu.addMenu(QIcon(CONNECT_ICON),"Open connection script")

			for host in user.COMMANDS:
				entry = QAction(QIcon(SCRIPT_ICON),f"{host}",self)
				entry.triggered.connect(lambda state,x=host,f=user.COMMANDS[host]: self.readConnect(x,f))
				sm.addAction(entry)

			self.fileMenu.addSeparator()


		entry = QAction(QIcon(QUIT_ICON),"Exit",self)
		entry.triggered.connect(self.close)
		self.fileMenu.addAction(entry)

		editMenu = self.menubar.addMenu("Edit")

		entry = QAction(QIcon(SELECTALL_ICON),"Select All",self)
		entry.triggered.connect(self.editor.selectAll)
		entry.setShortcut("Ctrl+A")
		editMenu.addAction(entry)

		editMenu.addSeparator()

		self.menuUndo = QAction(QIcon(UNDO_ICON),"Undo",self)
		self.menuUndo.triggered.connect(self.editor.undo)
		self.menuUndo.setShortcut("Ctrl+Z")
		editMenu.addAction(self.menuUndo)
		self.menuUndo.setEnabled(False)

		self.menuRedo = QAction(QIcon(REDO_ICON),"Redo",self)
		self.menuRedo.triggered.connect(self.editor.redo)
		self.menuRedo.setShortcut("Ctrl+Y")
		editMenu.addAction(self.menuRedo)
		self.menuRedo.setEnabled(False)

		editMenu.addSeparator()

		self.menuCut = QAction(QIcon(CUT_ICON),"Cut",self)
		self.menuCut.triggered.connect(self.editor.cut)
		self.menuCut.setShortcut("Ctrl+X")
		editMenu.addAction(self.menuCut)
		self.menuCut.setEnabled(False)

		self.menuCopy = QAction(QIcon(COPY_ICON),"Copy",self)
		self.menuCopy.triggered.connect(self.editor.copy)
		self.menuCopy.setShortcut("Ctrl+C")
		editMenu.addAction(self.menuCopy)
		self.menuCopy.setEnabled(False)

		self.menuPaste = QAction(QIcon(CLIPBOARD_ICON),"Paste",self)
		self.menuPaste.triggered.connect(self.editor.paste)
		self.menuPaste.setShortcut("Ctrl+V")
		editMenu.addAction(self.menuPaste)

		editMenu.addSeparator()

		self.menuZoomIn = QAction(QIcon(PLUS_ICON),"Zoom in",self)
		self.menuZoomIn.triggered.connect(self.editor.zoomIn)
		self.menuZoomIn.setShortcut("Ctrl++")
		editMenu.addAction(self.menuZoomIn)

		self.menuZoomOut = QAction(QIcon(MINUS_ICON),"Zoom out",self)
		self.menuZoomOut.triggered.connect(self.editor.zoomOut)
		self.menuZoomOut.setShortcut("Ctrl+-")
		editMenu.addAction(self.menuZoomOut)

		self.commandMenu = self.menubar.addMenu("Insert")

		e = textSeparator(self,"IRC Commands")
		self.commandMenu.addAction(e)

		entry = QAction(QIcon(CHANNEL_ICON),"Join channel",self)
		entry.triggered.connect(self.insertJoin)
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

		e = textSeparator(self,"Script Commands")
		self.commandMenu.addAction(e)

		entry = QAction(QIcon(SCRIPT_ICON),"Comment",self)
		entry.triggered.connect(self.insertComment)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Multiline comment",self)
		entry.triggered.connect(self.insertMLComment)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Pause",self)
		entry.triggered.connect(self.insertPause)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(EDIT_ICON),"Print to window",self)
		entry.triggered.connect(self.insertWrite)
		self.commandMenu.addAction(entry)

		self.setCentralWidget(self.editor)

		self.editor.setFocus()

	def insertNick(self):
		x = SetNick(self)
		e = x.get_nick_information(self)

		if not e: return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"nick "+str(e)+"\n")
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

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"wait "+str(e)+"\n")
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
				self.setWindowTitle("* Connection script for "+self.current_user_script)
			else:
				self.setWindowTitle("Connection script for "+self.current_user_script)
			return

		if self.filename!=None:
			base = os.path.basename(self.filename)
			if self.changed:
				self.setWindowTitle("* "+base)
			else:
				self.setWindowTitle(base)
		else:
			self.setWindowTitle(f"Unnamed {APPLICATION_NAME} script")

	def doFileSaveAs(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save Script As...",commands.SCRIPTS_DIRECTORY,f"{APPLICATION_NAME} Script (*.{SCRIPT_FILE_EXTENSION});;All Files (*)", options=options)
		if fileName:
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
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open Script", commands.SCRIPTS_DIRECTORY, f"{APPLICATION_NAME} Script (*.{SCRIPT_FILE_EXTENSION});;All Files (*)", options=options)
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

