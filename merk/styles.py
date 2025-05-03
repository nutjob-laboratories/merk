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
import re
from collections import defaultdict
from pathlib import Path

from .resources import *

CONFIG_DIRECTORY = None
STYLE_DIRECTORY = None
STYLE_FILE = None

def loadStyleFile(filename):
	if os.path.isfile(filename):
		return read_style_file(filename)
	else:
		return None

def saveStyle(client,channel,style,is_server_window=False):

	if hasattr(client,"network"):
		starter = client.network
	else:
		starter = client.server+"-"+str(client.port)

	if is_server_window:
		fname = os.path.join(STYLE_DIRECTORY,client.server+"-"+str(client.port)+".style")
	else:
		fname = starter+"-"+channel+".style"
		fname = os.path.join(STYLE_DIRECTORY,fname)

	write_style_file(style,fname)

def saveDefault(style):
	write_style_file(style,STYLE_FILE)

def loadDefault():
	return read_style_file(STYLE_FILE)

def loadStyleServer(client):
	fname = os.path.join(STYLE_DIRECTORY,client.server+"-"+str(client.port)+".style")

	if os.path.isfile(fname):
		return read_style_file(fname)
	else:
		return read_style_file(STYLE_FILE)

def loadPalette(name):
	fname = os.path.join(STYLE_DIRECTORY,name+".palette")

	if os.path.isfile(fname):
		return read_style_file(fname)

	return None

def loadStyle(client,channel):

	if hasattr(client,"network"):
		starter = client.network
	else:
		starter = client.server+"-"+str(client.port)

	fname = starter+"-"+channel+".style"
	fname = os.path.join(STYLE_DIRECTORY,fname)

	if os.path.isfile(fname):
		return read_style_file(fname)
	else:
		return read_style_file(STYLE_FILE)

def parseColor(style):
		text_color = "#000000"
		ps = style.split(";")
		for e in ps:
			px = e.split(':')
			if len(px)==2:
				if px[0].strip().lower()=='color':
					text_color = px[1].strip()

		return text_color

def parseBackgroundAndForegroundColor(style):
		background_color = "#FFFFFF"
		text_color = "#000000"
		ps = style.split(";")
		for e in ps:
			px = e.split(':')
			if len(px)==2:
				if px[0].strip().lower()=='background-color':
					background_color = px[1].strip()
				if px[0].strip().lower()=='color':
					text_color = px[1].strip()

		return background_color,text_color

def initialize(directory,directory_name):
	global CONFIG_DIRECTORY
	global STYLE_DIRECTORY
	global STYLE_FILE

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	# The config directory should already be created
	CONFIG_DIRECTORY = os.path.join(directory,directory_name)

	STYLE_DIRECTORY = os.path.join(CONFIG_DIRECTORY,"styles")
	if not os.path.isdir(STYLE_DIRECTORY): os.mkdir(STYLE_DIRECTORY)

	STYLE_FILE = os.path.join(STYLE_DIRECTORY, "default.style")

	# Check to see if the default file exists
	if not os.path.isfile(STYLE_FILE):
		# The file doesn't exist, so create it
		style = read_style_file('',DEFAULT_STYLE)
		write_style_file(style,STYLE_FILE)

	# Check to see if the dark palette exists, and
	# if not, create it
	DARK_MODE_PALETTE_FILE = os.path.join(STYLE_DIRECTORY, "dark.palette")

	if not os.path.isfile(DARK_MODE_PALETTE_FILE):
		# The file doesn't exist, so create it
		style = read_style_file('',DARK_PALETTE)
		write_palette_file(style,DARK_MODE_PALETTE_FILE)

def read_style_file(filename,raw=None):

	if raw!=None:
		text = raw
	else:
		# Read in the file
		f=open(filename, "r",encoding="utf-8",errors="ignore")
		text = f.read()
		f.close()

	# Strip comments
	text = re.sub(re.compile("/\\*.*?\\*/",re.DOTALL ) ,"" ,text)

	# Tokenize the file
	buff = ''
	name = ''
	tokens = []
	inblock = False
	for char in text:
		if char=='{':
			if inblock:
				raise SyntaxError("Nested styles are forbidden")
			inblock = True
			name = buff.strip()
			buff = ''
			continue

		if char=='}':
			inblock = False
			section = [ name,buff.strip() ]
			tokens.append(section)
			buff = ''
			continue

		buff = buff + char

	# Check for an unclosed brace
	if inblock:
		raise SyntaxError("Unclosed brace")

	# Build output dict of lists
	style = defaultdict(list)
	for section in tokens:
		name = section[0]
		entry = []
		for l in section[1].split(";"):
			l = l.strip()
			if len(l)>0:
				entry.append(l)

		if name in style:
			raise SyntaxError("Styles can only be defined once")
		else:
			if len(entry)!=0:
				comp = "; ".join(entry) + ";"
				style[name] = comp
			else:
				style[name] = ''

	# Return the dict
	return style

def write_style_file(style,filename):
	output = f'''/*

\t┳┳┓┏┓┳┓┓┏┓  ┳┳┓┏┓  ┏┓┏┳┓┓┏┓ ┏┓  ┏┓┳┓ ┏┓
\t┃┃┃┣ ┣┫┃┫   ┃┣┫┃   ┗┓ ┃ ┗┫┃ ┣   ┣ ┃┃ ┣ 
\t┛ ┗┗┛┛┗┛┗┛  ┻┛┗┗┛  ┗┛ ┻ ┗┛┗┛┗┛  ┻ ┻┗┛┗┛                                                 
\thttps://github.com/nutjob-laboratories/merk

\tText Style Configuration File
\t{filename}

\tGenerated by {APPLICATION_NAME} {APPLICATION_VERSION}

\tThis file is generated and maintained by the {APPLICATION_NAME} IRC Client

\t╔═════════════════════════════╗
\t║ Please don't edit manually! ║
\t╚═════════════════════════════╝

*/\n\n'''

	for key in style:
		output = output + key + " {\n"
		for s in style[key].split(';'):
			s = s.strip()
			if len(s)==0: continue
			output = output + "\t" + s + ";\n"
		output = output + "}\n\n"

	f=open(filename, "w",encoding="utf-8",errors="ignore")
	f.write(output)
	f.close()

def write_palette_file(style,filename):
	output = f'''/*

\t┳┳┓┏┓┳┓┓┏┓  ┏┓┏┓┓ ┏┓┏┳┓┏┳┓┏┓  ┏┓┳┓ ┏┓
\t┃┃┃┣ ┣┫┃┫   ┃┃┣┫┃ ┣  ┃  ┃ ┣   ┣ ┃┃ ┣ 
\t┛ ┗┗┛┛┗┛┗┛  ┣┛┛┗┗┛┗┛ ┻  ┻ ┗┛  ┻ ┻┗┛┗┛
\thttps://github.com/nutjob-laboratories/merk

\tApplication Palette Configuration File
\t{filename}

\tGenerated by {APPLICATION_NAME} {APPLICATION_VERSION}

\tThis file is generated and maintained by the {APPLICATION_NAME} IRC Client

\t╔═════════════════════════════╗
\t║ Please don't edit manually! ║
\t╚═════════════════════════════╝

*/\n\n'''

	for key in style:
		output = output + key + " {\n"
		for s in style[key].split(';'):
			s = s.strip()
			if len(s)==0: continue
			output = output + "\t" + s + ";\n"
		output = output + "}\n\n"

	f=open(filename, "w",encoding="utf-8",errors="ignore")
	f.write(output)
	f.close()