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

from .resources import *

CONFIG_DIRECTORY = None
CONFIG_FILE = None

APPLICATION_FONT = None
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
DEFAULT_QUIT_MESSAGE = APPLICATION_NAME+" $_VERSION"
DEFAULT_SPELLCHECK_LANGUAGE = "en"
SYSTEM_MESSAGE_PREFIX = "&diams;"
DISPLAY_IRC_COLORS = True
CONVERT_URLS_TO_LINKS = True
AUTOCOMPLETE_COMMANDS = True
AUTOCOMPLETE_NICKS = True
AUTOCOMPLETE_SHORTCODES = True
MAXIMUM_LOADED_LOG_SIZE = 500
MARK_END_OF_LOADED_LOG = True
SAVE_CHANNEL_LOGS = True
LOAD_CHANNEL_LOGS = True
SAVE_PRIVATE_LOGS = True
LOAD_PRIVATE_LOGS = True
ASK_BEFORE_DISCONNECT = True
INTERFACE_BUTTON_SIZE = 18
INTERFACE_BUTTON_ICON_SIZE = 18
SHOW_CONNECTION_UPTIME = True
SHOW_CHANNEL_UPTIME = True
SCROLL_CHAT_TO_BOTTOM_ON_RESIZE = True
ENABLE_EMOJI_SHORTCODES = True
ENABLE_SPELLCHECK = True
ASK_BEFORE_RECONNECT = False
NOTIFY_ON_LOST_OR_FAILED_CONNECTION = True
ALWAYS_SCROLL_TO_BOTTOM = False
PROMPT_ON_FAILED_CONNECTION = True
DISPLAY_ACTIVE_SUBWINDOW_IN_TITLE = True
TIMESTAMP_FORMAT = "%H:%M:%S"
TIMESTAMP_24_HOUR = True
TIMESTAMP_SHOW_SECONDS = True
PLAIN_USER_LISTS = False
SHOW_USER_INFO_ON_CHAT_WINDOWS = True
AUTOCOMPLETE_CHANNELS = True
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
SHOW_CHANNEL_TOPIC = True
SHOW_CHANNEL_TOPIC_IN_WINDOW_TITLE = False
SHOW_CHANNEL_NAME_AND_MODES = True
SHOW_BANLIST_MENU = True
SHOW_USERLIST = True
SHOW_INPUT_MENU = True
SHOW_WINDOWBAR = True
WINDOWBAR_TOP_OF_SCREEN = True
WINDOWBAR_INCLUDE_SERVERS = False
# center, left, or right
WINDOWBAR_JUSTIFY = 'center'
WINDOWBAR_CAN_FLOAT = False
WINDOWBAR_SHOW_ICONS = False
WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED = True
WINDOWBAR_INCLUDE_EDITORS = True
SHOW_CHAT_CONTEXT_MENUS = True
ALWAYS_SHOW_CURRENT_WINDOW_FIRST = True
MENUBAR_JUSTIFY = 'left'
MENUBAR_MENU = True
WINDOWBAR_MENU = True
MAIN_MENU_IRC_NAME = "IRC"
MAIN_MENU_TOOLS_NAME = "Tools"
MAIN_MENU_WINDOWS_NAME = "Windows"
MAIN_MENU_HELP_NAME = "Help"
DARK_MODE = False
SIMPLIFIED_DIALOGS = False
EDITOR_PROMPT_SAVE = True
WINDOWBAR_INCLUDE_CHANNELS = True
WINDOWBAR_INCLUDE_PRIVATE = True
JOIN_ON_INVITE = True
GET_HOSTMASKS_ON_CHANNEL_JOIN = True
MAIN_MENU_SETTINGS_NAME = "Settings"
DO_INTERMITTENT_LOG_SAVES = True
LOG_SAVE_INTERVAL = 1800000
SHOW_STATUS_BAR_ON_SERVER_WINDOWS = False
SHOW_STATUS_BAR_ON_CHAT_WINDOWS = True
MAXIMIZE_ON_STARTUP = False
SHOW_LINKS_TO_NETWORK_WEBPAGES = True
DISPLAY_NICK_ON_SERVER_WINDOWS = False
SOUND_NOTIFICATION_NICKNAME = True
SOUND_NOTIFICATION_DISCONNECT = True
SOUND_NOTIFICATION_PRIVATE = True
SOUND_NOTIFICATION_KICK = True
SOUND_NOTIFICATION_INVITE = True
SOUND_NOTIFICATION_NOTICE = True
SOUND_NOTIFICATION_MODE = True
SOUND_NOTIFICATION_FILE = BELL_NOTIFICATION
SOUND_NOTIFICATIONS = False
FORCE_MONOSPACE_RENDERING = False
FORCE_DEFAULT_STYLE = False
ALWAYS_ON_TOP = False
ASK_BEFORE_CLOSE = False
AUTOCOMPLETE_ALIAS = True
INTERPOLATE_ALIASES_INTO_INPUT = True
REQUEST_CHANNEL_LIST_ON_CONNECTION = True
EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH = True
WINDOWBAR_INCLUDE_LIST = False
SHOW_CHANNEL_LIST_IN_WINDOWS_MENU = True
SEARCH_ALL_TERMS_IN_CHANNEL_LIST = True
CLOSING_WINDOW_MINIMIZES_TO_TRAY = True
SHOW_SERVER_INFO_IN_WINDOWS_MENU = True
SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS = False
SHOW_SERVER_WINDOW_TOOLBAR = True
SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS = True
SHOW_STATUS_BAR_ON_LIST_WINDOWS = True
WINDOWBAR_UNDERLINE_ACTIVE_WINDOW = True
WINDOWBAR_HOVER_EFFECT = True
SHOW_CHANNEL_TOPIC_IN_APPLICATION_TITLE = False
DO_NOT_APPLY_STYLE_TO_INPUT_WIDGET = False
DO_NOT_APPLY_STYLE_TO_USERLIST = False
DO_NOT_SHOW_APPLICATION_NAME_IN_TITLE = False
APPLY_SYNTAX_STYLES_TO_INPUT_WIDGET = True
SYNTAX_NICKNAME_COLOR = "darkRed"
SYNTAX_NICKNAME_STYLE = "bold"
SYNTAX_EMOJI_COLOR = "Magenta"
SYNTAX_EMOJI_STYLE = "bold italic"
HIDE_USERLIST_HORIZONTAL_SCROLLBAR = True
SHOW_AWAY_AND_BACK_MESSAGES = True
SHOW_AWAY_STATUS_IN_USERLISTS = True
SHOW_AWAY_STATUS_IN_NICK_DISPLAY = True
DEFAULT_AWAY_MESSAGE = "Away at $_DATE $_TIME"
USE_AUTOAWAY = False
AUTOAWAY_TIME = 3600
PROMPT_FOR_AWAY_MESSAGE = False
CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES = False
DO_NOT_APPLY_STYLES_TO_TEXT = False
TYPING_INPUT_CANCELS_AUTOAWAY = True
WINDOW_INTERACTION_CANCELS_AUTOAWAY = False
APP_INTERACTION_CANCELS_AUTOAWAY = False
AUTOCOMPLETE_SHORTCODES_IN_AWAY_MESSAGE_WIDGET = True
DOUBLECLICK_TO_RESTORE_WINDOW_FROM_SYSTRAY = True
CLICK_SYSTRAY_ICON_TO_MINIMIZE_TO_TRAY = True
LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE = False
LOG_CHANNEL_TOPICS = True
LOG_CHANNEL_JOIN = True
LOG_CHANNEL_PART = True
LOG_CHANNEL_QUIT = True
TWISTED_CLIENT_HEARTBEAT = 120
SPELLCHECKER_DISTANCE = 1
LOG_CHANNEL_NICKNAME_CHANGE = True
ENABLE_COMMAND_INPUT_HISTORY = True
SHOW_CHANNEL_MENU = True
EMOJI_LANGUAGE = 'alias'
WRITE_INPUT_AND_OUTPUT_TO_CONSOLE = False
WRITE_INPUT_AND_OUTPUT_TO_FILE = False
AUTOCOMPLETE_SHORTCODES_IN_QUIT_MESSAGE_WIDGET = True
SHOW_STATUS_BAR_ON_EDITOR_WINDOWS = True
ENABLE_ALIASES = True
ENABLE_AUTOCOMPLETE = True
ENABLE_STYLE_EDITOR = True
DISPLAY_SCRIPT_ERRORS = True
STRIP_NICKNAME_PADDING_FROM_DISPLAY = False
WINDOWBAR_INCLUDE_MANAGER = False
IGNORE_LIST = []
USERLIST_ITEMS_NON_SELECTABLE = False
EDITOR_USES_SYNTAX_HIGHLIGHTING = True
SHOW_USER_COUNT_DISPLAY = True
ALLOW_MENUS_TO_CHANGE_SPELLCHECK_SETTINGS = True
SPELLCHECK_UNDERLINE_COLOR = "#FF0000"
SHOW_MISSPELLED_WORDS_IN_ITALICS = False
SHOW_MISSPELLED_WORDS_IN_BOLD = False
SHOW_MISSPELLED_WORDS_IN_STRIKEOUT = False
SHOW_MISSPELLED_WORDS_IN_COLOR = False
SCRIPTING_ENGINE_ENABLED = True
SHOW_PINGS_IN_CONSOLE = False
CLOSING_SERVER_WINDOW_DISCONNECTS = False
SHOW_IGNORE_STATUS_IN_USERLISTS = True
MAXIMUM_INSERT_DEPTH = 10
WINDOWBAR_SHOW_UNREAD_MESSAGES = True
WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH = 1000
WINDOWBAR_ENTRY_MENU = True
INCLUDE_SCRIPT_COMMAND_SHORTCUT = True
DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS = True
CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES = False
HALT_SCRIPT_EXECUTION_ON_ERROR = True
REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS = True
ENABLE_INSERT_COMMAND = True
LOG_CHANNEL_NOTICE = True
SHOW_DATES_IN_LOGS = True
INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE = True
INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE = True
HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG = False
ASK_FOR_SERVER_ON_STARTUP = True
PROMPT_FOR_SCRIPT_FILE = False
SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR = True
HIDE_SERVER_WINDOWS_ON_SIGNON = False
ENABLE_DELAY_COMMAND = True
WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS = True
DOUBLECLICK_TO_OPEN_PRIVATE_CHAT = True
AUTOCOMPLETE_FILENAMES = True
MAXIMIZE_SUBWINDOWS_ON_CREATION = False
SHOW_CHANNEL_NAME_IN_SUBWINDOW_TITLE = True
SHOW_HIDDEN_CHANNEL_WINDOWS_IN_WINDOWBAR = True
SHOW_HIDDEN_PRIVATE_WINDOWS_IN_WINDOWBAR = True
SYNTAX_SCRIPT_COLOR = "darkGreen"
SYNTAX_SCRIPT_STYLE = "bold"
AUTOCOMPLETE_SETTINGS = True
ENABLE_CONFIG_COMMAND = True
DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION = True
ESCAPE_HTML_FROM_RAW_SYSTEM_MESSAGE = False
HIDE_WINDOWBAR_IF_EMPTY = True
WINDOWBAR_INCLUDE_README = False
WINDOWBAR_BOLD_ACTIVE_WINDOW = True
MENUBAR_HOVER_EFFECT = True
ENABLE_BUILT_IN_ALIASES = True
SYNTAX_OPERATOR_COLOR = "blue"
SYNTAX_OPERATOR_STYLE = "bold"
ENABLE_GOTO_COMMAND = True
ENABLE_IF_COMMAND = True
WRITE_OUTGOING_PRIVATE_MESSAGES_TO_CURRENT_WINDOW = True
SHOW_FULL_SCREEN = False
SET_SUBWINDOW_ORDER = 'creation' # creation, stacking, activation
RUBBER_BAND_RESIZE = False
RUBBER_BAND_MOVE = False
INPUT_CURSOR_WIDTH = 1
ENABLE_WAIT_COMMAND = True
ELIDE_AWAY_MSG_IN_USERLIST_CONTEXT = True
ELIDE_HOSTMASK_IN_USERLIST_CONTEXT = True
USERLIST_CONTEXT_MENU = True
HOSTMASK_FETCH_FREQUENCY = 5
DO_NOT_SHOW_SERVER_IN_TITLE = False
SHOW_CONNECTIONS_IN_SYSTRAY_MENU = True
SHOW_SETTINGS_IN_SYSTRAY_MENU = True
SHOW_DIRECTORIES_IN_SYSTRAY_MENU = True
SHOW_LINKS_IN_SYSTRAY_MENU = True
SHOW_LIST_IN_SYSTRAY_MENU = True
SHOW_LOGS_IN_SYSTRAY_MENU = True
SHOW_LOGS_IN_WINDOWS_MENU = True
DELAY_AUTO_RECONNECTION = False
RECONNECTION_DELAY = 30
AUTOCOMPLETE_USER = True
ENABLE_USER_COMMAND = True
IRC_MAX_PAYLOAD_LENGTH = 400
FLOOD_PROTECTION_FOR_LONG_MESSAGES = True
SEARCH_INSTALL_DIRECTORY_FOR_FILES = False
AUTOCOMPLETE_MACROS = True
ELIDE_LONG_NICKNAMES_IN_CHAT_DISPLAY = True
DISPLAY_FULL_USER_INFO_IN_MODE_MESSAGES = True
DISPLAY_LONG_MESSAGE_INDICATOR = True
CURSOR_BLINK = True
REJECT_ALL_CHANNEL_NOTICES = False
CURSOR_BLINK_RATE = 1060
HOTKEYS = {}
EXECUTE_HOTKEY_AS_COMMAND = True
ENABLE_HOTKEYS = True
ENABLE_IGNORE = True
DISPLAY_MOTD_AS_RAW_TEXT = False
ENABLE_PLUGINS = True
PLUGIN_INIT = True
PLUGIN_MESSAGE = True
PLUGIN_NOTICE = True
PLUGIN_ACTION = True
PLUGIN_LEFT = True
PLUGIN_JOINED = True
PLUGIN_PART = True
PLUGIN_JOIN = True
PLUGIN_KICK = True
PLUGIN_KICKED = True
PLUGIN_TICK = True
PLUGIN_MODE = True
PLUGIN_UNMODE = True
PLUGIN_QUIT = True
PLUGIN_IN = True
PLUGIN_OUT = True
PLUGIN_AWAY = True
PLUGIN_BACK = True
PLUGIN_ACTIVATE = True
PLUGIN_INVITE = True
PLUGIN_RENAME = True
PLUGIN_TOPIC = True
PLUGIN_CONNECTED = True
PLUGIN_CONNECTING = True
PLUGIN_LOST = True
PLUGIN_CTICK = True
PLUGIN_NICK = True
PLUGIN_DISCONNECT = True
PLUGIN_PING = True
PLUGIN_MOTD = True
ENABLE_PLUGIN_EDITOR = True
PLUGIN_SERVER = True
PLUGIN_SUBWINDOW = True
PLUGIN_CLOSE = True
PLUGIN_ME = True
PLUGIN_ERROR = True
PYTHON_AUTOINDENT = True
PYTHON_SHOW_WHITESPACE = False
EDITOR_WORDWRAP = False
OVERWRITE_PLUGINS_ON_IMPORT = False
DEFAULT_PYTHON_INDENT = "    "
AUTOCOMPLETE_METHODS = True
ENABLE_CALL_COMMAND = True
IMPORT_SCRIPTS_IN_PLUGINS = True
NO_ENVIRONMENT_IN_CTCP_REPLIES = False
DO_NOT_REPLY_TO_CTCP_VERSION = False
DO_NOT_REPLY_TO_CTCP_SOURCE = False
PLUGIN_ISUPPORT = True
DOUBLECLICK_NICK_DISPLAY = True
PLUGIN_HAS_CONSOLE_MARKER = ":left_speech_bubble:"
SHOW_LUSER_INFO_IN_CURRENT_WINDOW = False
SHOW_ISON_INFO_IN_CURRENT_WINDOW = False
PLUGIN_ISON = True
BAD_NICKNAME_FALLBACK = 'Guest'
WINDOWBAR_SHOW_UNREAD_MENTIONS = False
AUTO_RELOAD_ON_CLOSE = False
DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS = True
DRAG_AND_DROP_MAIN_APPLICATION = True
MANAGERS_ALWAYS_ON_TOP = True
SCRIPT_THREAD_QUIT_TIMEOUT = 1000
PRINT_SCRIPT_ERRORS_TO_STDOUT = False
SAVE_CONNECTION_HISTORY = True
UNKNOWN_NETWORK_NAME = "Unknown"
WINDOWBAR_TOPIC_IN_TOOLTIP = False
EXECUTE_INIT_ON_PLUGIN_RELOAD = True
CLEAR_PLUGINS_FROM_MEMORY_ON_RELOAD = True
RELOAD_PLUGINS_AFTER_UNINSTALL = True
PLUGIN_UNINSTALL = True
PLUGIN_UNLOAD = True
SHOW_PLUGIN_CONSOLE_ON_CREATION = False
ENABLE_MARKDOWN_MARKUP = True
ENABLE_ASCIIMOJI_SHORTCODES = True
ENABLE_IRC_COLOR_MARKUP = True
PLUGIN_UPTIME = True
ENABLE_BROWSER_COMMAND = True
SHOW_TOPIC_IN_EDITOR_TOOLTIP = True
NOTIFY_ON_REPEATED_FAILED_RECONNECTIONS = True
IRC_COLOR_IN_TOPICS = True
CLOSE_EDITOR_ON_UNINSTALL = True
PLUGIN_PAUSE = True
PLUGIN_UNPAUSE = True
SHOW_TIPS_AT_START = True
MAXIMUM_FONT_SIZE_FOR_SETTINGS = 12
FLASH_SYSTRAY_CHANNEL = True
DISPLAY_IRC_ERRORS_IN_CURRENT_WINDOW = True
ALLOW_TOPIC_EDIT = True
USERLIST_WIDTH_IN_CHARACTERS = 15
SHOW_CONNECTION_SCRIPT_IN_WINDOWS_MENU = True
SHOW_ALL_SERVER_ERRORS = False

