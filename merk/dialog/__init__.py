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

from .away import Dialog as Away
from .newnick import Dialog as Nick
from .connect import Dialog as Connect
from .joinchannel import Dialog as JoinChannel
from .styler import Dialog as Styler
from .settings import Dialog as Settings
from .windowsize import Dialog as WindowSize
from .about import Dialog as About
from .new_connect_script import Dialog as NewConnectScript
from .get_script import Dialog as GetScript
from .menu_name import Dialog as SetMenuName
from .key import Dialog as SetKey
from .find import Dialog as Find
from .set_ignore import Dialog as SetIgnore
from .set_bind import Dialog as SetBind
from .set_file import Dialog as SetFilename
from .method_name import Dialog as SetMethodName

def SetFilenameDialog(obj):
	x = SetFilename(obj)
	info = x.get_window_information(obj)
	del x

	if not info: return None
	return info

def GetIgnore(msg,parent):
	x = SetIgnore(msg,parent)
	info = x.get_message_information(msg,parent)
	del x

	return info

def SetKeyDialog(parent,key=None):
	x = SetKey(parent,key)
	info = x.get_message_information(parent,key)
	del x

	return info

def SetMenuNameDialog(msg,parent):
	x = SetMenuName(msg,parent)
	info = x.get_message_information(msg,parent)
	del x

	return info

def SetMethodNameDialog(msg,parent):
	x = SetMethodName(msg,parent)
	info = x.get_message_information(msg,parent)
	del x

	return info

def AboutDialog():
	x = About()
	x.show()
	return x

def SizeDialog(obj):
	x = WindowSize(obj)
	info = x.get_window_information(obj)
	del x

	if not info: return None
	return info

def SettingsDialog(app,obj):
	x = Settings(app,obj)
	return x

def StylerDialog(client,chat,obj):
	x = Styler(client,chat,obj,False)
	info = x.get_style_information(client,chat,obj,False)
	del x

	if not info: return None
	return info

def StylerDefaultDialog(obj):
	x = Styler(None,None,obj,False,True)
	info = x.get_style_information(None,None,obj,False,True)
	del x

	if not info: return None
	return info

def SimpleStylerDialog(client,chat,obj):
	x = Styler(client,chat,obj,True)
	info = x.get_style_information(client,chat,obj,True)
	del x

	if not info: return None
	return info

def SimpleStylerDefaultDialog(obj):
	x = Styler(None,None,obj,True,True)
	info = x.get_style_information(None,None,obj,True,True)
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
	x = Connect(obj,parent,dismsg,reason,True,noexecute,donotsave,False)
	info = x.get_connect_information(obj,parent,dismsg,reason,True,noexecute,donotsave,False)
	del x

	if not info: return None
	return info

def ConnectDialogSimplified(obj,parent=None,dismsg='',reason='',noexecute=False,donotsave=False):
	x = Connect(obj,parent,dismsg,reason,False,noexecute,donotsave,False)
	info = x.get_connect_information(obj,parent,dismsg,reason,False,noexecute,donotsave,False)
	del x

	if not info: return None
	return info

def ConnectDialogInitial(obj,parent=None,dismsg='',reason='',noexecute=False,donotsave=False):
	x = Connect(obj,parent,dismsg,reason,True,noexecute,donotsave,True)
	info = x.get_connect_information(obj,parent,dismsg,reason,True,noexecute,donotsave,True)
	del x

	if not info: return None
	return info

def ConnectDialogSimplifiedInitial(obj,parent=None,dismsg='',reason='',noexecute=False,donotsave=False):
	x = Connect(obj,parent,dismsg,reason,False,noexecute,donotsave,True)
	info = x.get_connect_information(obj,parent,dismsg,reason,False,noexecute,donotsave,True)
	del x

	if not info: return None
	return info

def NewNickDialog(nick,obj):
	x = Nick(nick,obj)
	info = x.get_nick_information(nick,obj)
	del x

	if not info: return None
	return info

def AwayDialog(obj):
	x = Away(obj)
	info = x.get_away_information(obj)
	del x

	if not info: return None
	return info