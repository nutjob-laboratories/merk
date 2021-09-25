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

import argparse
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

app = QApplication([])

import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

from merk.main import Merk
from merk.resources import *
from merk.dialog import *
import merk.config as config
import merk.styles as styles
import merk.logs as logs
import merk.user as user
import merk.plugins as plugins

parser = argparse.ArgumentParser(
	prog=f"python {os.path.basename(__file__)}",
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=f'''
███╗   ███╗██████╗ ██████╗ ██╗  ██╗
████╗ ████║╚═══╗██╗██╔══██╗██║ ██╔╝
██╔████╔██║███████║██████╔╝█████╔╝
██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗
██║ ╚═╝ ██║ █████╔╝██║  ██║██║  ██╗
╚═╝     ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
Version {APPLICATION_VERSION}

An open source, cross-platform IRC client
https://github.com/nutjob-laboratories/merk

Available Qt widget styles: {", ".join(QStyleFactory.keys())}
''',
)

congroup = parser.add_argument_group('Connection')

congroup.add_argument("server", type=str,help="Server to connect to", metavar="SERVER", nargs='?')
congroup.add_argument("port", type=int,help="Server port to connect to (6667)", default=6667, nargs='?', metavar="PORT")
congroup.add_argument( "--ssl","--tls", help=f"Use SSL/TLS to connect to IRC", action="store_true")
congroup.add_argument( "--reconnect", help=f"Reconnect to servers on disconnection", action="store_true")
congroup.add_argument("-p","--password", type=str,help="Use server password to connect", metavar="PASSWORD", default='')
congroup.add_argument("-c","--channel", type=str,help="Join channel on connection", metavar="CHANNEL[:KEY]", action='append')

configuration_group = parser.add_argument_group('Configuration')

# Change the below default to None to store files in the home directory
configuration_group.add_argument("-D","--config-directory",dest="configdir",type=str,help="Location to store configuration files", metavar="DIRECTORY", default=None)
configuration_group.add_argument( "-L","--config-local",dest="configinstall",help=f"Store configuration files in install directory", action="store_true")
configuration_group.add_argument("--config-name",dest="configname",type=str,help="Name of the configuration file directory (default: .merk)", metavar="NAME", default=".merk")
configuration_group.add_argument("--qtstyle",dest="qtstyle",type=str,help="Set Qt widget style (default: Windows)", metavar="NAME", default="Windows")

devgroup = parser.add_argument_group('Plugins')

devgroup.add_argument("--generate", nargs='?', type=str,help="Create a \"blank\" plugin for editing", metavar="FILE",const=1)
devgroup.add_argument( "--noplugins", help=f"Disable plugins", action="store_true")

misc_group = parser.add_argument_group('Miscellaneous')

misc_group.add_argument( "-N","--noask", help=f"Don't ask for connection information on start", action="store_true")
misc_group.add_argument( "-X","--nocommands", help=f"Don't auto-execute commands on connection", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':

	app = QApplication([])

	# "Generate" a blank plugin
	if args.generate:
		if args.generate==1:
			# No argument, so print to STDOUT
			f = open(BLANK_PLUGIN_FILE,'r+')
			x = f.read()
			f.close()
			print(x)
			sys.exit(0)
		else:
			if os.path.isfile(args.generate):
				print("File \""+args.generate+"\" already exists.")
				sys.exit(1)
			# Copy the blank plugin in the data directory
			# to the new location
			shutil.copy(BLANK_PLUGIN_FILE,args.generate)
			print("Plugin generated!")
			sys.exit(0)

	# If user wants to store config data in the install
	# directory, then set that up here
	if args.configinstall:
		args.configdir = config.INSTALL_DIRECTORY

	# Initialize the config system
	config.initialize(args.configdir,args.configname)

	# Initialize the styles system
	styles.initialize(args.configdir,args.configname)

	# Initialize the logs system
	logs.initialize(args.configdir,args.configname)

	# Initialize the user system
	user.initialize(args.configdir,args.configname)

	# Initialize the plugin system
	plugins.initialize(args.configdir,args.configname)

	# Load the config file
	config.load_settings(config.CONFIG_FILE)

	# Set the application font
	if config.APPLICATION_FONT!=None:
		# Set the font set in the config file
		font = QFont()
		font.fromString(config.APPLICATION_FONT)
		app.setFont(font)
	else:
		# Load in fonts from the resources file
		fid = QFontDatabase.addApplicationFont(BUNDLED_FONT)
		for f in OTHER_BUNDLED_FONTS:
			QFontDatabase.addApplicationFont(f)
		_fontstr = QFontDatabase.applicationFontFamilies(fid)[0]
		font = QFont(_fontstr,BUNDLED_FONT_SIZE)
		app.setFont(font)

	# Set Qt widget style
	app.setStyle(args.qtstyle)

	# Handle connecting to a server if one has been provided
	if args.server:

		if args.password=='':
			pword = None
		else:
			pword = args.password

		chans = []
		if args.channel:
			for c in args.channel:
				if type(c)==list:
					chans.append(c)
				else:
					p = c.split(':')
					if len(p)==2:
						chans.append(p)
					else:
						chans.append( [c,''] )

		# Load in user settings
		user.load_user(user.USER_FILE)

		if len(user.NICKNAME.strip())==0:
			print("No nickname set!")
			sys.exit(1)

		if len(user.ALTERNATE.strip())==0:
			print("No alternate nickname set!")
			sys.exit(1)

		if len(user.USERNAME.strip())==0:
			print("No username set!")
			sys.exit(1)

		if len(user.REALNAME.strip())==0:
			print("No realname set!")
			sys.exit(1)

		i = ConnectInfo(
			user.NICKNAME,
			user.ALTERNATE,
			user.USERNAME,
			user.REALNAME,
			args.server,
			args.port,
			pword,
			args.reconnect,
			args.ssl,
		)

		GUI = Merk(
				app,				# Application
				args.configdir,		# Config directory, default None for home directory storage
				args.configname,	# Config directory name, default ".merk"
				i,					# Connection info
				font,				# Application font
				args.noplugins,		# Disable plugins
				args.nocommands,	# Disable connection commands
				chans,				# Channels
				None,				# Parent
			)

		GUI.show()

	else:

		if args.noask:
			# Create the main GUI and show it
			GUI = Merk(
					app,				# Application
					args.configdir,		# Config directory, default None for home directory storage
					args.configname,	# Config directory name, default ".merk"
					None,				# Connection info
					font,				# Application font
					args.noplugins,		# Disable plugins
					args.nocommands,	# Disable connection commands
					[],					# Channels
					None,				# Parent
				)

			GUI.show()
		else:
			# Bring up the connection dialog
			connection_info = ConnectDialog(app,None,'','',args.nocommands)
			if connection_info:
				# Create the main GUI and show it
				GUI = Merk(
						app,				# Application
						args.configdir,		# Config directory, default None for home directory storage
						args.configname,	# Config directory name, default ".merk"
						connection_info,	# Connection info
						font,				# Application font
						args.noplugins,		# Disable plugins
						args.nocommands,	# Disable connection commands
						[],					# Channels
						None,				# Parent
					)

				GUI.show()
			else:
				app.quit()

	# Start the reactor!
	reactor.run()
