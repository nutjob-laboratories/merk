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

import sys
import os
import json
from pathlib import Path

from .resources import *

INSTALL_DIRECTORY = sys.path[0]
MERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "merk")
DATA_DIRECTORY = os.path.join(MERK_MODULE_DIRECTORY, "data")

CONFIG_DIRECTORY = None
CONFIG_FILE = None

MDI_BACKGROUND_IMAGE = None
APPLICATION_FONT = None
DISPLAY_NAME = APPLICATION_NAME
DISPLAY_ICON = APPLICATION_ICON
DEFAULT_SUBWINDOW_WIDTH = 640
DEFAULT_SUBWINDOW_HEIGHT = 480
COMMAND_HISTORY_LENGTH = 20
DICTIONARY = [
	"merk",
	"mƏrk",
	"Merk",
]
NICKNAME_PAD_LENGTH = 15
DISPLAY_TIMESTAMP = True
TIMESTAMP_FORMAT = "%H:%M:%S"
CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES = True
WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW = True

def save_settings(filename):

	settings = {
		"mdi_background_image": MDI_BACKGROUND_IMAGE,
		"application_font": APPLICATION_FONT,
		"display_name": DISPLAY_NAME,
		"display_icon": DISPLAY_ICON,
		"default_subwindow_width": DEFAULT_SUBWINDOW_WIDTH,
		"default_subwindow_height": DEFAULT_SUBWINDOW_HEIGHT,
		"command_history_length": COMMAND_HISTORY_LENGTH,
		"dictionary": DICTIONARY,
		"nickname_pad_length": NICKNAME_PAD_LENGTH,
		"display_timestamp": DISPLAY_TIMESTAMP,
		"timestamp_format": TIMESTAMP_FORMAT,
		"create_window_for_incoming_private_messages": CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES,
		"write_private_messages_to_server_window": WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW,
	}

	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def patch_settings(settings):
	if not "mdi_background_image" in settings:
		settings["mdi_background_image"] = MDI_BACKGROUND_IMAGE
	if not "application_font" in settings:
		settings["application_font"] = APPLICATION_FONT
	if not "display_name" in settings:
		settings["display_name"] = DISPLAY_NAME
	if not "display_icon" in settings:
		settings["display_icon"] = DISPLAY_ICON
	if not "default_subwindow_width" in settings:
		settings["default_subwindow_width"] = DEFAULT_SUBWINDOW_WIDTH
	if not "default_subwindow_height" in settings:
		settings["default_subwindow_height"] = DEFAULT_SUBWINDOW_HEIGHT
	if not "command_history_length" in settings:
		settings["command_history_length"] = COMMAND_HISTORY_LENGTH
	if not "dictionary" in settings:
		settings["dictionary"] = DICTIONARY
	if not "nickname_pad_length" in settings:
		settings["nickname_pad_length"] = NICKNAME_PAD_LENGTH
	if not "display_timestamp" in settings:
		settings["display_timestamp"] = DISPLAY_TIMESTAMP
	if not "timestamp_format" in settings:
		settings["timestamp_format"] = TIMESTAMP_FORMAT
	if not "create_window_for_incoming_private_messages" in settings:
		settings["create_window_for_incoming_private_messages"] = CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES
	if not "write_private_messages_to_server_window" in settings:
		settings["write_private_messages_to_server_window"] = WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW

	return settings

def load_settings(filename):
	global MDI_BACKGROUND_IMAGE
	global APPLICATION_FONT
	global DISPLAY_NAME
	global DISPLAY_ICON
	global DEFAULT_SUBWINDOW_WIDTH
	global DEFAULT_SUBWINDOW_HEIGHT
	global COMMAND_HISTORY_LENGTH
	global DICTIONARY
	global NICKNAME_PAD_LENGTH
	global DISPLAY_TIMESTAMP
	global TIMESTAMP_FORMAT
	global CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES
	global WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW

	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			settings = json.load(read_settings)

		prepatch_length = len(settings)
		settings = patch_settings(settings)
		postpatch_length = len(settings)

		MDI_BACKGROUND_IMAGE = settings["mdi_background_image"]
		APPLICATION_FONT = settings["application_font"]
		DISPLAY_NAME = settings["display_name"]
		DISPLAY_ICON = settings["display_icon"]
		DEFAULT_SUBWINDOW_WIDTH = settings["default_subwindow_width"]
		DEFAULT_SUBWINDOW_HEIGHT = settings["default_subwindow_height"]
		COMMAND_HISTORY_LENGTH = settings["command_history_length"]
		DICTIONARY = settings["dictionary"]
		NICKNAME_PAD_LENGTH = settings["nickname_pad_length"]
		DISPLAY_TIMESTAMP = settings["display_timestamp"]
		TIMESTAMP_FORMAT = settings["timestamp_format"]
		CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES = settings["create_window_for_incoming_private_messages"]
		WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW = settings["write_private_messages_to_server_window"]

		if prepatch_length!=postpatch_length:
			save_settings(filename)
	else:
		save_settings(filename)

def check_settings(filename):
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			settings = json.load(read_settings)

			if not "mdi_background_image" in settings: return False
			if not "application_font" in settings: return False
			if not "display_name" in settings: return False
			if not "display_icon" in settings: return False
			if not "default_subwindow_width" in settings: return False
			if not "default_subwindow_height" in settings: return False
			if not "command_history_length" in settings: return False
			if not "dictionary" in settings: return False
			if not "nickname_pad_length" in settings: return False
			if not "display_timestamp" in settings: return False
			if not "timestamp_format" in settings: return False
			if not "create_window_for_incoming_private_messages" in settings: return False
			if not "write_private_messages_to_server_window" in settings: return False
	else:
		return False

	return True

def initialize(directory,directory_name):
	global CONFIG_DIRECTORY
	global CONFIG_FILE

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	CONFIG_DIRECTORY = os.path.join(directory,directory_name)
	if not os.path.isdir(CONFIG_DIRECTORY): os.mkdir(CONFIG_DIRECTORY)

	CONFIG_FILE = os.path.join(CONFIG_DIRECTORY, "config.json")