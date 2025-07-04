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

import os
import time
import uuid
import re
from pathlib import Path
import fnmatch
import datetime

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
COMMAND_HELP_INFORMATION = []
HELP = None
HELP_PREFIX = None
HELP_POSTFIX = None
HELP_EPILOGUE = None

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
			config.ISSUE_COMMAND_SYMBOL+"focus": config.ISSUE_COMMAND_SYMBOL+"focus ",
			config.ISSUE_COMMAND_SYMBOL+"maximize": config.ISSUE_COMMAND_SYMBOL+"maximize ",
			config.ISSUE_COMMAND_SYMBOL+"minimize": config.ISSUE_COMMAND_SYMBOL+"minimize ",
			config.ISSUE_COMMAND_SYMBOL+"cascade": config.ISSUE_COMMAND_SYMBOL+"cascade",
			config.ISSUE_COMMAND_SYMBOL+"tile": config.ISSUE_COMMAND_SYMBOL+"tile",
			config.ISSUE_COMMAND_SYMBOL+"clear": config.ISSUE_COMMAND_SYMBOL+"clear",
			config.ISSUE_COMMAND_SYMBOL+"settings": config.ISSUE_COMMAND_SYMBOL+"settings",
			config.ISSUE_COMMAND_SYMBOL+"style": config.ISSUE_COMMAND_SYMBOL+"style",
			config.ISSUE_COMMAND_SYMBOL+"log": config.ISSUE_COMMAND_SYMBOL+"log",
			config.ISSUE_COMMAND_SYMBOL+"exit": config.ISSUE_COMMAND_SYMBOL+"exit",
			config.ISSUE_COMMAND_SYMBOL+"config": config.ISSUE_COMMAND_SYMBOL+"config ",
			config.ISSUE_COMMAND_SYMBOL+"ignore": config.ISSUE_COMMAND_SYMBOL+"ignore ",
			config.ISSUE_COMMAND_SYMBOL+"unignore": config.ISSUE_COMMAND_SYMBOL+"unignore ",
		}

	# Remove the style command if the style editor is turned off 
	if not config.ENABLE_STYLE_EDITOR:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"style",'')

	if not config.ENABLE_ALIASES:
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"alias",'')
		AUTOCOMPLETE.pop(config.ISSUE_COMMAND_SYMBOL+"unalias",'')

	if new_autocomplete!=None:
		if isinstance(new_autocomplete, list):
			for a in new_autocomplete:
				AUTOCOMPLETE.update(a)
		else:
			AUTOCOMPLETE.update(new_autocomplete)

	# The command help system
	COMMAND_HELP_INFORMATION = [
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"help</b>", "Displays command usage information" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"me MESSAGE...</b>", "Sends a CTCP action message to the current chat" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"msg TARGET MESSAGE...</b>", "Sends a message" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"notice TARGET MESSAGE...</b>", "Sends a notice" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]</b>", "Joins a channel" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"part CHANNEL [MESSAGE]</b>", "Leaves a channel" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"nick NEW_NICKNAME</b>", "Changes your nickname" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC</b>", "Sets a channel topic" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"mode TARGET MODE...</b>", "Sets a mode on a channel or user" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"invite NICKNAME CHANNEL</b>", "Sends a channel invitation" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"kick CHANNEL NICKNAME [MESSAGE]</b>", "Kicks a user from a channel" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"whois NICKNAME [SERVER]</b>", "Requests user information from the server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"who NICKNAME [o]</b>", "Requests user information from the server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"whowas NICKNAME [COUNT] [SERVER]</b>", "Requests information about previously connected users" ],
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
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"script FILENAME</b>", "Executes a list of commands in a file" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"settings</b>", "Opens the settings dialog" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"style</b>", "Edits the current window's style" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"log</b>", "Opens the log manager" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"alias TOKEN TEXT...</b>", "Creates an alias that can be referenced by "+config.ALIAS_INTERPOLATION_SYMBOL+"TOKEN" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"alias</b>", "Prints a list of all current aliases" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"unalias TOKEN</b>", "Deletes the alias referenced by "+config.ALIAS_INTERPOLATION_SYMBOL+"TOKEN" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"edit [FILENAME]</b>", "Opens a script in the editor" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"play FILENAME</b>", "Plays a WAV file" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"print TEXT...</b>", "Prints text to the current window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"focus [SERVER] WINDOW</b>", "Switches focus to another window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"maximize [SERVER] WINDOW</b>", "Maximizes a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"minimize [SERVER] WINDOW</b>", "Minimizes a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"restore [SERVER] WINDOW</b>", "Restores a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"cascade</b>", "Cascades all subwindows" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"tile</b>", "Tiles all subwindows" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"clear [WINDOW]</b>", "Clears a window's chat display" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"exit [SECONDS]</b>", "Exits the client, with an optional pause of SECONDS before exit" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"config [SETTING] [VALUE...]</b>", "Changes a setting, or displays one or all settings in the configuration file. <i><b>Caution</b>: use at your own risk</i>" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"ignore USER</b>", "Hides a user's chat. USER can be a nickname or hostmask" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"unignore USER</b>", "Un-hides a user's chat. To un-hide all users, use * as the argument" ],
	]

	COPY = []
	for e in COMMAND_HELP_INFORMATION:
		if not config.ENABLE_STYLE_EDITOR:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"style</b>": continue
		if not config.ENABLE_ALIASES:
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"alias TOKEN TEXT...</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"alias</b>": continue
			if e[0]=="<b>"+config.ISSUE_COMMAND_SYMBOL+"unalias TOKEN</b>": continue
		COPY.append(e)
	COMMAND_HELP_INFORMATION = COPY

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
	TEMPORARY_ALIAS[name] = value
	TEMPORARY_ALIAS_AUTOCOMPLETE[name] = ''

