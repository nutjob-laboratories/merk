#
# ███╗   ███╗██████╗ ██████╗ ██╗  ██╗
# ████╗ ████║╚═══╗██╗██╔══██╗██║ ██╔╝
# ██╔████╔██║███████║██████╔╝█████╔╝
# ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗
# ██║ ╚═╝ ██║ █████╔╝██║  ██║██║  ██╗
# ╚═╝     ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
# Copyright (C) 2026  Daniel Hetrick
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
import zipfile
import shutil

import emoji

from .resources import *
from . import config
from . import user as USER
from . import dialog
from . import plugins
from . import logs
from . import styles
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
MACRO_HELP = {}
MACRO_USAGE = {}

class UserMacro:
	def __init__(self,name,script):
		self.name = name
		self.script = script

def add_macro(name,script,usage=None,mhelp=None):
	e = UserMacro(name,script)
	USER_MACROS[name] = e

	if usage!=None:
		MACRO_USAGE[name] = usage

	if mhelp!=None:
		MACRO_HELP[name] = mhelp

	build_help_and_autocomplete()

def remove_macro(name):
	USER_MACROS.pop(name,'')
	MACRO_USAGE.pop(name,'')
	MACRO_HELP.pop(name,'')

	build_help_and_autocomplete()

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
			config.ISSUE_COMMAND_SYMBOL+"window resize": config.ISSUE_COMMAND_SYMBOL+"window resize ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp time": config.ISSUE_COMMAND_SYMBOL+"ctcp TIME ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp userinfo": config.ISSUE_COMMAND_SYMBOL+"ctcp USERINFO ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp version": config.ISSUE_COMMAND_SYMBOL+"ctcp VERSION ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp source": config.ISSUE_COMMAND_SYMBOL+"ctcp SOURCE ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp finger": config.ISSUE_COMMAND_SYMBOL+"ctcp FINGER ",
			config.ISSUE_COMMAND_SYMBOL+"config import": config.ISSUE_COMMAND_SYMBOL+"config import ",
			config.ISSUE_COMMAND_SYMBOL+"config export": config.ISSUE_COMMAND_SYMBOL+"config export ",
			config.ISSUE_COMMAND_SYMBOL+"window restart": config.ISSUE_COMMAND_SYMBOL+"window restart",
			config.ISSUE_COMMAND_SYMBOL+"window readme": config.ISSUE_COMMAND_SYMBOL+"window readme",
			config.ISSUE_COMMAND_SYMBOL+"window settings": config.ISSUE_COMMAND_SYMBOL+"window settings",
			config.ISSUE_COMMAND_SYMBOL+"window logs": config.ISSUE_COMMAND_SYMBOL+"window logs ",
			config.ISSUE_COMMAND_SYMBOL+"window cascade": config.ISSUE_COMMAND_SYMBOL+"window cascade",
			config.ISSUE_COMMAND_SYMBOL+"window tile": config.ISSUE_COMMAND_SYMBOL+"window tile",
			config.ISSUE_COMMAND_SYMBOL+"window next": config.ISSUE_COMMAND_SYMBOL+"window next",
			config.ISSUE_COMMAND_SYMBOL+"window previous": config.ISSUE_COMMAND_SYMBOL+"window previous",
			config.ISSUE_COMMAND_SYMBOL+"window hotkey": config.ISSUE_COMMAND_SYMBOL+"window hotkey",
			config.ISSUE_COMMAND_SYMBOL+"window ignore": config.ISSUE_COMMAND_SYMBOL+"window ignore",
			config.ISSUE_COMMAND_SYMBOL+"window plugin": config.ISSUE_COMMAND_SYMBOL+"window plugin",
			config.ISSUE_COMMAND_SYMBOL+"window install": config.ISSUE_COMMAND_SYMBOL+"window install ",
			config.ISSUE_COMMAND_SYMBOL+"window uninstall": config.ISSUE_COMMAND_SYMBOL+"window uninstall ",
			config.ISSUE_COMMAND_SYMBOL+"window fullscreen": config.ISSUE_COMMAND_SYMBOL+"window fullscreen",
			config.ISSUE_COMMAND_SYMBOL+"window ontop": config.ISSUE_COMMAND_SYMBOL+"window ontop",
			config.ISSUE_COMMAND_SYMBOL+"window pause": config.ISSUE_COMMAND_SYMBOL+"window pause",
			config.ISSUE_COMMAND_SYMBOL+"window layout": config.ISSUE_COMMAND_SYMBOL+"window layout",
	}

	if not config.ENABLE_HOTKEYS:
		AUTOCOMPLETE_MULTI.pop(config.ISSUE_COMMAND_SYMBOL+"window hotkey",'')
	if not config.ENABLE_IGNORE:
		AUTOCOMPLETE_MULTI.pop(config.ISSUE_COMMAND_SYMBOL+"window ignore",'')
	if not config.ENABLE_PLUGINS:
		AUTOCOMPLETE_MULTI.pop(config.ISSUE_COMMAND_SYMBOL+"window plugin",'')
		AUTOCOMPLETE_MULTI.pop(config.ISSUE_COMMAND_SYMBOL+"window install",'')
		AUTOCOMPLETE_MULTI.pop(config.ISSUE_COMMAND_SYMBOL+"window uninstall",'')
		AUTOCOMPLETE_MULTI.pop(config.ISSUE_COMMAND_SYMBOL+"window pause",'')
	if not config.SCRIPTING_ENGINE_ENABLED:
		AUTOCOMPLETE_MULTI.pop(config.ISSUE_COMMAND_SYMBOL+"window layout",'')

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
			config.ISSUE_COMMAND_SYMBOL+"quote": config.ISSUE_COMMAND_SYMBOL+"quote ",
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
			config.ISSUE_COMMAND_SYMBOL+"clear": config.ISSUE_COMMAND_SYMBOL+"clear",
			config.ISSUE_COMMAND_SYMBOL+"style": config.ISSUE_COMMAND_SYMBOL+"style ",
			config.ISSUE_COMMAND_SYMBOL+"exit": config.ISSUE_COMMAND_SYMBOL+"exit ",
			config.ISSUE_COMMAND_SYMBOL+"config": config.ISSUE_COMMAND_SYMBOL+"config ",
			config.ISSUE_COMMAND_SYMBOL+"ignore": config.ISSUE_COMMAND_SYMBOL+"ignore ",
			config.ISSUE_COMMAND_SYMBOL+"unignore": config.ISSUE_COMMAND_SYMBOL+"unignore ",
			config.ISSUE_COMMAND_SYMBOL+"find": config.ISSUE_COMMAND_SYMBOL+"find ",
			config.ISSUE_COMMAND_SYMBOL+"ping": config.ISSUE_COMMAND_SYMBOL+"ping ",
			config.ISSUE_COMMAND_SYMBOL+"ctcp": config.ISSUE_COMMAND_SYMBOL+"ctcp ",
			config.ISSUE_COMMAND_SYMBOL+"private": config.ISSUE_COMMAND_SYMBOL+"private ",
			config.ISSUE_COMMAND_SYMBOL+"msgbox": config.ISSUE_COMMAND_SYMBOL+"msgbox ",
			config.ISSUE_COMMAND_SYMBOL+"delay": config.ISSUE_COMMAND_SYMBOL+"delay ",
			config.ISSUE_COMMAND_SYMBOL+"hide": config.ISSUE_COMMAND_SYMBOL+"hide ",
			config.ISSUE_COMMAND_SYMBOL+"show": config.ISSUE_COMMAND_SYMBOL+"show ",
			config.ISSUE_COMMAND_SYMBOL+"window": config.ISSUE_COMMAND_SYMBOL+"window ",
			config.ISSUE_COMMAND_SYMBOL+"close": config.ISSUE_COMMAND_SYMBOL+"close ",
			config.ISSUE_COMMAND_SYMBOL+"prints": config.ISSUE_COMMAND_SYMBOL+"prints ",
			config.ISSUE_COMMAND_SYMBOL+"quitall": config.ISSUE_COMMAND_SYMBOL+"quitall",
			config.ISSUE_COMMAND_SYMBOL+"size": config.ISSUE_COMMAND_SYMBOL+"size ",
			config.ISSUE_COMMAND_SYMBOL+"move": config.ISSUE_COMMAND_SYMBOL+"move ",
			config.ISSUE_COMMAND_SYMBOL+"focus": config.ISSUE_COMMAND_SYMBOL+"focus ",
			config.ISSUE_COMMAND_SYMBOL+"reconnect": config.ISSUE_COMMAND_SYMBOL+"reconnect ",
			config.ISSUE_COMMAND_SYMBOL+"reconnectssl": config.ISSUE_COMMAND_SYMBOL+"reconnectssl ",
			config.ISSUE_COMMAND_SYMBOL+"xreconnect": config.ISSUE_COMMAND_SYMBOL+"xreconnect ",
			config.ISSUE_COMMAND_SYMBOL+"xreconnectssl": config.ISSUE_COMMAND_SYMBOL+"xreconnectssl ",
			config.ISSUE_COMMAND_SYMBOL+"user": config.ISSUE_COMMAND_SYMBOL+"user ",
			config.ISSUE_COMMAND_SYMBOL+"macro": config.ISSUE_COMMAND_SYMBOL+"macro ",
			config.ISSUE_COMMAND_SYMBOL+"bind": config.ISSUE_COMMAND_SYMBOL+"bind ",
			config.ISSUE_COMMAND_SYMBOL+"unbind": config.ISSUE_COMMAND_SYMBOL+"unbind ",
			config.ISSUE_COMMAND_SYMBOL+"call": config.ISSUE_COMMAND_SYMBOL+"call ",
			config.ISSUE_COMMAND_SYMBOL+"admin": config.ISSUE_COMMAND_SYMBOL+"admin ",
			config.ISSUE_COMMAND_SYMBOL+"_die": config.ISSUE_COMMAND_SYMBOL+"_die",
			config.ISSUE_COMMAND_SYMBOL+"_connect": config.ISSUE_COMMAND_SYMBOL+"_connect",
			config.ISSUE_COMMAND_SYMBOL+"info": config.ISSUE_COMMAND_SYMBOL+"info ",
			config.ISSUE_COMMAND_SYMBOL+"ison": config.ISSUE_COMMAND_SYMBOL+"ison ",
			config.ISSUE_COMMAND_SYMBOL+"_kill": config.ISSUE_COMMAND_SYMBOL+"_kill ",
			config.ISSUE_COMMAND_SYMBOL+"links": config.ISSUE_COMMAND_SYMBOL+"links",
			config.ISSUE_COMMAND_SYMBOL+"lusers": config.ISSUE_COMMAND_SYMBOL+"lusers",
			config.ISSUE_COMMAND_SYMBOL+"_rehash": config.ISSUE_COMMAND_SYMBOL+"_rehash",
			config.ISSUE_COMMAND_SYMBOL+"wallops": config.ISSUE_COMMAND_SYMBOL+"wallops ",
			config.ISSUE_COMMAND_SYMBOL+"userhost": config.ISSUE_COMMAND_SYMBOL+"userhost ",
			config.ISSUE_COMMAND_SYMBOL+"python": config.ISSUE_COMMAND_SYMBOL+"python ",
			config.ISSUE_COMMAND_SYMBOL+"unmacro": config.ISSUE_COMMAND_SYMBOL+"unmacro ",
			config.ISSUE_COMMAND_SYMBOL+"_trace": config.ISSUE_COMMAND_SYMBOL+"_trace ",
			config.ISSUE_COMMAND_SYMBOL+"browser": config.ISSUE_COMMAND_SYMBOL+"browser ",
			config.ISSUE_COMMAND_SYMBOL+"folder": config.ISSUE_COMMAND_SYMBOL+"folder ",
		}

	# Remove the style command if the style editor is turned off 
	if not config.ENABLE_STYLE_EDITOR:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"style",'')

	if not config.ENABLE_BROWSER_COMMAND:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"browser",'')

	if not config.ENABLE_PLUGIN_EDITOR:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"python",'')

	if not config.ENABLE_PLUGINS:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"call",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"python",'')
	else:
		if not config.ENABLE_CALL_COMMAND:
			AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"call",'')

	if not config.ENABLE_IGNORE:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"ignore",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"unignore",'')

	if not config.ENABLE_HOTKEYS:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"bind",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"unbind",'')

	if not config.ENABLE_ALIASES:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"alias",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"unalias",'')

	if not config.SCRIPTING_ENGINE_ENABLED:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"script",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"edit",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"macro",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"unmacro",'')

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

	W_COMMAND = [
		"<b>move</b>","<b>resize</b>","<b>maximize</b>","<b>minimize</b>",
		"<b>restore</b>","<b>readme</b>","<b>settings</b>","<b>logs</b>",
		"<b>restart</b>","<b>next</b>","<b>previous</b>","<b>cascade</b>",
		"<b>tile</b>","<b>fullscreen</b>","<b>ontop</b>"
	]

	if config.ENABLE_HOTKEYS: W_COMMAND.append("<b>hotkey</b>")
	if config.ENABLE_IGNORE: W_COMMAND.append("<b>ignore</b>")
	if config.ENABLE_PLUGINS:
		W_COMMAND.append("<b>plugin</b>")
		W_COMMAND.append("<b>install</b>")
		W_COMMAND.append("<b>uninstall</b>")
		W_COMMAND.append("<b>pause</b>")
	if config.SCRIPTING_ENGINE_ENABLED:
		W_COMMAND.append("<b>layout</b>")

	W_COMMAND.sort()

	WINDOW_COMMANDS = join_with_and(W_COMMAND)

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
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"quote TEXT...</b>", "Sends unprocessed data to the server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"time</b>", "Requests server time" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"version [SERVER]</b>", "Requests server version" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"list [TERMS]</b>", "Lists or searches channels on the server; use <b>*</b> for multi-character wildcard, <b>?</b> for single character" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"refresh</b>", "Requests a new list of channels from the server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"knock CHANNEL [MESSAGE]</b>", "Requests an invitation to a channel" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"connect SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"connectssl SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server via SSL" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"xconnect SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server & executes connection script" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"xconnectssl SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server via SSL & executes connection script" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"script FILENAME [ARGUMENTS]</b>", "Executes a list of commands in a file" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"style [SERVER] [WINDOW]</b>", "Opens up a window's text style editor" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"alias [TOKEN] [TEXT...]</b>", "Creates an alias that can be referenced by "+config.ALIAS_INTERPOLATION_SYMBOL+"TOKEN" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"unalias TOKEN</b>", "Deletes the alias referenced by "+config.ALIAS_INTERPOLATION_SYMBOL+"TOKEN" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"edit [FILENAME]</b>", "Opens the script editor" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"play FILENAME</b>", "Plays a WAV file" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"print [WINDOW] TEXT...</b>", "Prints text to a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"maximize [SERVER] [WINDOW]</b>", "Maximizes a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"minimize [SERVER] [WINDOW]</b>", "Minimizes a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"restore [SERVER] [WINDOW]</b>", "Restores a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"clear [SERVER] [WINDOW]</b>", "Clears a window's chat display" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"exit [SECONDS]</b>", "Exits the client, with an optional pause of SECONDS before exit" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"config [SETTING] [VALUE...]</b>", "Changes a setting, or displays one or all settings in the configuration file. <i><b>Caution</b>: use at your own risk</i>" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"ignore USER</b>", "Hides a user's chat. USER can be a nickname or hostmask" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"unignore USER</b>", "Un-hides a user's chat. To un-hide all users, use <b>*</b> as the argument" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"find [TERMS]</b>", "Finds filenames that can be found by other commands; use <b>*</b> for multi-character wildcards, and <b>?</b> for single character wildcards" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"ping USER [TEXT]</b>", "Sends a CTCP ping to a user" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"ctcp REQUEST USER</b>", "Sends a CTCP request; valid requests are TIME, VERSION, USERINFO, SOURCE, or FINGER" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"private NICKNAME [MESSAGE]</b>", "Opens a private chat window for NICKNAME" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"msgbox MESSAGE...</b>", "Displays a messagebox with a short message" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"delay SECONDS COMMAND...</b>", "Executes COMMAND after SECONDS seconds" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"hide [SERVER] [WINDOW]</b>", "Hides a subwindow" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"show [SERVER] [WINDOW]</b>", "Shows a subwindow, if hidden; otherwise, shifts focus to that window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"window [COMMAND] [X] [Y]</b>", f"Manipulates the main application window. Valid commands are {WINDOW_COMMANDS}" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"close [SERVER] [WINDOW]</b>", "Closes a subwindow" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"prints [WINDOW]</b>", "Prints a system message to a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"quitall [MESSAGE]</b>", "Disconnects from all IRC servers" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"size [SERVER] [WINDOW] WIDTH HEIGHT</b>", "Resizes a subwindow. Call without arguments to see the current subwindow's size" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"move [SERVER] [WINDOW] X Y</b>", "Moves a subwindow. Call without arguments to see the current subwindow's coordinates" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"focus [SERVER] [WINDOW]</b>", "Sets focus on a subwindow" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"reconnect SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server, reconnecting on disconnection" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"reconnectssl SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server via SSL, reconnecting on disconnection" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"xreconnect SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server & executes connection script, reconnecting on disconnection" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"xreconnectssl SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server via SSL & executes connection script, reconnecting on disconnection" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"user [SETTING] [VALUE...]</b>", "Changes a setting, or displays one or all settings in the user configuration file. <i><b>Caution</b>: use at your own risk</i>" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"macro NAME SCRIPT [USAGE] [HELP]</b>", "Creates a macro, executable with "+config.ISSUE_COMMAND_SYMBOL+"NAME, that executes SCRIPT" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"config export [FILENAME]</b>", "Exports the current configuration file. <i><b>Caution</b>: use at your own risk</i>" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"config import [FILENAME]</b>", "Imports a configuration file. <i><b>Caution</b>: use at your own risk</i>" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"bind SEQUENCE COMMAND...</b>", f"Executes COMMAND when key SEQUENCE is pressed" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"unbind SEQUENCE</b>", f"Removes a bind for SEQUENCE. Pass <b>*</b> as the only argument to remove all binds" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"call METHOD [ARGUMENTS...]</b>", f"Executes METHOD in any plugin that contains METHOD" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"admin [SERVER]</b>", f"Requests administration information" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"_die</b>", f"Instructs the server to shut down. May only be issued by server operators" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"_connect SERVER PORT [REMOTE]</b>", f"Instructs the server to connect to another server. May only be issued by server operators" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"info [TARGET]</b>", f"Requests server information" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"ison NICKNAME(S)...</b>", f"Displays if the specified nicknames are currently online" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"links [REMOTE [MASK]]</b>", f"Requests a list of servers the server is connected to" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"_kill CLIENT COMMENT...</b>", f"Forcibly removes CLIENT from the network. May only be issued by IRC operators" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"lusers [MASK [SERVER]]</b>", f"Requests statistics about the server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"_rehash</b>", f"Causes the server to reprocess and reload configuration files. May only be issued by IRC operators" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"wallops MESSAGE</b>", f"Sends a message to all operators" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"userhost NICK(S)...</b>", f"Requests information about users from the server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"python [FILE]</b>", f"Opens the Python editor" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"unmacro NAME</b>", f"Removes a macro" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"_trace TARGET</b>", f"Executes a trace on a server or user. May only be issued by server operators" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"browser URL</b>", f"Opens URL in the default browser" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"folder PATH [PATH...]</b>", f"Opens PATH(s) in the default file manager" ],
	]

	if config.INCLUDE_SCRIPT_COMMAND_SHORTCUT:
		COMMAND_HELP_INFORMATION.append(["<b>"+config.ISSUE_COMMAND_SYMBOL+"s FILENAME [ARGUMENTS]</b>", f"Shortcut for the {config.ISSUE_COMMAND_SYMBOL}script command"])

	if config.SCRIPTING_ENGINE_ENABLED:
		for m in USER_MACROS:
			name = USER_MACROS[m].name
			script = USER_MACROS[m].script
			if m in MACRO_HELP:
				if m in MACRO_USAGE:
					COMMAND_HELP_INFORMATION.append([ "<b>"+MACRO_USAGE[m]+"</b>", f"{MACRO_HELP[m]}"])
				else:
					COMMAND_HELP_INFORMATION.append([ "<b>"+config.ISSUE_COMMAND_SYMBOL+name+"</b>", f"{MACRO_HELP[m]}"])
			else:
				if m in MACRO_USAGE:
					COMMAND_HELP_INFORMATION.append([ "<b>"+MACRO_USAGE[m]+"</b>", f"Executes script \"{script}\"" ])
				else:
					COMMAND_HELP_INFORMATION.append([ "<b>"+config.ISSUE_COMMAND_SYMBOL+name+"</b>", f"Executes script \"{script}\"" ])

	COPY = []
	for e in COMMAND_HELP_INFORMATION:
		if not config.ENABLE_BROWSER_COMMAND:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"browser URL</b>": continue
		if not config.ENABLE_PLUGIN_EDITOR:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"python [FILE]</b>": continue
		if not config.ENABLE_PLUGINS:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"call METHOD ARGUMENTS...</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"python [FILE]</b>": continue
		else:
			if not config.ENABLE_CALL_COMMAND:
				if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"call METHOD ARGUMENTS...</b>": continue
		if not config.ENABLE_IGNORE:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"ignore USER</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"unignore USER</b>": continue
		if not config.ENABLE_HOTKEYS:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"bind SEQUENCE COMMAND...</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"unbind SEQUENCE</b>": continue
		if not config.ENABLE_USER_COMMAND:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"user [SETTING] [VALUE...]</b>": continue
		if not config.ENABLE_CONFIG_COMMAND:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"config [SETTING] [VALUE...]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"config export [FILENAME]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"config import [FILENAME]</b>": continue
		if not config.ENABLE_DELAY_COMMAND:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"delay SECONDS COMMAND...</b>": continue
		if not config.ENABLE_STYLE_EDITOR:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"style</b>": continue
		if not config.ENABLE_ALIASES:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"alias [TOKEN] [TEXT...]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"unalias TOKEN</b>": continue
		if not config.SCRIPTING_ENGINE_ENABLED:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"script FILENAME</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"edit [FILENAME]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"s FILENAME [ARGUMENTS]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"macro NAME SCRIPT...</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"unmacro NAME</b>": continue
		if not SSL_AVAILABLE:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"connectssl SERVER [PORT] [PASSWORD]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"xconnectssl SERVER [PORT] [PASSWORD]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"reconnectssl SERVER [PORT] [PASSWORD]</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"xreconnectssl SERVER [PORT] [PASSWORD]</b>": continue

		COPY.append(e)

	def ignore_underscore_in_command_name(item):
		return item[0].replace('_', '').casefold()

	COMMAND_HELP_INFORMATION = sorted(COPY,key=ignore_underscore_in_command_name)

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