def build_settings():
	settings = {
		"display_all_server_errors": SHOW_ALL_SERVER_ERRORS,
		"show_connection_script_in_windows_menu": SHOW_CONNECTION_SCRIPT_IN_WINDOWS_MENU,
		"userlist_width_in_characters": USERLIST_WIDTH_IN_CHARACTERS,
		"enable_topic_editor": ALLOW_TOPIC_EDIT,
		"display_server_errors_in_current_window": DISPLAY_IRC_ERRORS_IN_CURRENT_WINDOW,
		"systray_notification_channel": FLASH_SYSTRAY_CHANNEL,
		"maximum_font_size_for_settings_dialog": MAXIMUM_FONT_SIZE_FOR_SETTINGS,
		"show_tips_at_startup": SHOW_TIPS_AT_START,
		"enable_plugin_pause_event": PLUGIN_PAUSE,
		"enable_plugin_unpause_event": PLUGIN_UNPAUSE,
		"close_editor_on_plugin_uninstall": CLOSE_EDITOR_ON_UNINSTALL,
		"display_irc_colors_in_topics": IRC_COLOR_IN_TOPICS,
		"notify_on_repeated_failed_reconnections": NOTIFY_ON_REPEATED_FAILED_RECONNECTIONS,
		"show_channel_topic_in_tooltip": SHOW_TOPIC_IN_EDITOR_TOOLTIP,
		"enable_browser_command": ENABLE_BROWSER_COMMAND,
		"enable_plugin_uptime_event": PLUGIN_UPTIME,
		"enable_irc_color_markup": ENABLE_IRC_COLOR_MARKUP,
		"enable_asciimoji_shortcodes": ENABLE_ASCIIMOJI_SHORTCODES,
		"enable_markdown_markup": ENABLE_MARKDOWN_MARKUP,
		"show_plugin_consoles_on_creation": SHOW_PLUGIN_CONSOLE_ON_CREATION,
		"enable_plugin_unload_event": PLUGIN_UNLOAD,
		"enable_plugin_uninstall_event": PLUGIN_UNINSTALL,
		"reload_plugins_after_uninstall": RELOAD_PLUGINS_AFTER_UNINSTALL,
		"clear_plugins_from_memory_on_reload": CLEAR_PLUGINS_FROM_MEMORY_ON_RELOAD,
		"execute_init_event_on_plugin_reload": EXECUTE_INIT_ON_PLUGIN_RELOAD,
		"windowbar_channel_topic_in_tooltip": WINDOWBAR_TOPIC_IN_TOOLTIP,
		"unknown_network_name": UNKNOWN_NETWORK_NAME,
		"save_connection_history": SAVE_CONNECTION_HISTORY,
		"print_script_errors_to_stdout": PRINT_SCRIPT_ERRORS_TO_STDOUT,
		"script_thread_quit_timeout": SCRIPT_THREAD_QUIT_TIMEOUT,
		"managers_always_on_top": MANAGERS_ALWAYS_ON_TOP,
		"enable_application_drag_and_drop": DRAG_AND_DROP_MAIN_APPLICATION,
		"display_messagebox_on_plugin_error": DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS,
		"reload_plugins_on_editor_close": AUTO_RELOAD_ON_CLOSE,
		"windowbar_show_unread_mentions": WINDOWBAR_SHOW_UNREAD_MENTIONS,
		"bad_nickname_fallback": BAD_NICKNAME_FALLBACK,
		"enable_plugin_ison_event": PLUGIN_ISON,
		"show_ison_response_in_current_window": SHOW_ISON_INFO_IN_CURRENT_WINDOW,
		"show_lusers_response_in_current_window": SHOW_LUSER_INFO_IN_CURRENT_WINDOW,
		"plugin_manager_console_icon": PLUGIN_HAS_CONSOLE_MARKER,
		"doubleclick_nick_display_to_change_nick": DOUBLECLICK_NICK_DISPLAY,
		"enable_plugin_isupport_event": PLUGIN_ISUPPORT,
		"do_not_reply_to_ctcp_source": DO_NOT_REPLY_TO_CTCP_SOURCE,
		"do_not_reply_to_ctcp_version": DO_NOT_REPLY_TO_CTCP_VERSION,
		"do_not_show_environment_in_ctcp_version": NO_ENVIRONMENT_IN_CTCP_REPLIES,
		"import_scripts_in_plugin_packages": IMPORT_SCRIPTS_IN_PLUGINS,
		"enable_call_command": ENABLE_CALL_COMMAND,
		"autocomplete_methods": AUTOCOMPLETE_METHODS,
		"default_python_indentation": DEFAULT_PYTHON_INDENT,
		"overwrite_files_on_plugin_import": OVERWRITE_PLUGINS_ON_IMPORT,
		"editor_word_wrap": EDITOR_WORDWRAP,
		"python_editor_auto_indent": PYTHON_AUTOINDENT,
		"python_editor_show_whitespace": PYTHON_SHOW_WHITESPACE,
		"enable_plugin_error_event": PLUGIN_ERROR,
		"enable_plugin_me_event": PLUGIN_ME,
		"enable_plugin_close_event": PLUGIN_CLOSE,
		"enable_plugin_subwindow_event": PLUGIN_SUBWINDOW,
		"enable_plugin_server_event": PLUGIN_SERVER,
		"enable_plugin_editor": ENABLE_PLUGIN_EDITOR,
		"enable_plugin_motd_event": PLUGIN_MOTD,
		"enable_plugin_ping_event": PLUGIN_PING,
		"enable_plugin_disconnect_event": PLUGIN_DISCONNECT,
		"enable_plugin_nick_event": PLUGIN_NICK,
		"enable_plugin_ctick_event": PLUGIN_CTICK,
		"enable_plugin_lost_event": PLUGIN_LOST,
		"enable_plugin_connected_event": PLUGIN_CONNECTED,
		"enable_plugin_connecting_event": PLUGIN_CONNECTING,
		"enable_plugin_topic_event": PLUGIN_TOPIC,
		"enable_plugin_rename_event": PLUGIN_RENAME,
		"enable_plugin_invite_event": PLUGIN_INVITE,
		"enable_plugin_activate_event": PLUGIN_ACTIVATE,
		"enable_plugin_away_event": PLUGIN_AWAY,
		"enable_plugin_back_event": PLUGIN_BACK,
		"enable_plugin_line_in_event": PLUGIN_IN,
		"enable_plugin_line_out_event": PLUGIN_OUT,
		"enable_plugin_quit_event": PLUGIN_QUIT,
		"enable_plugin_mode_event": PLUGIN_MODE,
		"enable_plugin_unmode_event": PLUGIN_UNMODE,
		"enable_plugin_kick_event": PLUGIN_KICK,
		"enable_plugin_kicked_event": PLUGIN_KICKED,
		"enable_plugin_tick_event": PLUGIN_TICK,
		"enable_plugin_part_event": PLUGIN_PART,
		"enable_plugin_join_event": PLUGIN_JOIN,
		"enable_plugin_left_event": PLUGIN_LEFT,
		"enable_plugin_joined_event": PLUGIN_JOINED,
		"enable_plugin_init_event": PLUGIN_INIT,
		"enable_plugin_message_event": PLUGIN_MESSAGE,
		"enable_plugin_notice_event": PLUGIN_NOTICE,
		"enable_plugin_action_event": PLUGIN_ACTION,
		"enable_plugins": ENABLE_PLUGINS,
		"display_server_motd_as_raw_text": DISPLAY_MOTD_AS_RAW_TEXT,
		"enable_ignore": ENABLE_IGNORE,
		"enable_hotkeys": ENABLE_HOTKEYS,
		"execute_hotkey_as_command": EXECUTE_HOTKEY_AS_COMMAND,
		"hotkeys": HOTKEYS,
		"cursor_blink_rate": CURSOR_BLINK_RATE,
		"reject_all_channel_notices": REJECT_ALL_CHANNEL_NOTICES,
		"cursor_blink": CURSOR_BLINK,
		"show_long_message_indicator": DISPLAY_LONG_MESSAGE_INDICATOR,
		"display_full_user_info_in_mode_messages": DISPLAY_FULL_USER_INFO_IN_MODE_MESSAGES,
		"elide_long_nicknames_in_chat_display": ELIDE_LONG_NICKNAMES_IN_CHAT_DISPLAY,
		"autocomplete_macros": AUTOCOMPLETE_MACROS,
		"search_install_directory_for_files": SEARCH_INSTALL_DIRECTORY_FOR_FILES,
		"flood_protection_for_sending_long_messages": FLOOD_PROTECTION_FOR_LONG_MESSAGES,
		"chat_message_max_length": IRC_MAX_PAYLOAD_LENGTH,
		"enable_user_command": ENABLE_USER_COMMAND,
		"autocomplete_user_settings": AUTOCOMPLETE_USER,
		"delay_automatic_reconnection": DELAY_AUTO_RECONNECTION,
		"automatic_reconnection_timer": RECONNECTION_DELAY,
		"show_network_logs_in_windows_menu": SHOW_LOGS_IN_WINDOWS_MENU,
		"show_channel_list_in_systray_menu": SHOW_LIST_IN_SYSTRAY_MENU,
		"show_network_logs_in_systray_menu": SHOW_LOGS_IN_SYSTRAY_MENU,
		"show_connections_in_systray_menu": SHOW_CONNECTIONS_IN_SYSTRAY_MENU,
		"show_settings_in_systray_menu": SHOW_SETTINGS_IN_SYSTRAY_MENU,
		"show_directories_in_systray_menu": SHOW_DIRECTORIES_IN_SYSTRAY_MENU,
		"show_links_in_systray_menu": SHOW_LINKS_IN_SYSTRAY_MENU,
		"do_not_show_server_name_in_application_title": DO_NOT_SHOW_SERVER_IN_TITLE,
		"fetch_hostmask_frequency": HOSTMASK_FETCH_FREQUENCY,
		"enable_userlist_context_menu": USERLIST_CONTEXT_MENU,
		"elide_hostmask_in_userlist_context_menu": ELIDE_HOSTMASK_IN_USERLIST_CONTEXT,
		"elide_away_message_in_userlist_context_menu": ELIDE_AWAY_MSG_IN_USERLIST_CONTEXT,
		"enable_wait_command": ENABLE_WAIT_COMMAND,
		"input_widget_cursor_width": INPUT_CURSOR_WIDTH,
		"rubberband_subwindow_move": RUBBER_BAND_MOVE,
		"rubberband_subwindow_resize": RUBBER_BAND_RESIZE,
		"subwindow_order": SET_SUBWINDOW_ORDER,
		"show_app_full_screen": SHOW_FULL_SCREEN,
		"write_outgoing_private_messages_to_current_window": WRITE_OUTGOING_PRIVATE_MESSAGES_TO_CURRENT_WINDOW,
		"enable_if_command": ENABLE_IF_COMMAND,
		"enable_goto_command": ENABLE_GOTO_COMMAND,
		"syntax_operator_color": SYNTAX_OPERATOR_COLOR,
		"syntax_operator_style": SYNTAX_OPERATOR_STYLE,
		"enable_built_in_aliases": ENABLE_BUILT_IN_ALIASES,
		"menubar_bold_on_hover": MENUBAR_HOVER_EFFECT,
		"windowbar_bold_active_window": WINDOWBAR_BOLD_ACTIVE_WINDOW,
		"windobar_include_readme": WINDOWBAR_INCLUDE_README,
		"hide_windowbar_if_empty": HIDE_WINDOWBAR_IF_EMPTY,
		"escape_html_in_print_and_prints_messages": ESCAPE_HTML_FROM_RAW_SYSTEM_MESSAGE,
		"display_error_message_for_restrict_and_only_violation": DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION,
		"enable_config_command": ENABLE_CONFIG_COMMAND,
		"autocomplete_settings": AUTOCOMPLETE_SETTINGS,
		"syntax_script_only_color": SYNTAX_SCRIPT_COLOR,
		"syntax_script_only_style": SYNTAX_SCRIPT_STYLE,
		"show_hidden_private_windows_in_windowbar": SHOW_HIDDEN_PRIVATE_WINDOWS_IN_WINDOWBAR,
		"show_hidden_channel_windows_in_windowbar": SHOW_HIDDEN_CHANNEL_WINDOWS_IN_WINDOWBAR,
		"show_channel_name_in_subwindow_title": SHOW_CHANNEL_NAME_IN_SUBWINDOW_TITLE,
		"maximize_subwindows_on_creation": MAXIMIZE_SUBWINDOWS_ON_CREATION,
		"autocomplete_filenames": AUTOCOMPLETE_FILENAMES,
		"doubleclick_userlist_to_open_private_chat": DOUBLECLICK_TO_OPEN_PRIVATE_CHAT,
		"windowbar_show_connecting_server_windows_in_italics": WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS,
		"enable_delay_command": ENABLE_DELAY_COMMAND,
		"hide_server_windows_when_registration_completes": HIDE_SERVER_WINDOWS_ON_SIGNON,
		"show_hidden_server_windows_in_windowbar": SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR,
		"prompt_for_file_on_calling_script_with_no_arguments": PROMPT_FOR_SCRIPT_FILE,
		"show_connection_dialog_on_startup": ASK_FOR_SERVER_ON_STARTUP,
		"hide_logo_on_initial_connection_dialog": HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG,
		"interpolate_aliases_into_quit_message": INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE,
		"interpolate_aliases_into_away_message": INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE,
		"display_dates_in_logs": SHOW_DATES_IN_LOGS,
		"log_channel_notice": LOG_CHANNEL_NOTICE,
		"enable_insert_command": ENABLE_INSERT_COMMAND,
		"require_exact_argument_count_for_usage": REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS,
		"halt_script_execution_on_error": HALT_SCRIPT_EXECUTION_ON_ERROR,
		"create_window_for_incoming_private_notices": CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES,
		"do_not_create_private_chat_windows_for_ignored_users": DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS,
		"include_script_command_shortcut": INCLUDE_SCRIPT_COMMAND_SHORTCUT,
		"windowbar_entry_context_menu": WINDOWBAR_ENTRY_MENU,
		"windowbar_unread_message_animation_length": WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH,
		"windowbar_show_unread_messages": WINDOWBAR_SHOW_UNREAD_MESSAGES,
		"maximum_insert_file_depth": MAXIMUM_INSERT_DEPTH,
		"show_ignore_status_in_userlists": SHOW_IGNORE_STATUS_IN_USERLISTS,
		"closing_server_window_disconnects_from_server": CLOSING_SERVER_WINDOW_DISCONNECTS,
		"display_server_pings_in_server_window": SHOW_PINGS_IN_CONSOLE,
		"enable_scripting": SCRIPTING_ENGINE_ENABLED,
		"spellcheck_in_color": SHOW_MISSPELLED_WORDS_IN_COLOR,
		"spellcheck_in_strikeout": SHOW_MISSPELLED_WORDS_IN_STRIKEOUT,
		"spellcheck_underline_color": SPELLCHECK_UNDERLINE_COLOR,
		"spellcheck_in_italics": SHOW_MISSPELLED_WORDS_IN_ITALICS,
		"spellcheck_in_bold": SHOW_MISSPELLED_WORDS_IN_BOLD,
		"show_spellcheck_settings_in_menus": ALLOW_MENUS_TO_CHANGE_SPELLCHECK_SETTINGS,
		"show_user_count_display": SHOW_USER_COUNT_DISPLAY,
		"editor_syntax_highlighting": EDITOR_USES_SYNTAX_HIGHLIGHTING,
		"do_not_allow_select_on_userlist": USERLIST_ITEMS_NON_SELECTABLE,
		"ignored_users": IGNORE_LIST,
		"windowbar_include_log_manager": WINDOWBAR_INCLUDE_MANAGER,
		"do_not_pad_nickname_in_chat_display": STRIP_NICKNAME_PADDING_FROM_DISPLAY,
		"show_script_execution_errors": DISPLAY_SCRIPT_ERRORS,
		"enable_style_editor": ENABLE_STYLE_EDITOR,
		"enable_autocomplete": ENABLE_AUTOCOMPLETE,
		"enable_aliases": ENABLE_ALIASES,
		"show_status_bar_on_editor_windows": SHOW_STATUS_BAR_ON_EDITOR_WINDOWS,
		"autocomplete_shortcodes_in_quit_message_widget": AUTOCOMPLETE_SHORTCODES_IN_QUIT_MESSAGE_WIDGET,
		"write_network_input_and_output_to_file": WRITE_INPUT_AND_OUTPUT_TO_FILE,
		"write_network_input_and_output_to_console": WRITE_INPUT_AND_OUTPUT_TO_CONSOLE,
		"emoji_shortcode_language": EMOJI_LANGUAGE,
		"show_channel_mode_menu": SHOW_CHANNEL_MENU,
		"enable_command_history": ENABLE_COMMAND_INPUT_HISTORY,
		"log_channel_nickname_changes": LOG_CHANNEL_NICKNAME_CHANGE,
		"spellchecker_distance": SPELLCHECKER_DISTANCE,
		"twisted_irc_client_heartbeat": TWISTED_CLIENT_HEARTBEAT,
		"log_channel_quits": LOG_CHANNEL_QUIT,
		"log_channel_joins": LOG_CHANNEL_JOIN,
		"log_channel_parts": LOG_CHANNEL_PART,
		"log_channel_topics": LOG_CHANNEL_TOPICS,
		"log_absolutely_all_messages_of_any_type": LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE,
		"click_systray_icon_to_minimize_to_tray": CLICK_SYSTRAY_ICON_TO_MINIMIZE_TO_TRAY,
		"doubleclick_to_restore_from_systray": DOUBLECLICK_TO_RESTORE_WINDOW_FROM_SYSTRAY,
		"autocomplete_shortcodes_in_away_message_widget": AUTOCOMPLETE_SHORTCODES_IN_AWAY_MESSAGE_WIDGET,
		"app_interaction_cancels_autoaway": APP_INTERACTION_CANCELS_AUTOAWAY,
		"window_interaction_cancels_autoaway": WINDOW_INTERACTION_CANCELS_AUTOAWAY,
		"typing_input_cancels_autoaway": TYPING_INPUT_CANCELS_AUTOAWAY,
		"do_not_apply_styles_to_text": DO_NOT_APPLY_STYLES_TO_TEXT,
		"create_window_for_outgoing_private_messages": CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES,
		"prompt_for_away_message": PROMPT_FOR_AWAY_MESSAGE,
		"autoaway": USE_AUTOAWAY,
		"autoaway_time": AUTOAWAY_TIME,
		"away_message": DEFAULT_AWAY_MESSAGE,
		"show_away_status_in_nick_display": SHOW_AWAY_STATUS_IN_NICK_DISPLAY,
		"show_away_status_in_userlists": SHOW_AWAY_STATUS_IN_USERLISTS,
		"show_away_and_back_messages": SHOW_AWAY_AND_BACK_MESSAGES,
		"hide_horizontal_scrollbar_on_userlists": HIDE_USERLIST_HORIZONTAL_SCROLLBAR,
		"syntax_nickname_color": SYNTAX_NICKNAME_COLOR,
		"syntax_nickname_style": SYNTAX_NICKNAME_STYLE,
		"syntax_shortcode_color": SYNTAX_EMOJI_COLOR,
		"syntax_shortcode_style": SYNTAX_EMOJI_STYLE,
		"apply_syntax_highlighting_to_input_widget": APPLY_SYNTAX_STYLES_TO_INPUT_WIDGET,
		"do_not_show_application_name_in_title": DO_NOT_SHOW_APPLICATION_NAME_IN_TITLE,
		"do_not_apply_text_style_to_userlist": DO_NOT_APPLY_STYLE_TO_USERLIST,
		"do_not_apply_text_style_to_input_widget": DO_NOT_APPLY_STYLE_TO_INPUT_WIDGET,
		"show_channel_topic_in_title": SHOW_CHANNEL_TOPIC_IN_APPLICATION_TITLE,
		"windowbar_bold_on_hover": WINDOWBAR_HOVER_EFFECT,
		"windowbar_underline_active_window": WINDOWBAR_UNDERLINE_ACTIVE_WINDOW,
		"show_status_bar_on_list_windows": SHOW_STATUS_BAR_ON_LIST_WINDOWS,
		"show_channel_list_button_on_server_windows": SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS,
		"show_server_window_toolbar": SHOW_SERVER_WINDOW_TOOLBAR,
		"show_list_refresh_button_on_server_windows": SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS,
		"show_server_information_in_windows_menu": SHOW_SERVER_INFO_IN_WINDOWS_MENU,
		"closing_main_window_minimizes_to_tray": CLOSING_WINDOW_MINIMIZES_TO_TRAY,
		"search_for_all_terms_in_channel_list_search": SEARCH_ALL_TERMS_IN_CHANNEL_LIST,
		"show_channel_list_entry_in_windows_menu": SHOW_CHANNEL_LIST_IN_WINDOWS_MENU,
		"windowbar_include_channel_lists": WINDOWBAR_INCLUDE_LIST,
		"examine_topic_in_channel_list_search": EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH,
		"request_channel_list_on_connection": REQUEST_CHANNEL_LIST_ON_CONNECTION,
		"interpolate_aliases_into_user_input": INTERPOLATE_ALIASES_INTO_INPUT,
		"autocomplete_aliases": AUTOCOMPLETE_ALIAS,
		"ask_before_exit": ASK_BEFORE_CLOSE,
		"main_window_always_on_top": ALWAYS_ON_TOP,
		"force_all_windows_to_use_default_style": FORCE_DEFAULT_STYLE,
		"sound_notification_nickname": SOUND_NOTIFICATION_NICKNAME,
		"sound_notification_disconnect": SOUND_NOTIFICATION_DISCONNECT,
		"sound_notification_private": SOUND_NOTIFICATION_PRIVATE,
		"sound_notification_kick": SOUND_NOTIFICATION_KICK,
		"sound_notification_invite": SOUND_NOTIFICATION_INVITE,
		"sound_notification_notice": SOUND_NOTIFICATION_NOTICE,
		"sound_notification_mode": SOUND_NOTIFICATION_MODE,
		"sound_notification_file": SOUND_NOTIFICATION_FILE,
		"sound_notifications": SOUND_NOTIFICATIONS,
		"display_nick_on_server_windows": DISPLAY_NICK_ON_SERVER_WINDOWS,
		"show_links_to_known_irc_networks": SHOW_LINKS_TO_NETWORK_WEBPAGES,
		"show_status_bar_on_server_windows": SHOW_STATUS_BAR_ON_SERVER_WINDOWS,
		"show_status_bar_on_chat_windows": SHOW_STATUS_BAR_ON_CHAT_WINDOWS,
		"application_font": APPLICATION_FONT,
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
		"quit_message": DEFAULT_QUIT_MESSAGE,
		"default_spellcheck_language": DEFAULT_SPELLCHECK_LANGUAGE,
		"system_message_prefix": SYSTEM_MESSAGE_PREFIX,
		"display_irc_colors": DISPLAY_IRC_COLORS,
		"convert_urls_to_links": CONVERT_URLS_TO_LINKS,
		"autocomplete_commands": AUTOCOMPLETE_COMMANDS,
		"autocomplete_nicks": AUTOCOMPLETE_NICKS,
		"autocomplete_shortcodes": AUTOCOMPLETE_SHORTCODES,
		"maximum_loaded_log_size": MAXIMUM_LOADED_LOG_SIZE,
		"mark_end_of_loaded_log": MARK_END_OF_LOADED_LOG,
		"save_channel_logs": SAVE_CHANNEL_LOGS,
		"load_channel_logs": LOAD_CHANNEL_LOGS,
		"save_private_logs": SAVE_PRIVATE_LOGS,
		"load_private_logs": LOAD_PRIVATE_LOGS,
		"ask_before_disconnect": ASK_BEFORE_DISCONNECT,
		"interface_button_size": INTERFACE_BUTTON_SIZE,
		"interface_button_icon_size": INTERFACE_BUTTON_ICON_SIZE,
		"show_connection_uptime": SHOW_CONNECTION_UPTIME,
		"show_channel_uptime": SHOW_CHANNEL_UPTIME,
		"scroll_chat_to_bottom_on_resize": SCROLL_CHAT_TO_BOTTOM_ON_RESIZE,
		"enable_emoji_shortcodes": ENABLE_EMOJI_SHORTCODES,
		"enable_spellcheck": ENABLE_SPELLCHECK,
		"ask_before_reconnect": ASK_BEFORE_RECONNECT,
		"notify_on_lost_or_failed_connection": NOTIFY_ON_LOST_OR_FAILED_CONNECTION,
		"always_scroll_to_bottom": ALWAYS_SCROLL_TO_BOTTOM,
		"prompt_on_failed_connection": PROMPT_ON_FAILED_CONNECTION,
		"display_active_subwindow_in_title": DISPLAY_ACTIVE_SUBWINDOW_IN_TITLE,
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
		"show_channel_topic_bar": SHOW_CHANNEL_TOPIC,
		"show_channel_topic_in_window_title": SHOW_CHANNEL_TOPIC_IN_WINDOW_TITLE,
		"show_channel_name_and_modes": SHOW_CHANNEL_NAME_AND_MODES,
		"show_channel_banlist_menu": SHOW_BANLIST_MENU,
		"show_userlists": SHOW_USERLIST,
		"show_input_menu": SHOW_INPUT_MENU,
		"show_windowbar": SHOW_WINDOWBAR,
		"windowbar_on_top": WINDOWBAR_TOP_OF_SCREEN,
		"windowbar_include_servers": WINDOWBAR_INCLUDE_SERVERS,
		"windowbar_justify": WINDOWBAR_JUSTIFY,
		"windowbar_can_float": WINDOWBAR_CAN_FLOAT,
		"windowbar_show_icons": WINDOWBAR_SHOW_ICONS,
		"windowbar_doubleclick_to_maximize": WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED,
		"windowbar_include_editors": WINDOWBAR_INCLUDE_EDITORS,
		"show_chat_context_menu_options": SHOW_CHAT_CONTEXT_MENUS,
		"always_show_current_first_in_windowbar": ALWAYS_SHOW_CURRENT_WINDOW_FIRST,
		"menubar_justify": MENUBAR_JUSTIFY,
		"show_menubar_context_menu": MENUBAR_MENU,
		"show_windowbar_context_menu": WINDOWBAR_MENU,
		"main_menu_irc_name": MAIN_MENU_IRC_NAME,
		"main_menu_tools_name": MAIN_MENU_TOOLS_NAME,
		"main_menu_windows_name": MAIN_MENU_WINDOWS_NAME,
		"main_menu_help_name": MAIN_MENU_HELP_NAME,
		"dark_mode": DARK_MODE,
		"simplified_dialogs": SIMPLIFIED_DIALOGS,
		"editor_prompt_save_on_close": EDITOR_PROMPT_SAVE,
		"windowbar_include_channels": WINDOWBAR_INCLUDE_CHANNELS,
		"windowbar_include_private": WINDOWBAR_INCLUDE_PRIVATE,
		"auto_join_on_invite": JOIN_ON_INVITE,
		"get_hostmasks_on_channel_join": GET_HOSTMASKS_ON_CHANNEL_JOIN,
		"main_menu_settings_name": MAIN_MENU_SETTINGS_NAME,
		"do_intermittent_log_saves": DO_INTERMITTENT_LOG_SAVES,
		"intermittent_log_save_interval": LOG_SAVE_INTERVAL,
		"maximize_app_on_startup": MAXIMIZE_ON_STARTUP,
		"force_monospace_text_rendering": FORCE_MONOSPACE_RENDERING,
	}

	return settings

