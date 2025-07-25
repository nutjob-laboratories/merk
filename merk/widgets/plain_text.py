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

PLAIN_TEXT = f'''
<table width="100%" border="0" cellspacing="1" cellpadding="1">
	<tbody>
		<tr>
			<td>&nbsp;&nbsp;!TEXT!&nbsp;&nbsp;</td>
		</tr>
	</tbody>
</table>'''

def plainTextAction(self,text):
		
	tsLabel = QLabel( PLAIN_TEXT.replace("!TEXT!",text) )
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)

	return tsAction

NS_PLAIN_TEXT = f'''
<table width="100%" border="0" cellspacing="1" cellpadding="1">
	<tbody>
		<tr>
			<td>!TEXT!</td>
		</tr>
	</tbody>
</table>'''

def noSpacePlainTextAction(self,text):
		
	tsLabel = QLabel( NS_PLAIN_TEXT.replace("!TEXT!",text) )
	tsAction = QWidgetAction(self)
	tsAction.setDefaultWidget(tsLabel)

	return tsAction