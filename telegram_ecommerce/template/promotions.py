from telegram import InputMediaPhoto

from telegram_ecommerce.language import get_text
from telegram_ecommerce.template.buttons import get_list_of_buttons, template_for_show_a_list_of_promotions, \
    template_for_show_a_detailed_promotion


class Promotion:
    def __init__(
            self,
            promotion_id,
            name,
            short_description,
            description,
            active,
            created_at,
            modified_at,
            deleted_at,
            image_id=None
            ):
        self.promotion_id = promotion_id
        self.name = name
        self.short_description = short_description
        self.description = description
        self.active = active
        self.image_id = image_id
        self.created_at = created_at
        self.modified_at = modified_at
        self.deleted_at = deleted_at

    def create_a_instance_of_this_class_from_a_list_of_properties(self):
        return Promotion(*self)


class ListPromotionIterator:
    def __init__(self, *list_of_promotions):
        self.list_of_promotions = list_of_promotions
        self.iter = -1

    def create_a_list_from_a_query(self):
        list_of_instances_of_Promotion_class = list(map(
            Promotion.create_a_instance_of_this_class_from_a_list_of_properties, self))
        return ListPromotionIterator(
            *list_of_instances_of_Promotion_class)

    def actual(self):
        actual_promotion = self.list_of_promotions[self.iter]
        return actual_promotion

    def next(self):
        self.__increment_iter__()
        actual_promotion = self.list_of_promotions[self.iter]
        return actual_promotion

    def previous(self):
        self.__decrement_iter__()
        actual_promotion = self.list_of_promotions[self.iter]
        return actual_promotion

    def __increment_iter__(self):
        if self.iter == len(self.list_of_promotions) - 1:
            self.iter = 0
        else:
            self.iter += 1

    def __decrement_iter__(self):
        if self.iter <= 0:
            self.iter = len(self.list_of_promotions) - 1
        else:
            self.iter -= 1

    def is_empty(self):
        if self.list_of_promotions:
            return False
        return True


def send_a_promotion(update, context, promotion, pattern_identifier):
    query = update.callback_query
    markup = template_for_show_a_list_of_promotions(
        pattern_identifier, context)
    text = get_text_for_promotion(promotion, context)
    try:
        if promotion.image_id is not None:
            query.message.edit_media(
                media=InputMediaPhoto(promotion.image_id, text),
                reply_markup=markup)
        else:
            query.message.edit_text(text, reply_markup=markup)
    except Exception as exception:
        print(exception)


def send_a_detailed_promotion(update, context, promotion, pattern_identifier):
    query = update.callback_query
    markup = template_for_show_a_detailed_promotion(
        pattern_identifier, context)
    text = get_text_for_detailed_promotion(promotion, context)
    try:
        if promotion.image_id is not None:
            query.message.edit_media(
                media=InputMediaPhoto(promotion.image_id, text),
                reply_markup=markup)
        else:
            query.message.edit_text(text, reply_markup=markup)
    except Exception as exception:
        print(exception)


def send_a_inline_with_a_list_of_promotion(update, context, text, list_of_names):
    buttons_with_list_of_names = get_list_of_buttons(*list_of_names)
    update.message.reply_text(text, reply_markup=buttons_with_list_of_names)


def get_text_for_promotion(promotion, context):
    text = (get_text("promotion_name", context) + promotion.name + "\n\n" +
            get_text("promotion_description_short", context) + str(promotion.short_description))
    return text


def get_text_for_detailed_promotion(promotion, context):
    text = (get_text("promotion_name", context) + promotion.name + "\n\n" +
            get_text("promotion_description", context) + str(promotion.description)
            )
    return text
