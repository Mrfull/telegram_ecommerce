from telegram import ParseMode
from telegram.ext import CommandHandler

from ..language import get_text
from ..template.buttons import main_menu_buttons


def start_callback(update, context):
    text = get_text("start", context)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=main_menu_buttons(context))


start = CommandHandler("start", start_callback)
