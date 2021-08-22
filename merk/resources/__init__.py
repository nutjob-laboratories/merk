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

from datetime import datetime
import sys
import os

# Load in resource file
globals()["merk.resources.resources"] = __import__("merk.resources.resources")

INSTALL_DIRECTORY = sys.path[0]
MERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "merk")
DATA_DIRECTORY = os.path.join(MERK_MODULE_DIRECTORY, "data")
AUTOCOMPLETE_DIRECTORY = os.path.join(DATA_DIRECTORY, "autocomplete")
EMOJI_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "emoji2.txt")
EMOJI_ALIAS_AUTOCOMPLETE_FILE = os.path.join(AUTOCOMPLETE_DIRECTORY, "emoji1.txt")

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
APPLICATION_NAME = "mƏrk"

MDI_BACKGROUND = ":/gui-background.png"

BUNDLED_FONT = ":/font-FiraMono-Regular.ttf"
OTHER_BUNDLED_FONTS = [
	":/font-FiraMono-Medium.ttf",
	":/font-FiraMono-Bold.ttf",
]
BUNDLED_FONT_SIZE = 9

# Constants

CHANNEL_WINDOW = 0
SERVER_WINDOW = 1
PRIVATE_WINDOW = 2

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

ROUND_UNCHECKED_ICON = ":/icon-runchecked.png"
ROUND_CHECKED_ICON = ":/icon-rchecked.png"

ADMIN_USER = ":/gui-admin.png"
HALFOP_USER = ":/gui-halfop.png"
OP_USER = ":/gui-op.png"
OWNER_USER = ":/gui-owner.png"
VOICE_USER = ":/gui-voice.png"
NORMAL_USER = ":/gui-normal.png"

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
