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
import random
import shutil
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

app = QApplication([])

import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

from merk.main import Merk
from merk.resources.version import *
from merk.dialog import *
import merk.config as config
import merk.styles as styles
import merk.logs as logs
import merk.user as user

import merk.commands as commands

parser = argparse.ArgumentParser(
	prog=f"python {os.path.basename(__file__)}",
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=f'''
┳┳┓┏┓┳┓┓┏┓  ┳┳┓┏┓  ┏┓┓ ┳┏┓┳┓┏┳┓ 
┃┃┃┣ ┣┫┃┫   ┃┣┫┃   ┃ ┃ ┃┣ ┃┃ ┃  Version
┛ ┗┗┛┛┗┛┗┛  ┻┛┗┗┛  ┗┛┗┛┻┗┛┛┗ ┻  {APPLICATION_VERSION}                              
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
congroup.add_argument("-n","--nickname", type=str,help="Use this nickname to connect", metavar="NICKNAME", default='')
congroup.add_argument("-u","--username", type=str,help="Use this username to connect", metavar="USERNAME", default='')
congroup.add_argument("-a","--alternate", type=str,help="Use this alternate nickname to connect", metavar="NICKNAME", default='')
congroup.add_argument("-r","--realname", type=str,help="Use this realname to connect", metavar="REALNAME", default='')

configuration_group = parser.add_argument_group('Configuration')

configuration_group.add_argument( "-C","--config-name",dest="configname",type=str,help="Name of the configuration file directory (default: .merk)", metavar="NAME", default=".merk")
configuration_group.add_argument( "-D","--config-directory",dest="configdir",type=str,help="Location to store configuration files", metavar="DIRECTORY", default=None)
configuration_group.add_argument( "-L","--config-local",dest="configinstall",help=f"Store configuration files in install directory", action="store_true")
configuration_group.add_argument( "-S","--scripts-directory",dest="scriptdir",type=str,help="Location to look for script files", metavar="DIRECTORY", default=None)

misc_group = parser.add_argument_group('Miscellaneous')

misc_group.add_argument( "-Q","--qtstyle",dest="qtstyle",type=str,help="Set Qt widget style (default: Fusion)", metavar="NAME", default="")
misc_group.add_argument( "-N","--noask", help=f"Don't ask for connection information on start", action="store_true")
misc_group.add_argument( "-X","--nocommands", help=f"Don't auto-execute commands on connection", action="store_true")
misc_group.add_argument( "-M","--dark",dest="darkmode", help=f"Run in dark mode", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':

	# If the user passes us a new Qt window style...
	if args.qtstyle!="":
		# Check to see if it's a valid style
		if args.qtstyle in QStyleFactory.keys():
			# Style is valid
			pass
		else:
			# Tell user the style is invalid and exit
			sys.stdout.write(f"Invalid Qt window style: {args.qtstyle}\n")
			sys.stdout.write(f"Valid available styles: {", ".join(QStyleFactory.keys())}\n")
			exit(1)

	app = QApplication([])

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

	# Load the config file
	config.load_settings(config.CONFIG_FILE)

	# Initialize the scripts system
	commands.initialize(args.configdir,args.configname,args.scriptdir)

	# Set the application font
	if config.APPLICATION_FONT!=None:
		# Set the font set in the config file
		font = QFont()
		font.fromString(config.APPLICATION_FONT)
		app.setFont(font)
	else:
		# Load in fonts from the resources 
		from merk.resources import *
		fid = QFontDatabase.addApplicationFont(BUNDLED_FONT)
		for f in OTHER_BUNDLED_FONTS:
			QFontDatabase.addApplicationFont(f)
		_fontstr = QFontDatabase.applicationFontFamilies(fid)[0]
		font = QFont(_fontstr,BUNDLED_FONT_SIZE)
		app.setFont(font)

	# If a new Qt window style has been passed...
	if args.qtstyle!="":
		# Set new style and save it to the config
		config.QT_WINDOW_STYLE = args.qtstyle
		config.save_settings(config.CONFIG_FILE)

	# Apply new style
	app.setStyle(config.QT_WINDOW_STYLE)

	default_palette = app.palette()

	# Set dark mode if it's in the config file
	if config.DARK_MODE==True:
		args.darkmode = True

	# Set dark mode palette if it's turned on
	if args.darkmode:
		dark_palette = QPalette()

		dark_palette.setColor(QPalette.Text, Qt.white)
		dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))

		dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.WindowText, Qt.white)
		dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
		dark_palette.setColor(QPalette.ToolTipText, Qt.white)
		dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.ButtonText, Qt.white)
		dark_palette.setColor(QPalette.BrightText, Qt.red)
		dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
		dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
		# dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
		dark_palette.setColor(QPalette.HighlightedText, Qt.white)
		dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
		dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
		dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
		dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
		dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
		app.setPalette(dark_palette)

		# Make sure that menu separators are visible
		app.setStyleSheet("""
			QMenu::separator {
				background-color: darkGray;
				height: 1px;
			}
			""")

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

		user_info_changed = False
		if args.nickname=='':
			if len(user.NICKNAME.strip())==0:
				print("No nickname set!")
				sys.exit(1)
			args.nickname = user.NICKNAME
		else:
			user.NICKNAME = args.nickname
			user_info_changed = True

		if args.username=='':
			if len(user.USERNAME.strip())==0:
				args.username = args.nickname
			else:
				args.username = user.USERNAME
		else:
			user.USERNAME = args.username
			user_info_changed = True

		if args.alternate=='':
			if len(user.ALTERNATE.strip())==0:
				args.alternate = args.nickname + str(random.randint(1,999))
			else:
				args.alternate = user.ALTERNATE
		else:
			user.ALTERNATE = args.alternate
			user_info_changed = True

		if args.realname=='':
			if len(user.REALNAME.strip())==0:
				args.realname = APPLICATION_NAME +" "+APPLICATION_VERSION
			else:
				args.realname = user.REALNAME
		else:
			user.REALNAME = args.realname
			user_info_changed = True

		if user_info_changed: user.save_user(user.USER_FILE)

		i = ConnectInfo(
			args.nickname,
			args.alternate,
			args.username,
			args.realname,
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
				args.nocommands,	# Disable connection commands
				chans,				# Channels
				args.darkmode,		# Dark mode
				default_palette,
				None,				# Parent
			)

		GUI.show()

	else:

		# Load in user settings
		user.load_user(user.USER_FILE)

		user_info_changed = False
		if args.nickname!='':
			user.NICKNAME = args.nickname
			user_info_changed = True

		if args.username!='':
			user.USERNAME = args.username
			user_info_changed = True

		if args.alternate!='':
			user.ALTERNATE = args.alternate
			user_info_changed = True

		if args.realname!='':
			user.REALNAME = args.realname
			user_info_changed = True

		if user_info_changed: user.save_user(user.USER_FILE)

		if args.noask:
			# Create the main GUI and show it
			GUI = Merk(
					app,				# Application
					args.configdir,		# Config directory, default None for home directory storage
					args.configname,	# Config directory name, default ".merk"
					None,				# Connection info
					font,				# Application font
					args.nocommands,	# Disable connection commands
					[],					# Channels
					args.darkmode,		# Dark mode
					default_palette,
					None,				# Parent
				)

			GUI.show()
		else:
			# Bring up the connection dialog
			connection_info = ConnectDialog(app,None,'','',args.nocommands,args.darkmode)
			if connection_info:
				# Create the main GUI and show it
				GUI = Merk(
						app,				# Application
						args.configdir,		# Config directory, default None for home directory storage
						args.configname,	# Config directory name, default ".merk"
						connection_info,	# Connection info
						font,				# Application font
						args.nocommands,	# Disable connection commands
						[],					# Channels
						args.darkmode,		# Dark mode
						default_palette,
						None,				# Parent
					)

				GUI.show()
			else:
				app.quit()

	# Start the reactor!
	reactor.run()
