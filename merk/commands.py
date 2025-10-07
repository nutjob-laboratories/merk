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

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QSound

SSL_AVAILABLE = True
try:
	from twisted.internet import ssl
except ImportError as error:
	SSL_AVAILABLE = False
except Exception as exception:
	pass

import os
import time
import uuid
import re
from pathlib import Path
import fnmatch
import datetime
import subprocess
import shlex
import random
import ast

import emoji

from .resources import *
from . import config
from . import user as USER
from . import dialog

from .dialog.away import Dialog as Away

CONFIG_DIRECTORY = None
SCRIPTS_DIRECTORY = None

ALIAS = {}
TEMPORARY_ALIAS = {}
TEMPORARY_ALIAS_AUTOCOMPLETE = {}
AUTOCOMPLETE = {}
AUTOCOMPLETE_MULTI = {}
COMMAND_HELP_INFORMATION = []
HELP = None
HELP_PREFIX = None
HELP_POSTFIX = None
HELP_EPILOGUE = None
HALT_SCRIPT = []

USER_MACROS = {}

class UserMacro:
	def __init__(self,name,script):
		self.name = name
		self.script = script

def add_command(name,script):
	e = UserMacro(name,script)
	USER_MACROS[name] = e

def add_halt(script_id):
	if script_id==None: return
	if not config.HALT_SCRIPT_EXECUTION_ON_ERROR: return
	global HALT_SCRIPT

	if script_id in HALT_SCRIPT: return
	HALT_SCRIPT.append(script_id)

def is_halting(script_id):
	if config.HALT_SCRIPT_EXECUTION_ON_ERROR:
		if script_id in HALT_SCRIPT: return True
	return False

def remove_halt(script_id):
	global HALT_SCRIPT
	clean = []
	for i in HALT_SCRIPT:
		if i!=script_id: clean.append(i)
	HALT_SCRIPT = clean

def initialize(directory,directory_name):
	global SCRIPTS_DIRECTORY

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	SCRIPTS_DIRECTORY = os.path.join(directory,directory_name)
	if not os.path.isdir(SCRIPTS_DIRECTORY): os.mkdir(SCRIPTS_DIRECTORY)

def build_help_and_autocomplete(new_autocomplete=None,new_help=None):
	global AUTOCOMPLETE
	global COMMAND_HELP_INFORMATION
	global HELP
	global HELP_PREFIX
	global HELP_POSTFIX
	global HELP_EPILOGUE
	global AUTOCOMPLETE_MULTI

	# Entries for command autocomplete
	AUTOCOMPLETE_MULTI = {
			config.ISSUE_COMMAND_SYMBOL+"window maximize": config.ISSUE_COMMAND_SYMBOL+"window maximize",
			config.ISSUE_COMMAND_SYMBOL+"window minimize": config.ISSUE_COMMAND_SYMBOL+"window minimize",
			config.ISSUE_COMMAND_SYMBOL+"window restore": config.ISSUE_COMMAND_SYMBOL+"window restore",
			config.ISSUE_COMMAND_SYMBOL+"window move": config.ISSUE_COMMAND_SYMBOL+"window move ",
			config.ISSUE_COMMAND_SYMBOL+"window size": config.ISSUE_COMMAND_SYMBOL+"window size ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp time": config.ISSUE_COMMAND_SYMBOL+"ctcp TIME ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp userinfo": config.ISSUE_COMMAND_SYMBOL+"ctcp USERINFO ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp version": config.ISSUE_COMMAND_SYMBOL+"ctcp VERSION ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp source": config.ISSUE_COMMAND_SYMBOL+"ctcp SOURCE ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp finger": config.ISSUE_COMMAND_SYMBOL+"ctcp FINGER ",
	}

	# Entries for command autocomplete
	AUTOCOMPLETE = {
			config.ISSUE_COMMAND_SYMBOL+"part": config.ISSUE_COMMAND_SYMBOL+"part ",
			config.ISSUE_COMMAND_SYMBOL+"join": config.ISSUE_COMMAND_SYMBOL+"join ",
			config.ISSUE_COMMAND_SYMBOL+"notice": config.ISSUE_COMMAND_SYMBOL+"notice ",
			config.ISSUE_COMMAND_SYMBOL+"nick": config.ISSUE_COMMAND_SYMBOL+"nick ",
			config.ISSUE_COMMAND_SYMBOL+"help": config.ISSUE_COMMAND_SYMBOL+"help",
			config.ISSUE_COMMAND_SYMBOL+"topic": config.ISSUE_COMMAND_SYMBOL+"topic ",
			config.ISSUE_COMMAND_SYMBOL+"quit": config.ISSUE_COMMAND_SYMBOL+"quit",
			config.ISSUE_COMMAND_SYMBOL+"msg": config.ISSUE_COMMAND_SYMBOL+"msg ",
			config.ISSUE_COMMAND_SYMBOL+"me": config.ISSUE_COMMAND_SYMBOL+"me ",
			config.ISSUE_COMMAND_SYMBOL+"mode": config.ISSUE_COMMAND_SYMBOL+"mode ",
			config.ISSUE_COMMAND_SYMBOL+"kick": config.ISSUE_COMMAND_SYMBOL+"kick ",
			config.ISSUE_COMMAND_SYMBOL+"whois": config.ISSUE_COMMAND_SYMBOL+"whois ",
			config.ISSUE_COMMAND_SYMBOL+"whowas": config.ISSUE_COMMAND_SYMBOL+"whowas ",
			config.ISSUE_COMMAND_SYMBOL+"who": config.ISSUE_COMMAND_SYMBOL+"who ",
			config.ISSUE_COMMAND_SYMBOL+"invite": config.ISSUE_COMMAND_SYMBOL+"invite ",
			config.ISSUE_COMMAND_SYMBOL+"oper": config.ISSUE_COMMAND_SYMBOL+"oper ",
			config.ISSUE_COMMAND_SYMBOL+"away": config.ISSUE_COMMAND_SYMBOL+"away ",
			config.ISSUE_COMMAND_SYMBOL+"back": config.ISSUE_COMMAND_SYMBOL+"back",
			config.ISSUE_COMMAND_SYMBOL+"raw": config.ISSUE_COMMAND_SYMBOL+"raw ",
			config.ISSUE_COMMAND_SYMBOL+"time": config.ISSUE_COMMAND_SYMBOL+"time",
			config.ISSUE_COMMAND_SYMBOL+"version": config.ISSUE_COMMAND_SYMBOL+"version",
			config.ISSUE_COMMAND_SYMBOL+"refresh" : config.ISSUE_COMMAND_SYMBOL+"refresh",
			config.ISSUE_COMMAND_SYMBOL+"knock" : config.ISSUE_COMMAND_SYMBOL+"knock ",
			config.ISSUE_COMMAND_SYMBOL+"connect": config.ISSUE_COMMAND_SYMBOL+"connect ",
			config.ISSUE_COMMAND_SYMBOL+"connectssl": config.ISSUE_COMMAND_SYMBOL+"connectssl ",
			config.ISSUE_COMMAND_SYMBOL+"xconnect": config.ISSUE_COMMAND_SYMBOL+"xconnect ",
			config.ISSUE_COMMAND_SYMBOL+"xconnectssl": config.ISSUE_COMMAND_SYMBOL+"xconnectssl ",
			config.ISSUE_COMMAND_SYMBOL+"alias": config.ISSUE_COMMAND_SYMBOL+"alias ",
			config.ISSUE_COMMAND_SYMBOL+"unalias": config.ISSUE_COMMAND_SYMBOL+"unalias ",
			config.ISSUE_COMMAND_SYMBOL+"script" : config.ISSUE_COMMAND_SYMBOL+"script ",
			config.ISSUE_COMMAND_SYMBOL+"edit" : config.ISSUE_COMMAND_SYMBOL+"edit ",
			config.ISSUE_COMMAND_SYMBOL+"play" : config.ISSUE_COMMAND_SYMBOL+"play ",
			config.ISSUE_COMMAND_SYMBOL+"list" : config.ISSUE_COMMAND_SYMBOL+"list ",
			config.ISSUE_COMMAND_SYMBOL+"restore": config.ISSUE_COMMAND_SYMBOL+"restore ",
			config.ISSUE_COMMAND_SYMBOL+"print": config.ISSUE_COMMAND_SYMBOL+"print ",
			config.ISSUE_COMMAND_SYMBOL+"maximize": config.ISSUE_COMMAND_SYMBOL+"maximize ",
			config.ISSUE_COMMAND_SYMBOL+"minimize": config.ISSUE_COMMAND_SYMBOL+"minimize ",
			config.ISSUE_COMMAND_SYMBOL+"cascade": config.ISSUE_COMMAND_SYMBOL+"cascade",
			config.ISSUE_COMMAND_SYMBOL+"tile": config.ISSUE_COMMAND_SYMBOL+"tile",
			config.ISSUE_COMMAND_SYMBOL+"clear": config.ISSUE_COMMAND_SYMBOL+"clear",
			config.ISSUE_COMMAND_SYMBOL+"settings": config.ISSUE_COMMAND_SYMBOL+"settings",
			config.ISSUE_COMMAND_SYMBOL+"style": config.ISSUE_COMMAND_SYMBOL+"style",
			config.ISSUE_COMMAND_SYMBOL+"log": config.ISSUE_COMMAND_SYMBOL+"log",
			config.ISSUE_COMMAND_SYMBOL+"exit": config.ISSUE_COMMAND_SYMBOL+"exit ",
			config.ISSUE_COMMAND_SYMBOL+"config": config.ISSUE_COMMAND_SYMBOL+"config ",
			config.ISSUE_COMMAND_SYMBOL+"ignore": config.ISSUE_COMMAND_SYMBOL+"ignore ",
			config.ISSUE_COMMAND_SYMBOL+"unignore": config.ISSUE_COMMAND_SYMBOL+"unignore ",
			config.ISSUE_COMMAND_SYMBOL+"find": config.ISSUE_COMMAND_SYMBOL+"find ",
			config.ISSUE_COMMAND_SYMBOL+"ping": config.ISSUE_COMMAND_SYMBOL+"ping ",
			config.ISSUE_COMMAND_SYMBOL+"shell": config.ISSUE_COMMAND_SYMBOL+"shell ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp": config.ISSUE_COMMAND_SYMBOL+"ctcp ",
			config.ISSUE_COMMAND_SYMBOL+"private": config.ISSUE_COMMAND_SYMBOL+"private ",
			config.ISSUE_COMMAND_SYMBOL+"msgbox": config.ISSUE_COMMAND_SYMBOL+"msgbox ",
			config.ISSUE_COMMAND_SYMBOL+"reclaim": config.ISSUE_COMMAND_SYMBOL+"reclaim ",
			config.ISSUE_COMMAND_SYMBOL+"next": config.ISSUE_COMMAND_SYMBOL+"next",
			config.ISSUE_COMMAND_SYMBOL+"previous": config.ISSUE_COMMAND_SYMBOL+"previous",
			config.ISSUE_COMMAND_SYMBOL+"delay": config.ISSUE_COMMAND_SYMBOL+"delay ",
			config.ISSUE_COMMAND_SYMBOL+"hide": config.ISSUE_COMMAND_SYMBOL+"hide ",
			config.ISSUE_COMMAND_SYMBOL+"show": config.ISSUE_COMMAND_SYMBOL+"show ",
			config.ISSUE_COMMAND_SYMBOL+"window": config.ISSUE_COMMAND_SYMBOL+"window",
			config.ISSUE_COMMAND_SYMBOL+"close": config.ISSUE_COMMAND_SYMBOL+"close ",
			config.ISSUE_COMMAND_SYMBOL+"random": config.ISSUE_COMMAND_SYMBOL+"random ",
			config.ISSUE_COMMAND_SYMBOL+"prints": config.ISSUE_COMMAND_SYMBOL+"prints ",
			config.ISSUE_COMMAND_SYMBOL+"quitall": config.ISSUE_COMMAND_SYMBOL+"quitall",
			config.ISSUE_COMMAND_SYMBOL+"fullscreen": config.ISSUE_COMMAND_SYMBOL+"fullscreen",
			config.ISSUE_COMMAND_SYMBOL+"resize": config.ISSUE_COMMAND_SYMBOL+"resize ",
			config.ISSUE_COMMAND_SYMBOL+"move": config.ISSUE_COMMAND_SYMBOL+"move ",
			config.ISSUE_COMMAND_SYMBOL+"focus": config.ISSUE_COMMAND_SYMBOL+"focus ",
			config.ISSUE_COMMAND_SYMBOL+"reconnect": config.ISSUE_COMMAND_SYMBOL+"reconnect ",
			config.ISSUE_COMMAND_SYMBOL+"reconnectssl": config.ISSUE_COMMAND_SYMBOL+"reconnectssl ",
			config.ISSUE_COMMAND_SYMBOL+"xreconnect": config.ISSUE_COMMAND_SYMBOL+"xreconnect ",
			config.ISSUE_COMMAND_SYMBOL+"xreconnectssl": config.ISSUE_COMMAND_SYMBOL+"xreconnectssl ",
			config.ISSUE_COMMAND_SYMBOL+"user": config.ISSUE_COMMAND_SYMBOL+"user ",
			config.ISSUE_COMMAND_SYMBOL+"macro": config.ISSUE_COMMAND_SYMBOL+"macro ",
		}

	# Remove the style command if the style editor is turned off 
	if not config.ENABLE_STYLE_EDITOR:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"style",'')

	if not config.ENABLE_ALIASES:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"alias",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"unalias",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"shell",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"random",'')

	if not config.SCRIPTING_ENGINE_ENABLED:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"script",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"edit",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"macro",'')

	if not config.ENABLE_SHELL_COMMAND:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"shell",'')

	if not config.ENABLE_DELAY_COMMAND:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"delay",'')

	if not config.ENABLE_CONFIG_COMMAND:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"config",'')

	if not config.ENABLE_USER_COMMAND:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"user",'')

	if not SSL_AVAILABLE:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"connectssl",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"xconnectssl",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"reconnectssl",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"xreconnectssl",'')

	if config.INCLUDE_SCRIPT_COMMAND_SHORTCUT:
		AUTOCOMPLETE[config.ISSUE_COMMAND_SYMBOL+"s"] = config.ISSUE_COMMAND_SYMBOL+"s "

	if new_autocomplete!=None:
		if isinstance(new_autocomplete, list):
			for a in new_autocomplete:
				AUTOCOMPLETE.update(a)
		else:
			AUTOCOMPLETE.update(new_autocomplete)

	# The command help system
	COMMAND_HELP_INFORMATION = [
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"help [COMMAND]</b>", "Displays command usage information" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"me MESSAGE...</b>", "Sends a CTCP action message to the current chat" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"me TARGET MESSAGE...</b>", "Sends a CTCP action message to a chat, only callable from server windows" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"msg TARGET MESSAGE...</b>", "Sends a message" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"notice TARGET MESSAGE...</b>", "Sends a notice" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]</b>", "Joins a channel" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"part CHANNEL [MESSAGE]</b>", "Leaves a channel" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"nick NEW_NICKNAME</b>", "Changes your nickname" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC</b>", "Sets a channel topic" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"mode TARGET MODE...</b>", "Sets a mode on a channel or user" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"invite USER CHANNEL</b>", "Sends a channel invitation" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"kick CHANNEL USER [MESSAGE]</b>", "Kicks a user from a channel" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"whois USER [SERVER]</b>", "Requests user information from the server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"who USER [o]</b>", "Requests user information from the server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"whowas USER [COUNT] [SERVER]</b>", "Requests information about previously connected users" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"quit [MESSAGE]</b>", "Disconnects from the current IRC server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"oper USERNAME PASSWORD</b>", "Logs into an operator account" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"away [MESSAGE]</b>", "Sets status as \"away\"" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"back</b>", "Sets status as \"back\"" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"raw TEXT...</b>", "Sends unprocessed data to the server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"time</b>", "Requests server time" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"version [SERVER]</b>", "Requests server version" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"list [TERMS]</b>", "Lists or searches channels on the server; use \"*\" for multi-character wildcard, \"?\" for single character" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"refresh</b>", "Requests a new list of channels from the server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"knock CHANNEL [MESSAGE]</b>", "Requests an invitation to a channel" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"connect SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"connectssl SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server via SSL" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"xconnect SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server & executes connection script" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"xconnectssl SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server via SSL & executes connection script" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"script FILENAME [ARGUMENTS]</b>", "Executes a list of commands in a file" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"settings</b>", "Opens the settings dialog" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"style</b>", "Edits the current window's style" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"log</b>", "Opens the log manager" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"alias [TOKEN] [TEXT...]</b>", "Creates an alias that can be referenced by "+config.ALIAS_INTERPOLATION_SYMBOL+"TOKEN" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"unalias TOKEN</b>", "Deletes the alias referenced by "+config.ALIAS_INTERPOLATION_SYMBOL+"TOKEN" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"edit [FILENAME]</b>", "Opens a script in the editor" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"play FILENAME</b>", "Plays a WAV file" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"print [WINDOW] TEXT...</b>", "Prints text to a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"maximize [SERVER] [WINDOW]</b>", "Maximizes a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"minimize [SERVER] [WINDOW]</b>", "Minimizes a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"restore [SERVER] [WINDOW]</b>", "Restores a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"cascade</b>", "Cascades all subwindows" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"tile</b>", "Tiles all subwindows" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"clear [SERVER] [WINDOW]</b>", "Clears a window's chat display" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"exit [SECONDS]</b>", "Exits the client, with an optional pause of SECONDS before exit" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"config [SETTING] [VALUE...]</b>", "Changes a setting, or displays one or all settings in the configuration file. <i><b>Caution</b>: use at your own risk</i>" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"ignore USER</b>", "Hides a user's chat. USER can be a nickname or hostmask" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"unignore USER</b>", "Un-hides a user's chat. To un-hide all users, use * as the argument" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"find [TERMS]</b>", "Finds filenames that can be found by other commands; use * for multi-character wildcards, and ? for single character wildcards" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"ping USER [TEXT]</b>", "Sends a CTCP ping to a user" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"shell ALIAS COMMAND...</b>", "Executes an external program, and stores the output in an alias" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"ctcp REQUEST USER</b>", "Sends a CTCP request; valid requests are TIME, VERSION, USERINFO, SOURCE, or FINGER" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"private NICKNAME [MESSAGE]</b>", "Opens a private chat window for NICKNAME" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"msgbox MESSAGE...</b>", "Displays a messagebox with a short message" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"reclaim NICKNAME</b>", "Attempts to change nickname to NICKNAME until claimed" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"next</b>", "Shifts focus to the \"next\" subwindow" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"previous</b>", "Shifts focus to the \"previous\" subwindow" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"delay SECONDS COMMAND...</b>", "Executes COMMAND after SECONDS seconds" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"hide [SERVER] [WINDOW]</b>", "Hides a subwindow" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"show [SERVER] [WINDOW]</b>", "Shows a subwindow, if hidden; otherwise, shifts focus to that window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"window [COMMAND] [X] [Y]</b>", "Manipulates the main application window. Valid commands are <b>move</b>, <b>size</b>, <b>maximize</b>, <b>minimize</b>, and <b>restore</b>" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"close [SERVER] [WINDOW]</b>", "Closes a subwindow" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"random ALIAS LOW HIGH</b>", "Generates a random number between LOW and HIGH and stores it in ALIAS" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"prints [WINDOW]</b>", "Prints a system message to a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"quitall [MESSAGE]</b>", "Disconnects from all IRC servers" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"fullscreen</b>", "Toggles full screen mode" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"resize [SERVER] [WINDOW] WIDTH HEIGHT</b>", "Resizes a subwindow" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"move [SERVER] [WINDOW] X Y</b>", "Moves a subwindow" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"focus [SERVER] [WINDOW]</b>", "Sets focus on a subwindow" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"reconnect SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server, reconnecting on disconnection" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"reconnectssl SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server via SSL, reconnecting on disconnection" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"xreconnect SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server & executes connection script, reconnecting on disconnection" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"xreconnectssl SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server via SSL & executes connection script, reconnecting on disconnection" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"user [SETTING] [VALUE...]</b>", "Changes a setting, or displays one or all settings in the user configuration file. <i><b>Caution</b>: use at your own risk</i>" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"macro NAME SCRIPT...</b>", "Creates a macro, executable with "+config.ISSUE_COMMAND_SYMBOL+"NAME, that executes SCRIPT" ],
	]

	if config.INCLUDE_SCRIPT_COMMAND_SHORTCUT:
		COMMAND_HELP_INFORMATION.append(["<b>"+config.ISSUE_COMMAND_SYMBOL+"s FILENAME [ARGUMENTS]</b>", f"Shortcut for the {config.ISSUE_COMMAND_SYMBOL}script command"])

	if config.SCRIPTING_ENGINE_ENABLED:
		for m in USER_MACROS:
			name = USER_MACROS[m].name
			script = USER_MACROS[m].script
			COMMAND_HELP_INFORMATION.append([ "<b>"+config.ISSUE_COMMAND_SYMBOL+name+"</b>", f"Executes script \"{script}\"" ])

	COPY = []
	for e in COMMAND_HELP_INFORMATION:
		if not config.ENABLE_USER_COMMAND:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"user [SETTING] [VALUE...]</b>": continue
		if not config.ENABLE_CONFIG_COMMAND:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"config [SETTING] [VALUE...]</b>": continue
		if not config.ENABLE_DELAY_COMMAND:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"delay SECONDS COMMAND...</b>": continue
		if not config.ENABLE_STYLE_EDITOR:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"style</b>": continue
		if not config.ENABLE_ALIASES:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"alias [TOKEN] [TEXT...]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"unalias TOKEN</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"shell ALIAS COMMAND...</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"random ALIAS LOW HIGH</b>": continue
		if not config.SCRIPTING_ENGINE_ENABLED:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"script FILENAME</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"edit [FILENAME]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"s FILENAME [ARGUMENTS]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"macro NAME SCRIPT...</b>": continue
		if not config.ENABLE_SHELL_COMMAND:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"shell ALIAS COMMAND...</b>": continue
		if not SSL_AVAILABLE:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"connectssl SERVER [PORT] [PASSWORD]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"xconnectssl SERVER [PORT] [PASSWORD]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"reconnectssl SERVER [PORT] [PASSWORD]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"xreconnectssl SERVER [PORT] [PASSWORD]</b>": continue

		COPY.append(e)
	COMMAND_HELP_INFORMATION = sorted(COPY)

	if new_help!=None:
		if isinstance(new_help, list):
			for i in new_help:
				COMMAND_HELP_INFORMATION.append(i)
		else:
			COMMAND_HELP_INFORMATION.append(new_help)

	global HELP_DISPLAY_TEMPLATE
	if config.AUTOCOMPLETE_COMMANDS:
		HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_AUTOCOMPLETE_%","Command autocomplete is turned on; to use autocomplete, type the first few characters of a command and press the \"tab\" key to complete the command.")
	else:
		HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_AUTOCOMPLETE_%","Command autocomplete is turned off.")

	if HELP_PREFIX!=None:
		HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_PREFIX_%","<tr><td><small>"+HELP_PREFIX+"</small></td></tr>")
	else:
		HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_PREFIX_%","")

	if HELP_POSTFIX!=None:
		HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_POSTFIX_%","<tr><td><small>"+HELP_POSTFIX+"</small></td></tr>")
	else:
		HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_POSTFIX_%","")

	if HELP_EPILOGUE!=None:
		HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_ENDING_%","<tr><td>&nbsp;</center></td></tr><tr><td><small>"+HELP_EPILOGUE+"</small></td></tr>")
	else:
		HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_ENDING_%","")

	hdisplay = []
	for e in COMMAND_HELP_INFORMATION:
		t = HELP_ENTRY_TEMPLATE
		t = t.replace("%_USAGE_%",e[0])
		t = t.replace("%_DESCRIPTION_%",e[1])
		hdisplay.append(t)
	help_display = HELP_DISPLAY_TEMPLATE.replace("%_LIST_%","\n".join(hdisplay))

	HELP = Message(RAW_SYSTEM_MESSAGE,'',help_display)

