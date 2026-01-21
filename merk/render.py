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
	
	msg_to_display = message.contents

	# Messages from /list results are special, and thus have their message built here
	# rather than being built from the default Message() object
	if message.type==LIST_MESSAGE:
		link = f"<a href=\"{message.channel}\"><span style=\"{style['hyperlink']}\">{message.channel}</span></a>"
		if len(message.channel_topic)>0:
			msg_to_display = link+" ("+message.channel_count+" users) - \""+message.channel_topic+"\""
		else:
			msg_to_display = link+" ("+message.channel_count+" users)"

	# Escape all HTML
	if message.type!=SYSTEM_MESSAGE and message.type!=ERROR_MESSAGE and message.type!=SERVER_MESSAGE and message.type!=RAW_SYSTEM_MESSAGE and message.type!=WHOIS_MESSAGE and message.type!=LIST_MESSAGE:
		msg_to_display = html.escape(msg_to_display)

	# Escape HTML if it's turned on for /print
	if config.ESCAPE_HTML_FROM_RAW_SYSTEM_MESSAGE:
		if message.type==RAW_SYSTEM_MESSAGE or message.type==SYSTEM_MESSAGE:
			msg_to_display = html.escape(msg_to_display)

	if config.CONVERT_URLS_TO_LINKS:
		msg_to_display = inject_www_links(msg_to_display,style)

	if config.DISPLAY_IRC_COLORS:
		if string_has_irc_formatting_codes(msg_to_display):
			msg_to_display = convert_irc_color_to_html(msg_to_display,style)
	else:
		if string_has_irc_formatting_codes(msg_to_display):
			msg_to_display = strip_color(msg_to_display)

	p = message.sender.split('!')
	if len(p)==2:
		nick = p[0]
	else:
		nick = message.sender

	if config.ELIDE_LONG_NICKNAMES_IN_CHAT_DISPLAY:
		if len(nick)>config.NICKNAME_PAD_LENGTH:
			nick = elide_text(nick,config.NICKNAME_PAD_LENGTH)

	if config.FORCE_MONOSPACE_RENDERING:
		msg_to_display = "<tt>"+msg_to_display+"</tt>"

	if not config.DO_NOT_APPLY_STYLES_TO_TEXT:

		if message.type==SYSTEM_MESSAGE:
			output = SYSTEM_TEMPLATE
			output_style = style["system"]
			if config.SYSTEM_MESSAGE_PREFIX!='':
				msg_to_display = config.SYSTEM_MESSAGE_PREFIX + " " + msg_to_display
		elif message.type==ERROR_MESSAGE:
			output = SYSTEM_TEMPLATE
			output_style = style["error"]
			if config.SYSTEM_MESSAGE_PREFIX!='':
				msg_to_display = config.SYSTEM_MESSAGE_PREFIX + " " + msg_to_display
		elif message.type==ACTION_MESSAGE:
			output = SYSTEM_TEMPLATE
			output_style = style["action"]
		elif message.type==CHAT_MESSAGE:
			output = MESSAGE_TEMPLATE
			output_style = style["message"]
		elif message.type==SELF_MESSAGE:
			output = MESSAGE_TEMPLATE
			output_style = style["message"]
		elif message.type==NOTICE_MESSAGE:
			if len(nick)==0:
				output = SYSTEM_TEMPLATE
				output_style = style["notice"]
			else:
				output = MESSAGE_TEMPLATE
				output_style = style["message"]
		elif message.type==SERVER_MESSAGE:
			output = SYSTEM_TEMPLATE
			output_style = style["server"]
		elif message.type==PRIVATE_MESSAGE:
			output = MESSAGE_TEMPLATE
			output_style = style["message"]
		elif message.type==RAW_SYSTEM_MESSAGE:
			output = SYSTEM_TEMPLATE
			output_style = style["raw"]
		elif message.type==HORIZONTAL_RULE_MESSAGE:

			if is_background_light:
				output = HORIZONTAL_RULE
			else:
				output = LIGHT_HORIZONTAL_RULE

			style = style["message"]
		elif message.type==HARD_HORIZONTAL_RULE_MESSAGE:

			if is_background_light:
				output = HARD_HORIZONTAL_RULE
			else:
				output = HARD_LIGHT_HORIZONTAL_RULE

			style = style["message"]
		elif message.type==TEXT_HORIZONTAL_RULE_MESSAGE:

			if is_background_light:
				output = TEXT_HORIZONTAL_RULE_TEMPLATE
			else:
				output = LIGHT_TEXT_HORIZONTAL_RULE_TEMPLATE

			style = style["message"]
		elif message.type==WHOIS_MESSAGE:
			output = MESSAGE_TEMPLATE
			output_style = style["server"]
		elif message.type==DATE_MESSAGE:

			if is_background_light:
				output = DATE_MESSAGE_TEMPLATE
			else:
				output = LIGHT_DATE_MESSAGE_TEMPLATE

			style = style["message"]
		elif message.type==LIST_MESSAGE:
			output = SYSTEM_TEMPLATE
			output_style = style["message"]

	else:
		if message.type==SYSTEM_MESSAGE:
			output = SYSTEM_TEMPLATE
			if config.SYSTEM_MESSAGE_PREFIX!='':
				msg_to_display = config.SYSTEM_MESSAGE_PREFIX + " " + msg_to_display
		elif message.type==ERROR_MESSAGE:
			output = SYSTEM_TEMPLATE
			if config.SYSTEM_MESSAGE_PREFIX!='':
				msg_to_display = config.SYSTEM_MESSAGE_PREFIX + " " + msg_to_display
		elif message.type==ACTION_MESSAGE:
			output = SYSTEM_TEMPLATE
		elif message.type==CHAT_MESSAGE:
			output = MESSAGE_TEMPLATE
		elif message.type==SELF_MESSAGE:
			output = MESSAGE_TEMPLATE
		elif message.type==NOTICE_MESSAGE:
			if len(nick)==0:
				output = SYSTEM_TEMPLATE
			else:
				output = MESSAGE_TEMPLATE
		elif message.type==SERVER_MESSAGE:
			output = SYSTEM_TEMPLATE
		elif message.type==PRIVATE_MESSAGE:
			output = MESSAGE_TEMPLATE
		elif message.type==RAW_SYSTEM_MESSAGE:
			output = SYSTEM_TEMPLATE
		elif message.type==HORIZONTAL_RULE_MESSAGE:
			if is_background_light:
				output = HORIZONTAL_RULE
			else:
				output = LIGHT_HORIZONTAL_RULE
		elif message.type==HARD_HORIZONTAL_RULE_MESSAGE:
			if is_background_light:
				output = HARD_HORIZONTAL_RULE
			else:
				output = HARD_LIGHT_HORIZONTAL_RULE
		elif message.type==TEXT_HORIZONTAL_RULE_MESSAGE:
			if is_background_light:
				output = TEXT_HORIZONTAL_RULE_TEMPLATE
			else:
				output = LIGHT_TEXT_HORIZONTAL_RULE_TEMPLATE
		elif message.type==WHOIS_MESSAGE:
			output = MESSAGE_TEMPLATE
		elif message.type==DATE_MESSAGE:

			if is_background_light:
				output = DATE_MESSAGE_TEMPLATE
			else:
				output = LIGHT_DATE_MESSAGE_TEMPLATE
		elif message.type==LIST_MESSAGE:
			output = SYSTEM_TEMPLATE
		output_style = f"color:{foreground};"

	if style=="":
		output = output.replace("!INSERT_MESSAGE_TEMPLATE!",MESSAGE_NO_STYLE_TEMPLATE)
	else:
		output = output.replace("!INSERT_MESSAGE_TEMPLATE!",MESSAGE_STYLE_TEMPLATE)
		output = output.replace("!MESSAGE_STYLE!",output_style)

	if message.type!=HORIZONTAL_RULE_MESSAGE and message.type!=HARD_HORIZONTAL_RULE_MESSAGE and message.type!=TEXT_HORIZONTAL_RULE_MESSAGE and message.type!=DATE_MESSAGE:

		if config.DISPLAY_TIMESTAMP:
			pretty_timestamp = datetime.fromtimestamp(message.timestamp).strftime(config.TIMESTAMP_FORMAT)

			ts = TIMESTAMP_TEMPLATE.replace("!TIMESTAMP_STYLE!",style["timestamp"])
			ts = ts.replace("!TIME!",pretty_timestamp)

			output = output.replace("!TIMESTAMP!",ts)
		else:
			output = output.replace("!TIMESTAMP!",'')

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

	output = output.replace("!ID_STYLE!",user_style)
	output = output.replace("!ID!",nick)

	if message.type==ACTION_MESSAGE:
		output = output.replace("!MESSAGE!",nick +" " +msg_to_display)
	else:
		output = output.replace("!MESSAGE!",msg_to_display)

	return output

