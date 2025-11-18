from merk import Plugin

import random

def roll(nick,window,dice):
    try:
        dice = int(dice)
    except:
        window.say("!roll requires a number argument")
        return
    roll = random.randint(1,dice)
    window.say(f"{nick} rolled a d{dice}: {roll}")

def raw_roll(nick,client,dice):
    try:
        dice = int(dice)
    except:
        client.msg(nick,"!roll requires a number argument")
        return
    roll = random.randint(1,dice)
    client.msg(nick,f"{nick} rolled a d{dice}: {roll}")

class DiceRoller(Plugin):

    NAME = "Dice Roller"
    AUTHOR = "Dan Hetrick"
    VERSION = "1.0"
    SOURCE = "https://github.com/nutjob-laboratories/merk"

    def me(self,**args):
        window = args["window"]
        message = args["message"]
        client = args["client"]
        nick = client.nickname
        
        tokens = message.split()
        if len(tokens)==2:
            if tokens[0].lower()=="!roll":
                tokens.pop(0)
                dice = tokens.pop(0)
                if window!=None:
                    roll(nick,window,dice)

    def message(self,**args):
        window = args["window"]
        message = args["message"]
        nick = args["nickname"]
        client = args["client"]

        tokens = message.split()
        if len(tokens)==2:
            if tokens[0].lower()=="!roll":
                tokens.pop(0)
                dice = tokens.pop(0)
                if window!=None:
                    roll(nick,window,dice)
                else:
                    raw_roll(nick,client,dice)