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

# Handle commandline arguments

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

configuration_group = parser.add_argument_group('Configuration')

# Change the below default to None to store files in the home directory
configuration_group.add_argument("-D","--config-directory",dest="configdir",type=str,help="Location to store configuration files", metavar="DIRECTORY", default=config.INSTALL_DIRECTORY)
configuration_group.add_argument("--config-name",dest="configname",type=str,help="Name of the configuration file directory (default: .merk)", metavar="NAME", default=".merk")
configuration_group.add_argument("--qtstyle",dest="qtstyle",type=str,help="Set Qt widget style (default: Windows)", metavar="NAME", default="Windows")

misc_group = parser.add_argument_group('Miscellaneous')

misc_group.add_argument( "-N","--noask", help=f"Don't ask for connection information on start", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':

	app = QApplication([])

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

	# Load in fonts from the resources file
	fid = QFontDatabase.addApplicationFont(BUNDLED_FONT)
	for f in OTHER_BUNDLED_FONTS:
		QFontDatabase.addApplicationFont(f)

	# Set the application font
	if config.APPLICATION_FONT!=None:
		# Set the font set in the config file
		font = QFont()
		font.fromString(config.APPLICATION_FONT)
		app.setFont(font)
	else:
		# Set the default font
		_fontstr = QFontDatabase.applicationFontFamilies(fid)[0]
		font = QFont(_fontstr,BUNDLED_FONT_SIZE)
		app.setFont(font)

	# Set Qt widget style
	app.setStyle(args.qtstyle)

	if args.noask:
		# Create the main GUI and show it
		GUI = Merk(
				app,				# Application
				args.configdir,		# Config directory, default None for home directory storage
				args.configname,	# Config directory name, default ".merk"
				None,				# Connection info
				font,				# Application font
				None,				# Parent
			)

		GUI.show()
	else:
		# Bring up the connection dialog
		connection_info = ConnectDialog(app)
		if connection_info:
			# Create the main GUI and show it
			GUI = Merk(
					app,				# Application
					args.configdir,		# Config directory, default None for home directory storage
					args.configname,	# Config directory name, default ".merk"
					connection_info,	# Connection info
					font,				# Application font
					None,				# Parent
				)

			GUI.show()
		else:
			app.quit()

	# Start the reactor!
	reactor.run()
