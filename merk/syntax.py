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

SSL_AVAILABLE = True
try:
	from twisted.internet import ssl
except ImportError as error:
	SSL_AVAILABLE = False
except Exception as exception:
	pass

from . import config
# from . import resources

def format(color, style=''):
	"""Return a QTextCharFormat with the given attributes.
	"""
	_color = QColor()
	_color.setNamedColor(color)

	_format = QTextCharFormat()
	_format.setForeground(_color)
	if 'bold' in style:
		_format.setFontWeight(QFont.Bold)
	if 'italic' in style:
		_format.setFontItalic(True)
	if 'bi' in style:
		_format.setFontWeight(QFont.Bold)
		_format.setFontItalic(True)

	return _format

class MerkScriptHighlighter (QSyntaxHighlighter):

	def __init__(self, document):
		QSyntaxHighlighter.__init__(self, document)

		# Make sure to escape any special characters in the
		# command symbol; this also allows for command
		# symbols that are more than one character
		special = ['\\','^','$','.','|','?','*','+','(',')','{']
		cmdsymbol = ''
		for c in config.ISSUE_COMMAND_SYMBOL:
			if c in special:
				c = '\\'+c
			cmdsymbol = cmdsymbol + c

		aliassymbol = ''
		for c in config.ALIAS_INTERPOLATION_SYMBOL:
			if c in special:
				c = '\\'+c
			aliassymbol = aliassymbol + c


		merk = [
			cmdsymbol+"part",
			cmdsymbol+"join",
			cmdsymbol+"notice",
			cmdsymbol+"nick",
			cmdsymbol+"help",
			cmdsymbol+"topic",
			cmdsymbol+"quit",
			cmdsymbol+"msg",
			cmdsymbol+"me",
			cmdsymbol+"mode",
			cmdsymbol+"kick",
			cmdsymbol+"whois",
			cmdsymbol+"whowas",
			cmdsymbol+"who",
			cmdsymbol+"invite",
			cmdsymbol+"script",
			cmdsymbol+"maximize",
			cmdsymbol+"minimize",
			cmdsymbol+"restore",
			cmdsymbol+"cascade",
			cmdsymbol+"tile",
			cmdsymbol+"away",
			cmdsymbol+"back",
			cmdsymbol+"raw",
			cmdsymbol+"oper",
			cmdsymbol+"time",
			cmdsymbol+"print",
			cmdsymbol+"version",
			cmdsymbol+"connect",
			cmdsymbol+"connectssl",
			cmdsymbol+"alias",
			cmdsymbol+"play",
			cmdsymbol+"list",
			cmdsymbol+"refresh",
			cmdsymbol+"knock",
			cmdsymbol+"exit",
			cmdsymbol+"config",
			cmdsymbol+"xconnect",
			cmdsymbol+"xconnectssl",
			cmdsymbol+"unalias",
			cmdsymbol+"ignore",
			cmdsymbol+"unignore",
			cmdsymbol+"find",
			cmdsymbol+"ping",
			cmdsymbol+"shell",
			cmdsymbol+"ctcp",
			cmdsymbol+"private",
			cmdsymbol+"msgbox",
			cmdsymbol+"reclaim",
			cmdsymbol+"next",
			cmdsymbol+"previous",
			cmdsymbol+"delay",
			cmdsymbol+"clear",
			cmdsymbol+"hide",
			cmdsymbol+"show",
			cmdsymbol+"window",
			cmdsymbol+"close",
			cmdsymbol+"random",
			cmdsymbol+"prints",
			cmdsymbol+"quitall",
			cmdsymbol+"rem",
			cmdsymbol+"fullscreen",
			cmdsymbol+"resize",
			cmdsymbol+"move",
			cmdsymbol+"focus",
			cmdsymbol+"reconnect",
			cmdsymbol+"reconnectssl",
			cmdsymbol+"xreconnect",
			cmdsymbol+"xreconnectssl",
			cmdsymbol+"user",
			cmdsymbol+"window move",
			cmdsymbol+"window size",
			cmdsymbol+"window maximize",
			cmdsymbol+"window minimize",
			cmdsymbol+"window restore",
			cmdsymbol+"ctcp version",
			cmdsymbol+"ctcp userinfo",
			cmdsymbol+"ctcp finger",
			cmdsymbol+"ctcp source",
			cmdsymbol+"ctcp time",
			cmdsymbol+"ctcp VERSION",
			cmdsymbol+"ctcp USERINFO",
			cmdsymbol+"ctcp FINGER",
			cmdsymbol+"ctcp SOURCE",
			cmdsymbol+"ctcp TIME",
			cmdsymbol+"macro",
			cmdsymbol+"config import",
			cmdsymbol+"config export",
			cmdsymbol+"config restart",
			cmdsymbol+"window readme",
			cmdsymbol+"window settings",
			cmdsymbol+"window logs",
			cmdsymbol+"edit",
		]

		script_only = [
			"restrict",
			"insert",
			"usage",
			"context",
			"wait",
			"end",
			"only",
			"exclude",
			"if",
			"restrict server",
			"restrict server channel",
			"restrict server private",
			"restrict channel",
			"restrict channel server",
			"restrict channel private",
			"restrict private",
			"restrict private server",
			"restrict private channel",
			"halt",
		]

		script_full = [
			"goto",
		]

		operators = [
			"\\(is\\)",
			"\\(not\\)",
			"\\(in\\)",
			"\\(lt\\)",
			"\\(gt\\)",
			"\\(eq\\)",
			"\\(ne\\)",
		]

		if not config.ENABLE_ALIASES:
			merk.remove(cmdsymbol+"alias")
			merk.remove(cmdsymbol+"unalias")
			merk.remove(cmdsymbol+"shell")
			merk.remove(cmdsymbol+"random")
		if not config.ENABLE_SHELL_COMMAND:
			merk.remove(cmdsymbol+"shell")
		if not SSL_AVAILABLE:
			merk.remove(cmdsymbol+"connectssl")
			merk.remove(cmdsymbol+"xconnectssl")
			merk.remove(cmdsymbol+"reconnectssl")
			merk.remove(cmdsymbol+"xreconnectssl")
		if not config.ENABLE_DELAY_COMMAND:
			merk.remove(cmdsymbol+"delay")
		if not config.ENABLE_CONFIG_COMMAND:
			merk.remove(cmdsymbol+"config")
			merk.remove(cmdsymbol+"config import")
			merk.remove(cmdsymbol+"config export")
			merk.remove(cmdsymbol+"config restart")
		if not config.ENABLE_GOTO_COMMAND: script_full = []
		if not config.ENABLE_IF_COMMAND:
			script_only.remove("if")
			operators = []
		if not config.ENABLE_INSERT_COMMAND:
			script_only.remove("insert")
		if not config.ENABLE_USER_COMMAND:
			merk.remove(cmdsymbol+"user")

		STYLES = {
			'comments': format(config.SYNTAX_COMMENT_COLOR,config.SYNTAX_COMMENT_STYLE),
			'merk': format(config.SYNTAX_COMMAND_COLOR,config.SYNTAX_COMMAND_STYLE),
			'channel': format(config.SYNTAX_CHANNEL_COLOR,config.SYNTAX_CHANNEL_STYLE),
			'alias': format(config.SYNTAX_ALIAS_COLOR,config.SYNTAX_ALIAS_STYLE),
			'script': format(config.SYNTAX_SCRIPT_COLOR,config.SYNTAX_SCRIPT_STYLE),
			'operator': format(config.SYNTAX_OPERATOR_COLOR,config.SYNTAX_OPERATOR_STYLE),
		}

		if not config.ENABLE_ALIASES: 
			STYLES['alias'] = format(config.SYNTAX_FOREGROUND,'')

		# Comments
		self.script_comments = (QRegExp("(\\/\\*|\\*\\/|\n)"), 1, STYLES['comments'])

		rules = []

		# Commands
		rules += [(r'^\s*%s' % o, 0, STYLES['merk'])
			for o in merk]

		# Script Only Commands
		rules += [(r'^\s*%s' % o, 0, STYLES['script'])
			for o in script_only]

		# Script Full Commands
		rules += [(r'%s' % o, 0, STYLES['script'])
			for o in script_full]

		# Script Operators
		rules += [(r'%s' % o, 0, STYLES['operator'])
			for o in operators]

		# Channel names and aliases
		rules += [
			(r'(#+[^#\s]+)', 0, STYLES['channel']),
			(r'(\&+[^\&\s]+)', 0, STYLES['channel']),
			(r'(\!+[^\!\s]+)', 0, STYLES['channel']),
			(r'(\++[^\+\s]+)', 0, STYLES['channel']),
			(r'(%s\w+)' % aliassymbol, 0, STYLES['alias']),
		]

		# Build a QRegExp for each pattern
		self.rules = [(QRegExp(pat), index, fmt)
			for (pat, index, fmt) in rules]

	def highlightBlock(self, text):

		"""Apply syntax highlighting to the given block of text.
		"""
		# Do other syntax formatting
		for expression, nth, format in self.rules:
			index = expression.indexIn(text, 0)

			while index >= 0:
				index = expression.pos(nth)
				length = len(expression.cap(nth))
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)

		self.setCurrentBlockState(0)

		# Do multi-line comments
		in_multiline = self.match_multiline(text, *self.script_comments)

	def match_multiline(self, text, delimiter, in_state, style):
		if self.previousBlockState() == in_state:
			start = 0
			add = 0
		else:
			start = delimiter.indexIn(text)
			add = delimiter.matchedLength()

		while start >= 0:
			end = delimiter.indexIn(text, start + add)
			if end >= add:
				length = end - start + add + delimiter.matchedLength()
				self.setCurrentBlockState(0)
			else:
				self.setCurrentBlockState(in_state)
				length = len(text) - start + add
			self.setFormat(start, length, style)
			start = delimiter.indexIn(text, start + length)

		if self.currentBlockState() == in_state:
			return True
		else:
			return False
