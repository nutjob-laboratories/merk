from merk import Plugin

class MentionNotify(Plugin):

    NAME = "Unread Notification"
    AUTHOR = "Dan Hetrick"
    VERSION = "1.0"
    SOURCE = "https://github.com/nutjob-laboratories/merk"

    def message(self,**args):
        window = args["window"]
        channel = args["channel"]
        user = args["user"]
        message = args["message"]
        client = args["client"]
        if window!=None:
            if window.type()!="server":
                if window.title()==window.name():
                    if not window.active():
                        window.title(window.name()+" - Unread messages")

    def activate(self,**args):
        window = args["window"]
        if window.title()!=window.name():
            window.title(window.name())