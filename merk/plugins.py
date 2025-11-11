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

from pike.manager import PikeManager

from .resources import *
from . import config
from . import commands

import emoji

CONFIG_DIRECTORY = None
PLUGIN_DIRECTORY = None
PLUGINS = []

class Window():

	def __init__(self,gui,window):
		self._gui = gui
		if hasattr(window,"widget"):
			self._window = window.widget()
		else:
			self._window = window

	def status(self,status=None):
		if status==None:
			if self._window.window_type!=CHANNEL_WINDOW: return 'normal'
			if self._window.owner: return 'owner'
			if self._window.admin: return 'admin'
			if self._window.operator: return 'operator'
			if self._window.halfop: return 'halfop'
			if self._window.protected: return 'protected'
			if self._window.voiced: return 'voiced'

			return 'normal'

		if self._window.window_type!=CHANNEL_WINDOW: return False
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
			self._window.setWindowTitle(self._window.name)
		else:
			return self._window.windowTitle()

	def script(self,script,arguments):
		commands.executeScript(self._gui,self._window,script,None,arguments)

	def resize(self,width,height):
		self._window.resize(width,height)

	def move(self,x,y):
		if self._gui.is_valid_position(self._window,x,y):
			self._window.move(x,y)
			return True
		else:
			return False

	def maximized(self):
		return self._window.isMaximized()

	def max(self):
		self._window.showMaximized()

	def minimized(self):
		return self._window.isMinimized()

	def min(self):
		self._window.showMinimized()

	def hide(self):
		self._window.hide()

	def show(self):
		self._window.show()

	def restore(self):
		self._window.showNormal()

	def name(self):
		return self._window.name

	def type(self):
		if self._window.window_type==CHANNEL_WINDOW:
			return "channel"
		elif self._window.window_type==PRIVATE_WINDOW:
			return "private"
		elif self._window.window_type==SERVER_WINDOW:
			return "server"
		else:
			return "unknown"

	def notice(self,target,message):
		if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
		message = commands.fullInterpolate(self._gui,self._window,message)
		self._window.client.notice(target,message)
		w = self._gui.getWindow(target,self._window.client)
		if w:
			t = Message(NOTICE_MESSAGE,self._window.client.nickname,message)
			w.writeText(t)
			return True
		return False

	def action(self,target,message):
		if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
		message = commands.fullInterpolate(self._gui,self._window,message)
		self._window.client.describe(target,message)
		w = self._gui.getWindow(target,self._window.client)
		if w:
			t = Message(ACTION_MESSAGE,self._window.client.nickname,message)
			w.writeText(t)
			return True
		return False

	def message(self,target,message):
		if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
		message = commands.fullInterpolate(self._gui,self._window,message)
		self._window.client.msg(target,message)
		w = self._gui.getWindow(target,self._window.client)
		if w:
			t = Message(CHAT_MESSAGE,self._window.client.nickname,message)
			w.writeText(t)
			return True
		return False

	def say(self,message):
		if self._window.window_type==CHANNEL_WINDOW or self._window.window_type==PRIVATE_WINDOW:
			if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
			message = commands.fullInterpolate(self._gui,self._window,message)
			self._window.client.msg(self._window.name,message)
			t = Message(CHAT_MESSAGE,self._window.client.nickname,message)
			self._window.writeText(t)
			return True
		return False

	def note(self,message):
		if self._window.window_type==CHANNEL_WINDOW or self._window.window_type==PRIVATE_WINDOW:
			if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
			message = commands.fullInterpolate(self._gui,self._window,message)
			self._window.client.notice(self._window.name,message)
			t = Message(NOTICE_MESSAGE,self._window.client.nickname,message)
			self._window.writeText(t)
			return True
		return False

	def describe(self,message):
		if self._window.window_type==CHANNEL_WINDOW or self._window.window_type==PRIVATE_WINDOW:
			if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
			message = commands.fullInterpolate(self._gui,self._window,message)
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
		if config.ENABLE_EMOJI_SHORTCODES: message = emoji.emojize(message,language=config.EMOJI_LANGUAGE)
		message = commands.fullInterpolate(self._gui,self._window,message)
		t = Message(RAW_SYSTEM_MESSAGE,'',f"{message}")
		self._window.writeText(t,config.LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE)

	def alias(self,text):
		return commands.fullInterpolate(self._gui,self._window,text)

	def users(self):
		if self._window.window_type==CHANNEL_WINDOW: return self._window.users
		return None

	def topic(self):
		if self._window.window_type==CHANNEL_WINDOW: return self._window.channel_topic
		return None

