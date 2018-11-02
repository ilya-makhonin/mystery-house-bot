import telebot
import config                 # Token вынесен в отдельный файл
from mysql import add_player, update_user, get_statistic    # Работа с базой данных MySQL, через библиотеку PyMySQL

bot = telebot.TeleBot('token')

users = dict()


def create_markup(events):
    markup = telebot.types.InlineKeyboardMarkup()
    for button in events:
        markup.add(telebot.types.InlineKeyboardButton(button[0], callback_data=button[1]))
    return markup


def send_mes(user_id, to_send, img_name):
    try:
        with open("img\\" + img_name + ".png", 'rb') as photo:
            bot.send_photo(user_id, photo, to_send["text"], reply_markup=create_markup(to_send["markup"]))
    except FileNotFoundError:
        bot.send_message(user_id, to_send["text"], reply_markup=create_markup(to_send["markup"]))


@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    start_game = telebot.types.InlineKeyboardButton("🎮 Начать игру", callback_data="start game")
    about_game = telebot.types.InlineKeyboardButton("❔ Информация об игре", callback_data="about")
    statistic = telebot.types.InlineKeyboardButton("❔ Информация о боте", callback_data="statistic")
    markup.add(start_game, about_game, statistic)
    bot.send_message(message.from_user.id, config.start_mes, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data
    user_id = call.from_user.id

    if call.message.content_type == 'text':
        bot.edit_message_text(call.message.text, call.from_user.id, call.message.message_id)
    elif call.message.content_type == 'photo':
        bot.edit_message_caption(call.message.caption, call.from_user.id, call.message.message_id)

    if data == "about":
        ab_markup = telebot.types.InlineKeyboardMarkup()
        start_game = telebot.types.InlineKeyboardButton("🎮 Начать игру", callback_data="start game")
        statistic = telebot.types.InlineKeyboardButton("❔ Информация о боте", callback_data="statistic")
        ab_markup.add(start_game, statistic)
        bot.send_message(user_id, config.about, reply_markup=ab_markup)
    elif data == "statistic":
        ab_markup = telebot.types.InlineKeyboardMarkup()
        start_game = telebot.types.InlineKeyboardButton("🎮 Начать игру", callback_data="start game")
        about_game = telebot.types.InlineKeyboardButton("❔ Информация об игре", callback_data="about")
        ab_markup.add(start_game, about_game)
        text = config.statistic.format(get_statistic())
        bot.send_message(user_id, text, reply_markup=ab_markup)
    elif data == "start game" or user_id not in users:
        room, events = add_player(user_id, call.from_user.first_name)
        if user_id not in users and room != 'yard':
            bot.send_message(user_id, config.error_mes)
        users[user_id] = [room, events]
        send_mes(user_id, config.events[room], room)
    else:
        if data in users[user_id][1]:
            data = 'not ' + data
        to_send = config.events[data]
        users[user_id][0] = data
        if data == 'button':
            if 'knife' not in users[user_id][1]:
                send_mes(user_id, config.events['cant use knife'], 'study')
                return
        elif data == 'kitchen':
            if 'hammer' in users[user_id][1]:
                send_mes(user_id, config.events['push'], 'kitchen')
                return
        elif data == 'pantry':
            if 'kitchen' not in users[user_id][1]:
                send_mes(user_id, config.events['not pantry'], 'pantry')
                return
        elif 'hammer' in data:
            if 'attic' in users[user_id][1]:
                send_mes(user_id, config.events['attic'], 'attic')
                return

        if 'command' in to_send:
            command = to_send['command'].split(' ')
            if 'chest' in command:
                if 'key' not in users[user_id][1]:
                    send_mes(user_id, config.events['return chest'], 'no image')
                    return
                elif 'chest' in users[user_id][1]:
                    send_mes(user_id, to_send, data)
                    return

            if 'add' in command:
                users[user_id][1] += command[1] + ' '
                update_user(user_id, users[user_id][0], users[user_id][1])
            elif 'fire' in command:
                if 'fire' not in users[user_id][1] and 'pitcher' in users[user_id][1]:
                    users[user_id][1] += 'fire '
                    send_mes(user_id, config.events['fire'], 'fire')
                    return
            elif 'end' in command:
                users[user_id][1] = ''
                update_user(user_id, 'yard', '')
        send_mes(user_id, to_send, data)


if __name__ == "__main__":
    bot.polling(none_stop=True)