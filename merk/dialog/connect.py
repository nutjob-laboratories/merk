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

class Dialog(QDialog):

	@staticmethod
	def get_connect_information(parent=None):
		dialog = Dialog(parent)
		r = dialog.exec_()
		if r:
			return dialog.return_info()
		return None

	def return_info(self):

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

	def __init__(self,app,parent=None):
		super(Dialog,self).__init__(parent)

		self.app = app

		self.StoredData = []
		self.StoredServer = 0

		self.CONNECT_VIA_SSL = False
		self.RECONNECT_OPTION = True

		self.setWindowTitle(APPLICATION_NAME+" "+APPLICATION_VERSION)
		self.setWindowIcon(QIcon(CONNECT_ICON))

		self.nick = QLineEdit('')
		self.alternative = QLineEdit('')
		self.username = QLineEdit('')
		self.realname = QLineEdit('')

		nickl = QLabel("Nickname")
		altl = QLabel("Alternate")
		usrl = QLabel("Username")
		reall = QLabel("Real name")

		userLayout = QFormLayout()
		userLayout.addRow(nickl, self.nick)
		userLayout.addRow(altl, self.alternative)
		userLayout.addRow(usrl, self.username)
		userLayout.addRow(reall, self.realname)

		userInfoBox = QGroupBox("User Information",self)
		userInfoBox.setLayout(userLayout)
		userInfoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		self.servers = QComboBox(self)
		self.servers.activated.connect(self.setServer)

		self.buildServerSelector()

		self.host = QLineEdit('')
		self.port = QLineEdit('6667')
		self.password = QLineEdit('')
		self.password.setEchoMode(QLineEdit.Password)

		serverLayout = QFormLayout()

		hostl = QLabel("Host")
		serverLayout.addRow(hostl, self.host)

		portl = QLabel("Port")
		serverLayout.addRow(portl, self.port)

		passl = QLabel("Password")
		serverLayout.addRow(passl, self.password)

		self.ssl = QCheckBox("Connect via SSL/TLS",self)
		self.ssl.stateChanged.connect(self.clickSSL)

		self.reconnect = QCheckBox("Reconnect",self)
		self.reconnect.stateChanged.connect(self.clickReconnect)

		sfBox = QVBoxLayout()
		sfBox.addWidget(self.servers)
		sfBox.addLayout(serverLayout)
		sfBox.addWidget(self.ssl)
		sfBox.addWidget(self.reconnect)

		serverInfoBox = QGroupBox("IRC Server",self)
		serverInfoBox.setLayout(sfBox)
		serverInfoBox.setStyleSheet("QGroupBox { font: bold; } QGroupBox::title { subcontrol-position: top center; }")

		buttons = QDialogButtonBox(self)
		buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)

		buttons.button(QDialogButtonBox.Ok).setText("Connect")

		finalLayout = QVBoxLayout()
		finalLayout.addWidget(userInfoBox)
		finalLayout.addWidget(serverInfoBox)
		finalLayout.addWidget(buttons)

		self.setWindowFlags(self.windowFlags()
					^ QtCore.Qt.WindowContextHelpButtonHint)

		self.setLayout(finalLayout)


	def buildServerSelector(self):
		self.StoredData = []
		self.StoredServer = 0

		self.servers.clear()

		self.StoredData.append( ['',"6667",'','normal','' ]    )
		self.servers.addItem("Select a server")

		# Load in stuff from disk
		self.built_in_server_list = get_network_list()

		organized_list = []

		counter = -1
		for entry in self.built_in_server_list:
			counter = counter + 1
			if len(entry) < 4: continue

			if "ssl" in entry[3]:
				if not SSL_AVAILABLE: continue

			organized_list.append(entry)
		
		for s in organized_list:
			if s[3].lower()=='ssl':
				self.servers.addItem(QIcon(NEXT_ICON),s[2]+" - "+s[0])
			else:
				self.servers.addItem(QIcon(PREVIOUS_ICON),s[2]+" - "+s[0])

			self.StoredData.append(s)

		self.StoredServer = self.servers.currentIndex()

def get_network_list():
	servlist = []
	with open(NETWORK_FILE) as fp:
		line = fp.readline()
		line=line.strip()
		while line:
			line=line.strip()
			p = line.split(':')
			servlist.append(p)
			line = fp.readline()
	return servlist