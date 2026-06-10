<p align="center">
  <img src="./graphics/banner.png"><br>
  <b><big>MERK Command Reference</big></b><br>
  <i>Every command, command-line option, and formatting code in MERK</i><br><br>
  <a href="./README.md">&larr; Back to the README</a> &nbsp;|&nbsp; <a href="./MERK_User_Guide.pdf">MERK User Guide (PDF)</a>
</p>

- [Command-Line Usage](#command-line-usage)
- [Commands](#commands)
- [MERK "Markdown"](#merk-markdown)

# Command-Line Usage

All command-line arguments work on all versions of **MERK** (Python, Windows executable, Linux executable, and Flatpak).

```
usage: python merk.py [--ssl] [-p PASSWORD] [-c CHANNEL[:KEY]] [-a NICKNAME]
                      [-C SERVER:PORT[:PASSWORD]] [-n NICKNAME] [-u USERNAME]
                      [-S SERVER:PORT[:PASSWORD]] [-r REALNAME] [-h] [-d] [-x] 
                      [-t] [-R] [-o] [-P] [-f] [-s FILENAME][--config-name NAME] 
                      [--config-directory DIRECTORY] [--config-local] [-D] [-L]
                      [--scripts-directory DIRECTORY] [--user-file FILENAME] [-E]
                      [--config-file FILENAME] [--reset] [--reset-user] [-Q NAME]
                      [--reset-all] [--uninstall [FILE]] [--install FILE] [-N] [-A]
                      [SERVER] [PORT]


Connection:
  SERVER                Server to connect to
  PORT                  Server port to connect to (6667)
  --ssl, --tls          Use SSL/TLS to connect to IRC
  -p, --password PASSWORD
                        Use server password to connect
  -c, --channel CHANNEL[:KEY]
                        Join channel on connection
  -C, --connect SERVER:PORT[:PASSWORD]
                        Connect to server via TCP/IP
  -S, --connectssl SERVER:PORT[:PASSWORD]
                        Connect to server via SSL/TLS

User Information:
  -n, --nickname NICKNAME
                        Use this nickname to connect
  -u, --username USERNAME
                        Use this username to connect
  -a, --alternate NICKNAME
                        Use this alternate nickname to connect
  -r, --realname REALNAME
                        Use this realname to connect

Options:
  -h, --help             Show help and usage information
  -d, --donotsave        Do not save new user settings
  -x, --donotexecute     Do not execute connection script
  -N, --noprofile        Do not use server profile
  -A, --nosasl           Do not use SASL login
  -t, --reconnect        Reconnect to servers on disconnection
  -R, --run              Don't ask for connection information on start
  -o, --on-top           Application window always on top
  -f, --full-screen      Application window displays full screen
  -s, --script FILE      Use a file as a connection script
  -P, --disable-plugins  Disables plugins
  -E, --enable-plugins   Enables plugins

Files and Directories:
  --config-name NAME    Name of the configuration file directory (default: .merk)
  --config-directory DIRECTORY
                        Location to store configuration files
  --config-local        Store configuration files in install directory
  --scripts-directory DIRECTORY
                        Location to look for script files
  --user-file FILE      File to use for user data
  --config-file FILE    File to use for configuration data
  --reset               Reset configuration file to default values
  --reset-user          Reset user file to default values
  --reset-all           Reset all configuration files to default values
  --uninstall [FILE]    Deletes an installed plugin
  --install FILE        Install plugin ZIP or Python module

Appearance:
  -Q, --qtstyle NAME    Set Qt widget style (default: Windows)
  -D, --dark            Run in dark mode
  -L, --light           Run in light mode
```

# Commands

All of these commands can be issued in the client or from scripts, unless otherwise noted. Commands that do not start with `/` can only be issued in scripts. Commands that start with `/_` are commands that are usually limited to [IRCops](https://en.wikipedia.org/wiki/IRC_operator), and usually display all output in server windows.

| Commands                                | Description                                                                                                                      |
|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| `/admin [SERVER]`                       | Requests administration information from the server  |
| `/alias [TOKEN] [TEXT...]`                  | Creates an alias that can be referenced by `$TOKEN`. Call with only `TOKEN` as an argument to see `TOKEN`'s value. If `TEXT` is a mathematical statement, it will be evaluated and the result used as the alias' value. Operations supported are parenthesis, addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), modulus (`%`), and exponents(`**`). Call without any arguments to see all aliases and their values                                                                              |
| `append FILENAME CONTENTS...`            | Appends `CONTENTS`to `FILENAME`, followed by a newline. *Can only be called by scripts*                                                        |
| `/away [SERVER] [MESSAGE]`                       | Sets status as "away". To specify what server to set the "away" status on, pass a hostID (the host and port used to connect to the server, in the format `host:port`, or the hostname used to connect) as `SERVER`       |
| `/back [SERVER]`                                 | Sets status as "back". To specify what server to set the "back" status on, pass a hostID (the host and port used to connect to the server, in the format `host:port`, or the hostname used to connect) as `SERVER`       |
| `/bind SEQUENCE COMMAND...`           | Executes `COMMAND` every time key `SEQUENCE` is pressed. Pass `save` as the only argument to save binds to the configuration file                                                                                                           |
| `/browser URL`           | Opens `URL` in the default browser  |
| `/call METHOD [ARGUMENTS...]`         | Executes `METHOD` in any plugin that contains that `METHOD`  |
| `/clear [SERVER] [WINDOW]`              | Clears a window's chat display. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `WINDOW` to clear the server window  |
| `/close [SERVER] [WINDOW]`              | Closes a subwindow. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `WINDOW` to hide the server window                    |
| `/config [SETTING] [VALUE...]`          | Changes a setting, or searches and displays one or all settings in the configuration file.  **Caution**: use at your own risk! |
| `/config export [FILENAME]`          | Exports the current configuration file.  **Caution**: use at your own risk! |
| `/config import [FILENAME]`          | Imports a configuration file into settings.  **Caution**: use at your own risk! |
| `/_connect SERVER PORT [REMOTE]`     | Instructs a server to connect to another server. May only be issued by server operators |
| `/connect SERVER [PORT] [PASSWORD]`     | Connects to an IRC server                                                                                                        |
| `/connectssl SERVER [PORT] [PASSWORD]`  | Connects to an IRC server via SSL                                                                                                |
| `context [HOSTID] WINDOW_NAME`                  | Moves execution of the script to `WINDOW_NAME`. To specify what server `WINDOW_NAME` is connected to, pass a `HOSTID` as the first argument. *Can only be called from scripts*                                                  |
| `/ctcp REQUEST USER`                  | Sends a CTCP request to `USER`; valid `REQUEST`s are TIME, VERSION, USERINFO, SOURCE, or FINGER                                                  |
| `decimal ALIAS LOW HIGH MESSAGE...`     | Requests a decimal number from the user, between `LOW` and `HIGH`, in a dialog (with `MESSAGE`), and stores the input in `ALIAS`. If the user cancels the dialog, `ALIAS` will be set to `*`. This command is blocking. *Can only be called by scripts*    |
| `/delay SECONDS COMMAND...`                  | Executes `COMMAND` after `SECONDS` seconds                                                 |
| `/_die`                  | Instructs the server to shut down. May only be issued by server operators                               |
| `/edit [FILENAME]`                      | Opens a script in the editor                                                                                                     |
| `end`                                  | Immediately ends a script; *can only be called from scripts*                                                                       |
| `/error [SERVER] [WINDOW] TEXT...`     | Prints an error message to a window, and immediately exits a script if called from a script. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `SERVER` to print to all open windows. Pass `*` as `WINDOW` to print to the server window     |
| `escape ALIAS TEXT...`       | Escapes MERK markdown in `TEXT`, and stores it in `ALIAS`; *can only be called from scripts*             |
| `exclude WINDOW...`                       | Prevents a script from executing in `WINDOW`'s context. Multiple `WINDOW`s can be specified. *Can only be called from scripts*              |
| `/exit [SECONDS]`                       | Exits the client, with an optional pause of `SECONDS` before exit                                                                |
| `/fade [SERVER] [WINDOW] PERCENTAGE`    | Sets transparency of a subwindow by `PERCENTAGE`. `SERVER` is optional if `WINDOW` belongs to the same context. Call without arguments to see current subwindow's transparency. Pass `*` as `WINDOW` to set the transparency of the server window     |
| `/find [TERMS]`                         | Finds filenames that can be found by other commands; use * for multi-character wildcards, and ? for single character wildcards   |
| `/folder PATH`              | Opens `PATH` in the default file manager               |
| `getfile ALIAS MESSAGE...`           | Shows an "open file" dialog, and stores the result in `ALIAS`. If no file is set, `ALIAS` will be set to `*`. This command is blocking. *Can only be called by scripts*            |
| `goto TARGET`                         | Moves execution of the script to `TARGET`. One of the only script-only commands that can be issued from an `if` command. *Can only be called from scripts*  |
| `halt [MESSAGE...]`                       | Asks the user if they want to halt the script's execution, and displays an error `MESSAGE`. One of the only script-only commands that can be issued from an `if` command. *Can only be called from scripts*       |
| `/help [COMMAND]`                                 | Displays command usage information                  |
| `/hide [SERVER] [WINDOW]`                                 | Hides a subwindow. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `WINDOW` to hide the server window      |
| `/highlight WORD [COLOR]`                                 | Highlights `WORD` with `COLOR` in chat. `COLOR` must be a valid 6 digit web color. Call without any arguments to see a list of highlighted words. Call without a `COLOR` argument to select a color with the GUI  |
| `hostmask ALIAS NICKNAME`                       | Retrieves the hostmask of `NICKNAME` and stores it in `ALIAS`. If the hostmask is not known or cannot be found, `ALIAS` is set to `unknown`. *Can only be called from scripts*       |
| `if VALUE1 OPERATOR VALUE2 COMMAND...`       | Executes `COMMAND` if `VALUE1` and `VALUE2` are true, depending on `OPERATOR`. Valid `OPERATOR`s are `(is)` (result is true if `VALUE1` and `VALUE2` are equal), `(not)` (result is true if `VALUE1` and `VALUE2` are not equal), `(in)` (result is true if `VALUE1` is contained in `VALUE2`), `(nin)` (result is true if `VALUE1` is not contained in `VALUE2`), `(gt)` (result is true if `VALUE1` is a greater number than `VALUE2`; if either value is a string, the length of that string will be used as the value), `(lt)` (result is true if `VALUE1` is a lesser number than `VALUE2`; if either value is a string, the length of that string will be used as the value), `(ne)` (result is true if `VALUE1` is not an equal number to `VALUE2`; if either value is a string, the length of that string will be used as the value), and `(eq)` (result is true if `VALUE1` is an equal number to `VALUE2`; if either value is a string, the length of that string will be used as the value). *Can only be called from scripts*    |
| `/ignore USER`                          | Hides a `USER`'s chat; use `*` as multiple character wildcards, and `?` as single character wildcards                                                                                                           |
| `/info [TARGET]`                          | Requests server information                         |
| `input ALIAS MESSAGE...`               | Requests input from the user in a dialog (with `MESSAGE`), and stores the input in `ALIAS`. If the user cancels the dialog or doesn’t input anything, `ALIAS` will be set to `*`. This command is blocking. *Can only be called from scripts*                     |
| `insert FILE [FILE...]`              | Inserts the contents of `FILE` where it appears in the script; *Can only be called by scripts*            |
| `/invite NICKNAME CHANNEL`              | Sends a channel invitation                                   |
| `/ison NICKNAME(S)...`              | Displays if the specified nicknames are online          |
| `/join CHANNEL [KEY]`                   | Joins a channel                                                                                                                  |
| `/kick CHANNEL NICKNAME [MESSAGE]`      | Kicks a user from a channel                                          |
| `/_kill CLIENT COMMENT...`      | Forcibly removes `CLIENT` from the network. May only be issued by IRC operators                     |
| `/knock CHANNEL [MESSAGE]`              | Requests an invitation to a channel                                                                                              |
| `/links [REMOTE [MASK]]`                         | Requests a list of servers the server is connected to |
| `/list [TERMS]`                         | Lists or searches channels on the server; use `*` for multi-character wildcard and `?` for single character wildcard                      |
| `loop COUNT`                         | Begins a `loop` block, executing any scripting until the script encounters a `pool` command, before moving execution back to the line after the `loop` call. The code in between `loop` and `pool` will be repeated `COUNT` times. *Can only be called from scripts* |
| `/lusers [MASK [SERVERS]]`                         | Requests statistics about the server |
| `/macro NAME SCRIPT [USAGE] [HELP]`               | Creates a macro, executable with `/NAME`, that executes `SCRIPT`                                            |
| `/maximize [SERVER] [WINDOW]`             | Maximizes a subwindow. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `WINDOW` to maximize the server window         |
| `/me MESSAGE...`                        | Sends a CTCP action message to the current chat                                                                                  |
| `/minimize [SERVER] [WINDOW]`             | Minimizes a subwindow. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `WINDOW` to minimize the server window                    |
| `/mode TARGET MODE...`                  | Sets a mode on a channel or user                                                                                                 |
| `/move [SERVER] [WINDOW] X Y` | Moves a subwindow to `X` (left and right) and `Y` (up and down) coordinates. `SERVER` is optional if `WINDOW` belongs to the same context. Call without arguments to see the current subwindow's coordinates. Pass `*` as `WINDOW` to move the server window      |
| `/msg TARGET MESSAGE...`                | Sends a message                                                                                                                  |
| `msgbox MESSAGE...`                    | Displays a messagebox with a short message. This command is blocking. One of the only script-only commands that can be issued from an `if` command. *Can only be called from scripts*             |
| `/nick NEW_NICKNAME`                    | Changes your nickname                                                                                                            |
| `/notice TARGET MESSAGE...`             | Sends a notice                                                                                                                   |
| `number ALIAS LOW HIGH MESSAGE...`     | Requests number from the user, between `LOW` and `HIGH`, in a dialog (with `MESSAGE`), and stores the input in `ALIAS`. If the user cancels the dialog, `ALIAS` will be set to `0*`. This command is blocking. *Can only be called by scripts*    |
| `only WINDOW...`                       | Restricts a script to only executing in `WINDOW`'s context. Multiple `WINDOW`s can be specified. *Can only be called from scripts*              |
| `/oper USERNAME PASSWORD`               | Logs into an operator account                                                                                                    |
| `/part CHANNEL [MESSAGE]`               | Leaves a channel                                                                                                                 |
| `/ping USER [TEXT]`                     | Sends a CTCP ping to a user                                                                                                      |
| `/play FILENAME`                        | Plays a WAV file                                                                                                                 |
| `pool`                        | Ends a `loop` block. *Can only be called from scripts*      |
| `/print [SERVER] [WINDOW] TEXT...`               | Prints text to a window. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `SERVER` to print to all open windows. Pass `*` as `WINDOW` to print to the server window                                                                       |
| `/prints [SERVER] [WINDOW] TEXT...`               | Prints system message to a window. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `SERVER` to print to all open windows. Pass `*` as `WINDOW` to print to the server window              |
| `/private NICKNAME [MESSAGE]`               | Opens a private chat subwindow for `NICKNAME`                             |
| `/python [FILENAME]`               | Opens a file in the Python editor                             |
| `/quit [MESSAGE]`                       | Disconnects from the current IRC server                                                                                          |
| `/quitall [MESSAGE]`                       | Disconnects from all IRC servers                                                                                          |
| `/quote [SERVER] TEXT...`                          | Sends unprocessed data to the current or another server. To specify what server to send the data to, pass a hostID (the host and port used to connect to the server, in the format `host:port`, or the hostname used to connect) as `SERVER` |
| `random ALIAS START FINISH`              | Generates a random integer from `START` to `FINISH`, and stores it in `ALIAS`. *Can only be called by scripts*            |
| `read ALIAS FILENAME`              | Reads `FILENAME` as a text file, and stores the contents in `ALIAS`. If the file is empty or contains only whitespace, `ALIAS` will be set to `*`. This command is blocking. *Can only be called by scripts*            |
| `/reconnect SERVER [PORT] [PASSWORD]`     | Connects to an IRC server, reconnecting on disconnection                                                   |
| `/reconnectssl SERVER [PORT] [PASSWORD]`  | Connects to an IRC server via SSL, reconnecting on disconnection                                         |
| `/refresh`                              | Requests a new list of channels from the server                                                                                  |
| `/_rehash`                              | Causes the server to reprocess and reload configuration files. May only be issued by IRC operators |
| `/reload`              | Reloads the configuration file, and attempts to apply as many settings as possible      |
| `/rem [TEXT...]`                        | Does nothing. Can be used for comments                                                     |
| `/rerender [SERVER] [WINDOW]`              | Re-renders the chat log of a window. Pass `*` as the only argument to re-render all open chat windows          |
| `restrict SERVER`\|`CHANNEL`\|`PRIVATE`     | Prevents a script from running if it is not being ran in a `SERVER`, `CHANNEL`, or `PRIVATE` window. Up to two window types can be passed. *Can only be called from scripts*                                                                                |
| `/restore [SERVER] [WINDOW]`              | Restores a subwindow. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `WINDOW` to restore the server window                                 |
| `setfile ALIAS MESSAGE...`           | Shows a "save file" dialog, and stores the result in `ALIAS`. If no file is set, `ALIAS` will be set to `*`. This command is blocking. *Can only be called by scripts*            |
| `/script FILENAME [ARGUMENTS]`                      | Executes a list of commands in a file                                                                                            |
| `/show [SERVER] [WINDOW]`               | Shows a subwindow, if hidden, and shifts focus to that subwindow. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `WINDOW` to show the server window  |
| `/size [SERVER] [WINDOW] WIDTH HEIGHT` | Resizes a subwindow. `SERVER` is optional if `WINDOW` belongs to the same context. Call without arguments to see current subwindow's size. Pass `*` as `WINDOW` to resize the server window |
| `/style [SERVER] [WINDOW]`                                | Opens a window's text style editor. Pass `*` as `WINDOW` to select the server window                                  |
| `target LABEL`                                 | Creates a target for the `goto` command. If used as a target for `goto`, script execution will move to the line this appears on. `LABEL` cannot contain spaces. Can only be called from scripts      |
| `/time`                                 | Requests server time                                                                                                             |
| `/toggle FEATURE`                                 | Toggles an input feature. Valid `FEATURE`s are `asciimoji`, `color`, `emoji`, `markdown`, and `protection`                                         |
| `/topic CHANNEL NEW_TOPIC`              | Sets a channel topic                                                                                                             |
| `/_trace TARGET`              | Executes a trace on a server or user. May only be issued by server operators |
| `/unalias TOKEN`                        | Deletes the alias referenced by `$TOKEN`. Does nothing in scripts                            |
| `/unbind SEQUENCE`                        | Removes a bind for `SEQUENCE`. To remove all binds, pass `*` as the argument                                                        |
| `/unhighlight WORD`                        | Removes highlighting for `WORD`. Call without arguments to see a list of all highlighted words. Pass `*` as the only argument to remove all word highlights  |
| `/unignore USER`                        | Un-hides a `USER`'s chat. To un-hide all users, use `*` as the argument                                                         |
| `/unmacro NAME`                        | Deletes the macro named `NAME`  |
| `usage NUMBER [MESSAGE...]`            | Prevents a script from running unless `NUMBER` arguments are passed to it, and displays `MESSAGE`. If the script can take one or more arguments, pass `+` as `NUMBER`. *Can only be called by scripts*                                                        |
| `/user [SETTING] [VALUE...]`          | Changes a user setting, or searches and displays one or all settings in the user configuration file. Pass `*` as `VALUE` to set a setting as blank. ***Caution**: use at your own risk! |
| `/userhost NICK(S)...`          | Requests information about users from the server |
| `/version [SERVER]`                     | Requests server version                                                                                                          |
| `wait SECONDS`                         | Pauses script execution for `SECONDS`; *can only be called from scripts*                                                           |
| `/wallops MESSAGE`                         | Sends a message to all operators  |
| `/warn [SERVER] [WINDOW] TEXT...`               | Prints an error message to a window. `SERVER` is optional if `WINDOW` belongs to the same context. Pass `*` as `SERVER` to print to all open windows. Pass `*` as `WINDOW` to print to the server window     |
| `/who NICKNAME [o]`                     | Requests user information from the server                                                                                        |
| `/whois NICKNAME [SERVER]`              | Requests user information from the server                                                                                        |
| `/whowas NICKNAME [COUNT] [SERVER]`     | Requests information about previously connected users                                                                            |
| `/window [COMMAND] [X] [Y]`     | Manipulates the main application window. Valid commands are `cascade`, `fade`, `fullscreen`, `hotkey`,  `ignore`, `install`, `layout`, `logs`, `maximize`, `minimize`, `move`, `next`, `ontop`, `pause`, `plugin`, `previous`, `readme`, `restart`, `restore`, `settings`, `size`, `tile`, and `uninstall`. Call with no arguments to see main window information and a list of subwindows                                                 |
| `write FILENAME CONTENTS...`            | Writes `CONTENTS`to `FILENAME`, followed by a newline. *Can only be called by scripts*                                                        |
| `/xconnect SERVER [PORT] [PASSWORD]`    | Connects to an IRC server &amp; executes connection script                                                                       |
| `/xconnectssl SERVER [PORT] [PASSWORD]` | Connects to an IRC server via SSL &amp; executes connection script                                                               |
| `/xreconnect SERVER [PORT] [PASSWORD]`    | Connects to an IRC server &amp; executes connection script, reconnecting on disconnection                                                                       |
| `/xreconnectssl SERVER [PORT] [PASSWORD]` | Connects to an IRC server via SSL &amp; executes connection script, reconnecting on disconnection                                                              |

# MERK "Markdown"

You can easily "inject" IRC colors and formatting into chat and topics using **MERK** "markdown" (also called **MERKdown** by users).

To insert IRC colors, open a chat message with `<NUMBER` (to set the foreground color of the chat), or `<NUMBER,NUMBER` (to set the foreground and background colors of the chat, respectively). `NUMBER` can be any number from 0 to 15, the "traditional" 16 colors of IRC chat. Stop using the color formatting by "closing" the text with `>`. So, to display the words "Hello world!" in white on a red background, you'd use `<0,4Hello world!>`.

| Number | Description | HTML Color |
|:------:|:-----------:|:----------:|
| 0      | White       | #FFFFFF    |
| 1      | Black       | #000000    |
| 2      | Blue        | #00007F    |
| 3      | Green       | #009300    |
| 4      | Light Red   | #FF0000    |
| 5      | Brown       | #7F0000    |
| 6      | Purple      | #9C009C    |
| 7      | Orange      | #FC7F00    |
| 8      | Yellow      | #FFFF00    |
| 9      | Light Green | #00FC00    |
| 10     | Cyan        | #009393    |
| 11     | Light Cyan  | #00FFFF    |
| 12     | Light Blue  | #0000FC    |
| 13     | Pink        | #FF00FF    |
| 14     | Grey        | #7F7F7F    |
| 15     | Light Grey  | #D2D2D2    |

You can also use markdown tags! To send text in italics, start (and finish) a message with `*`. For bold, use `**`. To underline text, start and finish with `__`. To send a strikethough, start and finish with `~` (this tag is not supported by all IRC clients, though it will render properly on most modern clients). To send the message "*Hello* **world!**", you'd use `*Hello* **world!**`.

Tags can be nested, so `<5,9***~Hello~ __world!__***>` is a completely valid statement in **MERK** "markdown". The client can be configured to strip colors and formatting from display, but messages sent in "markdown" will still appear with the formatting in clients the message is sent to. In channel windows, topics are automatically changed into "markdown" when the topic is edited via the GUI.

Just like almost everything in **MERK**, "markdown" can be turned off in the settings. More information about "markdown" can be found in the [**MERK** User Guide](./MERK_User_Guide.pdf).

[//]: # (End of document)
