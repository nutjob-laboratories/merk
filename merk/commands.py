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

import emoji

from .resources import *
from . import config

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
	}

# The command help system
COMMAND_HELP_INFORMATION = [
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"help</b>", "Displays command usage information" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"me MESSAGE</b>", "Sends a CTCP action message to the current chat" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"msg TARGET MESSAGE</b>", "Sends a message" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"notice TARGET MESSAGE</b>", "Sends a notice" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]</b>", "Joins a channel" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"part CHANNEL [MESSAGE]</b>", "Leaves a channel" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"nick NEW_NICKNAME</b>", "Changes your nickname" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC</b>", "Sets a channel topic" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"mode TARGET MODE...</b>", "Sets a mode on a channel or user" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"kick CHANNEL NICKNAME [MESSAGE]</b>", "Kicks a user from a channel" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"whois NICKNAME [SERVER]</b>", "Requests user information from the server" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"who NICKNAME [o]</b>", "Requests user information from the server" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"whowas NICKNAME [COUNT] [SERVER]</b>", "Requests information about previously connected users" ],
	[ "<b>"+config.ISSUE_COMMAND_SYMBOL+"quit [MESSAGE]</b>", "Disconnects from the current IRC server" ],
]

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

def handleChatCommands(gui,window,user_input):
	tokens = user_input.split()

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
			msg = emoji.emojize(msg,use_aliases=True)
			window.client.describe(window.name,msg)
			t = Message(ACTION_MESSAGE,window.client.nickname,msg)
			window.writeText(t)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'me':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"me MESSAGE")
			window.writeText(t)
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
					msg = emoji.emojize(msg,use_aliases=True)
					window.client.topic(channel,msg)
					return True
				else:
					t = Message(ERROR_MESSAGE,'',"Can't set topic for a private message")
					window.writeText(t)
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
				msg = emoji.emojize(msg,use_aliases=True)
				window.client.leave(channel,msg)
				return True

	return False

def handleCommonCommands(gui,window,user_input):
	tokens = user_input.split()

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
				window.writeText(t)
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
				window.writeText(t)
				return True
			window.client.sendLine("WHOWAS "+nick+" "+str(arg)+" "+serv)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'whowas':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"whowas NICKNAME [COUNT] [SERVER]")
			window.writeText(t)
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
				window.writeText(t)
				return True
			window.client.sendLine("WHO "+nick+" o")
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'who':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"who NICKNAME [o]")
			window.writeText(t)
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
			window.writeText(t)
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
			window.writeText(t)
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
			window.writeText(t)
			return True


	# |---------|
	# | /notice |
	# |---------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'notice' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			msg = emoji.emojize(msg,use_aliases=True)
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
			window.writeText(t)
			return True

	# |------|
	# | /msg |
	# |------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'msg' and len(tokens)>=3:
			tokens.pop(0)
			target = tokens.pop(0)
			msg = ' '.join(tokens)
			msg = emoji.emojize(msg,use_aliases=True)
			window.client.msg(target,msg)

			# If we have the target's window open, write
			# the message there
			w = gui.getWindow(target,window.client)
			if w:
				t = Message(SELF_MESSAGE,window.client.nickname,msg)
				w.writeText(t)

			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'msg':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"msg TARGET MESSAGE")
			window.writeText(t)
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
			msg = emoji.emojize(msg,use_aliases=True)
			window.client.topic(channel,msg)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'topic':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"topic CHANNEL NEW_TOPIC")
			window.writeText(t)
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
			msg = emoji.emojize(msg,use_aliases=True)
			window.client.quit(msg)
			gui.quitting[window.client.client_id] = 0
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'quit':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"quit [MESSAGE]")
			window.writeText(t)
			return True

	# |-------|
	# | /nick |
	# |-------|
	if len(tokens)>=1:
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'nick' and len(tokens)==2:
			tokens.pop(0)
			newnick = tokens.pop(0)

			# Check to see if the user is trying to /join the
			# channel from the same channel they are in
			if window.client.nickname.lower()==newnick.lower():
				t = Message(ERROR_MESSAGE,'',"You are currently using \""+newnick+"\" as a nickname")
				window.writeText(t)
				return True

			window.client.setNick(newnick)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'nick':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"nick NEW_NICKNAME")
			window.writeText(t)
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
			msg = emoji.emojize(msg,use_aliases=True)
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
				window.writeText(t)
				return True

			# Check to see if the user has already joined
			# the channel, and switch to the window if they have
			w = gui.getSubWindow(channel,window.client)
			if w:
				gui.showSubWindow(w)
				return True

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
				window.writeText(t)
				return True

			# Check to see if the user has already joined
			# the channel, and switch to the window if they have
			w = gui.getSubWindow(channel,window.client)
			if w:
				gui.showSubWindow(w)
				return True

			window.client.join(channel,key)
			return True
		if tokens[0].lower()==config.ISSUE_COMMAND_SYMBOL+'join':
			t = Message(ERROR_MESSAGE,'',"Usage: "+config.ISSUE_COMMAND_SYMBOL+"join CHANNEL [KEY]")
			window.writeText(t)
			return True

	return False