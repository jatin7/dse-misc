#from sopel import module
import sopel
import time
from random import randint
from sopel.module import commands, event, rule
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

#Configuration
contactpoints = ['1.2.3.4']
auth_provider = PlainTextAuthProvider (username='whois', password='Wh0D4t23')
keyspace = "whois"
chanmin = 40
NETWORK = "ircnetworkname"

#BOT Startup Logic
chanlist = []

print "Connecting to cluster"
cluster = Cluster( contact_points=contactpoints,
                   auth_provider=auth_provider )

session = cluster.connect(keyspace)

#Bot Running Logic
def send_whois(bot, nick):
    """
    Sends the WHOIS command to the server for the
    specified nick.
    """
    time.sleep(randint(10,420))
    nick1 = nick.replace("@","")
    nick = nick.replace("+","")
    bot.write(["WHOIS", nick])
    #bot.say("whois sent: " + nick)

def send_names(bot, channel):
    """
    Sends the NAMES command to the server for the
    specified channel.
    """
    bot.write(["NAMES", channel])

def check_chan(bot, channel):
    """
    new channel auto join logic
    """
    global chanlist
    known = 0
    #print("running new channel logic on: ")
    #print(channel)
    for c in chanlist:
        #print("channel: %s || c: %s") % (channel, c)
        if(channel == c):
           known = 1
           #print("Channel %s already known!") % channel
    if(known == 0):
       print("New channel %s found, joining!") % channel
       chanlist += [channel]
       bot.join(channel)

@event('319')
@rule('.*')
def whois_channels_found(bot, trigger):
    """
    Whois Channel Info
    """
    list1 = trigger.raw.split(":")
    channels = list1[2]
    clist = channels.split()
    list1 = trigger.raw.split()
    nick = list1[3]
    for c in clist:
        l = c.split("#")
        mode = l[0]
        channel = l[1]
        cname = "#" + channel
	check_chan(bot,cname)
        #print ("INSERT INTO whois.chan (network, nick, channel, ts, mode) VALUES ('%s', '%s', '%s', now(), '%s')") %  (NETWORK, nick, channel, mode)
        session.execute (""" INSERT INTO whois.chan (network, nick, channel, ts, mode) VALUES (%s, %s, %s, now(), %s); """, (NETWORK, nick, channel, mode))

@event('353')
@rule('.*')
def names_found(bot, trigger):
    """
    NAMES response
    """
    #print(trigger.raw)
    list1 = trigger.raw.split(":")
    list2 = trigger.raw.split()
    names = list1[2].split()
    channel = list2[4]
    print("people in %s: %s") % (channel, len(names))
    ##print("sending whois")
    for i in names:
       n1 = i.replace("@", "")
       n2 = n1.replace("+", "")
       print("whoising: %s") % n2
       send_whois(bot, n2)
       time.sleep(45)
    print(len(names), chanmin)
    if(len(names) < chanmin):
       print("Parting %s") % channel
       bot.part(channel)
    else:
       print("staying in %s") % channel


@event('311')
@rule('.*')
def whois_info_found(bot, trigger):
    """
    Whois User info
    """
    list1 = trigger.raw.split(":")
    list2 = trigger.raw.split()
    realn = list1[2]
    nick = list2[3]
    ident = list2[4]
    hostname = list2[5]
    print ("INSERT INTO whois.info (network, nick, identd, hostname, realname, ts) VALUES ('%s', '%s', '%s', '%s', '%s', now())") %  (NETWORK, nick, ident, hostname, realn)
    session.execute (""" INSERT INTO whois.info (network, nick, identd, hostname, realname, ts) VALUES (%s, %s, %s, %s, %s, now()); """, (NETWORK, nick, ident, hostname, realn))

@event('JOIN')
@rule('.*')
def on_join_whois(bot, trigger):
    """
    Trigger on join
    """
    l1 = trigger.raw.split()
    channel = l1[2]
    if(bot.nick == trigger.nick):
        send_names(bot, channel)
        print("bot has joined: %s") % channel
    send_whois(bot, trigger.nick)
