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
import json
from pathlib import Path

from .resources import *

CONFIG_DIRECTORY = None
CONFIG_FILE = None

MDI_BACKGROUND_IMAGE = None
APPLICATION_FONT = None
DISPLAY_NAME = APPLICATION_NAME
DISPLAY_ICON = APPLICATION_ICON
DEFAULT_SUBWINDOW_WIDTH = 640
DEFAULT_SUBWINDOW_HEIGHT = 480
COMMAND_HISTORY_LENGTH = 20
DICTIONARY = [
	"merk",
	"mƏrk",
	"Merk",
	"MERK",
]
NICKNAME_PAD_LENGTH = 15
DISPLAY_TIMESTAMP = True
CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES = True
WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW = True
ISSUE_COMMAND_SYMBOL = '/'
DEFAULT_QUIT_MESSAGE = APPLICATION_NAME+" "+APPLICATION_VERSION
DEFAULT_SPELLCHECK_LANGUAGE = "en"
SYSTEM_MESSAGE_PREFIX = "&diams;"
DISPLAY_IRC_COLORS = True
CONVERT_URLS_TO_LINKS = True
AUTOCOMPLETE_COMMANDS = True
AUTOCOMPLETE_NICKS = True
AUTOCOMPLETE_EMOJIS = True
MAXIMUM_LOADED_LOG_SIZE = 500
MARK_END_OF_LOADED_LOG = True
SAVE_CHANNEL_LOGS = True
LOAD_CHANNEL_LOGS = True
SAVE_PRIVATE_LOGS = True
LOAD_PRIVATE_LOGS = True
ASK_BEFORE_DISCONNECT = True
SERVER_TOOLBAR_BUTTON_SIZE = 18
SERVER_TOOLBAR_ICON_SIZE = 18
SHOW_CONNECTION_UPTIME = True
SHOW_CHANNEL_UPTIME = True
SCROLL_CHAT_TO_BOTTOM_ON_RESIZE = True
ENABLE_EMOJI_SHORTCODES = True
ENABLE_SPELLCHECK = True
ASK_BEFORE_RECONNECT = False
NOTIFY_ON_LOST_OR_FAILED_CONNECTION = True
ALWAYS_SCROLL_TO_BOTTOM = False
PROMPT_ON_FAILED_CONNECTION = True
DISPLAY_ACTIVE_CHAT_IN_TITLE = True
TIMESTAMP_FORMAT = "%H:%M:%S"
TIMESTAMP_24_HOUR = True
TIMESTAMP_SHOW_SECONDS = True
PLAIN_USER_LISTS = False
SHOW_USER_INFO_ON_CHAT_WINDOWS = True
AUTOCOMPLETE_CHANNELS = True
COMMANDLINE_NO_SCRIPT = False
SYNTAX_COMMENT_COLOR = "Magenta"
SYNTAX_COMMENT_STYLE = "bold italic"
SYNTAX_COMMAND_COLOR = "darkBlue"
SYNTAX_COMMAND_STYLE = "bold"
SYNTAX_CHANNEL_COLOR = "darkRed"
SYNTAX_CHANNEL_STYLE = "bold"
SYNTAX_BACKGROUND = "white"
SYNTAX_FOREGROUND = "black"
SHOW_SYSTRAY_ICON = True
SHOW_USERLIST_ON_LEFT = False
MINIMIZE_TO_SYSTRAY = False
FLASH_SYSTRAY_NOTIFICATION = True
FLASH_SYSTRAY_SPEED = 500
FLASH_SYSTRAY_NICKNAME = True
FLASH_SYSTRAY_DISCONNECT = True
FLASH_SYSTRAY_PRIVATE = True
FLASH_SYSTRAY_KICK = True
FLASH_SYSTRAY_INVITE = True
FLASH_SYSTRAY_NOTICE = True
FLASH_SYSTRAY_MODE = True
FLASH_SYSTRAY_LIST = True
SYSTRAY_MENU = True
ALIAS_INTERPOLATION_SYMBOL = '$'
SYNTAX_ALIAS_COLOR = "Red"
SYNTAX_ALIAS_STYLE = "bold italic"
MENUBAR_DOCKED_AT_TOP = True
MENUBAR_CAN_FLOAT = False
USE_MENUBAR = True
QT_WINDOW_STYLE = 'Windows'

CHANNEL_TOPIC_BOLD = True

