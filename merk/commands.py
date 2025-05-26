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
from PyQt5.QtMultimedia import QSound

import os
import time
import uuid
import re
from pathlib import Path
import fnmatch

import emoji

from .resources import *
from . import config
from . import user as USER

CONFIG_DIRECTORY = None
SCRIPTS_DIRECTORY = None

ALIAS = {}
AUTOCOMPLETE = {}
COMMAND_HELP_INFORMATION = []
HELP = None

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
			config.ISSUE_COMMAND_SYMBOL+"print": config.ISSUE_COMMAND_SYMBOL+"print ",
			config.ISSUE_COMMAND_SYMBOL+"focus": config.ISSUE_COMMAND_SYMBOL+"focus ",
			config.ISSUE_COMMAND_SYMBOL+"maximize": config.ISSUE_COMMAND_SYMBOL+"maximize ",
			config.ISSUE_COMMAND_SYMBOL+"minimize": config.ISSUE_COMMAND_SYMBOL+"minimize ",
			config.ISSUE_COMMAND_SYMBOL+"restore": config.ISSUE_COMMAND_SYMBOL+"restore ",
			config.ISSUE_COMMAND_SYMBOL+"cascade": config.ISSUE_COMMAND_SYMBOL+"cascade",
			config.ISSUE_COMMAND_SYMBOL+"tile": config.ISSUE_COMMAND_SYMBOL+"tile",
			config.ISSUE_COMMAND_SYMBOL+"clear": config.ISSUE_COMMAND_SYMBOL+"clear",
			config.ISSUE_COMMAND_SYMBOL+"settings": config.ISSUE_COMMAND_SYMBOL+"settings",
			config.ISSUE_COMMAND_SYMBOL+"style": config.ISSUE_COMMAND_SYMBOL+"style",
			config.ISSUE_COMMAND_SYMBOL+"connect": config.ISSUE_COMMAND_SYMBOL+"connect ",
			config.ISSUE_COMMAND_SYMBOL+"connectssl": config.ISSUE_COMMAND_SYMBOL+"connectssl ",
			config.ISSUE_COMMAND_SYMBOL+"xconnect": config.ISSUE_COMMAND_SYMBOL+"xconnect ",
			config.ISSUE_COMMAND_SYMBOL+"xconnectssl": config.ISSUE_COMMAND_SYMBOL+"xconnectssl ",
			config.ISSUE_COMMAND_SYMBOL+"alias": config.ISSUE_COMMAND_SYMBOL+"alias ",
			config.ISSUE_COMMAND_SYMBOL+"script" : config.ISSUE_COMMAND_SYMBOL+"script ",
			config.ISSUE_COMMAND_SYMBOL+"edit" : config.ISSUE_COMMAND_SYMBOL+"edit ",
			config.ISSUE_COMMAND_SYMBOL+"play" : config.ISSUE_COMMAND_SYMBOL+"play ",
			config.ISSUE_COMMAND_SYMBOL+"list" : config.ISSUE_COMMAND_SYMBOL+"list ",
			config.ISSUE_COMMAND_SYMBOL+"refresh" : config.ISSUE_COMMAND_SYMBOL+"refresh",
		}

	if new_autocomplete!=None:
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
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"connect SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"connectssl SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server via SSL" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"xconnect SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server & executes connection script" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"xconnectssl SERVER [PORT] [PASSWORD]</b>", "Connects to an IRC server via SSL & executes connection script" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"print TEXT...</b>", "Prints text to the current window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"focus [SERVER] WINDOW</b>", "Switches focus to another window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"maximize [SERVER] WINDOW</b>", "Maximizes a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"minimize [SERVER] WINDOW</b>", "Minimizes a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"restore [SERVER] WINDOW</b>", "Restores a window" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"cascade</b>", "Cascades all subwindows" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"tile</b>", "Tiles all subwindows" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"clear [WINDOW]</b>", "Clears a window's chat display" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"settings</b>", "Opens the settings dialog" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"style</b>", "Edits the current window's style" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"alias TOKEN TEXT...</b>", "Creates an alias that can be referenced by "+config.ALIAS_INTERPOLATION_SYMBOL+"TOKEN" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"alias</b>", "Prints a list of all current aliases" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"script FILENAME</b>", "Executes a list of commands in a file" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"edit [FILENAME]</b>", "Opens a script in the editor" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"play FILENAME</b>", "Plays a WAV file" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"list [TERMS]</b>", "Lists or searches channels on the server; use \"*\" for multi-character wildcard, \"?\" for single character" ],
		[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"refresh</b>", "Requests a new list of channels from the server" ],
	]

	if new_help!=None:
		for i in new_help:
			COMMAND_HELP_INFORMATION.append(i)

	global HELP_DISPLAY_TEMPLATE
	if config.AUTOCOMPLETE_COMMANDS:
		HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_AUTOCOMPLETE_%","Command autocomplete is turned on; to use autocomplete, type the first few characters of a command and press the \"tab\" key to complete the command.")
	else:
		HELP_DISPLAY_TEMPLATE = HELP_DISPLAY_TEMPLATE.replace("%_AUTOCOMPLETE_%","Command autocomplete is turned off.")

	hdisplay = []
	for e in COMMAND_HELP_INFORMATION:
		t = HELP_ENTRY_TEMPLATE
		t = t.replace("%_USAGE_%",e[0])
		t = t.replace("%_DESCRIPTION_%",e[1])
		hdisplay.append(t)
	help_display = HELP_DISPLAY_TEMPLATE.replace("%_LIST_%","\n".join(hdisplay))

	HELP = Message(RAW_SYSTEM_MESSAGE,'',help_display)

