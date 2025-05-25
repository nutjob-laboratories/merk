
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

from . import config

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
			cmdsymbol+"focus",
			cmdsymbol+"maximize",
			cmdsymbol+"minimize",
			cmdsymbol+"restore",
			cmdsymbol+"cascade",
			cmdsymbol+"tile",
			cmdsymbol+"wait",
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
		]

		STYLES = {
			'comments': format(config.SYNTAX_COMMENT_COLOR,config.SYNTAX_COMMENT_STYLE),
			'merk': format(config.SYNTAX_COMMAND_COLOR,config.SYNTAX_COMMAND_STYLE),
			'channel': format(config.SYNTAX_CHANNEL_COLOR,config.SYNTAX_CHANNEL_STYLE),
			'alias': format(config.SYNTAX_ALIAS_COLOR,config.SYNTAX_ALIAS_STYLE),
		}

		# Comments
		self.script_comments = (QRegExp("(\\/\\*|\\*\\/|\n)"), 1, STYLES['comments'])

		rules = []

		# Commands
		rules += [(r'^\s*%s' % o, 0, STYLES['merk'])
			for o in merk]

		# Channel names
		rules += [
			(r'(#\w+)', 0, STYLES['channel']),
			(r'(\&\w+)', 0, STYLES['channel']),
			(r'(\!\w+)', 0, STYLES['channel']),
			(r'(\+\w+)', 0, STYLES['channel']),
			(r'(\$\w+)', 0, STYLES['alias']),
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
