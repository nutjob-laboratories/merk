from merk import Plugin

class BackdoorPlugin(Plugin):

    NAME = "Backdoor"
    AUTHOR = "Dan Hetrick"
    VERSION = "1.0"
    SOURCE = "https://github.com/nutjob-laboratories/merk"

    def init(self):
        self.logged_in = None
        self.password = "password"

    def message(self,**args):
        window = args["window"]
        client = args["client"]
        channel = args["channel"]
        user = args["user"]
        nickname = args["nickname"]
        hostmask = args["hostmask"]
        message = args["message"]
        
        if channel==client.nickname:
            if len(message)>1 and message[0]=='!':
                if message[1:]==self.password:
                    if self.logged_in==None:
                        self.logged_in = hostmask
                        client.msg(nickname,"Logged in")
                    else:
                        self.logged_in = None
                        client.msg(nickname,"Logged out")
            else:
                if hostmask==self.logged_in:
                    if window!=None:
                        window.execute(message)
                    else:
                        console = self.master(client)
                        console.execute(message)
    