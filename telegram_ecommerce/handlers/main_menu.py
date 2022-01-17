from telegram import ParseMode
from telegram.ext import CommandHandler

from telegram_ecommerce.language import get_text
from telegram_ecommerce.template.buttons import main_menu_buttons


def main_menu_callback(update, context):
    text = get_text("main_menu", context)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=main_menu_buttons(context))


main_menu = CommandHandler("main_menu", main_menu_callback)
