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

from datetime import datetime
import sys
import os
import math

# Load in resource file
globals()["merk.resources.resources"] = __import__("merk.resources.resources")

INSTALL_DIRECTORY = sys.path[0]
MERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "merk")
DATA_DIRECTORY = os.path.join(MERK_MODULE_DIRECTORY, "data")
AUTOCOMPLETE_DIRECTORY = os.path.join(DATA_DIRECTORY, "autocomplete")
EMOJI_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "emoji2.txt")
EMOJI_ALIAS_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "emoji1.txt")
NETWORK_FILE = os.path.join(DATA_DIRECTORY, "servers.txt")

DOCUMENTATION_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "documentation")
PLUGIN_DOCUMENTATION = os.path.join(DOCUMENTATION_DIRECTORY, "MERK_Plugin_Development_Guide.pdf")

# Load in major and minor version
f = open(os.path.join(DATA_DIRECTORY, "major.txt"),mode="r",encoding="latin-1",errors="ignore")
major = f.read()
f.close()

f = open(os.path.join(DATA_DIRECTORY, "minor.txt"),mode="r",encoding="latin-1",errors="ignore")
minor = f.read()
f.close()

# Format minor version so it is always
# at least three digits long
if len(minor)==1:
	minor = f"00{minor}"
elif len(minor)==2:
	minor = f"0{minor}"

APPLICATION_VERSION = major+"."+minor
APPLICATION_NAME = "MERK"
APPLICATION_SOURCE = "https://github.com/nutjob-laboratories/merk"
SCRIPT_FILE_EXTENSION = "merk"

MDI_BACKGROUND = ":/gui-background.png"

BUNDLED_FONT = ":/font-FiraMono-Regular.ttf"
OTHER_BUNDLED_FONTS = [
	":/font-FiraMono-Medium.ttf",
	":/font-FiraMono-Bold.ttf",
]
BUNDLED_FONT_SIZE = 10

# Constants

CHANNEL_WINDOW = 0
SERVER_WINDOW = 1
PRIVATE_WINDOW = 2
EDITOR_WINDOW = 3

CHAT_WINDOW_WIDGET_SPACING = 5

SYSTEM_MESSAGE = 0
ERROR_MESSAGE = 1
ACTION_MESSAGE = 2
CHAT_MESSAGE = 3
SELF_MESSAGE = 4
NOTICE_MESSAGE = 5
SERVER_MESSAGE = 6
PRIVATE_MESSAGE = 7
RAW_SYSTEM_MESSAGE = 8
HORIZONTAL_RULE_MESSAGE = 9
HARD_HORIZONTAL_RULE_MESSAGE = 10
TEXT_HORIZONTAL_RULE_MESSAGE = 11
WHOIS_MESSAGE = 12
DATE_MESSAGE = 13
PLUGIN_MESSAGE = 14

UNKNOWN_NETWORK = "UNKNOWN"

# Icons

