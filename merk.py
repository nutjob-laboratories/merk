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

import argparse
import os
import random
import shutil
import sys
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

app = QApplication([])

import qt5reactor
qt5reactor.install()

from twisted.internet import reactor

SSL_AVAILABLE = True
try:
	from twisted.internet import ssl
except ImportError as error:
	SSL_AVAILABLE = False
except Exception as exception:
	pass

from merk.main import Merk
from merk.resources import *
from merk.dialog import *
import merk.config as config
import merk.styles as styles
import merk.logs as logs
import merk.user as user
import merk.commands as commands
import merk.connection_script as connection_script
import merk.plugins as plugins

if not is_running_from_pyinstaller():
	myprog = f"python {os.path.basename(__file__)}"
else:
	myprog = "merk.exe"

ARG_ABSENT = object()

parser = argparse.ArgumentParser(
	prog=myprog,
	formatter_class=argparse.RawDescriptionHelpFormatter,
	add_help=False,
	description=f'''
╔╦╗╔═╗╦═╗╦╔═  ╦╦═╗╔═╗  ╔═╗╦  ╦╔═╗╔╗╔╔╦╗
║║║║╣ ╠╦╝╠╩╗  ║╠╦╝║    ║  ║  ║║╣ ║║║ ║  Version
╩ ╩╚═╝╩╚═╩ ╩  ╩╩╚═╚═╝  ╚═╝╩═╝╩╚═╝╝╚╝ ╩  {APPLICATION_VERSION}
https://github.com/nutjob-laboratories/merk
https://github.com/danhetrick

Available Qt widget styles: {", ".join(QStyleFactory.keys())}
''',
	epilog=f'''
© {datetime.now().year} Copyright Daniel Hetrick
https://www.gnu.org/licenses/gpl-3.0.en.html
	''',
)

congroup = parser.add_argument_group('Connection')
congroup.add_argument("server",type=str,help="Server to connect to",metavar="SERVER",nargs='?')
congroup.add_argument("port",type=int,help="Server port to connect to (6667)",default=6667,nargs='?',metavar="PORT")
if SSL_AVAILABLE:
	congroup.add_argument("--ssl","--tls",help=f"Use SSL/TLS to connect to IRC",action="store_true")
congroup.add_argument("-p","--password",type=str,help="Use server password to connect",metavar="PASSWORD",default='')
congroup.add_argument("-c","--channel",type=str,help="Join channel on connection",metavar="CHANNEL[:KEY]",action='append')
congroup.add_argument('-C','--connect',metavar="SERVER:PORT[:PASSWORD]",action='append',help='Connect to server via TCP/IP')
if SSL_AVAILABLE:
	congroup.add_argument('-S','--connectssl',metavar="SERVER:PORT[:PASSWORD]",action='append',help='Connect to server via SSL/TLS')

usergroup = parser.add_argument_group('User Information')
usergroup.add_argument("-n","--nickname",type=str,help="Use this nickname to connect",metavar="NICKNAME",default='')
usergroup.add_argument("-u","--username",type=str,help="Use this username to connect",metavar="USERNAME",default='')
usergroup.add_argument("-a","--alternate",type=str,help="Use this alternate nickname to connect",metavar="NICKNAME",default='')
usergroup.add_argument("-r","--realname",type=str,help="Use this realname to connect",metavar="REALNAME",default='')

optiongroup = parser.add_argument_group('Options')
optiongroup.add_argument("-h","--help",help=f"Show help and usage information",action="help")
optiongroup.add_argument("-d","--donotsave",help=f"Do not save new user settings",action="store_true")
optiongroup.add_argument("-x","--donotexecute",help=f"Do not execute connection script",action="store_true")
optiongroup.add_argument("-t","--reconnect",help=f"Reconnect to servers on disconnection",action="store_true")
optiongroup.add_argument("-R","--run",dest="noask",help=f"Don't ask for connection information on start",action="store_true")
optiongroup.add_argument("-o","--on-top",dest="ontop",help=f"Application window always on top",action="store_true")
optiongroup.add_argument("-f","--full-screen",dest="fullscreen",help=f"Application window displays full screen",action="store_true")
optiongroup.add_argument("-s","--script",type=str,help="Use a file as a connection script",metavar="FILE",default='')
optiongroup.add_argument("-P","--disable-plugins",dest="disable",help=f"Disables plugins",action="store_true")

