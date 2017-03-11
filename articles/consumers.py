# In consumers.py
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

import json

# Connected to websocket.connect
from articles.models import Session


@channel_session_user_from_http
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})

    # Print the path
    print(message.content['path'])

    # Work out room name from path (ignore slashes)
    chatroom = message.content['path'].split('/')[2]

    # Save room in session and add us to the group
    message.channel_session['chatroom'] = chatroom

    print('ChatRoom: ' + chatroom)

    Group("chatroom-%s" % chatroom).add(message.reply_channel)

# Connected to websocket.receive
@channel_session_user
def ws_message(message):

    # Convert data to dict
    data = json.loads(message['text'])

    # Get session id
    session_id = message.channel_session['chatroom']

    # Get the session
    session = Session.objects.get(pk=session_id)

    # print data['========== Code ==========']
    session.code = data['code']

    # Save the session
    session.save()

    Group("chatroom-%s" % message.channel_session['chatroom']).send({
        "text": message['text']
    })

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['chatroom']).discard(message.reply_channel)