APPLICATION_ICON = ":/icon-app.png"
CASCADE_ICON = ":/icon-cascade.png"
TILE_ICON = ":/icon-tile.png"
NEXT_ICON = ":/icon-next.png"
PREVIOUS_ICON = ":/icon-previous.png"
CONSOLE_ICON = ":/icon-console.png"
PRIVATE_ICON = ":/icon-private.png"
CHANNEL_ICON = ":/icon-channel.png"
QUIT_ICON = ":/icon-quit.png"
SPELLCHECK_ICON = ":/icon-spellcheck.png"
TOGGLE_ON_ICON = ":/icon-turnon.png"
TOGGLE_OFF_ICON = ":/icon-turnoff.png"
NETWORK_ICON = ":/icon-network.png"
CONNECT_ICON = ":/icon-connect.png"
DISCONNECT_ICON = ":/icon-disconnect.png"
BOLD_ICON = ":/icon-bold.png"
ITALIC_ICON = ":/icon-italic.png"
RESET_ICON = ":/icon-reset.png"
INFO_ICON = ":/icon-info.png"
BOOKMARK_ICON = ":/icon-bookmark.png"
SECURE_ICON = ":/icon-secure.png"
VISITED_BOOKMARK_ICON = ":/icon-visited_bookmark.png"
VISITED_SECURE_ICON = ":/icon-visited_secure.png"
ROUND_UNCHECKED_ICON = ":/icon-runchecked.png"
ROUND_CHECKED_ICON = ":/icon-rchecked.png"
STYLE_ICON = ":/icon-style.png"
WHOIS_ICON = ":/icon-whois.png"
KICK_ICON = ":/icon-kick.png"
BAN_ICON = ":/icon-ban.png"
KICKBAN_ICON = ":/icon-kickban.png"
CLIPBOARD_ICON = ":/icon-clipboard.png"
PLUS_ICON = ":/icon-plus.png"
MINUS_ICON = ":/icon-minus.png"
KEY_ICON = ":/icon-key.png"
FONT_ICON = ":/icon-font.png"
RESIZE_ICON = ":/icon-resize.png"
SETTINGS_ICON = ":/icon-settings.png"
EDIT_ICON = ":/icon-edit.png"
INPUT_ICON = ":/icon-input.png"
LOG_ICON = ":/icon-log.png"
MESSAGE_ICON = ":/icon-message.png"
ABOUT_ICON = ":/icon-about.png"
OPTIONS_ICON = ":/icon-options.png"
PRIVATE_WINDOW_ICON = ":/icon-private_window.png"
CHANNEL_WINDOW_ICON = ":/icon-channel_window.png"
LINK_ICON = ":/icon-link.png"
FOLDER_ICON = ":/icon-folder.png"
DICTIONARY_ICON = ":/icon-dictionary.png"
COMMAND_ICON = ":/icon-command.png"
CHECKED_ICON = ":/icon-checked.png"
UNCHECKED_ICON = ":/icon-unchecked.png"
TIMESTAMP_ICON = ":/icon-timestamp.png"
INTERFACE_ICON = ":/icon-interface.png"
NEWFILE_ICON = ":/icon-new_file.png"
OPENFILE_ICON = ":/icon-file_open.png"
SAVEFILE_ICON = ":/icon-save_file.png"
SAVEASFILE_ICON = ":/icon-save_as.png"

UNDO_ICON = ":/icon-undo.png"
REDO_ICON = ":/icon-redo.png"
CUT_ICON = ":/icon-cut.png"
COPY_ICON = ":/icon-copy.png"
SELECTALL_ICON = ":/icon-select_all.png"

SCRIPT_MENU_ICON = ":/icon-script_menu.png"
SETTINGS_MENU_ICON = ":/icon-settings_menu.png"
STYLE_MENU_ICON = ":/icon-style_menu.png"
LOG_MENU_ICON = ":/icon-log_menu.png"
ABOUT_MENU_ICON = ":/icon-about_menu.png"

ADMIN_USER = ":/gui-admin.png"
HALFOP_USER = ":/gui-halfop.png"
OP_USER = ":/gui-op.png"
OWNER_USER = ":/gui-owner.png"
VOICE_USER = ":/gui-voice.png"
NORMAL_USER = ":/gui-normal.png"

HORIZONTAL_DOTTED_BACKGROUND = ":/gui-horizontal_dotted.png"
HORIZONTAL_RULE_BACKGROUND = ":/gui-horizontal_rule.png"
LIGHT_HORIZONTAL_DOTTED_BACKGROUND = ":/gui-light_horizontal_dotted.png"
LIGHT_HORIZONTAL_RULE_BACKGROUND = ":/gui-light_horizontal_rule.png"

DISCONNECT_DIALOG_IMAGE = ":/gui-disconnect_dialog.png"

MERK_SPLASH_IMAGE = ":/gui-merk_splash.png"

NUTJOB_LOGO = ":/gui-nutjob.png"

MERK_ABOUT_LOGO = ":/gui-about.png"

SCRIPT_ICON = ":/icon-script.png"
CLOSE_ICON = ":/icon-close.png"

# Load in autocomplete data
EMOJI_AUTOCOMPLETE = []
with open(EMOJI_ALIAS_AUTOCOMPLETE_FILE,mode="r",encoding="latin-1",errors="ignore") as fp:
	line = fp.readline()
	while line:
		e = line.strip()
		EMOJI_AUTOCOMPLETE.append(e)
		line = fp.readline()
