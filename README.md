# mƏrk IRC Client

**mƏrk** is a graphical open source [Internet relay chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat) client. The current development version is **001.004**. It uses a [multiple document interface](https://en.wikipedia.org/wiki/Multiple-document_interface), much like the popular Windows IRC client [mIRC](https://www.mirc.com/).  **mƏrk** is written in Python 3, using the [PyQt5](https://pypi.org/project/PyQt5/) and [Twisted](https://twistedmatrix.com/trac/) libraries, and runs on both Windows and Linux.

**mƏrk** is *extremely* alpha, and is not currently usable for chatting on IRC.

# Requirements

**mƏrk** requires Python 3, [PyQt5](https://pypi.org/project/PyQt5/), and [Twisted](https://twistedmatrix.com/trac/). PyQt5 and Twisted can be installed by using [**pip**](https://pypi.org/project/pip/):

    pip install pyqt5
    pip install Twisted

To connect to IRC servers via SSL, two additional libraries are needed:

    pip install pyOpenSSL
    pip install service_identity

**mƏrk** is being developed with Python 3.7 on Windows 11, and Python 3.8.5 on Linux Mint.

If you're running Windows, and you're getting errors when trying to run **mƏrk**, you may have to install another library, [pywin32](https://pypi.org/project/pywin32/). You can also install this with [**pip**](https://pypi.org/project/pip/):

    pip install pywin32
 To run properly on Linux, the latest version of all required software is recommended.  There is one library that comes bundled with **mƏrk**:
 - [qt5reactor](https://github.com/twisted/qt5reactor)

# Running mƏrk

First, make sure that all the requirements are installed. Next, [download **mƏrk**](https://github.com/nutjob-laboratories/merk/raw/main/downloads/merk-latest.zip). Extract the zipfile to a directory of your choice using your favorite archive/zip program. Open a command prompt, navigate to the directory you extracted **mƏrk** to, and type:

    python merk.py

# Developing mƏrk

Several tools are included in [the official **mƏrk** repository](https://github.com/nutjob-laboratories/merk) for developing **mƏrk**. The [`pyrcc5` utility](https://manpages.ubuntu.com/manpages/xenial/man1/pyrcc5.1.html) is required, and should be installed automatically when you install PyQt. These are only needed if you're developing **mƏrk**, and can be ignored if you're only using the **mƏrk** IRC client.

 - ***compile_resources.bat*** - This batch file compiles the miscellaneous resources (graphics, fonts, etc) required by **mƏrk** into a single file, `resources.py`, and inserts the file into the mƏrk source code. This is for development on the Windows platform.
 - ***compile_resources.sh*** - This shell script basically does the same thing that `compile_resources.bat` does, only it's for development on the Linux platform.
 - ***build_dist.py*** - This is a Python 3 script that, when executed, does several things:
	 - Executes either `compile_resources.bat` (if the host system is Windows) or `compile_resources.sh` (if the host system is Linux); if the host system is not running either Windows or Linux, `build_dist.py` will exit with an error
	 - Increments the **mƏrk**'s minor version (which is stored in `merk/data/minor.txt`) and saves it
	 - Reads`README.txt` into memory and replaces several symbols in it:
		 - `! _VERSION_ !` (without spaces) is replaced with **mƏrk**'s major version
		 - `! _MINOR_ !` (without spaces) is replaced with **mƏrk**'s minor version
		 - `! _FULL_VERSION_ !` (without spaces) is replaced with **mƏrk**'s major and minor version, with a period in between them.
	 - Overwrites `README.md` with the edited contents of `README.txt`
	 - Creates a new directory named `dist`, and copies into it:
		 - `merk.py`
		 - `LICENSE`
		 - `README.md`
		 - The `merk` directory and its contents
		 - The `qt5reactor` directory and its contents
	 - Zips up the `dist` directory either using [PowerShell](https://en.wikipedia.org/wiki/PowerShell) (if the host system is Windows) or the [zip](https://linux.die.net/man/1/zip) utility (if the host system is Linux) into a file named `dist.zip`
	 - Deletes the `dist` directory and its contents
	 - Renames `dist.zip` to "merk-*MAJOR VERSION*.zip", referred to as `merk.zip` in this description.
	 - If `merk.zip` exists in the `downloads` directory, the version in the `downloads` directory is deleted
	 - If `merk-latest.zip` exists in the `downloads` directory, it is deleted
	 - `merk.zip` is copied into the `downloads` directory, and is copied to `merk-latest.zip`

[//]: # (End of document)
