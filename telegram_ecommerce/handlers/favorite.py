from telegram import ParseMode
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, CommandHandler

from telegram_ecommerce.database.query import search_favorites
from telegram_ecommerce.language import get_text
from telegram_ecommerce.template.buttons import back_to_main_menu_buttons, template_for_show_a_list_of_favorite
from telegram_ecommerce.template.favorites import send_a_favorite, send_a_detailed_favorite, get_text_for_favorite, \
    ListFavoriteIterator
import json


(END,
 SHOW_NEW_FAVORITE,
 GET_LIST_OF_FAVORITES,
 SHOW_LIST_OF_FAVORITE_THAT_MATCH) = range(-1, 3)

favorites_data_key = "list_of_favorites"
favorites_data = {
    'favorites': []}

pattern_identifier = "response_from_buttons_in_favorites_that_match"
PATTERN_TO_CATCH_THE_PREVIOUS_FAVORITE = 'previous_favorites'
PATTERN_TO_CATCH_THE_NEXT_FAVORITE = 'next_favorites'
PATTERN_TO_CATCH_THE_VIEW_GO_TO_THE_PRODUCT_OR_CATEGORY = 'go_to_product_or_category'
PATTERN_TO_CATCH_THE_DELETE_FROM_FAVORITES = 'delete_from_favorites'


def put_favorites_data_in_user_data(user_data):
    user_data[favorites_data_key] = favorites_data


def save_favorites_in_user_data(user_data, update):
    query = update.message
    print("something: " + str(query))

    favorites_from_a_search_query = search_favorites(343193230)
    favorites = ListFavoriteIterator.create_a_list_from_a_query(
        favorites_from_a_search_query)
    user_data[favorites_data_key]["favorites"] = favorites


def show_new_favorite(update, context):
    put_favorites_data_in_user_data(context.user_data)
    text = get_text("ask_for_term_to_search_favorite", context)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=back_to_main_menu_buttons(context))
    return get_list_of_favorites_that_match(update, context)


def get_list_of_favorites_that_match(update, context):
    save_favorites_in_user_data(context.user_data, update)

    if not context.user_data[favorites_data_key]["favorites"].is_empty():
        text = get_text("OK", context)
        update.message.reply_text(text)
        show_list_of_favorite_that_match(update, context)
        return SHOW_LIST_OF_FAVORITE_THAT_MATCH
    else:
        text = get_text("without_favorite_in_this_search", context)
        update.message.reply_text(text)
        cancel_search(update, context)
        return END


def show_list_of_favorite_that_match(update, context):
    favorite = context.user_data[favorites_data_key]["favorites"].next()
    markup = template_for_show_a_list_of_favorite(pattern_identifier, context)
    text = get_text_for_favorite(favorite, context)
    try:
        if favorite.image_id is not None:
            update.message.reply_photo(
                favorite.image_id,
                caption=text,
                reply_markup=markup)
        else:
            update.message.reply_text(text, reply_markup=markup)
    except Exception as exception:
        print(exception)
    return SHOW_LIST_OF_FAVORITE_THAT_MATCH


def catch_previous(update, context):
    favorite = context.user_data[favorites_data_key]["favorites"].previous()
    send_a_favorite(update, context, favorite, pattern_identifier)
    return SHOW_LIST_OF_FAVORITE_THAT_MATCH


def catch_next(update, context):
    favorite = context.user_data[favorites_data_key]["favorites"].next()
    send_a_favorite(update, context, favorite, pattern_identifier)
    return SHOW_LIST_OF_FAVORITE_THAT_MATCH


def catch_details(update, context):
    favorite = context.user_data[favorites_data_key]["favorites"].actual()
    send_a_detailed_favorite(update, context, favorite, pattern_identifier)
    return END


def cancel_search(update, context):
    text = get_text("canceled_operation", context)
    update.message.reply_text(text)
    return END


favorite_command = (
    CommandHandler("favorites", show_new_favorite))

favorite_handler = ConversationHandler(
    entry_points=[favorite_command],
    states={
        SHOW_NEW_FAVORITE: [
            MessageHandler(
                Filters.text,
                show_new_favorite)
        ],
        SHOW_LIST_OF_FAVORITE_THAT_MATCH: [
            MessageHandler(
                Filters.text,
                show_list_of_favorite_that_match),
            CallbackQueryHandler(
                catch_next,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_NEXT_FAVORITE),
            CallbackQueryHandler(
                catch_previous,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_PREVIOUS_FAVORITE),
            CallbackQueryHandler(
                catch_details,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_VIEW_GO_TO_THE_PRODUCT_OR_CATEGORY)
        ]
    },
    fallbacks=[MessageHandler(Filters.all, cancel_search)]
)
