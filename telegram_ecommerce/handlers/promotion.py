from telegram import ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from telegram_ecommerce.database.query import search_promotions
from telegram_ecommerce.language import get_text
from telegram_ecommerce.template.buttons import template_for_show_a_list_of_promotions, back_to_main_menu_buttons
from telegram_ecommerce.template.promotions import ListPromotionIterator, get_text_for_promotion, send_a_promotion, \
    send_a_detailed_promotion

(END,
 SHOW_NEW_PROMOTION,
 GET_LIST_OF_PROMOTION,
 SHOW_LIST_OF_PROMOTION_THAT_MATCH, CATCH_DETAILS) = range(-1, 4)

promotions_data_key = "list_of_promotion"
promotions_data = {
    'promotions': []}

pattern_identifier = "response_from_buttons_in_promotion_that_match"
PATTERN_TO_CATCH_THE_PREVIOUS_PROMOTION = 'previous_promotion'
PATTERN_TO_CATCH_THE_NEXT_PROMOTION = 'next_promotion'
PATTERN_TO_CATCH_THE_VIEW_DETAILS = 'promotion_details'
PATTERN_TO_CATCH_THE_BACK_TO_THE_PROMOTION = 'back_to_promotion'


def put_promotions_data_in_user_data(user_data):
    user_data[promotions_data_key] = promotions_data


def save_promotions_in_user_data(user_data):
    promotions_from_a_search_query = search_promotions()
    promotions = ListPromotionIterator.create_a_list_from_a_query(
        promotions_from_a_search_query)
    user_data[promotions_data_key]["promotions"] = promotions


def show_new_promotion(update, context):
    put_promotions_data_in_user_data(context.user_data)
    text = get_text("ask_for_term_to_search_promotion", context)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=back_to_main_menu_buttons(context))
    return get_list_of_promotions_that_match(update, context)


def get_list_of_promotions_that_match(update, context):
    save_promotions_in_user_data(context.user_data)
    if not context.user_data[promotions_data_key]["promotions"].is_empty():
        text = get_text("OK", context)
        update.message.reply_text(text)
        show_list_of_promotion_that_match(update, context)
        return SHOW_LIST_OF_PROMOTION_THAT_MATCH
    else:
        text = get_text("without_promotion_in_this_search", context)
        update.message.reply_text(text)
        cancel_search(update, context)
        return END


def show_list_of_promotion_that_match(update, context):
    promotion = context.user_data[promotions_data_key]["promotions"].next()
    markup = template_for_show_a_list_of_promotions(pattern_identifier, context)
    text = get_text_for_promotion(promotion, context)
    try:
        if promotion.image_id is not None:
            update.message.reply_photo(
                promotion.image_id,
                caption=text,
                reply_markup=markup)
        else:
            update.message.reply_text(text, reply_markup=markup)
    except Exception as exception:
        print(exception)
    return SHOW_LIST_OF_PROMOTION_THAT_MATCH


def catch_previous(update, context):
    promotion = context.user_data[promotions_data_key]["promotions"].previous()
    send_a_promotion(update, context, promotion, pattern_identifier)
    return SHOW_LIST_OF_PROMOTION_THAT_MATCH


def catch_next(update, context):
    promotion = context.user_data[promotions_data_key]["promotions"].next()
    send_a_promotion(update, context, promotion, pattern_identifier)
    return SHOW_LIST_OF_PROMOTION_THAT_MATCH


def catch_details(update, context):
    promotion = context.user_data[promotions_data_key]["promotions"].actual()
    send_a_detailed_promotion(update, context, promotion, pattern_identifier)
    return CATCH_DETAILS


def catch_back(update, context):
    promotion = context.user_data[promotions_data_key]["promotions"].actual()
    send_a_promotion(update, context, promotion, pattern_identifier)
    return SHOW_LIST_OF_PROMOTION_THAT_MATCH


def cancel_search(update, context):
    text = get_text("canceled_operation", context)
    update.message.reply_text(text)
    return END


promotion_command = (
    CommandHandler("promotion", show_new_promotion))

promotion_handler = ConversationHandler(
    entry_points=[promotion_command],
    states={
        SHOW_NEW_PROMOTION: [
            MessageHandler(
                Filters.text,
                show_new_promotion)
        ],
        SHOW_LIST_OF_PROMOTION_THAT_MATCH: [
            MessageHandler(
                Filters.text,
                show_list_of_promotion_that_match),
            CallbackQueryHandler(
                catch_next,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_NEXT_PROMOTION),
            CallbackQueryHandler(
                catch_previous,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_PREVIOUS_PROMOTION),
            CallbackQueryHandler(
                catch_details,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_VIEW_DETAILS)
        ],
        CATCH_DETAILS: [
            CallbackQueryHandler(
                catch_back,
                pattern=pattern_identifier + PATTERN_TO_CATCH_THE_BACK_TO_THE_PROMOTION)
        ]
    },
    fallbacks=[MessageHandler(Filters.all, cancel_search)]
)