configuration_group = parser.add_argument_group('Files and Directories')
configuration_group.add_argument("--config-name",dest="configname",type=str,help="Name of the configuration file directory (default: .merk)",metavar="NAME",default=".merk")
configuration_group.add_argument("--config-directory",dest="configdir",type=str,help="Location to store configuration files",metavar="DIRECTORY",default=None)
configuration_group.add_argument("--config-local",dest="configinstall",help=f"Store configuration files in install directory",action="store_true")
configuration_group.add_argument("--scripts-directory",dest="scriptdir",type=str,help="Location to look for script files",metavar="DIRECTORY",default=None)
configuration_group.add_argument("--user-file",dest="userfile",type=str,help="File to use for user data",metavar="FILE",default=None)
configuration_group.add_argument("--config-file",dest="configfile",type=str,help="File to use for configuration data",metavar="FILE",default=None)
configuration_group.add_argument("--reset",dest="configdefault",help=f"Reset configuration file to default values",action="store_true")
configuration_group.add_argument("--reset-user",dest="userdefault",help=f"Reset user file to default values",action="store_true")
configuration_group.add_argument("--reset-all",dest="alldefault",help=f"Reset all configuration files to default values",action="store_true")
configuration_group.add_argument("--uninstall-all",dest="uninstall",help=f"Deletes all installed plugins",action="store_true")

