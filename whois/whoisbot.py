from sopel.module import commands, event, rule
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

#Configuration
contactpoints = ['1.2.3.4','4.3.2.1']
auth_provider = PlainTextAuthProvider (username='whois', password='Wh0D4t23')
keyspace = "whois"

print "Connecting to cluster"

cluster = Cluster( contact_points=contactpoints,
                   auth_provider=auth_provider )

session = cluster.connect(keyspace)

NETWORK = "testnet"

def send_whois(bot, nick):
    """
    Sends the WHOIS command to the server for the
    specified nick.
    """
    bot.write(["WHOIS", nick])
    #bot.say("whois sent: " + nick)

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
        #print ("INSERT INTO whois.chan (network, nick, channel, ts, mode) VALUES ('%s', '%s', '%s', now(), '%s')") %  (NETWORK, nick, channel, mode)
        session.execute (""" INSERT INTO whois.chan (network, nick, channel, ts, mode) VALUES (%s, %s, %s, now(), %s); """, (NETWORK, nick, channel, mode))

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
    #print ("INSERT INTO whois.info (network, nick, identd, hostname, realname, ts) VALUES ('%s', '%s', '%s', '%s', '%s', now())") %  (NETWORK, nick, ident, hostname, realn)
    session.execute (""" INSERT INTO whois.info (network, nick, identd, hostname, realname, ts) VALUES (%s, %s, %s, %s, %s, now()); """, (NETWORK, nick, ident, hostname, realn))

@event('JOIN')
@rule('.*')
def on_join_whois(bot, trigger):
    """
    Trigger on join
    """
    #bot.say(trigger.raw)
    send_whois(bot, trigger.nick)
