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
import inspect
import uuid
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from pike.manager import PikeManager

from .resources import *
from . import config

CONFIG_DIRECTORY = None
PLUGIN_DIRECTORY = None
PLUGINS = []
LOADED = []
GUI = None

EVENTS = [
	"load",
	"unload",
	"line_in",
	"line_out",
	"public",
	"private",
	"action",
	"notice",
	"join",
	"part",
	"connect",
]

def is_plugin_disabled(entry):
	for e in config.DISABLED_PLUGINS:
		if e==entry.id():
			return True
	return False

def disable_plugin(entry):
	for e in config.DISABLED_PLUGINS:
		if e==entry.id(): return
	config.DISABLED_PLUGINS.append(entry.id())
	config.save_settings(config.CONFIG_FILE)

def enable_plugin(entry):
	clean = []
	for e in config.DISABLED_PLUGINS:
		if e==entry.id(): continue
		clean.append(e)
	config.DISABLED_PLUGINS = clean
	config.save_settings(config.CONFIG_FILE)

def load():
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if p.id() in LOADED: continue
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,None)
		if hasattr(obj,"load"):
			obj.load()
			LOADED.append(p.id())
		cleanup_plugin(obj)

def unload():
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,None)
		if hasattr(obj,"unload"):
			obj.unload()
		cleanup_plugin(obj)

def line_in(client,data):
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"line_in"):
			obj.line_in(data)
		cleanup_plugin(obj)

def line_out(client,data):
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"line_out"):
			obj.line_out(data)
		cleanup_plugin(obj)

def public(client,channel,user,message):
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"public"):
			obj.public(channel,user,message)
		cleanup_plugin(obj)

def private(client,user,message):
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"private"):
			obj.private(user,message)
		cleanup_plugin(obj)

def action(client,channel,user,message):
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"action"):
			obj.action(channel,user,message)
		cleanup_plugin(obj)

def notice(client,channel,user,message):
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"notice"):
			obj.notice(channel,user,message)
		cleanup_plugin(obj)

def join(client,channel,user):
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"join"):
			obj.join(channel,user)
		cleanup_plugin(obj)

def part(client,channel,user):
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"part"):
			obj.part(channel,user)
		cleanup_plugin(obj)

def connect(client):
	if not config.PLUGINS_ENABLED: return
	for p in PLUGINS:
		if is_plugin_disabled(p): continue
		obj = p.obj
		inject_plugin(obj,p,client)
		if hasattr(obj,"connect"):
			obj.connect()
		cleanup_plugin(obj)

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

class Plugin():

	irc = None
	__class_icon = None
	__class_file = None
	__plugin_icon = None
	__plugin_directory = None

	def writeConsole(self,text):
		if GUI==None: return False
		if self.irc==None: return False

		w = GUI.getServerWindow(self.irc)
		if w:
			t = Message(PLUGIN_MESSAGE,'',text)
			w.writeText(t)
			return True
		return False

	def writeWindow(self,name,text):
		if GUI==None: return False
		if self.irc==None: return False

		w = GUI.getWindow(name,self.irc)
		if w:
			t = Message(PLUGIN_MESSAGE,'',text)
			w.writeText(t)
			return True
		return False

class PluginEntry():
	def __init__(self,pclass,pobj):
		self.pclass = pclass
		self.obj = pobj
		self.errors = []

		self.plugin_id = ''

		self.filename = inspect.getfile(pclass)
		self.directory = os.path.dirname(self.filename)
		self.basename = os.path.basename(self.filename)

		self.number_of_events = 0

		fname, extension = os.path.splitext(self.filename)

		module = inspect.getmodule(self.obj)
		if hasattr(module,"PACKAGE"):
			self.package = module.PACKAGE
		else:
			self.package = None

		icon_name = fname+".png"
		if os.path.isfile(icon_name):
			self.icon = icon_name
		else:
			self.icon = None

		self.events = 0
		self.event_list = []
		for e in EVENTS:
			if hasattr(self.obj,e):
				self.events = self.events + 1
				self.event_list.append(e)

		classicon = os.path.join(os.path.dirname(self.filename), self.pclass.__name__+".png")
		if os.path.isfile(classicon):
			self.class_icon = classicon
		else:
			self.class_icon = None

		if PLUGIN_DIRECTORY in self.filename:
			# This checks to see if the plugin is just a directory
			# in the user's HOME plugin directory
			self.relative_path = os.path.relpath(self.directory,PLUGIN_DIRECTORY)
			self.is_home_plugin = True
		else:
			self.relative_path = None
			self.is_home_plugin = False

		inject_plugin(self.obj,self,None)
		self.size = get_size(self.obj)
		cleanup_plugin(self.obj)

	def module_name(self):
		return self.pclass.__module__

	def class_name(self):
		return self.pclass.__name__

	def id(self):
		return self.pclass.__module__+"."+self.pclass.__name__

	def plugin_name(self):
		return self.obj.NAME

	def plugin_version(self):
		return self.obj.VERSION

	def plugin_description(self):
		if hasattr(self.obj,"DESCRIPTION"): return self.obj.DESCRIPTION
		return None

def inject_plugin(obj,p,client):
	obj.irc = client
	obj._Plugin__class_icon = p.class_icon
	obj._Plugin__class_file = p.filename
	obj._Plugin__plugin_icon = p.icon
	obj._Plugin__plugin_directory = p.directory

def cleanup_plugin(obj):
	obj.irc = None
	obj._Plugin__class_icon = None
	obj._Plugin__class_file = None
	obj._Plugin__plugin_icon = None
	obj._Plugin__plugin_directory = None

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

def load_plugins(additional_locations):
	global PLUGINS

	PLUGINS = []
	ERRORS = []
	DIRECTORIES = []

	DIRECTORIES.append(PLUGIN_DIRECTORY)
	if len(additional_locations)>0:
		for loc in additional_locations:
			DIRECTORIES.append(loc)

	# Remove duplicates from the list
	DIRECTORIES = list(dict.fromkeys(DIRECTORIES))

	with PikeManager(DIRECTORIES) as mgr:
		classes = mgr.get_classes()

	for c in classes:
		# Ignore the base plugin class
		if c.__name__=="Plugin": continue

		# Create an instance of the plugin class
		obj = c()

		# Create the plugin entry for the registry (and errors)
		entry = PluginEntry(c,obj)

		entry.plugin_id = str(uuid.uuid4())

		# Make sure the class has any required attributes
		had_error = False
		if not hasattr(obj,"NAME"):
			entry.errors.append("No name attribute")
			had_error = True
		else:
			n = obj.NAME.strip()
			if len(n)==0:
				entry.errors.append("Name entry is blank")
				had_error = True

		if not hasattr(obj,"VERSION"):
			entry.errors.append("No version attribute")
			had_error = True

		# Make sure the plugin inherits from the "Plugin" class
		if not issubclass(type(obj), Plugin):
			entry.errors.append("Plugin doesn't inherit from \"Plugin\"")
			had_error = True

		# Make sure that the plugin has at least *one* event method
		counter = 0
		for e in EVENTS:
			if hasattr(obj,e): counter = counter+1
		if counter==0:
			entry.errors.append("Plugin doesn't have any event methods")
			had_error = True

		entry.number_of_events = counter

		# If we had an error, don't add the plugin to the registry
		if had_error:
			ERRORS.append(entry)
			continue

		# Add the plugin to the registry
		PLUGINS.append(entry)

	# Return any errors
	return ERRORS