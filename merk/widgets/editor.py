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

	def closeEvent(self, event):

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

	def toggleWordwrap(self):
		if self.wordwrap:
			self.editor.setLineWrapMode(QPlainTextEdit.NoWrap)
			self.wordwrap = False
		else:
			self.editor.setLineWrapMode(QPlainTextEdit.WidgetWidth)
			self.wordwrap = True
		self.buildEditMenu()


	def buildEditMenu(self):

		self.editMenu.clear()

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

		if self.wordwrap:
			entry = QAction(QIcon(self.parent.checked_icon),"Word wrap",self)
		else:
			entry = QAction(QIcon(self.parent.unchecked_icon),"Word wrap",self)
		entry.triggered.connect(self.toggleWordwrap)
		self.editMenu.addAction(entry)

	def generateStylesheet(self,obj,fore,back):

		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def refreshHighlighter(self):
		self.highlight = syntax.MerkScriptHighlighter(self.editor.document())
		self.editor.setStyleSheet(self.generateStylesheet('QPlainTextEdit',config.SYNTAX_FOREGROUND,config.SYNTAX_BACKGROUND))

	def togglePrompt(self):
		if config.EDITOR_PROMPT_SAVE:
			config.EDITOR_PROMPT_SAVE = False
			self.menuPrompt.setIcon(QIcon(self.parent.unchecked_icon))
		else:
			config.EDITOR_PROMPT_SAVE = True
			self.menuPrompt.setIcon(QIcon(self.parent.checked_icon))
		config.save_settings(config.CONFIG_FILE)

	def __init__(self,filename=None,parent=None):
		super(Window, self).__init__(parent)

		self.filename = filename
		self.parent = parent
		self.changed = False
		self.cscript_menu = None
		self.window_type = EDITOR_WINDOW

		self.editing_user_script = False
		self.current_user_script = None

		self.name = "Untitled script"

		# Load in user settings
		user.load_user(user.USER_FILE)

		self.subwindow_id = str(uuid.uuid4())

		self.editor = QPlainTextEdit(self)

		self.highlight = syntax.MerkScriptHighlighter(self.editor.document())

		self.wordwrap = True
		self.editor.setLineWrapMode(QPlainTextEdit.WidgetWidth)

		self.editor.setStyleSheet(self.generateStylesheet('QPlainTextEdit',config.SYNTAX_FOREGROUND,config.SYNTAX_BACKGROUND))

		self.setWindowIcon(QIcon(SCRIPT_ICON))

		self.editor.textChanged.connect(self.docModified)
		self.editor.redoAvailable.connect(self.hasRedo)
		self.editor.undoAvailable.connect(self.hasUndo)
		self.editor.copyAvailable.connect(self.hasCopy)

		self.status = self.statusBar()
		self.status.setStyleSheet("QStatusBar::item { border: none; }")

		self.status_file = QLabel("<small><b>Untitled script</b></small>")
		self.status.addPermanentWidget(self.status_file,0)

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

		entry = QAction(QIcon(NEWFILE_ICON),"New script",self)
		entry.triggered.connect(self.doNewFile)
		entry.setShortcut("Ctrl+N")
		self.fileMenu.addAction(entry)

		entry = QAction(QIcon(OPENFILE_ICON),"Open script",self)
		entry.triggered.connect(self.doFileOpen)
		entry.setShortcut("Ctrl+O")
		self.fileMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"New connection script",self)
		entry.triggered.connect(self.doNewScript)
		self.fileMenu.addAction(entry)

		if len(user.COMMANDS)>0:

			self.cscript_menu = self.fileMenu.addMenu(QIcon(OPENFILE_ICON),"Open connection script")

			for host in user.COMMANDS:
				entry = QAction(QIcon(SCRIPT_ICON),f"{host}",self)
				entry.triggered.connect(lambda state,x=host,f=user.COMMANDS[host]: self.readConnect(x,f))
				self.cscript_menu.addAction(entry)

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

		menuPromptText = "Prompt to save on close"
		if config.EDITOR_PROMPT_SAVE:
			self.menuPrompt = QAction(QIcon(self.parent.checked_icon),menuPromptText,self)
		else:
			self.menuPrompt = QAction(QIcon(self.parent.unchecked_icon),menuPromptText,self)
		self.menuPrompt.triggered.connect(self.togglePrompt)
		self.fileMenu.addAction(self.menuPrompt)
		
		self.fileMenu.addSeparator()

		entry = QAction(QIcon(CLOSE_ICON),"Close",self)
		entry.triggered.connect(self.close)
		self.fileMenu.addAction(entry)

		self.editMenu = self.menubar.addMenu("Edit")

		self.buildEditMenu()

		self.commandMenu = self.menubar.addMenu("Insert")

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

		entry = QAction(QIcon(CONNECT_ICON),"Connect to server",self)
		entry.triggered.connect(self.insertConnect)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Pause",self)
		entry.triggered.connect(self.insertPause)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(EDIT_ICON),"Print to window",self)
		entry.triggered.connect(self.insertWrite)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(WINDOW_ICON),"Maximize window",self)
		entry.triggered.connect(self.insertMax)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(WINDOW_ICON),"Minimize window",self)
		entry.triggered.connect(self.insertMin)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(WINDOW_ICON),"Set focus on window",self)
		entry.triggered.connect(self.insertFocus)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Execute script",self)
		entry.triggered.connect(self.insertScript)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(SCRIPT_ICON),"Alias",self)
		entry.triggered.connect(self.insertAlias)
		self.commandMenu.addAction(entry)

		entry = QAction(QIcon(NOTIFICATION_ICON),"Play a sound",self)
		entry.triggered.connect(self.insertPlay)
		self.commandMenu.addAction(entry)

		self.runMenu = self.menubar.addMenu("Run")

		self.buildRunMenu()

		self.setCentralWidget(self.editor)

		self.editor.setFocus()

	def executeScript(self,window):
		script = self.editor.toPlainText()
		window.executeScript(script)
		self.runMenu.close()

	def executeScriptOnAll(self):
		servers = self.parent.getAllServerWindows()
		if len(servers)>0:
			for window in servers:
				c = window.widget()
				self.executeScript(c)

	def buildRunMenu(self):
		self.runMenu.clear()

		servers = self.parent.getAllServerWindows()
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
				if c.client.kwargs["ssl"]:
					sec = "Yes"
				else:
					sec = "No"
				runmenuLabel = MenuLabel( menuHtml(RUN_MENU_ICON,"Run on "+cname+"&nbsp;","<b>Host:</b> "+c.name+"<br><b>Network:</b> "+network+"<br><b>Nickname:</b> "+c.client.nickname+"<br><b>Encrypted:</b> "+sec,CUSTOM_MENU_ICON_SIZE) )
				runmenuAction = QWidgetAction(self)
				runmenuAction.setDefaultWidget(runmenuLabel)
				runmenuLabel.clicked.connect(lambda u=c: self.executeScript(u))
				self.runMenu.addAction(runmenuAction)

			if len(servers)>1:
				self.runMenu.addSeparator()

				entry = QAction(QIcon(RUN_ICON),"Run script on all servers",self)
				entry.triggered.connect(self.executeScriptOnAll)
				self.runMenu.addAction(entry)
			return

		# If there's no connected servers...
		entry = QAction(QIcon(DISCONNECT_ICON),"No connected servers",self)
		entry.setEnabled(False)
		self.runMenu.addAction(entry)

	def doNewScript(self):

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
		self.menuSave.setShortcut(QKeySequence())
		self.menuSaveAs.setShortcut("Ctrl+S")
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

		if len(port)==0: port = "6667"

		if len(password)==0:
			cmd = host+" "+port+"\n"
		else:
			cmd = host+" "+port+" "+password+"\n"

		if ssl==True:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"connectssl "+cmd)
			self.updateApplicationTitle()
		else:
			self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"connect "+cmd)
			self.updateApplicationTitle()

	def insertQuit(self):
		x = SetQuit(config.DEFAULT_QUIT_MESSAGE,self)
		e = x.get_message_information(config.DEFAULT_QUIT_MESSAGE,self)

		if not e: return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"quit "+str(e)+"\n")
		self.updateApplicationTitle()

	def insertFocus(self):
		e = SetWindowDialog("Set focus on",self)

		if not e: return

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"focus "+str(e)+"\n")
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
		x = SetAlias(self)
		e = x.get_alias_information(self)

		if not e: return

		aname = e[0]
		avalue = e[1]

		if len(aname)==0: return
		if len(avalue)==0: avalue = 'X'

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"alias "+aname+" "+avalue+"\n")
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

		self.editor.insertPlainText(config.ISSUE_COMMAND_SYMBOL+"script "+str(e)+"\n")
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
				self.setWindowTitle("Connection script for "+self.current_user_script+"*")
				self.status_file.setText(f"<small><b>Connection script for {self.current_user_script} - Changed</b></small>")
			else:
				self.setWindowTitle("Connection script for "+self.current_user_script)
				self.status_file.setText(f"<small><b>Connection script for {self.current_user_script}</b></small>")
			self.name = f"{self.current_user_script}"
			self.parent.buildWindowsMenu()
			
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