build_help_and_autocomplete()

def addAlias(name,value):
	ALIAS[name] = value

def detect_alias(text):
  pattern = r"\$([^\d]+)"
  match = re.search(pattern, text)
  return bool(match)

def interpolateAliases(text):
	if not detect_alias(text): return text
	counter = 0
	while detect_alias(text):
		for a in ALIAS:
			text = text.replace(config.ALIAS_INTERPOLATION_SYMBOL+a,ALIAS[a])
		counter = counter + 1
		if counter>=99: break
	return text

def handleChatCommands(gui,window,user_input,is_script):
	user_input = interpolateAliases(user_input)
	return executeChatCommands(gui,window,user_input,is_script)

def handleCommonCommands(gui,window,user_input,is_script):
	user_input = interpolateAliases(user_input)
	return executeCommonCommands(gui,window,user_input,is_script)

def executeChatCommands(gui,window,user_input,is_script):
	user_input = user_input.lstrip()
	tokens = user_input.split()

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
				t = Message(ERROR_MESSAGE,'',"You can't invite a user to a private chat")
				window.writeText(t,False)
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
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language='alias')
			window.client.describe(window.name,msg)
			t = Message(ACTION_MESSAGE,window.client.nickname,msg)
			window.writeText(t)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'me':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"me MESSAGE")
			window.writeText(t,False)
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
					if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language='alias')
					window.client.topic(channel,msg)
					return True
				else:
					t = Message(ERROR_MESSAGE,'',"Can't set topic for a private message")
					window.writeText(t,False)
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
			window.client.leave(channel,config.DEFAULT_QUIT_MESSAGE)
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
				if config.ENABLE_EMOJI_SHORTCODES:  msg = emoji.emojize(msg,language='alias')
				window.client.leave(channel,msg)
				return True

	return False

def find_script(filename):

	# Check if it's a complete filename
	if os.path.isfile(filename): return filename

	# Look for the script in the scripts directory
	if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, filename)): return os.path.join(SCRIPTS_DIRECTORY, filename)

	# Look for the script in the config directory
	if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, filename)): return os.path.join(config.CONFIG_DIRECTORY, filename)

	# Look for the script in the install directory
	if os.path.isfile(os.path.join(INSTALL_DIRECTORY, filename)): return os.path.join(INSTALL_DIRECTORY, filename)

	# Add the default file extension and see if we find it

	efilename = filename + "." + SCRIPT_FILE_EXTENSION

	# Check if it's a complete filename
	if os.path.isfile(efilename): return filename

	# Look for the script in the scripts directory
	if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, efilename)): return os.path.join(SCRIPTS_DIRECTORY, efilename)

	# Look for the script in the config directory
	if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, efilename)): return os.path.join(config.CONFIG_DIRECTORY, efilename)

	# Look for the script in the install directory
	if os.path.isfile(os.path.join(INSTALL_DIRECTORY, efilename)): return os.path.join(INSTALL_DIRECTORY, efilename)

	return None

