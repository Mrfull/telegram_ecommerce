from telegram import InputMediaPhoto

from telegram_ecommerce.template.buttons import get_list_of_buttons, template_for_show_a_list_of_favorite


class Favorite:
    def __init__(
            self,
            # favorite_id,
            customer_id,
            product_id
    ):
        # self.favorite_id = favorite_id
        self.customer_id = customer_id
        self.product_id = product_id

    def create_a_instance_of_this_class_from_a_list_of_properties(self):
        return Favorite(*self)


class ListFavoriteIterator:
    def __init__(self, *list_of_favorites):
        self.list_of_favorites = list_of_favorites
        self.iter = -1

    def create_a_list_from_a_query(self):
        list_of_instances_of_Favorite_class = list(map(
            Favorite.create_a_instance_of_this_class_from_a_list_of_properties, self))
        return ListFavoriteIterator(
            *list_of_instances_of_Favorite_class)

    def actual(self):
        actual_favorite = self.list_of_favorites[self.iter]
        return actual_favorite

    def next(self):
        self.__increment_iter__()
        actual_favorite = self.list_of_favorites[self.iter]
        return actual_favorite

    def previous(self):
        self.__decrement_iter__()
        actual_favorite = self.list_of_favorites[self.iter]
        return actual_favorite

    def __increment_iter__(self):
        if self.iter == len(self.list_of_favorites) - 1:
            self.iter = 0
        else:
            self.iter += 1

    def __decrement_iter__(self):
        if self.iter <= 0:
            self.iter = len(self.list_of_favorites) - 1
        else:
            self.iter -= 1

    def is_empty(self):
        if self.list_of_favorites:
            return False
        return True


def send_a_favorite(update, context, favorite, pattern_identifier):
    query = update.callback_query
    markup = template_for_show_a_list_of_favorite(
        pattern_identifier, context)
    text = get_text_for_favorite(favorite, context)
    try:
        if favorite.image_id is not None:
            query.message.edit_media(
                media=InputMediaPhoto(favorite.image_id, text),
                reply_markup=markup)
        else:
            query.message.edit_text(text, reply_markup=markup)
    except Exception as exception:
        print(exception)


def send_a_detailed_favorite(update, context, favorite, pattern_identifier):
    query = update.callback_query
    text = get_text_for_detailed_favorite(favorite, context)
    try:
        if favorite.image_id is not None:
            query.message.edit_media(
                media=InputMediaPhoto(favorite.image_id, text))
        else:
            query.message.edit_text(text)
    except Exception as exception:
        print(exception)


def send_a_inline_with_a_list_of_favorite(update, context, text, list_of_names):
    buttons_with_list_of_names = get_list_of_buttons(*list_of_names)
    update.message.reply_text(text, reply_markup=buttons_with_list_of_names)


def get_text_for_favorite(favorite, context):
    # print("favorite: " + str(Product.objects.filter(product_id=favorite.product_id) ))

    text = "text"
    # text = (get_text("favorite_name", context) + favorite + "\n\n" +
    #         get_text("favorite_description_short", context) + str(favorite))
    return text


def get_text_for_detailed_favorite(favorite, context):
    text = "text 2"
    # text = (get_text("favorite_name", context) + favorite + "\n\n" +
    #         get_text("favorite_description", context) + str(favorite)
    #         )
    return text
