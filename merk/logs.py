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

import sys
import os
import json
from pathlib import Path
from datetime import datetime,timezone

from .resources import *
from . import config

CONFIG_DIRECTORY = None
LOG_DIRECTORY = None

def initialize(directory,directory_name):
	global CONFIG_DIRECTORY
	global LOG_DIRECTORY

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	# The config directory should already be created
	CONFIG_DIRECTORY = os.path.join(directory,directory_name)

	LOG_DIRECTORY = os.path.join(CONFIG_DIRECTORY,"logs")
	if not os.path.isdir(LOG_DIRECTORY):
		os.mkdir(LOG_DIRECTORY)
	else:
		# Make sure all logs are all lower case
		for root, dirs, files in os.walk(LOG_DIRECTORY):
			for filename in files:
				# If any log file has any capital letters in the
				# filename, rename the file so that the file no
				# longer has capital letters in the filename.
				# This is for backwards compatability.
				if any(c.isupper() for c in filename):
					old_file = os.path.join(root, filename)
					new_file = os.path.join(root, filename.lower())
					try:
						os.rename(old_file, new_file)
					except FileExistsError:
						pass
					except PermissionError:
						pass
					except Exception as e:
						pass

# Functions

# Encodes a filename to use to save a log backup
def backup_filename(logfile):
	if config.SHOW_TIMESTAMPS_IN_UTC:
		ts = datetime.fromtimestamp(datetime.timestamp(datetime.now()),tz=timezone.utc).strftime('_%d_%m_%Y')
	else:
		ts = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime('_%d_%m_%Y')

	backup_name, _ = os.path.splitext(os.path.basename(logfile))
	backup_name = backup_name + ts + ".txt"
	return backup_name

# Saves a backup of a single log file
def backup_log_direct(logfile,outfile):
	if os.path.isfile(logfile):
		with open(logfile, "r",encoding="utf-8",errors="ignore") as logentries:
			data = json.load(logentries)
		data = array_to_log(data)
		store_log = trimLog(data,config.MAXIMUM_LOADED_LOG_SIZE)
		store_log = log_to_array(store_log)

		dump = dumpLogHuman(logfile,False,False)
		code = open(outfile,mode="w",encoding="utf-8")
		code.write(dump)

		with open(logfile, "w",encoding="utf-8",errors="ignore") as writelog:
			json.dump(store_log, writelog, indent=4, sort_keys=True)

# Backups a list of log files, and saves the results to a directory
def backup_log(logfile,directory):
	if os.path.isfile(logfile):
		with open(logfile, "r",encoding="utf-8",errors="ignore") as logentries:
			data = json.load(logentries)
		data = array_to_log(data)
		store_log = trimLog(data,config.MAXIMUM_LOADED_LOG_SIZE)
		store_log = log_to_array(store_log)

		backup_name = backup_filename(logfile)
		dump = dumpLogHuman(logfile,False,False)
		code = open(os.path.join(directory,backup_name),mode="w",encoding="utf-8")
		code.write(dump)

		with open(logfile, "w",encoding="utf-8",errors="ignore") as writelog:
			json.dump(store_log, writelog, indent=4, sort_keys=True)

# Searches for large log files, and returns a list of them
def find_large_logs():
	log_list = []
	for root, dirs, files in os.walk(LOG_DIRECTORY):
		for file in files:
			file_path = os.path.join(root, file)
			if os.path.getsize(file_path) >= config.LOG_WARNING_SIZE * 1024 * 1024:
				p = file_path.split(LOG_AND_STYLE_FILENAME_DELIMITER,1)
				if len(p)==2:
					log_list.append(file_path)
	return log_list

# Converts an array of Message() objects to an array of arrays
def log_to_array(log):
	out = []
	for l in log:
		entry = [ l.timestamp,l.type,l.sender,l.contents ]
		out.append(entry)
	return out

# Converts an array of arrays to an array of Message Objects
def array_to_log(log):
	out = []
	for l in log:
		m = Message(l[1],l[2],l[3],l[0])
		out.append(m)
	return out

# Trims a log file down to a specific line count
def trimLog(ilog,maxsize):
	count = 0
	shortlog = []
	for line in reversed(ilog):
		count = count + 1
		shortlog.append(line)
		if count >= maxsize:
			break
	return list(reversed(shortlog))

# Encodes a log name to use for storage
def encodeLogName(network,name=None):
	network = network.replace(":","-")
	network = network.lower()

	network = escape_for_filename(network)

	if name==None:
		return f"{network}.json"
	else:
		name = escape_for_filename(name)
		return f"{network}{LOG_AND_STYLE_FILENAME_DELIMITER}{name}.json"

# Finds log files for a specific network
def find_network_logs(network):
	log_list = []
	for root, dirs, files in os.walk(LOG_DIRECTORY):
		for file in files:
			p = file.split(LOG_AND_STYLE_FILENAME_DELIMITER,1)
			file_path = os.path.join(root, file)
			if len(p)==2:
				if p[0].lower()==network.lower():
					log_list.append(file_path)
	return log_list