def execute_script_line(data):
	gui = data[0]
	window = data[1]
	line = data[2]

	handleCommonCommands(gui,window,line,True)

def execute_script_error(data):
	gui = data[0]
	window = data[1]
	line = data[2]

	t = Message(ERROR_MESSAGE,'',line)
	window.writeText(t,False)

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
		window.writeText(t,False)
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

def find_sound_file(filename):

	# Check if it's a complete filename
	if os.path.isfile(filename): return filename

	# Look for the WAV in the scripts directory
	if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, filename)): return os.path.join(SCRIPTS_DIRECTORY, filename)

	# Look for the WAV in the config directory
	if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, filename)): return os.path.join(config.CONFIG_DIRECTORY, filename)

	# Look for the WAV in the install directory
	if os.path.isfile(os.path.join(INSTALL_DIRECTORY, filename)): return os.path.join(INSTALL_DIRECTORY, filename)

	# Add the default file extension and see if we find it

	efilename = filename + "." + "wav"

	# Check if it's a complete filename
	if os.path.isfile(efilename): return filename

	# Look for the WAV in the scripts directory
	if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, efilename)): return os.path.join(SCRIPTS_DIRECTORY, efilename)

	# Look for the WAV in the config directory
	if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, efilename)): return os.path.join(config.CONFIG_DIRECTORY, efilename)

	# Look for the WAV in the install directory
	if os.path.isfile(os.path.join(INSTALL_DIRECTORY, efilename)): return os.path.join(INSTALL_DIRECTORY, efilename)

	efilename = filename + "." + "WAV"

	# Check if it's a complete filename
	if os.path.isfile(efilename): return filename

	# Look for the WAV in the scripts directory
	if os.path.isfile(os.path.join(SCRIPTS_DIRECTORY, efilename)): return os.path.join(SCRIPTS_DIRECTORY, efilename)

	# Look for the WAV in the config directory
	if os.path.isfile(os.path.join(config.CONFIG_DIRECTORY, efilename)): return os.path.join(config.CONFIG_DIRECTORY, efilename)

	# Look for the WAV in the install directory
	if os.path.isfile(os.path.join(INSTALL_DIRECTORY, efilename)): return os.path.join(INSTALL_DIRECTORY, efilename)

	return None

