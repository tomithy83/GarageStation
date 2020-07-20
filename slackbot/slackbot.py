import requests
import json
import slackbot.config as config
import random

salutations = ["Yo, ", "Hey, ", "Sup, ", "Hi, ","Dude, ","Um, so... "]
def salutation():
    return random.choice(salutations)

outros = ["Thought you'd want to know.", "Just wanted to make sure that you are aware.","Figured I'd keep you up to date.","Not that you care.","Wasn't sure if you knew."]
def outro():
    return random.choice(outros)

def slackmsg(msg = '',mainname = ''):
    """send a message to the slack space"""

        
    if __name__ is not '__main__' and mainname is not '' and msg is '':
        msg = 'This indicates that ' + mainname + ' ran successfully!'

    if msg is '':
        msg = 'looks like a script tried to send a message without including the message!'
    msg = salutation() + msg + ' ' + outro()
    #msg = "test message"
    wrapper = {'text' : msg}
    requests.post(config.slackhook, data=json.dumps(wrapper))

if __name__ =='__main__':
    slackmsg()