with open(EMOJI_AUTOCOMPLETE_FILE,mode="r",encoding="latin-1",errors="ignore") as fp:
	line = fp.readline()
	while line:
		e = line.strip()
		EMOJI_AUTOCOMPLETE.append(e)
		line = fp.readline()

HELP_ENTRY_TEMPLATE='''<tr><td>%_USAGE_%&nbsp;</td><td>%_DESCRIPTION_%</td></tr>'''

HELP_DISPLAY_TEMPLATE='''<table style="width: 100%" border="0">
	<tbody>
        <tr>
          <td><center><b>Commands</b></center></td>
        </tr>
        <tr>
          <td><small>
          Arguments inside brackets are optional. If called from a channel window,
          channel windows can be omitted to apply the command to the current channel.
          %_AUTOCOMPLETE_%
          %_SCRIPTING_%
          </small></td>
        </tr>
        <tr>
          <td>&nbsp;</center></td>
        </tr>
        <tr>
          <td>
            <table style="width: 100%" border="0">
              <tbody>
                %_LIST_%
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>'''

# Classes

class Message:
	def __init__(self,mtype,sender,contents,timestamp=None):
		if timestamp:
			self.timestamp = timestamp
		else:
			self.timestamp = datetime.timestamp(datetime.now())
		self.type = mtype
		self.sender = sender
		self.contents = contents

class ConnectInfo:
	def __init__(self,nick,alt,username,realname,host,port,password,reconnect,ssl):
		self.nickname = nick
		self.alternate = alt
		self.username = username
		self.realname = realname
		self.host = host
		self.port = port
		self.password = password
		self.reconnect = reconnect
		self.ssl = ssl

class WhoisData:
	def __init__(self):
		self.nickname = 'Unknown'
		self.username = 'Unknown'
		self.realname = 'Unknown'
		self.host = 'Unknown'
		self.signon = '0'
		self.idle = '0'
		self.server = 'Unknown'
		self.channels = 'Unknown'
		self.privs = 'is a normal user'

class WhoData:
	def __init__(self):
		self.username = 'Unknown'
		self.host = 'Unknown'
		self.server = 'Unknown'
		self.channel = 'Unknown'

class WhoWasData:
	def __init__(self):
		self.username = 'Unknown'
		self.host = 'Unknown'
		self.realname = 'Unknown'

# Functions

def convert_size(size_bytes):
	if size_bytes == 0:
		return "0 B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])

def convertSeconds(seconds):
	h = seconds//(60*60)
	m = (seconds-h*60*60)//60
	s = seconds-(h*60*60)-(m*60)
	return [h, m, s]

def prettyUptime(uptime):
	t = convertSeconds(uptime)
	hours = t[0]
	if len(str(hours))==1: hours = f"0{hours}"
	minutes = t[1]
	if len(str(minutes))==1: minutes = f"0{minutes}"
	seconds = t[2]
	if len(str(seconds))==1: seconds = f"0{seconds}"
	return f"{hours}:{minutes}:{seconds}"

def test_if_window_background_is_light(obj):
	# Determine if window color is dark or light
		mbcolor = obj.palette().color(QPalette.Window).name()
		c = tuple(int(mbcolor[i:i + 2], 16) / 255. for i in (1, 3, 5))
		luma = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
		luma = luma*100

		if luma>=40:
			return True
		else:
			return False

def test_if_background_is_light(style):

	bg = None
	style = style.strip()
	for e in style.split(';'):
		y = e.split(':')
		if len(y)==2:
			c = y[0].strip()
			if c.lower()=='background-color':
				bg = y[1].strip()

	if bg!=None:
		c = tuple(int(bg[i:i + 2], 16) / 255. for i in (1, 3, 5))
		luma = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
		luma = luma*100

		if luma>=40:
			return True
		else:
			return False

# Widgets

class QNoSpaceLineEdit(QLineEdit):

	def __init__(self, *args):
		QLineEdit.__init__(self, *args)

	def keyPressEvent(self,event):

		if event.key() == Qt.Key_Space:
			return
		else:
			return super().keyPressEvent(event)