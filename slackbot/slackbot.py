import requests
import json
import slackbot.config as config

def slackmsg(msg = '',mainname = ''):
    """send a message to the harner slack space"""

        
    if __name__ is not '__main__' and mainname is not '' and msg is '':
        msg = 'This indicates that ' + mainname + ' ran successfully!'

    if msg is '':
        msg = 'Hey, looks like a script tried to send a message without including the message!'

    #msg = "test message"
    wrapper = {'text' : msg}
    requests.post(config.slackhook, data=json.dumps(wrapper))

if __name__ =='__main__':
    slackmsg()