def save_settings(filename):

	settings = {
		"mdi_background_image": MDI_BACKGROUND_IMAGE,
		"application_font": APPLICATION_FONT,
		"display_name": DISPLAY_NAME,
		"display_icon": DISPLAY_ICON,
		"default_subwindow_width": DEFAULT_SUBWINDOW_WIDTH,
		"default_subwindow_height": DEFAULT_SUBWINDOW_HEIGHT,
		"command_history_length": COMMAND_HISTORY_LENGTH,
		"dictionary": DICTIONARY,
		"nickname_pad_length": NICKNAME_PAD_LENGTH,
		"display_timestamp": DISPLAY_TIMESTAMP,
		"timestamp_format": TIMESTAMP_FORMAT,
		"create_window_for_incoming_private_messages": CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES,
		"write_private_messages_to_server_window": WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW,
		"issue_command_symbol": ISSUE_COMMAND_SYMBOL,
		"default_quit_message": DEFAULT_QUIT_MESSAGE,
		"default_spellcheck_language": DEFAULT_SPELLCHECK_LANGUAGE,
		"system_message_prefix": SYSTEM_MESSAGE_PREFIX,
		"display_irc_colors": DISPLAY_IRC_COLORS,
		"convert_urls_to_links": CONVERT_URLS_TO_LINKS,
		"autocomplete_commands": AUTOCOMPLETE_COMMANDS,
		"autocomplete_nicks": AUTOCOMPLETE_NICKS,
		"autocomplete_emojis": AUTOCOMPLETE_EMOJIS,
		"maximum_loaded_log_size": MAXIMUM_LOADED_LOG_SIZE,
		"mark_end_of_loaded_log": MARK_END_OF_LOADED_LOG,
		"save_channel_logs": SAVE_CHANNEL_LOGS,
		"load_channel_logs": LOAD_CHANNEL_LOGS,
		"save_private_logs": SAVE_PRIVATE_LOGS,
		"load_private_logs": LOAD_PRIVATE_LOGS,
		"ask_before_disconnect": ASK_BEFORE_DISCONNECT,
		"server_toolbar_button_size": SERVER_TOOLBAR_BUTTON_SIZE,
		"server_toolbar_icon_size": SERVER_TOOLBAR_ICON_SIZE,
		"show_connection_uptime": SHOW_CONNECTION_UPTIME,
		"show_channel_uptime": SHOW_CHANNEL_UPTIME,
		"scroll_chat_to_bottom_on_resize": SCROLL_CHAT_TO_BOTTOM_ON_RESIZE,
		"enable_emoji_shortcodes": ENABLE_EMOJI_SHORTCODES,
		"enable_spellcheck": ENABLE_SPELLCHECK,
		"ask_before_reconnect": ASK_BEFORE_RECONNECT,
		"notify_on_lost_or_failed_connection": NOTIFY_ON_LOST_OR_FAILED_CONNECTION,
		"always_scroll_to_bottom": ALWAYS_SCROLL_TO_BOTTOM,
		"prompt_on_failed_connection": PROMPT_ON_FAILED_CONNECTION,
		"display_active_chat_in_title": DISPLAY_ACTIVE_CHAT_IN_TITLE,
		"timestamp_24_hour": TIMESTAMP_24_HOUR,
		"timestamp_show_seconds": TIMESTAMP_SHOW_SECONDS,
		"plain_user_lists": PLAIN_USER_LISTS,
		"show_user_info_on_chat_windows": SHOW_USER_INFO_ON_CHAT_WINDOWS,
		"autocomplete_channels": AUTOCOMPLETE_CHANNELS,
		"syntax_comment_color": SYNTAX_COMMENT_COLOR,
		"syntax_comment_style": SYNTAX_COMMENT_STYLE,
		"syntax_command_color": SYNTAX_COMMAND_COLOR,
		"syntax_command_style": SYNTAX_COMMAND_STYLE,
		"syntax_channel_color": SYNTAX_CHANNEL_COLOR,
		"syntax_channel_style": SYNTAX_CHANNEL_STYLE,
		"syntax_background_color": SYNTAX_BACKGROUND,
		"syntax_foreground_color": SYNTAX_FOREGROUND,
		"show_systray_icon": SHOW_SYSTRAY_ICON,
		"show_userlist_on_left": SHOW_USERLIST_ON_LEFT,
		"minimize_to_system_tray": MINIMIZE_TO_SYSTRAY,
		"systray_notifications": FLASH_SYSTRAY_NOTIFICATION,
		"systray_notification_speed": FLASH_SYSTRAY_SPEED,
		"systray_notification_nickname": FLASH_SYSTRAY_NICKNAME,
		"systray_notification_disconnect": FLASH_SYSTRAY_DISCONNECT,
		"systray_notification_private": FLASH_SYSTRAY_PRIVATE,
		"systray_notification_kick": FLASH_SYSTRAY_KICK,
		"systray_notification_invite": FLASH_SYSTRAY_INVITE,
		"systray_notification_notice": FLASH_SYSTRAY_NOTICE,
		"systray_notification_mode": FLASH_SYSTRAY_MODE,
		"systray_notification_list": FLASH_SYSTRAY_LIST,
		"show_systray_menu": SYSTRAY_MENU,
		"alias_interpolation_symbol": ALIAS_INTERPOLATION_SYMBOL,
		"syntax_alias_color": SYNTAX_ALIAS_COLOR,
		"syntax_alias_style": SYNTAX_ALIAS_STYLE,
		"menubar_docked_at_top": MENUBAR_DOCKED_AT_TOP,
		"menubar_can_float": MENUBAR_CAN_FLOAT,
		"use_menubar": USE_MENUBAR,
		"qt_window_style": QT_WINDOW_STYLE,
	}

	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def patch_settings(settings):
	if not "qt_window_style" in settings:
		settings["qt_window_style"] = QT_WINDOW_STYLE
	if not "use_menubar" in settings:
		settings["use_menubar"] = USE_MENUBAR
	if not "menubar_can_float" in settings:
		settings["menubar_can_float"] = MENUBAR_CAN_FLOAT
	if not "menubar_docked_at_top" in settings:
		settings["menubar_docked_at_top"] = MENUBAR_DOCKED_AT_TOP
	if not "syntax_alias_color" in settings:
		settings["syntax_alias_color"] = SYNTAX_ALIAS_COLOR
	if not "syntax_alias_style" in settings:
		settings["syntax_alias_style"] = SYNTAX_ALIAS_STYLE
	if not "alias_interpolation_symbol" in settings:
		settings["alias_interpolation_symbol"] = ALIAS_INTERPOLATION_SYMBOL
	if not "systray_notification_list" in settings:
		settings["systray_notification_list"] = FLASH_SYSTRAY_LIST
	if not "systray_notification_notice" in settings:
		settings["systray_notification_notice"] = FLASH_SYSTRAY_NOTICE
	if not "systray_notification_mode" in settings:
		settings["systray_notification_mode"] = FLASH_SYSTRAY_MODE
	if not "minimize_to_system_tray" in settings:
		settings["minimize_to_system_tray"] = MINIMIZE_TO_SYSTRAY
	if not "show_userlist_on_left" in settings:
		settings["show_userlist_on_left"] = SHOW_USERLIST_ON_LEFT
	if not "show_systray_icon" in settings:
		settings["show_systray_icon"] = SHOW_SYSTRAY_ICON
	if not "syntax_comment_color" in settings:
		settings["syntax_comment_color"] = SYNTAX_COMMENT_COLOR
	if not "syntax_comment_style" in settings:
		settings["syntax_comment_style"] = SYNTAX_COMMENT_STYLE
	if not "syntax_command_color" in settings:
		settings["syntax_command_color"] = SYNTAX_COMMAND_COLOR
	if not "syntax_command_style" in settings:
		settings["syntax_command_style"] = SYNTAX_COMMAND_STYLE
	if not "syntax_channel_color" in settings:
		settings["syntax_channel_color"] = SYNTAX_CHANNEL_COLOR
	if not "syntax_channel_style" in settings:
		settings["syntax_channel_style"] = SYNTAX_CHANNEL_STYLE
	if not "syntax_background_color" in settings:
		settings["syntax_background_color"] = SYNTAX_BACKGROUND
	if not "syntax_foreground_color" in settings:
		settings["syntax_foreground_color"] = SYNTAX_FOREGROUND
	if not "autocomplete_channels" in settings:
		settings["autocomplete_channels"] = AUTOCOMPLETE_CHANNELS
	if not "show_user_info_on_chat_windows" in settings:
		settings["show_user_info_on_chat_windows"] = SHOW_USER_INFO_ON_CHAT_WINDOWS
	if not "plain_user_lists" in settings:
		settings["plain_user_lists"] = PLAIN_USER_LISTS
	if not "timestamp_24_hour" in settings:
		settings["timestamp_24_hour"] = TIMESTAMP_24_HOUR
	if not "timestamp_show_seconds" in settings:
		settings["timestamp_show_seconds"] = TIMESTAMP_SHOW_SECONDS
	if not "display_active_chat_in_title" in settings:
		settings["display_active_chat_in_title"] = DISPLAY_ACTIVE_CHAT_IN_TITLE
	if not "prompt_on_failed_connection" in settings:
		settings["prompt_on_failed_connection"] = PROMPT_ON_FAILED_CONNECTION
	if not "always_scroll_to_bottom" in settings:
		settings["always_scroll_to_bottom"] = ALWAYS_SCROLL_TO_BOTTOM
	if not "notify_on_lost_or_failed_connection" in settings:
		settings["notify_on_lost_or_failed_connection"] = NOTIFY_ON_LOST_OR_FAILED_CONNECTION
	if not "ask_before_reconnect" in settings:
		settings["ask_before_reconnect"] = ASK_BEFORE_RECONNECT
	if not "enable_spellcheck" in settings:
		settings["enable_spellcheck"] = ENABLE_SPELLCHECK
	if not "enable_emoji_shortcodes" in settings:
		settings["enable_emoji_shortcodes"] = ENABLE_EMOJI_SHORTCODES
	if not "scroll_chat_to_bottom_on_resize" in settings:
		settings["scroll_chat_to_bottom_on_resize"] = SCROLL_CHAT_TO_BOTTOM_ON_RESIZE
	if not "show_channel_uptime" in settings:
		settings["show_channel_uptime"] = SHOW_CHANNEL_UPTIME
	if not "show_connection_uptime" in settings:
		settings["show_connection_uptime"] = SHOW_CONNECTION_UPTIME
	if not "server_toolbar_button_size" in settings:
		settings["server_toolbar_button_size"] = SERVER_TOOLBAR_BUTTON_SIZE
	if not "server_toolbar_icon_size" in settings:
		settings["server_toolbar_icon_size"] = SERVER_TOOLBAR_ICON_SIZE
	if not "ask_before_disconnect" in settings:
		settings["ask_before_disconnect"] = ASK_BEFORE_DISCONNECT
	if not "save_private_logs" in settings:
		settings["save_private_logs"] = SAVE_PRIVATE_LOGS
	if not "load_private_logs" in settings:
		settings["load_private_logs"] = LOAD_PRIVATE_LOGS
	if not "save_channel_logs" in settings:
		settings["save_channel_logs"] = SAVE_CHANNEL_LOGS
	if not "load_channel_logs" in settings:
		settings["load_channel_logs"] = LOAD_CHANNEL_LOGS
	if not "mdi_background_image" in settings:
		settings["mdi_background_image"] = MDI_BACKGROUND_IMAGE
	if not "application_font" in settings:
		settings["application_font"] = APPLICATION_FONT
	if not "display_name" in settings:
		settings["display_name"] = DISPLAY_NAME
	if not "display_icon" in settings:
		settings["display_icon"] = DISPLAY_ICON
	if not "default_subwindow_width" in settings:
		settings["default_subwindow_width"] = DEFAULT_SUBWINDOW_WIDTH
	if not "default_subwindow_height" in settings:
		settings["default_subwindow_height"] = DEFAULT_SUBWINDOW_HEIGHT
	if not "command_history_length" in settings:
		settings["command_history_length"] = COMMAND_HISTORY_LENGTH
	if not "dictionary" in settings:
		settings["dictionary"] = DICTIONARY
	if not "nickname_pad_length" in settings:
		settings["nickname_pad_length"] = NICKNAME_PAD_LENGTH
	if not "display_timestamp" in settings:
		settings["display_timestamp"] = DISPLAY_TIMESTAMP
	if not "timestamp_format" in settings:
		settings["timestamp_format"] = TIMESTAMP_FORMAT
	if not "create_window_for_incoming_private_messages" in settings:
		settings["create_window_for_incoming_private_messages"] = CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES
	if not "write_private_messages_to_server_window" in settings:
		settings["write_private_messages_to_server_window"] = WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW
	if not "issue_command_symbol" in settings:
		settings["issue_command_symbol"] = ISSUE_COMMAND_SYMBOL
	if not "default_quit_message" in settings:
		settings["default_quit_message"] = DEFAULT_QUIT_MESSAGE
	if not "default_spellcheck_language" in settings:
		settings["default_spellcheck_language"] = DEFAULT_SPELLCHECK_LANGUAGE
	if not "system_message_prefix" in settings:
		settings["system_message_prefix"] = SYSTEM_MESSAGE_PREFIX
	if not "display_irc_colors" in settings:
		settings["display_irc_colors"] = DISPLAY_IRC_COLORS
	if not "convert_urls_to_links" in settings:
		settings["convert_urls_to_links"] = CONVERT_URLS_TO_LINKS
	if not "autocomplete_commands" in settings:
		settings["autocomplete_commands"] = AUTOCOMPLETE_COMMANDS
	if not "autocomplete_nicks" in settings:
		settings["autocomplete_nicks"] = AUTOCOMPLETE_NICKS
	if not "autocomplete_emojis" in settings:
		settings["autocomplete_emojis"] = AUTOCOMPLETE_EMOJIS
	if not "maximum_loaded_log_size" in settings:
		settings["maximum_loaded_log_size"] = MAXIMUM_LOADED_LOG_SIZE
	if not "mark_end_of_loaded_log" in settings:
		settings["mark_end_of_loaded_log"] = MARK_END_OF_LOADED_LOG
	if not "systray_notifications" in settings:
		settings["systray_notifications"] = FLASH_SYSTRAY_NOTIFICATION
	if not "systray_notification_speed" in settings:
		settings["systray_notification_speed"] = FLASH_SYSTRAY_SPEED
	if not "systray_notification_nickname" in settings:
		settings["systray_notification_nickname"] = FLASH_SYSTRAY_NICKNAME
	if not "systray_notification_disconnect" in settings:
		settings["systray_notification_disconnect"] = FLASH_SYSTRAY_DISCONNECT
	if not "systray_notification_private" in settings:
		settings["systray_notification_private"] = FLASH_SYSTRAY_PRIVATE
	if not "systray_notification_kick" in settings:
		settings["systray_notification_kick"] = FLASH_SYSTRAY_KICK
	if not "systray_notification_invite" in settings:
		settings["systray_notification_invite"] = FLASH_SYSTRAY_INVITE
	if not "show_systray_menu" in settings:
		settings["show_systray_menu"] = SYSTRAY_MENU

	return settings

