<p align="center">
  <img src="https://github.com/nutjob-laboratories/merk/raw/main/merk_splash.png"><br>
  <b><big>Open Source IRC Client</big></b><br>
  <i>A multiple-document interface IRC client for Windows and Linux</i><br>
</p>
<p align="center">
  <a href="https://github.com/nutjob-laboratories/merk/raw/main/screenshot_big.png"><img src="https://github.com/nutjob-laboratories/merk/raw/main/screenshot.png"></a><br>
  <i><small>MERK connected to <a href="https://libera.chat/">Libera</a>, <a href="https://www.scuttled.net/">2600net</a>, and a local IRC server. <a href="https://github.com/nutjob-laboratories/merk/raw/main/screenshot_big.png">Click</a> to enlarge.</small></i><br>
</p>
**MERK** is a graphical [open source](https://www.gnu.org/licenses/gpl-3.0.en.html) [Internet relay chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat) client. The current development version is **010.099**. It uses a [multiple-document interface](https://en.wikipedia.org/wiki/Multiple-document_interface), much like the popular Windows IRC client [mIRC](https://www.mirc.com/).  **MERK** is written in Python 3, using the [PyQt5](https://pypi.org/project/PyQt5/) and [Twisted](https://twistedmatrix.com/trac/) libraries, and runs on both Windows and Linux.

**MERK** is in beta, but it is usable. A lot of the fancier features don't work, but you can connect to a server, join channels, and chat with people. Private chat works, too.

Currently, user settings and logs are stored in the application directory. Later, user settings and logs will be stored in the user's home directory (or, via a command-line option, another directory of the user's choosing).

# Requirements

**MERK** requires Python 3, [PyQt5](https://pypi.org/project/PyQt5/), and [Twisted](https://twistedmatrix.com/trac/). PyQt5 and Twisted can be installed by using [**pip**](https://pypi.org/project/pip/):

    pip install pyqt5
    pip install Twisted

To connect to IRC servers via SSL, two additional libraries are needed:

    pip install pyOpenSSL
    pip install service_identity

**MERK** is being developed with Python 3.7 on Windows 11, and Python 3.8.5 on Linux Mint.

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
usage: python merk.py [-h] [--ssl] [--reconnect] [-p PASSWORD] [-D DIRECTORY]
                      [--config-name NAME] [--qtstyle NAME] [-N]
                      [SERVER] [PORT]

optional arguments:
  -h, --help            show this help message and exit

Connection:
  SERVER                Server to connect to
  PORT                  Server port to connect to (6667)
  --ssl                 Use SSL to connect to IRC
  --reconnect           Reconnect to servers on disconnection
  -p PASSWORD, --password PASSWORD
                        Use server password to connect

Configuration:
  -D DIRECTORY, --config-directory DIRECTORY
                        Location to store configuration files
  --config-name NAME    Name of the configuration file directory (default:
                        .merk)
  --qtstyle NAME        Set Qt widget style (default: Windows)

Miscellaneous:
  -N, --noask           Don't ask for connection information on start
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