build_help_and_autocomplete()

def addTemporaryAlias(name,value):
	global TEMPORARY_ALIAS

	TEMPORARY_ALIAS[name] = value
	TEMPORARY_ALIAS_AUTOCOMPLETE[name] = ''

def addAlias(name,value):
	global ALIAS
	ALIAS[name] = value

def removeAlias(name):
	global ALIAS
	if len(name)>0:
		if name[0]=="_": return False
	if name in ALIAS:
		ALIAS.pop(name,'')
		return True
	return False

def detect_alias(text):
	# Make sure the alias symbol is properly escaped
	aliassymbol = ''
	for c in config.ALIAS_INTERPOLATION_SYMBOL:
		if c in ['\\','^','$','.','|','?','*','+','(',')','{']:
			c = '\\'+c
		aliassymbol = aliassymbol + c
	pattern = fr"{aliassymbol}([^\d]+)"

	match = re.search(pattern, text)
	return bool(match)

def interpolateAliases(text):
	if not config.ENABLE_ALIASES: return text
	if not detect_alias(text): return text
	counter = 0
	while detect_alias(text):
		for a in ALIAS:
			text = text.replace(config.ALIAS_INTERPOLATION_SYMBOL+a,ALIAS[a])
		counter = counter + 1
		if counter>=99: break

	counter = 0
	while detect_alias(text):
		for a in TEMPORARY_ALIAS:
			text = text.replace(config.ALIAS_INTERPOLATION_SYMBOL+a,TEMPORARY_ALIAS[a])
		counter = counter + 1
		if counter>=99: break

	if config.ENABLE_EMOJI_SHORTCODES: text = emoji.emojize(text,language=config.EMOJI_LANGUAGE)

	return text

def clearTemporaryAliases():
	global TEMPORARY_ALIAS
	TEMPORARY_ALIAS = {}

def buildTemporaryAliases(gui,window):

	if not config.ENABLE_ALIASES: return
	if not config.ENABLE_BUILT_IN_ALIASES: return

	timestamp = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime(config.TIMESTAMP_FORMAT)
	mytime = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime("%H:%M:%S")
	mydate = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%m/%d/%Y')
	myedate = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%d/%m/%Y')
	day = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%A')
	month = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%B')
	year = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%Y')
	ordinal = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%d')

	addTemporaryAlias('_CLIENT',APPLICATION_NAME)
	if window.client.kwargs["ssl"]:
		addTemporaryAlias('_CONNECTION',"SSL/TLS")
	else:
		addTemporaryAlias('_CONNECTION',"TCP/IP")
	if window.window_type==CHANNEL_WINDOW:
		addTemporaryAlias('_COUNT',f"{len(window.nicks)}")
	else:
		addTemporaryAlias('_COUNT',f"0")
	addTemporaryAlias('_CUPTIME',str(gui.client_uptime))
	if hasattr(window.client,"hostname"):
		addTemporaryAlias('_HOST',window.client.hostname)
	else:
		addTemporaryAlias('_HOST',window.client.server+":"+str(window.client.port))
	addTemporaryAlias('_DATE',mydate)
	addTemporaryAlias('_DAY',day)
	addTemporaryAlias('_EDATE',myedate)
	addTemporaryAlias('_EPOCH',f"{datetime.timestamp(datetime.now())}")
	if window.client.usermodes!='':
		addTemporaryAlias('_MODE',window.client.usermodes)
	else:
		addTemporaryAlias('_MODE','none')
	addTemporaryAlias('_MONTH',month)
	if hasattr(window.client,"network"):
		if window.client.network:
			addTemporaryAlias('_NETWORK',window.client.network)
		else:
			addTemporaryAlias('_NETWORK',"unknown")
	else:
		addTemporaryAlias('_NETWORK',"unknown")
	addTemporaryAlias('_NICKNAME',window.client.nickname)
	addTemporaryAlias('_ORDINAL',ordinal)
	addTemporaryAlias('_PORT',str(window.client.port))
	if window.window_type==CHANNEL_WINDOW:
		addTemporaryAlias('_PRESENT',",".join(window.nicks))
	else:
		addTemporaryAlias('_PRESENT','none')
	addTemporaryAlias('_REALNAME',window.client.realname)
	addTemporaryAlias('_RELEASE',APPLICATION_RELEASE)
	addTemporaryAlias('_RVERSION',APPLICATION_RELEASE_VERSION)
	if window.client.actual_server_channel_count==0:
		if window.client.server_channel_count==0:
			addTemporaryAlias('_SCHANNELS',"0")
			addTemporaryAlias('_HCHANNELS',"0")
		else:
			addTemporaryAlias('_SCHANNELS',f"{window.client.server_channel_count}")
			addTemporaryAlias('_HCHANNELS',"0")
	else:
		diff = window.client.actual_server_channel_count - window.client.server_channel_count
		if window.client.server_channel_count==0:
			addTemporaryAlias('_SCHANNELS',f"{window.client.actual_server_channel_count}")
			addTemporaryAlias('_HCHANNELS',"0")
		else:
			addTemporaryAlias('_SCHANNELS',f"{window.client.server_channel_count}")
			addTemporaryAlias('_HCHANNELS',f"{diff}")
	if window.client.server_user_count==0:
		addTemporaryAlias('_SCOUNT',"0")
	else:
		addTemporaryAlias('_SCOUNT',f"{window.client.server_user_count}")
	addTemporaryAlias('_SERVER',window.client.server)
	if window.client.server_software:
		addTemporaryAlias('_SOFTWARE',f"{window.client.server_software}")
	else:
		addTemporaryAlias('_SOFTWARE',"unknown")
	addTemporaryAlias('_SOURCE',APPLICATION_SOURCE)
	if window.window_type==CHANNEL_WINDOW:
		if window.operator:
			addTemporaryAlias('_STATUS',"operator")
		elif window.voiced:
			addTemporaryAlias('_STATUS',"voiced")
		elif window.owner:
			addTemporaryAlias('_STATUS',"owner")
		elif window.admin:
			addTemporaryAlias('_STATUS',"admin")
		elif window.halfop:
			addTemporaryAlias('_STATUS',"halfop")
		elif window.protected:
			addTemporaryAlias('_STATUS',"protected")
		else:
			addTemporaryAlias('_STATUS',"normal")
	else:
		addTemporaryAlias('_STATUS',"normal")
	addTemporaryAlias('_STAMP',timestamp)
	addTemporaryAlias('_SUPTIME',str(window.client.uptime))
	addTemporaryAlias('_TIME',mytime)
	if window.window_type==CHANNEL_WINDOW:
		if window.channel_topic!='':
			addTemporaryAlias('_TOPIC',window.channel_topic)
		else:
			addTemporaryAlias('_TOPIC','No topic')
	else:
		addTemporaryAlias('_TOPIC','No topic')
	if hasattr(window,"uptime"):
		addTemporaryAlias('_UPTIME',str(window.uptime))
	else:
		addTemporaryAlias('_UPTIME',"0")
	addTemporaryAlias('_VERSION',APPLICATION_VERSION)
	addTemporaryAlias('_USERNAME',window.client.username)
	addTemporaryAlias('_WINDOW',window.name)
	if window.window_type==SERVER_WINDOW:
		addTemporaryAlias('_WINDOW_TYPE',"server")
	elif window.window_type==CHANNEL_WINDOW:
		addTemporaryAlias('_WINDOW_TYPE',"channel")
	elif window.window_type==PRIVATE_WINDOW:
		addTemporaryAlias('_WINDOW_TYPE',"private")
	else:
		addTemporaryAlias('_WINDOW_TYPE',"unknown")
	addTemporaryAlias('_YEAR',year)

def handleChatCommands(gui,window,user_input):
	buildTemporaryAliases(gui,window)

	user_input = interpolateAliases(user_input)
	retval = executeChatCommands(gui,window,user_input,False)
	clearTemporaryAliases()
	return retval

def handleCommonCommands(gui,window,user_input):
	buildTemporaryAliases(gui,window)

	user_input = interpolateAliases(user_input)
	retval = executeCommonCommands(gui,window,user_input,False)
	clearTemporaryAliases()
	return retval

def handleScriptCommands(gui,window,user_input,line_number,script_id):
	buildTemporaryAliases(gui,window)

	user_input = interpolateAliases(user_input)

	if window.window_type!=SERVER_WINDOW:
		if executeChatCommands(gui,window,user_input,True,line_number,script_id):
			clearTemporaryAliases()
			return True

	retval = executeCommonCommands(gui,window,user_input,True,line_number,script_id)
	clearTemporaryAliases()
	return retval

def check_readable(file):
	if os.path.exists(file) and os.access(file, os.R_OK):
		return file
	else:
		return None

