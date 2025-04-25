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

from .newnick import Dialog as Nick
from .connect import Dialog as Connect
from .joinchannel import Dialog as JoinChannel
from .styler import Dialog as Styler
from .settings import Dialog as Settings
from .windowsize import Dialog as WindowSize
from .logsize import Dialog as LogSize
from .historysize import Dialog as HistorySize
from .export import Dialog as ExportLog
from .about import Dialog as About
from .quitpart import Dialog as QuitPart
from .comment import Dialog as Comment
from .pause import Dialog as Pause
from .send_pm import Dialog as SendPM
from .print import Dialog as PrintMsg
from .send_notice import Dialog as SendNotice
from .set_nick import Dialog as SetNick
from .part_channel import Dialog as PartChannel
from .set_window import Dialog as SetWindow
from .set_quit import Dialog as SetQuit
from .connect_server import Dialog as ConnectServer
from .new_connect_script import Dialog as NewConnectScript
from .set_script import Dialog as SetScript
from .set_alias import Dialog as SetAlias
from .menu_name import Dialog as SetMenuName

def SetMenuNameDialog(msg,parent):
	x = SetMenuName(msg,parent)
	info = x.get_message_information(msg,parent)
	del x

	return info

def SetWindowDialog(win,obj):
	x = SetWindow(win,obj)
	info = x.get_window_information(win,obj)
	del x

	if not info: return None
	return info

def QuitPartDialog(msg,parent):
	x = QuitPart(msg,parent)
	info = x.get_message_information(msg,parent)
	del x

	return info

def AboutDialog():
	x = About()
	x.show()
	return x

def ExportLogDialog(logdir,obj):
	x = ExportLog(logdir,obj)
	info = x.get_name_information(logdir,obj)
	del x

	if not info: return None
	return info

def HistorySizeDialog(obj):
	x = HistorySize(obj)
	info = x.get_entry_information(obj)
	del x

	if not info: return None
	return info

def LogSizeDialog(obj):
	x = LogSize(obj)
	info = x.get_entry_information(obj)
	del x

	if not info: return None
	return info

def SizeDialog(obj):
	x = WindowSize(obj)
	info = x.get_window_information(obj)
	del x

	if not info: return None
	return info

def SettingsDialog(app,obj):
	x = Settings(app,obj)
	x.show()
	return x

def StylerDialog(client,chat,obj):
	x = Styler(client,chat,obj)
	info = x.get_style_information(client,chat,obj)
	del x

	if not info: return None
	return info

def StylerDefaultDialog(obj):
	x = Styler(None,None,obj,True)
	info = x.get_style_information(None,None,obj,True)
	del x

	if not info: return None
	return info

def JoinChannelDialog(obj):
	x = JoinChannel(obj)
	info = x.get_channel_information(obj)
	del x

	if not info: return None
	return info

def ConnectDialog(obj,parent=None,dismsg='',reason='',noexecute=False,donotsave=False):
	x = Connect(obj,parent,dismsg,reason,True,noexecute,donotsave)
	info = x.get_connect_information(obj,parent,dismsg,reason,True,noexecute,donotsave)
	del x

	if not info: return None
	return info

def ConnectDialogSimplified(obj,parent=None,dismsg='',reason='',noexecute=False,donotsave=False):
	x = Connect(obj,parent,dismsg,reason,False,noexecute,donotsave)
	info = x.get_connect_information(obj,parent,dismsg,reason,False,noexecute,donotsave)
	del x

	if not info: return None
	return info

def NewNickDialog(nick,obj):
	x = Nick(nick,obj)
	info = x.get_nick_information(nick,obj)
	del x

	if not info: return None
	return info