def patch_settings(settings):
	if not "display_all_server_errors" in settings:
		settings["display_all_server_errors"] = SHOW_ALL_SERVER_ERRORS
	if not "show_connection_script_in_windows_menu" in settings:
		settings["show_connection_script_in_windows_menu"] = SHOW_CONNECTION_SCRIPT_IN_WINDOWS_MENU
	if not "userlist_width_in_characters" in settings:
		settings["userlist_width_in_characters"] = USERLIST_WIDTH_IN_CHARACTERS
	if not "enable_topic_editor" in settings:
		settings["enable_topic_editor"] = ALLOW_TOPIC_EDIT
	if not "display_server_errors_in_current_window" in settings:
		settings["display_server_errors_in_current_window"] = DISPLAY_IRC_ERRORS_IN_CURRENT_WINDOW
	if not "systray_notification_channel" in settings:
		settings["systray_notification_channel"] = FLASH_SYSTRAY_CHANNEL
	if not "maximum_font_size_for_settings_dialog" in settings:
		settings["maximum_font_size_for_settings_dialog"] = MAXIMUM_FONT_SIZE_FOR_SETTINGS
	if not "show_tips_at_startup" in settings:
		settings["show_tips_at_startup"] = SHOW_TIPS_AT_START
	if not "enable_plugin_pause_event" in settings:
		settings["enable_plugin_pause_event"] = PLUGIN_PAUSE
	if not "enable_plugin_unpause_event" in settings:
		settings["enable_plugin_unpause_event"] = PLUGIN_UNPAUSE
	if not "close_editor_on_plugin_uninstall" in settings:
		settings["close_editor_on_plugin_uninstall"] = CLOSE_EDITOR_ON_UNINSTALL
	if not "display_irc_colors_in_topics" in settings:
		settings["display_irc_colors_in_topics"] = IRC_COLOR_IN_TOPICS
	if not "notify_on_repeated_failed_reconnections" in settings:
		settings["notify_on_repeated_failed_reconnections"] = NOTIFY_ON_REPEATED_FAILED_RECONNECTIONS
	if not "show_channel_topic_in_tooltip" in settings:
		settings["show_channel_topic_in_tooltip"] = SHOW_TOPIC_IN_EDITOR_TOOLTIP
	if not "enable_browser_command" in settings:
		settings["enable_browser_command"] = ENABLE_BROWSER_COMMAND
	if not "enable_plugin_uptime_event" in settings:
		settings["enable_plugin_uptime_event"] = PLUGIN_UPTIME
	if not "enable_irc_color_markup" in settings:
		settings["enable_irc_color_markup"] = ENABLE_IRC_COLOR_MARKUP
	if not "enable_asciimoji_shortcodes" in settings:
		settings["enable_asciimoji_shortcodes"] = ENABLE_ASCIIMOJI_SHORTCODES
	if not "enable_markdown_markup" in settings:
		settings["enable_markdown_markup"] = ENABLE_MARKDOWN_MARKUP
	if not "show_plugin_consoles_on_creation" in settings:
		settings["show_plugin_consoles_on_creation"] = SHOW_PLUGIN_CONSOLE_ON_CREATION
	if not "enable_plugin_unload_event" in settings:
		settings["enable_plugin_unload_event"] = PLUGIN_UNLOAD
	if not "enable_plugin_uninstall_event" in settings:
		settings["enable_plugin_uninstall_event"] = PLUGIN_UNINSTALL
	if not "reload_plugins_after_uninstall" in settings:
		settings["reload_plugins_after_uninstall"] = RELOAD_PLUGINS_AFTER_UNINSTALL
	if not "clear_plugins_from_memory_on_reload" in settings:
		settings["clear_plugins_from_memory_on_reload"] = CLEAR_PLUGINS_FROM_MEMORY_ON_RELOAD
	if not "execute_init_event_on_plugin_reload" in settings:
		settings["execute_init_event_on_plugin_reload"] = EXECUTE_INIT_ON_PLUGIN_RELOAD
	if not "windowbar_channel_topic_in_tooltip" in settings:
		settings["windowbar_channel_topic_in_tooltip"] = WINDOWBAR_TOPIC_IN_TOOLTIP
	if not "unknown_network_name" in settings:
		settings["unknown_network_name"] = UNKNOWN_NETWORK_NAME
	if not "save_connection_history" in settings:
		settings["save_connection_history"] = SAVE_CONNECTION_HISTORY
	if not "print_script_errors_to_stdout" in settings:
		settings["print_script_errors_to_stdout"] = PRINT_SCRIPT_ERRORS_TO_STDOUT
	if not "script_thread_quit_timeout" in settings:
		settings["script_thread_quit_timeout"] = SCRIPT_THREAD_QUIT_TIMEOUT
	if not "managers_always_on_top" in settings:
		settings["managers_always_on_top"] = MANAGERS_ALWAYS_ON_TOP
	if not "enable_application_drag_and_drop" in settings:
		settings["enable_application_drag_and_drop"] = DRAG_AND_DROP_MAIN_APPLICATION
	if not "display_messagebox_on_plugin_error" in settings:
		settings["display_messagebox_on_plugin_error"] = DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS
	if not "reload_plugins_on_editor_close" in settings:
		settings["reload_plugins_on_editor_close"] = AUTO_RELOAD_ON_CLOSE
	if not "windowbar_show_unread_mentions" in settings:
		settings["windowbar_show_unread_mentions"] = WINDOWBAR_SHOW_UNREAD_MENTIONS
	if not "bad_nickname_fallback" in settings:
		settings["bad_nickname_fallback"] = BAD_NICKNAME_FALLBACK
	if not "enable_plugin_ison_event" in settings:
		settings["enable_plugin_ison_event"] = PLUGIN_ISON
	if not "show_ison_response_in_current_window" in settings:
		settings["show_ison_response_in_current_window"] = SHOW_ISON_INFO_IN_CURRENT_WINDOW
	if not "show_lusers_response_in_current_window" in settings:
		settings["show_lusers_response_in_current_window"] = SHOW_LUSER_INFO_IN_CURRENT_WINDOW
	if not "plugin_manager_console_icon" in settings:
		settings["plugin_manager_console_icon"] = PLUGIN_HAS_CONSOLE_MARKER
	if not "doubleclick_nick_display_to_change_nick" in settings:
		settings["doubleclick_nick_display_to_change_nick"] = DOUBLECLICK_NICK_DISPLAY
	if not "enable_plugin_isupport_event" in settings:
		settings["enable_plugin_isupport_event"] = PLUGIN_ISUPPORT
	if not "do_not_reply_to_ctcp_source" in settings:
		settings["do_not_reply_to_ctcp_source"] = DO_NOT_REPLY_TO_CTCP_SOURCE
	if not "do_not_reply_to_ctcp_version" in settings:
		settings["do_not_reply_to_ctcp_version"] = DO_NOT_REPLY_TO_CTCP_VERSION
	if not "do_not_show_environment_in_ctcp_version" in settings:
		settings["do_not_show_environment_in_ctcp_version"] = NO_ENVIRONMENT_IN_CTCP_REPLIES
	if not "import_scripts_in_plugin_packages" in settings:
		settings["import_scripts_in_plugin_packages"] = IMPORT_SCRIPTS_IN_PLUGINS
	if not "enable_call_command" in settings:
		settings["enable_call_command"] = ENABLE_CALL_COMMAND
	if not "autocomplete_methods" in settings:
		settings["autocomplete_methods"] = AUTOCOMPLETE_METHODS
	if not "default_python_indentation" in settings:
		settings["default_python_indentation"] = DEFAULT_PYTHON_INDENT
	if not "overwrite_files_on_plugin_import" in settings:
		settings["overwrite_files_on_plugin_import"] = OVERWRITE_PLUGINS_ON_IMPORT
	if not "editor_word_wrap" in settings:
		settings["editor_word_wrap"] = EDITOR_WORDWRAP
	if not "python_editor_auto_indent" in settings:
		settings["python_editor_auto_indent"] = PYTHON_AUTOINDENT
	if not "python_editor_show_whitespace" in settings:
		settings["python_editor_show_whitespace"] = PYTHON_SHOW_WHITESPACE
	if not "enable_plugin_error_event" in settings:
		settings["enable_plugin_error_event"] = PLUGIN_ERROR
	if not "enable_plugin_me_event" in settings:
		settings["enable_plugin_me_event"] = PLUGIN_ME
	if not "enable_plugin_close_event" in settings:
		settings["enable_plugin_close_event"] = PLUGIN_CLOSE
	if not "enable_plugin_subwindow_event" in settings:
		settings["enable_plugin_subwindow_event"] = PLUGIN_SUBWINDOW
	if not "enable_plugin_server_event" in settings:
		settings["enable_plugin_server_event"] = PLUGIN_SERVER
	if not "enable_plugin_editor" in settings:
		settings["enable_plugin_editor"] = ENABLE_PLUGIN_EDITOR
	if not "enable_plugin_motd_event" in settings:
		settings["enable_plugin_motd_event"] = PLUGIN_MOTD
	if not "enable_plugin_ping_event" in settings:
		settings["enable_plugin_ping_event"] = PLUGIN_PING
	if not "enable_plugin_disconnect_event" in settings:
		settings["enable_plugin_disconnect_event"] = PLUGIN_DISCONNECT
	if not "enable_plugin_nick_event" in settings:
		settings["enable_plugin_nick_event"] = PLUGIN_NICK
	if not "enable_plugin_ctick_event" in settings:
		settings["enable_plugin_ctick_event"] = PLUGIN_CTICK
	if not "enable_plugin_lost_event" in settings:
		settings["enable_plugin_lost_event"] = PLUGIN_LOST
	if not "enable_plugin_connected_event" in settings:
		settings["enable_plugin_connected_event"] = PLUGIN_CONNECTED
	if not "enable_plugin_connecting_event" in settings:
		settings["enable_plugin_connecting_event"] = PLUGIN_CONNECTING
	if not "enable_plugin_topic_event" in settings:
		settings["enable_plugin_topic_event"] = PLUGIN_TOPIC
	if not "enable_plugin_rename_event" in settings:
		settings["enable_plugin_rename_event"] = PLUGIN_RENAME
	if not "enable_plugin_invite_event" in settings:
		settings["enable_plugin_invite_event"] = PLUGIN_INVITE
	if not "enable_plugin_activate_event" in settings:
		settings["enable_plugin_activate_event"] = PLUGIN_ACTIVATE
	if not "enable_plugin_away_event" in settings:
		settings["enable_plugin_away_event"] = PLUGIN_AWAY
	if not "enable_plugin_back_event" in settings:
		settings["enable_plugin_back_event"] = PLUGIN_BACK
	if not "enable_plugin_line_in_event" in settings:
		settings["enable_plugin_line_in_event"] = PLUGIN_IN
	if not "enable_plugin_line_out_event" in settings:
		settings["enable_plugin_line_out_event"] = PLUGIN_OUT
	if not "enable_plugin_quit_event" in settings:
		settings["enable_plugin_quit_event"] = PLUGIN_QUIT
	if not "enable_plugin_mode_event" in settings:
		settings["enable_plugin_mode_event"] = PLUGIN_MODE
	if not "enable_plugin_unmode_event" in settings:
		settings["enable_plugin_unmode_event"] = PLUGIN_UNMODE
	if not "enable_plugin_kick_event" in settings:
		settings["enable_plugin_kick_event"] = PLUGIN_KICK
	if not "enable_plugin_kicked_event" in settings:
		settings["enable_plugin_kicked_event"] = PLUGIN_KICKED
	if not "enable_plugin_tick_event" in settings:
		settings["enable_plugin_tick_event"] = PLUGIN_TICK
	if not "enable_plugin_part_event" in settings:
		settings["enable_plugin_part_event"] = PLUGIN_PART
	if not "enable_plugin_join_event" in settings:
		settings["enable_plugin_join_event"] = PLUGIN_JOIN
	if not "enable_plugin_left_event" in settings:
		settings["enable_plugin_left_event"] = PLUGIN_LEFT
	if not "enable_plugin_joined_event" in settings:
		settings["enable_plugin_joined_event"] = PLUGIN_JOINED
	if not "enable_plugin_init_event" in settings:
		settings["enable_plugin_init_event"] = PLUGIN_INIT
	if not "enable_plugin_message_event" in settings:
		settings["enable_plugin_message_event"] = PLUGIN_MESSAGE
	if not "enable_plugin_notice_event" in settings:
		settings["enable_plugin_notice_event"] = PLUGIN_NOTICE
	if not "enable_plugin_action_event" in settings:
		settings["enable_plugin_action_event"] = PLUGIN_ACTION
	if not "enable_plugins" in settings:
		settings["enable_plugins"] = ENABLE_PLUGINS
	if not "display_server_motd_as_raw_text" in settings:
		settings["display_server_motd_as_raw_text"] = DISPLAY_MOTD_AS_RAW_TEXT
	if not "enable_ignore" in settings:
		settings["enable_ignore"] = ENABLE_IGNORE
	if not "enable_hotkeys" in settings:
		settings["enable_hotkeys"] = ENABLE_HOTKEYS
	if not "execute_hotkey_as_command" in settings:
		settings["execute_hotkey_as_command"] = EXECUTE_HOTKEY_AS_COMMAND
	if not "hotkeys" in settings:
		settings["hotkeys"] = HOTKEYS
	if not "cursor_blink_rate" in settings:
		settings["cursor_blink_rate"] = CURSOR_BLINK_RATE
	if not "reject_all_channel_notices" in settings:
		settings["reject_all_channel_notices"] = REJECT_ALL_CHANNEL_NOTICES
	if not "cursor_blink" in settings:
		settings["cursor_blink"] = CURSOR_BLINK
	if not "show_long_message_indicator" in settings:
		settings["show_long_message_indicator"] = DISPLAY_LONG_MESSAGE_INDICATOR
	if not "display_full_user_info_in_mode_messages" in settings:
		settings["display_full_user_info_in_mode_messages"] = DISPLAY_FULL_USER_INFO_IN_MODE_MESSAGES
	if not "elide_long_nicknames_in_chat_display" in settings:
		settings["elide_long_nicknames_in_chat_display"] = ELIDE_LONG_NICKNAMES_IN_CHAT_DISPLAY
	if not "autocomplete_macros" in settings:
		settings["autocomplete_macros"] = AUTOCOMPLETE_MACROS
	if not "search_install_directory_for_files" in settings:
		settings["search_install_directory_for_files"] = SEARCH_INSTALL_DIRECTORY_FOR_FILES
	if not "flood_protection_for_sending_long_messages" in settings:
		settings["flood_protection_for_sending_long_messages"] = FLOOD_PROTECTION_FOR_LONG_MESSAGES
	if not "chat_message_max_length" in settings:
		settings["chat_message_max_length"] = IRC_MAX_PAYLOAD_LENGTH
	if not "enable_user_command" in settings:
		settings["enable_user_command"] = ENABLE_USER_COMMAND
	if not "autocomplete_user_settings" in settings:
		settings["autocomplete_user_settings"] = AUTOCOMPLETE_USER
	if not "delay_automatic_reconnection" in settings:
		settings["delay_automatic_reconnection"] = DELAY_AUTO_RECONNECTION
	if not "automatic_reconnection_timer" in settings:
		settings["automatic_reconnection_timer"] = RECONNECTION_DELAY
	if not "show_network_logs_in_windows_menu" in settings:
		settings["show_network_logs_in_windows_menu"] = SHOW_LOGS_IN_WINDOWS_MENU
	if not "show_channel_list_in_systray_menu" in settings:
		settings["show_channel_list_in_systray_menu"] = SHOW_LIST_IN_SYSTRAY_MENU
	if not "show_network_logs_in_systray_menu" in settings:
		settings["show_network_logs_in_systray_menu"] = SHOW_LOGS_IN_SYSTRAY_MENU
	if not "show_connections_in_systray_menu" in settings:
		settings["show_connections_in_systray_menu"] = SHOW_CONNECTIONS_IN_SYSTRAY_MENU
	if not "show_settings_in_systray_menu" in settings:
		settings["show_settings_in_systray_menu"] = SHOW_SETTINGS_IN_SYSTRAY_MENU
	if not "show_directories_in_systray_menu" in settings:
		settings["show_directories_in_systray_menu"] = SHOW_DIRECTORIES_IN_SYSTRAY_MENU
	if not "show_links_in_systray_menu" in settings:
		settings["show_links_in_systray_menu"] = SHOW_LINKS_IN_SYSTRAY_MENU
	if not "do_not_show_server_name_in_application_title" in settings:
		settings["do_not_show_server_name_in_application_title"] = DO_NOT_SHOW_SERVER_IN_TITLE
	if not "fetch_hostmask_frequency" in settings:
		settings["fetch_hostmask_frequency"] = HOSTMASK_FETCH_FREQUENCY
	if not "enable_userlist_context_menu" in settings:
		settings["enable_userlist_context_menu"] = USERLIST_CONTEXT_MENU
	if not "elide_hostmask_in_userlist_context_menu" in settings:
		settings["elide_hostmask_in_userlist_context_menu"] = ELIDE_HOSTMASK_IN_USERLIST_CONTEXT
	if not "elide_away_message_in_userlist_context_menu" in settings:
		settings["elide_away_message_in_userlist_context_menu"] = ELIDE_AWAY_MSG_IN_USERLIST_CONTEXT
	if not "enable_wait_command" in settings:
		settings["enable_wait_command"] = ENABLE_WAIT_COMMAND
	if not "input_widget_cursor_width" in settings:
		settings["input_widget_cursor_width"] = INPUT_CURSOR_WIDTH
	if not "rubberband_subwindow_move" in settings:
		settings["rubberband_subwindow_move"] = RUBBER_BAND_MOVE
	if not "rubberband_subwindow_resize" in settings:
		settings["rubberband_subwindow_resize"] = RUBBER_BAND_RESIZE
	if not "subwindow_order" in settings:
		settings["subwindow_order"] = SET_SUBWINDOW_ORDER
	if not "show_app_full_screen" in settings:
		settings["show_app_full_screen"] = SHOW_FULL_SCREEN
	if not "write_outgoing_private_messages_to_current_window" in settings:
		settings["write_outgoing_private_messages_to_current_window"] = WRITE_OUTGOING_PRIVATE_MESSAGES_TO_CURRENT_WINDOW
	if not "enable_if_command" in settings:
		settings["enable_if_command"] = ENABLE_IF_COMMAND
	if not "enable_goto_command" in settings:
		settings["enable_goto_command"] = ENABLE_GOTO_COMMAND
	if not "syntax_operator_color" in settings:
		settings["syntax_operator_color"] = SYNTAX_OPERATOR_COLOR
	if not "syntax_operator_style" in settings:
		settings["syntax_operator_style"] = SYNTAX_OPERATOR_STYLE
	if not "enable_built_in_aliases" in settings:
		settings["enable_built_in_aliases"] = ENABLE_BUILT_IN_ALIASES
	if not "menubar_bold_on_hover" in settings:
		settings["menubar_bold_on_hover"] = MENUBAR_HOVER_EFFECT
	if not "windowbar_bold_active_window" in settings:
		settings["windowbar_bold_active_window"] = WINDOWBAR_BOLD_ACTIVE_WINDOW
	if not "windobar_include_readme" in settings:
		settings["windobar_include_readme"] = WINDOWBAR_INCLUDE_README
	if not "hide_windowbar_if_empty" in settings:
		settings["hide_windowbar_if_empty"] = HIDE_WINDOWBAR_IF_EMPTY
	if not "escape_html_in_print_and_prints_messages" in settings:
		settings["escape_html_in_print_and_prints_messages"] = ESCAPE_HTML_FROM_RAW_SYSTEM_MESSAGE
	if not "display_error_message_for_restrict_and_only_violation" in settings:
		settings["display_error_message_for_restrict_and_only_violation"] = DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION
	if not "enable_config_command" in settings:
		settings["enable_config_command"] = ENABLE_CONFIG_COMMAND
	if not "autocomplete_settings" in settings:
		settings["autocomplete_settings"] = AUTOCOMPLETE_SETTINGS
	if not "syntax_script_only_color" in settings:
		settings["syntax_script_only_color"] = SYNTAX_SCRIPT_COLOR
	if not "syntax_script_only_style" in settings:
			settings["syntax_script_only_style"] = SYNTAX_SCRIPT_STYLE
	if not "show_hidden_private_windows_in_windowbar" in settings:
		settings["show_hidden_private_windows_in_windowbar"] = SHOW_HIDDEN_PRIVATE_WINDOWS_IN_WINDOWBAR
	if not "show_hidden_channel_windows_in_windowbar" in settings:
		settings["show_hidden_channel_windows_in_windowbar"] = SHOW_HIDDEN_CHANNEL_WINDOWS_IN_WINDOWBAR
	if not "show_channel_name_in_subwindow_title" in settings:
		settings["show_channel_name_in_subwindow_title"] = SHOW_CHANNEL_NAME_IN_SUBWINDOW_TITLE
	if not "maximize_subwindows_on_creation" in settings:
		settings["maximize_subwindows_on_creation"] = MAXIMIZE_SUBWINDOWS_ON_CREATION
	if not "autocomplete_filenames" in settings:
		settings["autocomplete_filenames"] = AUTOCOMPLETE_FILENAMES
	if not "doubleclick_userlist_to_open_private_chat" in settings:
		settings["doubleclick_userlist_to_open_private_chat"] = DOUBLECLICK_TO_OPEN_PRIVATE_CHAT
	if not "windowbar_show_connecting_server_windows_in_italics" in settings:
		settings["windowbar_show_connecting_server_windows_in_italics"] = WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS
	if not "enable_delay_command" in settings:
		settings["enable_delay_command"] = ENABLE_DELAY_COMMAND
	if not "hide_server_windows_when_registration_completes" in settings:
		settings["hide_server_windows_when_registration_completes"] = HIDE_SERVER_WINDOWS_ON_SIGNON
	if not "show_hidden_server_windows_in_windowbar" in settings:
		settings["show_hidden_server_windows_in_windowbar"] = SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR
	if not "prompt_for_file_on_calling_script_with_no_arguments" in settings:
		settings["prompt_for_file_on_calling_script_with_no_arguments"] = PROMPT_FOR_SCRIPT_FILE
	if not "show_connection_dialog_on_startup" in settings:
		settings["show_connection_dialog_on_startup"] = ASK_FOR_SERVER_ON_STARTUP
	if not "hide_logo_on_initial_connection_dialog" in settings:
		settings["hide_logo_on_initial_connection_dialog"] = HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG
	if not "interpolate_aliases_into_quit_message" in settings:
		settings["interpolate_aliases_into_quit_message"] = INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE
	if not "interpolate_aliases_into_away_message" in settings:
		settings["interpolate_aliases_into_away_message"] = INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE
	if not "display_dates_in_logs" in settings:
		settings["display_dates_in_logs"] = SHOW_DATES_IN_LOGS
	if not "log_channel_notice" in settings:
		settings["log_channel_notice"] = LOG_CHANNEL_NOTICE
	if not "enable_insert_command" in settings:
		settings["enable_insert_command"] = ENABLE_INSERT_COMMAND
	if not "require_exact_argument_count_for_usage" in settings:
		settings["require_exact_argument_count_for_usage"] = REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS
	if not "halt_script_execution_on_error" in settings:
		settings["halt_script_execution_on_error"] = HALT_SCRIPT_EXECUTION_ON_ERROR
	if not "create_window_for_incoming_private_notices" in settings:
		settings["create_window_for_incoming_private_notices"] = CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES
	if not "do_not_create_private_chat_windows_for_ignored_users" in settings:
		settings["do_not_create_private_chat_windows_for_ignored_users"] = DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS
	if not "include_script_command_shortcut" in settings:
		settings["include_script_command_shortcut"] = INCLUDE_SCRIPT_COMMAND_SHORTCUT
	if not "windowbar_entry_context_menu" in settings:
		settings["windowbar_entry_context_menu"] = WINDOWBAR_ENTRY_MENU
	if not "windowbar_unread_message_animation_length" in settings:
		settings["windowbar_unread_message_animation_length"] = WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH
	if not "windowbar_show_unread_messages" in settings:
		settings["windowbar_show_unread_messages"] = WINDOWBAR_SHOW_UNREAD_MESSAGES
	if not "maximum_insert_file_depth" in settings:
		settings["maximum_insert_file_depth"] = MAXIMUM_INSERT_DEPTH
	if not "show_ignore_status_in_userlists" in settings:
		settings["show_ignore_status_in_userlists"] = SHOW_IGNORE_STATUS_IN_USERLISTS
	if not "closing_server_window_disconnects_from_server" in settings:
		settings["closing_server_window_disconnects_from_server"] = CLOSING_SERVER_WINDOW_DISCONNECTS
	if not "display_server_pings_in_server_window" in settings:
		settings["display_server_pings_in_server_window"] = SHOW_PINGS_IN_CONSOLE
	if not "enable_scripting" in settings:
		settings["enable_scripting"] = SCRIPTING_ENGINE_ENABLED
	if not "spellcheck_in_color" in settings:
		settings["spellcheck_in_color"] = SHOW_MISSPELLED_WORDS_IN_COLOR
	if not "spellcheck_in_strikeout" in settings:
		settings["spellcheck_in_strikeout"] = SHOW_MISSPELLED_WORDS_IN_STRIKEOUT
	if not "spellcheck_underline_color" in settings:
		settings["spellcheck_underline_color"] = SPELLCHECK_UNDERLINE_COLOR
	if not "spellcheck_in_italics" in settings:
		settings["spellcheck_in_italics"] = SHOW_MISSPELLED_WORDS_IN_ITALICS
	if not "spellcheck_in_bold" in settings:
		settings["spellcheck_in_bold"] = SHOW_MISSPELLED_WORDS_IN_BOLD
	if not "show_spellcheck_settings_in_menus" in settings:
		settings["show_spellcheck_settings_in_menus"] = ALLOW_MENUS_TO_CHANGE_SPELLCHECK_SETTINGS
	if not "show_user_count_display" in settings:
		settings["show_user_count_display"] = SHOW_USER_COUNT_DISPLAY
	if not "editor_syntax_highlighting" in settings:
		settings["editor_syntax_highlighting"] = EDITOR_USES_SYNTAX_HIGHLIGHTING
	if not "do_not_allow_select_on_userlist" in settings:
		settings["do_not_allow_select_on_userlist"] = USERLIST_ITEMS_NON_SELECTABLE
	if not "ignored_users" in settings:
		settings["ignored_users"] = IGNORE_LIST
	if not "windowbar_include_log_manager" in settings:
		settings["windowbar_include_log_manager"] = WINDOWBAR_INCLUDE_MANAGER
	if not "do_not_pad_nickname_in_chat_display" in settings:
		settings["do_not_pad_nickname_in_chat_display"] = STRIP_NICKNAME_PADDING_FROM_DISPLAY
	if not "show_script_execution_errors" in settings:
		settings["show_script_execution_errors"] = DISPLAY_SCRIPT_ERRORS
	if not "enable_style_editor" in settings:
		settings["enable_style_editor"] = ENABLE_STYLE_EDITOR
	if not "enable_autocomplete" in settings:
		settings["enable_autocomplete"] = ENABLE_AUTOCOMPLETE
	if not "enable_aliases" in settings:
		settings["enable_aliases"] = ENABLE_ALIASES
	if not "show_status_bar_on_editor_windows" in settings:
		settings["show_status_bar_on_editor_windows"] = SHOW_STATUS_BAR_ON_EDITOR_WINDOWS
	if not "autocomplete_shortcodes_in_quit_message_widget" in settings:
		settings["autocomplete_shortcodes_in_quit_message_widget"] = AUTOCOMPLETE_SHORTCODES_IN_QUIT_MESSAGE_WIDGET
	if not "write_network_input_and_output_to_file" in settings:
		settings["write_network_input_and_output_to_file"] = WRITE_INPUT_AND_OUTPUT_TO_FILE
	if not "write_network_input_and_output_to_console" in settings:
		settings["write_network_input_and_output_to_console"] = WRITE_INPUT_AND_OUTPUT_TO_CONSOLE
	if not "emoji_shortcode_language" in settings:
		settings["emoji_shortcode_language"] = EMOJI_LANGUAGE
	if not "show_channel_mode_menu" in settings:
		settings["show_channel_mode_menu"] = SHOW_CHANNEL_MENU
	if not "enable_command_history" in settings:
		settings["enable_command_history"] = ENABLE_COMMAND_INPUT_HISTORY
	if not "log_channel_nickname_changes" in settings:
		settings["log_channel_nickname_changes"] = LOG_CHANNEL_NICKNAME_CHANGE
	if not "spellchecker_distance" in settings:
		settings["spellchecker_distance"] = SPELLCHECKER_DISTANCE
	if not "twisted_irc_client_heartbeat" in settings:
		settings["twisted_irc_client_heartbeat"] = TWISTED_CLIENT_HEARTBEAT
	if not "log_channel_quits" in settings:
		settings["log_channel_quits"] = LOG_CHANNEL_QUIT
	if not "log_channel_joins" in settings:
		settings["log_channel_joins"] = LOG_CHANNEL_JOIN
	if not "log_channel_parts" in settings:
		settings["log_channel_parts"] = LOG_CHANNEL_PART
	if not "log_channel_topics" in settings:
		settings["log_channel_topics"] = LOG_CHANNEL_TOPICS
	if not "log_absolutely_all_messages_of_any_type" in settings:
		settings["log_absolutely_all_messages_of_any_type"] = LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE
	if not "click_systray_icon_to_minimize_to_tray" in settings:
		settings["click_systray_icon_to_minimize_to_tray"] = CLICK_SYSTRAY_ICON_TO_MINIMIZE_TO_TRAY
	if not "doubleclick_to_restore_from_systray" in settings:
		settings["doubleclick_to_restore_from_systray"] = DOUBLECLICK_TO_RESTORE_WINDOW_FROM_SYSTRAY
	if not "autocomplete_shortcodes_in_away_message_widget" in settings:
		settings["autocomplete_shortcodes_in_away_message_widget"] = AUTOCOMPLETE_SHORTCODES_IN_AWAY_MESSAGE_WIDGET
	if not "app_interaction_cancels_autoaway" in settings:
		settings["app_interaction_cancels_autoaway"] = APP_INTERACTION_CANCELS_AUTOAWAY
	if not "window_interaction_cancels_autoaway" in settings:
		settings["window_interaction_cancels_autoaway"] = WINDOW_INTERACTION_CANCELS_AUTOAWAY
	if not "typing_input_cancels_autoaway" in settings:
		settings["typing_input_cancels_autoaway"] = TYPING_INPUT_CANCELS_AUTOAWAY
	if not "do_not_apply_styles_to_text" in settings:
		settings["do_not_apply_styles_to_text"] = DO_NOT_APPLY_STYLES_TO_TEXT
	if not "create_window_for_outgoing_private_messages" in settings:
		settings["create_window_for_outgoing_private_messages"] = CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES
	if not "prompt_for_away_message" in settings:
		settings["prompt_for_away_message"] = PROMPT_FOR_AWAY_MESSAGE
	if not "autoaway" in settings:
		settings["autoaway"] = USE_AUTOAWAY
	if not "autoaway_time" in settings:
		settings["autoaway_time"] = AUTOAWAY_TIME
	if not "away_message" in settings:
		settings["away_message"] = DEFAULT_AWAY_MESSAGE
	if not "show_away_status_in_nick_display" in settings:
		settings["show_away_status_in_nick_display"] = SHOW_AWAY_STATUS_IN_NICK_DISPLAY
	if not "show_away_status_in_userlists" in settings:
		settings["show_away_status_in_userlists"] = SHOW_AWAY_STATUS_IN_USERLISTS
	if not "show_away_and_back_messages" in settings:
		settings["show_away_and_back_messages"] = SHOW_AWAY_AND_BACK_MESSAGES
	if not "hide_horizontal_scrollbar_on_userlists" in settings:
		settings["hide_horizontal_scrollbar_on_userlists"] = HIDE_USERLIST_HORIZONTAL_SCROLLBAR
	if not "syntax_nickname_color" in settings:
		settings["syntax_nickname_color"] = SYNTAX_NICKNAME_COLOR
	if not "syntax_nickname_style" in settings:
		settings["syntax_nickname_style"] = SYNTAX_NICKNAME_STYLE
	if not "syntax_shortcode_color" in settings:
		settings["syntax_shortcode_color"] = SYNTAX_EMOJI_COLOR
	if not "syntax_shortcode_style" in settings:
		settings["syntax_shortcode_style"] = SYNTAX_EMOJI_STYLE
	if not "apply_syntax_highlighting_to_input_widget" in settings:
		settings["apply_syntax_highlighting_to_input_widget"] = APPLY_SYNTAX_STYLES_TO_INPUT_WIDGET
	if not "do_not_show_application_name_in_title" in settings:
		settings["do_not_show_application_name_in_title"] = DO_NOT_SHOW_APPLICATION_NAME_IN_TITLE
	if not "do_not_apply_text_style_to_userlist" in settings:
		settings["do_not_apply_text_style_to_userlist"] = DO_NOT_APPLY_STYLE_TO_USERLIST
	if not "do_not_apply_text_style_to_input_widget" in settings:
		settings["do_not_apply_text_style_to_input_widget"] = DO_NOT_APPLY_STYLE_TO_INPUT_WIDGET
	if not "show_channel_topic_in_title" in settings:
		settings["show_channel_topic_in_title"] = SHOW_CHANNEL_TOPIC_IN_APPLICATION_TITLE
	if not "windowbar_bold_on_hover" in settings:
		settings["windowbar_bold_on_hover"] = WINDOWBAR_HOVER_EFFECT
	if not "windowbar_underline_active_window" in settings:
		settings["windowbar_underline_active_window"] = WINDOWBAR_UNDERLINE_ACTIVE_WINDOW
	if not "show_status_bar_on_list_windows" in settings:
		settings["show_status_bar_on_list_windows"] = SHOW_STATUS_BAR_ON_LIST_WINDOWS
	if not "show_channel_list_button_on_server_windows" in settings:
		settings["show_channel_list_button_on_server_windows"] = SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS
	if not "show_server_window_toolbar" in settings:
		settings["show_server_window_toolbar"] = SHOW_SERVER_WINDOW_TOOLBAR
	if not "show_list_refresh_button_on_server_windows" in settings:
		settings["show_list_refresh_button_on_server_windows"] = SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS
	if not "show_server_information_in_windows_menu" in settings:
		settings["show_server_information_in_windows_menu"] = SHOW_SERVER_INFO_IN_WINDOWS_MENU
	if not "closing_main_window_minimizes_to_tray" in settings:
		settings["closing_main_window_minimizes_to_tray"] = CLOSING_WINDOW_MINIMIZES_TO_TRAY
	if not "search_for_all_terms_in_channel_list_search" in settings:
		settings["search_for_all_terms_in_channel_list_search"] = SEARCH_ALL_TERMS_IN_CHANNEL_LIST
	if not "show_channel_list_entry_in_windows_menu" in settings:
		settings["show_channel_list_entry_in_windows_menu"] = SHOW_CHANNEL_LIST_IN_WINDOWS_MENU
	if not "windowbar_include_channel_lists" in settings:
		settings["windowbar_include_channel_lists"] = WINDOWBAR_INCLUDE_LIST
	if not "examine_topic_in_channel_list_search" in settings:
		settings["examine_topic_in_channel_list_search"] = EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH
	if not "request_channel_list_on_connection" in settings:
		settings["request_channel_list_on_connection"] = REQUEST_CHANNEL_LIST_ON_CONNECTION
	if not "interpolate_aliases_into_user_input" in settings:
		settings["interpolate_aliases_into_user_input"] = INTERPOLATE_ALIASES_INTO_INPUT
	if not "autocomplete_aliases" in settings:
		settings["autocomplete_aliases"] = AUTOCOMPLETE_ALIAS
	if not "ask_before_exit" in settings:
		settings["ask_before_exit"] = ASK_BEFORE_CLOSE
	if not "main_window_always_on_top" in settings:
		settings["main_window_always_on_top"] = ALWAYS_ON_TOP
	if not "force_all_windows_to_use_default_style" in settings:
		settings["force_all_windows_to_use_default_style"] = FORCE_DEFAULT_STYLE
	if not "sound_notification_notice" in settings:
		settings["sound_notification_notice"] = SOUND_NOTIFICATION_INVITE
	if not "sound_notification_mode" in settings:
		settings["sound_notification_mode"] = SOUND_NOTIFICATION_MODE
	if not "sound_notification_nickname" in settings:
		settings["sound_notification_nickname"] = SOUND_NOTIFICATION_NICKNAME
	if not "sound_notification_disconnect" in settings:
		settings["sound_notification_disconnect"] = SOUND_NOTIFICATION_DISCONNECT
	if not "sound_notification_private" in settings:
		settings["sound_notification_private"] = SOUND_NOTIFICATION_PRIVATE
	if not "sound_notification_kick" in settings:
		settings["sound_notification_kick"] = SOUND_NOTIFICATION_KICK
	if not "sound_notification_invite" in settings:
		settings["sound_notification_invite"] = SOUND_NOTIFICATION_NOTICE
	if not "sound_notification_file" in settings:
		settings["sound_notification_file"] = SOUND_NOTIFICATION_FILE
	if not "sound_notifications" in settings:
		settings["sound_notifications"] = SOUND_NOTIFICATIONS
	if not "display_nick_on_server_windows" in settings:
		settings["display_nick_on_server_windows"] = DISPLAY_NICK_ON_SERVER_WINDOWS
	if not "show_links_to_known_irc_networks" in settings:
		settings["show_links_to_known_irc_networks"] = SHOW_LINKS_TO_NETWORK_WEBPAGES
	if not "show_status_bar_on_server_windows" in settings:
		settings["show_status_bar_on_server_windows"] = SHOW_STATUS_BAR_ON_SERVER_WINDOWS
	if not "show_status_bar_on_chat_windows" in settings:
		settings["show_status_bar_on_chat_windows"] = SHOW_STATUS_BAR_ON_CHAT_WINDOWS
	if not "do_intermittent_log_saves" in settings:
		settings["do_intermittent_log_saves"] = DO_INTERMITTENT_LOG_SAVES
	if not "intermittent_log_save_interval" in settings:
		settings["intermittent_log_save_interval"] = LOG_SAVE_INTERVAL
	if not "main_menu_settings_name" in settings:
		settings["main_menu_settings_name"] = MAIN_MENU_SETTINGS_NAME
	if not "get_hostmasks_on_channel_join" in settings:
		settings["get_hostmasks_on_channel_join"] = GET_HOSTMASKS_ON_CHANNEL_JOIN
	if not "auto_join_on_invite" in settings:
		settings["auto_join_on_invite"] = JOIN_ON_INVITE
	if not "windowbar_include_private" in settings:
		settings["windowbar_include_private"] = WINDOWBAR_INCLUDE_PRIVATE
	if not "windowbar_include_channels" in settings:
		settings["windowbar_include_channels"] = WINDOWBAR_INCLUDE_CHANNELS
	if not "editor_prompt_save_on_close" in settings:
		settings["editor_prompt_save_on_close"] = EDITOR_PROMPT_SAVE
	if not "simplified_dialogs" in settings:
		settings["simplified_dialogs"] = SIMPLIFIED_DIALOGS
	if not "dark_mode" in settings:
		settings["dark_mode"] = DARK_MODE
	if not "main_menu_irc_name" in settings:
		settings["main_menu_irc_name"] = MAIN_MENU_IRC_NAME
	if not "main_menu_tools_name" in settings:
		settings["main_menu_tools_name"] = MAIN_MENU_TOOLS_NAME
	if not "main_menu_windows_name" in settings:
		settings["main_menu_windows_name"] = MAIN_MENU_WINDOWS_NAME
	if not "main_menu_help_name" in settings:
		settings["main_menu_help_name"] = MAIN_MENU_HELP_NAME
	if not "show_menubar_context_menu" in settings:
		settings["show_menubar_context_menu"] = MENUBAR_MENU
	if not "show_windowbar_context_menu" in settings:
		settings["show_windowbar_context_menu"] = WINDOWBAR_MENU
	if not "menubar_justify" in settings:
		settings["menubar_justify"] = MENUBAR_JUSTIFY
	if not "always_show_current_first_in_windowbar" in settings:
		settings["always_show_current_first_in_windowbar"] = ALWAYS_SHOW_CURRENT_WINDOW_FIRST
	if not "show_chat_context_menu_options" in settings:
		settings["show_chat_context_menu_options"] = SHOW_CHAT_CONTEXT_MENUS
	if not "windowbar_include_editors" in settings:
		settings["windowbar_include_editors"] = WINDOWBAR_INCLUDE_EDITORS
	if not "windowbar_doubleclick_to_maximize" in settings:
		settings["windowbar_doubleclick_to_maximize"] = WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED
	if not "windowbar_show_icons" in settings:
		settings["windowbar_show_icons"] = WINDOWBAR_SHOW_ICONS
	if not "show_windowbar" in settings:
		settings["show_windowbar"] = SHOW_WINDOWBAR
	if not "windowbar_on_top" in settings:
		settings["windowbar_on_top"] = WINDOWBAR_TOP_OF_SCREEN
	if not "windowbar_include_servers" in settings:
		settings["windowbar_include_servers"] = WINDOWBAR_INCLUDE_SERVERS
	if not "windowbar_justify" in settings:
		settings["windowbar_justify"] = WINDOWBAR_JUSTIFY
	if not "windowbar_can_float" in settings:
		settings["windowbar_can_float"] = WINDOWBAR_CAN_FLOAT
	if not "show_input_menu" in settings:
		settings["show_input_menu"] = SHOW_INPUT_MENU
	if not "show_userlists" in settings:
		settings["show_userlists"] = SHOW_USERLIST
	if not "show_channel_name_and_modes" in settings:
		settings["show_channel_name_and_modes"] = SHOW_CHANNEL_NAME_AND_MODES
	if not "show_channel_banlist_menu" in settings:
		settings["show_channel_banlist_menu"] = SHOW_BANLIST_MENU
	if not "show_channel_topic_in_window_title" in settings:
		settings["show_channel_topic_in_window_title"] = SHOW_CHANNEL_TOPIC_IN_WINDOW_TITLE
	if not "show_channel_topic_bar" in settings:
		settings["show_channel_topic_bar"] = SHOW_CHANNEL_TOPIC
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
	if not "display_active_subwindow_in_title" in settings:
		settings["display_active_subwindow_in_title"] = DISPLAY_ACTIVE_SUBWINDOW_IN_TITLE
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
	if not "interface_button_size" in settings:
		settings["interface_button_size"] = INTERFACE_BUTTON_SIZE
	if not "interface_button_icon_size" in settings:
		settings["interface_button_icon_size"] = INTERFACE_BUTTON_ICON_SIZE
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
	if not "application_font" in settings:
		settings["application_font"] = APPLICATION_FONT
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
	if not "quit_message" in settings:
		settings["quit_message"] = DEFAULT_QUIT_MESSAGE
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
	if not "autocomplete_shortcodes" in settings:
		settings["autocomplete_shortcodes"] = AUTOCOMPLETE_SHORTCODES
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
	if not "maximize_app_on_startup" in settings:
		settings["maximize_app_on_startup"] = MAXIMIZE_ON_STARTUP
	if not "force_monospace_text_rendering" in settings:
		settings["force_monospace_text_rendering"] = FORCE_MONOSPACE_RENDERING

	return settings

