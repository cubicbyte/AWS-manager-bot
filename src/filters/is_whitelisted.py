import telebot.custom_filters, telebot.types
from ..get_whitelist import get_whitelist

class IsWhitelisted(telebot.custom_filters.SimpleCustomFilter):
    key='is_whitelisted'

    @staticmethod
    def check(message):
        if isinstance(message, telebot.types.CallbackQuery):
            message = message.message

        whitelist = get_whitelist()

        return str(message.chat.id) in whitelist
