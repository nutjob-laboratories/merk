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

from ..resources import *

class Dialog(QMainWindow):

	def clickCase(self):
		if self.findCase:
			self.findCase = False
		else:
			self.findCase = True

	def clickWord(self):
		if self.wholeWord:
			self.wholeWord = False
		else:
			self.wholeWord = True

	def doSearch(self):

		sterm = self.find.text()
		if len(sterm.strip())==0: return

		if self.findCase:
			if self.wholeWord:
				options = QTextDocument.FindWholeWords | QTextDocument.FindCaseSensitively
			else:
				options = QTextDocument.FindCaseSensitively
		else:
			options = None

		
		if options:
			if not self.parent.editor.find(sterm,options):
				pass
		else:
			if not self.parent.editor.find(sterm):
				pass

		f = self.parent.editor.toPlainText()
		if self.findCase:
			c = f.count(sterm)
		else:
			c = f.lower().count(sterm.lower())
		if c>=1:
			self.icount.setText("<small>"+str(c)+" matches</small>")
		else:
			self.icount.setText("<small>No matches found</small>")

	def doSearchBack(self):

		sterm = self.find.text()
		if len(sterm.strip())==0: return
		
		if self.findCase:
			if self.wholeWord:
				options = QTextDocument.FindWholeWords | QTextDocument.FindCaseSensitively | QTextDocument.FindBackward
			else:
				options = QTextDocument.FindCaseSensitively | QTextDocument.FindBackward
		else:
			options = QTextDocument.FindBackward

		if not self.parent.editor.find(sterm,options):
			pass

		f = self.parent.editor.toPlainText()
		if self.findCase:
			c = f.count(sterm)
		else:
			c = f.lower().count(sterm.lower())
		if c>=1:
			self.icount.setText("<small>"+str(c)+" matches</small>")
		else:
			self.icount.setText("<small>No matches found</small>")

	def doClose(self):
		pass

	def closeEvent(self, event):
		if self.parent.findWindow != None:
			del self.parent.findWindow
			self.parent.findWindow = None
		self.close()

	def setSubwindow(self,obj):
		self.subWindow = obj

	def doReplace(self):
		cursor = self.parent.editor.textCursor()
		cursor.select(QTextCursor.BlockUnderCursor)
		self.parent.editor.setTextCursor(cursor)
		if self.parent.editor.textCursor().hasSelection():
			text = self.parent.editor.textCursor().selectedText()
			cursor.beginEditBlock()
			reptext = text.replace(self.find.text(),self.replace.text())
			cursor.insertText(reptext)
			cursor.endEditBlock()
			self.doSearch()

	def doReplaceAll(self):
		old_text = self.find.text()
		new_text = self.replace.text()

		if not old_text:
			return

		text_cursor = self.parent.editor.textCursor()

		options = QTextDocument.FindFlags()
		if self.findCase:
			if self.wholeWord:
				options |= QTextDocument.FindWholeWords
				options |= QTextDocument.FindCaseSensitively
			else:
				options |= QTextDocument.FindCaseSensitively

		doc = self.parent.editor.document()
		cursor = QTextCursor(doc)

		while True:
			cursor = doc.find(old_text, cursor, options)
			if cursor.isNull(): break
			
			cursor.insertText(new_text)
	
		cursor.endEditBlock()
		
		self.parent.editor.setTextCursor(text_cursor)

	def __init__(self,parent=None,replace=False):
		super(Dialog,self).__init__(parent)

		self.parent = parent

		if replace:
			self.setWindowTitle("Find and replace")
			self.setWindowIcon(QIcon(EDIT_ICON))
		else:
			self.setWindowTitle("Find")
			self.setWindowIcon(QIcon(WHOIS_ICON))

		self.subWindow = None

		self.findCase = False
		self.wholeWord = False

		self.find = QLineEdit()

		if replace:
			self.replace = QLineEdit()

		self.icount = QLabel("<small>Ready</small>")
		self.icount.setAlignment(Qt.AlignCenter)

		findRepLayout = QFormLayout()
		findRepLayout.addRow(QLabel("<b>Find</b>"), self.find)
		if replace:
			self.repLabel = QLabel("<b>Replace</b>")
			findRepLayout.addRow(self.repLabel, self.replace)

		inputLayout = QVBoxLayout()
		inputLayout.addLayout(findRepLayout)
		inputLayout.addWidget(self.icount)

		inputBox = QGroupBox()
		inputBox.setAlignment(Qt.AlignHCenter)
		inputBox.setLayout(inputLayout)

		self.caseSensitive = QCheckBox("Case sensitive",self)
		self.caseSensitive.stateChanged.connect(self.clickCase)

		self.wordWhole = QCheckBox("Whole words",self)
		self.wordWhole.stateChanged.connect(self.clickWord)

		settingsLayout = QHBoxLayout()
		settingsLayout.addStretch()
		settingsLayout.addWidget(self.caseSensitive)
		settingsLayout.addStretch()
		settingsLayout.addWidget(self.wordWhole)
		settingsLayout.addStretch()

		doFind = QPushButton()
		doFind.clicked.connect(self.doSearch)
		doFind.setIcon(QIcon(NEXT_ICON))
		doFind.setToolTip("Next result")

		doBack = QPushButton()
		doBack.clicked.connect(self.doSearchBack)
		doBack.setIcon(QIcon(PREVIOUS_ICON))
		doBack.setToolTip("Previous result")

		if replace:
			doReplace = QPushButton("Replace")
			doReplace.clicked.connect(self.doReplace)

			doReplaceAll = QPushButton("Replace All")
			doReplaceAll.clicked.connect(self.doReplaceAll)

		doClose = QPushButton("Close")
		doClose.clicked.connect(self.close)

		buttonsLayout = QHBoxLayout()
		buttonsLayout.addWidget(doBack)
		if replace:
			buttonsLayout.addWidget(doReplace)
			buttonsLayout.addWidget(doReplaceAll)
		buttonsLayout.addWidget(doFind)
		
		finalLayout = QVBoxLayout()
		finalLayout.addWidget(inputBox)
		finalLayout.addLayout(settingsLayout)
		finalLayout.addLayout(buttonsLayout)
		# if replace:
		# 	finalLayout.addWidget(doReplaceAll)
		finalLayout.addWidget(doClose)

		x = QWidget()
		x.setLayout(finalLayout)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		#self.setLayout(finalLayout)
		self.setCentralWidget(x)

		self.setFixedSize(finalLayout.sizeHint())