def find_file(filename,extension):

	# Check if it's a complete filename
	if os.path.isfile(filename): return check_readable(filename)

	# Look for the script in the scripts directory
	if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, filename)): return check_readable(os.path.join(SCRIPTS_DIRECTORY, filename))

	# Look for the script in the config directory
	if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, filename)): return check_readable(os.path.join(config.CONFIG_DIRECTORY, filename))

	# Look for the script in the install directory
	if os.path.isfile(os.path.join(INSTALL_DIRECTORY, filename)): return check_readable(os.path.join(INSTALL_DIRECTORY, filename))

	if extension!=None:
		efilename = filename + "." + extension

		# Check if it's a complete filename
		if os.path.isfile(efilename): return check_readable(filename)

		# Look for the script in the scripts directory
		if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, efilename)): return check_readable(os.path.join(SCRIPTS_DIRECTORY, efilename))

		# Look for the script in the config directory
		if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, efilename)): return check_readable(os.path.join(config.CONFIG_DIRECTORY, efilename))

		# Look for the script in the install directory
		if os.path.isfile(os.path.join(INSTALL_DIRECTORY, efilename)): return check_readable(os.path.join(INSTALL_DIRECTORY, efilename))

		# Still not found? Case insensitive seach
		for root, dirs, files in os.walk(SCRIPTS_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.{extension}"):
				return check_readable(os.path.join(root, filename))

		for root, dirs, files in os.walk(config.CONFIG_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.{extension}"):
				return check_readable(os.path.join(root, filename))

		for root, dirs, files in os.walk(INSTALL_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.{extension}"):
				return check_readable(os.path.join(root, filename))

	for root, dirs, files in os.walk(SCRIPTS_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return check_readable(os.path.join(root, filename))

	for root, dirs, files in os.walk(config.CONFIG_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return check_readable(os.path.join(root, filename))

	for root, dirs, files in os.walk(INSTALL_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return check_readable(os.path.join(root, filename))

	return None

def is_valid_macro_name(name):
	for c in AUTOCOMPLETE:
		if c.lower()==config.ISSUE_COMMAND_SYMBOL+name: return False
	return True

def is_macro_name(name):
	for c in USER_MACROS:
		if USER_MACROS[c].name.lower()==name: return True
	return False

def execute_script_line(data):
	gui = data[0]
	window = data[1]
	script_id = data[2]
	line = data[3]
	line_number = data[4]
	script_only_command = data[5]

	if is_halting(script_id): return

	if not handleScriptCommands(gui,window,line,line_number,script_id):
		if len(line.strip())==0: return

		tokens = line.split()
		if len(tokens)>0:
			if len(tokens)==1:
				if tokens[0].lower()=='end':
					add_halt(script_id)
					return
			else:
				if tokens[1].lower()=='end':
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: end called with too many arguments")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return

		if config.DISPLAY_SCRIPT_ERRORS:
			# Check to make sure this isn't being thrown by script
			# only commands
			if not script_only_command:
				if line[0]==config.ISSUE_COMMAND_SYMBOL:
					add_halt(script_id)
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Unrecognized command \"{line}\"")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					add_halt(script_id)
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Line \"{line}\" contains no command")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

def execute_script_error(data):
	gui = data[0]
	window = data[1]
	line = data[2]

	if config.DISPLAY_SCRIPT_ERRORS:
		t = Message(ERROR_MESSAGE,'',line)
		window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

def execute_script_end(data):
	gui = data[0]
	script_id = data[1]

	del gui.scripts[script_id]
	remove_halt(script_id)

def executeScript(gui,window,text,filename=None):

	script_id = str(uuid.uuid4())
	gui.scripts[script_id] = ScriptThread(text,script_id,gui,window,[],filename)
	gui.scripts[script_id].execLine.connect(execute_script_line)
	gui.scripts[script_id].scriptEnd.connect(execute_script_end)
	gui.scripts[script_id].scriptError.connect(execute_script_error)
	gui.scripts[script_id].start()

def connect_to_irc(gui,window,host,port=6667,password=None,ssl=False,reconnect=False,execute=False):
	try:
		port = int(port)
	except:
		t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
		window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
		return True
	USER.load_user(USER.USER_FILE)
	i = ConnectInfo(
		USER.NICKNAME,
		USER.ALTERNATE,
		USER.USERNAME,
		USER.REALNAME,
		host,
		port,
		password,
		reconnect,
		ssl,
		execute, # execute script
	)
	gui.connectToIrc(i)

def exit_from_command(gui):
	gui.close()

def check_for_sane_values(setting,value):

	if setting=="qt_window_style":
		if not value in QStyleFactory.keys(): return INVALID_STYLE

	if setting=="windowbar_justify":
		if value.lower()!="left" and value.lower()!="right" and value.lower()!="center": return INVALID_JUSTIFY

	if setting=="menubar_justify":
		if value.lower()!="left" and value.lower()!="right" and value.lower()!="center": return INVALID_JUSTIFY

	if setting=="syntax_nickname_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="syntax_emoji_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="syntax_alias_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="syntax_background_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="syntax_foreground_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="syntax_channel_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="syntax_command_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="syntax_comment_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="spellcheck_underline_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="syntax_script_only_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="syntax_operator_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="default_spellcheck_language":
		v = ["en","fr","es","de","pt","it","nl","ru"]
		if not value.lower() in v: return INVALID_LANGUAGE

	v = ["bold","italic"]
	if setting=="syntax_comment_style":
		if not value.lower() in v: return INVALID_TEXT_STYLE

	if setting=="syntax_command_style":
		if not value.lower() in v: return INVALID_TEXT_STYLE

	if setting=="syntax_channel_style":
		if not value.lower() in v: return INVALID_TEXT_STYLE

	if setting=="syntax_alias_style":
		if not value.lower() in v: return INVALID_TEXT_STYLE

	if setting=="syntax_script_only_style":
		if not value.lower() in v: return INVALID_TEXT_STYLE

	v = ["creation","stacking","activation"]
	if setting=="subwindow_order":
		if not value.lower() in v: return INVALID_ORDER

	return ALL_VALID_SETTINGS

def list_scripts():
	file_paths = []
	for root, _, files in os.walk(SCRIPTS_DIRECTORY):
		for file in files:
			file_paths.append(os.path.basename(os.path.join(root, file)))
	file_paths = list(set(file_paths))
	return file_paths

def list_files():
	file_paths = []
	for root, _, files in os.walk(SCRIPTS_DIRECTORY):
		for file in files:
			file_paths.append(os.path.join(root, file))
	for root, _, files in os.walk(CONFIG_DIRECTORY):
		for file in files:
			file_paths.append(os.path.join(root, file))
	for root, _, files in os.walk(INSTALL_DIRECTORY):
		for file in files:
			file_paths.append(os.path.join(root, file))
	file_paths = list(set(file_paths))
	return file_paths

def mssleep(milliseconds):
	time.sleep(milliseconds * 0.001)

def math(statement):
	try:
		# Parse the expression into an AST
		tree = ast.parse(statement, mode='eval')
		evaluator = MathEvaluator()
		result = evaluator.visit(tree)
		return [result,False]
	except (SyntaxError, TypeError, ValueError) as e:
		return [e,True]

def executeChatCommands(gui,window,user_input,is_script,line_number=0,script_id=None):
	user_input = user_input.strip()
	tokens = user_input.split()

	if is_script:
		if script_id!=None:
			if is_halting(script_id): return True

	# |---------|
	# | exclude |
	# |---------|
	if not is_script:
		if len(tokens)>=1:
			if tokens[0].lower()=='exclude':
				t = Message(ERROR_MESSAGE,'',"exclude can only be called from scripts")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |--------|
	# | insert |
	# |--------|
	if not is_script:
		if len(tokens)>=1:
			if tokens[0].lower()=='insert':
				t = Message(ERROR_MESSAGE,'',"insert can only be called from scripts")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |-------|
	# | usage |
	# |-------|
	if not is_script:
		if len(tokens)>=1:
			if tokens[0].lower()=='usage':
				t = Message(ERROR_MESSAGE,'',"usage can only be called from scripts")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |------|
	# | only |
	# |------|
	if not is_script:
		if len(tokens)>=1:
			if tokens[0].lower()=='only':
				t = Message(ERROR_MESSAGE,'',"only can only be called from scripts")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |----------|
	# | restrict |
	# |----------|
	if not is_script:
		if len(tokens)>=1:
			if tokens[0].lower()=='restrict':
				t = Message(ERROR_MESSAGE,'',"restrict can only be called from scripts")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |-----|
	# | end |
	# |-----|
	if not is_script:
		if len(tokens)>=1:
			if tokens[0].lower()=='end':
				t = Message(ERROR_MESSAGE,'',"end can only be called from scripts")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |---------|
	# | context |
	# |---------|
	if not is_script:
		if len(tokens)>=1:
			if tokens[0].lower()=='context':
				t = Message(ERROR_MESSAGE,'',"context can only be called from scripts")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |------|
	# | wait |
	# |------|
	if not is_script:
		if len(tokens)>=1:
			if tokens[0].lower()=='wait':
				t = Message(ERROR_MESSAGE,'',"wait can only be called from scripts")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |--------|
	# | /close |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'close' and len(tokens)==1:
			w = gui.getSubWindow(window.name,window.client)
			w.close()
			gui.buildWindowbar()
			return True

	# |-------|
	# | /show |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'show' and len(tokens)==1:
			w = gui.getSubWindow(window.name,window.client)
			w.show()
			gui.buildWindowbar()
			return True

	# |-------|
	# | /hide |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'hide' and len(tokens)==1:
			w = gui.getSubWindow(window.name,window.client)
			w.hide()
			gui.buildWindowbar()
			return True

	# |--------|
	# | /clear |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'clear' and len(tokens)==1:
			window.clearChat()
			return True

	# |---------|
	# | /invite |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'invite' and len(tokens)==2:
			if window.name[:1]=='#' or window.name[:1]=='&' or window.name[:1]=='!' or window.name[:1]=='+':
				tokens.pop(0)
				user = tokens.pop(0)
				window.client.sendLine("INVITE "+user+" "+window.name)
				return True
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: You can't invite a user to a private chat")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"You can't invite a user to a private chat")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |-------|
	# | /kick |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'kick' and len(tokens)>=2:
			tokens.pop(0)
			if tokens[0][:1]=='#':
				# It's a channel, so do nothing; this will be handled
				# by handleCommonCommands()
				pass
			else:
				# If the current window is a channel, try to set the mode
				# on that channel; if not, then this will be handled
				# by handleCommonCommands()
				if window.name[:1]=='#' or window.name[:1]=='&' or window.name[:1]=='!' or window.name[:1]=='+':
					channel = window.name
					target = tokens.pop(0)
					msg = ' '.join(tokens)
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					if len(msg.strip())==0: msg = None
					window.client.kick(channel,target,msg)
					return True
				else:
					pass

	# |-------|
	# | /mode |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'mode' and len(tokens)>=2:
			tokens.pop(0)
			if tokens[0][:1]=='#':
				# It's a channel, so do nothing; this will be handled
				# by handleCommonCommands()
				pass
			else:
				# If the current window is a channel, try to set the mode
				# on that channel; if not, then this will be handled
				# by handleCommonCommands()
				if window.name[:1]=='#' or window.name[:1]=='&' or window.name[:1]=='!' or window.name[:1]=='+':
					target = window.name
					mode = ' '.join(tokens)
					window.client.sendLine("MODE "+target+" "+mode)
					return True
				else:
					pass

	# |-----|
	# | /me |
	# |-----|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'me' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			window.client.describe(window.name,msg)
			t = Message(ACTION_MESSAGE,window.client.nickname,msg)
			window.writeText(t)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'me':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"me MESSAGE")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"me MESSAGE")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /topic |
	# |--------|
	# The version of the command allows the user to omit the
	# channel name in the command, much like with /part
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'topic' and len(tokens)>=2:
			tokens.pop(0)
			if tokens[0][:1]=='#' or tokens[0][:1]=='&' or tokens[0][:1]=='!' or tokens[0][:1]=='+':
				# It's a channel, so do nothing; this will be handled
				# by handleCommonCommands()
				pass
			else:
				# Check to make sure that we're trying to set a topic on
				# a channel window and not a private message window
				if window.name[:1]=='#' or window.name[:1]=='&' or window.name[:1]=='!' or window.name[:1]=='+':
					channel = window.name
					msg = ' '.join(tokens)
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					window.client.topic(channel,msg)
					return True
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Can't set topic for a private chat")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Can't set topic for a private message")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
	
	# |-------|
	# | /part |
	# |-------|
	# This version of the command allows the user to omit the channel
	# name in the command, with the channel name being the name of
	# the chat window it was issued from
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)==1:
			channel = window.name
			if config.ENABLE_EMOJI_SHORTCODES:
				msg = emoji.emojize(config.DEFAULT_QUIT_MESSAGE,language=config.EMOJI_LANGUAGE)
			else:
				msg = config.DEFAULT_QUIT_MESSAGE
			if config.INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE:
				buildTemporaryAliases(gui,window)
				msg = interpolateAliases(msg)
			window.client.leave(channel,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)>=2:
			tokens.pop(0)
			if tokens[0][:1]=='#' or tokens[0][:1]=='&' or tokens[0][:1]=='!' or tokens[0][:1]=='+':
				# It's a channel, so do nothing; this will be handled
				# by handleCommonCommands()
				pass
			else:
				# Channel name hasn't been passed, it must be a message
				channel = window.name
				msg = ' '.join(tokens)
				if config.ENABLE_EMOJI_SHORTCODES:  msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
				if config.INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE:
					buildTemporaryAliases(gui,window)
					msg = interpolateAliases(msg)
				window.client.leave(channel,msg)
				return True

	return False

def executeCommonCommands(gui,window,user_input,is_script,line_number=0,script_id=None):
	user_input = user_input.strip()
	tokens = user_input.split()

	if is_script:
		if script_id!=None:
			if is_halting(script_id): return True

	# Insert macros
	if config.SCRIPTING_ENGINE_ENABLED:
		for c in USER_MACROS:
			a = USER_MACROS[c]
			symbol = config.ISSUE_COMMAND_SYMBOL+a.name
			if len(tokens)>=1:
				if tokens[0]==symbol:
					tokens.pop(0)
					if len(tokens)>0:
						args = ' '.join(tokens)
						user_input = f"{config.ISSUE_COMMAND_SYMBOL}script {a.script} {args}"
						tokens = user_input.split()
					else:
						user_input = f"{config.ISSUE_COMMAND_SYMBOL}script {a.script}"
						tokens = user_input.split()

	# |----|
	# | /s |
	# |----|
	if config.INCLUDE_SCRIPT_COMMAND_SHORTCUT:
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'s':
				tokens[0]=config.ISSUE_COMMAND_SYMBOL+'script'

	# |--------|
	# | /macro |
	# |--------|
	if len(tokens)>=1:

		if not config.SCRIPTING_ENGINE_ENABLED:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'macro':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: Scripting is disabled")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# /macro name script
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'macro' and len(tokens)>=3:
			tokens.pop(0)
			name = tokens.pop(0)
			script = ' '.join(tokens)

			# If the first character is the issue command
			# symbol, strip that out of the name
			if len(name)>len(config.ISSUE_COMMAND_SYMBOL):
				il = len(config.ISSUE_COMMAND_SYMBOL)
				if name[:il] == config.ISSUE_COMMAND_SYMBOL:
					name = name[il:]

			# Make sure that macro names start with a letter
			if len(name)>=1:
				if not name[0].isalpha():
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}alias: Macro names must begin with a letter")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Macro names must begin with a letter")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			# Make sure the macro name isn't the same as an
			# existing command
			if not is_valid_macro_name(name):
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: \""+name+"\" is not a valid macro name")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"\""+name+"\" is not a valid macro name")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			# Make sure that the macro's script file exists,
			# and is readable
			efilename = find_file(script,SCRIPT_FILE_EXTENSION)
			if not efilename:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: \""+script+"\" doesn't exist or is not readable")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"\""+script+"\" doesn't exist or is not readable")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			if is_macro_name(name):
				t = Message(SYSTEM_MESSAGE,'',f"Replacing macro \"{name}\", executing \"{efilename}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(SYSTEM_MESSAGE,'',f"Adding macro \"{name}\", executing \"{efilename}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			add_command(name,script)
			build_help_and_autocomplete()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'macro':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"macro NAME SCRIPT...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"macro NAME SCRIPT...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /user |
	# |-------|
	if len(tokens)>=1:

		if not config.ENABLE_USER_COMMAND:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'user':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}user has been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}user has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# No arguments dumps a list of all editable config values
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'user' and len(tokens)==1:
			settings = USER.build_settings()

			count = 0
			results = []
			for s in settings:
				if type(settings[s]) is list: continue
				if type(settings[s]) is dict: continue
				count = count + 1
				if type(settings[s]).__name__=='bool':
					dtype = "boolean"
				elif type(settings[s]).__name__=='int':
					dtype = "integer"
				elif type(settings[s]).__name__=='str':
					dtype = "string"
				else:
					dtype = "unknown"
				t = Message(SYSTEM_MESSAGE,'',f"{count}) {s} = \"{settings[s]}\" ({dtype})")
				results.append(t)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {count} user settings")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			for t in results:
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {count} user search results")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		# One argument displays the config value
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'user' and len(tokens)==2:
			settings = USER.build_settings()

			tokens.pop(0)
			my_setting = tokens.pop(0)

			if my_setting in settings:
				if type(settings[my_setting]) is list or type(settings[my_setting]) is dict:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found 0 user settings containing \"{my_setting}\"")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',"End 0 user search results")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			if my_setting in settings:
				if type(settings[my_setting]).__name__=='bool':
					dtype = "boolean"
				elif type(settings[my_setting]).__name__=='int':
					dtype = "integer"
				elif type(settings[my_setting]).__name__=='str':
					dtype = "string"
				else:
					dtype = "unknown"
				t = Message(SYSTEM_MESSAGE,'',f"{my_setting} = \"{settings[my_setting]}\" ({dtype})")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				results = []
				for a in settings:
					if type(settings[a]) is list: continue
					if type(settings[a]) is dict: continue
					if fnmatch.fnmatch(a,f"*{my_setting}*"):
						results.append(a)

				if len(results)==0:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: No settings found containing \"{my_setting}\"")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"No settings found containing \"{my_setting}\"")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				if len(results)>1:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(results)} user settings containing \"{my_setting}\"")
				else:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(results)} user setting containing \"{my_setting}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

				counter = 0
				for r in results:
					counter = counter + 1
					if type(settings[r]).__name__=='bool':
						dtype = "boolean"
					elif type(settings[r]).__name__=='int':
						dtype = "integer"
					elif type(settings[r]).__name__=='str':
						dtype = "string"
					else:
						dtype = "unknown"
					t = Message(SYSTEM_MESSAGE,'',f"&nbsp;&nbsp;{counter}) {r} = \"{settings[r]}\" ({dtype})")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

				if len(results)>1:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {len(results)} user search results")
				else:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {len(results)} user search result")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		# Two and more, we're editing user values
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'user' and len(tokens)>2:
			settings = USER.build_settings()

			tokens.pop(0)
			my_setting = tokens.pop(0)
			my_value = ' '.join(tokens)

			if my_value=='*': my_value = ''

			if my_setting in settings:
				if type(settings[my_setting])==list or type(settings[my_setting])==dict:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \"{my_setting}\" cannot be changed with the {config.ISSUE_COMMAND_SYMBOL}user command")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{my_setting}\" cannot be changed with the {config.ISSUE_COMMAND_SYMBOL}user command")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			if my_setting in settings:
				try:
					my_value=int(my_value)
				except:
					if str(my_value).lower()=='true': my_value = True
					if str(my_value).lower()=='false': my_value = False

				if type(my_value)!= type(settings[my_setting]):
					if type(settings[my_setting]).__name__=='bool':
						dtype = "boolean"
					elif type(settings[my_setting]).__name__=='int':
						dtype = "integer"
					elif type(settings[my_setting]).__name__=='str':
						dtype = "string"
					else:
						dtype = "unknown"
					if type(my_value).__name__=='bool':
						itype = "boolean"
					elif type(my_value).__name__=='int':
						itype = "integer"
					elif type(my_value).__name__=='str':
						itype = "string"
					else:
						itype = "unknown"
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \"{my_value}\" is not a valid value for \"{my_setting}\" (value is {itype}, requires {dtype})")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{my_value}\" is not a valid value for \"{my_setting}\" (value is {itype}, requires {dtype})")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				USER.import_data(my_setting,my_value)
				USER.save_user(USER.USER_FILE)

				t = Message(SYSTEM_MESSAGE,'',f"Setting \"{my_setting}\" to \"{my_value}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line: {line_number}: \"{my_setting}\" is not a valid user setting")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{my_setting}\" is not a valid user setting")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------------|
	# | /reconnectssl |
	# |---------------|
	if not SSL_AVAILABLE:
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnectssl':
				t = Message(ERROR_MESSAGE,'',"SSL/TLS is not available. Please install pyOpenSSL and service_identity to use this command.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	if len(tokens)>=1:
		# /reconnectssl HOST
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnectssl' and len(tokens)==2:
			tokens.pop(0)
			host = tokens.pop(0)
			port = 6667
			connect_to_irc(gui,window,host,port,None,True,True,False)
			return True
		# /reconnectssl HOST PORT
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnectssl' and len(tokens)==3:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}reconnectssl: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,None,True,True,False)
			return True
		# /reconnectssl HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnectssl' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}reconnectssl: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,password,True,True,False)
			return True
		# /reconnectssl
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnectssl' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnectssl':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"reconnectssl HOST [PORT] [PASSWORD]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"reconnectssl HOST [PORT] [PASSWORD]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |------------|
	# | /reconnect |
	# |------------|
	if len(tokens)>=1:
		# /reconnect HOST
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnect' and len(tokens)==2:
			tokens.pop(0)
			host = tokens.pop(0)
			port = 6667
			connect_to_irc(gui,window,host,port,None,False,True,False)
			return True
		# /reconnect HOST PORT
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnect' and len(tokens)==3:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}reconnect: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,None,False,True,False)
			return True
		# /reconnect HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnect' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}reconnect: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,password,False,True,False)
			return True
		# /reconnect
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnect' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reconnect':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"reconnect HOST [PORT] [PASSWORD]")
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"reconnect HOST [PORT] [PASSWORD]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------------|
	# | /xreconnectssl |
	# |----------------|
	if not SSL_AVAILABLE:
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnectssl':
				t = Message(ERROR_MESSAGE,'',"SSL/TLS is not available. Please install pyOpenSSL and service_identity to use this command.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	if len(tokens)>=1:
		# /reconnectssl HOST
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnectssl' and len(tokens)==2:
			tokens.pop(0)
			host = tokens.pop(0)
			port = 6667
			connect_to_irc(gui,window,host,port,None,True,True,True)
			return True
		# /reconnectssl HOST PORT
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnectssl' and len(tokens)==3:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xreconnectssl: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,None,True,True,True)
			return True
		# /reconnectssl HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnectssl' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xreconnectssl: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,password,True,True,True)
			return True
		# /xreconnectssl
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnectssl' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnectssl':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"xreconnectssl HOST [PORT] [PASSWORD]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"xreconnectssl HOST [PORT] [PASSWORD]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------------|
	# | /xreconnect |
	# |-------------|
	if len(tokens)>=1:
		# /reconnect HOST
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnect' and len(tokens)==2:
			tokens.pop(0)
			host = tokens.pop(0)
			port = 6667
			connect_to_irc(gui,window,host,port,None,False,True,True)
			return True
		# /reconnect HOST PORT
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnect' and len(tokens)==3:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xreconnect: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,None,False,True,True)
			return True
		# /reconnect HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnect' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xreconnect: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,password,False,True,True)
			return True
		# /xreconnect
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnect' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xreconnect':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"xreconnect HOST [PORT] [PASSWORD]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"xreconnect HOST [PORT] [PASSWORD]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /focus |
	# |--------|
	if len(tokens)>=1:

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus' and len(tokens)==1:
			window.input.setFocus()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)

			swins = gui.getAllServerWindows()
			for win in swins:
				if server.lower() in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.widget().input.setFocus()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}focus: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.server}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.widget().input.setFocus()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}focus: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.widget().input.setFocus()
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}focus: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"focus [SERVER] [WINDOW]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"focus [SERVER] [WINDOW]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /move |
	# |-------|
	if len(tokens)>=1:

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'move' and len(tokens)==5:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)
			x_val = tokens.pop(0)
			y_val = tokens.pop(0)

			x_val = is_int(x_val)
			if x_val==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid X value")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid X value passed to {config.ISSUE_COMMAND_SYMBOL}move")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			y_val = is_int(y_val)
			if y_val==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid Y value")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid Y value passed to {config.ISSUE_COMMAND_SYMBOL}move")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			swins = gui.getAllServerWindows()
			for win in swins:
				if server in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						if gui.is_valid_position(w,x_val,y_val):
							w.move(x_val,y_val)
						else:
							if is_script:
								add_halt(script_id)
								if config.DISPLAY_SCRIPT_ERRORS:
									t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Not a valid window position")
									window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
								return True
							t = Message(ERROR_MESSAGE,'',"Not a valid window position")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.server}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						if gui.is_valid_position(w,x_val,y_val):
							w.move(x_val,y_val)
						else:
							if is_script:
								add_halt(script_id)
								if config.DISPLAY_SCRIPT_ERRORS:
									t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Not a valid window position")
									window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
								return True
							t = Message(ERROR_MESSAGE,'',"Not a valid window position")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'move' and len(tokens)==4:
			tokens.pop(0)
			target = tokens.pop(0)
			x_val = tokens.pop(0)
			y_val = tokens.pop(0)

			x_val = is_int(x_val)
			if x_val==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid X value")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid X value passed to {config.ISSUE_COMMAND_SYMBOL}move")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			y_val = is_int(y_val)
			if y_val==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid Y value")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid Y Value passed to {config.ISSUE_COMMAND_SYMBOL}move")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			w = gui.getSubWindow(target,window.client)
			if w:
				if gui.is_valid_position(w,x_val,y_val):
					w.move(x_val,y_val)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Not a valid window position")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Not a valid window position")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'move' and len(tokens)==3:
			tokens.pop(0)
			x_val = tokens.pop(0)
			y_val = tokens.pop(0)

			x_val = is_int(x_val)
			if x_val==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid X value")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid X value passed to {config.ISSUE_COMMAND_SYMBOL}move")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			y_val = is_int(y_val)
			if y_val==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid Y value")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid Y value passed to {config.ISSUE_COMMAND_SYMBOL}move")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			w = gui.getSubWindow(window.name,window.client)
			if w:
				if gui.is_valid_position(w,x_val,y_val):
					w.move(x_val,y_val)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Not a valid window position")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Not a valid window position")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Window \""+window.name+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+window.name+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'move':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"move [SERVER] [WINDOW] X Y")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"move [SERVER] [WINDOW] X Y")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /resize |
	# |---------|
	if len(tokens)>=1:

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'resize' and len(tokens)==5:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)
			width = tokens.pop(0)
			height = tokens.pop(0)

			width = is_int(width)
			if width==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Invalid width")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid width passed to {config.ISSUE_COMMAND_SYMBOL}resize")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			height = is_int(height)
			if height==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Invalid height")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid height passed to {config.ISSUE_COMMAND_SYMBOL}resize")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			swins = gui.getAllServerWindows()
			for win in swins:
				if server in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.resize(width,height)
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.server}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.resize(width,height)
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'resize' and len(tokens)==4:
			tokens.pop(0)
			target = tokens.pop(0)
			width = tokens.pop(0)
			height = tokens.pop(0)

			width = is_int(width)
			if width==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Invalid width")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid width passed to {config.ISSUE_COMMAND_SYMBOL}resize")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			height = is_int(height)
			if height==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Invalid height")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid height passed to {config.ISSUE_COMMAND_SYMBOL}resize")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			w = gui.getSubWindow(target,window.client)
			if w:
				w.resize(width,height)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'resize' and len(tokens)==3:
			tokens.pop(0)
			width = tokens.pop(0)
			height = tokens.pop(0)

			width = is_int(width)
			if width==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Invalid width")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid width passed to {config.ISSUE_COMMAND_SYMBOL}resize")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			height = is_int(height)
			if height==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Invalid height")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid height passed to {config.ISSUE_COMMAND_SYMBOL}resize")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			w = gui.getSubWindow(window.name,window.client)
			if w:
				w.resize(width,height)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}resize: Window \""+window.name+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+window.name+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'resize':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"resize [SERVER] [WINDOW] WIDTH HEIGHT")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"resize [SERVER] [WINDOW] WIDTH HEIGHT")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------------|
	# | /fullscreen |
	# |-------------|
	if len(tokens)>=1:
		if len(tokens)==1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'fullscreen':
				if gui.fullscreen:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Full screen mode is turned on by command-line flag")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Full screen mode is turned on by command-line flag")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if config.SHOW_FULL_SCREEN:
					config.SHOW_FULL_SCREEN = False
					if gui.was_maximized:
						gui.showMaximized()
					else:
						gui.showNormal()
				else:
					if gui.isMaximized(): gui.was_maximized = True
					config.SHOW_FULL_SCREEN = True
					gui.showFullScreen()
				config.save_settings(config.CONFIG_FILE)
				gui.buildSettingsMenu()
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'fullscreen':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"fullscreen")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"fullscreen")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |------|
	# | /rem |
	# |------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'rem':
			# Does absolutely nothing
			return True

	# |----------|
	# | /quitall |
	# |----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quitall' and len(tokens)==1:
			gui.disconnectAll()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quitall' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)

			if config.ENABLE_EMOJI_SHORTCODES:
				msg = emoji.emojize(config.DEFAULT_QUIT_MESSAGE,language=config.EMOJI_LANGUAGE)
			else:
				msg = config.DEFAULT_QUIT_MESSAGE

			if config.INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE:
				buildTemporaryAliases(gui,window)
				msg = interpolateAliases(msg)


			gui.disconnectAll(msg)
			return True

	# |---------|
	# | /prints |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'prints' and len(tokens)>=2:
			tokens.pop(0)

			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				msg = ' '.join(tokens)
				if len(msg)>0:
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					t = Message(SYSTEM_MESSAGE,'',f"{msg}")
					w.widget().writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: No text to print")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"No text to print")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			msg = target+' '+' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			t = Message(SYSTEM_MESSAGE,'',f"{msg}")
			# Get the current active window
			w = gui.MDI.activeSubWindow()
			if hasattr(w,"widget"):
				c = w.widget()
				if hasattr(c,"writeText"):
					c.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'prints' and len(tokens)==1:
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"prints [WINDOW] TEXT")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"prints [WINDOW] TEXT")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /random |
	# |---------|
	if len(tokens)>=1:

		if not config.ENABLE_ALIASES:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'random':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}random: Aliases have been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Aliases have been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'random' and len(tokens)==4:
			
			tokens.pop(0)
			a =  tokens.pop(0)
			low = tokens.pop(0)
			high = tokens.pop(0)

			# If the first character is the interpolation
			# symbol, strip it from the name
			if len(a)>len(config.ALIAS_INTERPOLATION_SYMBOL):
				il = len(config.ALIAS_INTERPOLATION_SYMBOL)
				if a[:il] == config.ALIAS_INTERPOLATION_SYMBOL:
					a = a[il:]

			if len(a)>=1:
				if not a[0].isalpha():
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}random: Alias tokens must begin with a letter")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Alias tokens must begin with a letter")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			try:
				low = int(low)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}random: \"{low}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{low}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			try:
				high = int(high)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}random: \"{high}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{high}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			addAlias(a,f"{random.randint(low,high)}")
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'random':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"random ALIAS LOW HIGH")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"random ALIAS LOW HIGH")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /close |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'close' and len(tokens)==1:
			w = gui.getSubWindow(window.name,window.client)
			w.close()
			gui.buildWindowbar()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'close' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)

			swins = gui.getAllServerWindows()
			for win in swins:
				if server.lower() in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.close()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}close: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.server}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.close()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}close: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}close: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'close' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.close()
				gui.buildWindowbar()
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}close: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'close':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"close [SERVER] [WINDOW]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"close [SERVER] [WINDOW]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /window |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==1:
			
			results = []
			for w in gui.getAllAllConnectedSubWindows():
				if w.isVisible():
					v = "visible"
				else:
					v = "hidden"
				c = w.widget()
				if c.window_type==CHANNEL_WINDOW:
					entry = f"{c.name} - Channel ({c.client.server}:{c.client.port}, {v})"
				elif c.window_type==PRIVATE_WINDOW:
					entry = f"{c.name} - Private Chat ({c.client.server}:{c.client.port}, {v})"
				elif c.window_type==SERVER_WINDOW:
					entry = f"{c.name} - Server ({c.client.server}:{c.client.port}, {v})"
				results.append(entry)

			if len(results)>1:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(results)} windows")
			else:
				t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(results)} window")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			mdi_viewport = gui.MDI.viewport()
			viewport_size = mdi_viewport.size()

			t = Message(SYSTEM_MESSAGE,'',f"Subwindow display area: {viewport_size.width()}x{viewport_size.height()}")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			counter = 0
			for r in results:
				counter = counter + 1
				t = Message(SYSTEM_MESSAGE,'',f"{counter}) {r}")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			if len(results)>1:
				t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {len(results)} windows")
			else:
				t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {len(results)} window")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			return True

		# /window move X Y
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==4:
			if tokens[1].lower()=='move':
				tokens.pop(0)
				tokens.pop(0)
				x_val = tokens.pop(0)
				y_val = tokens.pop(0)
				
				x_val = is_int(x_val)
				if x_val==None:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window move: Invalid X value")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Invalid X value passed to {config.ISSUE_COMMAND_SYMBOL}window move")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				y_val = is_int(y_val)
				if y_val==None:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window move: Invalid Y value")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Invalid Y value passed to {config.ISSUE_COMMAND_SYMBOL}window move")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				if gui.is_move_valid_on_screen(gui,x_val,y_val):
					gui.move(x_val,y_val)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window move: Not a valid window position")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Not a valid window position")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# /window size X Y
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==4:
			if tokens[1].lower()=='size':
				tokens.pop(0)
				tokens.pop(0)
				x_val = tokens.pop(0)
				y_val = tokens.pop(0)
				
				x_val = is_int(x_val)
				if x_val==None:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window size: Invalid width")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Invalid width value passed to {config.ISSUE_COMMAND_SYMBOL}window size")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				y_val = is_int(y_val)
				if y_val==None:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window size: Invalid height")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Invalid height passed to {config.ISSUE_COMMAND_SYMBOL}window size")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				gui.resize(x_val,y_val)
				return True

		# /window minimize
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='minimize':
				gui.showMinimized()
				return True
			if tokens[1].lower()=='min':
				gui.showMinimized()
				return True

		# /window maximized
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='maximize':
				gui.showMaximized()
				return True
			if tokens[1].lower()=='max':
				gui.showMaximized()
				return True

		# /window restore
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='restore':
				gui.showNormal()
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"window [COMMAND] [X] [Y]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"window [COMMAND] [X] [Y]")
			window.writeTe

	# |-------|
	# | /show |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'show' and len(tokens)==1:
			w = gui.getSubWindow(window.name,window.client)
			w.show()
			gui.buildWindowbar()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'show' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)

			swins = gui.getAllServerWindows()
			for win in swins:
				if server.lower() in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						gui.showSubWindow(w)
						if hasattr(window,"input"): window.input.setFocus()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}show: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.server}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						gui.showSubWindow(w)
						if hasattr(window,"input"): window.input.setFocus()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}show: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}show: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'show' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				gui.showSubWindow(w)
				if hasattr(window,"input"): window.input.setFocus()
				gui.buildWindowbar()
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}show: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'show':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"show [SERVER] [WINDOW]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"show [SERVER] [WINDOW]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /hide |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'hide' and len(tokens)==1:
			w = gui.getSubWindow(window.name,window.client)
			w.hide()
			gui.buildWindowbar()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'hide' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)

			swins = gui.getAllServerWindows()
			for win in swins:
				if server.lower() in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.hide()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}hide: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.server}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.hide()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}hide: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}hide: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'hide' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.hide()
				gui.buildWindowbar()
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}hide: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'hide':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"hide [SERVER] [WINDOW]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"hide [SERVER] [WINDOW]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /delay |
	# |--------|
	if len(tokens)>=1:

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'delay':
			if not config.ENABLE_DELAY_COMMAND:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"delay has been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',config.ISSUE_COMMAND_SYMBOL+"delay has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'delay' and len(tokens)>=3:
			tokens.pop(0)
			wait = tokens.pop(0)
			command = ' '.join(tokens)

			try:
				wait = float(wait)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"delay requires a numerical argument")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"delay requires a numerical argument")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			script_id = str(uuid.uuid4())
			gui.scripts[script_id] = DelayThread(script_id,gui,window,command,wait)
			gui.scripts[script_id].threadEnd.connect(execute_script_end)
			gui.scripts[script_id].finished.connect(execute_delay)
			gui.scripts[script_id].start()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'delay':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"delay SECONDS COMMAND...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"delay SECONDS COMMAND...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /next |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'next' and len(tokens)==1:
			gui.MDI.activateNextSubWindow()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'next':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"next")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"next")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-----------|
	# | /previous |
	# |-----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'previous' and len(tokens)==1:
			gui.MDI.activateNextSubWindow()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'previous':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"previous")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"previous")
			window.writeTe

	# |----------|
	# | /reclaim |
	# |----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reclaim' and len(tokens)==2:
			tokens.pop(0)
			nickname = tokens.pop(0)

			script_id = str(uuid.uuid4())
			gui.scripts[script_id] = ReclaimThread(script_id,gui,window,nickname,config.RECLAIM_NICKNAME_FREQUENCY)
			gui.scripts[script_id].threadEnd.connect(execute_script_end)
			gui.scripts[script_id].reclaim.connect(do_reclaim)
			gui.scripts[script_id].already.connect(do_already)
			gui.scripts[script_id].tstart.connect(do_start)
			gui.scripts[script_id].start()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'reclaim':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"reclaim NICKNAME")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"reclaim NICKNAME")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /msgbox |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'msgbox' and len(tokens)>=2:
			tokens.pop(0)
			
			msg = ' '.join(tokens)

			msgBox = QMessageBox()
			msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
			msgBox.setText(msg)
			msgBox.setWindowTitle(APPLICATION_NAME)
			msgBox.setStandardButtons(QMessageBox.Ok)

			msgBox.exec()

			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'msgbox':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"msgbox MESSAGE...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"msgbox MESSAGE...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /private |
	# |----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'private' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = window.parent.openPrivate(window.client,target)
			w.show()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'private' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			w = window.parent.openPrivate(window.client,target)
			window.client.msg(target,msg)
			t = Message(SELF_MESSAGE,window.client.nickname,msg)
			w.widget().writeText(t)
			w.show()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'private':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"private NICKNAME")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"private NICKNAME")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-----|
	# | /me |
	# |-----|
	if window.window_type==SERVER_WINDOW:
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'me' and len(tokens)>=3:
				tokens.pop(0)
				target = tokens.pop(0)
				msg = ' '.join(tokens)
				if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)

				# If we have the target's window open, write
				# the message there
				displayed_message = False
				w = gui.getWindow(target,window.client)
				if w:
					t = Message(ACTION_MESSAGE,window.client.nickname,msg)
					w.writeText(t)
					displayed_message = True

				# Write the message to the server window
				if config.WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW:
					if target[:1]!='#' and target[:1]!='&' and target[:1]!='!' and target[:1]!='+':
						w = gui.getServerWindow(window.client)
						if w:
							t = Message(ACTION_MESSAGE,"&rarr; "+target+": ",window.client.nickname+" "+msg)
							w.writeText(t)

				if config.CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES:
					if target[:1]!='#' and target[:1]!='&' and target[:1]!='!' and target[:1]!='+':
						if not displayed_message:
							w = gui.newPrivateWindow(target,window.client)
							if w:
								c = w.widget()
								t = Message(ACTION_MESSAGE,window.client.nickname,msg)
								c.writeText(t)

				window.client.describe(target,msg)
				return True
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'me':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"me TARGET MESSAGE")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"me TARGET MESSAGE")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |-------|
	# | /ctcp |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ctcp' and len(tokens)>=3:
			tokens.pop(0)
			request = tokens.pop(0).upper()
			target = tokens.pop(0)
			args = ' '.join(tokens)

			if request=="VERSION":
				pass
			elif request=="TIME":
				pass
			elif request=="FINGER":
				pass
			elif request=="USERINFO":
				pass
			elif request=="SOURCE":
				pass
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}ctcp: Invalid request type (not VERSION, TIME, USERINFO, SOURCE, or FINGER)")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Invalid request type (not VERSION, TIME, USERINFO, SOURCE, or FINGER)")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			window.client.ctcpMakeQuery(target, [(request, args)])
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ctcp':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"ctcp REQUEST USER")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"ctcp REQUEST USER")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /shell |
	# |--------|
	if len(tokens)>=1:

		if not config.ENABLE_ALIASES:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'shell':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}shell: Aliases have been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Aliases have been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'shell':
			if not config.ENABLE_SHELL_COMMAND:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"shell has been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',config.ISSUE_COMMAND_SYMBOL+"shell has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'shell' and len(tokens)>=3:
			tokens.pop(0)
			alias = tokens.pop(0)

			# If the first character is the interpolation
			# symbol, strip it from the name
			if len(alias)>len(config.ALIAS_INTERPOLATION_SYMBOL):
				il = len(config.ALIAS_INTERPOLATION_SYMBOL)
				if alias[:il] == config.ALIAS_INTERPOLATION_SYMBOL:
					alias = alias[il:]

			if len(alias)>=1:
				if not alias[0].isalpha():
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}shell: Alias tokens must begin with a letter")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Alias tokens must begin with a letter")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			try:
				result = subprocess.run(tokens, capture_output=True, text=True, check=True, shell=True)
				stored = f"{result.stdout}"
				addAlias(alias,stored)
			except subprocess.CalledProcessError as e:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}:{config.ISSUE_COMMAND_SYMBOL}shell returned \"{e.stderr}\"")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Error executing {config.ISSUE_COMMAND_SYMBOL}shell {alias} {' '.join(tokens)}")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				t = Message(ERROR_MESSAGE,'',f"{e.stderr}")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'shell':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"shell ALIAS COMMAND...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"shell ALIAS COMMAND...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /ping |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ping' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			window.client.ping(target)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ping' and len(tokens)>2:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			window.client.ping(target,msg)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ping':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"ping USER")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"ping USER")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /find |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'find' and len(tokens)==1:
			flist = list_files()

			count = len(flist)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {count} files")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			for f in flist:
				t = Message(SYSTEM_MESSAGE,'',f"{f}")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {count} file results")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'find' and len(tokens)>=2:
			tokens.pop(0)
			target = ' '.join(tokens)

			found = []
			for f in list_files():
				b = os.path.basename(f)
				if fnmatch.fnmatch(b, f"{target}"): found.append(b)

			count = len(found)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {count} files")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			for f in found:
				t = Message(SYSTEM_MESSAGE,'',f"{f}")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {count} file results")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /ignore |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ignore' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0).lower()

			for e in config.IGNORE_LIST:
				if target.lower()==e.lower():
					if is_script==True:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \"{target}\" is already in the ignore list")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{target}\" is already in the ignore list")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			t = Message(SYSTEM_MESSAGE,'',f"Ignoring user \"{target}\"")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			config.IGNORE_LIST.append(target)
			config.save_settings(config.CONFIG_FILE)
			gui.buildSettingsMenu()
			gui.reRenderAll(True)
			gui.rerenderUserlists()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ignore':

			if len(config.IGNORE_LIST)==0:
				t = Message(SYSTEM_MESSAGE,'',f"Ignore list is empty")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			count = 0
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Begin ignore list")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			for i in config.IGNORE_LIST:
				count = count + 1
				t = Message(SYSTEM_MESSAGE,'',f"{count}) {i}")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End ignore list")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-----------|
	# | /unignore |
	# |-----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unignore' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0).lower()

			if target=='*':
				config.IGNORE_LIST = []
				t = Message(SYSTEM_MESSAGE,'',f"Unignoring all users")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				config.save_settings(config.CONFIG_FILE)
				gui.buildSettingsMenu()
				gui.reRenderAll(True)
				gui.rerenderUserlists()
				return True

			if target in config.IGNORE_LIST:
				config.IGNORE_LIST.remove(target)
			else:
				if is_script==True:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \"{target}\" is not in the ignore list")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{target}\" is not in the ignore list")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(SYSTEM_MESSAGE,'',f"Unignoring user \"{target}\"")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			config.save_settings(config.CONFIG_FILE)
			gui.buildSettingsMenu()
			gui.reRenderAll(True)
			gui.rerenderUserlists()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unignore':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"unignore USER")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"unignore USER")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |------|
	# | /log |
	# |------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'log' and len(tokens)==1:
			gui.menuExportLog()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'log':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"log")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /config |
	# |---------|
	if len(tokens)>=1:

		if not config.ENABLE_CONFIG_COMMAND:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'config':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}config has been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}config has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# No arguments dumps a list of all editable config values
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'config' and len(tokens)==1:
			settings = config.build_settings()

			count = 0
			results = []
			for s in settings:
				if s=="timestamp_format": continue
				if s=="log_absolutely_all_messages_of_any_type": continue
				if not type(settings[s]) is list:
					count = count + 1
					if type(settings[s]).__name__=='bool':
						dtype = "boolean"
					elif type(settings[s]).__name__=='int':
						dtype = "integer"
					elif type(settings[s]).__name__=='str':
						dtype = "string"
					else:
						dtype = "unknown"
					t = Message(SYSTEM_MESSAGE,'',f"{count}) {s} = \"{settings[s]}\" ({dtype})")
					results.append(t)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {count} config settings")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			for t in results:
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {count} config search results")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		# One argument displays the config value
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'config' and len(tokens)==2:
			settings = config.build_settings()

			tokens.pop(0)
			my_setting = tokens.pop(0)

			if my_setting in settings:
				if type(settings[my_setting]) is list or my_setting=="timestamp_format" or my_setting=="log_absolutely_all_messages_of_any_type":
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found 0 config settings containing \"{my_setting}\"")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',"End 0 config search results")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			if my_setting in settings:
				if type(settings[my_setting]).__name__=='bool':
					dtype = "boolean"
				elif type(settings[my_setting]).__name__=='int':
					dtype = "integer"
				elif type(settings[my_setting]).__name__=='str':
					dtype = "string"
				else:
					dtype = "unknown"
				t = Message(SYSTEM_MESSAGE,'',f"{my_setting} = \"{settings[my_setting]}\" ({dtype})")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				results = []
				for a in settings:
					if not type(settings[a]) is list:
						if a!="timestamp_format" and a!="log_absolutely_all_messages_of_any_type":
							if fnmatch.fnmatch(a,f"*{my_setting}*"):
								results.append(a)

				if len(results)==0:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: No settings found containing \"{my_setting}\"")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"No settings found containing \"{my_setting}\"")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				if len(results)>1:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(results)} config settings containing \"{my_setting}\"")
				else:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(results)} config setting containing \"{my_setting}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

				counter = 0
				for r in results:
					counter = counter + 1
					if type(settings[r]).__name__=='bool':
						dtype = "boolean"
					elif type(settings[r]).__name__=='int':
						dtype = "integer"
					elif type(settings[r]).__name__=='str':
						dtype = "string"
					else:
						dtype = "unknown"
					t = Message(SYSTEM_MESSAGE,'',f"&nbsp;&nbsp;{counter}) {r} = \"{settings[r]}\" ({dtype})")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

				if len(results)>1:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {len(results)} config search results")
				else:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {len(results)} config search result")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		# Two and more, we're editing config values
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'config' and len(tokens)>2:
			settings = config.build_settings()

			tokens.pop(0)
			my_setting = tokens.pop(0)
			my_value = ' '.join(tokens)

			if my_setting in settings:
				if type(settings[my_setting]) is list or my_setting=="timestamp_format" or my_setting=="log_absolutely_all_messages_of_any_type":
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \"{my_setting}\" cannot be changed with the {config.ISSUE_COMMAND_SYMBOL}config command")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{my_setting}\" cannot be changed with the {config.ISSUE_COMMAND_SYMBOL}config command")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			if my_setting in settings:
				try:
					my_value=int(my_value)
				except:
					if str(my_value).lower()=='true': my_value = True
					if str(my_value).lower()=='false': my_value = False

				if type(my_value)!= type(settings[my_setting]):
					if type(settings[my_setting]).__name__=='bool':
						dtype = "boolean"
					elif type(settings[my_setting]).__name__=='int':
						dtype = "integer"
					elif type(settings[my_setting]).__name__=='str':
						dtype = "string"
					else:
						dtype = "unknown"
					if type(my_value).__name__=='bool':
						itype = "boolean"
					elif type(my_value).__name__=='int':
						itype = "integer"
					elif type(my_value).__name__=='str':
						itype = "string"
					else:
						itype = "unknown"
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \"{my_value}\" is not a valid value for \"{my_setting}\" (value is {itype}, requires {dtype})")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{my_value}\" is not a valid value for \"{my_setting}\" (value is {itype}, requires {dtype})")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				# Make sure the spellcheck language is lowercase
				if my_setting=="default_spellcheck_language":
					my_value = my_value.lower()

				# Check for sanity
				check = check_for_sane_values(my_setting,my_value)
				if check!=ALL_VALID_SETTINGS:
					if check==INVALID_STYLE:
						qlist = [f"\"{item}\"" for item in QStyleFactory.keys()]
						reason = f"must be {", ".join(qlist[:-1]) + " or " + qlist[-1]}"
					elif check==INVALID_JUSTIFY:
						reason = "must be \"center\", \"left\", or \"right\""
					elif check==INVALID_COLOR:
						reason = f"not a recognized color"
					elif check==INVALID_LANGUAGE:
						reason = f"not a valid spellchecker language"
					elif check==INVALID_TEXT_STYLE:
						reason = f"not a valid text style"
					elif check==INVALID_ORDER:
						reason = "must be \"creation\", \"stacking\", or \"activation\""
					else:
						reason = "unknown"
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line: {line_number}: \"{my_value}\" is not a valid value for \"{my_setting}\" ({reason})")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{my_value}\" is not a valid value for \"{my_setting}\" ({reason})")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				settings[my_setting] = my_value
				config.save_settings(config.CONFIG_FILE,settings)

				gui.reload_settings()

				t = Message(SYSTEM_MESSAGE,'',f"Setting \"{my_setting}\" to \"{my_value}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line: {line_number}: \"{my_setting}\" is not a valid configuration setting")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{my_setting}\" is not a valid configuration setting")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /exit |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'exit' and len(tokens)==2:
			tokens.pop(0)
			timer = tokens.pop(0)

			try:
				timer=float(timer)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}exit: \"{timer}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{timer}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			t = Message(SYSTEM_MESSAGE,'',f"Exiting {APPLICATION_NAME} in {timer} seconds...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			script_id = str(uuid.uuid4())
			gui.scripts[script_id] = ExitThread(script_id,gui,timer)
			gui.scripts[script_id].threadEnd.connect(exit_from_command)
			gui.scripts[script_id].start()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'exit' and len(tokens)==1:
			t = Message(SYSTEM_MESSAGE,'',f"Exiting {APPLICATION_NAME}...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			script_id = str(uuid.uuid4())
			gui.scripts[script_id] = ExitThread(script_id,gui,0.5)
			gui.scripts[script_id].threadEnd.connect(exit_from_command)
			gui.scripts[script_id].start()
			return True

	# |--------|
	# | /knock |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'knock' and len(tokens)==2:
			if not 'KNOCK' in window.client.supports:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"knock command is not supported by this server")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',config.ISSUE_COMMAND_SYMBOL+"knock command is not supported by this server")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			tokens.pop(0)
			target = tokens.pop(0)
			window.client.sendLine('KNOCK '+target)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'knock' and len(tokens)>=2:
			if not 'KNOCK' in window.client.supports:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"knock command is not supported by this server")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',config.ISSUE_COMMAND_SYMBOL+"knock command is not supported by this server")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			tokens.pop(0)
			target = tokens.pop(0)
			message = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
			window.client.sendLine('KNOCK '+target+' '+message)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'knock':
			if not 'KNOCK' in window.client.supports:
				t = Message(ERROR_MESSAGE,'',config.ISSUE_COMMAND_SYMBOL+"knock command is not supported by this server")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"knock CHANNEL [MESSAGE]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"knock CHANNEL [MESSAGE]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /refresh |
	# |----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'refresh' and len(tokens)==1:
			window.client.sendLine('LIST')
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'refresh':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"refresh")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"refresh")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /list |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'list' and len(tokens)==1:

			if len(window.client.server_channel_list)==0:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Channel list is empty, please use "+config.ISSUE_COMMAND_SYMBOL+"refresh to populate it.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Channel list is empty, please use "+config.ISSUE_COMMAND_SYMBOL+"refresh to populate it.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			# No search terms, so open the channel list window
			window.showChannelList()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'list' and len(tokens)>=2:

			tokens.pop(0)
			target = ' '.join(tokens)

			# Check for list "freshness"
			dt1 = datetime.fromtimestamp(window.client.last_list_timestamp)
			dt2 = datetime.fromtimestamp(datetime.utcnow().timestamp())
			time_difference = dt2 - dt1
			if time_difference.total_seconds() / 60 > 60:
				# list was last fetched an hour or more ago
				t = Message(SYSTEM_MESSAGE,'',f"List was last fetched a while ago, you may want to use {config.ISSUE_COMMAND_SYMBOL}refresh to fetch a new one")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			# Show the channel list window and inject search
			window.showChannelListSearch(target)
			return True

	# |-------|
	# | /play |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'play' and len(tokens)==2:

			tokens.pop(0)
			filename = tokens.pop(0)

			efilename = find_file(filename,"wav")
			if efilename!=None:
				if is_wav_file(efilename):
					QSound.play(efilename)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \""+filename+"\" is not a WAV file.")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"\""+filename+"\" is not a WAV file.")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Audio file \""+filename+"\" cannot be found.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Audio file \""+filename+"\" cannot be found.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'play':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"play FILENAME")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"play FILENAME")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /alias |
	# |--------|

	if not config.ENABLE_ALIASES:
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}alias: Aliases have been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Aliases have been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias' and len(tokens)>=3:

			tokens.pop(0)
			a = tokens.pop(0)

			# If the first character is the interpolation
			# symbol, strip it from the name
			if len(a)>len(config.ALIAS_INTERPOLATION_SYMBOL):
				il = len(config.ALIAS_INTERPOLATION_SYMBOL)
				if a[:il] == config.ALIAS_INTERPOLATION_SYMBOL:
					a = a[il:]

			if len(a)>=1:
				if not a[0].isalpha():
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}alias: Alias tokens must begin with a letter")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Alias tokens must begin with a letter")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			value = ' '.join(tokens)

			result,error = math(value)
			if not error: value = str(result)

			addAlias(a,value)

			if not is_script:
				t = Message(SYSTEM_MESSAGE,'',"Alias "+config.ALIAS_INTERPOLATION_SYMBOL+a+" set to \""+value+"\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias' and len(tokens)==1:

			if len(ALIAS)==0 and len(TEMPORARY_ALIAS)==0:
				t = Message(SYSTEM_MESSAGE,'',"No aliases are currently defined.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True


			count = len(TEMPORARY_ALIAS) + len(ALIAS)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {count} aliases")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			for a in TEMPORARY_ALIAS:
				t = Message(SYSTEM_MESSAGE,'',config.ALIAS_INTERPOLATION_SYMBOL+a+" = \""+TEMPORARY_ALIAS[a]+"\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			for a in ALIAS:
				t = Message(SYSTEM_MESSAGE,'',config.ALIAS_INTERPOLATION_SYMBOL+a+" = \""+ALIAS[a]+"\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {count} aliases")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"alias TOKEN TEXT...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"alias TOKEN TEXT...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /unalias |
	# |----------|

	if not config.ENABLE_ALIASES:
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unalias' and len(tokens)>=1:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}unalias: Aliases have been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Aliases have been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	if len(tokens)>0:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unalias' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)

			if removeAlias(target):
				if not is_script:
					t = Message(SYSTEM_MESSAGE,'',f"Alias \"{target}\" deleted.")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}unalias: Alias \"{target}\" not found.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Alias \"{target}\" not found.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unalias':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"unalias TOKEN")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"unalias TOKEN")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------------|
	# | /connectssl |
	# |-------------|
	if not SSL_AVAILABLE:
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connectssl':
				t = Message(ERROR_MESSAGE,'',"SSL/TLS is not available. Please install pyOpenSSL and service_identity to use this command.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	if len(tokens)>=1:
		# /connectssl HOST
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connectssl' and len(tokens)==2:
			tokens.pop(0)
			host = tokens.pop(0)
			port = 6667
			connect_to_irc(gui,window,host,port,None,True,False,False)
			return True
		# /connectssl HOST PORT
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connectssl' and len(tokens)==3:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}connectssl: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,None,True,False,False)
			return True
		# /connectssl HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connectssl' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}connectssl: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,password,True,False,False)
			return True
		# /connectssl
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connectssl' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connectssl':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"connectssl HOST [PORT] [PASSWORD]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"connectssl HOST [PORT] [PASSWORD]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /connect |
	# |----------|
	if len(tokens)>=1:
		# /connect HOST
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connect' and len(tokens)==2:
			tokens.pop(0)
			host = tokens.pop(0)
			port = 6667
			connect_to_irc(gui,window,host,port,None,False,False,False)
			return True
		# /connect HOST PORT
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connect' and len(tokens)==3:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}connect: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,None,False,False,False)
			return True
		# /connect HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connect' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}connect: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,password,False,False,False)
			return True
		# /connect
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connect' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connect':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"connect HOST [PORT] [PASSWORD]")
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"connect HOST [PORT] [PASSWORD]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------------|
	# | /xconnectssl |
	# |--------------|
	if not SSL_AVAILABLE:
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnectssl':
				t = Message(ERROR_MESSAGE,'',"SSL/TLS is not available. Please install pyOpenSSL and service_identity to use this command.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	if len(tokens)>=1:
		# /connectssl HOST
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnectssl' and len(tokens)==2:
			tokens.pop(0)
			host = tokens.pop(0)
			port = 6667
			connect_to_irc(gui,window,host,port,None,True,False,True)
			return True
		# /connectssl HOST PORT
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnectssl' and len(tokens)==3:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xconnectssl: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,None,True,False,True)
			return True
		# /connectssl HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnectssl' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xconnectssl: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,password,True,False,True)
			return True
		# /xconnectssl
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnectssl' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnectssl':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"xconnectssl HOST [PORT] [PASSWORD]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"xconnectssl HOST [PORT] [PASSWORD]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-----------|
	# | /xconnect |
	# |-----------|
	if len(tokens)>=1:
		# /connect HOST
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnect' and len(tokens)==2:
			tokens.pop(0)
			host = tokens.pop(0)
			port = 6667
			connect_to_irc(gui,window,host,port,None,False,False,True)
			return True
		# /connect HOST PORT
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnect' and len(tokens)==3:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xconnect: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,None,False,False,True)
			return True
		# /connect HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnect' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			try:
				port = int(port)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xconnect: \"{port}\" is not a number")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{port}\" is not a number")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			connect_to_irc(gui,window,host,port,password,False,False,True)
			return True
		# /xconnect
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnect' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnect':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"xconnect HOST [PORT] [PASSWORD]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"xconnect HOST [PORT] [PASSWORD]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /edit |
	# |-------|
	if len(tokens)>=1:

		if not config.SCRIPTING_ENGINE_ENABLED:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit':
				t = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit' and len(tokens)>=2:

			tokens.pop(0)
			filename = ' '.join(tokens)

			efilename = find_file(filename,SCRIPT_FILE_EXTENSION)
			if efilename!=None:
				gui.newEditorWindowFile(efilename)

			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: File \""+filename+"\" doesn't exist or is not readable.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"File \""+filename+"\" doesn't exist or is not readable.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit' and len(tokens)==1:
			gui.newEditorWindow()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"edit [FILENAME]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"edit [FILENAME]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /version |
	# |----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'version' and len(tokens)==1:
			window.client.sendLine("VERSION")
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'version' and len(tokens)==2:
			tokens.pop(0)
			server = tokens.pop(0)
			window.client.sendLine("VERSION "+server)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'version':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"version")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"version")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /print |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'print' and len(tokens)>=2:
			tokens.pop(0)

			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				msg = ' '.join(tokens)
				if len(msg)>0:
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					t = Message(RAW_SYSTEM_MESSAGE,'',f"{msg}")
					w.widget().writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: No text to print")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"No text to print")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			msg = target+' '+' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			t = Message(RAW_SYSTEM_MESSAGE,'',f"{msg}")
			# Get the current active window
			w = gui.MDI.activeSubWindow()
			if hasattr(w,"widget"):
				c = w.widget()
				if hasattr(c,"writeText"):
					c.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'print' and len(tokens)==1:
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"print [WINDOW] TEXT")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"print [WINDOW] TEXT")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /time |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'time' and len(tokens)==1:
			window.client.sendLine("TIME")
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'time':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"time")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"time")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |------|
	# | /raw |
	# |------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'raw' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			window.client.sendLine(msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'raw' and len(tokens)==1:
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"raw TEXT")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"raw TEXT")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /back |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'back' and len(tokens)==1:
			window.client.back()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'back':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"back")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"back")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /away |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'away' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			window.client.away(msg)
			window.client.away_msg = msg
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'away' and len(tokens)==1:
			if config.PROMPT_FOR_AWAY_MESSAGE:
				x = Away(gui)
				msg = x.get_away_information(gui)
				if msg:
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					window.client.away(msg)
					window.client.away_msg = msg
			else:
				if config.ENABLE_EMOJI_SHORTCODES:
					msg = emoji.emojize(config.DEFAULT_AWAY_MESSAGE,language=config.EMOJI_LANGUAGE)
				else:
					msg = config.DEFAULT_AWAY_MESSAGE
				if config.INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE:
					buildTemporaryAliases(gui,window)
					msg = interpolateAliases(msg)
				window.client.away(msg)
				window.client.away_msg = msg
			return True

	# |-------|
	# | /oper |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'oper' and len(tokens)==3:
			tokens.pop(0)
			username = tokens.pop(0)
			password = tokens.pop(0)
			window.client.sendLine("OPER "+username+" "+password)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'oper':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"oper USERNAME PASSWORD")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"oper USERNAME PASSWORD")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /style |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'style' and len(tokens)==1:
			if not config.ENABLE_STYLE_EDITOR:
				t = Message(ERROR_MESSAGE,'',"The style editor has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			window.pressedStyleButton()
			return True

	# |-----------|
	# | /settings |
	# |-----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'settings' and len(tokens)==1:
			gui.openSettings()
			return True

	# |--------|
	# | /clear |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'clear' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)
			swins = gui.getAllServerWindows()
			for win in swins:
				if server.lower() in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.widget().clearChat()
						if hasattr(window,"input"): window.input.setFocus()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}clear: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.server}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.widget().clearChat()
						if hasattr(window,"input"): window.input.setFocus()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}clear: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}clear: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'clear' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.widget().clearChat()
				if hasattr(window,"input"): window.input.setFocus()
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}clear: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'clear':
			window.clearChat()
			return True

	# |-------|
	# | /tile |
	# |-------|
	if len(tokens)>=1:
		if len(tokens)==1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'tile':
				gui.MDI.tileSubWindows()
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'tile':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"tile")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"tile")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /cascade |
	# |----------|
	if len(tokens)>=1:
		if len(tokens)==1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'cascade':
				gui.MDI.cascadeSubWindows()
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'cascade':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"cascade")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"cascade")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /restore |
	# |----------|
	if len(tokens)>=1:

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'restore' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)

			swins = gui.getAllServerWindows()
			for win in swins:
				if server.lower() in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.showNormal()
						if hasattr(window,"input"): window.input.setFocus()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}restore: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.server}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.showNormal()
						if hasattr(window,"input"): window.input.setFocus()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}restore: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}restore: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'restore' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.showNormal()
				if hasattr(window,"input"): window.input.setFocus()
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}restore: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'restore':
			window.showNormal()
			return True

	# |-----------|
	# | /minimize |
	# |-----------|
	if len(tokens)>=1:

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'minimize' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)

			swins = gui.getAllServerWindows()
			for win in swins:
				if server.lower() in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.showMinimized()
						if hasattr(window,"input"): window.input.setFocus()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}minimize: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.server}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.showMinimized()
						if hasattr(window,"input"): window.input.setFocus()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}minimize: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}minimize: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'minimize' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.showMinimized()
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}minimize: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'minimize':
			window.showMinimized()
			return True

	# |-----------|
	# | /maximize |
	# |-----------|
	if len(tokens)>=1:

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'maximize' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)

			swins = gui.getAllServerWindows()
			for win in swins:
				if server.lower() in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.showMaximized()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}maximize: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.server}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.showMaximized()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}maximize: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}maximize: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'maximize' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.showMaximized()
				if hasattr(window,"input"): window.input.setFocus()
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}maximize: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'maximize':
			window.showMaximized()
			return True

	# |---------|
	# | /invite |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'invite' and len(tokens)==3:
			tokens.pop(0)
			user = tokens.pop(0)
			channel = tokens.pop(0)
			window.client.sendLine("INVITE "+user+" "+channel)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'invite':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"invite NICKNAME CHANNEL")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"invite NICKNAME CHANNEL")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /script |
	# |---------|
	if len(tokens)>=1:

		if not config.SCRIPTING_ENGINE_ENABLED:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'script':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}script: Scripting is disabled")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'script' and len(tokens)>=2:

			tokens.pop(0)
			tokens = shlex.split(' '.join(tokens), comments=False)
			filename = tokens.pop(0)
			arguments = list(tokens)

			efilename = find_file(filename,SCRIPT_FILE_EXTENSION)
			if efilename:
				f=open(efilename, "r",encoding="utf-8",errors="ignore")
				text = f.read()
				f.close()

				script_id = str(uuid.uuid4())
				gui.scripts[script_id] = ScriptThread(text,script_id,gui,window,arguments,efilename)
				gui.scripts[script_id].execLine.connect(execute_script_line)
				gui.scripts[script_id].scriptEnd.connect(execute_script_end)
				gui.scripts[script_id].scriptError.connect(execute_script_error)
				gui.scripts[script_id].start()

			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}script: \""+filename+"\" doesn't exist or is not readable.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"\""+filename+"\" doesn't exist or is not readable.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'script':

			if config.PROMPT_FOR_SCRIPT_FILE and not is_script:
				x = dialog.GetScript(gui)
				e = x.get_script_information(gui)
				if e:
					script = e[0]
					args = shlex.split(e[1], comments=False)

					# Check to see if the filename is a filename
					# in the application's "path"
					ffile = find_file(script,SCRIPT_FILE_EXTENSION)
					if ffile:
						f=open(ffile, "r",encoding="utf-8",errors="ignore")
						text = f.read()
						f.close()

						script_id = str(uuid.uuid4())
						gui.scripts[script_id] = ScriptThread(text,script_id,gui,window,args,ffile)
						gui.scripts[script_id].execLine.connect(execute_script_line)
						gui.scripts[script_id].scriptEnd.connect(execute_script_end)
						gui.scripts[script_id].scriptError.connect(execute_script_error)
						gui.scripts[script_id].start()

					else:
						# If the filename isn't on the "path", we check
						# to see if the filename actually exists
						if Path(script).exists():
							f=open(script, "r",encoding="utf-8",errors="ignore")
							text = f.read()
							f.close()

							script_id = str(uuid.uuid4())
							gui.scripts[script_id] = ScriptThread(text,script_id,gui,window,args,script)
							gui.scripts[script_id].execLine.connect(execute_script_line)
							gui.scripts[script_id].scriptEnd.connect(execute_script_end)
							gui.scripts[script_id].scriptError.connect(execute_script_error)
							gui.scripts[script_id].start()
						else:
							if is_script:
								add_halt(script_id)
								if config.DISPLAY_SCRIPT_ERRORS:
									t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}script: \"{script}\" doesn't exist or is not readable.")
									window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
								return True
							t = Message(ERROR_MESSAGE,'',f"\"{script}\" doesn't exist or is not readable.")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
				return True
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"script FILENAME")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"script FILENAME")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |---------|
	# | /whowas |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whowas' and len(tokens)==2:
			tokens.pop(0)
			nick = tokens.pop(0)
			window.client.sendLine("WHOWAS "+nick)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whowas' and len(tokens)==3:
			tokens.pop(0)
			nick = tokens.pop(0)
			arg = tokens.pop(0)
			try:
				arg = int(arg)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Second argument for "+config.ISSUE_COMMAND_SYMBOL+"whowas must be numeric")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Second argument for "+config.ISSUE_COMMAND_SYMBOL+"whowas must be numeric")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			window.client.sendLine("WHOWAS "+nick+" "+str(arg))
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whowas' and len(tokens)==4:
			tokens.pop(0)
			nick = tokens.pop(0)
			arg = tokens.pop(0)
			serv = tokens.pop(0)
			try:
				arg = int(arg)
			except:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Second argument for "+config.ISSUE_COMMAND_SYMBOL+"whowas must be numeric")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Second argument for "+config.ISSUE_COMMAND_SYMBOL+"whowas must be numeric")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			window.client.sendLine("WHOWAS "+nick+" "+str(arg)+" "+serv)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whowas':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"whowas NICKNAME [COUNT] [SERVER]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"whowas NICKNAME [COUNT] [SERVER]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |------|
	# | /who |
	# |------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'who' and len(tokens)==2:
			tokens.pop(0)
			nick = tokens.pop(0)
			window.client.sendLine("WHO "+nick)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'who' and len(tokens)==3:
			tokens.pop(0)
			nick = tokens.pop(0)
			arg = tokens.pop(0)
			if arg.lower()!='o':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Improper argument for "+config.ISSUE_COMMAND_SYMBOL+"who")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Improper argument for "+config.ISSUE_COMMAND_SYMBOL+"who")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			window.client.sendLine("WHO "+nick+" o")
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'who':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"who NICKNAME [o]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"who NICKNAME [o]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /whois |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whois' and len(tokens)==2:
			tokens.pop(0)
			nick = tokens.pop(0)
			window.client.whois(nick)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whois' and len(tokens)==3:
			tokens.pop(0)
			nick = tokens.pop(0)
			server = tokens.pop(0)
			window.client.whois(nick,server)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whois':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"whois NICKNAME [SERVER]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"whois NICKNAME [SERVER]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /kick |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'kick' and len(tokens)>=3:
			tokens.pop(0)
			channel = tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if len(msg.strip())==0: msg = None
			window.client.kick(channel,target,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'kick':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"kick CHANNEL NICKNAME [REASON]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"kick CHANNEL NICKNAME [REASON]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /mode |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'mode' and len(tokens)>=2:
			tokens.pop(0)
			target = tokens.pop(0)
			mode = ' '.join(tokens)
			window.client.sendLine("MODE "+target+" "+mode)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'mode':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"mode TARGET MODE...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"mode TARGET MODE...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True


	# |---------|
	# | /notice |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'notice' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			window.client.notice(target,msg)

			# If we have the target's window open, write
			# the message there
			w = gui.getWindow(target,window.client)
			if w:
				t = Message(NOTICE_MESSAGE,window.client.nickname,msg)
				w.writeText(t)

			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'notice':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"notice TARGET MESSAGE")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"notice TARGET MESSAGE")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |------|
	# | /msg |
	# |------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'msg' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			window.client.msg(target,msg)

			# If we have the target's window open, write
			# the message there
			displayed_message = False
			w = gui.getWindow(target,window.client)
			if w:
				t = Message(SELF_MESSAGE,window.client.nickname,msg)
				w.writeText(t)
				displayed_message = True

			# Write the message to the server window
			written_to_server_window = False
			if config.WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW:
				if target[:1]!='#' and target[:1]!='&' and target[:1]!='!' and target[:1]!='+':
					w = gui.getServerWindow(window.client)
					if w:
						written_to_server_window = True
						t = Message(SELF_MESSAGE,"&rarr; "+target,msg)
						w.writeText(t)

			if config.WRITE_OUTGOING_PRIVATE_MESSAGES_TO_CURRENT_WINDOW:
				if not is_script:
					if window == gui.getServerWindow(window.client):
						if not written_to_server_window:
							t = Message(SELF_MESSAGE,"&rarr; "+target,msg)
							window.writeText(t)
					else:
						t = Message(SELF_MESSAGE,"&rarr; "+target,msg)
						window.writeText(t)

			if config.CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES:
				if target[:1]!='#' and target[:1]!='&' and target[:1]!='!' and target[:1]!='+':
					if not displayed_message:
						w = gui.newPrivateWindow(target,window.client)
						if w:
							c = w.widget()
							t = Message(SELF_MESSAGE,window.client.nickname,msg)
							c.writeText(t)

			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'msg':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"msg TARGET MESSAGE")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"msg TARGET MESSAGE")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /help |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'help' and len(tokens)==2:
			tokens.pop(0)
			cmd = tokens.pop(0)
			if cmd[0]!=config.ISSUE_COMMAND_SYMBOL:
				cmd = config.ISSUE_COMMAND_SYMBOL+cmd
			found = False
			for entry in COMMAND_HELP_INFORMATION:
				if cmd in entry[0]:
					h = HELP_ENTRY_COMMAND_TEMPLATE
					h = h.replace("%_USAGE_%",entry[0])
					h = h.replace("%_DESCRIPTION_%",entry[1])
					t = Message(SYSTEM_MESSAGE,'',h)
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					found = True
			if found: return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Command "+cmd+" not found.")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Command "+cmd+" not found.")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'help':
			window.writeText(HELP,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /topic |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'topic' and len(tokens)>=3:
			tokens.pop(0)
			channel = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			window.client.topic(channel,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'topic':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /quit |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quit' and len(tokens)==1:

			if not gui.askDisconnect(window.client): return True

			if len(config.DEFAULT_QUIT_MESSAGE)>0:

				if config.ENABLE_EMOJI_SHORTCODES:
					msg = emoji.emojize(config.DEFAULT_QUIT_MESSAGE,language=config.EMOJI_LANGUAGE)
				else:
					msg = config.DEFAULT_QUIT_MESSAGE

				if config.INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE:
					buildTemporaryAliases(gui,window)
					msg = interpolateAliases(msg)

				window.client.quit(msg)
			else:
				window.client.quit()
			gui.quitting[window.client.client_id] = 0
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quit' and len(tokens)>=2:

			if not gui.askDisconnect(window.client): return True
			
			tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			window.client.quit(msg)
			gui.quitting[window.client.client_id] = 0
			return True

	# |-------|
	# | /nick |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'nick' and len(tokens)==2:
			tokens.pop(0)
			newnick = tokens.pop(0)

			# Check to see if the user is trying set their
			# new nickname to the nickname they are already using
			if window.client.nickname.lower()==newnick.lower():
				t = Message(ERROR_MESSAGE,'',"You are currently using \""+newnick+"\" as a nickname")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			window.client.setNick(newnick)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'nick':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"nick NEW_NICKNAME")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"nick NEW_NICKNAME")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /part |
	# |-------|
	if len(tokens)>1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)==2:
			tokens.pop(0)
			channel = tokens.pop(0)
			if config.ENABLE_EMOJI_SHORTCODES:
				msg = emoji.emojize(config.DEFAULT_QUIT_MESSAGE,language=config.EMOJI_LANGUAGE)
			else:
				msg = config.DEFAULT_QUIT_MESSAGE
			if config.INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE:
				buildTemporaryAliases(gui,window)
				msg = interpolateAliases(msg)
			window.client.leave(channel,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)>=3:
			tokens.pop(0)
			channel = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE:
				buildTemporaryAliases(gui,window)
				msg = interpolateAliases(msg)
			window.client.leave(channel,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"part CHANNEL [MESSAGE]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"part CHANNEL [MESSAGE]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /join |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'join' and len(tokens)==2:
			tokens.pop(0)
			channel = tokens.pop(0)

			# Check to see if the user is trying to /join the
			# channel from the same channel they are in
			if window.name.lower()==channel.lower():
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: You have already joined "+window.name)
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"You have already joined "+window.name)
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			# Check to see if the user has already joined
			# the channel, and switch to the window if they have
			w = gui.getSubWindow(channel,window.client)
			if w:
				gui.showSubWindow(w)
				return True

			# Check to see if a channel name prefix (like #) starts the channel's name,
			# and if not, add a # to the channel name
			if channel[:1]!='#' and channel[:1]!='&' and channel[:1]!='!' and channel[:1]!='+':
				channel = "#"+channel

			window.client.join(channel)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'join' and len(tokens)==3:
			tokens.pop(0)
			channel = tokens.pop(0)
			key = tokens.pop(0)

			# Check to see if the user is trying to /join the
			# channel from the same channel they are in
			if window.name.lower()==channel.lower():
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: You have already joined "+window.name)
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"You have already joined "+window.name)
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			# Check to see if the user has already joined
			# the channel, and switch to the window if they have
			w = gui.getSubWindow(channel,window.client)
			if w:
				gui.showSubWindow(w)
				return True

			# Check to see if a channel name prefix (like #) starts the channel's name,
			# and if not, add a # to the channel name
			if channel[:1]!='#' and channel[:1]!='&' and channel[:1]!='!' and channel[:1]!='+':
				channel = "#"+channel

			window.client.join(channel,key)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'join':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	return False