def load_settings(filename):
	global MDI_BACKGROUND_IMAGE
	global APPLICATION_FONT
	global DISPLAY_NAME
	global DISPLAY_ICON
	global DEFAULT_SUBWINDOW_WIDTH
	global DEFAULT_SUBWINDOW_HEIGHT
	global COMMAND_HISTORY_LENGTH
	global DICTIONARY
	global NICKNAME_PAD_LENGTH
	global DISPLAY_TIMESTAMP
	global TIMESTAMP_FORMAT
	global CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES
	global WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW
	global ISSUE_COMMAND_SYMBOL
	global DEFAULT_QUIT_MESSAGE
	global DEFAULT_SPELLCHECK_LANGUAGE
	global SYSTEM_MESSAGE_PREFIX
	global DISPLAY_IRC_COLORS
	global CONVERT_URLS_TO_LINKS
	global AUTOCOMPLETE_COMMANDS
	global AUTOCOMPLETE_NICKS
	global AUTOCOMPLETE_EMOJIS
	global MAXIMUM_LOADED_LOG_SIZE
	global MARK_END_OF_LOADED_LOG
	global SAVE_CHANNEL_LOGS
	global LOAD_CHANNEL_LOGS
	global SAVE_PRIVATE_LOGS
	global LOAD_PRIVATE_LOGS
	global ASK_BEFORE_DISCONNECT
	global SERVER_TOOLBAR_BUTTON_SIZE
	global SERVER_TOOLBAR_ICON_SIZE
	global SHOW_CONNECTION_UPTIME
	global SHOW_CHANNEL_UPTIME
	global SCROLL_CHAT_TO_BOTTOM_ON_RESIZE
	global ENABLE_EMOJI_SHORTCODES
	global ENABLE_SPELLCHECK
	global ASK_BEFORE_RECONNECT
	global NOTIFY_ON_LOST_OR_FAILED_CONNECTION
	global ALWAYS_SCROLL_TO_BOTTOM
	global PROMPT_ON_FAILED_CONNECTION
	global DISPLAY_ACTIVE_CHAT_IN_TITLE
	global TIMESTAMP_24_HOUR
	global TIMESTAMP_SHOW_SECONDS
	global PLAIN_USER_LISTS
	global SHOW_USER_INFO_ON_CHAT_WINDOWS
	global AUTOCOMPLETE_CHANNELS
	global SYNTAX_COMMENT_COLOR
	global SYNTAX_COMMENT_STYLE
	global SYNTAX_COMMAND_COLOR
	global SYNTAX_COMMAND_STYLE
	global SYNTAX_CHANNEL_COLOR
	global SYNTAX_CHANNEL_STYLE
	global SYNTAX_BACKGROUND
	global SYNTAX_FOREGROUND
	global SHOW_SYSTRAY_ICON
	global SHOW_USERLIST_ON_LEFT
	global MINIMIZE_TO_SYSTRAY
	global FLASH_SYSTRAY_NOTIFICATION
	global FLASH_SYSTRAY_SPEED
	global FLASH_SYSTRAY_NICKNAME
	global FLASH_SYSTRAY_DISCONNECT
	global FLASH_SYSTRAY_PRIVATE
	global FLASH_SYSTRAY_KICK
	global FLASH_SYSTRAY_INVITE
	global FLASH_SYSTRAY_NOTICE
	global FLASH_SYSTRAY_MODE
	global FLASH_SYSTRAY_LIST
	global SYSTRAY_MENU
	global ALIAS_INTERPOLATION_SYMBOL
	global SYNTAX_ALIAS_COLOR
	global SYNTAX_ALIAS_STYLE
	global MENUBAR_DOCKED_AT_TOP
	global MENUBAR_CAN_FLOAT
	global USE_MENUBAR
	global QT_WINDOW_STYLE

	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			settings = json.load(read_settings)

		prepatch_length = len(settings)
		settings = patch_settings(settings)
		postpatch_length = len(settings)

		USE_MENUBAR = settings["use_menubar"]
		MENUBAR_CAN_FLOAT = settings["menubar_can_float"]
		MENUBAR_DOCKED_AT_TOP = settings["menubar_docked_at_top"]
		SYNTAX_ALIAS_COLOR = settings["syntax_alias_color"]
		SYNTAX_ALIAS_STYLE = settings["syntax_alias_style"]
		ALIAS_INTERPOLATION_SYMBOL = settings["alias_interpolation_symbol"]
		MINIMIZE_TO_SYSTRAY = settings["minimize_to_system_tray"]
		SHOW_USERLIST_ON_LEFT = settings["show_userlist_on_left"]
		SHOW_SYSTRAY_ICON = settings["show_systray_icon"]
		AUTOCOMPLETE_CHANNELS = settings["autocomplete_channels"]
		SHOW_USER_INFO_ON_CHAT_WINDOWS = settings["show_user_info_on_chat_windows"]
		PLAIN_USER_LISTS = settings["plain_user_lists"]
		TIMESTAMP_24_HOUR = settings["timestamp_24_hour"]
		TIMESTAMP_SHOW_SECONDS = settings["timestamp_show_seconds"]
		DISPLAY_ACTIVE_CHAT_IN_TITLE = settings["display_active_chat_in_title"]
		PROMPT_ON_FAILED_CONNECTION = settings["prompt_on_failed_connection"]
		ALWAYS_SCROLL_TO_BOTTOM = settings["always_scroll_to_bottom"]
		NOTIFY_ON_LOST_OR_FAILED_CONNECTION = settings["notify_on_lost_or_failed_connection"]
		ASK_BEFORE_RECONNECT = settings["ask_before_reconnect"]
		ENABLE_SPELLCHECK = settings["enable_spellcheck"]
		ENABLE_EMOJI_SHORTCODES = settings["enable_emoji_shortcodes"]
		SCROLL_CHAT_TO_BOTTOM_ON_RESIZE = settings["scroll_chat_to_bottom_on_resize"]
		SHOW_CHANNEL_UPTIME = settings["show_channel_uptime"]
		SHOW_CONNECTION_UPTIME = settings["show_connection_uptime"]
		SERVER_TOOLBAR_BUTTON_SIZE = settings["server_toolbar_button_size"]
		SERVER_TOOLBAR_ICON_SIZE = settings["server_toolbar_icon_size"]
		ASK_BEFORE_DISCONNECT = settings["ask_before_disconnect"]
		SAVE_PRIVATE_LOGS = settings["save_private_logs"]
		LOAD_PRIVATE_LOGS = settings["load_private_logs"]
		SAVE_CHANNEL_LOGS = settings["save_channel_logs"]
		LOAD_CHANNEL_LOGS = settings["load_channel_logs"]
		MDI_BACKGROUND_IMAGE = settings["mdi_background_image"]
		APPLICATION_FONT = settings["application_font"]
		DISPLAY_NAME = settings["display_name"]
		DISPLAY_ICON = settings["display_icon"]
		DEFAULT_SUBWINDOW_WIDTH = settings["default_subwindow_width"]
		DEFAULT_SUBWINDOW_HEIGHT = settings["default_subwindow_height"]
		COMMAND_HISTORY_LENGTH = settings["command_history_length"]
		DICTIONARY = settings["dictionary"]
		NICKNAME_PAD_LENGTH = settings["nickname_pad_length"]
		DISPLAY_TIMESTAMP = settings["display_timestamp"]
		TIMESTAMP_FORMAT = settings["timestamp_format"]
		CREATE_WINDOW_FOR_INCOMING_PRIVATE_MESSAGES = settings["create_window_for_incoming_private_messages"]
		WRITE_PRIVATE_MESSAGES_TO_SERVER_WINDOW = settings["write_private_messages_to_server_window"]
		ISSUE_COMMAND_SYMBOL = settings["issue_command_symbol"]
		DEFAULT_QUIT_MESSAGE = settings["default_quit_message"]
		DEFAULT_SPELLCHECK_LANGUAGE = settings["default_spellcheck_language"]
		SYSTEM_MESSAGE_PREFIX = settings["system_message_prefix"]
		DISPLAY_IRC_COLORS = settings["display_irc_colors"]
		CONVERT_URLS_TO_LINKS = settings["convert_urls_to_links"]
		AUTOCOMPLETE_COMMANDS = settings["autocomplete_commands"]
		AUTOCOMPLETE_NICKS = settings["autocomplete_nicks"]
		AUTOCOMPLETE_EMOJIS = settings["autocomplete_emojis"]
		MAXIMUM_LOADED_LOG_SIZE = settings["maximum_loaded_log_size"]
		MARK_END_OF_LOADED_LOG = settings["mark_end_of_loaded_log"]
		SYNTAX_COMMENT_COLOR = settings["syntax_comment_color"]
		SYNTAX_COMMENT_STYLE = settings["syntax_comment_style"]
		SYNTAX_COMMAND_COLOR = settings["syntax_command_color"]
		SYNTAX_COMMAND_STYLE = settings["syntax_command_style"]
		SYNTAX_CHANNEL_COLOR = settings["syntax_channel_color"]
		SYNTAX_CHANNEL_STYLE = settings["syntax_channel_style"]
		SYNTAX_BACKGROUND = settings["syntax_background_color"]
		SYNTAX_FOREGROUND = settings["syntax_foreground_color"]
		FLASH_SYSTRAY_NOTIFICATION = settings["systray_notifications"]
		FLASH_SYSTRAY_SPEED = settings["systray_notification_speed"]
		FLASH_SYSTRAY_NICKNAME = settings["systray_notification_nickname"]
		FLASH_SYSTRAY_DISCONNECT = settings["systray_notification_disconnect"]
		FLASH_SYSTRAY_PRIVATE = settings["systray_notification_private"]
		FLASH_SYSTRAY_KICK = settings["systray_notification_kick"]
		FLASH_SYSTRAY_INVITE = settings["systray_notification_invite"]
		FLASH_SYSTRAY_NOTICE = settings["systray_notification_notice"]
		FLASH_SYSTRAY_MODE = settings["systray_notification_mode"]
		FLASH_SYSTRAY_LIST = settings["systray_notification_list"]
		SYSTRAY_MENU = settings["show_systray_menu"]
		QT_WINDOW_STYLE = settings["qt_window_style"]

		if prepatch_length!=postpatch_length:
			save_settings(filename)
	else:
		save_settings(filename)

def initialize(directory,directory_name):
	global CONFIG_DIRECTORY
	global CONFIG_FILE

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	CONFIG_DIRECTORY = os.path.join(directory,directory_name)
	if not os.path.isdir(CONFIG_DIRECTORY): os.mkdir(CONFIG_DIRECTORY)

	CONFIG_FILE = os.path.join(CONFIG_DIRECTORY,"settings.json")
