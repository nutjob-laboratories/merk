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

DARK_PALETTE="""
text {
	color: #FFFFFF;
}

base {
	color: #232323;
}

window {
	color: #353535;
}

window_text {
	color: #FFFFFF;
}

alternate_base {
	color: #353535;
}

tooltip_base {
	color: #191919;
}

tooltip_text {
	color: #FFFFFF;
}

button {
	color: #353535;
}

button_text {
	color: #FFFFFF;
}

bright_text {
	color: #FF0000;
}

link {
	color: #2B82DA;
}

highlight {
	color: #2B82DA;
}

highlighted_text {
	color: #FFFFFF;
}

active_button {
	color: #353535;
}

disabled_button_text {
	color: #A9A9A9;
}

disabled_window_text {
	color: #A9A9A9;
}

disabled_text {
	color: #A9A9A9;
}

disabled_light {
	color: #353535;
}

separator {
	color: #A9A9A9;
}
"""

DEFAULT_STYLE="""timestamp {
	font-weight: bold;
}

username {
	font-weight: bold;
	color: #0000FF;
}

private {
	font-style: italic;
	font-weight: bold;
	color: #0000FF;
}

message {
}

system {
	font-weight: bold;
	color: #FF8C00;
}

self {
	font-weight: bold;
	color: #FF0000;
}

action {
	font-style: italic;
	font-weight: bold;
	color: #006400;
}

notice {
	font-weight: bold;
	color: #800080;
}

hyperlink {
	text-decoration: underline;
	font-weight: bold;
	color: #0000FF;
}

all {
	background-color: #FFFFFF;
	color: #000000;
}

error {
	font-weight: bold;
	color: #FF0000;
}

server {
	font-weight: bold;
	color: #0073ad;
}

raw {
}"""