<p align="center">
  <img src="https://github.com/nutjob-laboratories/merk//raw/main/graphics/banner.png"><br>
  <b><big>Open Source IRC Client</big></b><br>
  <i>A multiple-document interface IRC client for Windows and Linux</i><br>
</p>

 - [Features](#Features)
 - [Requirements](#Requirements)
 - [Running MERK](#running-merk)
 - [Screenshots](#screenshots)
 - [Usage](#usage)
 - [Example commandline usage](#example-commandline-usage)
 - [Why does MERK exist?](#why-does-merk-exist)
 - [What does MERK mean?](#what-does-merk-mean)
 - [Developing MERK](#developing-merk)

 <p align="center"><h1><b><a href="https://github.com/nutjob-laboratories/merk/raw/main/downloads/merk-latest.zip">Download MERK 0.034.016</a></b></h1></p>
  
**MERK** is a graphical [open source](https://www.gnu.org/licenses/gpl-3.0.en.html) [Internet relay chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat) client. The current development version is **0.034.016**. It uses a [multiple-document interface](https://en.wikipedia.org/wiki/Multiple-document_interface), much like the popular Windows IRC client [mIRC](https://www.mirc.com/).  **MERK** is written in Python 3, using the [PyQt5](https://pypi.org/project/PyQt5/) and [Twisted](https://twistedmatrix.com/trac/) libraries, and runs on both Windows and Linux. **MERK** is updated frequently with new features and bugfixes.

**MERK** is still in development, but it works, and can be used for most IRC activities.

Join me on the official **MERK** IRC channel, **#merk** on the Libera Chat network! Connect to  Libera in the client as one of the built-in server suggestions, or at **irc.libera.chat**, port **6667** (you can also connect via SSL on port **6697**). Honestly, I work a lot, so I'm almost always idle, but I pop in and chat a few times a day!

# Features

-   Runs on Windows and Linux
-   Supports multiple connections (you can chat on more than one IRC server at a time)
-   Open source ([GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html))
-   Uses a [multiple document interface](https://en.wikipedia.org/wiki/Multiple-document_interface), much like popular Windows IRC client [mIRC](https://www.mirc.com/)
    - Multiple channel and server windows can be open for viewing and chatting at once
    - All chat windows are contained in a single "parent" window
- Dark mode!
  - Dark mode can be enabled from the commandline, or from the settings dialog
  - If dark mode is enabled from the settings dialog, an application restart is required
- Very configurable, without having to manually edit a configuration file
    - Control application behavior, logging, features, and more!
    - Over 80 different settings can be changed, allowing you to customize **MERK** to look and function _exactly_ the way you want it to look and function.
    - Almost all settings can be changed in the settings dialog without a restart. Have fun testing different options!
    - Configuration data is stored in JSON
 -  Extensive commandline options
    - Set defaults and settings
    - Connect to one or multiple servers automatically on start-up
    - Almost everything about how **MERK** starts up can be customized
-   A built-in list of over 80 IRC servers to connect to
-   All text colors (and backgrounds) can be customized
    - Text customization can be saved to importable files
    - Individual channels can have their own color schemes
    - Styles are saved and loaded automatically
      - Channel styles are saved and loaded by network, so they work no matter what server you connect to.
    - Easy to use GUI text style editor is built-in
    - Changes to text style are immediate, without having to restart!
-   Built-in [spell checker](https://github.com/barrust/pyspellchecker) (supports English, Spanish, French, and German)
-   [Emoji](https://en.wikipedia.org/wiki/Emoji) support
    -   Insert emojis into chat by using shortcodes (such as `:joy:` 😂, `:yum:` 😋, etc.)
    -   A list of supported emoji short codes can be found [here](https://carpedm20.github.io/emoji/all.html?enableList=enable_list_alias)
-   Command/nickname/channel auto-completion
-   Full IRC color support
-   Full scripting engine
    - Includes a built in script editor, with scripting macros and syntax highlighting
    - Automatically execute scripts on connection (to join channels, login in ChanServ, etc.)
- Multithreaded
-   Automatic logging of channel and private chats
    - Includes a utility to export logs to JSON, CSV, or your own custom format
    - Logs are stored in JSON, so parsing/scraping your own logs in easy

# Requirements

**MERK** requires Python 3, [PyQt5](https://pypi.org/project/PyQt5/), and [Twisted](https://twistedmatrix.com/trac/). PyQt5 and Twisted can be installed by using [**pip**](https://pypi.org/project/pip/):

    pip install pyqt5
    pip install Twisted

To connect to IRC servers via SSL, two additional libraries may be needed:

    pip install pyOpenSSL
    pip install service_identity

**MERK** is being developed with Python 3.13 on Windows 11 and Linux Mint.

If you're running Windows, and you're getting errors when trying to run **MERK**, you may have to install another library, [pywin32](https://pypi.org/project/pywin32/). You can also install this with [**pip**](https://pypi.org/project/pip/):

    pip install pywin32

To run properly on Linux, the latest version of all required software is recommended.

There are three libraries that comes bundled with **MERK**:
 - [qt5reactor](https://github.com/twisted/qt5reactor)
 - [pyspellchecker](https://github.com/barrust/pyspellchecker)
 - [emoji](https://github.com/carpedm20/emoji)

# Running MERK

First, make sure that all the requirements are installed. Next, [download **MERK**](https://github.com/nutjob-laboratories/merk/raw/main/downloads/merk-latest.zip). Extract the zipfile to a directory of your choice using your favorite archive/zip program. Open a command prompt, navigate to the directory you extracted **MERK** to, and type:

    python merk.py
# Screenshots

<p align="center">
<center><a href="https://github.com/nutjob-laboratories/merk//raw/main/graphics/screenshot_big.png"><img src="https://github.com/nutjob-laboratories/merk//raw/main/graphics/screenshot1.png"></a></center></br>
 <center><i><small>MERK connected to <a href="https://libera.chat/">Libera</a>, <a href="http://www.efnet.org/">EFnet</a>, and a local IRC server, on Windows 11, using the "windows" widget set. </small></i></center>
 </p>
 <p align="center">
 <center><a href="https://github.com/nutjob-laboratories/merk//raw/main/graphics/screenshot_linux_big.png"><img src="https://github.com/nutjob-laboratories/merk//raw/main/graphics/screenshot_linux2.png"></a></center></br>
  <center><i><small>MERK connected to <a href="http://www.efnet.org/">EFnet</a>, <a href="https://freenode.net/">Freenode</a>, and <a href="https://libera.chat/">Libera</a> on Linux Mint 20.2 in "dark mode", using the "fusion" widget set.</small></i></center>
  </p>
  <p align="center">
 <center><a href="https://github.com/nutjob-laboratories/merk//raw/main/graphics/connect_1.png"><img src="https://github.com/nutjob-laboratories/merk//raw/main/graphics/connect_1_small.png"></a><a href="https://github.com/nutjob-laboratories/merk//raw/main/graphics/connect_2.png"><img src="https://github.com/nutjob-laboratories/merk//raw/main/graphics/connect_2_small.png"></a><a href="https://github.com/nutjob-laboratories/merk//raw/main/graphics/connect_3.png"><img src="https://github.com/nutjob-laboratories/merk//raw/main/graphics/connect_3_small.png"></a></center></br>
  <center><i><small>The MERK connection dialog, the first thing users see when running MERK. All settings are saved automatically, including the connection script.</small></i></center>
  </p>
  <p align="center">
 <center><a href="https://github.com/nutjob-laboratories/merk//raw/main/graphics/styler.png"><img src="https://github.com/nutjob-laboratories/merk//raw/main/graphics/styler_small.png"></a></center></br>
  <center><i><small>The text style dialog. The text style can be edited for all windows/channels, or for specific channels. Styles are saved by network, so they are applied no matter what server is connected to. Changes, once saved, are automatically and instantly applied.</small></i></center>
  </p>
  <p align="center">
 <center><a href="https://github.com/nutjob-laboratories/merk//raw/main/graphics/settings.png"><img src="https://github.com/nutjob-laboratories/merk//raw/main/graphics/settings_small.png"></a></center></br>
  <center><i><small>The first "page" of the settings dialog. MERK features over 80 settings that can be tweaked until MERK looks and works exactly like you want it to. All settings (except for "dark mode") are applied instantly.</small></i></center>
  </p>
  
# Usage

```

usage: python merk.py [-h] [--ssl] [--reconnect] [-p PASSWORD] [-c CHANNEL[:KEY]]
                      [-n NICKNAME] [-u USERNAME] [-a NICKNAME] [-r REALNAME] [-x]
                      [-d] [-C SERVER:PORT[:PASSWORD]] [-S SERVER:PORT[:PASSWORD]]
                      [--config-name NAME] [--config-directory DIRECTORY]
                      [--config-local] [--scripts-directory DIRECTORY] [-Q NAME]
                      [-R] [-D] [-L] [-E]
                      [SERVER] [PORT]

options:
  -h, --help            show this help message and exit

Connection:
  SERVER                Server to connect to
  PORT                  Server port to connect to (6667)
  --ssl, --tls          Use SSL/TLS to connect to IRC
  --reconnect           Reconnect to servers on disconnection
  -p, --password PASSWORD
                        Use server password to connect
  -c, --channel CHANNEL[:KEY]
                        Join channel on connection
  -n, --nickname NICKNAME
                        Use this nickname to connect
  -u, --username USERNAME
                        Use this username to connect
  -a, --alternate NICKNAME
                        Use this alternate nickname to connect
  -r, --realname REALNAME
                        Use this realname to connect
  -x, --donotexecute    Do not execute connection script
  -d, --donotsave       Do not save new user settings
  -C, --connect SERVER:PORT[:PASSWORD]
                        Connect to server via TCP/IP
  -S, --connectssl SERVER:PORT[:PASSWORD]
                        Connect to server via SSL/TLS

Configuration:
  --config-name NAME    Name of the configuration file directory (default: .merk)
  --config-directory DIRECTORY
                        Location to store configuration files
  --config-local        Store configuration files in install directory
  --scripts-directory DIRECTORY
                        Location to look for script files

Miscellaneous:
  -Q, --qtstyle NAME    Set Qt widget style (default: Fusion)
  -R, --run             Don't ask for connection information on start
  -D, --dark            Run in dark mode
  -L, --light           Run in light mode
  -E, --simple          Show simplified connection dialog

```
# Example Commandline Usage
Let's assume that you want to use the commandline to connect **MERK** to the `2600.net` network and join the `#linux` channel:
```
python merk.py --channel "#linux" irc.2600.net 6667
```
Easy, right? Now let's try something a little more complex. Let's say you want to connect the the `Libera` network, which uses SSL/TLS. You want to use a different nickname than you normally use; you want to use the nickname `merker`, but you don't want to save this nickname as your default. When you join the network, you want to join two channels: `#python` and `#merk`:
```
python merk.py --donotsave -n merker -c "#python" -c "#merk" --ssl irc.libera.chat 6697
```
You can do some things with the commandline that you can't do with the GUI. Let's say that you're using **MERK** on a computer that someone else also uses for **MERK**. You want to store your configuration files in a different folder, just for your use. You always want to use light mode, no matter what the configuration file says, and you've stored some **MERK** scripts in the "C:\Merk_Scripts" folder. You don't want **MERK** to ask you for a server to connect to, you just want it to start up, and you can choose a server from the "IRC" menu:
```
python merk.py --light --config-name .mymerk --scripts-directory "C:\Merk_Scripts" --run
```
Now, let's try something that commonly done with other IRC clients: connecting to multiple servers automatically on startup. You want to use your standard settings, but connect to three different IRC servers as soon as you run **MERK**: you want to connect to the 2600 network and DALNet, using standard TCP/IP,and Libera, using SSL:
```
python merk.py -C irc.2600.net:6667 -S irc.libera.chat:6697 -C us.dal.net:6667
```
This command will start up **MERK** and connect to three of these servers without any extra effort!

All commandline options are what they say on the tin: _optional_. Just running the script with no commandline options will initally open up the connection dialog, and you can do just about everything completely inside the GUI.

# Why does MERK exist?
It's simple. I don't currently like any of the other IRC clients. I've used many, _many_ other IRC clients for Windows and Linux, and they just didn't feel _right_. They weren't customizable enough, didn't have features that I wanted, or just plain looked ancient. I wanted a GUI IRC client that looked and felt modern, and could be heavily customized. My previous IRC client was called [**Ərk**](https://github.com/nutjob-laboratories/erk), and although I liked developing it and working on it, I honestly didn't use it that much. I fell out of love with the "single window" interface that so many other IRC clients use, and decided to try something "new" (and by "new" I mean 30 years old). I remembered using [mIRC](https://www.mirc.com/) back when I was younger, and decided to try and write a new client that used the [multiple-document interface](https://en.wikipedia.org/wiki/Multiple-document_interface) style I remember fondly. And thus, __MERK__ was born!

# What does MERK mean?
Well, if you were to pronounce "IRC" as a word and not an acronym, it would probably be pronounced _/Ərk/_. Since the client allows a user to connect to multiple IRC servers at the same time, well, that might be what the "M" stands for. Either that, or "multiple-document interface". "MDIIRC" doesn't exactly roll off the tongue, so we combined the "M" with the word-pronunciation of IRC, and came up with __MERK__!

# Developing MERK

Several tools are included in [the official **MERK** repository](https://github.com/nutjob-laboratories/merk) for developing **MERK**. The [`pyrcc5` utility](https://manpages.ubuntu.com/manpages/xenial/man1/pyrcc5.1.html) is required, and should be installed automatically when you install PyQt. These are only needed if you're developing **MERK**, and can be ignored if you're only using the **MERK** IRC client.

 - ***compile_resources.bat*** - This batch file compiles the miscellaneous resources (graphics, fonts, etc) required by **MERK** into a single file, `resources.py`, and inserts the file into the **MERK** source code. This is for development on the Windows platform.
 - ***compile_resources.sh*** - This shell script basically does the same thing that `compile_resources.bat` does, only it's for development on the Linux platform.
 - ***build_readme.py*** - This is a Python 3 script that rebuilds the README:
   - Reads`README.txt` into memory and replaces several symbols in it:
     - `! _VERSION_ !` (without spaces) is replaced with **MERK**'s major version
     - `! _MINOR_ !` (without spaces) is replaced with **MERK**'s minor version
     - `! _FULL_VERSION_ !` (without spaces) is replaced with **MERK**'s major and minor version, with a period in between them.
   - Overwrites `README.md` with the edited contents of `README.txt`
 - ***build_dist.py*** - This is a Python 3 script that, when executed, does several things:
   - Executes either `compile_resources.bat` (if the host system is Windows) or `compile_resources.sh` (if the host system is Linux); if the host system is not running either Windows or Linux, `build_dist.py` will exit with an error
   - Increments the **MERK**'s minor version (which is stored in `merk/data/minor.txt`) and saves it
   - Reads`README.txt` into memory and replaces several symbols in it:
     - `! _VERSION_ !` (without spaces) is replaced with **MERK**'s major version
     - `! _MINOR_ !` (without spaces) is replaced with **MERK**'s minor version
     - `! _FULL_VERSION_ !` (without spaces) is replaced with **MERK**'s major and minor version, with a period in between them.
   - Overwrites `README.md` with the edited contents of `README.txt`
   - Creates a new directory named `dist`, and copies into it:
     - `merk.py`
     - `LICENSE`
     - `merk.ico`
     - The `merk` directory and its contents
     - The `qt5reactor` directory and its contents
     - The `spellchecker` directory and its contents
     - The `emoji` directory and its contents
     
   - Zips up the `dist` directory either using [PowerShell](https://en.wikipedia.org/wiki/PowerShell) (if the host system is Windows) or the [zip](https://linux.die.net/man/1/zip) utility (if the host system is Linux) into a file named `dist.zip`
   - Deletes the `dist` directory and its contents
   - Renames `dist.zip` to "merk-*MAJOR VERSION*.zip", referred to as `merk.zip` in this description.
   - If `merk.zip` exists in the `downloads` directory, the version in the `downloads` directory is deleted
   - If `merk-latest.zip` exists in the `downloads` directory, it is deleted
   - `merk.zip` is copied into the `downloads` directory, and is copied to `merk-latest.zip`

[//]: # (End of document)




