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
DISPLAY_ACTIVE_CHAT_IN_TITLE = True
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
CHANNEL_TOPIC_BOLD = True
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
DEFAULT_AWAY_MESSAGE = "Busy"
USE_AUTOAWAY = False
AUTOAWAY_TIME = 3600
PROMPT_FOR_AWAY_MESSAGE = False
CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES = False
CONVERT_CHANNELS_TO_LINKS = False
DO_NOT_APPLY_STYLES_TO_TEXT = False
TYPING_INPUT_CANCELS_AUTOAWAY = True
WINDOW_INTERACTION_CANCELS_AUTOAWAY = False
APP_INTERACTION_CANCELS_AUTOAWAY = False
AUTOCOMPLETE_EMOJIS_IN_AWAY_MESSAGE_WIDGET = True
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
AUTOCOMPLETE_EMOJIS_IN_QUIT_MESSAGE_WIDGET = True
SHOW_STATUS_BAR_ON_EDITOR_WINDOWS = True
USERLIST_ICON_SIZE = 16
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
ENABLE_SHELL_COMMAND = True
SHOW_IGNORE_STATUS_IN_USERLISTS = True
MAXIMUM_INSERT_DEPTH = 10
WINDOWBAR_SHOW_UNREAD_MESSAGES = True
WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH = 1000
WINDOWBAR_ENTRY_MENU = True
INCLUDE_SCRIPT_COMMAND_SHORTCUT = True
LOG_MANAGER_MAXIMUM_LOAD_SIZE = 5000
DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS = True
CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES = False
HALT_SCRIPT_EXECUTION_ON_ERROR = True
REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS = False
ENABLE_INSERT_COMMAND = True
LOG_CHANNEL_NOTICE = True
SHOW_DATES_IN_LOGS = True
INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE = True
INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE = True
RECLAIM_NICKNAME_FREQUENCY = 30
HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG = False
ASK_FOR_SERVER_ON_STARTUP = True
PROMPT_FOR_SCRIPT_FILE = False
SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR = True
HIDE_SERVER_WINDOWS_ON_SIGNON = False
ENABLE_DELAY_COMMAND = True
WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS = True
DOUBLECLICK_TO_OPEN_PRIVATE_CHAT = True
AUTOCOMPLETE_SCRIPTS = True
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