def addAlias(name,value):
	ALIAS[name] = value

def removeAlias(name):
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

	return text

def buildTemporaryAliases(gui,window):

	addTemporaryAlias('_NICKNAME',window.client.nickname)
	addTemporaryAlias('_USERNAME',window.client.username)
	addTemporaryAlias('_REALNAME',window.client.realname)

	addTemporaryAlias('_WINDOW',window.name)

	if window.window_type==SERVER_WINDOW:
		addTemporaryAlias('_WINDOW_TYPE',"server")
	elif window.window_type==CHANNEL_WINDOW:
		addTemporaryAlias('_WINDOW_TYPE',"channel")
	elif window.window_type==PRIVATE_WINDOW:
		addTemporaryAlias('_WINDOW_TYPE',"private")
	else:
		addTemporaryAlias('_WINDOW_TYPE',"unknown")

	addTemporaryAlias('_SERVER',window.client.server)
	addTemporaryAlias('_PORT',str(window.client.port))

	if hasattr(window.client,"hostname"):
		addTemporaryAlias('_HOST',window.client.hostname)
	else:
		addTemporaryAlias('_HOST',window.client.server+":"+str(window.client.port))

	addTemporaryAlias('_UPTIME',str(window.uptime))

	if window.channel_topic!='':
		addTemporaryAlias('_TOPIC',window.channel_topic)
	else:
		addTemporaryAlias('_TOPIC','')

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

	if len(window.nicks)>0:
		addTemporaryAlias('_PRESENT',",".join(window.nicks))
	else:
		addTemporaryAlias('_PRESENT','')

	if window.client.usermodes!='':
		addTemporaryAlias('_MODE',window.client.usermodes)
	else:
		addTemporaryAlias('_MODE','')

def handleChatCommands(gui,window,user_input):
	global TEMPORARY_ALIAS

	buildTemporaryAliases(gui,window)

	user_input = interpolateAliases(user_input)
	retval = executeChatCommands(gui,window,user_input,False)
	TEMPORARY_ALIAS = {}
	return retval

def handleCommonCommands(gui,window,user_input):
	global TEMPORARY_ALIAS

	buildTemporaryAliases(gui,window)

	user_input = interpolateAliases(user_input)
	retval = executeCommonCommands(gui,window,user_input,False)
	TEMPORARY_ALIAS = {}
	return retval

def handleScriptCommands(gui,window,user_input,line_number):
	global TEMPORARY_ALIAS

	buildTemporaryAliases(gui,window)

	user_input = interpolateAliases(user_input)

	if window.window_type!=SERVER_WINDOW:
		if executeChatCommands(gui,window,user_input,True,line_number):
			TEMPORARY_ALIAS = {}
			return True

	retval = executeCommonCommands(gui,window,user_input,True,line_number)
	TEMPORARY_ALIAS = {}
	return retval

