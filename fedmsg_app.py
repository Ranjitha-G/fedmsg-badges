import fedmsg
import fedmsg.meta
import pprint
import fedmsg.consumers
import fedmsg.config
import logging.config
import socket


# First, load the fedmsg config from fedmsg.d/
config = fedmsg.config.load_config()
irc = config['irc']
port = config['port']
channel = config['channel']
nick = config['nick']

topic_filter = 'fedbadges'

# Then, configure the python stdlib logging to use fedmsg's logging config
logging.config.dictConfig(config.get('logging'))

fedmsg.meta.make_processors(**config)

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect((irc, port))
sck.send('NICK ' + nick + '\r\n')
sck.send('USER ' + nick + ' ' + nick + ' ' + nick + ' :Fedbadges bot\r\n')
sck.send('JOIN ' + channel + '\r\n')

data = ''
while True:
    data = sck.recv(2040)
    if data.find('PING') != -1:
        sck.send('PONG ' + data.split() [1] + '\r\n')
        break

print "Posting up to listen on the fedmsg bus.  Waiting for a message..."
for name, endpoint, topic, msg in fedmsg.tail_messages():
    if topic_filter not in topic:
        continue

    title = fedmsg.meta.msg2title(msg, **config)
    if title is not 'fedbadges.badge.award':
        continue

    subtitle = fedmsg.meta.msg2subtitle(msg, **config)
    link = fedmsg.meta.msg2link(msg, **config)

#    sck.send('PRIVMSG ' + channel + '|' + nick + ' :' + subtitle + ". Congratulations. Checkout the badges here:" + link + '\r\n')
