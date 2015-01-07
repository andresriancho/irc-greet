"""
Sends a message to each user that joins.

Features:
    * Remembers who was greeted
    * Blacklist for some users
    * The greeting can also be sent manually by using /greet <nick>

TODO:
    * Make the list of greeted users persistent
"""


__module_name__ = 'ChanGreeter'
__module_version__ = '0.3'
__module_description__ = 'Send a private message when someone joins'

import xchat

BLACKLIST = ['github_bot', 'kost', '__apr__']
GREETING_CHAN = ['#w3af']
GREETING = '''\
Hi, welcome to the #w3af channel. I'm Andres Riancho, w3af's project leader, \
please ask any questions in the main channel and I'll try to answer. Since I'm \
not here all day you might want to wait a few minutes/hours online for me to \
be able to answer. This is an automated response! More info at \
http://docs.w3af.org/en/latest/
'''

already_greeted = []


def send(user, hostmask, word_eol, userdata):
    xchat.command("privmsg %s :%s" % (user, GREETING))
    xchat.emit_print("Notice", "guide", "Greeting sent to %s (%s)." % (user, hostmask))
    return xchat.EAT_ALL


def grab(word, word_eol, userdata):
    channel_joined = word[1]
    user = word[0]
    hostmask = word[2]

    if channel_joined not in GREETING_CHAN:
        return xchat.EAT_NONE

    if user in BLACKLIST:
        return xchat.EAT_NONE

    if user in already_greeted:
        return xchat.EAT_NONE

    already_greeted.append(user)
    send(user, hostmask, word_eol, userdata)
    return xchat.EAT_NONE


xchat.hook_command('greet', send, help='/GREET <nick> manually sends your'
                                       ' greeting to the desired nick')
xchat.hook_print('JOIN', grab)

xchat.prnt('%s v%s loaded' % (__module_name__, __module_version__))