def executeCommonCommands(gui,window,user_input,is_script):
	user_input = user_input.lstrip()
	tokens = user_input.split()

	# |----------|
	# | /refresh |
	# |----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'refresh' and len(tokens)==1:

			window.client.doing_list_refresh = True
			window.client.sendLine('LIST')
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'refresh':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"refresh")
			window.writeText(t,False)
			return True

	# |-------|
	# | /list |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'list' and len(tokens)==1:

			if len(window.client.server_channel_list)==0:
				t = Message(ERROR_MESSAGE,'',"Channel list is empty, please use "+config.ISSUE_COMMAND_SYMBOL+"refresh to populate it.")
				window.writeText(t)
				return True

			for entry in window.client.server_channel_list:
				channel_name = entry[0]
				channel_count = entry[1]
				channel_topic = entry[2]
				if len(channel_topic)>0:
					t = Message(LIST_MESSAGE,'','')
					t.channel = channel_name
					t.channel_count = channel_count
					t.channel_topic = channel_topic
				else:
					t = Message(LIST_MESSAGE,'','')
					t.channel = channel_name
					t.channel_count = channel_count
				window.writeText(t,False)
			if len(window.client.server_channel_list)==1:
				t = Message(SYSTEM_MESSAGE,'',"1 channel found.")
			else:
				t = Message(SYSTEM_MESSAGE,'',str(len(window.client.server_channel_list))+" channels found.")
			window.writeText(t,False)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'list' and len(tokens)>=2:

			if len(window.client.server_channel_list)==0:
				t = Message(ERROR_MESSAGE,'',"Channel list is empty, please use "+config.ISSUE_COMMAND_SYMBOL+"refresh to populate it.")
				window.writeText(t)
				return True

			tokens.pop(0)
			target = ' '.join(tokens)
			results = []
			t = Message(SYSTEM_MESSAGE,'',"Searching for \""+target+"\"...")
			window.writeText(t,False)
			for entry in window.client.server_channel_list:
				channel_name = entry[0]
				channel_count = entry[1]
				channel_topic = entry[2]
				if fnmatch.fnmatch(channel_name,f"{target}"):
					results.append(entry)
				if fnmatch.fnmatch(channel_topic,f"{target}"):
					results.append(entry)

			results = remove_duplicate_sublists(results)

			if len(results)==0:
				t = Message(ERROR_MESSAGE,'',"No results found.")
				window.writeText(t)
				return True

			for entry in results:
				channel_name = entry[0]
				channel_count = entry[1]
				channel_topic = entry[2]
				if len(channel_topic)>0:
					t = Message(LIST_MESSAGE,'','')
					t.channel = channel_name
					t.channel_count = channel_count
					t.channel_topic = channel_topic
				else:
					t = Message(LIST_MESSAGE,'','')
					t.channel = channel_name
					t.channel_count = channel_count
				window.writeText(t,False)
			t = Message(SYSTEM_MESSAGE,'',"Search for \""+target+"\" complete, "+str(len(results))+" entries found.")
			window.writeText(t,False)
			return True

	# |-------|
	# | /play |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'play' and len(tokens)==2:

			tokens.pop(0)
			filename = tokens.pop(0)

			efilename = find_sound_file(filename)
			if efilename!=None:
				if is_wav_file(efilename):
					QSound.play(efilename)
				else:
					t = Message(ERROR_MESSAGE,'',"\""+filename+"\" is not a WAV file.")
					window.writeText(t)
			else:
				t = Message(ERROR_MESSAGE,'',"Audio file \""+filename+"\" cannot be found.")
				window.writeText(t)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'play':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"play FILENAME")
			window.writeText(t,False)
			return True

	# |--------|
	# | /alias |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias' and len(tokens)>=3:

			tokens.pop(0)
			a = tokens.pop(0)

			# Alias tokens cannot be numbers
			is_number = True
			try:
				a = int(a)
			except:
				is_number = False
			if is_number:
				t = Message(ERROR_MESSAGE,'',"Alias tokens cannot be numbers")
				window.writeText(t,False)
				return True

			value = ' '.join(tokens)
			addAlias(a,value)

			if not is_script:
				t = Message(SYSTEM_MESSAGE,'',"Alias "+config.ALIAS_INTERPOLATION_SYMBOL+a+" set to \""+value+"\"")
				window.writeText(t,False)
			
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias' and len(tokens)>=1:

			if len(ALIAS)==0:
				t = Message(SYSTEM_MESSAGE,'',"No aliases are currently defined.")
				window.writeText(t,False)
				return True

			for a in ALIAS:
				t = Message(SYSTEM_MESSAGE,'',config.ALIAS_INTERPOLATION_SYMBOL+a+" = \""+ALIAS[a]+"\"")
				window.writeText(t,False)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'alias':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"alias TOKEN TEXT...")
			window.writeText(t,False)
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
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connectssl':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"connectssl HOST [PORT] [PASSWORD]")
			window.writeText(t)
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
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'connect':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"connect HOST [PORT] [PASSWORD]")
			window.writeText(t)
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
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnectssl':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"xconnectssl HOST [PORT] [PASSWORD]")
			window.writeText(t)
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
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'xconnect':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"xconnect HOST [PORT] [PASSWORD]")
			window.writeText(t)
			return True

	# |-------|
	# | /edit |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit' and len(tokens)==2:

			tokens.pop(0)
			filename = tokens.pop(0)

			filename = find_script(filename)
			if filename!=None:
				gui.newEditorWindowFile(filename)

			else:
				t = Message(ERROR_MESSAGE,'',"\""+filename+"\" doesn't exist.")
				window.writeText(t)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit' and len(tokens)==1:
			gui.newEditorWindow()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'edit':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"edit [FILENAME]")
			window.writeText(t,False)
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
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"version")
			window.writeText(t)
			return True

	# |--------|
	# | /print |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'print' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			t = Message(RAW_SYSTEM_MESSAGE,'',f"{msg}")
			# Get the current active window
			w = gui.MDI.activeSubWindow()
			if hasattr(w,"widget"):
				c = w.widget()
				if hasattr(c,"writeText"):
					c.writeText(t,False)
				else:
					window.writeText(t,False)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'print' and len(tokens)==1:
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"print TEXT")
			window.writeText(t)
			return True

	# |-------|
	# | /time |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'time' and len(tokens)==1:
			window.client.sendLine("TIME")
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'time':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"time")
			window.writeText(t)
			return True

	# |------|
	# | /raw |
	# |------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'raw' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			window.client.sendLine(msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'raw' and len(tokens)==1:
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"raw TEXT")
			window.writeText(t)
			return True

	# |-------|
	# | /back |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'back' and len(tokens)==1:
			window.client.back()
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'back':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"back")
			window.writeText(t)
			return True

	# |-------|
	# | /away |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'away' and len(tokens)>=2:
			tokens.pop(0)
			msg = ' '.join(tokens)
			window.client.away(msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'away' and len(tokens)==1:
			window.client.away("busy")
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
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"oper USERNAME PASSWORD")
			window.writeText(t)
			return True

	# |--------|
	# | /style |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'style' and len(tokens)==1:

			if is_script==True:
				t = Message(ERROR_MESSAGE,'',""+config.ISSUE_COMMAND_SYMBOL+"style cannot be called from a script")
				window.writeText(t)
				return True

			window.pressedStyleButton()
			return True

	# |-----------|
	# | /settings |
	# |-----------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'settings' and len(tokens)==1:

			if is_script==True:
				t = Message(ERROR_MESSAGE,'',""+config.ISSUE_COMMAND_SYMBOL+"settings cannot be called from a script")
				window.writeText(t)
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
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t)
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
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t)
					return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'restore' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.showNormal()
			else:
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t)
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
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t)
					return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'minimize' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.showMinimized()
			else:
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t)
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
						t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
						window.writeText(t)
					return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'maximize' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				w.showMaximized()
			else:
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t)
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
						window.writeText(t)
					return True
			t = Message(ERROR_MESSAGE,'',"Server \""+server+"\" not found")
			window.writeText(t)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus' and len(tokens)==2:
			tokens.pop(0)
			target = tokens.pop(0)
			w = gui.getSubWindow(target,window.client)
			if w:
				gui.showSubWindow(w)
			else:
				t = Message(ERROR_MESSAGE,'',"Window \""+target+"\" not found")
				window.writeText(t)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'focus':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"focus [SERVER] WINDOW")
			window.writeText(t)
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
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"invite NICKNAME CHANNEL")
			window.writeText(t)
			return True

	# |---------|
	# | /script |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'script' and len(tokens)>=2:

			tokens.pop(0)
			# Filename might have spaces in it
			filename = ' '.join(tokens)

			filename = find_script(filename)
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
				t = Message(ERROR_MESSAGE,'',"\""+filename+"\" doesn't exist.")
				window.writeText(t)
			return True

		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'script':

			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"script FILENAME")
			window.writeText(t,False)
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
				t = Message(ERROR_MESSAGE,'',"Second argument for "+config.ISSUE_COMMAND_SYMBOL+"whowas must be numeric")
				window.writeText(t,False)
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
				t = Message(ERROR_MESSAGE,'',"Second argument for "+config.ISSUE_COMMAND_SYMBOL+"whowas must be numeric")
				window.writeText(t,False)
				return True
			window.client.sendLine("WHOWAS "+nick+" "+str(arg)+" "+serv)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whowas':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"whowas NICKNAME [COUNT] [SERVER]")
			window.writeText(t,False)
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
				t = Message(ERROR_MESSAGE,'',"Improper argument for "+config.ISSUE_COMMAND_SYMBOL+"who")
				window.writeText(t,False)
				return True
			window.client.sendLine("WHO "+nick+" o")
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'who':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"who NICKNAME [o]")
			window.writeText(t,False)
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
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"whois NICKNAME [SERVER]")
			window.writeText(t,False)
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
			if len(msg.strip())==0: msg = None
			window.client.kick(channel,target,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'kick':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"kick CHANNEL NICKNAME [REASON]")
			window.writeText(t,False)
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
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"mode TARGET MODE...")
			window.writeText(t,False)
			return True


	# |---------|
	# | /notice |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'notice' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language='alias')
			window.client.notice(target,msg)

			# If we have the target's window open, write
			# the message there
			w = gui.getWindow(target,window.client)
			if w:
				t = Message(NOTICE_MESSAGE,window.client.nickname,msg)
				w.writeText(t)

			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'notice':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"notice TARGET MESSAGE")
			window.writeText(t,False)
			return True

	# |------|
	# | /msg |
	# |------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'msg' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language='alias')
			window.client.msg(target,msg)

			# If we have the target's window open, write
			# the message there
			w = gui.getWindow(target,window.client)
			if w:
				t = Message(SELF_MESSAGE,window.client.nickname,msg)
				w.writeText(t)

			# Write the message to the server window
			if config.WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW:
				if target[:1]!='#' and target[:1]!='&' and target[:1]!='!' and target[:1]!='+':
					w = gui.getServerWindow(window.client)
					if w:
						t = Message(SELF_MESSAGE,"&rarr;"+target,msg)
						w.writeText(t)

			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'msg':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"msg TARGET MESSAGE")
			window.writeText(t,False)
			return True

	# |-------|
	# | /help |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'help':
			window.writeText(HELP,False)
			return True

	# |--------|
	# | /topic |
	# |--------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'topic' and len(tokens)>=3:
			tokens.pop(0)
			channel = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language='alias')
			window.client.topic(channel,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'topic':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC")
			window.writeText(t,False)
			return True

	# |-------|
	# | /quit |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quit' and len(tokens)==1:

			if not gui.askDisconnect(window.client): return True

			if len(config.DEFAULT_QUIT_MESSAGE)>0:
				window.client.quit(config.DEFAULT_QUIT_MESSAGE)
			else:
				window.client.quit()
			gui.quitting[window.client.client_id] = 0
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quit' and len(tokens)>=2:

			if not gui.askDisconnect(window.client): return True
			
			tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language='alias')
			window.client.quit(msg)
			gui.quitting[window.client.client_id] = 0
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quit':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"quit [MESSAGE]")
			window.writeText(t,False)
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
				window.writeText(t,False)
				return True

			window.client.setNick(newnick)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'nick':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"nick NEW_NICKNAME")
			window.writeText(t,False)
			return True

	# |-------|
	# | /part |
	# |-------|
	if len(tokens)>1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)==2:
			tokens.pop(0)
			channel = tokens.pop(0)
			window.client.leave(channel,config.DEFAULT_QUIT_MESSAGE)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'part' and len(tokens)>=3:
			tokens.pop(0)
			channel = tokens.pop(0)
			msg = ' '.join(tokens)
			if config.ENABLE_EMOJI_SHORTCODES: msg = emoji.emojize(msg,language='alias')
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
				t = Message(ERROR_MESSAGE,'',"You have already joined "+window.name)
				window.writeText(t,False)
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
				t = Message(ERROR_MESSAGE,'',"You have already joined "+window.name)
				window.writeText(t,False)
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
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]")
			window.writeText(t,False)
			return True

	return False

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
		for line in self.script.split("\n"):
			line = line.strip()
			if len(line)==0: continue
			tokens = line.split()

			if len(tokens)==2:
				if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'wait':
					count = tokens[1]
					try:
						count = int(count)
					except:
						self.scriptError.emit([self.gui,self.window,config.ISSUE_COMMAND_SYMBOL+'wait must be called with a numerical argument'])
						no_errors = False
					
		if no_errors:
			for line in self.script.split("\n"):
				line = line.strip()
				if len(line)==0: continue

				tokens = line.split()

				if len(tokens)==2:
					if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'wait':
						count = tokens[1]
						count = int(count)
						time.sleep(count)
						continue

				self.execLine.emit([self.gui,self.window,line])

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