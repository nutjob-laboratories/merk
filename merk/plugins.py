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

import sys
import os
from pathlib import Path
import inspect
import importlib
import gc
import hashlib

from pike.manager import PikeManager

from .resources import *
from . import config
from . import commands
from . import render

import emoji

CONFIG_DIRECTORY = None
PLUGIN_DIRECTORY = None
PLUGINS = []
PAUSED = []

class Window():

	def __init__(self,gui,window):
		self._gui = gui
		if hasattr(window,"widget"):
			self._window = window.widget()
		else:
			self._window = window

		if hasattr(self._window,"window_type"):
			self.wtype = self._window.window_type
		else:
			self.wtype = None

	def chat(self):
		return self._window.dumpChat()

	def history(self):
		if config.ENABLE_COMMAND_INPUT_HISTORY:
			return self._window.history_buffer
		else:
			return []

	def size(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			width = w.width()
			height = w.height()
			return [width,height]
		return [0,0]

	def position(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			p = w.pos()
			return [p.x(),p.y()]
		return [0,0]

	def active(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			if self._gui.MDI.activeSubWindow()==w:
				return True
			else:
				return False
		return False

	def key(self,new_key=None):
		if self.wtype!=CHANNEL_WINDOW: return None
		if self._window.name in self._window.client.channelkeys:
			if new_key==None:
				return self._window.client.channelkeys[self._window.name]
			else:
				self._window.client.mode(self._window.name,False,'k '+new_key)
				return True
		else:
			if new_key==None:
				return None
			else:
				self._window.client.mode(self._window.name,True,'k '+new_key)
				return True
			return None

	def uptime(self):
		return self._window.uptime

	def modes(self):
		if self.wtype!=CHANNEL_WINDOW: return None
		if len(self._window.client.channelmodes[self._window.name])>0:
			return self._window.client.channelmodes[self._window.name]

	def bans(self):
		if self.wtype!=CHANNEL_WINDOW: return None
		if len(self._window.banlist)>0:
			return self._window.banlist
		else:
			return []

	def status(self,status=None):
		if status==None:
			if self.wtype!=CHANNEL_WINDOW: return 'normal'
			if self._window.owner: return 'owner'
			if self._window.admin: return 'admin'
			if self._window.operator: return 'operator'
			if self._window.halfop: return 'halfop'
			if self._window.protected: return 'protected'
			if self._window.voiced: return 'voiced'
			return 'normal'

		if self.wtype!=CHANNEL_WINDOW: return False
		if self._window.owner and status.lower()=='owner': return True
		if self._window.admin and status.lower()=='admin': return True
		if self._window.operator and status.lower()=='operator': return True
		if self._window.halfop and status.lower()=='halfop': return True
		if self._window.protected and status.lower()=='protected': return True
		if self._window.voiced and status.lower()=='voiced': return True
		if status.lower()=='normal': return True
		return False

	def title(self,title=None):
		if title==None:
			return self._window.windowTitle()
		else:
			self._window.setWindowTitle(title)

	def script(self,script,arguments):

		f = commands.find_file(script,SCRIPT_FILE_EXTENSION)
		if f!=None:
			s = open(f,"r")
			script = s.read()
			s.close()
		
		commands.executeScript(self._gui,self._window,script,f,arguments)

	def resize(self,width,height):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			w.resize(width,height)

	def clear(self):
		self._window.clearChat()

	def move(self,x,y):
		if self._gui.is_valid_position(self._window,x,y):
			self._window.move(x,y)
			return True
		else:
			return False

	def maximized(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			return w.isMaximized()
		return False

	def max(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			w.showMaximized()

	def minimized(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			return w.isMinimized()
		return False

	def min(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			w.showMinimized()

	def close(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			w.close()
		self._gui.initWindowbar()

	def hide(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			w.hide()
		self._gui.initWindowbar()

	def show(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			w.show()
		self._gui.initWindowbar()

	def restore(self):
		w = self._gui.getSubWindow(self._window.name,self._window.client)
		if w:
			w.showNormal()

	def name(self):
		return self._window.name

	def type(self):
		if self.wtype==CHANNEL_WINDOW:
			return "channel"
		elif self.wtype==PRIVATE_WINDOW:
			return "private"
		elif self.wtype==SERVER_WINDOW:
			return "server"
		else:
			return "unknown"

	def notice(self,target,message):
		message = commands.fullInterpolate(self._gui,self._window,message)
		if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
		if config.ENABLE_ASCIIMOJI_SHORTCODES: message = emojize(message)
		self._window.client.notice(target,message)
		w = self._gui.getWindow(target,self._window.client)
		if w:
			t = Message(NOTICE_MESSAGE,self._window.client.nickname,message)
			w.writeText(t)
			return True
		return False

	def action(self,target,message):
		message = commands.fullInterpolate(self._gui,self._window,message)
		if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
		if config.ENABLE_ASCIIMOJI_SHORTCODES: message = emojize(message)
		self._window.client.describe(target,message)
		w = self._gui.getWindow(target,self._window.client)
		if w:
			t = Message(ACTION_MESSAGE,self._window.client.nickname,message)
			w.writeText(t)
			return True
		return False

	def message(self,target,message):
		message = commands.fullInterpolate(self._gui,self._window,message)
		if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
		if config.ENABLE_ASCIIMOJI_SHORTCODES: message = emojize(message)
		self._window.client.msg(target,message)
		w = self._gui.getWindow(target,self._window.client)
		if w:
			t = Message(CHAT_MESSAGE,self._window.client.nickname,message)
			w.writeText(t)
			return True
		return False

	def say(self,message):
		if self.wtype==CHANNEL_WINDOW or self.wtype==PRIVATE_WINDOW:
			message = commands.fullInterpolate(self._gui,self._window,message)
			if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: message = emojize(message)
			self._window.client.msg(self._window.name,message)
			t = Message(CHAT_MESSAGE,self._window.client.nickname,message)
			self._window.writeText(t)
			return True
		return False

	def note(self,message):
		if self.wtype==CHANNEL_WINDOW or self.wtype==PRIVATE_WINDOW:
			message = commands.fullInterpolate(self._gui,self._window,message)
			if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: message = emojize(message)
			self._window.client.notice(self._window.name,message)
			t = Message(NOTICE_MESSAGE,self._window.client.nickname,message)
			self._window.writeText(t)
			return True
		return False

	def describe(self,message):
		if self.wtype==CHANNEL_WINDOW or self.wtype==PRIVATE_WINDOW:
			message = commands.fullInterpolate(self._gui,self._window,message)
			if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
			if config.ENABLE_ASCIIMOJI_SHORTCODES: message = emojize(message)
			self._window.client.describe(self._window.name,message)
			t = Message(ACTION_MESSAGE,self._window.client.nickname,message)
			self._window.writeText(t)
			return True
		return False

	def execute(self,command):
		self._window.handleHotkeyCommand(command)

	def client(self):
		return self._window.client

	def print(self,message):
		message = commands.fullInterpolate(self._gui,self._window,message)
		if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
		if config.ENABLE_ASCIIMOJI_SHORTCODES: message = emojize(message)
		t = Message(RAW_SYSTEM_MESSAGE,'',f"{message}")
		self._window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

	def prints(self,message):
		message = commands.fullInterpolate(self._gui,self._window,message)
		if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
		if config.ENABLE_ASCIIMOJI_SHORTCODES: message = emojize(message)
		t = Message(SYSTEM_MESSAGE,'',f"{message}")
		self._window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

	def alias(self,text):
		return commands.fullInterpolate(self._gui,self._window,text)

	def users(self,status=None):
		if self.wtype!=CHANNEL_WINDOW: return []
		if status==None: return self._window.users

		if status.lower()=='normal':
			if len(self._window.users_normal)==0: return []
			return self._window.users_normal

		if status.lower()=='protected':
			if len(self._window.users_protected)==0: return []
			return self._window.users_protected

		if status.lower()=='halfop':
			if len(self._window.users_halfop)==0: return []
			return self._window.users_halfop

		if status.lower()=='admin':
			if len(self._window.users_admin)==0: return []
			return self._window.users_admin

		if status.lower()=='owner':
			if len(self._window.users_owner)==0: return []
			return self._window.users_owner

		if status.lower()=='voiced':
			if len(self._window.users_voiced)==0: return []
			return self._window.users_voiced
		
		if status.lower()=='operator':
			if len(self._window.users_operator)==0: return []
			return self._window.users_operator

		return []

	def nicks(self):
		if self.wtype==CHANNEL_WINDOW:
			output = []
			for u in self._window.users:
				output.append(self._window.clean_nick(u))
			return output
		return []

	def topic(self,new_topic=None):
		if self.wtype==CHANNEL_WINDOW:
			if new_topic==None:
				return self._window.channel_topic
			else:
				self._window.client.topic(self._window.name,new_topic)
				return True
		else:
			if new_topic!=None: return False
		return None

class Console():
	_console = None

	def __init__(self,gui,plugin):
		self._gui = gui
		self._plugin = plugin

		self._subwindow,self._console = self._gui.openConsole(self._plugin)

		if self._gui.plugin_manager!=None: self._gui.plugin_manager.update_console(self._plugin)

	def dump(self):
		return self._console.dump()

	def print(self,message):
		t = Message(RAW_SYSTEM_MESSAGE,'',f"{message}")
		self._console.writeText(t)

	def prints(self,message):
		t = Message(SYSTEM_MESSAGE,'',f"{message}")
		self._console.writeText(t)

	def title(self,title=None):
		if title==None:
			return self._subwindow.windowTitle()
		else:
			self._subwindow.setWindowTitle(title)
			self._gui.buildWindowsMenu()

	def clear(self):
		self._console.chat.clear()
		self._console.log = []

	def min(self):
		self._subwindow.showMinimized()

	def max(self):
		self._subwindow.showMaximized()

	def minimized(self):
		if self._subwindow.isMinimized():
			return True
		else:
			return False

	def maximized(self):
		if self._subwindow.isMaximized():
			return True
		else:
			return False

	def restore(self):
		self._subwindow.showNormal()

	def show(self):
		self._subwindow.show()

	def hide(self):
		self._subwindow.close()

	def close(self):
		self._console.force_close = True
		self._console.close()
		self._subwindow.close()

		if self._gui.plugin_manager!=None: self._gui.plugin_manager.update_console(self._plugin)

	def move(self,x_val,y_val):
		if self._gui.is_move_valid_on_screen(self._gui,x_val,y_val):
			if self._subwindow.isMaximized() or self._subwindow.isMinimized(): self._subwindow.showNormal()
			self._subwindow.move(x_val,y_val)
			return True
		return False

	def resize(self,x_val,y_val):
		if self._subwindow.isMaximized() or self._subwindow.isMinimized(): self._subwindow.showNormal()
		self._subwindow.resize(x_val,y_val)

	def size(self):
		width = self._subwindow.width()
		height = self._subwindow.height()
		return [width,height]

	def position(self):
		p = self._subwindow.pos()
		return [p.x(),p.y()]

class Plugin():

	_gui = None

	NAME = "Unknown"
	AUTHOR = "Unknown"
	VERSION = "1.0"
	SOURCE = "Unknown"

	def current(self):
		if self._gui!=None:
			w = self._gui.getCurrentChat()
			if w==None:
				return None
			else:
				return Window(self._gui,w)
		return None

	def markup(self,text):
		text = emoji.emojize(text,language=config.EMOJI_LANGUAGE)
		text = emojize(text)
		text = markdown_to_irc(text)
		text = inject_irc_colors(text)
		return text

	def unmarkup(self,text):
		text = demojize(text)
		text = emoji.demojize(text)
		return decode_irc_formatting(text)

	def folder(self,path):
		if self._gui!=None:
			if os.path.isdir(path):
				self._gui.open_folder(path)

	def browser(self,url):
		if self._gui!=None:
			if has_url(url) and url.count(' ')==0:
				self._gui.openLinkInBrowser(url)

	def colored(text):
		return string_has_irc_formatting_codes(text)

	def strip(self,text):
		return render.strip_color(text)

	def markdown(self,text):
		return markdown_to_irc(text)

	def unmarkdown(self,text):
		return irc_to_markdown(text)

	def color(self,text):
		return inject_irc_colors(text)

	def uncolor(self,text):
		return decode_irc_colors(text)

	def connect(self,server,port,password=None,ssl=False,reconnect=False):
		commands.connect_to_irc(self._gui,None,server,port,password,ssl,reconnect)

	def xconnect(self,server,port,password=None,ssl=False,reconnect=False):
		commands.connect_to_irc(self._gui,None,server,port,password,ssl,reconnect,True)

	def console(self):
		return Console(self._gui,self)

	def id(self):
		return self._id

	def resize(self,x_val,y_val):
		if self._gui!=None:
			if self._gui.isMaximized() or self._gui.isMinimized(): self._gui.showNormal()
			self._gui.resize(x_val,y_val)

	def move(self,x_val,y_val):
		if self._gui!=None:
			if self._gui.is_move_valid_on_screen(self._gui,x_val,y_val):
				if self._gui.isMaximized() or self._gui.isMinimized(): self._gui.showNormal()
				self._gui.move(x_val,y_val)
				return True
		return False

	def emojize(self,message):
		return emoji.emojize(message,language=config.EMOJI_LANGUAGE)

	def asciimojize(self,message):
		return emojize(message)

	def demojize(self,message):
		return emoji.demojize(message)

	def deasciimojize(self,message):
		return demojize(message)

	def unmacro(self,name):
		if self._gui!=None:
			if not commands.does_macro_name_exist(name): return False
			commands.remove_macro(name)
			return True

	def macro(self,name,script,musage=None,mhelp=None):
		if self._gui!=None:
			# If the first character is the issue command
			# symbol, strip that out of the name
			if len(name)>len(config.ISSUE_COMMAND_SYMBOL):
				il = len(config.ISSUE_COMMAND_SYMBOL)
				if name[:il] == config.ISSUE_COMMAND_SYMBOL:
					name = name[il:]

			# Make sure that macro names start with a letter
			if len(name)>=1:
				if not name[0].isalpha(): return False
			else:
				return False

			if not commands.is_valid_macro_name(name): return False

			if commands.does_macro_name_exist(name): return False

			efilename = commands.find_file(script,SCRIPT_FILE_EXTENSION)
			if not efilename: return False

			if musage!=None and len(musage.strip())==0: musage = None
			if mhelp!=None and len(mhelp.strip())==0: mhelp = None

			if musage==None and mhelp!=None: musage = config.ISSUE_COMMAND_SYMBOL+name

			commands.add_macro(name,script,musage,mhelp)
			return True
		return False

	def unbind(self,sequence):
		if self._gui!=None:
			if sequence=='*':
				self._gui.remove_all_shortcuts()
			else:
				self._gui.remove_shortcut(sequence)
			self._gui.save_shortcuts()
			if self._gui.hotkey_manager!=None:
				self._gui.hotkey_manager.refresh()

	def bind(self,sequence,command):
		if self._gui!=None:
			r = self._gui.add_shortcut(sequence,command)
			if r==BAD_SHORTCUT or r==SHORTCUT_IN_USE: return False
			self._gui.save_shortcuts()
			if self._gui.hotkey_manager!=None:
				self._gui.hotkey_manager.refresh()
			return True
		return False

	def script(self,client,script,arguments):
		if self._gui!=None:

			f = commands.find_file(script,SCRIPT_FILE_EXTENSION)
			if f!=None:
				s = open(f,"r")
				script = s.read()
				s.close()
		
			w = self._gui.getServerSubWindow(client)
			if w:
				commands.executeScript(self._gui,w,script,f,arguments)
				return True
		return False
		
	def is_ignored(self,nickname,hostmask):
		if self._gui==None: return False
		return self._gui.is_ignored(nickname,hostmask)

	def alias(self,alias=None,value=None):
		if not config.ENABLE_ALIASES: return None

		# Return list of aliases
		if alias==None and value==None:
			return commands.ALIAS

		# Return alias value
		if alias!=None and value==None:
			if alias in commands.ALIAS:
				return commands.ALIAS[alias]
			else:
				return None

		# Set alias value
		if alias!=None and value!=None:

			if len(alias)>len(config.ALIAS_INTERPOLATION_SYMBOL):
				il = len(config.ALIAS_INTERPOLATION_SYMBOL)
				if alias[:il] == config.ALIAS_INTERPOLATION_SYMBOL:
					alias = alias[il:]

			if len(alias)>=1:
				if not alias[0].isalpha(): return False

			commands.ALIAS[alias] = value
			return True

	def ignores(self):
		return config.IGNORE_LIST

	def unignore(self,user):
		if self._gui!=None:
			if not user in config.IGNORE_LIST: return False
			config.IGNORE_LIST.remove(user)
			config.save_settings(config.CONFIG_FILE)
			self._gui.reRenderAll(True)
			self._gui.rerenderUserlists()
			if self._gui.ignore_manager!=None:
				self._gui.ignore_manager.refresh()
			return True

	def ignore(self,user):
		if self._gui!=None:
			if user in config.IGNORE_LIST: return False
			config.IGNORE_LIST.append(user)
			config.save_settings(config.CONFIG_FILE)
			self._gui.reRenderAll(True)
			self._gui.rerenderUserlists()
			if self._gui.ignore_manager!=None:
				self._gui.ignore_manager.refresh()
			return True

	def all_servers(self):
		if self._gui!=None:
			output = []
			for w in self._gui.getTotalWindows():
				if w.window_type==SERVER_WINDOW:
					output.append(Window(self._gui,w))
			return output
		return []

	def all_privates(self):
		if self._gui!=None:
			output = []
			for w in self._gui.getTotalWindows():
				if w.window_type==PRIVATE_WINDOW:
					output.append(Window(self._gui,w))
			return output
		return []

	def privates(self,client):
		if self._gui!=None:
			output = []
			for w in self._gui.getAllConnectedWindows(client):
				if w.window_type==PRIVATE_WINDOW:
					output.append(Window(self._gui,w))
			return output
		return []

	def all_channels(self):
		if self._gui!=None:
			output = []
			for w in self._gui.getTotalWindows():
				if w.window_type==CHANNEL_WINDOW:
					output.append(Window(self._gui,w))
			return output
		return []

	def channels(self,client):
		if self._gui!=None:
			output = []
			for w in self._gui.getAllConnectedWindows(client):
				if w.window_type==CHANNEL_WINDOW:
					output.append(Window(self._gui,w))
			return output
		return []

	def restore(self):
		self._gui.showNormal()

	def maximized(self):
		return self._gui.isMaximized()

	def max(self):
		self._gui.showMaximized()

	def minimized(self):
		return self._gui.isMinimized()

	def min(self):
		self._gui.showMinimized()

	def find(self,filename,extension=None):
		return commands.find_file_plugin(filename,extension)

	def home(self):
		return f"{CONFIG_DIRECTORY}"

	def clients(self):
		if self._gui!=None:
			return self._gui.getAllClients()
		return []

	def modes(self,client):
		return client.usermodes

	def server_window(self,client):
		if self._gui!=None:
			w = self._gui.getServerSubWindow(client)
			if w:
				return Window(self._gui,w)
		return None

	def channel(self,client,channel):
		if self._gui!=None:
			w = self._gui.getSubWindow(channel,client)
			if w:
				c = w.widget()
				if c.window_type==CHANNEL_WINDOW:
					return Window(self._gui,c)
		return None

	def private(self,client,user,create_new=False):
		if self._gui!=None:
			w = self._gui.getSubWindow(user,user)
			if w:
				c = w.widget()
				if c.window_type==PRIVATE_WINDOW:
					return Window(self._gui,c)
			if create_new:
				w = self._gui.openPrivate(client,user)
				w.show()
				return Window(self._gui,w.widget())
		return None

	def windows(self,client):
		if self._gui!=None:
			output = []
			for w in self._gui.getAllConnectedWindows(client):
				output.append(Window(self._gui,w))
			return output
		return []

	def all_windows(self):
		if self._gui!=None:
			output = []
			for w in self._gui.getTotalWindows():
				output.append(Window(self._gui,w))
			return output
		return []

	def is_away(self,client):
		if client.is_away:
			return True
		else:
			return False
	
	def list(self,client):
		if len(client.server_channel_list):
			output = []
			for entry in client.server_channel_list:
				e = []
				e.append(entry[0])
				e.append(entry[1])
				e.append(entry[2])
				output.append(e)
			return output
		else:
			return []

EVENTS = [
	'message', 'notice', 'action', 'left', 'joined', 'part', 'join', 
	'kick', 'kicked', 'tick', 'mode', 'unmode', 'quit', 'line_in', 'line_out', 
	'away', 'back', 'activate', 'invite', 'rename', 'topic', 'connected', 
	'connecting', 'lost', 'ctick', 'nick', 'disconnect', 'init','ping','motd',
	'server', 'subwindow', 'close', 'me', 'error', 'isupport','ison', 'uninstall',
	'unload', 'uptime', 'pause', 'unpause',
]

BUILT_IN = [
	'alias', 'all_channels', 'all_servers', 'all_privates',
	'all_windows', 'bind', 'channel', 'channels', 'clients',
	'console', 'emojize', 'find', 'home', 'id', 'ignore',
	'ignores', 'is_away', 'is_ignored', 'list', 'macro',
	'server_window', 'max', 'maximized', 'min', 'minimized', 'modes',
	'move', 'private', 'privates', 'resize', 'restore', 'script',
	'unbind', 'unignore', 'windows', 'unmacro', 'asciimojize',
	'connect', 'xconnect', 'markdown','color', 'strip', 'colored',
	'browser', 'folder', 'current', 'uncolor', 'unmarkdown',
	'markup','unmarkup','demojize','deasciimojize',
]

def uninstall(obj):
	if not config.ENABLE_PLUGINS: return
	if not config.PLUGIN_UNINSTALL: return
	if hasattr(obj,"uninstall"):
		try:
			obj.uninstall()
		except Exception as e:
			if config.DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS:
				QMessageBox.critical(obj._gui, f'{obj.NAME} {obj.VERSION} ({obj._filename})', f'Error executing event \"uninstall\": {e}')
				sys.stdout.write(f"Error executing {obj._filename} event \"uninstall\": {e}\n")
			else:
				sys.stdout.write(f"Error executing {obj._filename} event \"uninstall\": {e}\n")

def remove_plugin(obj):
	global PLUGINS
	if not config.ENABLE_PLUGINS: return
	if config.PLUGIN_UNINSTALL:
		if hasattr(obj,"uninstall"):
			try:
				obj.uninstall()
			except Exception as e:
				if config.DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS:
					QMessageBox.critical(obj._gui, f'{obj.NAME} {obj.VERSION} ({obj._filename})', f'Error executing event \"uninstall\": {e}')
					sys.stdout.write(f"Error executing {obj._filename} event \"uninstall\": {e}\n")
				else:
					sys.stdout.write(f"Error executing {obj._filename} event \"uninstall\": {e}\n")

	if config.PLUGIN_UNLOAD:
		if hasattr(obj,"unload"):
			try:
				obj.unload()
			except Exception as e:
				if config.DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS:
					QMessageBox.critical(obj._gui, f'{obj.NAME} {obj.VERSION} ({obj._filename})', f'Error executing event \"unload\": {e}')
					sys.stdout.write(f"Error executing {obj._filename} event \"unload\": {e}\n")
				else:
					sys.stdout.write(f"Error executing {obj._filename} event \"unload\": {e}\n")

	if obj._module in sys.modules:
		del sys.modules[obj._module]

	PLUGINS.remove(obj)
	gc.collect()

def init(obj):
	if not config.ENABLE_PLUGINS: return
	if not config.PLUGIN_INIT: return
	if hasattr(obj,"init"):
		try:
			obj.init()
		except Exception as e:
			if config.DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS:
				QMessageBox.critical(obj._gui, f'{obj.NAME} {obj.VERSION} ({obj._filename})', f'Error executing event \"init\": {e}')
				sys.stdout.write(f"Error executing {obj._filename} event \"init\": {e}\n")
			else:
				sys.stdout.write(f"Error executing {obj._filename} event \"init\": {e}\n")

def call(gui,method,**arguments):
	if not config.ENABLE_PLUGINS: return
	if method=='message' and not config.PLUGIN_MESSAGE: return
	if method=='notice' and not config.PLUGIN_NOTICE: return
	if method=='action' and not config.PLUGIN_ACTION: return
	if method=='left' and not config.PLUGIN_LEFT: return
	if method=='joined' and not config.PLUGIN_JOINED: return
	if method=='part' and not config.PLUGIN_PART: return
	if method=='join' and not config.PLUGIN_JOIN: return
	if method=='kick' and not config.PLUGIN_KICK: return
	if method=='kicked' and not config.PLUGIN_KICKED: return
	if method=='tick' and not config.PLUGIN_TICK: return
	if method=='mode' and not config.PLUGIN_MODE: return
	if method=='unmode' and not config.PLUGIN_UNMODE: return
	if method=='quit' and not config.PLUGIN_QUIT: return
	if method=='line_in' and not config.PLUGIN_IN: return
	if method=='line_out' and not config.PLUGIN_OUT: return
	if method=='away' and not config.PLUGIN_AWAY: return
	if method=='back' and not config.PLUGIN_BACK: return
	if method=='activate' and not config.PLUGIN_ACTIVATE: return
	if method=='invite' and not config.PLUGIN_INVITE: return
	if method=='rename' and not config.PLUGIN_RENAME: return
	if method=='topic' and not config.PLUGIN_TOPIC: return
	if method=='connected' and not config.PLUGIN_CONNECTED: return
	if method=='connecting' and not config.PLUGIN_CONNECTING: return
	if method=='lost' and not config.PLUGIN_LOST: return
	if method=='ctick' and not config.PLUGIN_CTICK: return
	if method=='nick' and not config.PLUGIN_NICK: return
	if method=='disconnect' and not config.PLUGIN_DISCONNECT: return
	if method=='ping' and not config.PLUGIN_PING: return
	if method=='motd' and not config.PLUGIN_MOTD: return
	if method=='server' and not config.PLUGIN_SERVER: return
	if method=='subwindow' and not config.PLUGIN_SUBWINDOW: return
	if method=='close' and not config.PLUGIN_CLOSE: return
	if method=='me' and not config.PLUGIN_ME: return
	if method=='error' and not config.PLUGIN_ERROR: return
	if method=='isupport' and not config.PLUGIN_ISUPPORT: return
	if method=='ison' and not config.PLUGIN_ISON: return
	if method=='unload' and not config.PLUGIN_UNLOAD: return
	if method=='uptime' and not config.PLUGIN_UPTIME: return

	for obj in PLUGINS:
		if paused(obj): continue
		if hasattr(obj,method):
			m = getattr(obj,method)

			try:
				if 'window' in arguments:
					if arguments['window']!=None:
						arguments["window"] = Window(gui,arguments["window"])
				m(**arguments)
			except Exception as e:
				if config.DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS:
					QMessageBox.critical(gui, f'{obj.NAME} {obj.VERSION} ({obj._filename})', f'Error executing event \"{method}\": {e}')
					sys.stdout.write(f"Error executing {obj._filename} event \"{method}\": {e}\n")
				else:
					sys.stdout.write(f"Error executing {obj._filename} event \"{method}\": {e}\n")

def command_call(gui,window,method,arguments):
	if not config.ENABLE_PLUGINS: return
	window = Window(gui,window)
	for obj in PLUGINS:
		if paused(obj): continue
		if hasattr(obj,method):
			m = getattr(obj,method)

			specs = inspect.getfullargspec(m)
			if len(specs.args)==3:
				try:
					m(window,arguments)
				except Exception as e:
					if config.DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS:
						QMessageBox.critical(gui, f'{obj.NAME} {obj.VERSION} ({obj._filename})', f'Error executing event \"{method}\": {e}')
						sys.stdout.write(f"Error executing {obj._filename} event \"{method}\": {e}\n")
					else:
						sys.stdout.write(f"Error executing {obj._filename} event \"{method}\": {e}\n")

def pause_event(obj):
	if not config.ENABLE_PLUGINS: return
	if not config.PLUGIN_PAUSE: return
	if hasattr(obj,"pause"):
		try:
			obj.pause()
		except Exception as e:
			if config.DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS:
				QMessageBox.critical(obj._gui, f'{obj.NAME} {obj.VERSION} ({obj._filename})', f'Error executing event \"pause\": {e}')
				sys.stdout.write(f"Error executing {obj._filename} event \"pause\": {e}\n")
			else:
				sys.stdout.write(f"Error executing {obj._filename} event \"pause\": {e}\n")

def unpause_event(obj):
	if not config.ENABLE_PLUGINS: return
	if not config.PLUGIN_UNPAUSE: return
	if hasattr(obj,"unpause"):
		try:
			obj.unpause()
		except Exception as e:
			if config.DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS:
				QMessageBox.critical(obj._gui, f'{obj.NAME} {obj.VERSION} ({obj._filename})', f'Error executing event \"unpause\": {e}')
				sys.stdout.write(f"Error executing {obj._filename} event \"unpause\": {e}\n")
			else:
				sys.stdout.write(f"Error executing {obj._filename} event \"unpause\": {e}\n")

def pause(obj):
	if not obj._id in PAUSED:
		pause_event(obj)
		PAUSED.append(obj._id)

def unpause(obj):
	if obj._id in PAUSED:
		unpause_event(obj)
		PAUSED.remove(obj._id)

def paused(obj):
	if obj._id in PAUSED:
		return True
	return False

def list_all_call_methods():
	output = []
	for obj in PLUGINS:
		if paused(obj): continue
		all_methods = inspect.getmembers(obj, predicate=inspect.ismethod)
		method_names = [name for name, method in all_methods]

		for m in method_names:
			if m=='__init__': continue
			if m in EVENTS: continue
			if m in BUILT_IN: continue
			mi = getattr(obj,m)
			specs = inspect.getfullargspec(mi)
			if len(specs.args)!=3: continue
			output.append(m)
	return output

def count_callable_methods(obj):
	callables = 0
	all_methods = inspect.getmembers(obj, predicate=inspect.ismethod)
	method_names = [name for name, method in all_methods]

	for m in method_names:
		if m=='__init__': continue
		if m in EVENTS: continue
		if m in BUILT_IN: continue
		mi = getattr(obj,m)
		specs = inspect.getfullargspec(mi)
		if len(specs.args)!=3: continue
		callables = callables + 1
	return callables

def is_valid_call_method(method):
	if method in EVENTS: return EVENT_METHOD
	if method in BUILT_IN: return BUILT_IN_METHOD
	for obj in PLUGINS:
		if hasattr(obj,method):
			if paused(obj): return NO_METHOD
			mi = getattr(obj,method)
			specs = inspect.getfullargspec(mi)
			if len(specs.args)==3:
				return VALID_METHOD
			else:
				return INVALID_METHOD
	return NO_METHOD

def get_plugin(path):
	for obj in PLUGINS:
		if obj._filename==path: return obj
		if obj._basename==os.path.basename(path): return obj
	return None

def load_plugins(gui):
	global PLUGINS
	
	PLUGIN_IDS = []
	ERRORS = []

	if len(PLUGINS)>0:
		for o in PLUGINS:
			PLUGIN_IDS.append(str(o._id))

	# Remove the old plugins from memory
	if config.CLEAR_PLUGINS_FROM_MEMORY_ON_RELOAD:
		modules_to_reload = set(obj.__class__.__module__ for obj in PLUGINS)
		
	PLUGINS.clear()

	if config.CLEAR_PLUGINS_FROM_MEMORY_ON_RELOAD:
		for mod_name in modules_to_reload:
			if mod_name in sys.modules:
				del sys.modules[mod_name]

	if not config.ENABLE_PLUGINS:
		if config.CLEAR_PLUGINS_FROM_MEMORY_ON_RELOAD: gc.collect()
		return

	with PikeManager([PLUGIN_DIRECTORY]) as mgr:
		classes = mgr.get_classes()

	for c in classes:
		# Ignore the base plugin class
		if c.__name__=="Plugin": continue

		# Only load Plugin subclasses as plugins
		# Do not try to create an instance of classes
		# that are not plugin classes
		if issubclass(c, Plugin):

			# Store any loading errors
			PLUGIN_LOAD_ERRORS = []

			try:
				# Create an instance of the plugin class
				obj = c()

				# Make sure that the class has access to
				# the "parent" window
				obj._gui = gui

				# Make sure the plugin has some necessary attributes
				obj._filename = inspect.getfile(c)
				obj._basename = os.path.basename(obj._filename)
				obj._calls = count_callable_methods(obj)
				obj._module = obj.__class__.__module__
				obj._class = obj.__class__.__name__

				# Find out if the plugin has an icon
				name_without_extension, extension = os.path.splitext(obj._filename)
				icon_filename = name_without_extension + ".png"
				if not os.path.exists(icon_filename):
					icon_filename = None
				obj._icon = icon_filename

				# Count the number of events
				obj._events = 0
				for e in EVENTS:
					if hasattr(obj,e):
						obj._events = obj._events + 1

				# Set default necessary attributes if
				# they do not exist
				if not hasattr(obj,"NAME"): obj.NAME = "Unknown"
				if not hasattr(obj,"AUTHOR"): obj.AUTHOR = "Unknown"
				if not hasattr(obj,"SOURCE"): obj.SOURCE = "Unknown"
				if not hasattr(obj,"VERSION"): obj.VERSION = "1.0"

				# Build the plugin's ID hash
				obj._id = hashlib.md5(f"{obj._filename}{obj._module}{obj._class}".encode()).hexdigest()

				# Check to see if we've already loaded this
				# plugin in this session
				if obj._id in PLUGIN_IDS:
					plugin_is_being_reloaded = True
				else:
					plugin_is_being_reloaded = False

				# Count the number of methods
				instance_methods = inspect.getmembers(obj, predicate=inspect.ismethod)
				obj._methods = len(instance_methods) - obj._events
				obj._methods = obj._methods - len(BUILT_IN)
				if obj._methods<0: obj._methods = 0

				# Make sure the plugin has at least one
				# event or callable methods
				if obj._events==0 and obj._calls==0:
					PLUGIN_LOAD_ERRORS.append(f"{obj._basename} doesn't contain any events or callable methods")
						
				# Add the plugin to the registry if
				# the plugin had no loading errors
				if len(PLUGIN_LOAD_ERRORS)==0:
					PLUGINS.append(obj)

					# Execute plugin init
					if config.EXECUTE_INIT_ON_PLUGIN_RELOAD:
						if not paused(obj):
							init(obj)
					else:
						if not plugin_is_being_reloaded:
							init(obj)
			except Exception as e:
				PLUGIN_LOAD_ERRORS.append(f"Error loading plugin class \"{c.__name__}\": {e}")

			# Append any loading errors to the main
			# error list
			for e in PLUGIN_LOAD_ERRORS:
				ERRORS.append(e)

	# Call the garbage collector, if needed
	if config.CLEAR_PLUGINS_FROM_MEMORY_ON_RELOAD: gc.collect()

	# Reload the plugin manager, if it's open
	if gui.plugin_manager!=None:
		gui.plugin_manager.refresh()

	# Return any errors
	return ERRORS

def list_all_plugins():
	output = {}
	for obj in PLUGINS:
		output[f"{obj.NAME} {obj.VERSION}"] = obj._basename
	return output

def list_plugin_files():
	file_paths = []
	for root, _, files in os.walk(PLUGIN_DIRECTORY):
		for file in files:
			name_without_extension, extension = os.path.splitext(file)
			if extension.lower()=='.py':
				file_paths.append(os.path.basename(os.path.join(root, file)))
	file_paths = list(set(file_paths))
	return file_paths

def initialize(directory,directory_name):
	global CONFIG_DIRECTORY
	global PLUGIN_DIRECTORY

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	# The config directory should already be created
	CONFIG_DIRECTORY = os.path.join(directory,directory_name)

	PLUGIN_DIRECTORY = os.path.join(CONFIG_DIRECTORY,"plugins")
	if not os.path.isdir(PLUGIN_DIRECTORY): os.mkdir(PLUGIN_DIRECTORY)
