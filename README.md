<p align="center">
  <img src="https://github.com/nutjob-laboratories/merk/raw/main/merk_splash.png"><br>
  <b><big>Open Source IRC Client</big></b><br>
  <i>A multiple-document interface IRC client for Windows and Linux</i><br>
  <a href="https://github.com/nutjob-laboratories/merk/raw/main/downloads/merk-latest.zip">Download MERK 0.024.071</a><br>
</p>

**MERK** is a graphical [open source](https://www.gnu.org/licenses/gpl-3.0.en.html) [Internet relay chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat) client. The current development version is **0.024.071**. It uses a [multiple-document interface](https://en.wikipedia.org/wiki/Multiple-document_interface), much like the popular Windows IRC client [mIRC](https://www.mirc.com/).  **MERK** is written in Python 3, using the [PyQt5](https://pypi.org/project/PyQt5/) and [Twisted](https://twistedmatrix.com/trac/) libraries, and runs on both Windows and Linux.

**MERK** is in beta, but it works, and can be used for most IRC activities.

# Screenshots

<p align="center">
<center><a href="https://github.com/nutjob-laboratories/merk/raw/main/screenshot_big.png"><img src="https://github.com/nutjob-laboratories/merk/raw/main/screenshot1.png"></a></center></br>
 <center><i><small>MERK connected to <a href="https://libera.chat/">Libera</a>, <a href="http://www.efnet.org/">EFnet</a>, and a local IRC server, on Windows 11. </small></i></center>
 </p>
 <p align="center">
 <center><a href="https://github.com/nutjob-laboratories/merk/raw/main/screenshot_linux_big.png"><img src="https://github.com/nutjob-laboratories/merk/raw/main/screenshot_linux2.png"></a></center></br>
  <center><i><small>MERK connected to <a href="http://www.efnet.org/">EFnet</a>, <a href="https://freenode.net/">Freenode</a>, and <a href="https://libera.chat/">Libera</a> on Linux Mint 20.2.</small></i></center>
  </p>
  
# Features

-   Runs on Windows and Linux
-   Supports multiple connections (you can chat on more than one IRC server at a time)
-   Open source ([GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html))
-   Uses a [multiple document interface](https://en.wikipedia.org/wiki/Multiple-document_interface), much like popular Windows IRC client [mIRC](https://www.mirc.com/)
    - Multiple channel and server windows can be open for viewing and chatting at once
    - All chat windows are contained in a single "parent" window
-   A built-in list of over 80 IRC servers to connect to
-   All text colors (and backgrounds) can be customized
    - Text customization can be saved to importable files
    - Individual channels can have their own color schemes
-   Built-in [spell checker](https://github.com/barrust/pyspellchecker) (supports English, Spanish, French, and German)
-   [Emoji](https://en.wikipedia.org/wiki/Emoji) support
    -   Insert emojis into chat by using shortcodes (such as `:joy:` 😂, `:yum:` 😋, etc.)
    -   A list of supported emoji short codes can be found [here](https://carpedm20.github.io/emoji/all.html?enableList=enable_list_alias)
-   Command/nickname auto-completion
-   Full IRC color support
-   Scripting
    - Includes a built in script editor, with scripting macros and syntax highlighting
- Automatically execute scripts on connection (to join channels, login in ChanServ, etc.)
- Multithreaded
-   Automatic logging of channel and private chats
  - Includes a utility to export logs to JSON, CSV, or your own custom format

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

# Usage

```

usage: python merk.py [-h] [--ssl] [--reconnect] [-p PASSWORD] [-c CHANNEL[:KEY]] [-n NICKNAME]
                      [-u USERNAME] [-a NICKNAME] [-r REALNAME] [-D DIRECTORY] [-L]
                      [--config-name NAME] [--qtstyle NAME] [-s DIRECTORY] [-N] [-X] [-S]
                      [SERVER] [PORT]

optional arguments:
  -h, --help            show this help message and exit

Connection:
  SERVER                Server to connect to
  PORT                  Server port to connect to (6667)
  --ssl, --tls          Use SSL/TLS to connect to IRC
  --reconnect           Reconnect to servers on disconnection
  -p PASSWORD, --password PASSWORD
                        Use server password to connect
  -c CHANNEL[:KEY], --channel CHANNEL[:KEY]
                        Join channel on connection
  -n NICKNAME, --nickname NICKNAME
                        Use this nickname to connect
  -u USERNAME, --username USERNAME
                        Use this username to connect
  -a NICKNAME, --alternate NICKNAME
                        Use this alternate nickname to connect
  -r REALNAME, --realname REALNAME
                        Use this realname to connect

Configuration:
  -D, --config-directory DIRECTORY
                        Location to store configuration files
  -L, --config-local    Store configuration files in install directory
  --config-name NAME    Name of the configuration file directory (default:
                        .merk)
  --qtstyle NAME        Set Qt widget style (default: Windows)
  -s, --scripts-directory DIRECTORY
                        Location to look for script files

Miscellaneous:
  -N, --noask           Don't ask for connection information on start
  -X, --nocommands      Don't auto-execute commands on connection
  -S, --noscripts       Don't allow script execution
```
# Developing MERK

Several tools are included in [the official **MERK** repository](https://github.com/nutjob-laboratories/merk) for developing **MERK**. The [`pyrcc5` utility](https://manpages.ubuntu.com/manpages/xenial/man1/pyrcc5.1.html) is required, and should be installed automatically when you install PyQt. These are only needed if you're developing **MERK**, and can be ignored if you're only using the **MERK** IRC client.

 - ***compile_resources.bat*** - This batch file compiles the miscellaneous resources (graphics, fonts, etc) required by **MERK** into a single file, `resources.py`, and inserts the file into the **MERK** source code. This is for development on the Windows platform.
 - ***compile_resources.sh*** - This shell script basically does the same thing that `compile_resources.bat` does, only it's for development on the Linux platform.
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
     - `README.md`
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