def execute_delay(data):
	gui = data[0]
	window = data[1]
	line = data[2]
	script_id = data[3]

	if not handleScriptCommands(gui,window,line,1,script_id):
		if len(line.strip())==0: return
		if config.DISPLAY_SCRIPT_ERRORS:
			if line[0]==config.ISSUE_COMMAND_SYMBOL:
				t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}delay: Unrecognized command \"{line}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}delay: Line \"{line}\" contains no command")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

class DelayThread(QThread):

	threadEnd = pyqtSignal(list)
	finished = pyqtSignal(list)

	def __init__(self,sid,gui,window,script,wait,parent=None):
		super(DelayThread, self).__init__(parent)
		self.id = sid
		self.gui = gui
		self.window = window
		self.script = script
		self.time = wait

	def run(self):

		time.sleep(self.time)
		self.finished.emit([self.gui,self.window,self.script,self.id])

		self.threadEnd.emit([self.gui,self.id])

def do_reclaim(data):
	window = data[0]
	nickname = data[1]
	window.client.setNick(nickname)

def do_already(data):
	window = data[0]
	nickname = data[1]
	
	t = Message(SYSTEM_MESSAGE,'',f"Nickname \"{nickname}\" already claimed")
	window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

def do_start(data):
	window = data[0]
	nickname = data[1]
	t = Message(SYSTEM_MESSAGE,'',f"Reclaiming nickname \"{nickname}\"...")
	window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