def build_settings():
	settings = {
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
		"autocomplete_scripts": AUTOCOMPLETE_SCRIPTS,
		"doubleclick_userlist_to_open_private_chat": DOUBLECLICK_TO_OPEN_PRIVATE_CHAT,
		"windowbar_show_connecting_server_windows_in_italics": WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS,
		"enable_delay_command": ENABLE_DELAY_COMMAND,
		"hide_server_windows_when_registration_completes": HIDE_SERVER_WINDOWS_ON_SIGNON,
		"show_hidden_server_windows_in_windowbar": SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR,
		"prompt_for_file_on_calling_script_with_no_arguments": PROMPT_FOR_SCRIPT_FILE,
		"show_connection_dialog_on_startup": ASK_FOR_SERVER_ON_STARTUP,
		"hide_logo_on_initial_connection_dialog": HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG,
		"reclaim_nickname_frequency": RECLAIM_NICKNAME_FREQUENCY,
		"interpolate_aliases_into_quit_message": INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE,
		"interpolate_aliases_into_away_message": INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE,
		"display_dates_in_logs": SHOW_DATES_IN_LOGS,
		"log_channel_notice": LOG_CHANNEL_NOTICE,
		"enable_insert_command": ENABLE_INSERT_COMMAND,
		"require_exact_argument_count_for_scripts": REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS,
		"halt_script_execution_on_error": HALT_SCRIPT_EXECUTION_ON_ERROR,
		"create_window_for_incoming_private_notices": CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES,
		"do_not_create_private_chat_windows_for_ignored_users": DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS,
		"log_manager_maximum_load_size": LOG_MANAGER_MAXIMUM_LOAD_SIZE,
		"include_script_command_shortcut": INCLUDE_SCRIPT_COMMAND_SHORTCUT,
		"windowbar_entry_context_menu": WINDOWBAR_ENTRY_MENU,
		"windowbar_unread_message_animation_length": WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH,
		"windowbar_show_unread_messages": WINDOWBAR_SHOW_UNREAD_MESSAGES,
		"maximum_insert_file_depth": MAXIMUM_INSERT_DEPTH,
		"show_ignore_status_in_userlists": SHOW_IGNORE_STATUS_IN_USERLISTS,
		"enable_shell_command": ENABLE_SHELL_COMMAND,
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
		"userlist_status_icon_size": USERLIST_ICON_SIZE,
		"show_status_bar_on_editor_windows": SHOW_STATUS_BAR_ON_EDITOR_WINDOWS,
		"autocomplete_emojis_in_quit_message_widget": AUTOCOMPLETE_EMOJIS_IN_QUIT_MESSAGE_WIDGET,
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
		"autocomplete_emojis_in_away_message_widget": AUTOCOMPLETE_EMOJIS_IN_AWAY_MESSAGE_WIDGET,
		"app_interaction_cancels_autoaway": APP_INTERACTION_CANCELS_AUTOAWAY,
		"window_interaction_cancels_autoaway": WINDOW_INTERACTION_CANCELS_AUTOAWAY,
		"typing_input_cancels_autoaway": TYPING_INPUT_CANCELS_AUTOAWAY,
		"do_not_apply_styles_to_text": DO_NOT_APPLY_STYLES_TO_TEXT,
		"convert_channel_names_to_links": CONVERT_CHANNELS_TO_LINKS,
		"create_window_for_outgoing_private_messages": CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES,
		"prompt_for_away_message": PROMPT_FOR_AWAY_MESSAGE,
		"autoaway": USE_AUTOAWAY,
		"autoaway_time": AUTOAWAY_TIME,
		"default_away_message": DEFAULT_AWAY_MESSAGE,
		"show_away_status_in_nick_display": SHOW_AWAY_STATUS_IN_NICK_DISPLAY,
		"show_away_status_in_userlists": SHOW_AWAY_STATUS_IN_USERLISTS,
		"show_away_and_back_messages": SHOW_AWAY_AND_BACK_MESSAGES,
		"hide_horizontal_scrollbar_on_userlists": HIDE_USERLIST_HORIZONTAL_SCROLLBAR,
		"syntax_nickname_color": SYNTAX_NICKNAME_COLOR,
		"syntax_nickname_style": SYNTAX_NICKNAME_STYLE,
		"syntax_emoji_color": SYNTAX_EMOJI_COLOR,
		"syntax_emoji_style": SYNTAX_EMOJI_STYLE,
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
		"show_channel_topic_bold": CHANNEL_TOPIC_BOLD,
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
	if not "autocomplete_scripts" in settings:
		settings["autocomplete_scripts"] = AUTOCOMPLETE_SCRIPTS
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
	if not "reclaim_nickname_frequency" in settings:
		settings["reclaim_nickname_frequency"] = RECLAIM_NICKNAME_FREQUENCY
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
	if not "require_exact_argument_count_for_scripts" in settings:
		settings["require_exact_argument_count_for_scripts"] = REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS
	if not "halt_script_execution_on_error" in settings:
		settings["halt_script_execution_on_error"] = HALT_SCRIPT_EXECUTION_ON_ERROR
	if not "create_window_for_incoming_private_notices" in settings:
		settings["create_window_for_incoming_private_notices"] = CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES
	if not "do_not_create_private_chat_windows_for_ignored_users" in settings:
		settings["do_not_create_private_chat_windows_for_ignored_users"] = DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS
	if not "log_manager_maximum_load_size" in settings:
		settings["log_manager_maximum_load_size"] = LOG_MANAGER_MAXIMUM_LOAD_SIZE
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
	if not "enable_shell_command" in settings:
		settings["enable_shell_command"] = ENABLE_SHELL_COMMAND
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
	if not "userlist_status_icon_size" in settings:
		settings["userlist_status_icon_size"] = USERLIST_ICON_SIZE
	if not "show_status_bar_on_editor_windows" in settings:
		settings["show_status_bar_on_editor_windows"] = SHOW_STATUS_BAR_ON_EDITOR_WINDOWS
	if not "autocomplete_emojis_in_quit_message_widget" in settings:
		settings["autocomplete_emojis_in_quit_message_widget"] = AUTOCOMPLETE_EMOJIS_IN_QUIT_MESSAGE_WIDGET
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
	if not "autocomplete_emojis_in_away_message_widget" in settings:
		settings["autocomplete_emojis_in_away_message_widget"] = AUTOCOMPLETE_EMOJIS_IN_AWAY_MESSAGE_WIDGET
	if not "app_interaction_cancels_autoaway" in settings:
		settings["app_interaction_cancels_autoaway"] = APP_INTERACTION_CANCELS_AUTOAWAY
	if not "window_interaction_cancels_autoaway" in settings:
		settings["window_interaction_cancels_autoaway"] = WINDOW_INTERACTION_CANCELS_AUTOAWAY
	if not "typing_input_cancels_autoaway" in settings:
		settings["typing_input_cancels_autoaway"] = TYPING_INPUT_CANCELS_AUTOAWAY
	if not "do_not_apply_styles_to_text" in settings:
		settings["do_not_apply_styles_to_text"] = DO_NOT_APPLY_STYLES_TO_TEXT
	if not "convert_channel_names_to_links" in settings:
		settings["convert_channel_names_to_links"] = CONVERT_CHANNELS_TO_LINKS
	if not "create_window_for_outgoing_private_messages" in settings:
		settings["create_window_for_outgoing_private_messages"] = CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES
	if not "prompt_for_away_message" in settings:
		settings["prompt_for_away_message"] = PROMPT_FOR_AWAY_MESSAGE
	if not "autoaway" in settings:
		settings["autoaway"] = USE_AUTOAWAY
	if not "autoaway_time" in settings:
		settings["autoaway_time"] = AUTOAWAY_TIME
	if not "default_away_message" in settings:
		settings["default_away_message"] = DEFAULT_AWAY_MESSAGE
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
	if not "syntax_emoji_color" in settings:
		settings["syntax_emoji_color"] = SYNTAX_EMOJI_COLOR
	if not "syntax_emoji_style" in settings:
		settings["syntax_emoji_style"] = SYNTAX_EMOJI_STYLE
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
	if not "show_channel_topic_bold" in settings:
		settings["show_channel_topic_bold"] = CHANNEL_TOPIC_BOLD
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
	if not "maximize_app_on_startup" in settings:
		settings["maximize_app_on_startup"] = MAXIMIZE_ON_STARTUP
	if not "force_monospace_text_rendering" in settings:
		settings["force_monospace_text_rendering"] = FORCE_MONOSPACE_RENDERING

	return settings

def load_settings(filename):
	global MDI_BACKGROUND_IMAGE
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
	global AUTOCOMPLETE_EMOJIS
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
	global CHANNEL_TOPIC_BOLD
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
	global CONVERT_CHANNELS_TO_LINKS
	global DO_NOT_APPLY_STYLES_TO_TEXT
	global TYPING_INPUT_CANCELS_AUTOAWAY
	global WINDOW_INTERACTION_CANCELS_AUTOAWAY
	global APP_INTERACTION_CANCELS_AUTOAWAY
	global AUTOCOMPLETE_EMOJIS_IN_AWAY_MESSAGE_WIDGET
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
	global AUTOCOMPLETE_EMOJIS_IN_QUIT_MESSAGE_WIDGET
	global SHOW_STATUS_BAR_ON_EDITOR_WINDOWS
	global USERLIST_ICON_SIZE
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
	global ENABLE_SHELL_COMMAND
	global SHOW_IGNORE_STATUS_IN_USERLISTS
	global MAXIMUM_INSERT_DEPTH
	global WINDOWBAR_SHOW_UNREAD_MESSAGES
	global WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH
	global WINDOWBAR_ENTRY_MENU
	global INCLUDE_SCRIPT_COMMAND_SHORTCUT
	global LOG_MANAGER_MAXIMUM_LOAD_SIZE
	global DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS
	global CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES
	global HALT_SCRIPT_EXECUTION_ON_ERROR
	global REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS
	global ENABLE_INSERT_COMMAND
	global LOG_CHANNEL_NOTICE
	global SHOW_DATES_IN_LOGS
	global INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE
	global INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE
	global RECLAIM_NICKNAME_FREQUENCY
	global HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG
	global ASK_FOR_SERVER_ON_STARTUP
	global PROMPT_FOR_SCRIPT_FILE
	global SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR
	global HIDE_SERVER_WINDOWS_ON_SIGNON
	global ENABLE_DELAY_COMMAND
	global WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS
	global DOUBLECLICK_TO_OPEN_PRIVATE_CHAT
	global AUTOCOMPLETE_SCRIPTS
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

	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			settings = json.load(read_settings)

		prepatch_length = len(settings)
		settings = patch_settings(settings)
		postpatch_length = len(settings)

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
		AUTOCOMPLETE_SCRIPTS = settings["autocomplete_scripts"]
		DOUBLECLICK_TO_OPEN_PRIVATE_CHAT = settings["doubleclick_userlist_to_open_private_chat"]
		WINDOWBAR_SHOW_CONNECTING_SERVERS_IN_ITALICS = settings["windowbar_show_connecting_server_windows_in_italics"]
		ENABLE_DELAY_COMMAND = settings["enable_delay_command"]
		HIDE_SERVER_WINDOWS_ON_SIGNON = settings["hide_server_windows_when_registration_completes"]
		SHOW_HIDDEN_SERVER_WINDOWS_IN_WINDOWBAR = settings["show_hidden_server_windows_in_windowbar"]
		PROMPT_FOR_SCRIPT_FILE = settings["prompt_for_file_on_calling_script_with_no_arguments"]
		ASK_FOR_SERVER_ON_STARTUP = settings["show_connection_dialog_on_startup"]
		HIDE_LOGO_ON_INITIAL_CONNECT_DIALOG = settings["hide_logo_on_initial_connection_dialog"]
		RECLAIM_NICKNAME_FREQUENCY = settings["reclaim_nickname_frequency"]
		INTERPOLATE_ALIASES_INTO_QUIT_MESSAGE = settings["interpolate_aliases_into_quit_message"]
		INTERPOLATE_ALIASES_INTO_AWAY_MESSAGE = settings["interpolate_aliases_into_away_message"]
		SHOW_DATES_IN_LOGS = settings["display_dates_in_logs"]
		LOG_CHANNEL_NOTICE = settings["log_channel_notice"]
		ENABLE_INSERT_COMMAND = settings["enable_insert_command"]
		REQUIRE_EXACT_ARGCOUNT_FOR_SCRIPTS = settings["require_exact_argument_count_for_scripts"]
		HALT_SCRIPT_EXECUTION_ON_ERROR = settings["halt_script_execution_on_error"]
		CREATE_WINDOW_FOR_INCOMING_PRIVATE_NOTICES = settings["create_window_for_incoming_private_notices"]
		DO_NOT_CREATE_PRIVATE_CHAT_WINDOWS_FOR_IGNORED_USERS = settings["do_not_create_private_chat_windows_for_ignored_users"]
		LOG_MANAGER_MAXIMUM_LOAD_SIZE = settings["log_manager_maximum_load_size"]
		INCLUDE_SCRIPT_COMMAND_SHORTCUT = settings["include_script_command_shortcut"]
		WINDOWBAR_ENTRY_MENU = settings["windowbar_entry_context_menu"]
		WINDOWBAR_UNREAD_MESSAGE_ANIMATION_LENGTH = settings["windowbar_unread_message_animation_length"]
		WINDOWBAR_SHOW_UNREAD_MESSAGES = settings["windowbar_show_unread_messages"]
		MAXIMUM_INSERT_DEPTH = settings["maximum_insert_file_depth"]
		SHOW_IGNORE_STATUS_IN_USERLISTS = settings["show_ignore_status_in_userlists"]
		ENABLE_SHELL_COMMAND = settings["enable_shell_command"]
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
		USERLIST_ICON_SIZE = settings["userlist_status_icon_size"]
		SHOW_STATUS_BAR_ON_EDITOR_WINDOWS = settings["show_status_bar_on_editor_windows"]
		AUTOCOMPLETE_EMOJIS_IN_QUIT_MESSAGE_WIDGET = settings["autocomplete_emojis_in_quit_message_widget"]
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
		AUTOCOMPLETE_EMOJIS_IN_AWAY_MESSAGE_WIDGET = settings["autocomplete_emojis_in_away_message_widget"]
		APP_INTERACTION_CANCELS_AUTOAWAY = settings["app_interaction_cancels_autoaway"]
		WINDOW_INTERACTION_CANCELS_AUTOAWAY = settings["window_interaction_cancels_autoaway"]
		TYPING_INPUT_CANCELS_AUTOAWAY = settings["typing_input_cancels_autoaway"]
		DO_NOT_APPLY_STYLES_TO_TEXT = settings["do_not_apply_styles_to_text"]
		CONVERT_CHANNELS_TO_LINKS = settings["convert_channel_names_to_links"]
		CREATE_WINDOW_FOR_OUTGOING_PRIVATE_MESSAGES = settings["create_window_for_outgoing_private_messages"]
		PROMPT_FOR_AWAY_MESSAGE = settings["prompt_for_away_message"]
		USE_AUTOAWAY = settings["autoaway"]
		AUTOAWAY_TIME = settings["autoaway_time"]
		DEFAULT_AWAY_MESSAGE = settings["default_away_message"]
		SHOW_AWAY_STATUS_IN_NICK_DISPLAY = settings["show_away_status_in_nick_display"]
		SHOW_AWAY_STATUS_IN_USERLISTS = settings["show_away_status_in_userlists"]
		SHOW_AWAY_AND_BACK_MESSAGES = settings["show_away_and_back_messages"]
		HIDE_USERLIST_HORIZONTAL_SCROLLBAR = settings["hide_horizontal_scrollbar_on_userlists"]
		SYNTAX_NICKNAME_COLOR = settings["syntax_nickname_color"]
		SYNTAX_NICKNAME_STYLE = settings["syntax_nickname_style"]
		SYNTAX_EMOJI_COLOR = settings["syntax_emoji_color"]
		SYNTAX_EMOJI_STYLE = settings["syntax_emoji_style"]
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
		CHANNEL_TOPIC_BOLD = settings["show_channel_topic_bold"]
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
