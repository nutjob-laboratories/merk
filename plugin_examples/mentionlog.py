from merk import Plugin

class MentionLogPlugin(Plugin):

    NAME = "Mention Log"
    AUTHOR = "Dan Hetrick"
    VERSION = "1.0"
    SOURCE = "https://github.com/nutjob-laboratories/merk"

    def init(self):
        c = self.console()
        c.html("<h1>Mention Log</h1>")

    def message(self,**args):
        window = args["window"]
        client = args["client"]
        channel = args["channel"]
        user = args["user"]
        nickname = args["nickname"]
        hostmask = args["hostmask"]
        message = args["message"]
        
        c = self.console()
        if client.nickname in message:
            entry = f"{client.hostname} {channel} {nickname}: {message}"
            c.print(entry)