class ReclaimThread(QThread):

	threadEnd = pyqtSignal(list)
	reclaim = pyqtSignal(list)
	finished = pyqtSignal(list)
	already = pyqtSignal(list)
	tstart = pyqtSignal(object)

	def __init__(self,sid,gui,window,nickname,wait,parent=None):
		super(ReclaimThread, self).__init__(parent)
		self.id = sid
		self.gui = gui
		self.window = window
		self.nickname = nickname
		self.time = wait

	def run(self):

		if self.window.client.nickname==self.nickname:
			self.already.emit([self.window,self.nickname])
			self.threadEnd.emit([self.gui,self.id])
		else:
			self.tstart.emit([self.window,self.nickname])
			needreclaim = True
			while needreclaim:
				if self.window.client.nickname==self.nickname:
					needreclaim = False
					break
				self.reclaim.emit([self.window,self.nickname])
				time.sleep(self.time)

			self.threadEnd.emit([self.gui,self.id])


class ExitThread(QThread):

	threadEnd = pyqtSignal(object)

	def __init__(self,sid,gui,wait,parent=None):
		super(ExitThread, self).__init__(parent)
		self.id = sid
		self.gui = gui
		self.time = wait

	def run(self):

		time.sleep(self.time)

		self.threadEnd.emit(self.gui)

