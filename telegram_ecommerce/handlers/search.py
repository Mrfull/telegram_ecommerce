from telegram import ParseMode
from telegram.ext import (
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler)

from ..database.query import search_products
from ..filters.decorators import execute_if_user_exist
from ..language import get_text
from ..template.buttons import template_for_show_a_list_of_products, back_to_main_menu_buttons
from ..template.buy_callbacks import send_a_shipping_message
from ..template.products import (
    send_a_product,
    send_a_detailed_product,
    get_text_for_product,
    ListProductIterator)

(END,
 ASK_FOR_TERM_TO_SEARCH,
 GET_LIST_OF_PRODUCTS,
 SHOW_LIST_OF_PRODUCT_THAT_MATCH,
 BUY_PROCESS) = range(-1, 4)

products_data_key = "list_of_products"
products_data = {
    'products': []}

pattern_identifier = "response_from_buttons_in_products_that_match"
PATTERN_TO_CATCH_THE_PREVIOUS_PRODUCT = 'previous_product'
PATTERN_TO_CATCH_THE_NEXT_PRODUCT = 'next_product'
PATTERN_TO_CATCH_THE_VIEW_DETAILS = 'product_details'
PATTERN_TO_CATCH_THE_BUY_BUTTON = 'buy_product'


def put_products_data_in_user_data(user_data):
    user_data[products_data_key] = products_data


def save_products_in_user_data(user_data, string_to_search):
    products_from_a_search_query = search_products(string_to_search)
    products = ListProductIterator.create_a_list_from_a_query(
        products_from_a_search_query)
    user_data[products_data_key]["products"] = products


def ask_for_term_to_search(update, context):
    put_products_data_in_user_data(context.user_data)
    text = get_text("ask_for_term_to_search", context)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=back_to_main_menu_buttons(context))
    return GET_LIST_OF_PRODUCTS


def get_list_of_products_that_match(update, context):
    string_to_search = update.message.text
    save_products_in_user_data(context.user_data, string_to_search)
    if not context.user_data[products_data_key]["products"].is_empty():
        text = get_text("OK", context)
        update.message.reply_text(text)
        show_list_of_product_that_match(update, context)
        return SHOW_LIST_OF_PRODUCT_THAT_MATCH
    else:

        text = get_text("without_product_in_this_search", context)
        update.message.reply_text(text)
        cancel_search(update, context)
        return END


def show_list_of_product_that_match(update, context):
    product = context.user_data[products_data_key]["products"].next()
    markup = template_for_show_a_list_of_products(
        pattern_identifier, context)
    text = get_text_for_product(product, context)
    try:
        if product.image_id is not None:
            update.message.reply_photo(
                product.image_id,
                caption=text,
                reply_markup=markup)
        else:
            update.message.reply_text(text, reply_markup=markup)
    except Exception as exception:
        print(exception)
    return SHOW_LIST_OF_PRODUCT_THAT_MATCH


def catch_previous(update, context):
    product = context.user_data[products_data_key]["products"].previous()
    send_a_product(update, context, product, pattern_identifier)
    return SHOW_LIST_OF_PRODUCT_THAT_MATCH


def catch_next(update, context):
    product = context.user_data[products_data_key]["products"].next()
    send_a_product(update, context, product, pattern_identifier)
    return SHOW_LIST_OF_PRODUCT_THAT_MATCH


def catch_details(update, context):
    product = context.user_data[products_data_key]["products"].actual()
    send_a_detailed_product(update, context, product, pattern_identifier)
    return BUY_PROCESS


@execute_if_user_exist
def send_a_shipping_message_callback(update, context):
    product = context.user_data[products_data_key]["products"].actual()
    send_a_shipping_message(update, context, product, pattern_identifier)
    return END


def cancel_search(update, context):
    text = get_text("canceled_operation", context)
    update.message.reply_text(text)
    return END


search_command = (
    CommandHandler("search", ask_for_term_to_search))

search = ConversationHandler(
    entry_points=[search_command],
    states={
        ASK_FOR_TERM_TO_SEARCH: [
            MessageHandler(
                Filters.text,
                ask_for_term_to_search)
        ],
        GET_LIST_OF_PRODUCTS: [
            MessageHandler(
                Filters.text,
                get_list_of_products_that_match)
        ],
        SHOW_LIST_OF_PRODUCT_THAT_MATCH: [
            MessageHandler(
                Filters.text,
                show_list_of_product_that_match),
            CallbackQueryHandler(
                catch_next,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_NEXT_PRODUCT),
            CallbackQueryHandler(
                catch_previous,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_PREVIOUS_PRODUCT),
            CallbackQueryHandler(
                catch_details,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_VIEW_DETAILS)
        ],
        BUY_PROCESS: [
            CallbackQueryHandler(
                catch_previous,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_PREVIOUS_PRODUCT),
            CallbackQueryHandler(
                send_a_shipping_message_callback,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_BUY_BUTTON)
        ]
    },
    fallbacks=[MessageHandler(Filters.all, cancel_search)]
)
