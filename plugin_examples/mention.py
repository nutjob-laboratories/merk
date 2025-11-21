from merk import Plugin

class MentionNotify(Plugin):

    NAME = "Mention Notification"
    AUTHOR = "Dan Hetrick"
    VERSION = "1.0"
    SOURCE = "https://github.com/nutjob-laboratories/merk"

    def init(self):
        self.notified = []

    def message(self,**args):
        window = args["window"]
        channel = args["channel"]
        user = args["user"]
        message = args["message"]
        client = args["client"]

        if window!=None:
            if window.type()!="server":
                if client.nickname in message:
                    if not channel in self.notified:
                        if not window.active():
                            self.notified.append(channel)
                            window.title(window.name()+" - Mentioned")

    def activate(self,**args):
        window = args["window"]
        if window.name() in self.notified:
            self.notified.remove(window.name())
            window.title(window.name())