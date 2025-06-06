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

NETWORK_LINKS="""Abjects:https://abjects.net/
AfterNET:https://www.afternet.org/
AllNightCafe:https://allnightcafe.org/
BrasIRC:https://www.brasirc.org/
Chatzona:https://www.chatzona.net/
DigitalIRC:https://www.digitalirc.org/
EuropNet:https://www.europnet.org/
Freenode:https://freenode.net/
FurNet:https://furrent.org/
IRCCloud:https://irccloud.com/
IRCHighWay:https://www.irchighway.net/
LewdChat:https://lewdchat.com/
LinkNet:https://www.link-net.org/
MozillaIRC:https://wiki.mozilla.org/IRC
Libera.Chat:https://libera.chat/
OFTC:https://www.oftc.net/
Undernet:https://www.undernet.org/
IRCnet:http://www.ircnet.org/
EFnet:http://www.efnet.org/
DALnet:http://www.dal.net/
QuakeNet:http://www.quakenet.org/
Rizon:http://www.rizon.net/
Snoonet:https://snoonet.org/
GameSurge:http://www.gamesurge.net/
SwiftIRC:http://www.swiftirc.net/
EsperNet:https://www.esper.net/
IRC-Hispano:https://www.irc-hispano.es/
DarkMyst:http://www.darkmyst.org/
GeekShed:https://www.geeksh.ed/
GimpNet:https://www.gimpnet.org/
Ogame:https://www.ogame.org/
SlashNET:https://slashnet.org/
"""

NETWORK_LIST = """irc.2600.net:6667:2600net:normal
irc.accessirc.net:6667:AccessIRC:normal
irc.afternet.org:6667:AfterNET:normal
irc.data.lt:6667:Aitvaras:normal
irc.omnitel.net:6667:Aitvaras:normal
irc.ktu.lt:6667:Aitvaras:normal
irc.kis.lt:6667:Aitvaras:normal
irc.vub.lt:6667:Aitvaras:normal
irc.anthrochat.net:6667:Anthrochat:normal
arcnet-irc.org:6667:ARCNet:normal
irc.austnet.org:6667:AustNet:normal
irc.azzurra.org:6667:AzzurraNet:normal
irc.betachat.net:6667:BetaChat:normal
irc.buddy.im:6667:BuddyIM:normal
irc.canternet.org:6667:Canternet:normal
irc.chat4all.org:6667:Chat4all:normal
irc.chatjunkies.org:6667:ChatJunkies:normal
irc.chatnet.org:6667:ChatNet:normal
irc.chatspike.net:6667:ChatSpike:normal
irc.chattingaway.com:6667:ChattingAway:normal
irc.criten.net:6667:Criten:normal
us.dal.net:6667:DALnet:normal
irc.darkmyst.org:6667:DarkMyst:normal
irc.d-t-net.de:6667:Dark-Tou-Net:normal
irc.deltaanime.net:6667:DeltaAnime:normal
irc.PRISON.net:6667:EFnet:normal
irc.choopa.net:6667:EFnet:normal
irc.choopa.net:9999:EFnet:ssl
irc.paraphysics.net:6667:EFnet:normal
efnet.port80.se:6667:EFnet:normal
irc.underworld.no:6667:EFnet:normal
irc.underworld.no:6697:EFnet:ssl
irc.inet.tele.dk:6667:EFnet:normal
irc.electrocode.net:6667:ElectroCode:normal
irc.enterthegame.com:6667:EnterTheGame:normal
irc.entropynet.net:6667:EntropyNet:normal
irc.esper.net:6667:EsperNet:normal
irc.euirc.net:6667:EUIrc:normal
irc.europnet.org:6667:EuropNet:normal
irc.fdfnet.net:6667:FDFNet:normal
chat.freenode.net:6667:freenode:normal
chat.freenode.net:6697:freenode:ssl
irc.freenode.net:6667:freenode:normal
irc.freenode.net:6697:freenode:ssl
irc.furnet.org:6667:Furnet:normal
irc.galaxynet.org:6667:GalaxyNet:normal
irc.gamesurge.net:6667:GameSurge:normal
irc.geeksirc.net:6667:GeeksIRC:normal
irc.geekshed.net:6667:GeekShed:normal
irc.gimp.org:6667:GIMPNet:normal
irc.gnome.org:6667:GIMPNet:normal
irc.globalgamers.net:6667:GlobalGamers:normal
irc.hashmark.net:6667:Hashmark:normal
irc.idlemonkeys.net:6667:IdleMonkeys:normal
irc.indirectirc.com:6667:IndirectIRC:normal
irc.interlinked.me:6667:Interlinked:normal
irc.irc4fun.net:6667:IRC4Fun:normal
irc.irchighway.net:6667:IRCHighWay:normal
open.ircnet.net:6667:IRCNet:normal
irc.irctoo.net:6667:Irctoo.net:normal
irc.kbfail.net:6667:KBFail:normal
irc.krstarica.com:6667:Krstarica:normal
irc.libera.chat:6697:Libera.Chat:ssl
irc.librairc.net:6667:LibraIRC:normal
irc.mindforge.org:6667:MindForge:normal
irc.mixxnet.net:6667:MIXXnet:normal
irc.mozilla.org:6667:Moznet:normal
irc.obsidianirc.net:6667:ObsidianIRC:normal
irc.oceanius.com:6667:Oceanius:normal
irc.oftc.net:6667:OFTC:normal
irc.othernet.org:6667:OtherNet:normal
irc.oz.org:6667:OzNet:normal
irc.pirc.pl:6667:PIRC.PL:normal
irc.ponychat.net:6667:PonyChat:normal
uevora.ptnet.org:6667:PTNet.org:normal
vianetworks.ptnet.org:6667:PTNet.org:normal
irc.quakenet.org:6667:QuakeNet:normal
irc.rizon.net:6667:Rizon:normal
irc.rizon.net:6697:Rizon:ssl
irc.scene.org:6667:SceneNet:normal
irc.serenity-irc.net:6667:Serenity-IRC:normal
irc.slashnet.org:6667:SlashNET:normal
irc.slashnet.org:6697:SlashNET:ssl
irc.snoonet.org:6667:Snoonet:normal
irc.solidirc.com:6667:SolidIRC:normal
irc.sorcery.net:6667:SorceryNet:normal
irc.spotchat.org:6667:SpotChat:normal
irc.starchat.net:6667:StarChat:normal
irc.station51.net:6667:Station51:normal
irc.stormbit.net:6667:StormBit:normal
irc.swiftirc.net:6667:SwiftIRC:normal
irc.synirc.net:6667:synIRC:normal
irc.techtronix.net:6667:Techtronix:normal
irc.servx.ru:6667:TURLINet:normal
us.undernet.org:6667:UnderNet:normal
irc.worldnet.net:6667:Worldnet:normal
irc.xertion.org:6667:Xertion:normal"""