def inject_www_links(txt,style):

	if config.DO_NOT_APPLY_STYLES_TO_TEXT:
		background,foreground = styles.parseBackgroundAndForegroundColor(style["all"])
		style = f"color:{foreground};"
	else:
		style = style["hyperlink"]

	search_for_urls = r"(https?:\/\/[a-zA-Z0-9\-\.]+(?:\.[a-zA-Z]{2,6})(?::[0-9]{1,5})?(?:\/([a-zA-Z0-9\-\.\_\~\:\/\?\#\[\]\@\!\$\&\'\(\)\*\+\,\;\=\%]*))?(?:#([a-zA-Z0-9\-\.\_\~\:\/\?\#\[\]\@\!\$\&\'\(\)\*\+\,\;\=\%]+))?)"
	found_urls = re.finditer(search_for_urls, html.unescape(txt))
	urls = [match.group(0).rstrip('.,;:!?()[]{}<>\'"').lstrip('.,;:!?()[]{}<>\'"') for match in found_urls]

	for u in urls:
		u = re.sub('<[^<]+?>', '', u)
		link = f"<a href=\"{u}\"><span style=\"{style}\">{u}</span></a>"
		txt = txt.replace(u,link)
	return txt

# IRC COLOR CODES

def string_has_irc_formatting_codes(data):
	for code in ["\x03","\x02","\x1D","\x1F","\x0F","\x1E"]:
		if code in data: return True
	return False