def load_settings(filename):
	global APPLICATION_FONT
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
	global AUTOCOMPLETE_SHORTCODES
	global MAXIMUM_LOADED_LOG_SIZE
	global MARK_END_OF_LOADED_LOG
	global SAVE_CHANNEL_LOGS
	global LOAD_CHANNEL_LOGS
	global SAVE_PRIVATE_LOGS
	global LOAD_PRIVATE_LOGS
	global ASK_BEFORE_DISCONNECT
	global INTERFACE_BUTTON_SIZE
	global INTERFACE_BUTTON_ICON_SIZE
	global SHOW_CONNECTION_UPTIME
	global SHOW_CHANNEL_UPTIME
	global SCROLL_CHAT_TO_BOTTOM_ON_RESIZE
	global ENABLE_EMOJI_SHORTCODES
	global ENABLE_SPELLCHECK
	global ASK_BEFORE_RECONNECT
	global NOTIFY_ON_LOST_OR_FAILED_CONNECTION
	global ALWAYS_SCROLL_TO_BOTTOM
	global PROMPT_ON_FAILED_CONNECTION
	global DISPLAY_ACTIVE_SUBWINDOW_IN_TITLE
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
	global SHOW_CHANNEL_TOPIC
	global SHOW_CHANNEL_TOPIC_IN_WINDOW_TITLE
	global SHOW_CHANNEL_NAME_AND_MODES
	global SHOW_BANLIST_MENU
	global SHOW_USERLIST
	global SHOW_INPUT_MENU
	global SHOW_WINDOWBAR
	global WINDOWBAR_TOP_OF_SCREEN
	global WINDOWBAR_INCLUDE_SERVERS
	global WINDOWBAR_JUSTIFY
	global WINDOWBAR_CAN_FLOAT
	global WINDOWBAR_SHOW_ICONS
	global WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED
	global WINDOWBAR_INCLUDE_EDITORS
	global SHOW_CHAT_CONTEXT_MENUS
	global ALWAYS_SHOW_CURRENT_WINDOW_FIRST
	global MENUBAR_JUSTIFY
	global MENUBAR_MENU
	global WINDOWBAR_MENU
	global MAIN_MENU_IRC_NAME
	global MAIN_MENU_TOOLS_NAME
	global MENUBAR_MENU
	global MAIN_MENU_HELP_NAME
	global DARK_MODE
	global SIMPLIFIED_DIALOGS
	global EDITOR_PROMPT_SAVE
	global WINDOWBAR_INCLUDE_CHANNELS
	global WINDOWBAR_INCLUDE_PRIVATE
	global JOIN_ON_INVITE
	global GET_HOSTMASKS_ON_CHANNEL_JOIN
	global MAIN_MENU_SETTINGS_NAME
	global DO_INTERMITTENT_LOG_SAVES
	global LOG_SAVE_INTERVAL
	global SHOW_STATUS_BAR_ON_SERVER_WINDOWS
	global SHOW_STATUS_BAR_ON_CHAT_WINDOWS
	global MAXIMIZE_ON_STARTUP
	global SHOW_LINKS_TO_NETWORK_WEBPAGES
	global DISPLAY_NICK_ON_SERVER_WINDOWS
	global SOUND_NOTIFICATION_NICKNAME
	global SOUND_NOTIFICATION_DISCONNECT
	global SOUND_NOTIFICATION_PRIVATE
	global SOUND_NOTIFICATION_KICK
	global SOUND_NOTIFICATION_INVITE
	global SOUND_NOTIFICATION_NOTICE
	global SOUND_NOTIFICATION_MODE
	global SOUND_NOTIFICATION_FILE
	global SOUND_NOTIFICATIONS
	global FORCE_MONOSPACE_RENDERING
	global FORCE_DEFAULT_STYLE
	global ALWAYS_ON_TOP
	global ASK_BEFORE_CLOSE
	global AUTOCOMPLETE_ALIAS
	global INTERPOLATE_ALIASES_INTO_INPUT
	global REQUEST_CHANNEL_LIST_ON_CONNECTION
	global EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH
	global WINDOWBAR_INCLUDE_LIST
	global SHOW_CHANNEL_LIST_IN_WINDOWS_MENU
	global SEARCH_ALL_TERMS_IN_CHANNEL_LIST
	global CLOSING_WINDOW_MINIMIZES_TO_TRAY
	global SHOW_SERVER_INFO_IN_WINDOWS_MENU
	global SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS
	global SHOW_SERVER_WINDOW_TOOLBAR
	global SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS
	global SHOW_STATUS_BAR_ON_LIST_WINDOWS
	global WINDOWBAR_UNDERLINE_ACTIVE_WINDOW
	global WINDOWBAR_HOVER_EFFECT
	global SHOW_CHANNEL_TOPIC_IN_APPLICATION_TITLE
	global DO_NOT_APPLY_STYLE_TO_INPUT_WIDGET
	global DO_NOT_APPLY_STYLE_TO_USERLIST
	global DO_NOT_SHOW_APPLICATION_NAME_IN_TITLE
	global APPLY_SYNTAX_STYLES_TO_INPUT_WIDGET
	global SYNTAX_NICKNAME_COLOR
	global SYNTAX_NICKNAME_STYLE
	global SYNTAX_EMOJI_COLOR
	global SYNTAX_EMOJI_STYLE
	global HIDE_USERLIST_HORIZONTAL_SCROLLBAR
	global SHOW_AWAY_AND_BACK_MESSAGES
	global SHOW_AWAY_STATUS_IN_USERLISTS
	global SHOW_AWAY_STATUS_IN_NICK_DISPLAY
	global DEFAULT_AWAY_MESSAGE
	global USE_AUTOAWAY
	global AUTOAWAY_TIME
	global PROMPT_FOR_AWAY_MESSAGE
	global CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES
	global DO_NOT_APPLY_STYLES_TO_TEXT
	global TYPING_INPUT_CANCELS_AUTOAWAY
	global WINDOW_INTERACTION_CANCELS_AUTOAWAY
	global APP_INTERACTION_CANCELS_AUTOAWAY
	global AUTOCOMPLETE_SHORTCODES_IN_AWAY_MESSAGE_WIDGET
	global DOUBLECLICK_TO_RESTORE_WINDOW_FROM_SYSTRAY
	global CLICK_SYSTRAY_ICON_TO_MINIMIZE_TO_TRAY
	global LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE
	global LOG_CHANNEL_TOPICS
	global LOG_CHANNEL_JOIN
	global LOG_CHANNEL_PART
	global LOG_CHANNEL_QUIT
	global TWISTED_CLIENT_HEARTBEAT
	global SPELLCHECKER_DISTANCE
	global LOG_CHANNEL_NICKNAME_CHANGE
	global ENABLE_COMMAND_INPUT_HISTORY
	global SHOW_CHANNEL_MENU
	global EMOJI_LANGUAGE
	global WRITE_INPUT_AND_OUTPUT_TO_CONSOLE
	global WRITE_INPUT_AND_OUTPUT_TO_FILE
	global AUTOCOMPLETE_SHORTCODES_IN_QUIT_MESSAGE_WIDGET
	global SHOW_STATUS_BAR_ON_EDITOR_WINDOWS
	global ENABLE_ALIASES
	global ENABLE_AUTOCOMPLETE
	global ENABLE_STYLE_EDITOR
	global DISPLAY_SCRIPT_ERRORS
	global STRIP_NICKNAME_PADDING_FROM_DISPLAY
	global WINDOWBAR_INCLUDE_MANAGER
	global IGNORE_LIST
	global USERLIST_ITEMS_NON_SELECTABLE
	global EDITOR_USES_SYNTAX_HIGHLIGHTING
	global SHOW_USER_COUNT_DISPLAY
	global ALLOW_MENUS_TO_CHANGE_SPELLCHECK_SETTINGS
	global SPELLCHECK_UNDERLINE_COLOR
	global SHOW_MISSPELLED_WORDS_IN_ITALICS
	global SHOW_MISSPELLED_WORDS_IN_BOLD
	global SHOW_MISSPELLED_WORDS_IN_STRIKEOUT
	global SHOW_MISSPELLED_WORDS_IN_COLOR
	global SCRIPTING_ENGINE_ENABLED
	global SHOW_PINGS_IN_CONSOLE
	global CLOSING_SERVER_WINDOW_DISCONNECTS
	global SHOW_IGNORE_STATUS_IN_USERLISTS
	global MAXIMUM_INSERT_DEPTH
	global WINDOWBAR_SHOW_UNREAD_MESSAGES
	global WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH
	global WINDOWBAR_ENTRY_MENU
	global INCLUDE_SCRIPT_COMMAND_SHORTCUT
	global DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS
	global CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES
	global HALT_SCRIPT_EXECUTION_ON_ERROR
	global REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS
	global ENABLE_INSERT_COMMAND
	global LOG_CHANNEL_NOTICE
	global SHOW_DATES_IN_LOGS
	global INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE
	global INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE
	global HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG
	global ASK_FOR_SERVER_ON_STARTUP
	global PROMPT_FOR_SCRIPT_FILE
	global SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR
	global HIDE_SERVER_WINDOWS_ON_SIGNON
	global ENABLE_DELAY_COMMAND
	global WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS
	global DOUBLECLICK_TO_OPEN_PRIVATE_CHAT
	global AUTOCOMPLETE_FILENAMES
	global MAXIMIZE_SUBWINDOWS_ON_CREATION
	global SHOW_CHANNEL_NAME_IN_SUBWINDOW_TITLE
	global SHOW_HIDDEN_CHANNEL_WINDOWS_IN_WINDOWBAR
	global SHOW_HIDDEN_PRIVATE_WINDOWS_IN_WINDOWBAR
	global SYNTAX_SCRIPT_COLOR
	global SYNTAX_SCRIPT_STYLE
	global AUTOCOMPLETE_SETTINGS
	global ENABLE_CONFIG_COMMAND
	global DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION
	global ESCAPE_HTML_FROM_RAW_SYSTEM_MESSAGE
	global HIDE_WINDOWBAR_IF_EMPTY
	global WINDOWBAR_INCLUDE_README
	global WINDOWBAR_BOLD_ACTIVE_WINDOW
	global MENUBAR_HOVER_EFFECT
	global ENABLE_BUILT_IN_ALIASES
	global SYNTAX_OPERATOR_COLOR
	global SYNTAX_OPERATOR_STYLE
	global ENABLE_GOTO_COMMAND
	global ENABLE_IF_COMMAND
	global WRITE_OUTGOING_PRIVATE_MESSAGES_TO_CURRENT_WINDOW
	global SHOW_FULL_SCREEN
	global SET_SUBWINDOW_ORDER
	global RUBBER_BAND_RESIZE
	global RUBBER_BAND_MOVE
	global INPUT_CURSOR_WIDTH
	global ENABLE_WAIT_COMMAND
	global ELIDE_AWAY_MSG_IN_USERLIST_CONTEXT
	global ELIDE_HOSTMASK_IN_USERLIST_CONTEXT
	global USERLIST_CONTEXT_MENU
	global HOSTMASK_FETCH_FREQUENCY
	global DO_NOT_SHOW_SERVER_IN_TITLE
	global SHOW_CONNECTIONS_IN_SYSTRAY_MENU
	global SHOW_SETTINGS_IN_SYSTRAY_MENU
	global SHOW_DIRECTORIES_IN_SYSTRAY_MENU
	global SHOW_LINKS_IN_SYSTRAY_MENU
	global SHOW_LIST_IN_SYSTRAY_MENU
	global SHOW_LOGS_IN_SYSTRAY_MENU
	global SHOW_LOGS_IN_WINDOWS_MENU
	global DELAY_AUTO_RECONNECTION
	global RECONNECTION_DELAY
	global AUTOCOMPLETE_USER
	global ENABLE_USER_COMMAND
	global IRC_MAX_PAYLOAD_LENGTH
	global FLOOD_PROTECTION_FOR_LONG_MESSAGES
	global SEARCH_INSTALL_DIRECTORY_FOR_FILES
	global AUTOCOMPLETE_MACROS
	global ELIDE_LONG_NICKNAMES_IN_CHAT_DISPLAY
	global DISPLAY_FULL_USER_INFO_IN_MODE_MESSAGES
	global DISPLAY_LONG_MESSAGE_INDICATOR
	global CURSOR_BLINK
	global REJECT_ALL_CHANNEL_NOTICES
	global CURSOR_BLINK_RATE
	global HOTKEYS
	global EXECUTE_HOTKEY_AS_COMMAND
	global ENABLE_HOTKEYS
	global ENABLE_IGNORE
	global DISPLAY_MOTD_AS_RAW_TEXT
	global ENABLE_PLUGINS
	global PLUGIN_INIT
	global PLUGIN_MESSAGE
	global PLUGIN_NOTICE
	global PLUGIN_ACTION
	global PLUGIN_LEFT
	global PLUGIN_JOINED
	global PLUGIN_PART
	global PLUGIN_JOIN
	global PLUGIN_KICK
	global PLUGIN_KICKED
	global PLUGIN_TICK
	global PLUGIN_MODE
	global PLUGIN_UNMODE
	global PLUGIN_QUIT
	global PLUGIN_IN
	global PLUGIN_OUT
	global PLUGIN_AWAY
	global PLUGIN_BACK
	global PLUGIN_ACTIVATE
	global PLUGIN_INVITE
	global PLUGIN_RENAME
	global PLUGIN_TOPIC
	global PLUGIN_CONNECTED
	global PLUGIN_CONNECTING
	global PLUGIN_LOST
	global PLUGIN_CTICK
	global PLUGIN_NICK
	global PLUGIN_DISCONNECT
	global PLUGIN_PING
	global PLUGIN_MOTD
	global ENABLE_PLUGIN_EDITOR
	global PLUGIN_SERVER
	global PLUGIN_SUBWINDOW
	global PLUGIN_CLOSE
	global PLUGIN_ME
	global PLUGIN_ERROR
	global PYTHON_AUTOINDENT
	global PYTHON_SHOW_WHITESPACE
	global EDITOR_WORDWRAP
	global OVERWRITE_PLUGINS_ON_IMPORT
	global DEFAULT_PYTHON_INDENT
	global AUTOCOMPLETE_METHODS
	global ENABLE_CALL_COMMAND
	global IMPORT_SCRIPTS_IN_PLUGINS
	global NO_ENVIRONMENT_IN_CTCP_REPLIES
	global DO_NOT_REPLY_TO_CTCP_VERSION
	global DO_NOT_REPLY_TO_CTCP_SOURCE
	global PLUGIN_ISUPPORT
	global DOUBLECLICK_NICK_DISPLAY
	global PLUGIN_HAS_CONSOLE_MARKER
	global SHOW_LUSER_INFO_IN_CURRENT_WINDOW
	global SHOW_ISON_INFO_IN_CURRENT_WINDOW
	global PLUGIN_ISON
	global BAD_NICKNAME_FALLBACK
	global WINDOWBAR_SHOW_UNREAD_MENTIONS
	global AUTO_RELOAD_ON_CLOSE
	global DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS
	global DRAG_AND_DROP_MAIN_APPLICATION
	global MANAGERS_ALWAYS_ON_TOP
	global SCRIPT_THREAD_QUIT_TIMEOUT
	global PRINT_SCRIPT_ERRORS_TO_STDOUT
	global SAVE_CONNECTION_HISTORY
	global UNKNOWN_NETWORK_NAME
	global WINDOWBAR_TOPIC_IN_TOOLTIP
	global EXECUTE_INIT_ON_PLUGIN_RELOAD
	global CLEAR_PLUGINS_FROM_MEMORY_ON_RELOAD
	global RELOAD_PLUGINS_AFTER_UNINSTALL
	global PLUGIN_UNINSTALL
	global PLUGIN_UNLOAD
	global SHOW_PLUGIN_CONSOLE_ON_CREATION
	global ENABLE_MARKDOWN_MARKUP
	global ENABLE_ASCIIMOJI_SHORTCODES
	global ENABLE_IRC_COLOR_MARKUP
	global PLUGIN_UPTIME
	global ENABLE_BROWSER_COMMAND
	global SHOW_TOPIC_IN_EDITOR_TOOLTIP
	global NOTIFY_ON_REPEATED_FAILED_RECONNECTIONS
	global IRC_COLOR_IN_TOPICS
	global CLOSE_EDITOR_ON_UNINSTALL
	global PLUGIN_PAUSE
	global PLUGIN_UNPAUSE
	global SHOW_TIPS_AT_START
	global MAXIMUM_FONT_SIZE_FOR_SETTINGS
	global FLASH_SYSTRAY_CHANNEL
	global DISPLAY_IRC_ERRORS_IN_CURRENT_WINDOW
	global ALLOW_TOPIC_EDIT
	global USERLIST_WIDTH_IN_CHARACTERS
	global SHOW_CONNECTION_SCRIPT_IN_WINDOWS_MENU
	global SHOW_ALL_SERVER_ERRORS

	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			settings = json.load(read_settings)

		prepatch_length = len(settings)
		settings = patch_settings(settings)
		postpatch_length = len(settings)

		SHOW_ALL_SERVER_ERRORS = settings["display_all_server_errors"]
		SHOW_CONNECTION_SCRIPT_IN_WINDOWS_MENU = settings["show_connection_script_in_windows_menu"]
		USERLIST_WIDTH_IN_CHARACTERS = settings["userlist_width_in_characters"]
		ALLOW_TOPIC_EDIT = settings["enable_topic_editor"]
		DISPLAY_IRC_ERRORS_IN_CURRENT_WINDOW = settings["display_server_errors_in_current_window"]
		FLASH_SYSTRAY_CHANNEL = settings["systray_notification_channel"]
		MAXIMUM_FONT_SIZE_FOR_SETTINGS = settings["maximum_font_size_for_settings_dialog"]
		SHOW_TIPS_AT_START = settings["show_tips_at_startup"]
		PLUGIN_PAUSE = settings["enable_plugin_pause_event"]
		PLUGIN_UNPAUSE = settings["enable_plugin_unpause_event"]
		CLOSE_EDITOR_ON_UNINSTALL = settings["close_editor_on_plugin_uninstall"]
		IRC_COLOR_IN_TOPICS = settings["display_irc_colors_in_topics"]
		NOTIFY_ON_REPEATED_FAILED_RECONNECTIONS = settings["notify_on_repeated_failed_reconnections"]
		SHOW_TOPIC_IN_EDITOR_TOOLTIP = settings["show_channel_topic_in_tooltip"]
		ENABLE_BROWSER_COMMAND = settings["enable_browser_command"]
		PLUGIN_UPTIME = settings["enable_plugin_uptime_event"]
		ENABLE_IRC_COLOR_MARKUP = settings["enable_irc_color_markup"]
		ENABLE_ASCIIMOJI_SHORTCODES = settings["enable_asciimoji_shortcodes"]
		ENABLE_MARKDOWN_MARKUP = settings["enable_markdown_markup"]
		SHOW_PLUGIN_CONSOLE_ON_CREATION = settings["show_plugin_consoles_on_creation"]
		PLUGIN_UNLOAD = settings["enable_plugin_unload_event"]
		PLUGIN_UNINSTALL = settings["enable_plugin_uninstall_event"]
		RELOAD_PLUGINS_AFTER_UNINSTALL = settings["reload_plugins_after_uninstall"]
		CLEAR_PLUGINS_FROM_MEMORY_ON_RELOAD = settings["clear_plugins_from_memory_on_reload"]
		EXECUTE_INIT_ON_PLUGIN_RELOAD = settings["execute_init_event_on_plugin_reload"]
		WINDOWBAR_TOPIC_IN_TOOLTIP = settings["windowbar_channel_topic_in_tooltip"]
		UNKNOWN_NETWORK_NAME = settings["unknown_network_name"]
		SAVE_CONNECTION_HISTORY = settings["save_connection_history"]
		PRINT_SCRIPT_ERRORS_TO_STDOUT = settings["print_script_errors_to_stdout"]
		SCRIPT_THREAD_QUIT_TIMEOUT = settings["script_thread_quit_timeout"]
		MANAGERS_ALWAYS_ON_TOP = settings["managers_always_on_top"]
		DRAG_AND_DROP_MAIN_APPLICATION = settings["enable_application_drag_and_drop"]
		DISPLAY_MESSAGEBOX_ON_PLUGIN_RUNTIME_ERRORS = settings["display_messagebox_on_plugin_error"]
		AUTO_RELOAD_ON_CLOSE = settings["reload_plugins_on_editor_close"]
		WINDOWBAR_SHOW_UNREAD_MENTIONS = settings["windowbar_show_unread_mentions"]
		BAD_NICKNAME_FALLBACK = settings["bad_nickname_fallback"]
		PLUGIN_ISON = settings["enable_plugin_ison_event"]
		SHOW_ISON_INFO_IN_CURRENT_WINDOW = settings["show_ison_response_in_current_window"]
		SHOW_LUSER_INFO_IN_CURRENT_WINDOW = settings["show_lusers_response_in_current_window"]
		PLUGIN_HAS_CONSOLE_MARKER = settings["plugin_manager_console_icon"]
		DOUBLECLICK_NICK_DISPLAY = settings["doubleclick_nick_display_to_change_nick"]
		PLUGIN_ISUPPORT = settings["enable_plugin_isupport_event"]
		DO_NOT_REPLY_TO_CTCP_SOURCE = settings["do_not_reply_to_ctcp_source"]
		DO_NOT_REPLY_TO_CTCP_VERSION = settings["do_not_reply_to_ctcp_version"]
		NO_ENVIRONMENT_IN_CTCP_REPLIES = settings["do_not_show_environment_in_ctcp_version"]
		IMPORT_SCRIPTS_IN_PLUGINS = settings["import_scripts_in_plugin_packages"]
		ENABLE_CALL_COMMAND = settings["enable_call_command"]
		AUTOCOMPLETE_METHODS = settings["autocomplete_methods"]
		DEFAULT_PYTHON_INDENT = settings["default_python_indentation"]
		OVERWRITE_PLUGINS_ON_IMPORT = settings["overwrite_files_on_plugin_import"]
		EDITOR_WORDWRAP = settings["editor_word_wrap"]
		PYTHON_AUTOINDENT = settings["python_editor_auto_indent"]
		PYTHON_SHOW_WHITESPACE = settings["python_editor_show_whitespace"]
		PLUGIN_ERROR = settings["enable_plugin_error_event"]
		PLUGIN_ME = settings["enable_plugin_me_event"]
		PLUGIN_CLOSE = settings["enable_plugin_close_event"]
		PLUGIN_SUBWINDOW = settings["enable_plugin_subwindow_event"]
		PLUGIN_SERVER = settings["enable_plugin_server_event"]
		ENABLE_PLUGIN_EDITOR = settings["enable_plugin_editor"]
		PLUGIN_MOTD = settings["enable_plugin_motd_event"]
		PLUGIN_PING = settings["enable_plugin_ping_event"]
		PLUGIN_DISCONNECT = settings["enable_plugin_disconnect_event"]
		PLUGIN_NICK = settings["enable_plugin_nick_event"]
		PLUGIN_CTICK = settings["enable_plugin_ctick_event"]
		PLUGIN_LOST = settings["enable_plugin_lost_event"]
		PLUGIN_CONNECTED = settings["enable_plugin_connected_event"]
		PLUGIN_CONNECTING = settings["enable_plugin_connecting_event"]
		PLUGIN_TOPIC = settings["enable_plugin_topic_event"]
		PLUGIN_RENAME = settings["enable_plugin_rename_event"]
		PLUGIN_INVITE = settings["enable_plugin_invite_event"]
		PLUGIN_ACTIVATE = settings["enable_plugin_activate_event"]
		PLUGIN_AWAY = settings["enable_plugin_away_event"]
		PLUGIN_BACK = settings["enable_plugin_back_event"]
		PLUGIN_IN = settings["enable_plugin_line_in_event"]
		PLUGIN_OUT = settings["enable_plugin_line_out_event"]
		PLUGIN_QUIT = settings["enable_plugin_quit_event"]
		PLUGIN_MODE = settings["enable_plugin_mode_event"]
		PLUGIN_UNMODE = settings["enable_plugin_unmode_event"]
		PLUGIN_KICK = settings["enable_plugin_kick_event"]
		PLUGIN_KICKED = settings["enable_plugin_kicked_event"]
		PLUGIN_TICK = settings["enable_plugin_tick_event"]
		PLUGIN_PART = settings["enable_plugin_part_event"]
		PLUGIN_JOIN = settings["enable_plugin_join_event"]
		PLUGIN_LEFT = settings["enable_plugin_left_event"]
		PLUGIN_JOINED = settings["enable_plugin_joined_event"]
		PLUGIN_INIT = settings["enable_plugin_init_event"]
		PLUGIN_MESSAGE = settings["enable_plugin_message_event"]
		PLUGIN_NOTICE = settings["enable_plugin_notice_event"]
		PLUGIN_ACTION = settings["enable_plugin_action_event"]
		ENABLE_PLUGINS = settings["enable_plugins"]
		DISPLAY_MOTD_AS_RAW_TEXT = settings["display_server_motd_as_raw_text"]
		ENABLE_IGNORE = settings["enable_ignore"]
		ENABLE_HOTKEYS = settings["enable_hotkeys"]
		EXECUTE_HOTKEY_AS_COMMAND = settings["execute_hotkey_as_command"]
		HOTKEYS = settings["hotkeys"]
		CURSOR_BLINK_RATE = settings["cursor_blink_rate"]
		REJECT_ALL_CHANNEL_NOTICES = settings["reject_all_channel_notices"]
		CURSOR_BLINK = settings["cursor_blink"]
		DISPLAY_LONG_MESSAGE_INDICATOR = settings["show_long_message_indicator"]
		DISPLAY_FULL_USER_INFO_IN_MODE_MESSAGES = settings["display_full_user_info_in_mode_messages"]
		ELIDE_LONG_NICKNAMES_IN_CHAT_DISPLAY = settings["elide_long_nicknames_in_chat_display"]
		AUTOCOMPLETE_MACROS = settings["autocomplete_macros"]
		SEARCH_INSTALL_DIRECTORY_FOR_FILES = settings["search_install_directory_for_files"]
		FLOOD_PROTECTION_FOR_LONG_MESSAGES = settings["flood_protection_for_sending_long_messages"]
		IRC_MAX_PAYLOAD_LENGTH = settings["chat_message_max_length"]
		ENABLE_USER_COMMAND = settings["enable_user_command"]
		AUTOCOMPLETE_USER = settings["autocomplete_user_settings"]
		DELAY_AUTO_RECONNECTION = settings["delay_automatic_reconnection"]
		RECONNECTION_DELAY = settings["automatic_reconnection_timer"]
		SHOW_LOGS_IN_WINDOWS_MENU = settings["show_network_logs_in_windows_menu"]
		SHOW_LIST_IN_SYSTRAY_MENU = settings["show_channel_list_in_systray_menu"]
		SHOW_LOGS_IN_SYSTRAY_MENU = settings["show_network_logs_in_systray_menu"]
		SHOW_CONNECTIONS_IN_SYSTRAY_MENU = settings["show_connections_in_systray_menu"]
		SHOW_SETTINGS_IN_SYSTRAY_MENU = settings["show_settings_in_systray_menu"]
		SHOW_DIRECTORIES_IN_SYSTRAY_MENU = settings["show_directories_in_systray_menu"]
		SHOW_LINKS_IN_SYSTRAY_MENU = settings["show_links_in_systray_menu"]
		DO_NOT_SHOW_SERVER_IN_TITLE = settings["do_not_show_server_name_in_application_title"]
		HOSTMASK_FETCH_FREQUENCY = settings["fetch_hostmask_frequency"]
		USERLIST_CONTEXT_MENU = settings["enable_userlist_context_menu"]
		ELIDE_HOSTMASK_IN_USERLIST_CONTEXT = settings["elide_hostmask_in_userlist_context_menu"]
		ELIDE_AWAY_MSG_IN_USERLIST_CONTEXT = settings["elide_away_message_in_userlist_context_menu"]
		ENABLE_WAIT_COMMAND = settings["enable_wait_command"]
		INPUT_CURSOR_WIDTH = settings["input_widget_cursor_width"]
		RUBBER_BAND_MOVE = settings["rubberband_subwindow_move"]
		RUBBER_BAND_RESIZE = settings["rubberband_subwindow_resize"]
		SET_SUBWINDOW_ORDER = settings["subwindow_order"]
		SHOW_FULL_SCREEN = settings["show_app_full_screen"]
		WRITE_OUTGOING_PRIVATE_MESSAGES_TO_CURRENT_WINDOW = settings["write_outgoing_private_messages_to_current_window"]
		ENABLE_IF_COMMAND = settings["enable_if_command"]
		ENABLE_GOTO_COMMAND = settings["enable_goto_command"]
		SYNTAX_OPERATOR_COLOR = settings["syntax_operator_color"]
		SYNTAX_OPERATOR_STYLE = settings["syntax_operator_style"]
		ENABLE_BUILT_IN_ALIASES = settings["enable_built_in_aliases"]
		MENUBAR_HOVER_EFFECT = settings["menubar_bold_on_hover"]
		WINDOWBAR_BOLD_ACTIVE_WINDOW = settings["windowbar_bold_active_window"]
		WINDOWBAR_INCLUDE_README = settings["windobar_include_readme"]
		HIDE_WINDOWBAR_IF_EMPTY = settings["hide_windowbar_if_empty"]
		ESCAPE_HTML_FROM_RAW_SYSTEM_MESSAGE = settings["escape_html_in_print_and_prints_messages"]
		DISPLAY_ERROR_FOR_RESTRICT_AND_ONLY_VIOLATION = settings["display_error_message_for_restrict_and_only_violation"]
		ENABLE_CONFIG_COMMAND = settings["enable_config_command"]
		AUTOCOMPLETE_SETTINGS = settings["autocomplete_settings"]
		SYNTAX_SCRIPT_COLOR = settings["syntax_script_only_color"]
		SYNTAX_SCRIPT_STYLE = settings["syntax_script_only_style"]
		SHOW_HIDDEN_PRIVATE_WINDOWS_IN_WINDOWBAR = settings["show_hidden_private_windows_in_windowbar"]
		SHOW_HIDDEN_CHANNEL_WINDOWS_IN_WINDOWBAR = settings["show_hidden_channel_windows_in_windowbar"]
		SHOW_CHANNEL_NAME_IN_SUBWINDOW_TITLE = settings["show_channel_name_in_subwindow_title"]
		MAXIMIZE_SUBWINDOWS_ON_CREATION = settings["maximize_subwindows_on_creation"]
		AUTOCOMPLETE_FILENAMES = settings["autocomplete_filenames"]
		DOUBLECLICK_TO_OPEN_PRIVATE_CHAT = settings["doubleclick_userlist_to_open_private_chat"]
		WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS = settings["windowbar_show_connecting_server_windows_in_italics"]
		ENABLE_DELAY_COMMAND = settings["enable_delay_command"]
		HIDE_SERVER_WINDOWS_ON_SIGNON = settings["hide_server_windows_when_registration_completes"]
		SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR = settings["show_hidden_server_windows_in_windowbar"]
		PROMPT_FOR_SCRIPT_FILE = settings["prompt_for_file_on_calling_script_with_no_arguments"]
		ASK_FOR_SERVER_ON_STARTUP = settings["show_connection_dialog_on_startup"]
		HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG = settings["hide_logo_on_initial_connection_dialog"]
		INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE = settings["interpolate_aliases_into_quit_message"]
		INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE = settings["interpolate_aliases_into_away_message"]
		SHOW_DATES_IN_LOGS = settings["display_dates_in_logs"]
		LOG_CHANNEL_NOTICE = settings["log_channel_notice"]
		ENABLE_INSERT_COMMAND = settings["enable_insert_command"]
		REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS = settings["require_exact_argument_count_for_usage"]
		HALT_SCRIPT_EXECUTION_ON_ERROR = settings["halt_script_execution_on_error"]
		CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES = settings["create_window_for_incoming_private_notices"]
		DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS = settings["do_not_create_private_chat_windows_for_ignored_users"]
		INCLUDE_SCRIPT_COMMAND_SHORTCUT = settings["include_script_command_shortcut"]
		WINDOWBAR_ENTRY_MENU = settings["windowbar_entry_context_menu"]
		WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH = settings["windowbar_unread_message_animation_length"]
		WINDOWBAR_SHOW_UNREAD_MESSAGES = settings["windowbar_show_unread_messages"]
		MAXIMUM_INSERT_DEPTH = settings["maximum_insert_file_depth"]
		SHOW_IGNORE_STATUS_IN_USERLISTS = settings["show_ignore_status_in_userlists"]
		CLOSING_SERVER_WINDOW_DISCONNECTS = settings["closing_server_window_disconnects_from_server"]
		SHOW_PINGS_IN_CONSOLE = settings["display_server_pings_in_server_window"]
		SCRIPTING_ENGINE_ENABLED = settings["enable_scripting"]
		SHOW_MISSPELLED_WORDS_IN_COLOR = settings["spellcheck_in_color"]
		SHOW_MISSPELLED_WORDS_IN_STRIKEOUT = settings["spellcheck_in_strikeout"]
		SPELLCHECK_UNDERLINE_COLOR = settings["spellcheck_underline_color"]
		SHOW_MISSPELLED_WORDS_IN_ITALICS = settings["spellcheck_in_italics"]
		SHOW_MISSPELLED_WORDS_IN_BOLD = settings["spellcheck_in_bold"]
		ALLOW_MENUS_TO_CHANGE_SPELLCHECK_SETTINGS = settings["show_spellcheck_settings_in_menus"]
		SHOW_USER_COUNT_DISPLAY = settings["show_user_count_display"]
		EDITOR_USES_SYNTAX_HIGHLIGHTING = settings["editor_syntax_highlighting"]
		USERLIST_ITEMS_NON_SELECTABLE = settings["do_not_allow_select_on_userlist"]
		IGNORE_LIST = settings["ignored_users"]
		WINDOWBAR_INCLUDE_MANAGER = settings["windowbar_include_log_manager"]
		STRIP_NICKNAME_PADDING_FROM_DISPLAY = settings["do_not_pad_nickname_in_chat_display"]
		DISPLAY_SCRIPT_ERRORS = settings["show_script_execution_errors"]
		ENABLE_STYLE_EDITOR = settings["enable_style_editor"]
		ENABLE_AUTOCOMPLETE = settings["enable_autocomplete"]
		ENABLE_ALIASES = settings["enable_aliases"]
		SHOW_STATUS_BAR_ON_EDITOR_WINDOWS = settings["show_status_bar_on_editor_windows"]
		AUTOCOMPLETE_SHORTCODES_IN_QUIT_MESSAGE_WIDGET = settings["autocomplete_shortcodes_in_quit_message_widget"]
		WRITE_INPUT_AND_OUTPUT_TO_FILE = settings["write_network_input_and_output_to_file"]
		WRITE_INPUT_AND_OUTPUT_TO_CONSOLE = settings["write_network_input_and_output_to_console"]
		EMOJI_LANGUAGE = settings["emoji_shortcode_language"]
		SHOW_CHANNEL_MENU = settings["show_channel_mode_menu"]
		ENABLE_COMMAND_INPUT_HISTORY = settings["enable_command_history"]
		LOG_CHANNEL_NICKNAME_CHANGE = settings["log_channel_nickname_changes"]
		SPELLCHECKER_DISTANCE = settings["spellchecker_distance"]
		TWISTED_CLIENT_HEARTBEAT = settings["twisted_irc_client_heartbeat"]
		LOG_CHANNEL_QUIT = settings["log_channel_quits"]
		LOG_CHANNEL_JOIN = settings["log_channel_joins"]
		LOG_CHANNEL_PART = settings["log_channel_parts"]
		LOG_CHANNEL_TOPICS = settings["log_channel_topics"]
		LOG_ABSOLUTELY_ALL_MESSAGES_OF_ANY_TYPE = settings["log_absolutely_all_messages_of_any_type"]
		CLICK_SYSTRAY_ICON_TO_MINIMIZE_TO_TRAY = settings["click_systray_icon_to_minimize_to_tray"]
		DOUBLECLICK_TO_RESTORE_WINDOW_FROM_SYSTRAY = settings["doubleclick_to_restore_from_systray"]
		AUTOCOMPLETE_SHORTCODES_IN_AWAY_MESSAGE_WIDGET = settings["autocomplete_shortcodes_in_away_message_widget"]
		APP_INTERACTION_CANCELS_AUTOAWAY = settings["app_interaction_cancels_autoaway"]
		WINDOW_INTERACTION_CANCELS_AUTOAWAY = settings["window_interaction_cancels_autoaway"]
		TYPING_INPUT_CANCELS_AUTOAWAY = settings["typing_input_cancels_autoaway"]
		DO_NOT_APPLY_STYLES_TO_TEXT = settings["do_not_apply_styles_to_text"]
		CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES = settings["create_window_for_outgoing_private_messages"]
		PROMPT_FOR_AWAY_MESSAGE = settings["prompt_for_away_message"]
		USE_AUTOAWAY = settings["autoaway"]
		AUTOAWAY_TIME = settings["autoaway_time"]
		DEFAULT_AWAY_MESSAGE = settings["away_message"]
		SHOW_AWAY_STATUS_IN_NICK_DISPLAY = settings["show_away_status_in_nick_display"]
		SHOW_AWAY_STATUS_IN_USERLISTS = settings["show_away_status_in_userlists"]
		SHOW_AWAY_AND_BACK_MESSAGES = settings["show_away_and_back_messages"]
		HIDE_USERLIST_HORIZONTAL_SCROLLBAR = settings["hide_horizontal_scrollbar_on_userlists"]
		SYNTAX_NICKNAME_COLOR = settings["syntax_nickname_color"]
		SYNTAX_NICKNAME_STYLE = settings["syntax_nickname_style"]
		SYNTAX_EMOJI_COLOR = settings["syntax_shortcode_color"]
		SYNTAX_EMOJI_STYLE = settings["syntax_shortcode_style"]
		APPLY_SYNTAX_STYLES_TO_INPUT_WIDGET = settings["apply_syntax_highlighting_to_input_widget"]
		DO_NOT_SHOW_APPLICATION_NAME_IN_TITLE = settings["do_not_show_application_name_in_title"]
		DO_NOT_APPLY_STYLE_TO_USERLIST = settings["do_not_apply_text_style_to_userlist"]
		DO_NOT_APPLY_STYLE_TO_INPUT_WIDGET = settings["do_not_apply_text_style_to_input_widget"]
		SHOW_CHANNEL_TOPIC_IN_APPLICATION_TITLE = settings["show_channel_topic_in_title"]
		WINDOWBAR_HOVER_EFFECT = settings["windowbar_bold_on_hover"]
		WINDOWBAR_UNDERLINE_ACTIVE_WINDOW = settings["windowbar_underline_active_window"]
		SHOW_STATUS_BAR_ON_LIST_WINDOWS = settings["show_status_bar_on_list_windows"]
		SHOW_CHANNEL_LIST_BUTTON_ON_SERVER_WINDOWS = settings["show_channel_list_button_on_server_windows"]
		SHOW_SERVER_WINDOW_TOOLBAR = settings["show_server_window_toolbar"]
		SHOW_LIST_REFRESH_BUTTON_ON_SERVER_WINDOWS = settings["show_list_refresh_button_on_server_windows"]
		SHOW_SERVER_INFO_IN_WINDOWS_MENU = settings["show_server_information_in_windows_menu"]
		CLOSING_WINDOW_MINIMIZES_TO_TRAY = settings["closing_main_window_minimizes_to_tray"]
		SEARCH_ALL_TERMS_IN_CHANNEL_LIST = settings["search_for_all_terms_in_channel_list_search"]
		SHOW_CHANNEL_LIST_IN_WINDOWS_MENU = settings["show_channel_list_entry_in_windows_menu"]
		WINDOWBAR_INCLUDE_LIST = settings["windowbar_include_channel_lists"]
		EXAMINE_TOPIC_IN_CHANNEL_LIST_SEARCH = settings["examine_topic_in_channel_list_search"]
		REQUEST_CHANNEL_LIST_ON_CONNECTION = settings["request_channel_list_on_connection"]
		INTERPOLATE_ALIASES_INTO_INPUT = settings["interpolate_aliases_into_user_input"]
		AUTOCOMPLETE_ALIAS = settings["autocomplete_aliases"]
		ASK_BEFORE_CLOSE = settings["ask_before_exit"]
		ALWAYS_ON_TOP = settings["main_window_always_on_top"]
		FORCE_DEFAULT_STYLE = settings["force_all_windows_to_use_default_style"]
		FORCE_MONOSPACE_RENDERING = settings["force_monospace_text_rendering"]
		SOUND_NOTIFICATION_NICKNAME = settings["sound_notification_nickname"]
		SOUND_NOTIFICATION_DISCONNECT = settings["sound_notification_disconnect"]
		SOUND_NOTIFICATION_PRIVATE = settings["sound_notification_private"]
		SOUND_NOTIFICATION_KICK = settings["sound_notification_kick"]
		SOUND_NOTIFICATION_INVITE = settings["sound_notification_invite"]
		SOUND_NOTIFICATION_NOTICE = settings["sound_notification_notice"]
		SOUND_NOTIFICATION_MODE = settings["sound_notification_mode"]
		SOUND_NOTIFICATION_FILE = settings["sound_notification_file"]
		SOUND_NOTIFICATIONS = settings["sound_notifications"]
		DISPLAY_NICK_ON_SERVER_WINDOWS = settings["display_nick_on_server_windows"]
		SHOW_LINKS_TO_NETWORK_WEBPAGES = settings["show_links_to_known_irc_networks"]
		MAXIMIZE_ON_STARTUP = settings["maximize_app_on_startup"]
		SHOW_STATUS_BAR_ON_SERVER_WINDOWS = settings["show_status_bar_on_server_windows"]
		SHOW_STATUS_BAR_ON_CHAT_WINDOWS = settings["show_status_bar_on_chat_windows"]
		DO_INTERMITTENT_LOG_SAVES = settings["do_intermittent_log_saves"]
		LOG_SAVE_INTERVAL = settings["intermittent_log_save_interval"]
		MAIN_MENU_SETTINGS_NAME = settings["main_menu_settings_name"]
		GET_HOSTMASKS_ON_CHANNEL_JOIN = settings["get_hostmasks_on_channel_join"]
		JOIN_ON_INVITE = settings["auto_join_on_invite"]
		WINDOWBAR_INCLUDE_CHANNELS = settings["windowbar_include_channels"]
		WINDOWBAR_INCLUDE_PRIVATE = settings["windowbar_include_private"]
		EDITOR_PROMPT_SAVE = settings["editor_prompt_save_on_close"]
		SIMPLIFIED_DIALOGS = settings["simplified_dialogs"]
		DARK_MODE = settings["dark_mode"]
		MAIN_MENU_IRC_NAME = settings["main_menu_irc_name"]
		MAIN_MENU_TOOLS_NAME = settings["main_menu_tools_name"]
		MAIN_MENU_WINDOWS_NAME = settings["main_menu_windows_name"]
		MAIN_MENU_HELP_NAME = settings["main_menu_help_name"]
		MENUBAR_MENU = settings["show_menubar_context_menu"]
		WINDOWBAR_MENU = settings["show_windowbar_context_menu"]
		MENUBAR_JUSTIFY = settings["menubar_justify"]
		ALWAYS_SHOW_CURRENT_WINDOW_FIRST = settings["always_show_current_first_in_windowbar"]
		SHOW_CHAT_CONTEXT_MENUS = settings["show_chat_context_menu_options"]
		WINDOWBAR_INCLUDE_EDITORS = settings["windowbar_include_editors"]
		WINDOWBAR_DOUBLECLICK_TO_SHOW_MAXIMIZED = settings["windowbar_doubleclick_to_maximize"]
		WINDOWBAR_SHOW_ICONS = settings["windowbar_show_icons"]
		SHOW_WINDOWBAR = settings["show_windowbar"]
		WINDOWBAR_TOP_OF_SCREEN = settings["windowbar_on_top"]
		WINDOWBAR_INCLUDE_SERVERS = settings["windowbar_include_servers"]
		WINDOWBAR_JUSTIFY = settings["windowbar_justify"]
		WINDOWBAR_CAN_FLOAT = settings["windowbar_can_float"]
		SHOW_INPUT_MENU = settings["show_input_menu"]
		SHOW_USERLIST = settings["show_userlists"]
		SHOW_CHANNEL_NAME_AND_MODES = settings["show_channel_name_and_modes"]
		SHOW_BANLIST_MENU = settings["show_channel_banlist_menu"]
		SHOW_CHANNEL_TOPIC_IN_WINDOW_TITLE = settings["show_channel_topic_in_window_title"]
		SHOW_CHANNEL_TOPIC = settings["show_channel_topic_bar"]
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
		DISPLAY_ACTIVE_SUBWINDOW_IN_TITLE = settings["display_active_subwindow_in_title"]
		PROMPT_ON_FAILED_CONNECTION = settings["prompt_on_failed_connection"]
		ALWAYS_SCROLL_TO_BOTTOM = settings["always_scroll_to_bottom"]
		NOTIFY_ON_LOST_OR_FAILED_CONNECTION = settings["notify_on_lost_or_failed_connection"]
		ASK_BEFORE_RECONNECT = settings["ask_before_reconnect"]
		ENABLE_SPELLCHECK = settings["enable_spellcheck"]
		ENABLE_EMOJI_SHORTCODES = settings["enable_emoji_shortcodes"]
		SCROLL_CHAT_TO_BOTTOM_ON_RESIZE = settings["scroll_chat_to_bottom_on_resize"]
		SHOW_CHANNEL_UPTIME = settings["show_channel_uptime"]
		SHOW_CONNECTION_UPTIME = settings["show_connection_uptime"]
		INTERFACE_BUTTON_SIZE = settings["interface_button_size"]
		INTERFACE_BUTTON_ICON_SIZE = settings["interface_button_icon_size"]
		ASK_BEFORE_DISCONNECT = settings["ask_before_disconnect"]
		SAVE_PRIVATE_LOGS = settings["save_private_logs"]
		LOAD_PRIVATE_LOGS = settings["load_private_logs"]
		SAVE_CHANNEL_LOGS = settings["save_channel_logs"]
		LOAD_CHANNEL_LOGS = settings["load_channel_logs"]
		APPLICATION_FONT = settings["application_font"]
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
		DEFAULT_QUIT_MESSAGE = settings["quit_message"]
		DEFAULT_SPELLCHECK_LANGUAGE = settings["default_spellcheck_language"]
		SYSTEM_MESSAGE_PREFIX = settings["system_message_prefix"]
		DISPLAY_IRC_COLORS = settings["display_irc_colors"]
		CONVERT_URLS_TO_LINKS = settings["convert_urls_to_links"]
		AUTOCOMPLETE_COMMANDS = settings["autocomplete_commands"]
		AUTOCOMPLETE_NICKS = settings["autocomplete_nicks"]
		AUTOCOMPLETE_SHORTCODES = settings["autocomplete_shortcodes"]
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

def save_settings(filename,dump=None):
	if dump==None:
		settings = build_settings()

		with open(filename, "w") as write_data:
			json.dump(settings, write_data, indent=4, sort_keys=True)
	else:
		with open(filename, "w") as write_data:
			json.dump(dump, write_data, indent=4, sort_keys=True)

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

def initialize_file(directory,directory_name,filename):
	global CONFIG_DIRECTORY
	global CONFIG_FILE

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	CONFIG_DIRECTORY = os.path.join(directory,directory_name)
	if not os.path.isdir(CONFIG_DIRECTORY): os.mkdir(CONFIG_DIRECTORY)

	CONFIG_FILE = filename