class ScriptThread(QThread):

	execLine = pyqtSignal(list)
	scriptEnd = pyqtSignal(list)
	scriptError = pyqtSignal(list)

	def __init__(self,script,sid,gui,window,arguments=[],filename=None,parent=None):
		super(ScriptThread, self).__init__(parent)
		self.script = script
		self.id = sid
		self.gui = gui
		self.window = window
		self.arguments = arguments
		self.filename = filename
		self.ALIAS = {}

		# Strip comments from script
		self.script = re.sub(re.compile("/\\*.*?\\*/",re.DOTALL ) ,"" ,self.script)

	def process_inserts(self):
		script = []
		got_error = False

		line_number = 0
		for line in self.script.split("\n"):
			line_number = line_number + 1
			line = line.strip()
			if len(line)==0: continue
			tokens = line.split()

			line = re.sub(re.compile("/\\*.*?\\*/",re.DOTALL ) ,"" ,line)

			skip_this_line = False

			# |=========|
			# | /insert |
			# |=========|
			if len(tokens)>=1:
				if len(tokens)>=2:
					if tokens[0].lower()=='insert':
						tokens.pop(0)

						# Use shlex to tokenize the input, so that we can
						# handle filenames with spaces in them
						ftokens = shlex.split(' '.join(tokens), comments=False)

						for f in ftokens:
							f = interpolateAliases(f)
							file = find_file(f,SCRIPT_FILE_EXTENSION)
							if file==None: file = find_file(f,None)
							if file!=None:
								x = open(file,"r")
								contents = x.read()
								x.close()

								if not self.check_for_errors(contents,file): return True

								for l in contents.split("\n"): script.append(l)
							else:
								self.scriptError.emit([self.gui,self.window,f"Error processing insert: File \"{f}\" cannot be found"])
								got_error = True
						skip_this_line = True
				elif tokens[0].lower()=='insert' and len(tokens)==1:
					self.scriptError.emit([self.gui,self.window,f"Error processing insert: insert called without any arguments"])
					skip_this_line = True
					got_error = True

			if not skip_this_line:
				script.append(line)

		if len(script)>0: self.script = interpolateAliases("\n".join(script))

		return got_error

	def check_for_errors(self,script,filename):
		if filename==None: filename = "script"
		no_errors = True
		line_number = 0
		for line in script.split("\n"):
			line_number = line_number + 1
			line = line.strip()
			if len(line)==0: continue
			tokens = line.split()

			line = re.sub(re.compile("/\\*.*?\\*/",re.DOTALL ) ,"" ,line)

			# |=========|
			# | exclude |
			# |=========|
			if len(tokens)>=1:
				if tokens[0].lower()=='exclude' and len(tokens)>=2:
					tokens.pop(0)
					
					valid = True
					buildTemporaryAliases(self.gui,self.window)
					for e in tokens:
						e = interpolateAliases(e)
						if e.lower()==self.window.name.lower(): valid = False

					if valid==False:
						if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
							self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Script cannot be ran in {self.window.name}"])
						no_errors = False

				elif tokens[0].lower()=='exclude' and len(tokens)==1:
					self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: exclude called without an argument"])
					no_errors = False

			# |======|
			# | only |
			# |======|
			if len(tokens)>=1:
				if tokens[0].lower()=='only' and len(tokens)>=2:
					tokens.pop(0)
					
					valid = False
					buildTemporaryAliases(self.gui,self.window)
					for e in tokens:
						e = interpolateAliases(e)
						if e.lower()==self.window.name.lower(): valid = True

					if valid==False:
						if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
							self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Script cannot be ran in {self.window.name}"])
						no_errors = False

				elif tokens[0].lower()=='only' and len(tokens)==1:
					self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: only called without an argument"])
					no_errors = False

			# |==========|
			# | restrict |
			# |==========|
			if len(tokens)>=1:
				if tokens[0].lower()=='restrict' and len(tokens)==2:
					tokens.pop(0)
					arg = tokens.pop(0)
					buildTemporaryAliases(self.gui,self.window)
					arg = interpolateAliases(arg)

					if arg.lower()=='server':
						if self.window.window_type!=SERVER_WINDOW:
							if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Script must be ran in server windows"])
							no_errors = False
					elif arg.lower()=='channel':
						if self.window.window_type!=CHANNEL_WINDOW:
							if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Script must be ran in channel windows"])
							no_errors = False
					elif arg.lower()=='private':
						if self.window.window_type!=PRIVATE_WINDOW:
							if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Script must be ran in private chat windows"])
							no_errors = False
					else:
						self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Unrecognized restriction: \"{arg}\""])
						no_errors = False

				elif tokens[0].lower()=='restrict' and len(tokens)==3:
					tokens.pop(0)
					arg1 = tokens.pop(0)
					arg2 = tokens.pop(0)
					buildTemporaryAliases(self.gui,self.window)
					arg1 = interpolateAliases(arg1)
					arg2 = interpolateAliases(arg2)
					valid = False
					if arg1.lower()=='server':
						if self.window.window_type==SERVER_WINDOW: valid = True
					if arg1.lower()=='channel':
						if self.window.window_type==CHANNEL_WINDOW: valid = True
					if arg1.lower()=='private':
						if self.window.window_type==PRIVATE_WINDOW: valid = True
					if arg2.lower()=='server':
						if self.window.window_type==SERVER_WINDOW: valid = True
					if arg2.lower()=='channel':
						if self.window.window_type==CHANNEL_WINDOW: valid = True
					if arg2.lower()=='private':
						if self.window.window_type==PRIVATE_WINDOW: valid = True

					if arg1.lower()!='server' and arg1.lower()!='channel' and arg1.lower()!='private':
						self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Unrecognized restriction: \"{arg1}\""])
						no_errors = False
					elif arg2.lower()!='server' and arg2.lower()!='channel' and arg2.lower()!='private':
						self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Unrecognized restriction: \"{arg2}\""])
						no_errors = False
					elif not valid:
						if self.window.window_type==PRIVATE_WINDOW: reason = "private chat"
						if self.window.window_type==SERVER_WINDOW: reason = "server"
						if self.window.window_type==CHANNEL_WINDOW: reason = "channel"
						if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
							self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Script is restricted from running in {reason} windows"])
						no_errors = False

				elif tokens[0].lower()=='restrict' and len(tokens)==1:
					self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: restrict called without an argument"])
					no_errors = False
				elif tokens[0].lower()=='restrict' and len(tokens)>3:
					self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: restrict called with too many arguments"])
					no_errors = False

			# |=======|
			# | usage |
			# |=======|
			if len(tokens)>=1:
				if tokens[0].lower()=='usage' and len(tokens)>=2:
					tokens.pop(0)
					arg = tokens.pop(0)
					buildTemporaryAliases(self.gui,self.window)
					arg = interpolateAliases(arg)
					try:
						arg = int(arg)
						if config.REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS:
							if len(tokens)>0:
								if len(self.arguments)!=arg:
									self.scriptError.emit([self.gui,self.window,f"{' '.join(tokens)}"])
									no_errors = False
							else:
								if len(self.arguments)!=arg:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Script must be called with {arg} arguments"])
									no_errors = False
						else:
							if len(tokens)>0:
								if len(self.arguments)<arg:
									self.scriptError.emit([self.gui,self.window,f"{' '.join(tokens)}"])
									no_errors = False
							else:
								if len(self.arguments)<arg:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Script must be called with {arg} arguments"])
									no_errors = False
					except:
						self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: usage must be called with a numerical first argument"])
						no_errors = False

			# Usage must be called with at least one argument
			if len(tokens)>=1:
				if tokens[0].lower()=='usage' and len(tokens)==1:
					self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: usage called without an argument"])
					no_errors = False

			# /style can't be called in scripts
			if len(tokens)>=1:
				if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'style':
					self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: {config.ISSUE_COMMAND_SYMBOL}style cannot be called from a script"])
					no_errors = False

			# /settings can't be called in scripts
			if len(tokens)>=1:
				if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'settings':
					self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: {config.ISSUE_COMMAND_SYMBOL}settings cannot be called from a script"])
					no_errors = False

			# /log can't be called in scripts
			if len(tokens)>=1:
				if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'log':
					self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: {config.ISSUE_COMMAND_SYMBOL}log cannot be called from a script"])
					no_errors = False

			# /edit can't be called in scripts
			if len(tokens)>=1:
				if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit':
					self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: {config.ISSUE_COMMAND_SYMBOL}edit cannot be called from a script"])
					no_errors = False

			# /end doesn't take any arguments
			if len(tokens)>=1:
				if tokens[0].lower()=='end' and len(tokens)>1: 
					self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: end called with too many arguments"])
					no_errors = False

			if config.ENABLE_WAIT_COMMAND:
				# Make sure that wait has only one argument
				if len(tokens)>=1:
					if tokens[0].lower()=='wait' and len(tokens)>2:
						self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: wait called with too many arguments"])
						no_errors = False
					if tokens[0].lower()=='wait' and len(tokens)==1:
						self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: wait must be called with a numerical argument"])
						no_errors = False
			else:
				if len(tokens)>=1:
					if tokens[0].lower()=='wait':
						self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: wait has been disabled"])
						no_errors = False

		return no_errors

	def math(self,statement):
		try:
			# Parse the expression into an AST
			tree = ast.parse(statement, mode='eval')
			evaluator = MathEvaluator()
			result = evaluator.visit(tree)
			return [result,False]
		except (SyntaxError, TypeError, ValueError) as e:
			return [e,True]

	def run(self):

		if self.filename==None:
			filename = "script"
		else:
			filename = self.filename

		no_errors = True

		# This should never happen, but if it does...
		# Do not execute any scripts if scripting is disabled
		if not config.SCRIPTING_ENGINE_ENABLED:
			self.scriptError.emit([self.gui,self.window,f"Scripting has been disabled"])
			no_errors = False

		counter = 1
		for a in self.arguments:
			addTemporaryAlias(f"_{counter}",a)
			counter = counter + 1

		if len(self.arguments)>0:
			addTemporaryAlias(f"_0",' '.join(self.arguments))
		else:
			addTemporaryAlias(f"_0",'none')
			
		addTemporaryAlias(f"_ARGS",str(len(self.arguments)))

		if self.filename!=None:
			addTemporaryAlias(f"_FILE",self.filename)
			addTemporaryAlias(f"_SCRIPT",os.path.basename(self.filename))

		self.script = interpolateAliases(self.script)
		
		# First passes through the script,
		# insert any files that are to be
		# /inserted into the script, up to
		# the maximum depth
		if no_errors:
			if config.ENABLE_INSERT_COMMAND:
				counter = 0
				while counter<config.MAXIMUM_INSERT_DEPTH:
					counter = counter + 1
					err = self.process_inserts()
					if err:
						no_errors = False
						break

		# Second pass, check for errors
		if no_errors:
			no_errors = self.check_for_errors(self.script,self.filename)

		# Third pass through the script, here's
		# where we actually do stuff
		if no_errors:

			script = self.script.split("\n")
			index = -1
			loop = True

			while(loop):
				index = index + 1
				line_number = index + 1
				script_only_command = False

				if index==len(script):
					loop =  False
				else:
					line = script[index]

					line = re.sub(re.compile("/\\*.*?\\*/",re.DOTALL ) ,"" ,line)

					tokens = line.split()

					# |======|
					# | halt |
					# |======|
					if len(tokens)>=2:
						if tokens[0].lower()=='halt':
							tokens.pop(0)
							msg = ' '.join(tokens)
							self.scriptError.emit([self.gui,self.window,f"Halt on line {line_number} in {os.path.basename(filename)}: {msg}"])
							loop = False
							continue

					if len(tokens)>0 and len(tokens)<2:
						if tokens[0].lower()=='halt':
							self.scriptError.emit([self.gui,self.window,f"Halt on line {line_number} in {os.path.basename(filename)}"])
							loop = False
							continue
					
					# |====|
					# | if |
					# |====|
					if len(tokens)>=5:
						if tokens[0].lower()=='if':

							if not config.ENABLE_IF_COMMAND:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: if has been disabled"])
								loop = False
								continue

							try:
								stokens = shlex.split(line, comments=False)
							except:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: Error tokenizing if command. Try using quotation marks"])
								loop = False
								continue

							stokens.pop(0)

							buildTemporaryAliases(self.gui,self.window)
							examine = interpolateAliases(stokens.pop(0))
							operator = interpolateAliases(stokens.pop(0))
							target = interpolateAliases(stokens.pop(0))

							r,error = self.math(examine)
							if not error: examine = r

							r,error = self.math(target)
							if not error: target = r

							valid_operator = False
							do_command = False
							if operator.lower()=='(is)':
								examine = str(examine)
								target = str(target)
								valid_operator = True
								if examine.lower()==target.lower():
									do_command = True
							if operator.lower()=='(not)':
								examine = str(examine)
								target = str(target)
								valid_operator = True
								if examine.lower()!=target.lower():
									do_command = True
							if operator.lower()=='(in)':
								examine = str(examine)
								target = str(target)
								valid_operator = True
								if examine.lower() in target.lower():
									do_command = True

							if operator.lower()=='(lt)':
								valid_operator = True
								try:
									ei = float(examine)
								except:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{examine}\" is not a number"])
									loop = False
									continue
								try:
									ti = float(target)
								except:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{target}\" is not a number"])
									loop = False
									continue
								if ei<ti:
									do_command = True

							if operator.lower()=='(gt)':
								valid_operator = True
								try:
									ei = float(examine)
								except:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{examine}\" is not a number"])
									loop = False
									continue
								try:
									ti = float(target)
								except:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{target}\" is not a number"])
									loop = False
									continue
								if ei>ti: 
									do_command = True

							if operator.lower()=='(eq)':
								valid_operator = True
								try:
									ei = float(examine)
								except:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{examine}\" is not a number"])
									loop = False
									continue
								try:
									ti = float(target)
								except:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{target}\" is not a number"])
									loop = False
									continue
								if ei==ti: 
									do_command = True

							if operator.lower()=='(ne)':
								valid_operator = True
								try:
									ei = float(examine)
								except:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{examine}\" is not a number"])
									loop = False
									continue
								try:
									ti = float(target)
								except:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{target}\" is not a number"])
									loop = False
									continue
								if ei!=ti: 
									do_command = True

							if not valid_operator:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{operator}\" is not a valid \"if\" operator"])
								loop = False
								do_command = False
								continue

							if do_command:
								handled_goto = False
								if len(stokens)==2:
									if stokens[0].lower()=='goto':
										if config.ENABLE_GOTO_COMMAND:
											try:
												ln = int(stokens[1])
											except:
												self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{stokens[1]}\" is not a valid line number"])
												loop = False
												continue
											ln = ln - 1
											try:
												code = script[ln]
											except:
												self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{stokens[1]}\" is not a valid line number"])
												loop = False
												continue
											index = ln
											self.execLine.emit([self.gui,self.window,self.id,script[index],index,False])
											handled_goto = True
											continue
										else:
											self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: goto has been disabled"])
											loop = False
											handled_goto = True
											continue
								if not handled_goto:
									self.execLine.emit([self.gui,self.window,self.id,' '.join(stokens),line_number,False])
								script_only_command = True
								continue

					if len(tokens)>0 and len(tokens)<5:
						if tokens[0].lower()=='if':
							self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: if called without enough arguments"])
							loop = False
							continue

					# |=========|
					# | context |
					# |=========|
					if len(tokens)==2:
						if tokens[0].lower()=='context':
							target = tokens[1]

							buildTemporaryAliases(self.gui,self.window)
							target = interpolateAliases(target)

							is_valid = False
							valids = self.gui.getAllConnectedWindows(self.window.client)
							for c in valids:
								if c.name==target:
									self.window = c
									is_valid = True

							if is_valid==False:
								valids = self.gui.getAllAllConnectedWindows()
								for c in valids:
									if c.name==target:
										self.window = c
										is_valid = True

							if is_valid==False:
								valids = self.gui.getAllConnectedServerWindows()
								for w in valids:
									c = w.widget()
									if c.name==target:
										self.window = c
										is_valid = True
									elif target==f"{c.client.server}":
										self.window = c
										is_valid = True
									elif target==f"{c.client.server}:{c.client.port}":
										self.window = c
										is_valid = True

							script_only_command = True

							if not is_valid:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: context cannot find window \"{target}\""])
								loop = False
							else:
								continue

					if len(tokens)>=1:
						if tokens[0].lower()=='context' and len(tokens)==1:
							self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: context called without an argument"])
							script_only_command = True
							loop = False

						if tokens[0].lower()=='context' and len(tokens)>2:
							self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: context called with too many arguments"])
							script_only_command = True
							loop = False

					# |======|
					# | wait |
					# |======|
					if len(tokens)==2:
						if tokens[0].lower()=='wait':
							count = tokens[1]

							buildTemporaryAliases(self.gui,self.window)
							count = interpolateAliases(count)
							try:
								count = float(count)
							except:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: wait called with a non-numerical argument"])
								script_only_command = True
								loop = False
								continue
							time.sleep(count)
							script_only_command = True
							continue

					# |=====|
					# | end |
					# |=====|
					if len(tokens)==1:
						if tokens[0].lower()=='end':
							loop = False
							script_only_command = True
							continue

					# Bypass usage, already handled
					if len(tokens)>=1:
						if tokens[0].lower()=='usage':
							script_only_command = True
							continue

					# Bypass restrict, already handled
					if len(tokens)>=1:
						if tokens[0].lower()=='restrict':
							script_only_command = True
							continue

					# Bypass only, already handled
					if len(tokens)>=1:
						if tokens[0].lower()=='only':
							script_only_command = True
							continue

					# Bypass exclude, already handled
					if len(tokens)>=1:
						if tokens[0].lower()=='exclude':
							script_only_command = True
							continue

					# Bypass if, already handled
					if len(tokens)>=1:
						if tokens[0].lower()=='if':
							script_only_command = True
							continue

					# Bypass insert, already handled
					if len(tokens)>=1:
						if tokens[0].lower()=='insert':
							if config.ENABLE_INSERT_COMMAND:
								script_only_command = True
								continue
							else:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: insert has been disabled"])
								script_only_command = True
								loop = False
								continue

					if len(tokens)==2:
						if tokens[0].lower()=='goto':
							if config.ENABLE_GOTO_COMMAND:
								target = tokens[1]

								buildTemporaryAliases(self.gui,self.window)
								target = interpolateAliases(target)

								try:
									target = int(target)
								except:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{target}\" is not a valid line number"])
									loop = False
									script_only_command = True
									continue
								try:
									code = script[target-1]
								except:
									self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: \"{target}\" is not a valid line number"])
									loop = False
									continue

								index = target-1
								self.execLine.emit([self.gui,self.window,self.id,script[index],index,False])
								script_only_command = True
								continue
							else:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number} in {os.path.basename(filename)}: goto has been disabled"])
								script_only_command = True
								loop = False
								continue
					try:
						self.execLine.emit([self.gui,self.window,self.id,line,line_number,script_only_command])
					except:
						pass

		self.scriptEnd.emit([self.gui,self.id])

def initialize(directory,directory_name,folder):
	global CONFIG_DIRECTORY
	global SCRIPTS_DIRECTORY

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	CONFIG_DIRECTORY = os.path.join(directory,directory_name)
	if not os.path.isdir(CONFIG_DIRECTORY): os.mkdir(CONFIG_DIRECTORY)

	if folder==None: folder="scripts"

	SCRIPTS_DIRECTORY = os.path.join(CONFIG_DIRECTORY,folder)
	if not os.path.isdir(SCRIPTS_DIRECTORY): os.mkdir(SCRIPTS_DIRECTORY)