def convert_irc_color_to_html(text, style):
	background, foreground = styles.parseBackgroundAndForegroundColor(style["all"])
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

def strip_color(text):

	html_tag = "font"

	combos = list(combinations(["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		t = f"\x03{fore},{back}"
		text = text.replace(t,'')

	combos = list(combinations(["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		t = f"\x03{fore},{back}"
		text = text.replace(t,'')

	text = text.replace("\x0310","")
	text = text.replace("\x0311","")
	text = text.replace("\x0312","")
	text = text.replace("\x0313","")
	text = text.replace("\x0314","")
	text = text.replace("\x0315","")

	text = text.replace("\x0300","")
	text = text.replace("\x0301","")
	text = text.replace("\x0302","")
	text = text.replace("\x0303","")
	text = text.replace("\x0304","")
	text = text.replace("\x0305","")
	text = text.replace("\x0306","")
	text = text.replace("\x0307","")
	text = text.replace("\x0308","")
	text = text.replace("\x0309","")

	text = text.replace("\x030","")
	text = text.replace("\x031","")
	text = text.replace("\x032","")
	text = text.replace("\x033","")
	text = text.replace("\x034","")
	text = text.replace("\x035","")
	text = text.replace("\x036","")
	text = text.replace("\x037","")
	text = text.replace("\x038","")
	text = text.replace("\x039","")

	text = text.replace("\x03","")

	text = text.replace("\x02","")
	text = text.replace("\x1D","")
	text = text.replace("\x1F","")
	text = text.replace("\x0F","")

	return text