def addAlias(name,value,gui):
	global ALIAS
	ALIAS[name] = value

	for script_id in gui.scripts:
		if hasattr(gui.scripts[script_id],"updateAlias"):
			try:
				gui.scripts[script_id].updateAlias.emit(name, value)
			except:
				pass

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
			if TEMPORARY_ALIAS[a]==None: continue
			text = text.replace(config.ALIAS_INTERPOLATION_SYMBOL+a,TEMPORARY_ALIAS[a])
		counter = counter + 1
		if counter>=99: break

	if config.ENABLE_EMOJI_SHORTCODES: text = emoji.emojize(text,language=config.EMOJI_LANGUAGE)
	if config.ENABLE_ASCIIMOJI_SHORTCODES: text = emojize(text)

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
	addTemporaryAlias('_DLOGS',logs.LOG_DIRECTORY)
	addTemporaryAlias('_DPLUGINS',plugins.PLUGIN_DIRECTORY)
	addTemporaryAlias('_DSCRIPTS',SCRIPTS_DIRECTORY)
	addTemporaryAlias('_DSETTINGS',config.CONFIG_DIRECTORY)
	addTemporaryAlias('_DSTYLES',styles.STYLE_DIRECTORY)
	addTemporaryAlias('_EDATE',myedate)
	addTemporaryAlias('_EPOCH',f"{datetime.timestamp(datetime.now())}")
	addTemporaryAlias('_LATEST',f"{APPLICATION_DEVELOPMENT}")
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
		addTemporaryAlias('_WTYPE',"server")
	elif window.window_type==CHANNEL_WINDOW:
		addTemporaryAlias('_WTYPE',"channel")
	elif window.window_type==PRIVATE_WINDOW:
		addTemporaryAlias('_WTYPE',"private")
	else:
		addTemporaryAlias('_WTYPE',"unknown")
	addTemporaryAlias('_YEAR',year)

def fullInterpolate(gui,window,user_input):
	buildTemporaryAliases(gui,window)

	user_input = interpolateAliases(user_input)
	clearTemporaryAliases()
	return user_input

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

