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

# Load in resource file
globals()["merk.resources.resources"] = __import__("merk.resources.resources")

# Load in major and minor version
f = open("./merk/data/major.txt","r")
major = f.read()
f.close()

f = open("./merk/data/minor.txt","r")
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

ROUND_UNCHECKED_ICON = ":/icon-runchecked.png"
ROUND_CHECKED_ICON = ":/icon-rchecked.png"

ADMIN_USER = ":/gui-admin.png"
HALFOP_USER = ":/gui-halfop.png"
OP_USER = ":/gui-op.png"
OWNER_USER = ":/gui-owner.png"
VOICE_USER = ":/gui-voice.png"
NORMAL_USER = ":/gui-normal.png"
