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

SSL_AVAILABLE = True
try:
	from twisted.internet import ssl
except ImportError as error:
	SSL_AVAILABLE = False
except Exception as exception:
	pass

from ..resources import *
from .. import config
from .. import user
from .. import syntax
from .. import connection_script
from .get_sasl import Dialog as GetSasl

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

def GetSaslDialog(obj,username=None,password=None):
	x = GetSasl(obj,username,password)
	info = x.get_sasl_information(obj,username,password)
	del x

	if not info: return None
	return info

class Dialog(QDialog):

	def doSkip(self):
		self.skipping = True
		self.accept()

	@staticmethod
	def get_connect_information(app,parent=None,dismsg='',reason='',logo=True,noexecute=False,donotsave=False,initial=False):
		dialog = Dialog(app,parent,dismsg,reason,logo,noexecute,donotsave,initial)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return ConnectInfo(CONNECTION_DIALOG_CANCELED,None,None,None,None,None,None,None,None,None)

	def check_input(self):

		errors = []

		missing_info = False
		missing_host = False
		if len(self.nick.text().strip())==0:
			errors.append("No nickname entered")
			missing_info = True
		if len(self.username.text().strip())==0:
			errors.append("No username entered")
			missing_info = True
		if len(self.realname.text().strip())==0:
			errors.append("No realname entered")
			missing_info = True
		if len(self.host.text().strip())==0:
			errors.append("No host entered")
			missing_info = True
			missing_host = True

		bad_info = False
		try:
			sp = int(self.port.text())
		except:
			errors.append("Port must be a number")
			bad_info = True

		if len(errors)>=1:

			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setWindowIcon(QIcon(APPLICATION_ICON))
			if bad_info and missing_info:
				msg.setText("<big><b>Bad/Missing connection information</b></big>")
				msg.setInformativeText("<b>Can't connect to server!</b><br><br>Please enter all information needed and try again.")
			elif bad_info:
				msg.setText("<big><b>Bad connection information</b></big>")
				msg.setInformativeText("<b>Server port must be a number!</b><br><br>Please enter all information needed and try again.")
			elif missing_info:
				msg.setText("<big><b>Missing connection information</b></big>")
				if missing_host:
					msg.setInformativeText("<b>Missing server host!</b><br><br>Please enter all information needed and try again.")
				else:
					msg.setInformativeText("<b>User information needed!</b><br><br>Please enter all information needed and try again.")
			msg.setDetailedText("\n".join(errors))
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)

			msg.exec_()

			return False
		return True

	def return_info(self):

		if self.skipping:
			retval = ConnectInfo(None,None,None,None,None,None,None,None,None,None)
			return retval

		if self.check_input():

			user_history = list(user.HISTORY)
			hostid = self.host.text()+":"+self.port.text()

			sasl_username = None
			sasl_password = None
			if self.use_SASL:
				if self.SASL_Username!=None and self.SASL_Password!=None:
					sasl_username = self.SASL_Username
					sasl_password = self.SASL_Password

			if self.SAVE:

				if self.use_profile:
					e = [self.nick.text(),self.alternative.text(),self.username.text(),self.realname.text()]
					user.PROFILES[hostid] = e
				else:
					user.NICKNAME = self.nick.text()
					user.USERNAME = self.username.text()
					user.REALNAME = self.realname.text()
					user.ALTERNATE = self.alternative.text()

				# Save user settings
				user.LAST_HOST = self.host.text()
				user.LAST_PORT = self.port.text()
				user.LAST_PASSWORD = self.password.text()
				user.LAST_SSL = self.CONNECT_VIA_SSL
				user.LAST_RECONNECT = self.RECONNECT_OPTION
				user.HISTORY = user_history

				commands = self.commands.toPlainText()
				if hostid in user.COMMANDS:
					if len(commands.strip())==0:
						del user.COMMANDS[hostid]
					else:
						user.COMMANDS[hostid] = self.commands.toPlainText()
				else:
					if len(commands.strip())>0:
						user.COMMANDS[hostid] = self.commands.toPlainText()

				if sasl_username!=None and sasl_password!=None:
					sentry = [sasl_username,sasl_password]
					user.SASL[hostid] = sentry

				user.save_user(user.USER_FILE)

				if len(self.password.text().strip())==0:
					server_pass = None
				else:
					server_pass = self.password.text()

				retval = ConnectInfo(
					self.nick.text(),
					self.alternative.text(),
					self.username.text(),
					self.realname.text(),
					self.host.text(),
					int(self.port.text()),
					server_pass,
					self.RECONNECT_OPTION,
					self.CONNECT_VIA_SSL,
					self.EXECUTE,	# execute script
					sasl_username,
					sasl_password,
				)

				if self.parent!=None:
					self.parent.donotsave = False

				return retval
			else:

				connection_script.add_connection_script(hostid,self.commands.toPlainText())

				if len(self.password.text().strip())==0:
					server_pass = None
				else:
					server_pass = self.password.text()

				retval = ConnectInfo(
					self.nick.text(),
					self.alternative.text(),
					self.username.text(),
					self.realname.text(),
					self.host.text(),
					int(self.port.text()),
					server_pass,
					self.RECONNECT_OPTION,
					self.CONNECT_VIA_SSL,
					self.EXECUTE,	# execute script
					sasl_username,
					sasl_password,
				)

				if self.parent!=None:
					self.parent.donotsave = True

				return retval

		return ConnectInfo(CONNECTION_MISSING_INFO_ERROR,None,None,None,None,None,None,None,None,None)

	def setServer(self):

		self.StoredServer = self.servers.currentIndex()

		# Fill in the server info
		h = self.StoredData[self.StoredServer]
		if "ssl" in h[3]:
			use_ssl = True
		else:
			use_ssl = False
		host = h[0]
		port = int(h[1])

		self.host.setText(host)
		self.port.setText(h[1])

		if len(h)==5:
			if h[4]=='':
				password = None
				self.password.setText('')
			else:
				password = h[4]
				self.password.setText(h[4])
		else:
			password = None
			self.password.setText('')

		if use_ssl:
			self.ssl.setCheckState(Qt.Checked)
		else:
			self.ssl.setCheckState(Qt.Unchecked)

		self.SASL_Username = None
		self.SASL_Password = None
		self.use_SASL = False
		self.sasl.setCheckState(Qt.Unchecked)

		hostid = f"{host}:{h[1]}"
		if hostid in user.SASL:
			u = user.SASL[hostid]
			self.SASL_Username = u[0]
			self.SASL_Password = u[1]
			self.use_SASL = True
			self.sasl.setCheckState(Qt.Checked)
			self.clear.setEnabled(True)
			self.edit.setEnabled(True)
		else:
			self.SASL_Username = None
			self.SASL_Password = None
			self.use_SASL = False
			self.sasl.setCheckState(Qt.Unchecked)
			self.clear.setEnabled(False)
			self.edit.setEnabled(False)

		if hostid in user.PROFILES and config.ALWAYS_USE_SERVER_PROFILES:
			self.profile.setChecked(True)
			n = user.PROFILES[hostid][0]
			a = user.PROFILES[hostid][1]
			u = user.PROFILES[hostid][2]
			r = user.PROFILES[hostid][3]

			self.nick.setText(n)
			self.alternative.setText(a)
			self.username.setText(u)
			self.realname.setText(r)
		else:
			self.profile.setChecked(False)
			self.nick.setText(user.NICKNAME)
			self.alternative.setText(user.ALTERNATE)
			self.username.setText(user.USERNAME)
			self.realname.setText(user.REALNAME)

		if hostid in user.PROFILES:
			self.profile.setText(f"Use {hostid} profile")
		else:
			self.profile.setText(f"Save as server profile")

		if user.NICKNAME=='' or user.USERNAME=='' or user.REALNAME=='':
			self.tabs.setCurrentWidget(self.user_tab)
			self.nick.setFocus()
			QTimer.singleShot(0, lambda: self.nick.setCursorPosition(len(self.nick.text())))
		else:
			QTimer.singleShot(0, lambda: self.moveCursor())

	def moveCursor(self):
		self.host.setFocus()
		self.host.setCursorPosition(len(self.host.text()))

	def clickProfile(self):
		if self.profile.isChecked():
			self.use_profile = True

			host = self.host.text()
			port = self.port.text()
			hostid = host+":"+port

			if hostid in user.PROFILES:
				n = user.PROFILES[hostid][0]
				a = user.PROFILES[hostid][1]
				u = user.PROFILES[hostid][2]
				r = user.PROFILES[hostid][3]

				self.nick.setText(n)
				self.alternative.setText(a)
				self.username.setText(u)
				self.realname.setText(r)
		else:
			self.use_profile = False

			self.nick.setText(user.NICKNAME)
			self.alternative.setText(user.ALTERNATE)
			self.username.setText(user.USERNAME)
			self.realname.setText(user.REALNAME)

	def clickSASL(self,state):
		if state==Qt.Checked:
			self.use_SASL = True
			if self.SASL_Username==None and self.SASL_Password==None:
				u = GetSaslDialog(self)
				if u:
					if len(u[0])>0 and len(u[1])>0:
						self.SASL_Username = u[0]
						self.SASL_Password = u[1]
						self.clear.setEnabled(True)
						self.edit.setEnabled(True)
					else:
						self.SASL_Username = None
						self.SASL_Password = None
						self.use_SASL = False
						self.sasl.setCheckState(Qt.Unchecked)
						self.clear.setEnabled(False)
						self.edit.setEnabled(False)
				else:
					self.SASL_Username = None
					self.SASL_Password = None
					self.use_SASL = False
					self.sasl.setCheckState(Qt.Unchecked)
					self.clear.setEnabled(False)
					self.edit.setEnabled(False)
		else:
			self.use_SASL = False

	def clearSASL(self):
		if len(self.host.text())>0 and len(self.port.text())>0:
			self.SASL_Username = None
			self.SASL_Password = None
			self.use_SASL = False
			self.sasl.setCheckState(Qt.Unchecked)
			self.clear.setEnabled(False)
			self.edit.setEnabled(False)

	def editSasl(self):
		if self.SASL_Username!=None and self.SASL_Password!=None:
			u = GetSaslDialog(self,self.SASL_Username,self.SASL_Password)
			if u:
				self.SASL_Username = u[0]
				self.SASL_Password = u[1]

	def clickSSL(self,state):
		if state == Qt.Checked:
			self.CONNECT_VIA_SSL = True
		else:
			self.CONNECT_VIA_SSL = False

	def clickExe(self,state):
		if state == Qt.Checked:
			self.EXECUTE = True
		else:
			self.EXECUTE = False

	def clickSave(self,state):
		if state == Qt.Checked:
			self.SAVE = True
		else:
			self.SAVE = False

	def clickReconnect(self,state):
		if state == Qt.Checked:
			self.RECONNECT_OPTION = True
		else:
			self.RECONNECT_OPTION = False

	def check_info(self):
		host = self.host.text()
		port = self.port.text()
		nick = self.nick.text()
		uname = self.username.text()
		rname = self.realname.text()

		if len(host.strip())==0: return False
		if len(port.strip())==0: return False
		if len(nick.strip())==0: return False
		if len(uname.strip())==0: return False
		if len(rname.strip())==0: return False

		return True

	def userInfoEntered(self):
		host = self.host.text()
		port = self.port.text()
		hostid = host+":"+port

		if self.check_info()==False:
			self.ok_button.setEnabled(False)
			self.sasl.setEnabled(False)
			self.commands_tab.setEnabled(False)
			self.profile.setEnabled(False)
			if len(host.strip())==0 or len(port.strip())==0:
				self.commandHost.setText("<center><small><b>No server selected</b></small></center>")
				self.commands.clear()
		else:
			self.ok_button.setEnabled(True)
			self.sasl.setEnabled(True)
			self.commands_tab.setEnabled(True)
			self.profile.setEnabled(True)
			self.commandHost.setText(self.exeTemplate.replace('%__SERVER__%',hostid))

			if hostid in user.COMMANDS:
				self.commands.setPlainText(user.COMMANDS[hostid])
			else:
				self.commands.clear()

			if hostid in user.SASL:
				u = user.SASL[hostid]
				self.SASL_Username = u[0]
				self.SASL_Password = u[1]
				self.use_SASL = True
				self.sasl.setCheckState(Qt.Checked)
				self.clear.setEnabled(True)
				self.edit.setEnabled(True)
			else:
				self.SASL_Username = None
				self.SASL_Password = None
				self.use_SASL = False
				self.sasl.setCheckState(Qt.Unchecked)
				self.clear.setEnabled(False)
				self.edit.setEnabled(False)

	def infoEntered(self):
		host = self.host.text()
		port = self.port.text()
		hostid = host+":"+port

		if len(self.host.text().strip())>0 and len(self.port.text().strip())>0:
			if self.use_profile:
				if hostid in user.PROFILES:
					n = user.PROFILES[hostid][0]
					a = user.PROFILES[hostid][1]
					u = user.PROFILES[hostid][2]
					r = user.PROFILES[hostid][3]

					self.nick.setText(n)
					self.alternative.setText(a)
					self.username.setText(u)
					self.realname.setText(r)
					self.profile.setChecked(True)

		if self.check_info()==False:
			self.ok_button.setEnabled(False)
			self.sasl.setEnabled(False)
			self.commands_tab.setEnabled(False)
			self.profile.setEnabled(False)
			if len(host.strip())==0 or len(port.strip())==0:
				self.commandHost.setText("<center><small><b>No server selected</b></small></center>")
				self.commands.clear()
		else:
			self.ok_button.setEnabled(True)
			self.sasl.setEnabled(True)
			self.commands_tab.setEnabled(True)
			self.profile.setEnabled(True)
			self.commandHost.setText(self.exeTemplate.replace('%__SERVER__%',hostid))

			if hostid in user.COMMANDS:
				self.commands.setPlainText(user.COMMANDS[hostid])
			else:
				self.commands.clear()

			if hostid in user.SASL:
				u = user.SASL[hostid]
				self.SASL_Username = u[0]
				self.SASL_Password = u[1]
				self.use_SASL = True
				self.sasl.setCheckState(Qt.Checked)
				self.clear.setEnabled(True)
				self.edit.setEnabled(True)
			else:
				self.SASL_Username = None
				self.SASL_Password = None
				self.use_SASL = False
				self.sasl.setCheckState(Qt.Unchecked)
				self.clear.setEnabled(False)
				self.edit.setEnabled(False)

			if hostid in user.PROFILES:
				self.profile.setText(f"Use {hostid} profile")
			else:
				self.profile.setText(f"Save as server profile")

	def generateStylesheet(self,obj,fore,back):

		return obj+"{ background-color:"+back+"; color: "+fore +"; }";

	def __init__(self,app,parent=None,dismsg='',reason='',logo=True,noexecute=False,donotsave=False,initial=False):
		super(Dialog,self).__init__(parent)

		self.app = app
		self.parent = parent
		self.disconnect_message = dismsg
		self.reason = reason
		self.not_simplified = logo
		self.noexecute = noexecute
		self.donotsave = donotsave
		self.initial = initial
		self.skipping = False
		self.use_profile = False

		if test_if_window_background_is_light(self):
			self.dark_mode = False
		else:
			self.dark_mode = True

		self.StoredData = []
		self.StoredServer = 0

		self.SASL_Username = None
		self.SASL_Password = None
		self.use_SASL = False

		# Make a version of the font that is slightly
		# smaller than the current font, but never
		# smaller than 8pt
		smaller_font = self.font()
		smaller_point_size = smaller_font.pointSize() - 2
		if smaller_point_size<8: smaller_point_size = 8
		smaller_font.setPointSize(smaller_point_size)

		# Load the config file
		config.load_settings(config.CONFIG_FILE)

		# Load in user settings
		user.load_user(user.USER_FILE)

		self.CONNECT_VIA_SSL = False
		self.RECONNECT_OPTION = False
		self.EXECUTE = True
		self.SAVE = True

		if not self.not_simplified:
			self.exeTemplate = f"""
				<center><b>%__SERVER__%</b></center>
			"""
		else:
			self.exeTemplate = f"""
				<small>
				Execute these commands upon connection to <b>%__SERVER__%</b>. To insert a pause in between commands,
				use the <b>wait</b> command, passing the number
				of seconds to pause as an argument.
				</small>
			"""

		if self.initial:
			self.setWindowTitle(f"{APPLICATION_NAME} IRC Client {APPLICATION_VERSION}")
			self.setWindowIcon(QIcon(APPLICATION_ICON))
		else:
			if self.disconnect_message=='':
				self.setWindowTitle("Connect to server")
			else:
				self.setWindowTitle("Connection failed")
			self.setWindowIcon(QIcon(CONNECT_MENU_ICON))

		if user.USERNAME=='':
			username = f"{APPLICATION_NAME}"
		else:
			username = user.USERNAME

		if user.REALNAME=='':
			realname = APPLICATION_NAME+" "+APPLICATION_VERSION
		else:
			realname = user.REALNAME

		if config.PREVENT_ILLEGAL_NICKNAMES:
			self.nick = QNickEdit(user.NICKNAME)
			self.alternative = QNickEdit(user.NICKNAME)
		else:
			self.nick = QNoSpaceLineEdit(user.NICKNAME)
			self.alternative = QNoSpaceLineEdit(user.NICKNAME)
		
		self.username = QNoSpaceLineEdit(username)
		self.realname = QRealnameEdit(realname)

		nickl = QLabel("<b>Nickname</b>")
		altl = QLabel("<b>Alternate</b>")
		usrl = QLabel("<b>Username</b>")
		reall = QLabel("<b>Real name</b>")

		self.profile = QCheckBox("Save as server profile",self)
		self.profile.stateChanged.connect(self.clickProfile)
		self.profile.setFont(smaller_font)

		userLayout = QFormLayout()
		userLayout.addRow(nickl, self.nick)
		userLayout.addRow(altl, self.alternative)
		userLayout.addRow(usrl, self.username)
		userLayout.addRow(reall, self.realname)
		userLayout.addRow(self.profile)

		self.servers = QComboBox(self)
		self.servers.activated.connect(self.setServer)

		self.buildServerSelector()

		self.host = QNoSpaceLineEdit(user.LAST_HOST)
		self.port = QNoSpaceLineEdit(user.LAST_PORT)
		self.password = QLineEdit(user.LAST_PASSWORD)
		self.password.setEchoMode(QLineEdit.Password)

		# Make sure that only positive integers
		# can be input into the port entry
		validator = QIntValidator(1, 2147483647)
		self.port.setValidator(validator)

		self.host.textChanged.connect(self.infoEntered)
		self.port.textChanged.connect(self.infoEntered)

		self.nick.textChanged.connect(self.userInfoEntered)
		self.username.textChanged.connect(self.userInfoEntered)
		self.realname.textChanged.connect(self.userInfoEntered)

		serverLayout = QFormLayout()

		hostl = QLabel("<b>Host</b>")
		serverLayout.addRow(hostl, self.host)

		portl = QLabel("<b>Port</b>")
		serverLayout.addRow(portl, self.port)

		passl = QLabel("<b>Password</b>")
		serverLayout.addRow(passl, self.password)

		self.sasl = QCheckBox("Login via SASL",self)
		self.sasl.stateChanged.connect(self.clickSASL)
		self.sasl.setFont(smaller_font)

		self.edit = QPushButton("Edit")
		self.edit.clicked.connect(self.editSasl)
		self.edit.setToolTip("Edit the SASL account for this server")
		self.edit.setFixedHeight(self.sasl.sizeHint().height())
		self.edit.setFont(smaller_font)

		self.clear = QPushButton("Clear")
		self.clear.clicked.connect(self.clearSASL)
		self.clear.setToolTip("Clear SASL account for this server")
		self.clear.setFixedHeight(self.sasl.sizeHint().height())
		self.clear.setFont(smaller_font)

		sasl_row = QWidget()
		sLayout = QHBoxLayout()
		sLayout.setSpacing(0)
		sLayout.setContentsMargins(0, 0, 0, 0)
		sLayout.addWidget(self.sasl)
		sLayout.addStretch()
		sLayout.addWidget(self.edit)
		sLayout.addWidget(self.clear)
		sasl_row.setLayout(sLayout)

		self.ssl = QCheckBox("Connect via SSL/TLS",self)
		self.ssl.stateChanged.connect(self.clickSSL)
		self.ssl.setFont(smaller_font)

		if not SSL_AVAILABLE: self.ssl.hide()

		if config.SCRIPTING_ENGINE_ENABLED:
			self.exe = QCheckBox("Execute connection script",self)
			self.exe.stateChanged.connect(self.clickExe)
			self.exe.toggle()
			self.exe.setFont(smaller_font)

		if self.noexecute: self.exe.toggle()

		if user.LAST_SSL: self.ssl.toggle()

		self.reconnect = QCheckBox("Reconnect",self)
		self.reconnect.stateChanged.connect(self.clickReconnect)
		self.reconnect.setFont(smaller_font)

		if user.LAST_RECONNECT: self.reconnect.toggle()

		self.serverDescription = QLabel("""
			<small>
			Select a server below, or enter connection information by hand. To automatically
			reconnect on disconnection, check the <b>Reconnect</b> checkbox. If the <b>Execute connection
			script</b> option is enabled, the commands entered in the <b>Script</b> tab will be executed
			when connection to the server is complete.
			</small>

			""")
		self.serverDescription.setWordWrap(True)
		self.serverDescription.setAlignment(Qt.AlignJustify)

		optionLayout = QFormLayout()

		if not SSL_AVAILABLE:
			optionLayout.addRow(self.reconnect)
		else:
			optionLayout.addRow(self.ssl,self.reconnect)

		optionLayout.addRow(sasl_row)

		hostid = f"{user.LAST_HOST}:{user.LAST_PORT}"
		if hostid in user.SASL:
			u = user.SASL[hostid]
			self.SASL_Username = u[0]
			self.SASL_Password = u[1]
			self.use_SASL = True
			self.sasl.toggle()

		if self.SASL_Username==None and self.SASL_Password==None:
			self.clear.setEnabled(False)
			self.edit.setEnabled(False)

		if config.SCRIPTING_ENGINE_ENABLED:
			optionLayout.addRow(self.exe,QLabel(''))
		optionLayout.setVerticalSpacing(0)

		serverInfoLayout = QVBoxLayout()
		serverInfoLayout.addStretch()
		if self.not_simplified:
			serverInfoLayout.addWidget(self.serverDescription)
		serverInfoLayout.addWidget(self.servers)
		serverInfoLayout.addLayout(serverLayout)
		serverInfoLayout.addLayout(optionLayout)
		serverInfoLayout.setContentsMargins(3,3,3,3)

		self.commandHost = QLabel(self.exeTemplate.replace('%__SERVER__%','UNKNOWN'))
		self.commandHost.setWordWrap(True)
		self.commandHost.setAlignment(Qt.AlignJustify)

		self.commands = CodeEditor()

		# Add syntax highlighting
		self.highlight = syntax.MerkScriptHighlighter(self.commands.document())

		# Set whether to highlight the current line
		self.commands.setHighlightLine(config.HIGHLIGHT_CURRENT_LINE_IN_EDITOR)

		# Set background/foreground
		self.commands.setStyleSheet(self.generateStylesheet('CodeEditor',config.SYNTAX_FOREGROUND,config.SYNTAX_BACKGROUND))
		self.commands.highlight_current_line(True)

		height = self.servers.height()+self.reconnect.height()
		if self.not_simplified:
			height = height + serverLayout.sizeHint().height() + 165
		else:
			height = height + serverLayout.sizeHint().height() + 120
		self.commands.setFixedHeight(height)

		commandsLayout = QVBoxLayout()
		commandsLayout.addStretch()
		commandsLayout.addWidget(self.commandHost)
		commandsLayout.addWidget(self.commands)
		commandsLayout.setContentsMargins(3,3,3,3)

		self.tabs = QTabWidget()
		self.tabs.tabBar().setExpanding(True)
		self.tabs.tabBar().setDocumentMode(True)

		self.userDescription = QLabel(f"""
			<small>
			<b>Nickname</b> is the nickname you want to use, and
			<b>alternate</b> (optional) is used if your primary choice is taken. If both <b>nickname</b>
			and <b>alternate</b> are taken, a random number will be attached to <b>nickname</b>, and that
			will be used as the nickname. All settings are saved when you click <b>Connect</b>,
			unless you uncheck <b>Save to user settings file</b> below. Click <b>Save as server profile</b>
			if you'd like to use this user information every time you connect to this specific server.
			</small>

			""")
		self.userDescription.setWordWrap(True)
		self.userDescription.setAlignment(Qt.AlignJustify)

		self.saveU = QCheckBox("Save to user settings file",self)
		self.saveU.stateChanged.connect(self.clickSave)
		self.saveU.toggle()

		if self.donotsave: self.saveU.toggle()

		userPageLayout = QVBoxLayout()
		if self.not_simplified:
			userPageLayout.addStretch()
			userPageLayout.addWidget(self.userDescription)
		else:
			userPageLayout.addStretch()
		userPageLayout.addLayout(userLayout)
		userPageLayout.addStretch()
		userPageLayout.setContentsMargins(6,6,6,6)

		self.user_tab = QWidget()
		self.user_tab.setLayout(userPageLayout)
		self.tabs.addTab(self.user_tab, QIcon(PRIVATE_ICON), "User")

		self.server_tab = QWidget()
		self.server_tab.setLayout(serverInfoLayout)
		self.tabs.addTab(self.server_tab, QIcon(NETWORK_ICON), "Server")

		if config.SCRIPTING_ENGINE_ENABLED:
			self.commands_tab = QWidget()
			self.commands_tab.setLayout(commandsLayout)
			self.tabs.addTab(self.commands_tab, QIcon(SCRIPT_ICON), "Script")

		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		self.ok_button = buttons.button(QDialogButtonBox.Ok)
		self.cancel_button = buttons.button(QDialogButtonBox.Cancel)
		buttons.button(QDialogButtonBox.Ok).setText("Connect")

		# Make sure that the "Connect" button is what triggers
		# if the enter button is pressed
		self.ok_button.setDefault(True)
		self.ok_button.setAutoDefault(True)

		if hostid in user.PROFILES and config.ALWAYS_USE_SERVER_PROFILES:
			self.use_profile = True
			n = user.PROFILES[hostid][0]
			a = user.PROFILES[hostid][1]
			u = user.PROFILES[hostid][2]
			r = user.PROFILES[hostid][3]

			self.nick.setText(n)
			self.alternative.setText(a)
			self.username.setText(u)
			self.realname.setText(r)
			self.profile.setChecked(True)

			self.profile.setText(f"Use {hostid} profile")

		elif hostid in user.PROFILES and config.ALWAYS_USE_SERVER_PROFILES==False:

			self.profile.setText(f"Use {hostid} profile")

		if self.initial:
			buttons.button(QDialogButtonBox.Cancel).setText("Exit")
		else:
			buttons.button(QDialogButtonBox.Cancel).setText("Cancel")

		if self.initial:
			self.skip = QPushButton(f" Open {APPLICATION_NAME} ")
			self.skip.setToolTip(f"Open {APPLICATION_NAME} without connecting")
			self.skip.clicked.connect(self.doSkip)

			initialLayout = QHBoxLayout()
			initialLayout.addWidget(self.skip)
			initialLayout.addStretch()
			initialLayout.addWidget(buttons)

		if self.disconnect_message!='':

			discoMessage = QLabel(f"""
				<center>
					<b><div style="color: red;" alt="{self.reason}">{self.disconnect_message}</div></b><br>
					<small><b>Please select another server below.</b></small>
				</center>
				""")

			bannerTabs = QVBoxLayout()
			bannerTabs.setSpacing(0)
			bannerTabs.addWidget(discoMessage)
			bannerTabs.addWidget(self.tabs)
			bannerTabs.addWidget(self.saveU)
		else:
			bannerTabs = QVBoxLayout()
			bannerTabs.setSpacing(0)
			bannerTabs.addWidget(self.tabs)
			bannerTabs.addWidget(self.saveU)

		finalLayout = QVBoxLayout()
		if self.initial:
			if not config.HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG:
				splash = QLabel()
				pixmap = QPixmap(SPLASH_LOGO)
				scaled_pixmap = pixmap.scaled(190, 49, Qt.KeepAspectRatio, Qt.SmoothTransformation)
				splash.setPixmap(scaled_pixmap)

				spLayout = QHBoxLayout()
				spLayout.addStretch()
				spLayout.addWidget(splash)
				spLayout.addStretch()

				vLayout = QVBoxLayout()
				vLayout.addLayout(spLayout)

				finalLayout.addLayout(vLayout)
		finalLayout.addLayout(bannerTabs)
		if self.initial:
			finalLayout.addLayout(initialLayout)
		else:
			finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.adjustSize()

		self.setFixedSize(finalLayout.sizeHint())

		if user.NICKNAME=='' or user.USERNAME=='' or user.REALNAME=='':
			if len(self.nick.text().strip())==0 or len(self.username.text().strip())==0 or len(self.realname.text().strip())==0:
				self.tabs.setCurrentWidget(self.user_tab)
				self.nick.setFocus()
				QTimer.singleShot(0, lambda: self.nick.setCursorPosition(len(self.nick.text())))
			else:
				self.tabs.setCurrentWidget(self.server_tab)
				self.host.setFocus()
				QTimer.singleShot(0, lambda: self.host.setCursorPosition(len(self.host.text())))
		else:
			self.tabs.setCurrentWidget(self.server_tab)
			self.host.setFocus()
			QTimer.singleShot(0, lambda: self.host.setCursorPosition(len(self.host.text())))

		self.infoEntered()


	def buildServerSelector(self):
		self.StoredData = []
		self.StoredServer = 0

		self.servers.clear()

		if user.LAST_SSL:
			dussl = "ssl"
			icon = QIcon(VISITED_SECURE_ICON)
		else:
			dussl = "normal"
			icon = QIcon(VISITED_BOOKMARK_ICON)

		if len(user.LAST_HOST)>0:
			self.StoredData.append( [ user.LAST_HOST,user.LAST_PORT,"Last server",dussl,user.LAST_PASSWORD ]    )
			self.servers.addItem(icon,"Last server connection")
		else:
			self.StoredData.append( ['',"6667",'','normal','' ]    )
			self.servers.addItem("Select or enter a server")

		# Load in stuff from disk
		self.built_in_server_list = get_network_list()

		organized_list = []

		if len(user.HISTORY)>0:
			# servers are in history
			for s in user.HISTORY:

				builtin = False
				for entry in self.built_in_server_list:
					if entry[0]==s[0]:
						if entry[1]==s[1]:
							builtin = True

				if not builtin:
					self.built_in_server_list.insert(0,s)

		counter = -1
		for entry in self.built_in_server_list:
			counter = counter + 1
			if len(entry) < 4: continue

			if "ssl" in entry[3]:
				if not SSL_AVAILABLE: continue

			visited = False
			if len(user.HISTORY)>0:
				for s in user.HISTORY:
					if s[0]==entry[0]:
						if s[1]==entry[1]:
							visited = True

			if visited:
				organized_list.append([True,entry])
			else:
				organized_list.append([False,entry])
		
		vserver = []
		nserver = []
		for x in organized_list:
			if x[0]:
				vserver.append(x)
			else:
				nserver.append(x)
		finallist = vserver + nserver

		for s in finallist:
			if s[0]:
				if s[1][3].lower()=='ssl':
					self.servers.addItem(QIcon(VISITED_SECURE_ICON),s[1][2]+" - "+s[1][0])
				else:
					self.servers.addItem(QIcon(VISITED_BOOKMARK_ICON),s[1][2]+" - "+s[1][0])
			else:
				if s[1][3].lower()=='ssl':
					self.servers.addItem(QIcon(SECURE_ICON),s[1][2]+" - "+s[1][0])
				else:
					self.servers.addItem(QIcon(BOOKMARK_ICON),s[1][2]+" - "+s[1][0])

			self.StoredData.append(s[1])

		self.StoredServer = self.servers.currentIndex()

def get_network_list():
	servlist = []
	for line in NETWORK_LIST.split("\n"):
		line = line.strip()
		p = line.split(":")
		servlist.append(p)
	return servlist