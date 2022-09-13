def create_message(message):
    message_text = 'Sorry, but you are not on the white list.\n\nContact @Bogdan4igg'

    msg = {
        'chat_id': message.chat.id,
        'text': message_text
    }

    return msg
