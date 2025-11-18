from merk import Plugin

class AwayNotify(Plugin):

    NAME = "Away Notify"
    AUTHOR = "Dan Hetrick"
    VERSION = "1.0"
    SOURCE = "https://github.com/nutjob-laboratories/merk"

    def init(self):
        self.notified = []

    def ctick(self,**args):
        uptime = args["uptime"]

        for client in self.clients():
            if self.is_away(client):
                if not client in self.notified:
                    self.notified.append(client)
                    for window in self.windows(client):
                        window.describe("is now away")
            else:
                if client in self.notified:
                    self.notified.remove(client)
                    for window in self.windows(client):
                        window.describe("is now back")