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
import merk.config as config

# Handle commandline arguments

parser = argparse.ArgumentParser(
	prog=f"python {os.path.basename(__file__)}",
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description=f'''
███╗   ███╗██████╗ ██████╗ ██╗  ██╗
████╗ ████║╚═══╗██╗██╔══██╗██║ ██╔╝	╔══════════════╗
██╔████╔██║███████║██████╔╝█████╔╝	║ {APPLICATION_NAME} {APPLICATION_VERSION} ║
██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗	╚══════════════╝
██║ ╚═╝ ██║ █████╔╝██║  ██║██║  ██╗
╚═╝     ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

An open source, cross-platform IRC client
https://github.com/nutjob-laboratories/merk
''',
)

miscgroup = parser.add_argument_group('Configuration')

miscgroup.add_argument("-C","--config", type=str,help="Use an alternate configuration file", metavar="FILE", default=None)
# Change the below default to None to store files in the home directory
miscgroup.add_argument("-D","--config-directory",dest="configdir",type=str,help="Location to store configuration files", metavar="DIRECTORY", default=config.INSTALL_DIRECTORY)
miscgroup.add_argument("--config-name",dest="configname",type=str,help="Name of the config file directory (default: .merk)", metavar="NAME", default=".merk")

args = parser.parse_args()

if __name__ == '__main__':

	app = QApplication([])

	# Load in fonts from the resources file
	fid = QFontDatabase.addApplicationFont(BUNDLED_FONT)
	for f in OTHER_BUNDLED_FONTS:
		QFontDatabase.addApplicationFont(f)

	# Set the default font
	_fontstr = QFontDatabase.applicationFontFamilies(fid)[0]
	font = QFont(_fontstr,BUNDLED_FONT_SIZE)

	app.setFont(font)

	GUI = Merk(
			app,				# Application
			args.configdir,		# Config directory, default None for home directory storage
			args.configname,	# Config directory name, default ".merk"
			args.config,		# Config filename, default None for default config file
			None,				# Parent
		)

	GUI.show()

	reactor.run()
