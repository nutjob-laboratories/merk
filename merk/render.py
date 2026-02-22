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

from itertools import combinations
import re
import html

from .resources import *
from . import config
from . import styles

TIMESTAMP_TEMPLATE = """<td style="vertical-align:top; font-size:small; text-align:left;"><div style="!TIMESTAMP_STYLE!">[!TIME!]</div></td><td style="font-size:small;">&nbsp;</td>"""

MESSAGE_TEMPLATE = f"""
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		<td style="text-align: right; vertical-align: top;"><div style="!ID_STYLE!">!ID!</div></td>
		<td style="text-align: left; vertical-align: top;">&nbsp;</td>
		!INSERT_MESSAGE_TEMPLATE!
	</tr>
	</tbody>
</table>
"""

SYSTEM_TEMPLATE = f"""
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		!INSERT_MESSAGE_TEMPLATE!
	</tr>
	</tbody>
</table>
"""

MESSAGE_STYLE_TEMPLATE = """<td style="text-align: left; vertical-align: top;"><div style="!MESSAGE_STYLE!">!MESSAGE!</div></td>"""
MESSAGE_NO_STYLE_TEMPLATE = """<td style="text-align: left; vertical-align: top;">!MESSAGE!</td>"""

HORIZONTAL_RULE = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({HORIZONTAL_DOTTED_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

HARD_HORIZONTAL_RULE = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

LIGHT_HORIZONTAL_RULE = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({LIGHT_HORIZONTAL_DOTTED_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

HARD_LIGHT_HORIZONTAL_RULE = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({LIGHT_HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

TEXT_HORIZONTAL_RULE_TEMPLATE = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({HORIZONTAL_DOTTED_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
			<td><small><center>!MESSAGE!</center></small></td>
			<td style="background-image: url({HORIZONTAL_DOTTED_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

LIGHT_TEXT_HORIZONTAL_RULE_TEMPLATE = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({LIGHT_HORIZONTAL_DOTTED_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
			<td><small><center>!MESSAGE!</center></small></td>
			<td style="background-image: url({LIGHT_HORIZONTAL_DOTTED_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

DATE_MESSAGE_TEMPLATE = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
			<td><center><small><b>!MESSAGE!</b></small></center></td>
			<td style="background-image: url({HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

LIGHT_DATE_MESSAGE_TEMPLATE = f'''
<table width="100%" border="0">
	<tbody>
		<tr>
			<td style="background-image: url({LIGHT_HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
			<td><center><small><b>!MESSAGE!</b></small></center></td>
			<td style="background-image: url({LIGHT_HORIZONTAL_RULE_BACKGROUND}); background-repeat: repeat-x;">&nbsp;
			</td>
		</tr>
	</tbody>
</table>'''

def render_message(message,style,client=None,no_padding=False):

	if config.DO_NOT_APPLY_STYLES_TO_TEXT: background,foreground = styles.parseBackgroundAndForegroundColor(style["all"])
	is_background_light = test_if_background_is_light(style["all"])
	
	# Set message contents
	msg_to_display = message.contents

	# Set nickname
	p = message.sender.split('!')
	if len(p)==2:
		nick = p[0]
	else:
		nick = message.sender

	# Escape all HTML
	if message.type!=SYSTEM_MESSAGE and message.type!=ERROR_MESSAGE and message.type!=SERVER_MESSAGE and message.type!=RAW_SYSTEM_MESSAGE and message.type!=WHOIS_MESSAGE:
		msg_to_display = html.escape(msg_to_display)

	# Escape HTML if it's turned on for /print
	if config.ESCAPE_HTML_FROM_RAW_SYSTEM_MESSAGE:
		if message.type==RAW_SYSTEM_MESSAGE or message.type==SYSTEM_MESSAGE:
			msg_to_display = html.escape(msg_to_display)

	# Convert URLs to links
	if config.CONVERT_URLS_TO_LINKS:
		if has_url(msg_to_display):
			msg_to_display = inject_www_links(msg_to_display,style)

	# Insert or remove IRC colors
	if config.DISPLAY_IRC_COLORS:
		if message.type!=WHOIS_MESSAGE:
			if string_has_irc_formatting_codes(msg_to_display):
				optional = "all"
				if message.type==SYSTEM_MESSAGE: optional = "system"
				if message.type==ERROR_MESSAGE: optional = "error"
				if message.type==ACTION_MESSAGE: optional = "action"
				if message.type==SERVER_MESSAGE: optional = "server"
				msg_to_display = convert_irc_color_to_html(msg_to_display,style,optional)
		else:
			msg_to_display = strip_color(msg_to_display)
	else:
		if string_has_irc_formatting_codes(msg_to_display):
			msg_to_display = strip_color(msg_to_display)

	# Elide nicknames if we need to
	if config.ELIDE_LONG_NICKNAMES_IN_CHAT_DISPLAY:
		if len(nick)>config.NICKNAME_PAD_LENGTH:
			nick = elide_text(nick,config.NICKNAME_PAD_LENGTH)

	# Add system message prefix if necessary
	if message.type==SYSTEM_MESSAGE or message.type==ERROR_MESSAGE:
		if config.SYSTEM_MESSAGE_PREFIX!='':
			msg_to_display = config.SYSTEM_MESSAGE_PREFIX + " " + msg_to_display

	# Force monospace rendering if need be
	if config.FORCE_MONOSPACE_RENDERING:
		msg_to_display = "<tt>"+msg_to_display+"</tt>"

	if config.HIGHLIGHT_NICK_IN_CHAT:
		if message.type==CHAT_MESSAGE or message.type==PRIVATE_MESSAGE:
			if client!=None:
				msg_to_display = highlight_nick(msg_to_display,client.nickname,style)

	# Assign template and style to the message
	message_templates = {
		SYSTEM_MESSAGE: SYSTEM_TEMPLATE,
		ERROR_MESSAGE: SYSTEM_TEMPLATE,
		ACTION_MESSAGE: SYSTEM_TEMPLATE,
		SERVER_MESSAGE: SYSTEM_TEMPLATE,
		RAW_SYSTEM_MESSAGE: SYSTEM_TEMPLATE,
		NOTICE_MESSAGE: SYSTEM_TEMPLATE if len(nick) == 0 else MESSAGE_TEMPLATE,
	}
	message_styles = {
		SYSTEM_MESSAGE: "system",
		ERROR_MESSAGE: "error",
		ACTION_MESSAGE: "action",
		CHAT_MESSAGE: "message",
		SELF_MESSAGE: "message",
		NOTICE_MESSAGE: "notice" if len(nick) == 0 else "message",
		SERVER_MESSAGE: "server",
		PRIVATE_MESSAGE: "message",
		RAW_SYSTEM_MESSAGE: "raw",
		WHOIS_MESSAGE: "server",
	}
	horizontal_rule_messages = {
		HORIZONTAL_RULE_MESSAGE: (HORIZONTAL_RULE if is_background_light else LIGHT_HORIZONTAL_RULE),
		HARD_HORIZONTAL_RULE_MESSAGE: (HARD_HORIZONTAL_RULE if is_background_light else HARD_LIGHT_HORIZONTAL_RULE),
		TEXT_HORIZONTAL_RULE_MESSAGE: (TEXT_HORIZONTAL_RULE_TEMPLATE if is_background_light else LIGHT_TEXT_HORIZONTAL_RULE_TEMPLATE),
		DATE_MESSAGE: (DATE_MESSAGE_TEMPLATE if is_background_light else LIGHT_DATE_MESSAGE_TEMPLATE),
	}
	if not config.DO_NOT_APPLY_STYLES_TO_TEXT:
		output = message_templates.get(message.type, MESSAGE_TEMPLATE)
		style_key = message_styles.get(message.type, "message")
		output_style = style[style_key]
	else:
		output = message_templates.get(message.type, MESSAGE_TEMPLATE)
		output_style = f"color:{foreground};"
	if message.type in horizontal_rule_messages:
		output = horizontal_rule_messages[message.type]
		style = style["message"]

	# Insert message info into the appropriate
	# template, and make sure styles are applied

	replacements = {}
	if style == "":
		replacements["!INSERT_MESSAGE_TEMPLATE!"] = MESSAGE_NO_STYLE_TEMPLATE
	else:
		replacements["!INSERT_MESSAGE_TEMPLATE!"] = MESSAGE_STYLE_TEMPLATE
		replacements["!MESSAGE_STYLE!"] = output_style

	# Handle timestamps
	if (message.type != HORIZONTAL_RULE_MESSAGE and
		message.type != HARD_HORIZONTAL_RULE_MESSAGE and
		message.type != TEXT_HORIZONTAL_RULE_MESSAGE and
		message.type != DATE_MESSAGE):
		if config.DISPLAY_TIMESTAMP:
			pretty_timestamp = datetime.fromtimestamp(message.timestamp).strftime(config.TIMESTAMP_FORMAT)
			ts = TIMESTAMP_TEMPLATE.replace("!TIMESTAMP_STYLE!", style["timestamp"]).replace("!TIME!", pretty_timestamp)
			replacements["!TIMESTAMP!"] = ts
		else:
			replacements["!TIMESTAMP!"] = ''

	# Apply all insertions to the template
	for key, value in replacements.items():
		output = output.replace(key, value)

	# Assign style to the nick, and modify it
	# if we need to
	if not config.DO_NOT_APPLY_STYLES_TO_TEXT:
		if message.type==SELF_MESSAGE:
			user_style = style["self"]
		elif message.type==CHAT_MESSAGE:
			user_style = style["username"]
		elif message.type==NOTICE_MESSAGE:
			user_style = style["notice"]
		elif message.type==PRIVATE_MESSAGE:
			user_style = style["private"]
		elif message.type==WHOIS_MESSAGE:
			user_style = style["username"]
		else:
			user_style = ''
		if message.type!=ACTION_MESSAGE:
			if not no_padding:
				if message.type!=NOTICE_MESSAGE and len(nick)>0:
					idl = config.NICKNAME_PAD_LENGTH - len(nick)
					if idl>0:
						nick = ('&nbsp;'*idl)+nick
	else:
		user_style = f"color:{foreground};"

	# Insert nicks into the template
	replacements = {
		"!ID_STYLE!": user_style,
		"!ID!": nick,
	}
	if message.type == ACTION_MESSAGE:
		replacements["!MESSAGE!"] = nick + " " + msg_to_display
	else:
		replacements["!MESSAGE!"] = msg_to_display
	for key, value in replacements.items():
		output = output.replace(key, value)

	# Message has been rendered, so return it
	return output

def highlight_nick(text, target_word, style):

	if config.DO_NOT_APPLY_STYLES_TO_TEXT:
		background, foreground = styles.parseBackgroundAndForegroundColor(style["all"])
		style_str = f"color:{foreground};"
	else:
		style_str = style["self"]
	
	pattern = rf'\b{re.escape(target_word)}\b'
	
	def replacer(match):
		original_word = match.group(0)
		return f'<span style="{style_str}">{original_word}</span>'

	result = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
	return result

def inject_www_links(txt, style):
	if config.DO_NOT_APPLY_STYLES_TO_TEXT:
		background, foreground = styles.parseBackgroundAndForegroundColor(style["all"])
		style_str = f"color:{foreground};"
	else:
		style_str = style["hyperlink"]

	url_pattern = re.compile(
		r"((?:https?://|www\.)"
		r"(?:[^\s<>'\"&]|&(?!gt;|quot;))+" 
		r"(?=[/]?\s|[/]?>|&gt;|&quot;|[\"']|$))", 
		re.IGNORECASE
	)

	def replace_url(match):
		full_match = match.group(0)
		u_visible = full_match.rstrip('.,;:!?')
		if u_visible.endswith(')') and u_visible.count('(') < u_visible.count(')'):
			u_visible = u_visible[:-1]
		trailing_punctuation = full_match[len(u_visible):]
		if u_visible.endswith('/') and match.end() < len(txt) and txt[match.end()] == '>':
			trailing_punctuation = '/' + trailing_punctuation
			u_visible = u_visible[:-1]
		href = u_visible
		if not href.lower().startswith(('http://', 'https://')):
			href = 'http://' + href
		return f'<a href="{href}" style="{style_str}">{u_visible}</a>{trailing_punctuation}'

	return re.sub(url_pattern, replace_url, txt)

def convert_irc_color_to_html(text, style, optional="all"):
	background, foreground = styles.parseBackgroundAndForegroundColor(style[optional])
	pattern = re.compile(r'(\x02|\x03(?:\d{1,2}(?:,\d{1,2})?)?|\x0F|\x1D|\x1F|\x1E)')
	
	state = {'bold': False, 'italic': False, 'underline': False, 'strikethrough': False, 'fg': None, 'bg': None}
	parts = pattern.split(text)
	result = []

	def get_style(s):
		styles = []
		if s['bold']: styles.append("font-weight: bold;")
		if s['italic']: styles.append("font-style: italic;")
		if s['underline']: styles.append("text-decoration: underline;")
		if s['strikethrough']: styles.append("text-decoration: line-through;")
		
		fg_color = IRC_COLORS.get(s['fg'].zfill(2)) if s['fg'] else foreground
		bg_color = IRC_COLORS.get(s['bg'].zfill(2)) if s['bg'] else background
		
		if fg_color:
			styles.append(f"color: {fg_color};")
		if bg_color:
			styles.append(f"background-color: {bg_color};")
		return " ".join(styles)

	for part in parts:
		if not part:
			continue
		
		# Handle formatting characters
		char = part[0]
		if char == '\x02': 
			state['bold'] = not state['bold']
		elif char == '\x1D': 
			state['italic'] = not state['italic']
		elif char == '\x1F': 
			state['underline'] = not state['underline']
		elif char == '\x1E':  # Strikethrough toggle
			state['strikethrough'] = not state['strikethrough']
		elif char == '\x03':
			if len(part) > 1:
				colors = part[1:].split(',')
				state['fg'] = colors[0]
				if len(colors) > 1:
					state['bg'] = colors[1]
			else:  # Reset color
				state['fg'], state['bg'] = None, None
		elif char == '\x0F':  # Reset all styles
			state = {k: False if isinstance(v, bool) else None for k, v in state.items()}
		else:
			style = get_style(state)
			result.append(f'<span style="{style}">{part}</span>' if style else part)

	return "".join(result)