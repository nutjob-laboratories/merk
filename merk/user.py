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

CONFIG_DIRECTORY = None
USER_FILE = None

NICKNAME = ''
ALTERNATE = ''
USERNAME = ''
REALNAME = ''
LAST_HOST = ''
LAST_PORT = '6667'
LAST_SSL = False
LAST_RECONNECT = False
LAST_PASSWORD = ''
HISTORY = []
COMMANDS = {}

def save_user(filename):

	settings = {
		"nickname": NICKNAME,
		"alternate": ALTERNATE,
		"username": USERNAME,
		"realname": REALNAME,
		"last_host": LAST_HOST,
		"last_port": LAST_PORT,
		"last_ssl": LAST_SSL,
		"last_reconnect": LAST_RECONNECT,
		"last_password": LAST_PASSWORD,
		"history": HISTORY,
		"commands": COMMANDS,
	}

	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def patch_user(settings):
	if not "nickname" in settings:
		settings["nickname"] = NICKNAME
	if not "alternate" in settings:
		settings["alternate"] = ALTERNATE
	if not "username" in settings:
		settings["username"] = USERNAME
	if not "realname" in settings:
		settings["realname"] = REALNAME
	if not "last_host" in settings:
		settings["last_host"] = LAST_HOST
	if not "last_port" in settings:
		settings["last_port"] = LAST_PORT
	if not "last_ssl" in settings:
		settings["last_ssl"] = LAST_SSL
	if not "last_reconnect" in settings:
		settings["last_reconnect"] = LAST_RECONNECT
	if not "last_password" in settings:
		settings["last_password"] = LAST_PASSWORD
	if not "history" in settings:
		settings["history"] = HISTORY
	if not "commands" in settings:
		settings["commands"] = COMMANDS

	return settings

def load_user(filename):
	global NICKNAME
	global ALTERNATE
	global REALNAME
	global USERNAME
	global LAST_HOST
	global LAST_PORT
	global LAST_SSL
	global LAST_RECONNECT
	global LAST_PASSWORD
	global HISTORY
	global COMMANDS

	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			settings = json.load(read_settings)

		prepatch_length = len(settings)
		settings = patch_user(settings)
		postpatch_length = len(settings)

		NICKNAME = settings["nickname"]
		ALTERNATE = settings["alternate"]
		REALNAME = settings["realname"]
		USERNAME = settings["username"]
		LAST_HOST = settings["last_host"]
		LAST_PORT = settings["last_port"]
		LAST_SSL = settings["last_ssl"]
		LAST_RECONNECT = settings["last_reconnect"]
		LAST_PASSWORD = settings["last_password"]
		LAST_PASSWORD = settings["last_password"]
		HISTORY = settings["history"]
		COMMANDS = settings["commands"]

		if prepatch_length!=postpatch_length:
			save_user(filename)
	else:
		save_user(filename)

def initialize(directory,directory_name):
	global CONFIG_DIRECTORY
	global USER_FILE

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	CONFIG_DIRECTORY = os.path.join(directory,directory_name)
	if not os.path.isdir(CONFIG_DIRECTORY): os.mkdir(CONFIG_DIRECTORY)

	USER_FILE = os.path.join(CONFIG_DIRECTORY,"user.json")

def initialize_file(directory,directory_name,filename):
	global CONFIG_DIRECTORY
	global USER_FILE

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	CONFIG_DIRECTORY = os.path.join(directory,directory_name)
	if not os.path.isdir(CONFIG_DIRECTORY): os.mkdir(CONFIG_DIRECTORY)

	USER_FILE = filename