# Takes an array of Message() objects, converts it to
# an AoA, and appens the AoA to a file containing
# AoAs on disk
def saveLog(network,name,logs,logdir=LOG_DIRECTORY):
	f = encodeLogName(network,name)
	logfile = os.path.join(logdir,f)

	logs = log_to_array(logs)

	slog = loadLog(network,name,logdir)
	for e in logs:
		slog.append(e)

	with open(logfile, "w",encoding="utf-8",errors="ignore") as writelog:
		json.dump(slog, writelog, indent=4, sort_keys=True)

# Loads an AoA from disk and returns it
def loadLog(network,name,logdir=LOG_DIRECTORY):
	f = encodeLogName(network,name)
	logfile = os.path.join(logdir,f)

	if os.path.isfile(logfile):
		with open(logfile, "r",encoding="utf-8",errors="ignore") as logentries:
			data = json.load(logentries)
			return data
	else:
		return []

# Loads an AoA from disk, converts it to an arroy
# of Message() objects, and returns it
def readLog(network,name,logdir=LOG_DIRECTORY):
	logs = loadLog(network,name,logdir)
	logs = array_to_log(logs)
	return logs

# Formats a timestamp for a date
def pretty_timestamp_date(ts):
	if config.TIMESTAMP_24_HOUR:
		if config.SHOW_TIMESTAMPS_IN_UTC:
			return datetime.fromtimestamp(ts,tz=timezone.utc).strftime('%a, %d %b %Y '+config.TIMESTAMP_FORMAT+' UTC')
		else:
			return datetime.fromtimestamp(ts).strftime('%a, %d %b %Y '+config.TIMESTAMP_FORMAT)
	else:
		if config.SHOW_TIMESTAMPS_IN_UTC:
			return datetime.fromtimestamp(ts,tz=timezone.utc).strftime('%a, %d %b %Y '+config.TIMESTAMP_FORMAT+' %p UTC')
		else:
			return datetime.fromtimestamp(ts).strftime('%a, %d %b %Y '+config.TIMESTAMP_FORMAT+' %p')

# Formats a timestamp for a time
def pretty_timestamp_time(ts):
	if config.TIMESTAMP_24_HOUR:
		if config.SHOW_TIMESTAMPS_IN_UTC:
			return datetime.fromtimestamp(ts,tz=timezone.utc).strftime(config.TIMESTAMP_FORMAT+' UTC')
		else:
			return datetime.fromtimestamp(ts).strftime(config.TIMESTAMP_FORMAT)
	else:
		if config.SHOW_TIMESTAMPS_IN_UTC:
			return datetime.fromtimestamp(ts,tz=timezone.utc).strftime(config.TIMESTAMP_FORMAT+' %p UTC')
		else:
			return datetime.fromtimestamp(ts).strftime(config.TIMESTAMP_FORMAT+' %p')

# Loads an AoA from disk, converts it to a string
def dumpLog(filename,delimiter,linedelim="\n",epoch=True):
	if os.path.isfile(filename):
		with open(filename, "r",encoding="utf-8",errors="ignore") as logentries:
			logs = json.load(logentries)
	if logs:
		out = []
		for l in logs:
			if l[2]!=None:
				l[2] = l[2].strip()
			else:
				l[2] = ''
			if l[3]!=None:
				l[3] = l[3].strip()
			else:
				l[3] = ''
			if l[2]=='': l[2] = '***'
			if l[2].startswith('&rarr;'): l[2] = l[2].replace('&rarr;','-> ',1)

			if not epoch:
				pretty_timestamp = pretty_timestamp_date(l[0])
				entry = pretty_timestamp+delimiter+l[2]+delimiter+l[3]
			else:
				entry = str(l[0])+delimiter+l[2]+delimiter+l[3]
			if l[3]!="": out.append(entry)
		return linedelim.join(out)
	else:
		return ''

