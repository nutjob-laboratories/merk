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

class Dialog(QDialog):

	@staticmethod
	def get_connect_information(app,parent=None,dismsg='',reason='',logo=True,nocommands=False,darkmode=False):
		dialog = Dialog(app,parent,dismsg,reason,logo,nocommands,darkmode)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

	def check_input(self):

		errors = []

		if len(self.nick.text().strip())==0: errors.append("No nickname entered")
		if len(self.username.text().strip())==0: errors.append("No username entered")
		if len(self.realname.text().strip())==0: errors.append("No realname entered")
		if len(self.alternative.text().strip())==0: errors.append("No alternate nickname entered")
		if len(self.host.text().strip())==0: errors.append("No host entered")

		try:
			sp = int(self.port.text())
		except:
			errors.append("Port must be a number")

		if len(errors)>=1:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setWindowIcon(QIcon(APPLICATION_ICON))
			msg.setText("Can't connect to server!")
			msg.setInformativeText("\n".join(errors))
			msg.setWindowTitle("Error")
			msg.exec_()

			return False
		return True

	def return_info(self):

		if self.check_input():

			# Add connection to the user history
			user_history = list(user.HISTORY)

			# Check to make sure that the connection isn't
			# already in the user's history
			inhistory = False
			for s in user_history:
				if s[0]==self.host.text():
					if s[1]==self.port.text():
						inhistory = True

			# If the connection isn't already in the user's
			# history, then add it
			if inhistory==False:
				if self.CONNECT_VIA_SSL:
					ussl = "ssl"
				else:
					ussl = "normal"
				entry = [ self.host.text(),self.port.text(),UNKNOWN_NETWORK,ussl,self.password.text() ]
				user_history.append(entry)

			# Save user settings
			user.NICKNAME = self.nick.text()
			user.ALTERNATE = self.alternative.text()
			user.USERNAME = self.username.text()
			user.REALNAME = self.realname.text()
			user.LAST_HOST = self.host.text()
			user.LAST_PORT = self.port.text()
			user.LAST_PASSWORD = self.password.text()
			user.LAST_SSL = self.CONNECT_VIA_SSL
			user.LAST_RECONNECT = self.RECONNECT_OPTION
			user.HISTORY = user_history

			commands = self.commands.toPlainText()
			hostid = self.host.text()+":"+self.port.text()
			if hostid in user.COMMANDS:
				if len(commands.strip())==0:
					del user.COMMANDS[hostid]
				else:
					user.COMMANDS[hostid] = self.commands.toPlainText()
			else:
				if len(commands.strip())>0:
					user.COMMANDS[hostid] = self.commands.toPlainText()

			user.save_user(user.USER_FILE)

			retval = ConnectInfo(
				self.nick.text(),
				self.alternative.text(),
				self.username.text(),
				self.realname.text(),
				self.host.text(),
				int(self.port.text()),
				self.password.text(),
				self.RECONNECT_OPTION,
				self.CONNECT_VIA_SSL,
			)

			return retval

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

	def clickSSL(self,state):
		if state == Qt.Checked:
			self.CONNECT_VIA_SSL = True
		else:
			self.CONNECT_VIA_SSL = False

	def clickReconnect(self,state):
		if state == Qt.Checked:
			self.RECONNECT_OPTION = True
		else:
			self.RECONNECT_OPTION = False

	def serverEntered(self):
		host = self.host.text()
		port = self.port.text()

		if len(host.strip())==0:
			hostid = "Unknown"
		else:
			hostid = host+":"+port
		self.commandHost.setText(f"<center><big><b>{hostid}</b></big></center>")

		if hostid in user.COMMANDS:
			self.commands.setPlainText(user.COMMANDS[hostid])
		else:
			self.commands.clear()

	def __init__(self,app,parent=None,dismsg='',reason='',logo=True,nocommands=False,darkmode=False):
		super(Dialog,self).__init__(parent)

		self.app = app
		self.parent = parent
		self.disconnect_message = dismsg
		self.reason = reason
		self.logo = logo
		self.no_commands = nocommands
		self.darkmode = darkmode

		self.StoredData = []
		self.StoredServer = 0

		# Load in user settings
		user.load_user(user.USER_FILE)

		self.CONNECT_VIA_SSL = False
		self.RECONNECT_OPTION = False

		if self.logo:
			self.setWindowTitle(APPLICATION_NAME+" IRC Client "+APPLICATION_VERSION)
			self.setWindowIcon(QIcon(APPLICATION_ICON))
		else:
			if self.disconnect_message=='':
				self.setWindowTitle("Connect to IRC")
			else:
				self.setWindowTitle("Connection failed")
			self.setWindowIcon(QIcon(CONNECT_ICON))

		if user.USERNAME=='':
			username = "MERK"
		else:
			username = user.USERNAME

		if user.REALNAME=='':
			realname = APPLICATION_NAME+" "+APPLICATION_VERSION
		else:
			realname = user.REALNAME

		self.nick = QNoSpaceLineEdit(user.NICKNAME)
		self.alternative = QNoSpaceLineEdit(user.ALTERNATE)
		self.username = QNoSpaceLineEdit(username)
		self.realname = QLineEdit(realname)

		nickl = QLabel("<b>Nickname:</b>")
		altl = QLabel("<b>Alternate:</b>")
		usrl = QLabel("<b>Username:</b>")
		reall = QLabel("<b>Real name:</b>")

		userLayout = QFormLayout()
		userLayout.addRow(nickl, self.nick)
		userLayout.addRow(altl, self.alternative)
		userLayout.addRow(usrl, self.username)
		userLayout.addRow(reall, self.realname)

		self.servers = QComboBox(self)
		self.servers.activated.connect(self.setServer)

		self.buildServerSelector()

		self.host = QNoSpaceLineEdit(user.LAST_HOST)
		self.port = QNoSpaceLineEdit(user.LAST_PORT)
		self.password = QLineEdit(user.LAST_PASSWORD)
		self.password.setEchoMode(QLineEdit.Password)

		self.host.textChanged.connect(self.serverEntered)
		self.port.textChanged.connect(self.serverEntered)

		serverLayout = QFormLayout()

		hostl = QLabel("<b>Host:</b>")
		serverLayout.addRow(hostl, self.host)

		portl = QLabel("<b>Port:</b>")
		serverLayout.addRow(portl, self.port)

		passl = QLabel("<b>Password:</b>")
		serverLayout.addRow(passl, self.password)

		self.ssl = QCheckBox("Connect via SSL/TLS",self)
		self.ssl.stateChanged.connect(self.clickSSL)

		if user.LAST_SSL: self.ssl.toggle()

		self.reconnect = QCheckBox("Reconnect",self)
		self.reconnect.stateChanged.connect(self.clickReconnect)

		if user.LAST_RECONNECT: self.reconnect.toggle()

		self.serverDescription = QLabel("""
			<small>
			Select a server below, or enter connection information by hand. To automatically
			reconnect on disconnection, check the <b>Reconnect</b> checkbox.
			</small>

			""")
		self.serverDescription.setWordWrap(True)
		self.serverDescription.setAlignment(Qt.AlignJustify)

		serverInfoLayout = QVBoxLayout()
		serverInfoLayout.addWidget(self.serverDescription)
		serverInfoLayout.addWidget(self.servers)
		serverInfoLayout.addLayout(serverLayout)
		serverInfoLayout.addWidget(self.ssl)
		serverInfoLayout.addWidget(self.reconnect)

		self.commandHost = QLabel("<center><big><b>Unknown</b></big></center>")
		self.commandDescription = QLabel(f"""
			<small>
			Execute these commands upon connection to the server. To insert a pause in between commands,
			use the <b>{config.ISSUE_COMMAND_SYMBOL}wait</b> command, passing the number
			of seconds to pause as an argument.
			</small>

			""")
		self.commandDescription.setWordWrap(True)
		self.commandDescription.setAlignment(Qt.AlignJustify)
		self.commands = QPlainTextEdit()

		# Add syntax highlighting
		self.highlight = syntax.MerkScriptHighlighter(self.commands.document())

		# Set background/foreground
		p = self.commands.palette()
		p.setColor(QPalette.Base, QColor(config.SYNTAX_BACKGROUND))
		p.setColor(QPalette.Text, QColor(config.SYNTAX_FOREGROUND))
		self.commands.setPalette(p)

		height = self.servers.height()+self.ssl.height()+self.reconnect.height()
		height = height + serverLayout.sizeHint().height() + 25
		self.commands.setFixedHeight(height)

		commandsLayout = QVBoxLayout()
		commandsLayout.addWidget(self.commandHost)
		commandsLayout.addWidget(self.commandDescription)
		commandsLayout.addWidget(self.commands)

		self.tabs = QTabWidget()

		self.userDescription = QLabel(f"""
			<small>
			Enter your user information here. <b>Nickname</b> is the nickname you'd like to be known by, and
			<b>alternate</b> is the nickname to use if your primary choice is taken. When
			you're done, click the <b>Server</b> tab to select or enter a server.
			</small>

			""")
		self.userDescription.setWordWrap(True)
		self.userDescription.setAlignment(Qt.AlignJustify)

		userPageLayout = QVBoxLayout()
		userPageLayout.addWidget(self.userDescription)
		userPageLayout.addLayout(userLayout)
		userPageLayout.addStretch()
		

		self.user_tab = QWidget()
		self.user_tab.setLayout(userPageLayout)
		self.tabs.addTab(self.user_tab, QIcon(PRIVATE_ICON), "User")

		self.server_tab = QWidget()
		self.server_tab.setLayout(serverInfoLayout)
		self.tabs.addTab(self.server_tab, QIcon(NETWORK_ICON), "Server")

		self.commands_tab = QWidget()
		self.commands_tab.setLayout(commandsLayout)
		self.tabs.addTab(self.commands_tab, QIcon(SCRIPT_ICON), "Script")

		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Connect")

		if self.no_commands:
			self.tabs.removeTab(2)

		if self.disconnect_message!='':

			discoMessage = QLabel(f"""
				<center>
					<b><div style="color: red;" alt="{self.reason}">{self.disconnect_message}</div></b><br>
					<small><b>Please select another server below.</b></small>
				</center>
				""")

			bannerTabs = QVBoxLayout()
			bannerTabs.addWidget(discoMessage)
			bannerTabs.addWidget(self.tabs)
		else:
			bannerTabs = QVBoxLayout()
			bannerTabs.addWidget(self.tabs)

		finalLayout = QVBoxLayout()
		finalLayout.addLayout(bannerTabs)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)

		self.setFixedSize(finalLayout.sizeHint())

		if user.NICKNAME=='' or user.ALTERNATE=='' or user.USERNAME=='' or user.REALNAME=='':
			self.tabs.setCurrentWidget(self.user_tab)
		else:
			self.tabs.setCurrentWidget(self.server_tab)

		self.serverEntered()


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