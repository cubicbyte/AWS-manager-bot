from telebot import types
import os
import boto3
import uuid

from ..load_messages import messages

states = {
    'running': 'TEXT_RUNNING',
    'starting': 'TEXT_STARTING',
    'polling': 'TEXT_STOPPING',
    'stopped': 'TEXT_STOPPED'
}

colors = {
    'TEXT_RUNNING': 'COLOR_GREEN',
    'TEXT_STARTING': 'COLOR_YELLOW',
    'TEXT_STOPPING': 'COLOR_ORANGE',
    'TEXT_STOPPED': 'COLOR_RED',
    'TEXT_UNKNOWN': 'COLOR_UNKNOWN'
}

def create_message(message):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(os.getenv('INSTANCE_ID'))

    if not instance.state['Name'] in states:
        state = 'TEXT_UNKNOWN'
    else:
        state = states[instance.state['Name']]

    message_text = messages['COMMAND_MENU'].format(color=messages[colors[state]], state=messages[state], ray_id=str(uuid.uuid4()))
    message_text = message_text.encode('utf-8', 'surrogateescape').decode()
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=messages['BUTTON_START_SERVER'], callback_data='start_instance'),
        types.InlineKeyboardButton(text=messages['BUTTON_STOP_SERVER'], callback_data='stop_instance')
    )

    markup.add(
        types.InlineKeyboardButton(text=messages['BUTTON_REFRESH'], callback_data='menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
