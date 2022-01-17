from telegram import (
    KeyboardButton as Button,
    ReplyKeyboardMarkup,
    InlineKeyboardButton as InlineButton,
    InlineKeyboardMarkup)

from ..utils.consts import BAD_RATING, REGULAR_RATING, GOOD_RATING
from ..language import get_text


def main_menu_buttons(context=None):
    return ReplyKeyboardMarkup([
        [
            Button(get_text("search_products", context)),
            Button(get_text("promotion", context))],
        [
            Button(get_text("favorites", context)), Button(get_text("basket", context))
        ],
        [
            Button(get_text("my_orders", context))
        ],
        [
            Button(get_text("settings", context)), Button(get_text("support", context))
        ]])


def back_to_main_menu_buttons(context=None):
    return ReplyKeyboardMarkup([
        [
            Button(get_text("main_menu", context))
        ]])


def boolean_question(pattern_identifier, context=None):
    return InlineKeyboardMarkup([
        [
            InlineButton(get_text("cancel", context),
                         callback_data=pattern_identifier + 'cancel'),
            InlineButton(get_text("OK", context),
                         callback_data=pattern_identifier + 'OK')
        ]
    ])


def rating_template(pattern_identifier, context=None):
    return InlineKeyboardMarkup([
        [
            InlineButton(get_text("bad", context),
                         callback_data=pattern_identifier + str(BAD_RATING))
        ],
        [
            InlineButton(get_text("regular", context),
                         callback_data=pattern_identifier + str(REGULAR_RATING))
        ],
        [
            InlineButton(get_text("good", context),
                         callback_data=pattern_identifier + str(GOOD_RATING))
        ]
    ])


def numeric_keyboard(pattern_identifier, context=None):
    return (InlineKeyboardMarkup([
        [
            InlineButton("1", callback_data=pattern_identifier + 'digit_1'),
            InlineButton("2", callback_data=pattern_identifier + 'digit_2'),
            InlineButton("3", callback_data=pattern_identifier + 'digit_3')
        ],
        [
            InlineButton("4", callback_data=pattern_identifier + 'digit_4'),
            InlineButton("5", callback_data=pattern_identifier + 'digit_5'),
            InlineButton("6", callback_data=pattern_identifier + 'digit_6')
        ],
        [
            InlineButton("7", callback_data=pattern_identifier + 'digit_7'),
            InlineButton("8", callback_data=pattern_identifier + 'digit_8'),
            InlineButton("9", callback_data=pattern_identifier + 'digit_9')
        ],
        [
            InlineButton(get_text("cancel", context),
                         callback_data=pattern_identifier + 'cancel_numeric_keyboard'),
            InlineButton("0", callback_data=pattern_identifier + 'digit_0'),
            InlineButton(get_text("next", context),
                         callback_data=pattern_identifier + 'end_numeric_keyboard')
        ]]))


def login_keyboard(pattern_identifier, context=None):
    return ({
        "step_1": InlineKeyboardMarkup([
            [
                InlineButton(get_text("cancel", context),
                             callback_data=pattern_identifier + 'cancel_loging_process'),
                InlineButton(get_text("next", context),
                             callback_data=pattern_identifier + 'next_step_1_login_process'),
            ]]),
        "step_2": numeric_keyboard(pattern_identifier, context),
        "step_3": InlineKeyboardMarkup([
            [
                InlineButton(get_text("cancel", context),
                             callback_data=pattern_identifier + 'cancel_loging_process'),
                InlineButton(get_text("next", context),
                             callback_data=pattern_identifier + 'end_login_process'),
            ]])})


def get_list_of_buttons(*names_in_buttons):
    list_of_buttons = []
    for name_of_the_button in names_in_buttons:
        list_of_buttons.append(
            [
                Button(name_of_the_button)
            ]
        )
    return ReplyKeyboardMarkup(list_of_buttons)


def template_for_show_a_list_of_products(pattern_identifier, context=None):
    return InlineKeyboardMarkup([
        [
            InlineButton(
                get_text("previous_product", context),
                callback_data=pattern_identifier + 'previous_product'),
            InlineButton(
                get_text("product_details", context),
                callback_data=pattern_identifier + 'product_details'),
            InlineButton(
                get_text("next_product", context),
                callback_data=pattern_identifier + 'next_product')
        ]])


def template_for_show_a_detailed_product(pattern_identifier, context=None):
    return InlineKeyboardMarkup([
        [
            InlineButton(
                get_text("previous_product", context),
                callback_data=pattern_identifier + 'previous_product'),
            InlineButton(
                get_text("buy", context),
                callback_data=pattern_identifier + 'buy_product')
        ]])


def template_for_show_a_list_of_promotions(pattern_identifier, context=None):
    return InlineKeyboardMarkup([
        [
            InlineButton(
                get_text("previous_promotion", context),
                callback_data=pattern_identifier + 'previous_promotion'),
            InlineButton(
                get_text("promotion_details", context),
                callback_data=pattern_identifier + 'promotion_details'),
            InlineButton(
                get_text("next_promotion", context),
                callback_data=pattern_identifier + 'next_promotion')
        ]])


def template_for_show_a_detailed_promotion(pattern_identifier, context=None):
    return InlineKeyboardMarkup([
        [
            InlineButton(
                get_text("back_to_promotion", context),
                callback_data=pattern_identifier + 'back_to_promotion')
        ]])


def template_for_show_a_list_of_favorite(pattern_identifier, context=None):
    return InlineKeyboardMarkup([
        [
            InlineButton(
                get_text("previous_favorite", context),
                callback_data=pattern_identifier + 'previous_favorite'),
            InlineButton(
                get_text("next_favorite", context),
                callback_data=pattern_identifier + 'next_favorite')
        ],
        [
            InlineButton(
                get_text("go_to_product_or_category", context),
                callback_data=pattern_identifier + 'go_to_product_or_category'),
            InlineButton(
                get_text("delete_from_favorites", context),
                callback_data=pattern_identifier + 'delete_from_favorites'),
        ]
    ])
