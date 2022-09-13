import boto3
import telebot
import os
import sys
import time

os.chdir(sys.path[0])

from src.load_messages import messages
from src.messages import menu_message, not_whitelisted_message
from src.filters.is_whitelisted import IsWhitelisted
from dotenv import load_dotenv

load_dotenv()



ec2 = boto3.client('ec2')
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
bot.add_custom_filter(IsWhitelisted())



@bot.message_handler(func=lambda m: True, is_whitelisted=False)
@bot.callback_query_handler(func=lambda call: True, is_whitelisted=False)
def not_whitelisted(message):
    bot.send_message(**not_whitelisted_message(message))



@bot.message_handler(commands=['start'], is_whitelisted=True)
def start_command(message):
    bot.send_message(**menu_message(message))

@bot.callback_query_handler(func=lambda call: call.data == 'menu', is_whitelisted=True)
def handle_open(call):
    bot.edit_message_text(
        **menu_message(call.message),
        message_id=call.message.message_id
    )

@bot.callback_query_handler(func=lambda call: call.data == 'start_instance', is_whitelisted=True)
def handle_start(call):
    res = boto3.resource('ec2')
    instance = res.Instance(os.getenv('INSTANCE_ID'))
    state = instance.state['Name']

    if not state != 'running':
        bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=True,
            text=messages['TEXT_ALREADY_RUNNING']
        )

    ec2.start_instances(InstanceIds=[os.getenv('INSTANCE_ID')])

    bot.edit_message_text(
        **menu_message(call.message),
        message_id=call.message.message_id
    )

@bot.callback_query_handler(func=lambda call: call.data == 'stop_instance', is_whitelisted=True)
def handle_stop(call):
    res = boto3.resource('ec2')
    instance = res.Instance(os.getenv('INSTANCE_ID'))
    state = instance.state['Name']

    if not state != 'stopped':
        bot.answer_callback_query(
            callback_query_id=call.id,
            show_alert=True,
            text=messages['TEXT_ALREADY_STOPPED']
        )

    ec2.stop_instances(InstanceIds=[os.getenv('INSTANCE_ID')])

    bot.edit_message_text(
        **menu_message(call.message),
        message_id=call.message.message_id
    )

while True:
    #try:
        bot.polling(none_stop=True)

    #except Exception as e:
    #    print('Bot polling error:', e)
    #    time.sleep(5)

