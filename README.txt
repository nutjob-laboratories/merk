# mƏrk IRC Client

**mƏrk** is a graphical open source [Internet relay chat](https://en.wikipedia.org/wiki/Internet_Relay_Chat) client. The current development version is **!_FULL_VERSION_!**. It uses a [multiple document interface](https://en.wikipedia.org/wiki/Multiple-document_interface), much like the popular Windows IRC client [mIRC](https://www.mirc.com/).  **mƏrk** is written in Python 3, using the [PyQt5](https://pypi.org/project/PyQt5/) and [Twisted](https://twistedmatrix.com/trac/) libraries, and runs on both Windows and Linux.

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

First, make sure that all the requirements are installed. Next, [download **mƏrk**](https://github.com/nutjob-laboratories/merk/raw/master/downloads/merk-latest.zip). Extract the zipfile to a directory of your choice using your favorite archive/zip program. Open a command prompt, navigate to the directory you extracted **mƏrk** to, and type:

    python merk.py