def find_plugin(filename,extension):

	# Check if it's a complete filename
	if os.path.isfile(filename): return check_readable(filename)

	# Look for the script in the scripts directory
	if os.path.isfile(os.path.join(plugins.PLUGIN_DIRECTORY, filename)): return check_readable(os.path.join(plugins.PLUGIN_DIRECTORY, filename))

	if extension!=None:
		efilename = filename + "." + extension

		# Check if it's a complete filename
		if os.path.isfile(efilename): return check_readable(filename)

		# Look for the script in the scripts directory
		if os.path.isfile(os.path.join(plugins.PLUGIN_DIRECTORY, efilename)): return check_readable(os.path.join(plugins.PLUGIN_DIRECTORY, efilename))

		# Still not found? Case insensitive seach
		for root, dirs, files in os.walk(plugins.PLUGIN_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.{extension}"):
				return check_readable(os.path.join(root, filename))

	for root, dirs, files in os.walk(plugins.PLUGIN_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return check_readable(os.path.join(root, filename))

	return None

def find_file_plugin(filename,extension):

	# Check if it's a complete filename
	if os.path.isfile(filename): return check_readable(filename)

	# Look for the script in the plugins directory
	if os.path.isfile(os.path.join(plugins.PLUGIN_DIRECTORY, filename)): return check_readable(os.path.join(plugins.PLUGIN_DIRECTORY, filename))

	# Look for the script in the scripts directory
	if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, filename)): return check_readable(os.path.join(SCRIPTS_DIRECTORY, filename))

	# Look for the script in the config directory
	if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, filename)): return check_readable(os.path.join(config.CONFIG_DIRECTORY, filename))

	if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES:
		# Look for the script in the install directory
		if os.path.isfile(os.path.join(INSTALL_DIRECTORY, filename)): return check_readable(os.path.join(INSTALL_DIRECTORY, filename))

	if extension!=None:
		efilename = filename + "." + extension

		# Check if it's a complete filename
		if os.path.isfile(efilename): return check_readable(filename)

		# Look for the script in the scripts directory
		if os.path.isfile(os.path.join(plugins.PLUGIN_DIRECTORY, efilename)): return check_readable(os.path.join(plugins.PLUGIN_DIRECTORY, efilename))

		# Look for the script in the scripts directory
		if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, efilename)): return check_readable(os.path.join(SCRIPTS_DIRECTORY, efilename))

		# Look for the script in the config directory
		if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, efilename)): return check_readable(os.path.join(config.CONFIG_DIRECTORY, efilename))

		if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES:
			# Look for the script in the install directory
			if os.path.isfile(os.path.join(INSTALL_DIRECTORY, efilename)): return check_readable(os.path.join(INSTALL_DIRECTORY, efilename))

		# Still not found? Case insensitive seach
		for root, dirs, files in os.walk(plugins.PLUGIN_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.{extension}"):
				return check_readable(os.path.join(root, filename))

		for root, dirs, files in os.walk(SCRIPTS_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.{extension}"):
				return check_readable(os.path.join(root, filename))

		for root, dirs, files in os.walk(config.CONFIG_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.{extension}"):
				return check_readable(os.path.join(root, filename))

		if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES:
			for root, dirs, files in os.walk(INSTALL_DIRECTORY):
				for filename in fnmatch.filter(files, f"{filename}.{extension}"):
					return check_readable(os.path.join(root, filename))

	for root, dirs, files in os.walk(plugins.PLUGIN_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return check_readable(os.path.join(root, filename))

	for root, dirs, files in os.walk(SCRIPTS_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return check_readable(os.path.join(root, filename))

	for root, dirs, files in os.walk(config.CONFIG_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return check_readable(os.path.join(root, filename))

	if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES:
		for root, dirs, files in os.walk(INSTALL_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.*"):
				return check_readable(os.path.join(root, filename))

	return None

def find_file(filename,extension):

	# Check if it's a complete filename
	if os.path.isfile(filename): return check_readable(filename)

	# Look for the script in the scripts directory
	if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, filename)): return check_readable(os.path.join(SCRIPTS_DIRECTORY, filename))

	# Look for the script in the config directory
	if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, filename)): return check_readable(os.path.join(config.CONFIG_DIRECTORY, filename))

	if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES:
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

		if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES:
			# Look for the script in the install directory
			if os.path.isfile(os.path.join(INSTALL_DIRECTORY, efilename)): return check_readable(os.path.join(INSTALL_DIRECTORY, efilename))

		# Still not found? Case insensitive seach
		for root, dirs, files in os.walk(SCRIPTS_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.{extension}"):
				return check_readable(os.path.join(root, filename))

		for root, dirs, files in os.walk(config.CONFIG_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.{extension}"):
				return check_readable(os.path.join(root, filename))

		if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES:
			for root, dirs, files in os.walk(INSTALL_DIRECTORY):
				for filename in fnmatch.filter(files, f"{filename}.{extension}"):
					return check_readable(os.path.join(root, filename))

	for root, dirs, files in os.walk(SCRIPTS_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return check_readable(os.path.join(root, filename))

	for root, dirs, files in os.walk(config.CONFIG_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return check_readable(os.path.join(root, filename))

	if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES:
		for root, dirs, files in os.walk(INSTALL_DIRECTORY):
			for filename in fnmatch.filter(files, f"{filename}.*"):
				return check_readable(os.path.join(root, filename))

	return None

def is_valid_macro_name(name):
	for c in AUTOCOMPLETE:
		if c.lower()==config.ISSUE_COMMAND_SYMBOL+name: return False
	if contains_punctuation(name): return False
	if ' ' in name: return False
	return True

def is_valid_alias_name(name):
	if contains_punctuation(name): return False
	if ' ' in name: return False
	return True

def does_macro_name_exist(name):
	for c in USER_MACROS:
		if USER_MACROS[c].name.lower()==name: return True
	return False

def list_all_macros():
	ret = []
	for m in USER_MACROS:
		name = USER_MACROS[m].name
		script = USER_MACROS[m].script
		if m in MACRO_HELP:
			if m in MACRO_USAGE:
				ret.append(MACRO_USAGE[m]+" - "+MACRO_HELP[m])
			else:
				ret.append(config.ISSUE_COMMAND_SYMBOL+name+" - "+MACRO_HELP[m])
		else:
			if m in MACRO_USAGE:
				ret.append(MACRO_USAGE[m]+f" - Executes script \"{script}\"")
			else:
				ret.append(config.ISSUE_COMMAND_SYMBOL+name+f" - Executes script \"{script}\"")
	return ret

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

		if gui.scripts[script_id].filename==None:
			script_file = 'script'
		else:
			script_file = os.path.basename(gui.scripts[script_id].filename)

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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: end called with too many arguments")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					if config.PRINT_SCRIPT_ERRORS_TO_STDOUT:
						sys.stdout.write(f"{script_file}, line {line_number}: end called with too many arguments\n")
					return

		if config.DISPLAY_SCRIPT_ERRORS:
			# Check to make sure this isn't being thrown by script
			# only commands
			if not script_only_command:
				if line[0]==config.ISSUE_COMMAND_SYMBOL:
					add_halt(script_id)
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Unrecognized command \"{line}\"")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					add_halt(script_id)
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Line \"{line}\" contains no command")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

		if config.PRINT_SCRIPT_ERRORS_TO_STDOUT:
			if not script_only_command:
				if line[0]==config.ISSUE_COMMAND_SYMBOL:
					sys.stdout.write(f"{script_file}, line {line_number}: Unrecognized command \"{line}\"\n")
				else:
					sys.stdout.write(f"{script_file}, line {line_number}: Line \"{line}\" contains no command\n")

def execute_script_error(data):
	gui = data[0]
	window = data[1]
	line = data[2]

	if config.PRINT_SCRIPT_ERRORS_TO_STDOUT:
		sys.stdout.write(f"{line}\n")

	if config.DISPLAY_SCRIPT_ERRORS:
		t = Message(ERROR_MESSAGE,'',line)
		window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

def execute_script_alias(data):
	alias = data[0]
	value = data[1]
	gui = data[2]

	addAlias(alias,value,gui)

def execute_script_end(data):
	gui = data[0]
	script_id = data[1]
	aliases_to_destroy = data[2]

	gui.scripts[script_id].quit()
	gui.scripts[script_id].wait(config.SCRIPT_THREAD_QUIT_TIMEOUT)

	del gui.scripts[script_id]

	for alias in aliases_to_destroy:
		removeAlias(alias)

	remove_halt(script_id)

def executeScript(gui,window,text,filename=None,args=[]):

	script_id = str(uuid.uuid4())
	gui.scripts[script_id] = ScriptThread(text,script_id,gui,window,args,filename)
	gui.scripts[script_id].execLine.connect(execute_script_line)
	gui.scripts[script_id].scriptEnd.connect(execute_script_end)
	gui.scripts[script_id].scriptError.connect(execute_script_error)
	gui.scripts[script_id].scriptAlias.connect(execute_script_alias)
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

	if setting=="alias_interpolation_symbol":
		if "*" in value: return INVALID_VALUE
		if "<" in value: return INVALID_VALUE
		if ">" in value: return INVALID_VALUE
		if "\\" in value: return INVALID_VALUE
		if "~" in value: return INVALID_VALUE
		if "/" in value: return INVALID_VALUE

	if setting=="issue_command_symbol":
		if "*" in value: return INVALID_VALUE
		if "<" in value: return INVALID_VALUE
		if ">" in value: return INVALID_VALUE
		if "~" in value: return INVALID_VALUE
		if "/" in value and value!="/": return INVALID_VALUE

	if setting=="mdi_workspace_background":
		if value=="": return ALL_VALID_SETTINGS
		if not os.path.isfile(value): return INVALID_IMAGE
		pixmap = QPixmap()
		if not pixmap.load(value): return INVALID_IMAGE
		if pixmap.isNull(): return INVALID_IMAGE

	if setting=="qt_window_style":
		if not value in QT_STYLES: return INVALID_STYLE

	if setting=="windowbar_justify":
		if value.lower()!="left" and value.lower()!="right" and value.lower()!="center": return INVALID_JUSTIFY

	if setting=="menubar_justify":
		if value.lower()!="left" and value.lower()!="right" and value.lower()!="center": return INVALID_JUSTIFY

	if setting=="syntax_nickname_color":
		if not QColor(value).isValid(): return INVALID_COLOR

	if setting=="syntax_shortcode_color":
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
		for e in value.split():
			if e.lower() in v: continue
			return INVALID_TEXT_STYLE

	if setting=="syntax_command_style":
		for e in value.split():
			if e.lower() in v: continue
			return INVALID_TEXT_STYLE

	if setting=="syntax_channel_style":
		for e in value.split():
			if e.lower() in v: continue
			return INVALID_TEXT_STYLE

	if setting=="syntax_alias_style":
		for e in value.split():
			if e.lower() in v: continue
			return INVALID_TEXT_STYLE

	if setting=="syntax_script_only_style":
		for e in value.split():
			if e.lower() in v: continue
			return INVALID_TEXT_STYLE

	if setting=="syntax_operator_style":
		for e in value.split():
			if e.lower() in v: continue
			return INVALID_TEXT_STYLE

	if setting=="syntax_nickname_style":
		for e in value.split():
			if e.lower() in v: continue
			return INVALID_TEXT_STYLE

	if setting=="syntax_shortcode_style":
		for e in value.split():
			if e.lower() in v: continue
			return INVALID_TEXT_STYLE

	v = ["creation","stacking","activation"]
	if setting=="subwindow_order":
		if not value.lower() in v: return INVALID_ORDER

	if setting=="sound_notification_file":
		efilename = find_file(value,"wav")
		if efilename!=None:
			if not is_wav_file(efilename): return INVALID_SOUND
		else:
			return INVALID_SOUND

	if setting=="timestamp_format":
		test_date_string = "2025-10-29 14:30:00"
		try:
			datetime.strptime(test_date_string, value)
		except ValueError:
			return INVALID_TIME

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
	if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES:
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
			if hasattr(gui.scripts[script_id],"filename"):
				if gui.scripts[script_id].filename==None:
					script_file = 'script'
				else:
					script_file = os.path.basename(gui.scripts[script_id].filename)
			else:
				script_file = 'command'
			if is_halting(script_id): return True

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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: You can't invite a user to a private chat")
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
					if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
					if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
			window.client.describe(window.name,msg)
			t = Message(ACTION_MESSAGE,window.client.nickname,msg)
			window.writeText(t)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'me':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"me MESSAGE")
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
					if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
					if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
					window.client.topic(channel,msg)
					return True
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Can't set topic for a private chat")
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
			msg = config.DEFAULT_QUIT_MESSAGE
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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
				if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
				if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
				if config.ENABLE_EMOJI_SHORTCODES:  msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
				if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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
			if hasattr(gui.scripts[script_id],"filename"):
				if gui.scripts[script_id].filename==None:
					script_file = 'script'
				else:
					script_file = os.path.basename(gui.scripts[script_id].filename)
			else:
				script_file = 'command'
			if is_halting(script_id): return True

	# |---------------|
	# | Insert macros |
	# |---------------|
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

	# |---------|
	# | /folder |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'folder' and len(tokens)>=2:
			tokens.pop(0)
			dirs = shlex.split(' '.join(tokens), comments=False)
			for d in dirs:
				if os.path.isdir(d):
					gui.open_folder(d)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{d}\" is not a valid path")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{d}\" is not a valid path")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'folder':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"folder PATH")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"folder PATH")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /browser |
	# |----------|
	if len(tokens)>=1:

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'browser' and len(tokens)>=1:
			if not config.ENABLE_BROWSER_COMMAND:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}browser has been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}browser has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'browser' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			if has_url(target) and target.count(' ')==0:
				gui.openLinkInBrowser(target)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{target}\" is not a valid URL")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{target}\" is not a valid URL")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'browser':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"browser URL")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"browser URL")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /_trace |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_trace' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			window.client.sendLine(f'TRACE {target}')
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_trace':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"_trace TARGET")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"_trace TARGET")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /python |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'python' and len(tokens)>=1:
			if not config.ENABLE_PLUGINS:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}python: Plugins are disabled")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Plugins are disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			if not config.ENABLE_PLUGIN_EDITOR:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}python: The Python editor has been disabled")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"The Python editor has been disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			if len(tokens)>=2:
				tokens.pop(0)
				file = " ".join(tokens)
			else:
				file = None
			gui.openPythonEditorCommand(file)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'python':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"python [FILE]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"python [FILE]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-----------|
	# | /userhost |
	# |-----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'userhost' and len(tokens)>=2:
			tokens.pop(0)
			msg = " ".join(tokens)
			window.client.sendLine('USERHOST '+msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'userhost':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"userhost NICK(S)...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"userhost NICK(S)...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /wallops |
	# |----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'wallops' and len(tokens)>=2:
			tokens.pop(0)
			msg = " ".join(tokens)
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
			window.client.sendLine('WALLOPS '+msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'wallops':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"wallops MESSAGE")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"wallops MESSAGE")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /_rehash |
	# |----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_rehash' and len(tokens)==1:
			window.client.sendLine('REHASH')
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_rehash':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"_rehash")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"_rehash")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /lusers |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'lusers' and len(tokens)>=2:
			tokens.pop(0)
			target = ' '.join(tokens)
			window.client.sendLine('LUSERS '+target)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'lusers' and len(tokens)==1:
			tokens.pop(0)
			window.client.sendLine('LUSERS')
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'lusers':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"lusers [MASK [SERVER]]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"lusers [MASK [SERVER]]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /links |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'links' and len(tokens)>=2:
			tokens.pop(0)
			target = ' '.join(tokens)
			window.client.sendLine('LINKS '+target)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'links' and len(tokens)==1:
			tokens.pop(0)
			window.client.sendLine('LINKS')
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'links':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"links [REMOTE [MASK]]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"links [REMOTE [MASK]]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /_kill |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_kill' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			comment = ' '.join(tokens)
			window.client.sendLine('KILL '+target+' '+comment)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_kill':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"_kill CLIENT COMMENT...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"_kill CLIENT COMMENT...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /ison |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ison' and len(tokens)>=2:
			tokens.pop(0)
			target = ' '.join(tokens)
			window.client.sendLine('ISON '+target)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ison':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"ison NICKNAME(S)...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"ison NICKNAME(S)...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /info |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'info' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			window.client.sendLine('INFO '+target)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'info' and len(tokens)==1:
			window.client.sendLine('INFO')
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'info':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"info [TARGET]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"info [TARGET]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-----------|
	# | /_connect |
	# |-----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_connect' and len(tokens)==3:
			tokens.pop(0)
			target = tokens.pop(0)
			port = tokens.pop(0)
			window.client.sendLine('CONNECT '+target+' '+port)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_connect' and len(tokens)==4:
			tokens.pop(0)
			target = tokens.pop(0)
			port = tokens.pop(0)
			remote = tokens.pop(0)
			window.client.sendLine('CONNECT '+target+' '+port+' '+remote)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_connect':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"_connect SERVER PORT [REMOTE]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"_connect SERVER PORT [REMOTE]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /_die |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_die' and len(tokens)==1:
			window.client.sendLine('DIE')
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'_die':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"_die")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"_die")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /admin |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'admin' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			window.client.sendLine('ADMIN '+target)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'admin' and len(tokens)==1:
			window.client.sendLine('ADMIN')
			return True

	# |-------|
	# | /call |
	# |-------|
	if len(tokens)>=1:

		if not config.ENABLE_PLUGINS:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'call':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}call: Plugins are disabled")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Plugins are disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if not config.ENABLE_CALL_COMMAND:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'call':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}call has been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}call has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'call' and len(tokens)>=2:
			tokens.pop(0)
			method = tokens.pop(0)

			mcheck = plugins.is_valid_call_method(method)
			if mcheck==NO_METHOD:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}call: Plugin method \"{method}\" can't be found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Plugin method \"{method}\" can't be found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			elif mcheck==INVALID_METHOD:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}call: Plugin method \"{method}\" accepts the wrong number of arguments")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Plugin method \"{method}\" accepts the wrong number of arguments")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			elif mcheck==EVENT_METHOD or mcheck==BUILT_IN_METHOD:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}call: Plugin method \"{method}\" can't be called")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Plugin method \"{method}\" can't be called")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			if len(tokens)==0:
				args = []
			else:
				args = shlex.split(' '.join(tokens), comments=False)

			plugins.command_call(gui,window,method,args)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'call':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"call METHOD [ARGUMENTS...]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"call METHOD [ARGUMENTS...]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /unbind |
	# |---------|
	if len(tokens)>=1:

		if not config.ENABLE_HOTKEYS:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unbind':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}unbind: Hotkeys are disabled")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Hotkeys are disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unbind' and len(tokens)==2:
			tokens.pop(0)
			seq = tokens.pop(0)

			if seq=='*':
				gui.remove_all_shortcuts()
				if not is_script:
					t = Message(SYSTEM_MESSAGE,'',f"All binds removed")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				gui.save_shortcuts()
				if gui.hotkey_manager!=None:
					gui.hotkey_manager.refresh()
				return True

			gui.remove_shortcut(seq)
			if not is_script:
				t = Message(SYSTEM_MESSAGE,'',f"Bind for \"{seq}\" removed")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			gui.save_shortcuts()
			if gui.hotkey_manager!=None:
				gui.hotkey_manager.refresh()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unbind':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"unbind SEQUENCE")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"unbind SEQUENCE")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /bind |
	# |-------|
	if len(tokens)>=1:

		if not config.ENABLE_HOTKEYS:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'bind':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}bind: Hotkeys are disabled")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Hotkeys are disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'bind' and len(tokens)==1:
			r = gui.list_all_shortcuts()
			if len(r)>0:
				t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(r)} binds")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				for i in r:
					t = Message(SYSTEM_MESSAGE,'',f"{i}")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {len(r)} binds")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(SYSTEM_MESSAGE,'',f"No binds found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'bind' and len(tokens)>=3:
			tokens.pop(0)
			seq = tokens.pop(0)
			cmd = ' '.join(tokens)

			r = gui.add_shortcut(seq,cmd)
			if r==BAD_SHORTCUT:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+f"bind: \"{seq}\" is not a valid key sequence")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{seq}\" is not a valid key sequence")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			elif r==SHORTCUT_IN_USE:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+f"bind: \"{seq}\" is already in use as a shortcut")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{seq}\" is already in use as a shortcut")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if not is_script:
					t = Message(SYSTEM_MESSAGE,'',f"Bind for \"{seq}\" added (executes \"{cmd}\")")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				gui.save_shortcuts()
				if gui.hotkey_manager!=None:
					gui.hotkey_manager.refresh()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'bind':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"bind SEQUENCE COMMAND...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"bind SEQUENCE COMMAND...")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /macro |
	# |--------|
	if len(tokens)>=1:
		if not config.SCRIPTING_ENGINE_ENABLED:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'macro':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: Scripting is disabled")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# /macro
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'macro' and len(tokens)==1:
			r = list_all_macros()
			if len(r)>0:
				t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(r)} macros")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				for i in r:
					t = Message(SYSTEM_MESSAGE,'',f"{i}")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {len(r)} macros")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(SYSTEM_MESSAGE,'',f"No macros found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		# /macro name script
		try:
			stokens = shlex.split(user_input, comments=False)
		except:
			stokens = user_input.split()
		if stokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'macro' and len(stokens)==3:
			stokens.pop(0)
			name = stokens.pop(0)
			script = stokens.pop(0)

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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: Macro names must begin with a letter")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: \""+name+"\" is not a valid macro name")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: \""+script+"\" doesn't exist or is not readable")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"\""+script+"\" doesn't exist or is not readable")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			if does_macro_name_exist(name):
				t = Message(SYSTEM_MESSAGE,'',f"Replacing macro \"{name}\", executing \"{efilename}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(SYSTEM_MESSAGE,'',f"Adding macro \"{name}\", executing \"{efilename}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			add_macro(name,script)
			return True

		# /macro name script usage
		try:
			stokens = shlex.split(user_input, comments=False)
		except:
			stokens = user_input.split()
		if stokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'macro' and len(stokens)==4:
			stokens.pop(0)
			name = stokens.pop(0)
			script = stokens.pop(0)
			usage = stokens.pop(0)

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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: Macro names must begin with a letter")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: \""+name+"\" is not a valid macro name")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: \""+script+"\" doesn't exist or is not readable")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"\""+script+"\" doesn't exist or is not readable")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			if does_macro_name_exist(name):
				t = Message(SYSTEM_MESSAGE,'',f"Replacing macro \"{name}\", executing \"{efilename}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(SYSTEM_MESSAGE,'',f"Adding macro \"{name}\", executing \"{efilename}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			add_macro(name,script,usage)
			return True

		# /macro name script usage help
		try:
			stokens = shlex.split(user_input, comments=False)
		except:
			stokens = user_input.split()
		if stokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'macro' and len(stokens)==5:
			stokens.pop(0)
			name = stokens.pop(0)
			script = stokens.pop(0)
			usage = stokens.pop(0)
			mhelp = stokens.pop(0)

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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: Macro names must begin with a letter")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: \""+name+"\" is not a valid macro name")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}macro: \""+script+"\" doesn't exist or is not readable")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"\""+script+"\" doesn't exist or is not readable")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			if does_macro_name_exist(name):
				t = Message(SYSTEM_MESSAGE,'',f"Replacing macro \"{name}\", executing \"{efilename}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(SYSTEM_MESSAGE,'',f"Adding macro \"{name}\", executing \"{efilename}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			add_macro(name,script,usage,mhelp)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'macro':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"macro NAME SCRIPT [USAGE] [HELP]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"macro NAME SCRIPT [USAGE] [HELP]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |----------|
	# | /unmacro |
	# |----------|
	if len(tokens)>=1:
		if not config.SCRIPTING_ENGINE_ENABLED:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unmacro':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}unmacro: Scripting is disabled")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if stokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unmacro' and len(stokens)==2:
			stokens.pop(0)
			name = stokens.pop(0)

			if does_macro_name_exist(name):
				remove_macro(name)
				if not is_script:
					t = Message(SYSTEM_MESSAGE,'',f"Macro \"{name}\" removed")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Macro \"{name}\" doesn't exist")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Macro \"{name}\" doesn't exist")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unmacro':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"unmacro NAME")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"unmacro NAME")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}user has been disabled in settings")
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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: No settings found containing \"{my_setting}\"")
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

			if my_setting.lower()=='nickname' or my_setting.lower()=='alternate' or my_setting.lower()=='username':
				if is_invalid_nickname(my_value):
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{my_value}\" is not a valid value for {my_setting}")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{my_value}\" is not a valid value for {my_setting}")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			if my_setting in settings:
				if type(settings[my_setting])==list or type(settings[my_setting])==dict:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{my_setting}\" cannot be changed with the {config.ISSUE_COMMAND_SYMBOL}user command")
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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{my_value}\" is not a valid value for \"{my_setting}\" (value is {itype}, requires {dtype})")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}: Error on line: {line_number}: \"{my_setting}\" is not a valid user setting")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}reconnectssl: \"{port}\" is not a number")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}reconnectssl: \"{port}\" is not a number")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"reconnectssl HOST [PORT] [PASSWORD]")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}reconnect: \"{port}\" is not a number")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}reconnect: \"{port}\" is not a number")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"reconnect HOST [PORT] [PASSWORD]")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xreconnectssl: \"{port}\" is not a number")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xreconnectssl: \"{port}\" is not a number")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"xreconnectssl HOST [PORT] [PASSWORD]")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xreconnect: \"{port}\" is not a number")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xreconnect: \"{port}\" is not a number")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"xreconnect HOST [PORT] [PASSWORD]")
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
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}focus: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.widget().input.setFocus()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}focus: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Server \""+server+"\" not found")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}focus: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"focus [SERVER] [WINDOW]")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid X value")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid Y value")
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
									t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Not a valid window position")
									window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
								return True
							t = Message(ERROR_MESSAGE,'',"Not a valid window position")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						if gui.is_valid_position(w,x_val,y_val):
							w.move(x_val,y_val)
						else:
							if is_script:
								add_halt(script_id)
								if config.DISPLAY_SCRIPT_ERRORS:
									t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Not a valid window position")
									window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
								return True
							t = Message(ERROR_MESSAGE,'',"Not a valid window position")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Server \""+server+"\" not found")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid X value")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid Y value")
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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Not a valid window position")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Not a valid window position")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Window \""+target+"\" not found")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid X value")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Invalid Y value")
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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Not a valid window position")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Not a valid window position")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}move: Window \""+window.name+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+window.name+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'move' and len(tokens)==1:
			w = gui.getSubWindow(window.name,window.client)
			x_val = w.x()
			y_val = w.y()
			t = Message(SYSTEM_MESSAGE,'',f"{window.name}: X:{x_val} Y:{y_val}")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'move' and len(tokens)>4:
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"move [SERVER] [WINDOW] X Y")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"move [SERVER] [WINDOW] X Y")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /size |
	# |-------|
	if len(tokens)>=1:

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'size' and len(tokens)==5:
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Invalid width")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid width passed to {config.ISSUE_COMMAND_SYMBOL}size")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			height = is_int(height)
			if height==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Invalid height")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid height passed to {config.ISSUE_COMMAND_SYMBOL}size")
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
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.resize(width,height)
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'size' and len(tokens)==4:
			tokens.pop(0)
			target = tokens.pop(0)
			width = tokens.pop(0)
			height = tokens.pop(0)

			width = is_int(width)
			if width==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Invalid width")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid width passed to {config.ISSUE_COMMAND_SYMBOL}size")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			height = is_int(height)
			if height==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Invalid height")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid height passed to {config.ISSUE_COMMAND_SYMBOL}size")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			w = gui.getSubWindow(target,window.client)
			if w:
				w.resize(width,height)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'size' and len(tokens)==3:
			tokens.pop(0)
			width = tokens.pop(0)
			height = tokens.pop(0)

			width = is_int(width)
			if width==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Invalid width")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid width passed to {config.ISSUE_COMMAND_SYMBOL}size")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			height = is_int(height)
			if height==None:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Invalid height")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Invalid height passed to {config.ISSUE_COMMAND_SYMBOL}size")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			w = gui.getSubWindow(window.name,window.client)
			if w:
				w.resize(width,height)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}size: Window \""+window.name+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+window.name+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'size' and len(tokens)==1:
			w = gui.getSubWindow(window.name,window.client)
			width = w.width()
			height = w.height()
			t = Message(SYSTEM_MESSAGE,'',f"{window.name}: {width}x{height}")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'size' and len(tokens)>4:
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"size [SERVER] [WINDOW] WIDTH HEIGHT")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"size [SERVER] [WINDOW] WIDTH HEIGHT")
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

			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)

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
					if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
					if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
					t = Message(SYSTEM_MESSAGE,'',f"{msg}")
					w.widget().writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: No text to print")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"No text to print")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			msg = target+' '+' '.join(tokens)
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"prints [WINDOW] TEXT")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"prints [WINDOW] TEXT")
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
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}close: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.close()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}close: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}close: Server \""+server+"\" not found")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}close: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'close':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"close [SERVER] [WINDOW]")
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
				width = w.width()
				height = w.height()
				x_val = w.x()
				y_val = w.y()
				c = w.widget()
				if c.window_type==CHANNEL_WINDOW:
					entry = f"{c.name} - Channel ({c.client.server}:{c.client.port}, {v}, {width}x{height}, X:{x_val} Y:{y_val})"
				elif c.window_type==PRIVATE_WINDOW:
					entry = f"{c.name} - Private Chat ({c.client.server}:{c.client.port}, {v}, {width}x{height}, X:{x_val} Y:{y_val})"
				elif c.window_type==SERVER_WINDOW:
					entry = f"{c.name} - Server ({c.client.server}:{c.client.port}, {v}, {width}x{height}, X:{x_val} Y:{y_val})"
				results.append(entry)

			if len(results)>1:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(results)} windows")
			else:
				t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(results)} window")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

			mdi_viewport = gui.MDI.viewport()
			viewport_size = mdi_viewport.size()
			screen = gui.app.primaryScreen()
			size = screen.size()

			t = Message(SYSTEM_MESSAGE,'',f"Desktop area: {size.width()}x{size.height()}")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

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

		# /window layout
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='layout':

				if not config.SCRIPTING_ENGINE_ENABLED:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window layout: Scripting is disabled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Scripting is disabled")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				results = []
				for w in gui.getAllAllConnectedSubWindows():
					if w.isVisible():
						width = w.width()
						height = w.height()
						x_val = w.x()
						y_val = w.y()
						results.append(f"/size {w.widget().client.server}:{w.widget().client.port} {w.widget().name} {width} {height}")
						results.append(f"/move {w.widget().client.server}:{w.widget().client.port} {w.widget().name} {x_val} {y_val}")
				if len(results)>0:
					results.insert(0,f"/rem Subwindow layout for {datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('%A %B %d, %Y')}")
					gui.newEditorWindowContents("\n".join(results))
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: No visible windows found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"No visible windows found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# /window ontop
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='ontop':
				if gui.ontop:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: On-top mode is turned on by command-line flag")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"On-top mode is turned on by command-line flag")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if config.ALWAYS_ON_TOP:
					config.ALWAYS_ON_TOP = False
					gui.setWindowFlags(gui.windowFlags() & ~Qt.WindowStaysOnTopHint)
					if gui.hotkey_manager!=None: gui.hotkey_manager.toggleTop()
					if gui.ignore_manager!=None: gui.ignore_manager.toggleTop()
					if gui.plugin_manager!=None: gui.plugin_manager.toggleTop()
					gui.show()
				else:
					config.ALWAYS_ON_TOP = True
					gui.setWindowFlags(gui.windowFlags() | Qt.WindowStaysOnTopHint)
					if gui.hotkey_manager!=None: gui.hotkey_manager.toggleTop()
					if gui.ignore_manager!=None: gui.ignore_manager.toggleTop()
					if gui.plugin_manager!=None: gui.plugin_manager.toggleTop()
					gui.show()
				config.save_settings(config.CONFIG_FILE)
				gui.buildSettingsMenu()
				return True

		# /window fullscreen
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='fullscreen':
				if gui.fullscreen:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Full screen mode is turned on by command-line flag")
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

		# /window pause
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='pause':
				if not config.ENABLE_PLUGINS:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window pause: Plugins are disabled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Plugins are disabled")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				if len(plugins.PLUGINS)>0:
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(plugins.PLUGINS)} plugins")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					for p in plugins.PLUGINS:
						if plugins.paused(p):
							t = Message(SYSTEM_MESSAGE,'',f"{p._class} - {p.NAME} {p.VERSION} ({p._basename}) (paused)")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(SYSTEM_MESSAGE,'',f"{p._class} - {p.NAME} {p.VERSION} ({p._basename})")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',"End plugin list")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(SYSTEM_MESSAGE,'',f"No plugins installed")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==3:
			if tokens[1].lower()=='pause':
				if not config.ENABLE_PLUGINS:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window pause: Plugins are disabled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Plugins are disabled")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				tokens.pop(0)
				tokens.pop(0)
				target = tokens.pop(0)
				for p in plugins.PLUGINS:
					if target==p._class:
						if plugins.paused(p):
							plugins.unpause(p)
							t = Message(SYSTEM_MESSAGE,'',f"Plugin {target} unpaused")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							plugins.pause(p)
							t = Message(SYSTEM_MESSAGE,'',f"Plugin {target} paused")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window pause: Plugin \"{target}\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Plugin \"{target}\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# /window install
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='install':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"window install FILE")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"window install FILE")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# /window uninstall
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='uninstall':
				if not config.ENABLE_PLUGINS:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window uninstall: Plugins are disabled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Plugins are disabled")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				p = plugins.list_all_plugins()
				if len(p)>0:
					count = 0
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {len(p)} plugins")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					for plug in p:
						count = count + 1
						t = Message(SYSTEM_MESSAGE,'',f"{count}) {plug} ({p[plug]})")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {len(p)} plugins")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(SYSTEM_MESSAGE,'',f"No plugins installed")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# /window uninstall FILE
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==3:
			if tokens[1].lower()=='uninstall':

				if not config.ENABLE_PLUGINS:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window uninstall: Plugins are disabled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Plugins are disabled")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				
				tokens.pop(0)
				tokens.pop(0)
				plugin = tokens.pop(0)

				file_path = os.path.join(plugins.PLUGIN_DIRECTORY, plugin)
				name_without_extension, extension = os.path.splitext(plugin)
				icon_path = os.path.join(plugins.PLUGIN_DIRECTORY, name_without_extension+".png")
				uninstalled_plugin = plugins.get_plugin(file_path)

				uninstalled = False
				if os.path.exists(file_path) and file_path.endswith(".py"):
					try:
						os.remove(file_path)
						uninstalled = True
					except OSError as e:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {e}")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',f"{e}")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True

				if os.path.exists(icon_path) and icon_path.endswith(".png"):
					try:
						os.remove(icon_path)
					except OSError as e:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {e}")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',f"{e}")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
				if uninstalled:
					if config.RELOAD_PLUGINS_AFTER_UNINSTALL:
						plugins.call(gui,"unload")
						if uninstalled_plugin!=None: plugins.uninstall(uninstalled_plugin)
						errors = plugins.load_plugins(gui)
						if len(errors)>0:
							if is_script:
								add_halt(script_id)
								if config.DISPLAY_SCRIPT_ERRORS:
									t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Plugin load errors: {', '.join(errors)}")
									window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
								return True
							t = Message(ERROR_MESSAGE,'',f"Plugin load errors: {', '.join(errors)}")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(SYSTEM_MESSAGE,'',f"Plugin \"{plugin}\" uninstalled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					else:
						if uninstalled_plugin!=None:
							plugins.remove_plugin(uninstalled_plugin)
							if gui.plugin_manager!=None: gui.plugin_manager.refresh()
							t = Message(SYSTEM_MESSAGE,'',f"Plugin \"{plugin}\" uninstalled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							if is_script:
								add_halt(script_id)
								if config.DISPLAY_SCRIPT_ERRORS:
									t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window uninstall: \"{plugin}\" uninstalled, but not removed from memory")
									window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
								return True
							t = Message(ERROR_MESSAGE,'',f"\"{plugin}\" uninstalled, but not removed from memory")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				else:
					t = Message(SYSTEM_MESSAGE,'',f"Plugin \"{plugin}\" was not uninstalled, or does not exist")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				return True

		# /window install FILE
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)>=3:
			if tokens[1].lower()=='install':
				if not config.ENABLE_PLUGINS:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window install: Plugins are disabled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Plugins are disabled")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				
				tokens.pop(0)
				tokens.pop(0)
				file = " ".join(tokens)

				efile = find_file(file,None)
				if not efile:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{file}\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{file}\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				
				file = efile

				base = os.path.basename(file)
				name_without_extension, extension = os.path.splitext(file)
				if extension==".py":
					imported_file = os.path.join(plugins.PLUGIN_DIRECTORY,base)

					if not config.OVERWRITE_PLUGINS_ON_IMPORT:
						if os.path.isfile(imported_file):
							if is_script:
								add_halt(script_id)
								if config.DISPLAY_SCRIPT_ERRORS:
									t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{imported_file}\" already exists")
									window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
								return True
							t = Message(ERROR_MESSAGE,'',f" \"{imported_file}\" already exists")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True

					try:
						shutil.copy(file, imported_file)
					except FileNotFoundError:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{file}\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',f"\"{file}\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					except Exception as e:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {e}")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',f"{e}")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True

					plugin_icon = name_without_extension + ".png"
					if os.path.isfile(plugin_icon):
						base = os.path.basename(plugin_icon)
						imported_file = os.path.join(plugins.PLUGIN_DIRECTORY,base)
						try:
							shutil.copy(plugin_icon, imported_file)
						except FileNotFoundError:
							if is_script:
								add_halt(script_id)
								if config.DISPLAY_SCRIPT_ERRORS:
									t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{plugin_icon}\" not found")
									window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
								return True
							t = Message(ERROR_MESSAGE,'',f"\"{plugin_icon}\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						except Exception as e:
							if is_script:
								add_halt(script_id)
								if config.DISPLAY_SCRIPT_ERRORS:
									t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {e}")
									window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
								return True
							t = Message(ERROR_MESSAGE,'',f"{e}")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True

					plugins.call(gui,"unload")
					errors = plugins.load_plugins(gui)
					if len(errors)>0:
						t = Message(ERROR_MESSAGE,'',f"Plugin load errors: {', '.join(errors)}")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					else:
						t = Message(SYSTEM_MESSAGE,'',f"Plugin \"{file}\" installed")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				elif extension==".zip":
					try:
						unextracted = []
						with zipfile.ZipFile(file, 'r') as zf:
							for member in zf.infolist():
								file_path = os.path.join(plugins.PLUGIN_DIRECTORY, member.filename)

								extract_file = False
								name_without_extension, extension = os.path.splitext(file_path)
								if extension.lower()=='.py' or extension.lower()=='.png': extract_file = True

								if not config.OVERWRITE_PLUGINS_ON_IMPORT:
									if os.path.isfile(file_path):
										extract_file = False
										unextracted.append(member.filename)

								if extract_file: zf.extract(member, plugins.PLUGIN_DIRECTORY)

								if config.IMPORT_SCRIPTS_IN_PLUGINS:
									file_path = os.path.join(SCRIPTS_DIRECTORY, member.filename)

									extract_file = False
									name_without_extension, extension = os.path.splitext(file_path)
									if extension.lower()=='.merk': extract_file = True

									if not config.OVERWRITE_PLUGINS_ON_IMPORT:
										if os.path.isfile(file_path):
											extract_file = False
											unextracted.append(member.filename)

									if extract_file: zf.extract(member, SCRIPTS_DIRECTORY)

					except zipfile.BadZipFile:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{file}\" is not a valid ZIP file")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',f"\"{file}\" is not a valid ZIP file")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					except FileNotFoundError:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{file}\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',f"\"{file}\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					except Exception as e:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {e}")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',f"{e}")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True

					if len(unextracted)>0:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Files not overwritten: {', '.join(unextracted)}")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',f"Files not overwritten: {', '.join(unextracted)}")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True

					plugins.call(gui,"unload")
					errors = plugins.load_plugins(gui)
					if len(errors)>0:
						t = Message(ERROR_MESSAGE,'',f"Plugin load errors: {', '.join(errors)}")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					else:
						t = Message(SYSTEM_MESSAGE,'',f"Plugin \"{file}\" installed")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{file}\" is not a Python file or ZIP")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Usage: \"{file}\" is not a Python file or ZIP")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				return True

		# /window plugin
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='plugin':
				if not config.ENABLE_PLUGINS:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window plugin: Plugins are disabled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Plugins are disabled")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				gui.openPlugin()
				return True

		# /window hotkey
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='hotkey':
				if not config.ENABLE_HOTKEYS:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window hotkey: Hotkeys are disabled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Hotkeys are disabled")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				gui.openHotkeys()
				return True

		# /window ignore
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='ignore':
				if not config.ENABLE_IGNORE:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window ignore: Ignore is disabled")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Ignore is disabled")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				gui.openIgnore()
				return True

		# /window next
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='next':
				gui.MDI.activateNextSubWindow()
				return True

		# /window previous
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='previous':
				gui.MDI.activatePreviousSubWindow()
				return True

		# /window cascade
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='cascade':
				gui.MDI.cascadeSubWindows()
				return True

		# /window tile
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='tile':
				gui.MDI.tileSubWindows()
				return True

		# /window logs
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='logs':
				gui.menuExportLog()
				return True

		# /window logs target
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==3:
			if tokens[1].lower()=='logs':
				target = tokens[2]
				gui.menuExportLogTarget(target)
				return True

		# /window settings
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='settings':
				gui.openSettings()
				return True

		# /window readme
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='readme':
				gui.menuReadMeCmd()
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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window move: Invalid X value")
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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window move: Invalid Y value")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Invalid Y value passed to {config.ISSUE_COMMAND_SYMBOL}window move")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				if gui.is_move_valid_on_screen(gui,x_val,y_val):
					if gui.isMaximized() or gui.isMinimized(): gui.showNormal()
					gui.move(x_val,y_val)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window move: Not a valid window position")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Not a valid window position")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# /window size X Y
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==4:
			if tokens[1].lower()=='resize':
				tokens.pop(0)
				tokens.pop(0)
				x_val = tokens.pop(0)
				y_val = tokens.pop(0)
				
				x_val = is_int(x_val)
				if x_val==None:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window resize: Invalid width")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Invalid width value passed to {config.ISSUE_COMMAND_SYMBOL}window resize")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				y_val = is_int(y_val)
				if y_val==None:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}window resize: Invalid height")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"Invalid height passed to {config.ISSUE_COMMAND_SYMBOL}window resize")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				if gui.isMaximized() or gui.isMinimized(): gui.showNormal()
				gui.resize(x_val,y_val)
				return True

		# /window restart
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'window' and len(tokens)==2:
			if tokens[1].lower()=='restart':

				msg = f"Restart {APPLICATION_NAME}?\n\n{APPLICATION_NAME} will disconnect from any connected servers, and\nrestart without any command-line arguments."

				msgBox = QMessageBox()
				msgBox.setIconPixmap(QPixmap(QUIT_ICON))
				msgBox.setWindowIcon(QIcon(APPLICATION_ICON))
				msgBox.setText(msg)
				msgBox.setInformativeText("Click \"OK\" to restart, or \"Cancel\" to abort restart.")
				msgBox.setWindowTitle(f"{config.ISSUE_COMMAND_SYMBOL}reboot")
				msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

				rval = msgBox.exec()
				if rval == QMessageBox.Cancel:
					pass
				else:
					if is_running_from_pyinstaller():
						subprocess.Popen([sys.executable] + ["-R"])
						gui.close()
						gui.app.exit()
					else:
						os.execl(sys.executable, sys.executable, sys.argv[0], "-R")
						sys.exit()
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"window [COMMAND] [X] [Y]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"window [COMMAND] [X] [Y]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
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
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}show: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						gui.showSubWindow(w)
						if hasattr(window,"input"): window.input.setFocus()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}show: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}show: Server \""+server+"\" not found")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}show: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'show':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"show [SERVER] [WINDOW]")
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
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}hide: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.hide()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}hide: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}hide: Server \""+server+"\" not found")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}hide: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'hide':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"hide [SERVER] [WINDOW]")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"delay has been disabled in settings")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"delay requires a numerical argument")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"delay SECONDS COMMAND...")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"delay SECONDS COMMAND...")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"msgbox MESSAGE...")
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
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"private NICKNAME")
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
				if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
				if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
				if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
				if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)

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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"me TARGET MESSAGE")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}ctcp: Invalid request type (not VERSION, TIME, USERINFO, SOURCE, or FINGER)")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"ctcp REQUEST USER")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"ctcp REQUEST USER")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"ping USER")
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
			if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES: QApplication.setOverrideCursor(Qt.WaitCursor)
			flist = list_files()

			count = len(flist)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"Found {count} files")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			for f in flist:
				t = Message(SYSTEM_MESSAGE,'',f"{f}")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			t = Message(TEXT_HORIZONTAL_RULE_MESSAGE,'',f"End {count} file results")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES: QApplication.restoreOverrideCursor()
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'find' and len(tokens)>=2:
			tokens.pop(0)
			target = ' '.join(tokens)

			if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES: QApplication.setOverrideCursor(Qt.WaitCursor)
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
			if config.SEARCH_INSTALL_DIRECTORY_FOR_FILES: QApplication.restoreOverrideCursor()
			return True

	# |---------|
	# | /ignore |
	# |---------|
	if len(tokens)>=1:

		if not config.ENABLE_IGNORE:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ignore':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}ignore has been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}ignore has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ignore' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0).lower()

			for e in config.IGNORE_LIST:
				if target.lower()==e.lower():
					if is_script==True:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{target}\" is already in the ignore list")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{target}\" is already in the ignore list")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			t = Message(SYSTEM_MESSAGE,'',f"Ignoring user \"{target}\"")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			config.IGNORE_LIST.append(target)
			config.save_settings(config.CONFIG_FILE)
			gui.reRenderAll(True)
			gui.rerenderUserlists()
			if gui.ignore_manager!=None:
				gui.ignore_manager.refresh()
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

		if not config.ENABLE_IGNORE:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unignore':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}unignore has been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}unignore has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unignore' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0).lower()

			if target=='*':
				config.IGNORE_LIST = []
				t = Message(SYSTEM_MESSAGE,'',f"Unignoring all users")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				config.save_settings(config.CONFIG_FILE)
				gui.reRenderAll(True)
				gui.rerenderUserlists()
				if gui.ignore_manager!=None:
					gui.ignore_manager.refresh()
				return True

			if target in config.IGNORE_LIST:
				config.IGNORE_LIST.remove(target)
			else:
				if is_script==True:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{target}\" is not in the ignore list")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{target}\" is not in the ignore list")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(SYSTEM_MESSAGE,'',f"Unignoring user \"{target}\"")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			config.save_settings(config.CONFIG_FILE)
			gui.reRenderAll(True)
			gui.rerenderUserlists()
			if gui.ignore_manager!=None:
				gui.ignore_manager.refresh()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unignore':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"unignore USER")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"unignore USER")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}config has been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}config has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'config' and len(tokens)==2:
			if tokens[1].lower()=='import':

				options = QFileDialog.Options()
				options |= QFileDialog.DontUseNativeDialog
				fileName, _ = QFileDialog.getOpenFileName(gui,"Import Configuration File", INSTALL_DIRECTORY, f"{APPLICATION_NAME} Configuration File (*.json);;Text Files (*.txt);;All Files (*)", options=options)
				if fileName:
					config.load_settings(fileName)
					config.save_settings(config.CONFIG_FILE)
					gui.reload_settings()
					t = Message(SYSTEM_MESSAGE,'',f"Imported \"{fileName}\" configuration file")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					t = Message(SYSTEM_MESSAGE,'',f"Use {config.ISSUE_COMMAND_SYMBOL}window restart to restart {APPLICATION_NAME}")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				else:
					return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'config' and len(tokens)>=3:
			if tokens[1].lower()=='import':
				tokens.pop(0)
				tokens.pop(0)
				filename = ' '.join(tokens)
				f = find_file(filename,"json")
				if f!=None:
					config.load_settings(f)
					config.save_settings(config.CONFIG_FILE)
					gui.reload_settings()
					t = Message(SYSTEM_MESSAGE,'',f"Imported \"{f}\" configuration file")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					t = Message(SYSTEM_MESSAGE,'',f"Use {config.ISSUE_COMMAND_SYMBOL}window restart to restart {APPLICATION_NAME}")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}config: \"{filename}\" not found or is not readable")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}config: \"{filename}\" not found or is not readable")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'config' and len(tokens)==2:
			if tokens[1].lower()=='export':

				options = QFileDialog.Options()
				options |= QFileDialog.DontUseNativeDialog
				fileName, _ = QFileDialog.getSaveFileName(gui,"Export configuration as...",INSTALL_DIRECTORY,f"{APPLICATION_NAME} Configuration File (*.json);;All Files (*)", options=options)
				if fileName:
					_, file_extension = os.path.splitext(fileName)
					if file_extension=='':
						efl = len("json")+1
						if fileName[-efl:].lower()!=f".json": fileName = fileName+f".json"
					settings = config.build_settings()
					config.save_settings(fileName,settings)
					t = Message(SYSTEM_MESSAGE,'',f"Exported configuration to \"{fileName}\"")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				else:
					return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'config' and len(tokens)>=3:
			if tokens[1].lower()=='export':
				tokens.pop(0)
				tokens.pop(0)
				filename = ' '.join(tokens)
				settings = config.build_settings()
				config.save_settings(filename,settings)
				t = Message(SYSTEM_MESSAGE,'',f"Exported configuration to \"{filename}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		# No arguments dumps a list of all editable config values
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'config' and len(tokens)==1:
			settings = config.build_settings()

			count = 0
			results = []
			for s in settings:
				if s=="log_absolutely_all_messages_of_any_type": continue
				if s=="hotkeys": continue
				if s=="application_font": continue
				if s=="default_python_indentation": continue
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
				if type(settings[my_setting]) is list or my_setting=="log_absolutely_all_messages_of_any_type" or my_setting=="hotkeys" or my_setting=="application_font" or my_setting=="default_python_indentation":
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
						if a!="log_absolutely_all_messages_of_any_type" and a!="hotkeys" and a!="application_font" and a!="default_python_indentation":
							if fnmatch.fnmatch(a,f"*{my_setting}*"):
								results.append(a)

				if len(results)==0:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: No settings found containing \"{my_setting}\"")
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
				if type(settings[my_setting]) is list or my_setting=="log_absolutely_all_messages_of_any_type" or my_setting=="hotkeys" or my_setting=="application_font" or my_setting=="default_python_indentation":
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{my_setting}\" cannot be changed with the {config.ISSUE_COMMAND_SYMBOL}config command")
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

				if my_setting=="mdi_workspace_background" and my_value=="*": my_value=""

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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{my_value}\" is not a valid value for \"{my_setting}\" (value is {itype}, requires {dtype})")
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
						qlist = [f"\"{item}\"" for item in QT_STYLES]
						reason = f"must be {', '.join(qlist[:-1]) + ' or ' + qlist[-1]}"
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
					elif check==INVALID_SOUND:
						reason = "must be a valid WAV file"
					elif check==INVALID_TIME:
						reason = "must be a valid strptime format"
					elif check==INVALID_IMAGE:
						reason = "must be a supported image format"
					elif check==INVALID_VALUE:
						reason = "invalid value for setting"
					else:
						reason = "unknown"
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}: Error on line: {line_number}: \"{my_value}\" is not a valid value for \"{my_setting}\" ({reason})")
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
				t = Message(SYSTEM_MESSAGE,'',f"Use {config.ISSUE_COMMAND_SYMBOL}window restart to restart {APPLICATION_NAME}")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}: Error on line: {line_number}: \"{my_setting}\" is not a valid configuration setting")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}exit: \"{timer}\" is not a number")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"knock command is not supported by this server")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"knock command is not supported by this server")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',config.ISSUE_COMMAND_SYMBOL+"knock command is not supported by this server")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			tokens.pop(0)
			target = tokens.pop(0)
			message = ' '.join(tokens)
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"knock CHANNEL [MESSAGE]")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"refresh")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Channel list is empty, please use "+config.ISSUE_COMMAND_SYMBOL+"refresh to populate it.")
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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \""+filename+"\" is not a WAV file.")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"\""+filename+"\" is not a WAV file.")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Audio file \""+filename+"\" cannot be found.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Audio file \""+filename+"\" cannot be found.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'play':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"play FILENAME")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}alias: Aliases have been disabled in settings")
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
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}alias: Alias tokens must begin with a letter")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Alias tokens must begin with a letter")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			if not is_valid_alias_name(a):
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}alias: \""+a+"\" is not a valid alias name")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"\""+a+"\" is not a valid alias name")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			value = ' '.join(tokens)

			result,error = math(value)
			if not error and result!=None: value = str(result)

			addAlias(a,value,gui)

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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"alias TOKEN TEXT...")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}unalias: Aliases have been disabled in settings")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}unalias: Alias \"{target}\" not found.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Alias \"{target}\" not found.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unalias':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"unalias TOKEN")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}connectssl: \"{port}\" is not a number")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}connectssl: \"{port}\" is not a number")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"connectssl HOST [PORT] [PASSWORD]")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}connect: \"{port}\" is not a number")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}connect: \"{port}\" is not a number")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"connect HOST [PORT] [PASSWORD]")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xconnectssl: \"{port}\" is not a number")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xconnectssl: \"{port}\" is not a number")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"xconnectssl HOST [PORT] [PASSWORD]")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xconnect: \"{port}\" is not a number")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}xconnect: \"{port}\" is not a number")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"xconnect HOST [PORT] [PASSWORD]")
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

			# First, check to see if the argument passed
			# to the command is a hostid for a connection
			# script that already exists; if it is, then
			# open up the appropriate connection script
			USER.load_user(USER.USER_FILE)
			if filename in USER.COMMANDS:
				gui.newEditorWindowConnect(filename)
				return True

			efilename = find_file(filename,SCRIPT_FILE_EXTENSION)
			if efilename!=None:
				gui.openEditor(efilename)
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: File \""+filename+"\" doesn't exist or is not readable.")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"edit [FILENAME]")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"version")
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
					if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
					if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
					t = Message(RAW_SYSTEM_MESSAGE,'',f"{msg}")
					w.widget().writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					if is_script:
						add_halt(script_id)
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: No text to print")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"No text to print")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			msg = target+' '+' '.join(tokens)
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"print [WINDOW] TEXT")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"time")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"time")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /quote |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quote' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
			window.client.sendLine(msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quote' and len(tokens)==1:
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"raw TEXT")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"quote TEXT")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"back")
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
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
			window.client.away(msg)
			window.client.away_msg = msg
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'away' and len(tokens)==1:
			if config.PROMPT_FOR_AWAY_MESSAGE:
				x = Away(gui)
				msg = x.get_away_information(gui)
				if msg:
					if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
					if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
					if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
					window.client.away(msg)
					window.client.away_msg = msg
			else:
				msg = config.DEFAULT_AWAY_MESSAGE
				if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
				if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
				if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
				if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"oper USERNAME PASSWORD")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"oper USERNAME PASSWORD")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------|
	# | /style |
	# |--------|
	if len(tokens)>=1:

		if not config.ENABLE_STYLE_EDITOR:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'style':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}style has been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"{config.ISSUE_COMMAND_SYMBOL}style has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'style' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)

			swins = gui.getAllServerWindows()
			for win in swins:
				if server.lower() in win.widget().name.lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.widget().pressedStyleButton()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}style: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.widget().pressedStyleButton()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}style: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Server \""+server+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'style' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.widget().pressedStyleButton()
			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}style: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
					t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'style' and len(tokens)>=1:
			window.pressedStyleButton()
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
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}clear: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.widget().clearChat()
						if hasattr(window,"input"): window.input.setFocus()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}clear: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}clear: Server \""+server+"\" not found")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}clear: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'clear':
			window.clearChat()
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
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}restore: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.showNormal()
						if hasattr(window,"input"): window.input.setFocus()
						gui.buildWindowbar()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}restore: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}restore: Server \""+server+"\" not found")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}restore: Window \""+target+"\" not found")
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
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}minimize: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.showMinimized()
						if hasattr(window,"input"): window.input.setFocus()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}minimize: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}minimize: Server \""+server+"\" not found")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}minimize: Window \""+target+"\" not found")
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
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}maximize: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				if server.lower()==f"{win.widget().client.server.lower()}" or server.lower()==f"{win.widget().client.server}:{win.widget().client.port}".lower():
					w = gui.getSubWindowCommand(target,win.widget().client)
					if w:
						w.showMaximized()
					else:
						if is_script:
							add_halt(script_id)
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}maximize: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						else:
							t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}maximize: Server \""+server+"\" not found")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}maximize: Window \""+target+"\" not found")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"invite NICKNAME CHANNEL")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}script: Scripting is disabled")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Scripting is disabled")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'script' and len(tokens)>=2:

			tokens.pop(0)
			filename = tokens.pop(0)
			tokens = shlex.split(' '.join(tokens), comments=False)
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
				gui.scripts[script_id].scriptAlias.connect(execute_script_alias)
				gui.scripts[script_id].start()

			else:
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}script: \""+filename+"\" doesn't exist or is not readable.")
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
						gui.scripts[script_id].scriptAlias.connect(execute_script_alias)
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
							gui.scripts[script_id].scriptAlias.connect(execute_script_alias)
							gui.scripts[script_id].start()
						else:
							if is_script:
								add_halt(script_id)
								if config.DISPLAY_SCRIPT_ERRORS:
									t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}script: \"{script}\" doesn't exist or is not readable.")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"script FILENAME")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Second argument for "+config.ISSUE_COMMAND_SYMBOL+"whowas must be numeric")
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
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Second argument for "+config.ISSUE_COMMAND_SYMBOL+"whowas must be numeric")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"whowas NICKNAME [COUNT] [SERVER]")
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
			print(nick)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'who' and len(tokens)==3:
			tokens.pop(0)
			nick = tokens.pop(0)
			arg = tokens.pop(0)
			if arg.lower()!='o':
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Improper argument for "+config.ISSUE_COMMAND_SYMBOL+"who")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"who NICKNAME [o]")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"whois NICKNAME [SERVER]")
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
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
			if len(msg.strip())==0: msg = None
			window.client.kick(channel,target,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'kick':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"kick CHANNEL NICKNAME [REASON]")
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"mode TARGET MODE...")
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
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
			window.client.notice(target,msg)

			if target[:1]=='#' or target[:1]=='&' or target[:1]=='!' or target[:1]=='+':
				if config.REJECT_ALL_CHANNEL_NOTICES: return True

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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"notice TARGET MESSAGE")
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
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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
						t = Message(SELF_MESSAGE,"&rarr;"+target,msg)
						w.writeText(t)

			if config.WRITE_OUTGOING_PRIVATE_MESSAGES_TO_CURRENT_WINDOW:
				if not is_script:
					if window == gui.getServerWindow(window.client):
						if not written_to_server_window:
							t = Message(SELF_MESSAGE,"&rarr;"+target,msg)
							window.writeText(t)
					else:
						if window.name!=target:
							t = Message(SELF_MESSAGE,"&rarr;"+target,msg)
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"msg TARGET MESSAGE")
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
			# Check to see if the command is a macro, and
			# display help if needed
			for entry in MACRO_USAGE:
				if cmd==entry:
					h = HELP_ENTRY_COMMAND_TEMPLATE
					h = h.replace("%_USAGE_%",MACRO_USAGE[entry])
					if entry in MACRO_HELP:
						h = h.replace("%_DESCRIPTION_%",MACRO_HELP[entry])
					else:
						h = h.replace("%_DESCRIPTION_%",f"Executes script \"{USER_MACROS[entry].script}\"")
					t = Message(SYSTEM_MESSAGE,'',h)
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					found = True
			if found: return True
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Command "+cmd+" not found.")
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
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
			window.client.topic(channel,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'topic':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC")
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
				msg = config.DEFAULT_QUIT_MESSAGE
				if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
				if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
				if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
				if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
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

			if is_invalid_nickname(newnick):
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{newnick}\" is not a valid nickname")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{newnick}\" is not a valid nickname")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			window.client.setNick(newnick)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'nick':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"nick NEW_NICKNAME")
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
			msg = config.DEFAULT_QUIT_MESSAGE
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
			if config.INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE:
				buildTemporaryAliases(gui,window)
				msg = interpolateAliases(msg)
			window.client.leave(channel,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)>=3:
			tokens.pop(0)
			channel = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_MARKDOWN_MARKUP: msg = markdown_to_irc(msg)
			if config.ENABLE_IRC_COLOR_MARKUP: msg = inject_irc_colors(msg)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: msg = emojize(msg)
			if config.INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE:
				buildTemporaryAliases(gui,window)
				msg = interpolateAliases(msg)
			window.client.leave(channel,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part':
			if is_script:
				add_halt(script_id)
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"part CHANNEL [MESSAGE]")
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

			if is_invalid_channel(channel):
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{channel}\" is not a valid channel name")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{channel}\" is not a valid channel name")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			# Check to see if the user is trying to /join the
			# channel from the same channel they are in
			if window.name.lower()==channel.lower():
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: You have already joined "+window.name)
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

			if is_invalid_channel(channel):
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: \"{channel}\" is not a valid channel name")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"\"{channel}\" is not a valid channel name")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			# Check to see if the user is trying to /join the
			# channel from the same channel they are in
			if window.name.lower()==channel.lower():
				if is_script:
					add_halt(script_id)
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: You have already joined "+window.name)
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
					t = Message(ERROR_MESSAGE,'',f"{script_file}, line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]")
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

	threadEnd = pyqtSignal(object)
	finished = pyqtSignal(object)

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

	execLine = pyqtSignal(object)
	scriptEnd = pyqtSignal(object)
	scriptError = pyqtSignal(object)
	scriptAlias = pyqtSignal(object)
	updateAlias = pyqtSignal(str, object)

	def __init__(self,script,sid,gui,window,arguments=[],filename=None,parent=None):
		super(ScriptThread, self).__init__(parent)
		self.script = script
		self.id = sid
		self.gui = gui
		self.window = window
		self.arguments = arguments
		self.filename = filename
		self.ALIAS = dict(ALIAS)
		self.TEMPORARY_ALIAS = dict(TEMPORARY_ALIAS)
		self.CREATED = []

		self.updateAlias.connect(self.handle_update)

	@pyqtSlot(str, object)
	def handle_update(self, k, v):
		self.ALIAS[k] = v

	def addTemporaryAlias(self,name,value):
		self.TEMPORARY_ALIAS[name] = value

	def addAlias(self,name,value):
		self.ALIAS[name] = value
		self.scriptAlias.emit([name,value,self.gui])

	def removeAlias(self,name):
		if len(name)>0:
			if name[0]=="_": return False
		if name in self.ALIAS:
			self.ALIAS.pop(name,'')
			return True
		return False

	def interpolateAliases(self,text):

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
				if TEMPORARY_ALIAS[a]==None: continue
				text = text.replace(config.ALIAS_INTERPOLATION_SYMBOL+a,TEMPORARY_ALIAS[a])
			counter = counter + 1
			if counter>=99: break

		counter = 0
		while detect_alias(text):
			for a in self.ALIAS:
				text = text.replace(config.ALIAS_INTERPOLATION_SYMBOL+a,self.ALIAS[a])
			counter = counter + 1
			if counter>=99: break

		counter = 0
		while detect_alias(text):
			for a in self.TEMPORARY_ALIAS:
				if self.TEMPORARY_ALIAS[a]==None: continue
				text = text.replace(config.ALIAS_INTERPOLATION_SYMBOL+a,self.TEMPORARY_ALIAS[a])
			counter = counter + 1
			if counter>=99: break

		if config.ENABLE_EMOJI_SHORTCODES: text = emoji.emojize(text,language=config.EMOJI_LANGUAGE)
		if config.ENABLE_ASCIIMOJI_SHORTCODES: text = emojize(text)

		return text

	def process_inserts(self):
		script = []
		got_error = False

		line_number = 0
		for line in self.script.split("\n"):
			line_number = line_number + 1
			line = line.strip()
			if len(line)==0: continue
			tokens = line.split()

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
							f = self.interpolateAliases(f)
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

		if len(script)>0: self.script = self.interpolateAliases("\n".join(script))
		if not config.HALT_SCRIPT_EXECUTION_ON_ERROR: got_error = False
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

			# |=========|
			# | exclude |
			# |=========|
			if len(tokens)>=1:
				if tokens[0].lower()=='exclude' and len(tokens)>=2:
					tokens.pop(0)
					
					valid = True
					buildTemporaryAliases(self.gui,self.window)
					for e in tokens:
						e = self.interpolateAliases(e)
						if e.lower()==self.window.name.lower(): valid = False

					if valid==False:
						if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
							self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Script cannot be ran in {self.window.name}"])
						no_errors = False

				elif tokens[0].lower()=='exclude' and len(tokens)==1:
					self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: exclude called without an argument"])
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
						e = self.interpolateAliases(e)
						if e.lower()==self.window.name.lower(): valid = True

					if valid==False:
						if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
							self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Script cannot be ran in {self.window.name}"])
						no_errors = False

				elif tokens[0].lower()=='only' and len(tokens)==1:
					self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: only called without an argument"])
					no_errors = False

			# |==========|
			# | restrict |
			# |==========|
			if len(tokens)>=1:
				if tokens[0].lower()=='restrict' and len(tokens)==2:
					tokens.pop(0)
					arg = tokens.pop(0)
					buildTemporaryAliases(self.gui,self.window)
					arg = self.interpolateAliases(arg)

					if arg.lower()=='server':
						if self.window.window_type!=SERVER_WINDOW:
							if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
								self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Script must be ran in server windows"])
							no_errors = False
					elif arg.lower()=='channel':
						if self.window.window_type!=CHANNEL_WINDOW:
							if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
								self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Script must be ran in channel windows"])
							no_errors = False
					elif arg.lower()=='private':
						if self.window.window_type!=PRIVATE_WINDOW:
							if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
								self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Script must be ran in private chat windows"])
							no_errors = False
					else:
						self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Unrecognized restriction: \"{arg}\""])
						no_errors = False

				elif tokens[0].lower()=='restrict' and len(tokens)==3:
					tokens.pop(0)
					arg1 = tokens.pop(0)
					arg2 = tokens.pop(0)
					buildTemporaryAliases(self.gui,self.window)
					arg1 = self.interpolateAliases(arg1)
					arg2 = self.interpolateAliases(arg2)
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
						self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Unrecognized restriction: \"{arg1}\""])
						no_errors = False
					elif arg2.lower()!='server' and arg2.lower()!='channel' and arg2.lower()!='private':
						self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Unrecognized restriction: \"{arg2}\""])
						no_errors = False
					elif not valid:
						if self.window.window_type==PRIVATE_WINDOW: reason = "private chat"
						if self.window.window_type==SERVER_WINDOW: reason = "server"
						if self.window.window_type==CHANNEL_WINDOW: reason = "channel"
						if config.DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION:
							self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Script is restricted from running in {reason} windows"])
						no_errors = False

				elif tokens[0].lower()=='restrict' and len(tokens)==1:
					self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: restrict called without an argument"])
					no_errors = False
				elif tokens[0].lower()=='restrict' and len(tokens)>3:
					self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: restrict called with too many arguments"])
					no_errors = False

			# |=======|
			# | usage |
			# |=======|
			if len(tokens)>=1:
				if tokens[0].lower()=='usage' and len(tokens)>=2:
					tokens.pop(0)
					arg = tokens.pop(0)
					buildTemporaryAliases(self.gui,self.window)
					arg = self.interpolateAliases(arg)

					if arg=='+':
						if len(self.arguments)==0:
							if len(tokens)>0:
								self.scriptError.emit([self.gui,self.window,f"{' '.join(tokens)}"])
								no_errors = False
							else:
								self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Script must be called with {arg} arguments"])
								no_errors = False
					else:
						try:
							arg = int(arg)
							if config.REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS:
								if len(tokens)>0:
									if len(self.arguments)!=arg:
										self.scriptError.emit([self.gui,self.window,f"{' '.join(tokens)}"])
										no_errors = False
								else:
									if len(self.arguments)!=arg:
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Script must be called with {arg} arguments"])
										no_errors = False
							else:
								if len(tokens)>0:
									if len(self.arguments)<arg:
										self.scriptError.emit([self.gui,self.window,f"{' '.join(tokens)}"])
										no_errors = False
								else:
									if len(self.arguments)<arg:
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Script must be called with {arg} arguments"])
										no_errors = False
						except:
							self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: usage must be called with a numerical first argument"])
							no_errors = False

			# Usage must be called with at least one argument
			if len(tokens)>=1:
				if tokens[0].lower()=='usage' and len(tokens)==1:
					self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: usage called without an argument"])
					no_errors = False

			# /end doesn't take any arguments
			if len(tokens)>=1:
				if tokens[0].lower()=='end' and len(tokens)>1: 
					self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: end called with too many arguments"])
					no_errors = False

			if config.ENABLE_WAIT_COMMAND:
				# Make sure that wait has only one argument
				if len(tokens)>=1:
					if tokens[0].lower()=='wait' and len(tokens)>2:
						self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: wait called with too many arguments"])
						no_errors = False
					if tokens[0].lower()=='wait' and len(tokens)==1:
						self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: wait must be called with a numerical argument"])
						no_errors = False
			else:
				if len(tokens)>=1:
					if tokens[0].lower()=='wait':
						self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: wait has been disabled"])
						no_errors = False
		if not config.HALT_SCRIPT_EXECUTION_ON_ERROR: no_errors = True
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

		try:
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
				self.addTemporaryAlias(f"_{counter}",a)
				counter = counter + 1

			if len(self.arguments)>0:
				self.addTemporaryAlias(f"_0",' '.join(self.arguments))
			else:
				self.addTemporaryAlias(f"_0",'none')
				
			self.addTemporaryAlias(f"_ARGS",str(len(self.arguments)))

			if self.filename!=None:
				self.addTemporaryAlias(f"_FILE",self.filename)
				self.addTemporaryAlias(f"_SCRIPT",os.path.basename(self.filename))

			self.script = self.interpolateAliases(self.script)
			
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
					halt_issued = False

					if index==len(script):
						loop =  False
					else:
						line = script[index]

						tokens = line.split()

						# |========|
						# | /alias |
						# |========|
						# 
						# Here, we're creating a "shadow" of the alias table,
						# We make sure that any aliases created in the script
						# are "destroyed" as soon as the script exits, and
						# prevent the script from changing the value of any
						# alias in a different scope.
						# 
						if len(tokens)>=1:
							if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias' and len(tokens)>=3:

								if config.ENABLE_ALIASES:
									tokens.pop(0)
									a = tokens.pop(0)

									# If the first character is the interpolation
									# symbol, strip it from the name
									if len(a)>len(config.ALIAS_INTERPOLATION_SYMBOL):
										il = len(config.ALIAS_INTERPOLATION_SYMBOL)
										if a[:il] == config.ALIAS_INTERPOLATION_SYMBOL:
											a = a[il:]

									# Only add the local alias if it follows all the
									# "rules" of aliases
									errors = None
									if len(a)>=1:
										if a[0].isalpha():
											if not a in ALIAS:
												if is_valid_alias_name(a):
													value = ' '.join(tokens)
													result,error = math(value)
													if not error and result!=None: value = str(result)
													self.addAlias(a,value)
													self.CREATED.append(a)
												else:
													errors = f"\"{a}\" is not a valid alias token"
											else:
												errors = f"\"{a}\" already exists in another scope"
										else:
											errors = f"\"{a}\" is not a valid alias token"
									if errors!=None:
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: {config.ISSUE_COMMAND_SYMBOL}alias: {errors}"])
										loop = False
								continue

						# |======|
						# | halt |
						# |======|
						if len(tokens)>=2:
							if tokens[0].lower()=='halt':
								tokens.pop(0)
								msg = ' '.join(tokens)
								self.scriptError.emit([self.gui,self.window,f"Halt on line {line_number} in {os.path.basename(filename)}: {msg}"])
								loop = False
								halt_issued = True
								continue

						if len(tokens)>0 and len(tokens)==1:
							if tokens[0].lower()=='halt':
								self.scriptError.emit([self.gui,self.window,f"Halt on line {line_number} in {os.path.basename(filename)}"])
								loop = False
								halt_issued = True
								continue
						
						# |====|
						# | if |
						# |====|
						if len(tokens)>=5:
							if tokens[0].lower()=='if':

								if not config.ENABLE_IF_COMMAND:
									self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: if has been disabled"])
									loop = False
									continue

								try:
									stokens = shlex.split(line, comments=False)
								except:
									self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: Error tokenizing if command. Try using quotation marks"])
									loop = False
									continue

								stokens.pop(0)

								buildTemporaryAliases(self.gui,self.window)
								examine = self.interpolateAliases(stokens.pop(0))
								operator = self.interpolateAliases(stokens.pop(0))
								target = self.interpolateAliases(stokens.pop(0))

								r,error = self.math(examine)
								if not error and r!=None: examine = r

								r,error = self.math(target)
								if not error and r!=None: target = r

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
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{examine}\" is not a number"])
										loop = False
										continue
									try:
										ti = float(target)
									except:
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{target}\" is not a number"])
										loop = False
										continue
									if ei<ti:
										do_command = True

								if operator.lower()=='(gt)':
									valid_operator = True
									try:
										ei = float(examine)
									except:
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{examine}\" is not a number"])
										loop = False
										continue
									try:
										ti = float(target)
									except:
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{target}\" is not a number"])
										loop = False
										continue
									if ei>ti: 
										do_command = True

								if operator.lower()=='(eq)':
									valid_operator = True
									try:
										ei = float(examine)
									except:
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{examine}\" is not a number"])
										loop = False
										continue
									try:
										ti = float(target)
									except:
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{target}\" is not a number"])
										loop = False
										continue
									if ei==ti: 
										do_command = True

								if operator.lower()=='(ne)':
									valid_operator = True
									try:
										ei = float(examine)
									except:
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{examine}\" is not a number"])
										loop = False
										continue
									try:
										ti = float(target)
									except:
										self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{target}\" is not a number"])
										loop = False
										continue
									if ei!=ti: 
										do_command = True

								if not valid_operator:
									self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{operator}\" is not a valid \"if\" operator"])
									loop = False
									do_command = False
									continue

								if do_command:
									handled_goto = False
									if len(stokens)==2:
										if stokens[0].lower()=='goto':
											if config.ENABLE_GOTO_COMMAND:
												if stokens[1].lower()=='end':
													loop = False
													script_only_command = True
													continue
												else:
													try:
														ln = int(stokens[1])
													except:
														self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{stokens[1]}\" is not a valid line number"])
														loop = False
														continue
													ln = ln - 1
													try:
														code = script[ln]
													except:
														self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{stokens[1]}\" is not a valid line number"])
														loop = False
														continue
													index = ln
													self.execLine.emit([self.gui,self.window,self.id,script[index],index,False])
													handled_goto = True
													continue
											else:
												self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: goto has been disabled"])
												loop = False
												handled_goto = True
												continue
									if not handled_goto:
										self.execLine.emit([self.gui,self.window,self.id,' '.join(stokens),line_number,False])
									script_only_command = True
									continue

						if len(tokens)>0 and len(tokens)<5:
							if tokens[0].lower()=='if':
								self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: if called without enough arguments"])
								loop = False
								continue

						# |=========|
						# | context |
						# |=========|
						if len(tokens)==2:
							if tokens[0].lower()=='context':
								target = tokens[1]

								buildTemporaryAliases(self.gui,self.window)
								target = self.interpolateAliases(target)

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
									self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: context cannot find window \"{target}\""])
									loop = False
								else:
									continue

						if len(tokens)>=1:
							if tokens[0].lower()=='context' and len(tokens)==1:
								self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: context called without an argument"])
								script_only_command = True
								loop = False

							if tokens[0].lower()=='context' and len(tokens)>2:
								self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: context called with too many arguments"])
								script_only_command = True
								loop = False

						# |======|
						# | wait |
						# |======|
						if len(tokens)==2:
							if tokens[0].lower()=='wait':
								count = tokens[1]

								buildTemporaryAliases(self.gui,self.window)
								count = self.interpolateAliases(count)
								try:
									count = float(count)
								except:
									self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: wait called with a non-numerical argument"])
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
									self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: insert has been disabled"])
									script_only_command = True
									loop = False
									continue

						if len(tokens)==2:
							if tokens[0].lower()=='goto':
								if config.ENABLE_GOTO_COMMAND:
									target = tokens[1]

									buildTemporaryAliases(self.gui,self.window)
									target = self.interpolateAliases(target)

									if target.lower()=='end':
										loop = False
										script_only_command = True
										continue
									else:
										try:
											target = int(target)
										except:
											self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{target}\" is not a valid line number"])
											loop = False
											script_only_command = True
											continue
										try:
											code = script[target-1]
										except:
											self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: \"{target}\" is not a valid line number"])
											loop = False
											continue

										index = target-1
										self.execLine.emit([self.gui,self.window,self.id,script[index],index,False])
										script_only_command = True
										continue
								else:
									self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: goto has been disabled"])
									script_only_command = True
									loop = False
									continue
						if not config.HALT_SCRIPT_EXECUTION_ON_ERROR:
							if not halt_issued: loop = True
						try:
							self.execLine.emit([self.gui,self.window,self.id,line,line_number,script_only_command])
						except Exception as e:
							self.scriptError.emit([self.gui,self.window,f"{os.path.basename(filename)}, line {line_number}: {e}"])
		except Exception as e:
			if self.filename==None:
				filename = "script"
			else:
				filename = self.filename
			self.scriptError.emit([self.gui,self.window,f"Error executing {os.path.basename(filename)}: {e}"])
									
		self.scriptEnd.emit([self.gui,self.id,self.CREATED])

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