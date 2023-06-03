import telebot
import vk_api

from telebot import types
from loguru import logger as log
from request import DataBaseRequets

bot = telebot.TeleBot(token="а вот фиг вам :D", parse_mode="HTML")

base = DataBaseRequets()


@bot.message_handler(content_types=["text"])
def commands(message):
    command = message.text.split(" ")[0]
    params_split = message.text.split(" ")

    if len(params_split) < 2:
        bot.send_message(message.chat.id, "Укажите токен")
        return

    params = message.text.split(" ")[1].strip()
    if command in ['/token', "!token", '/токен', "!токен"]:
        if len(params) > 298:
            bot.send_message(message.chat.id, "⚠️ Укажите обрезанный токен. Инструкцию можете спросить в лс у <a "
                                              "href='https://vk.com/official_hexvel'>Димы</a>")
            return

        try:
            vk = vk_api.VkApi(token=params)
            app = vk.method('apps.get')["items"][0]["id"]
            owner_id = vk.method('account.getProfileInfo')['id']
        except:
            bot.send_message(message.chat.id, "⚠️ Токен невалидный")
            return
        else:
            if app in [6121396]:
                bot.send_message(message.chat.id, "⚠️ Вставьте токен от VkMe, а не от VkAdmin.")
                return

            filters = dict(user_id=owner_id)
            params = dict(token_vkh=params)
            if not base.base_getter(filters, 'users'):
                bot.send_message(message.chat.id, f"⚠️ Пользователь, владевший <a href='https://vk.com/id"
                                                  f"{owner_id}'>данной</a> страницей не зарегистрирован.")
                return

            update = base.update_base(filters, params, 'users')
            if update['running']:
                bot.send_message(message.chat.id, "[✅] -> Токен скриптов успешно сохранён.")
                return

            bot.send_message(message.chat.id, "[⚠️] -> Произошла ошибка.")
            return


if __name__ == '__main__':
    bot.infinity_polling()