misc_group = parser.add_argument_group('Appearance')
misc_group.add_argument("-Q","--qtstyle",dest="qtstyle",type=str,help="Set Qt widget style (default: Windows)",metavar="NAME",default="")
misc_group.add_argument("-D","--dark",dest="darkmode",help=f"Run in dark mode",action="store_true")
misc_group.add_argument("-L","--light",dest="lightmode",help=f"Run in light mode",action="store_true")

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
			sys.stdout.write(f"Valid available styles: {', '.join(QStyleFactory.keys())}\n")
			exit(1)

	app = QApplication([])

	# If user wants to store config data in the install
	# directory, then set that up here
	if args.configinstall:
		if not is_running_from_pyinstaller():
			args.configdir = INSTALL_DIRECTORY
		else:
			args.configdir = os.path.dirname(sys.executable)

	# If we're resetting all config files, make
	# sure that happens
	if args.alldefault:
		args.configdefault = True
		args.userdefault = True

	if args.configfile:
		# Initialize the config system
		config.initialize_file(args.configdir,args.configname,args.configfile)
	else:
		# Initialize the config system
		config.initialize(args.configdir,args.configname)

	# Reset the config files to the default values
	if args.configdefault:
		sys.stdout.write("Resetting configuration file to defaults\n")
		config.save_settings(config.CONFIG_FILE)

	# Initialize the user system
	if args.userfile!=None:
		user.initialize_file(args.configdir,args.configname,args.userfile)
	else:
		user.initialize(args.configdir,args.configname)

	if args.userdefault:
		sys.stdout.write("Resetting user file to defaults\n")
		user.save_user(user.USER_FILE)

	# Initialize the styles system
	styles.initialize(args.configdir,args.configname)

	# Initialize the logs system
	logs.initialize(args.configdir,args.configname)

	# Initialize the plugins system
	plugins.initialize(args.configdir,args.configname)

	# Load the config file
	config.load_settings(config.CONFIG_FILE)

	# Initialize the scripts system
	commands.initialize(args.configdir,args.configname,args.scriptdir)

	# Uninstalls all plugins
	if args.uninstall:
		for root, _, files in os.walk(plugins.PLUGIN_DIRECTORY):
			for file in files:
				file_path = os.path.join(root, file)
				if os.path.exists(file_path):
					try:
						os.remove(file_path)
						sys.stdout.write(f"Deleted {file_path}\n")
					except OSError as e:
						sys.stdout.write(f"Error deleting file: {e}\n")
				else:
					sys.stdout.write(f"File {file_path} not found\n")
		exit(0)

	# Disabled plugins
	if args.disable:
		config.ENABLE_PLUGINS = False
		if not args.donotsave: config.save_settings(config.CONFIG_FILE)

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
		if not args.donotsave: config.save_settings(config.CONFIG_FILE)

	# Apply new style
	app.setStyle(config.QT_WINDOW_STYLE)

	# Set cursor blink rate
	if config.CURSOR_BLINK:
		QApplication.setCursorFlashTime(config.CURSOR_BLINK_RATE)
	else:
		QApplication.setCursorFlashTime(0)

	# Set dark mode if it's in the config file
	if config.DARK_MODE==True:
		args.darkmode = True

	# Set light mode if it's turned on
	if args.lightmode:
		args.darkmode = False

	# Set dark mode palette if it's turned on
	if args.darkmode:
		application_palette = 'dark'
	else:
		application_palette = 'default'

	# Load in the appropriate application palette
	if application_palette!= 'default':
		style = styles.loadPalette(application_palette)

		# Create a new application palette with the loaded settings
		merk_app_palette = QPalette()
		merk_app_palette.setColor(QPalette.Text, QColor(styles.parseColor(style["text"])))
		merk_app_palette.setColor(QPalette.Base, QColor(styles.parseColor(style["base"])))
		merk_app_palette.setColor(QPalette.Window, QColor(styles.parseColor(style["window"])))
		merk_app_palette.setColor(QPalette.WindowText, QColor(styles.parseColor(style["window_text"])))
		merk_app_palette.setColor(QPalette.AlternateBase, QColor(styles.parseColor(style["alternate_base"])))
		merk_app_palette.setColor(QPalette.ToolTipBase, QColor(styles.parseColor(style["tooltip_base"])))
		merk_app_palette.setColor(QPalette.ToolTipText, QColor(styles.parseColor(style["tooltip_text"])))
		merk_app_palette.setColor(QPalette.Button, QColor(styles.parseColor(style["button"])))
		merk_app_palette.setColor(QPalette.ButtonText, QColor(styles.parseColor(style["button_text"])))
		merk_app_palette.setColor(QPalette.BrightText, QColor(styles.parseColor(style["bright_text"])))
		merk_app_palette.setColor(QPalette.Link, QColor(styles.parseColor(style["link"])))
		merk_app_palette.setColor(QPalette.Highlight, QColor(styles.parseColor(style["highlight"])))
		merk_app_palette.setColor(QPalette.HighlightedText, QColor(styles.parseColor(style["highlighted_text"])))
		merk_app_palette.setColor(QPalette.Active, QPalette.Button, QColor(styles.parseColor(style["active_button"])))
		merk_app_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(styles.parseColor(style["disabled_button_text"])))
		merk_app_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(styles.parseColor(style["disabled_window_text"])))
		merk_app_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(styles.parseColor(style["disabled_text"])))
		merk_app_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(styles.parseColor(style["disabled_light"])))

		# Apply palette to the app
		app.setPalette(merk_app_palette)

		# Make sure that menu separators have the palette colors
		# applied to them
		app.setStyleSheet(f"""
			QMenu::separator {{
				background-color: {styles.parseColor(style["separator"])};
				height: 1px;
			}}
			QGroupBox {{
				border: 1px solid {styles.parseColor(style["separator"])};
			}}
			""")

	def find_file(file):
		if os.path.exists(file) and os.access(file, os.R_OK): return file
		if args.scriptdir!=None:
			file2 = os.path.join(args.scriptdir,file)
			if os.path.exists(file2) and os.access(file2, os.R_OK): return file2
		return commands.find_file(file,SCRIPT_FILE_EXTENSION)

	def create_connection(host,port,password,ssl):
		if password=='':
			pword = None
		else:
			pword = password

		# Load in user settings
		user.load_user(user.USER_FILE)

		user_info_changed = False
		if args.nickname=='':
			if len(user.NICKNAME.strip())==0:
				sys.stdout.write("No nickname set!\n")
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
				args.alternate = args.nickname + str(random.randint(1,99))
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

		if not args.donotsave:
			# Add connection to history
			user_history = list(user.HISTORY)

			# Check to make sure that the connection isn't
			# already in the user's history
			inhistory = False
			for s in user_history:
				if s[0]==host:
					if s[1]==str(port):
						inhistory = True

			# If the connection isn't already in the user's
			# history, then add it
			if inhistory==False:
				if ssl:
					ussl = "ssl"
				else:
					ussl = "normal"
				if pword==None:
					spass = ''
				else:
					spass = pword
				entry = [ host,str(port),UNKNOWN_NETWORK,ussl,spass ]
				user_history.append(entry)
				user.HISTORY = user_history
				user_info_changed = True

			if user_info_changed:
				user.save_user(user.USER_FILE)

		if args.donotexecute==True:
			EXECUTE_CONNECTION_SCRIPT = False
		else:
			EXECUTE_CONNECTION_SCRIPT = True

			if args.script!='':
				file = find_file(args.script)

				if file!=None:
					f = open(file,"r")
					cscript = f.read()
					f.close()

					connection_script.add_connection_script(f"{host}:{port}",cscript)
				else:
					# throw error
					sys.stdout.write(f"File \"{args.script}\" does not exist or is not readable.\n")
					sys.exit(1)

		i = ConnectInfo(
			args.nickname,
			args.alternate,
			args.username,
			args.realname,
			host,
			port,
			pword,
			args.reconnect,
			ssl,
			EXECUTE_CONNECTION_SCRIPT, # execute script
			)

		return i

	def startMERK(app,gui):
		gui.show()
		sys.exit(reactor.run())

	# Handle connecting to a server if one has been provided
	if args.server:

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

		i = create_connection(args.server,args.port,args.password,args.ssl)

		GUI = Merk(
				app,							# Application
				args.configdir,					# Config directory, default None for home directory storage
				args.configname,				# Config directory name, default ".merk"
				i,								# Connection info
				font,							# Application font
				chans,							# Channels
				args.donotexecute,				# Do not execute script default
				args.donotsave,					# Do not save default
				args.ontop,						# Always on top
				args.fullscreen,				# Full screen
				None,							# Parent
			)

		startMERK(app,GUI)

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

		if args.noask or not config.ASK_FOR_SERVER_ON_STARTUP:
			# Create the main GUI and show it
			GUI = Merk(
					app,							# Application
					args.configdir,					# Config directory, default None for home directory storage
					args.configname,				# Config directory name, default ".merk"
					None,							# Connection info
					font,							# Application font
					[],								# Channels
					args.donotexecute,				# Do not execute script default
					args.donotsave,					# Do not save default
					args.ontop,						# Always on top
					args.fullscreen,				# Full screen
					None,							# Parent
				)

			startMERK(app,GUI)
		else:

			connections = []
			if args.connect:
				for c in args.connect:
					serv = c.split(':')
					if len(serv)==3:
						server = serv[0]
						port = serv[1]
						password = serv[2]
					elif len(serv)==2:
						server = serv[0]
						port = serv[1]
						password = ''
					else:
						server = c
						port = 6667
						password = ''

					try:
						int(port)
					except:
						sys.stdout.write("Port must be a number!\n")
						sys.exit(1)

					port = int(port)

					i = create_connection(server,port,password,False)
					connections.append(i)

			if args.connectssl:
				for c in args.connectssl:
					serv = c.split(':')
					if len(serv)==3:
						server = serv[0]
						port = serv[1]
						password = serv[2]
					elif len(serv)==2:
						server = serv[0]
						port = serv[1]
						password = ''
					else:
						server = c
						port = 6697
						password = ''

					try:
						int(port)
					except:
						sys.stdout.write("Port must be a number!\n")
						sys.exit(1)

					port = int(port)

					i = create_connection(server,port,password,True)
					connections.append(i)

			# Bring up the connection dialog
			if len(connections)==0:
				connection_info = ConnectInfo(CONNECTION_MISSING_INFO_ERROR,None,None,None,None,None,None,None,None,None)
				while connection_info.nickname==CONNECTION_MISSING_INFO_ERROR:
					if config.SIMPLIFIED_DIALOGS:
						connection_info = ConnectDialogSimplifiedInitial(app,None,'','',args.donotexecute,args.donotsave)
					else:
						connection_info = ConnectDialogInitial(app,None,'','',args.donotexecute,args.donotsave)
				if connection_info:
					# Create the main GUI and show it
					if connection_info.nickname==CONNECTION_DIALOG_CANCELED:
						app.quit()
					else:
						GUI = Merk(
								app,							# Application
								args.configdir,					# Config directory, default None for home directory storage
								args.configname,				# Config directory name, default ".merk"
								connection_info,				# Connection info
								font,							# Application font
								[],								# Channels
								args.donotexecute,				# Do not execute script default
								args.donotsave,					# Do not save default
								args.ontop,						# Always on top
								args.fullscreen,				# Full screen
								None,							# Parent
							)

						startMERK(app,GUI)
				else:
					app.quit()
			else:

				# If the --channel argument is used,
				# make sure the channels are passed
				# I'm not sure why someone would do this,
				# but who am I to judge?
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

				# Create the main GUI and show it
				GUI = Merk(
						app,							# Application
						args.configdir,					# Config directory, default None for home directory storage
						args.configname,				# Config directory name, default ".merk"
						connections,					# Connection info
						font,							# Application font
						chans,							# Channels
						args.donotexecute,				# Do not execute script default
						args.donotsave,					# Do not save default
						args.ontop,						# Always on top
						args.fullscreen,				# Full screen
						None,							# Parent
					)

				startMERK(app,GUI)