def executeChatCommands(gui,window,user_input,is_script,line_number=0):
	user_input = user_input.strip()
	tokens = user_input.split()

	# |-------|
	# | /jump |
	# |-------|
	if not is_script:
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'jump':
				t = Message(ERROR_MESSAGE,'',config.ISSUE_COMMAND_SYMBOL+"jump can only be called from scripts")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	# |-------|
	# | /wait |
	# |-------|
	if not is_script:
		if len(tokens)>=1:
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'wait':
				t = Message(ERROR_MESSAGE,'',config.ISSUE_COMMAND_SYMBOL+"wait can only be called from scripts")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
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
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Can't set topic for a private message")
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
				window.client.leave(channel,msg)
				return True

	return False

def find_file(filename,extension):

	# Check if it's a complete filename
	if os.path.isfile(filename): return filename

	# Look for the script in the scripts directory
	if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, filename)): return os.path.join(SCRIPTS_DIRECTORY, filename)

	# Look for the script in the config directory
	if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, filename)): return os.path.join(config.CONFIG_DIRECTORY, filename)

	# Look for the script in the install directory
	if os.path.isfile(os.path.join(INSTALL_DIRECTORY, filename)): return os.path.join(INSTALL_DIRECTORY, filename)

	# Add the default file extension and see if we find it

	efilename = filename + "." + extension

	# Check if it's a complete filename
	if os.path.isfile(efilename): return filename

	# Look for the script in the scripts directory
	if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, efilename)): return os.path.join(SCRIPTS_DIRECTORY, efilename)

	# Look for the script in the config directory
	if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, efilename)): return os.path.join(config.CONFIG_DIRECTORY, efilename)

	# Look for the script in the install directory
	if os.path.isfile(os.path.join(INSTALL_DIRECTORY, efilename)): return os.path.join(INSTALL_DIRECTORY, efilename)

	# Still not found? Case insensitive seach
	for root, dirs, files in os.walk(SCRIPTS_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.{extension}"):
			return os.path.join(root, filename)

	for root, dirs, files in os.walk(config.CONFIG_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.{extension}"):
			return os.path.join(root, filename)

	for root, dirs, files in os.walk(INSTALL_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.{extension}"):
			return os.path.join(root, filename)

	for root, dirs, files in os.walk(SCRIPTS_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return os.path.join(root, filename)

	for root, dirs, files in os.walk(config.CONFIG_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return os.path.join(root, filename)

	for root, dirs, files in os.walk(INSTALL_DIRECTORY):
		for filename in fnmatch.filter(files, f"{filename}.*"):
			return os.path.join(root, filename)

	return None

def execute_script_line(data):
	gui = data[0]
	window = data[1]
	script_id = data[2]
	line = data[3]
	line_number = data[4]
	script_only_command = data[5]

	if not handleScriptCommands(gui,window,line,line_number):
		if len(line.strip())==0: return
		if config.DISPLAY_SCRIPT_ERRORS:
			# Check to make sure this isn't being thrown by script
			# only commands
			if not script_only_command:
				if line[0]==config.ISSUE_COMMAND_SYMBOL:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Unrecognized command \"{line}\"")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				else:
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

def executeScript(gui,window,text):

	script_id = str(uuid.uuid4())
	gui.scripts[script_id] = ScriptThread(text,script_id,gui,window)
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

	# Do colors
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

	return ALL_VALID_SETTINGS

def executeCommonCommands(gui,window,user_input,is_script,line_number=0):
	user_input = user_input.strip()
	tokens = user_input.split()

	# |---------|
	# | /ignore |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ignore' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0).lower()

			t = Message(SYSTEM_MESSAGE,'',f"Ignoring user \"{target}\"")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			config.IGNORE_LIST.append(target)
			config.save_settings(config.CONFIG_FILE)
			gui.buildSettingsMenu()
			gui.reRenderAll(True)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'ignore':
			if is_script:
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"ignore USER")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"ignore USER")
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
				return True

			if target in config.IGNORE_LIST:
				config.IGNORE_LIST.remove(target)
			else:
				if is_script==True:
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
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unignore':
			if is_script:
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
			if is_script==True:
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"log cannot be called from a script")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			gui.menuExportLog()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'log':
			if is_script==True:
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"log cannot be called from a script")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"log")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |---------|
	# | /config |
	# |---------|
	if len(tokens)>=1:

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
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \"{my_value}\" is not a valid value for \"{my_setting}\" (value is {itype}, requires {dtype})")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{my_value}\" is not a valid value for \"{my_setting}\" (value is {itype}, requires {dtype})")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				# Check for sanity
				check = check_for_sane_values(my_setting,my_value)
				if check!=ALL_VALID_SETTINGS:
					if check==INVALID_STYLE:
						qlist = [f"\"{item}\"" for item in QStyleFactory.keys()]
						reason = f"Invalid Qt style (must be {", ".join(qlist[:-1]) + " or " + qlist[-1]})"
					elif check==INVALID_JUSTIFY:
						reason = "Invalid justify value (must be \"center\", \"left\", or \"right\")"
					elif check==INVALID_COLOR:
						reason = f"Invalid color (\"{my_value}\" is not a recognized color)"
					else:
						reason = "Invalid setting for unknown reasons"
					if is_script:
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line: {line_number}: \"{my_value}\" is not a valid value for \"{my_setting}\"")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							t = Message(ERROR_MESSAGE,'',f"Error on line: {line_number}: {reason}")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',f"\"{my_value}\" is not a valid value for \"{my_setting}\"")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					t = Message(ERROR_MESSAGE,'',f"{reason}")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

				settings[my_setting] = my_value
				config.save_settings(config.CONFIG_FILE,settings)

				gui.reload_settings()

				t = Message(SYSTEM_MESSAGE,'',f"Setting \"{my_setting}\" to \"{my_value}\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				t = Message(SYSTEM_MESSAGE,'',f"Please restart {APPLICATION_NAME} as soon as possible!")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
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
				timer=int(timer)
			except:
				if is_script:
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \"{timer}\" is not a number")
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
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \""+filename+"\" is not a WAV file.")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"\""+filename+"\" is not a WAV file.")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			else:
				if is_script:
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Audio file \""+filename+"\" cannot be found.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Audio file \""+filename+"\" cannot be found.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'play':
			if is_script:
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
			if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias' and len(tokens)>=1:
				if is_script:
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Aliases have been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Aliases have been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias' and len(tokens)>=3:

			tokens.pop(0)
			a = tokens.pop(0)

			if len(a)>=1:
				if not a[0].isalpha():
					if is_script:
						if config.DISPLAY_SCRIPT_ERRORS:
							t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Alias tokens must begin with a letter")
							window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
						return True
					t = Message(ERROR_MESSAGE,'',"Alias tokens must begin with a letter")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True

			# Alias tokens cannot be numbers
			is_number = True
			try:
				a = int(a)
			except:
				is_number = False
			if is_number:
				if is_script:
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Alias tokens cannot be numbers")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Alias tokens cannot be numbers")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			value = ' '.join(tokens)
			addAlias(a,value)

			if not is_script:
				t = Message(SYSTEM_MESSAGE,'',"Alias "+config.ALIAS_INTERPOLATION_SYMBOL+a+" set to \""+value+"\"")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias' and len(tokens)>=1:

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
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Aliases have been disabled in settings")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Aliases have been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unalias' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)

			if removeAlias(target):
				t = Message(SYSTEM_MESSAGE,'',f"Alias \"{target}\" deleted.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			else:
				if is_script:
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Alias \"{target}\" not found.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',f"Alias \"{target}\" not found.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'unalias':
			if is_script:
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
			connect_to_irc(gui,window,host,port,None,True,False,False)
			return True
		# /connectssl HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connectssl' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			connect_to_irc(gui,window,host,port,password,True,False,False)
			return True
		# /connectssl
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connectssl' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connectssl':
			if is_script:
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
			connect_to_irc(gui,window,host,port,None,False,False,False)
			return True
		# /connect HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connect' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			connect_to_irc(gui,window,host,port,password,False,False,False)
			return True
		# /connect
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connect' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connect':
			if is_script:
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"connect HOST [PORT] [PASSWORD]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"connect HOST [PORT] [PASSWORD]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |--------------|
	# | /xconnectssl |
	# |--------------|
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
			connect_to_irc(gui,window,host,port,None,True,False,True)
			return True
		# /connectssl HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnectssl' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			connect_to_irc(gui,window,host,port,password,True,False,True)
			return True
		# /xconnectssl
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnectssl' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnectssl':
			if is_script:
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
			connect_to_irc(gui,window,host,port,None,False,False,True)
			return True
		# /connect HOST PORT PASSWORD
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnect' and len(tokens)==4:
			tokens.pop(0)
			host = tokens.pop(0)
			port = tokens.pop(0)
			password = tokens.pop(0)
			connect_to_irc(gui,window,host,port,password,False,False,True)
			return True
		# /xconnect
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnect' and len(tokens)==1:
			gui.connectToIrc()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnect':
			if is_script:
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
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit' and len(tokens)==2:

			tokens.pop(0)
			filename = tokens.pop(0)

			efilename = find_file(filename,SCRIPT_FILE_EXTENSION)
			if efilename!=None:
				gui.newEditorWindowFile(efilename)

			else:
				if is_script:
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: File \""+filename+"\" doesn't exist.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"File \""+filename+"\" doesn't exist.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit' and len(tokens)==1:
			gui.newEditorWindow()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit':
			if is_script:
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
			msg = ' '.join(tokens)
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
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"print TEXT")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"print TEXT")
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

			if is_script==True:
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"style cannot be called from a script")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			if not config.ENABLE_STYLE_EDITOR:
				t = Message(ERROR_MESSAGE,'',"The style editor has been disabled in settings")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			if window.window_type==SERVER_WINDOW:
				gui.menuEditStyle()
			else:
				window.pressedStyleButton()
			return True

	# |-----------|
	# | /settings |
	# |-----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'settings' and len(tokens)==1:

			if is_script:
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: "+config.ISSUE_COMMAND_SYMBOL+"settings cannot be called from a script")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True

			gui.openSettings()
			return True

	# |--------|
	# | /clear |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'clear' and len(tokens)==1:
			window.clearChat()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'clear' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.widget().clearChat()
				# Move focus back to the calling window
				gui.showSubWindow(gui.getSubWindow(window.name,window.client))
			else:
				if is_script:
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	# |-------|
	# | /tile |
	# |-------|
	if len(tokens)==1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'tile':
			gui.MDI.tileSubWindows()
			return True

	# |----------|
	# | /cascade |
	# |----------|
	if len(tokens)==1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'cascade':
			gui.MDI.cascadeSubWindows()
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
				if server in win.widget().name.lower():
					w = gui.getSubWindow(target,win.widget().client)
					if w:
						w.showNormal()
					else:
						if is_script:
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Server \""+server+"\" not found")
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
			else:
				if is_script:
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Window \""+target+"\" not found")
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
				if server in win.widget().name.lower():
					w = gui.getSubWindow(target,win.widget().client)
					if w:
						w.showMinimized()
					else:
						if is_script:
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Server \""+server+"\" not found")
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
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Window \""+target+"\" not found")
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
				if server in win.widget().name.lower():
					w = gui.getSubWindow(target,win.widget().client)
					if w:
						w.showMaximized()
					else:
						if is_script:
							if config.DISPLAY_SCRIPT_ERRORS:
								t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Window \""+target+"\" not found")
								window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
							return True
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Server \""+server+"\" not found")
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
			else:
				if is_script:
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'maximize':
			window.showMaximized()
			return True

	# |--------|
	# | /focus |
	# |--------|

	if len(tokens)>=1:

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus' and len(tokens)==3:
			tokens.pop(0)
			server = tokens.pop(0)
			target = tokens.pop(0)

			swins = gui.getAllServerWindows()
			for win in swins:
				if server in win.widget().name.lower():
					w = gui.getSubWindow(target,win.widget().client)
					if w:
						gui.showSubWindow(w)
					else:
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				gui.showSubWindow(w)
			else:
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"focus [SERVER] WINDOW")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
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
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'script' and len(tokens)>=2:

			tokens.pop(0)
			# Filename might have spaces in it
			filename = ' '.join(tokens)

			filename = find_file(filename,SCRIPT_FILE_EXTENSION)
			if filename:
				f=open(filename, "r",encoding="utf-8",errors="ignore")
				text = f.read()
				f.close()

				script_id = str(uuid.uuid4())
				gui.scripts[script_id] = ScriptThread(text,script_id,gui,window)
				gui.scripts[script_id].execLine.connect(execute_script_line)
				gui.scripts[script_id].scriptEnd.connect(execute_script_end)
				gui.scripts[script_id].scriptError.connect(execute_script_error)
				gui.scripts[script_id].start()

			else:
				if is_script:
					if config.DISPLAY_SCRIPT_ERRORS:
						t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: \""+filename+"\" doesn't exist.")
						window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
				t = Message(ERROR_MESSAGE,'',"\""+filename+"\" doesn't exist.")
				window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'script':
			if is_script:
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
			if config.WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW:
				if target[:1]!='#' and target[:1]!='&' and target[:1]!='!' and target[:1]!='+':
					w = gui.getServerWindow(window.client)
					if w:
						t = Message(SELF_MESSAGE,"&rarr;"+target,msg)
						w.writeText(t)

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
			for entry in COMMAND_HELP_INFORMATION:
				if cmd in entry[0]:
					h = HELP_ENTRY_COMMAND_TEMPLATE
					h = h.replace("%_USAGE_%",entry[0])
					h = h.replace("%_DESCRIPTION_%",entry[1])
					t = Message(SYSTEM_MESSAGE,'',h)
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
					return True
			if is_script:
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
				msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			else:
				msg = config.DEFAULT_QUIT_MESSAGE
			window.client.leave(channel,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)>=3:
			tokens.pop(0)
			channel = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language=config.EMOJI_LANGUAGE)
			window.client.leave(channel,msg)
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
				if config.DISPLAY_SCRIPT_ERRORS:
					t = Message(ERROR_MESSAGE,'',f"Error on line {line_number}: Usage: "+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]")
					window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
				return True
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]")
			window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)
			return True

	return False

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

	def __init__(self,script,sid,gui,window,parent=None):
		super(ScriptThread, self).__init__(parent)
		self.script = script
		self.id = sid
		self.gui = gui
		self.window = window

		# Strip comments from script
		self.script = re.sub(re.compile("/\\*.*?\\*/",re.DOTALL ) ,"" ,self.script)

	def run(self):

		no_errors = True

		# First pass through the script, to see if there's
		# any problem with /wait calls
		line_number = 0
		for line in self.script.split("\n"):
			line_number = line_number + 1
			line = line.strip()
			if len(line)==0: continue
			tokens = line.split()

			if len(tokens)==2:
				if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'wait':
					count = tokens[1]
					try:
						count = int(count)
					except:
						self.scriptError.emit([self.gui,self.window,f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}wait must be called with a numerical argument."])
						no_errors = False

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

					tokens = line.split()

					if len(tokens)==2:
						if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'jump':
							target = tokens[1]

							is_valid = False
							valids = self.gui.getAllConnectedWindows(self.window.client)
							for c in valids:
								if c.name==target:
									self.window = c
									is_valid = True

							valids = self.gui.getAllConnectedServerWindows()
							for w in valids:
								c = w.widget()
								if c.name==target:
									self.window = c
									is_valid = True

							script_only_command = True

							if not is_valid:
								self.scriptError.emit([self.gui,self.window,f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}jump cannot find window \"{target}\"."])
								loop = False
							else:
								continue

					if len(tokens)>=1:
						if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus': 
							self.scriptError.emit([self.gui,self.window,f"Error on line {line_number}: {config.ISSUE_COMMAND_SYMBOL}focus cannot be called in scripts."])
							loop = False

					if len(tokens)==2:
						if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'wait':
							count = tokens[1]
							count = int(count)
							time.sleep(count)
							script_only_command = True
							continue

					# if len(tokens)==2:
					# 	if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'goto':
					# 		target = tokens[1]
					# 		index = int(target) - 2
					# 		continue

					self.execLine.emit([self.gui,self.window,self.id,line,line_number,script_only_command])

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