class Plugin():

	_gui = None

	NAME = "Unknown"
	AUTHOR = "Unknown"
	VERSION = "1.0"
	SOURCE = "Unknown"

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
		return commands.find_file(filename,extension)

	def home(self):
		return f"{CONFIG_DIRECTORY}"

	def clients(self):
		if self._gui!=None:
			return self._gui.getAllClients()
		return []

	def master(self,client):
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

	def private(self,client,user):
		if self._gui!=None:
			w = self._gui.getSubWindow(channel,user)
			if w:
				c = w.widget()
				if c.window_type==PRIVATE_WINDOW:
					return Window(self._gui,c)
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
	'server', 'subwindow', 'close', 'me', 'error'
]

def init(obj):
	if not config.ENABLE_PLUGINS: return
	if not config.PLUGIN_INIT: return
	if hasattr(obj,"init"):
		obj.init()

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

	for obj in PLUGINS:
		if hasattr(obj,method):
			m = getattr(obj,method)

			if 'window' in arguments:
				if arguments['window']!=None:
					arguments["window"] = Window(gui,arguments["window"])

			m(**arguments)

def load_plugins(gui,force_reload=False):
	global PLUGINS

	PLUGIN_FILENAMES = []
	for o in PLUGINS:
		if os.path.exists(o._filename) or os.path.isfile(o._filename):
			PLUGIN_FILENAMES.append(f"{o._filename}")

	PLUGIN_NAMES = []
	for o in PLUGINS:
		if os.path.exists(o._filename) or os.path.isfile(o._filename):
			PLUGIN_NAMES.append(f"{o.NAME} {o.VERSION}")

	PLUGIN_INIT = []
	for o in PLUGINS:
		if hasattr(o,"init"):
			if os.path.exists(o._filename) or os.path.isfile(o._filename):
				s = inspect.getsourcelines(o.init)
				PLUGIN_INIT.append([o._filename,s])

	PLUGINS = []
	ERRORS = []

	if not config.ENABLE_PLUGINS: return

	with PikeManager([PLUGIN_DIRECTORY]) as mgr:
		classes = mgr.get_classes()

	for c in classes:
		# Ignore the base plugin class
		if c.__name__=="Plugin": continue

		# Create an instance of the plugin class
		obj = c()

		# Make sure that the class has access to
		# the "parent" window
		obj._gui = gui

		obj._filename = inspect.getfile(c)

		do_init = True
		for o in PLUGIN_FILENAMES:
			if o==f"{obj._filename}":
				do_init = False

		if hasattr(obj,"init"):
			s = inspect.getsourcelines(obj.init)
			for o in PLUGIN_INIT:
				if o[0]==obj._filename:
					if o[1]!=s:
						# The reloaded object's init() event
						# has changed, so let's re-execute the
						# event
						do_init = True

		obj._basename = os.path.basename(obj._filename)

		obj._events = 0
		obj._event_list = []
		for e in EVENTS:
			if hasattr(obj,e):
				obj._events = obj._events + 1
				obj._event_list.append(e)

		# Make sure the plugin inherits from the "Plugin" class
		if not issubclass(type(obj), Plugin):
			ERRORS.append(f"{obj._basename} doesn't inherit from \"Plugin\"")

		if not hasattr(obj,"NAME"): obj.NAME = "Unknown"
		if not hasattr(obj,"AUTHOR"): obj.AUTHOR = "Unknown"
		if not hasattr(obj,"SOURCE"): obj.SOURCE = "Unknown"
		if not hasattr(obj,"VERSION"): obj.VERSION = "1.0"

		obj._size = get_size(obj)

		if obj._events==0:
			ERRORS.append(f"{obj._basename} doesn't have any events to respond to")

		no_error = True
		for o in PLUGIN_NAMES:
			if o==f"{obj.NAME} {obj.VERSION}":
				no_error = False
				# The plugin may have been edited in the manager.
				# If the offending plugin has the same file name
				# as the loaded plugin, then we will assume the
				# plugin has been edited, not show an error, and
				# load it anyway.
				for p in PLUGIN_FILENAMES:
					if p==obj._filename:
						no_error = True
		if no_error==False:
			ERRORS.append(f"{obj._basename}'s NAME and VERSION conflicts with a loaded plugin")

		# Add the plugin to the registry if
		# the plugin had no errors
		if len(ERRORS)==0:
			PLUGINS.append(obj)

			# Run plugin init
			if do_init: init(obj)

	# Reload the plugin manager, if it's open
	if gui.plugin_manager!=None:
		gui.plugin_manager.refresh()

	# Return
	return ERRORS

def get_size(obj, seen=None):
	"""Recursively finds size of objects"""
	size = sys.getsizeof(obj)
	if seen is None:
		seen = set()
	obj_id = id(obj)
	if obj_id in seen:
		return 0
	# Important mark as seen *before* entering recursion to gracefully handle
	# self-referential objects
	seen.add(obj_id)
	if isinstance(obj, dict):
		size += sum([get_size(v, seen) for v in obj.values()])
		size += sum([get_size(k, seen) for k in obj.keys()])
	elif hasattr(obj, '__dict__'):
		size += get_size(obj.__dict__, seen)
	elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
		size += sum([get_size(i, seen) for i in obj])
	return size

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