# Handles both rendering a log for the log viewer, and
# exporting a log to the "human readable" format
def dumpLogHuman(filename,render_for_viewer=False,epoch=False):
	if os.path.isfile(filename):
		with open(filename, "r",encoding="utf-8",errors="ignore") as logentries:
			logs = json.load(logentries)

	# If the setting is turned on, make sure that the log
	# is "trimmed" for the log viewer
	if config.LIMIT_LOG_VIEW:
		if len(logs)>config.MAX_LOG_DISPLAY_SIZE and render_for_viewer==True:
			logs = logs[-config.MAX_LOG_DISPLAY_SIZE:]
			trimmed = True
		else:
			trimmed = False
	else:
		trimmed = False

	# Render the log
	if logs:
		out = []
		cdate = None
		for l in logs:
			if l[2]!=None:
				l[2] = l[2].strip()
			else:
				l[2] = ''
			if l[3]!=None:
				l[3] = l[3].strip()
			else:
				l[3] = ''
			if l[2]=='': l[2] = '***'

			u = l[2].split('!')
			if len(u)==2:
				u = u[0]
			else:
				u = l[2]

			# Just to make the code a bit more readable
			username = u
			message_type = l[1]
			message = l[3]
			timestamp = l[0]

			# If we're not rendering the log for the log
			# viewer, we display the entire nickname and
			# hostmask
			if render_for_viewer==False: username = l[2]

			# Outgoing private messages are stored as
			# "self" messages, with a HTML entity prefixed
			# to the targeted user to show it's an outgoing
			# private message; here, we replace the outgoing
			# prefix HTML entity with an appropriate text
			# representation
			if message_type==SELF_MESSAGE:
				if username.startswith('&rarr;'):
					username = username.replace('&rarr;','-> ',1)

			# Since the background of the log viewer is white,
			# we need to make sure that white colored text is
			# still visible; if we're rendering the log for the
			# viewer, we'll replace white colored text with
			# grey colored text
			if render_for_viewer:
				message = message.replace("\x0300","\x0314")

			# If the log has been trimmed, it's being rendered
			# for the log viewer, so notify the user that the
			# log has been trimmed
			if trimmed==True:
				out.append(f"\x02\x1d\x0304Viewing only the last {len(logs)} lines of the log\x0f")
				trimmed = False

			# Now, we handle showing different dates.
			# This will only show up when the date changes,
			# so chat will be displayed/exported with notation
			# showing what chat happened on what dates
			if config.SHOW_TIMESTAMPS_IN_UTC:
				ndate = datetime.fromtimestamp(timestamp,tz=timezone.utc).strftime('%A %B %d, %Y UTC')
			else:
				ndate = datetime.fromtimestamp(timestamp).strftime('%A %B %d, %Y')
			if cdate!=ndate:
				cdate=ndate
				if render_for_viewer:
					out.append(f"\x02\x1F{cdate}\x0f")
				else:
					if epoch:
						out.append(f"*** {timestamp}")
					else:
						out.append(f"*** {cdate}")

			# Render chat messages according to message type
			if message_type==CHAT_MESSAGE:
				# Regular chat
				if render_for_viewer:
					pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"\x02[{pretty_timestamp}]\x0f \x02\x0302{username}\x0f: {message}"
				else:
					if epoch:
						pretty_timestamp = timestamp
					else:
						pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"{pretty_timestamp}\t{username}: {strip_color(message)}"
			elif message_type==PRIVATE_MESSAGE:
				# Private message
				if render_for_viewer:
					pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"\x02[{pretty_timestamp}]\x0f \x02\x1d\x0302{username}\x0f: {message}"
				else:
					if epoch:
						pretty_timestamp = timestamp
					else:
						pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"{pretty_timestamp}\t{username}: {strip_color(message)}"
			elif message_type==SELF_MESSAGE:
				# Regular chat
				if render_for_viewer:
					pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"\x02[{pretty_timestamp}]\x0f \x1F\x02\x0302{username}\x0f: {message}"
				else:
					if epoch:
						pretty_timestamp = timestamp
					else:
						pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"{pretty_timestamp}\t{username}: {strip_color(message)}"
			elif message_type==ACTION_MESSAGE:
				# CTCP Action message
				if render_for_viewer:
					pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"\x02[{pretty_timestamp}]\x0f \x02\x1d\x0302{username} {message}\x0f"
				else:
					if epoch:
						pretty_timestamp = timestamp
					else:
						pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"{pretty_timestamp}\t{username} {strip_color(message)}"
			elif message_type==NOTICE_MESSAGE:
				# Notice message
				if render_for_viewer:
					pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"\x02[{pretty_timestamp}]\x0f \x02\x0302*{username}\x0f*: {message}"
				else:
					if epoch:
						pretty_timestamp = timestamp
					else:
						pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"{pretty_timestamp}\t*{username}*\t{strip_color(message)}"
			else:
				# Everything else; this is usually logged system messages
				if render_for_viewer:
					pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"\x02[{pretty_timestamp}]\x0f \x02\x0304{message}\x0f"
				else:
					if epoch:
						pretty_timestamp = timestamp
					else:
						pretty_timestamp = pretty_timestamp_time(timestamp)
					entry = f"{pretty_timestamp}\t{strip_color(message)}"

			# If the message is not blank, add it to the
			# log render/export
			if message!="": out.append(entry)

		return "\n".join(out)
	else:
		return ''

# Loads an AoA from disk, converts it to a JSON string
def dumpLogJson(filename,epoch=True):
	if os.path.isfile(filename):
		with open(filename, "r",encoding="utf-8",errors="ignore") as logentries:
			logs = json.load(logentries)
	if logs:
		out = []
		for l in logs:
			if l[2]!=None:
				l[2] = l[2].strip()
			else:
				l[2] = ''
			if l[3]!=None:
				l[3] = l[3].strip()
			else:
				l[3] = ''
			if l[2]=='': l[2] = '*'
			if l[2].startswith('&rarr;'): l[2] = l[2].replace('&rarr;','-> ',1)
			if not epoch:
				l[0] = pretty_timestamp_date(l[0])
			entry = [ l[0],l[2],l[3] ]
			if l[3]!="": out.append(entry)
		return json.dumps(out, indent=4, sort_keys=True)
	else:
		return ''