
import telebot
from telebot import types

# Вставь свой токен сюда
TOKEN = "ВАШ_ТОКЕН"
bot = telebot.TeleBot(TOKEN)

# Словари для хранения данных
admins = {}
muted_users = set()
creator_id = 123456789  # Замените на свой Telegram ID

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом и игр. Напиши /помощь для списка команд.")

# Команда /помощь
@bot.message_handler(commands=['помощь'])
def help_command(message):
    help_text = (
        "📋 Доступные команды:
"
        "/kick [id] — кикнуть участника
"
        "/mute [id] — замьютить
"
        "/unmute [id] — размьютить
"
        "/rank [id] — выдать админку
"
        "/guess — мини-игра угадай число
"
        "+создатель — авторизоваться как создатель"
    )
    bot.reply_to(message, help_text)

# Команда создателя
@bot.message_handler(func=lambda message: message.text == "+создатель")
def authorize_creator(message):
    if message.from_user.id == creator_id:
        admins[message.from_user.id] = "creator"
        bot.reply_to(message, "✅ Вы авторизованы как создатель!")
    else:
        bot.reply_to(message, "❌ У вас нет прав.")

# Кик
@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            bot.kick_chat_member(message.chat.id, user_id)
            bot.reply_to(message, "Пользователь кикнут.")
        except:
            bot.reply_to(message, "Ошибка. Укажите ID.")
    else:
        bot.reply_to(message, "Нет прав.")

# Мут
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            muted_users.add(user_id)
            bot.reply_to(message, "Пользователь замьючен.")
        except:
            bot.reply_to(message, "Ошибка. Укажите ID.")
    else:
        bot.reply_to(message, "Нет прав.")

# Анмут
@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            muted_users.discard(user_id)
            bot.reply_to(message, "Пользователь размьючен.")
        except:
            bot.reply_to(message, "Ошибка. Укажите ID.")
    else:
        bot.reply_to(message, "Нет прав.")

# Выдача админки
@bot.message_handler(commands=['rank'])
def give_admin(message):
    if message.from_user.id in admins:
        try:
            user_id = int(message.text.split()[1])
            admins[user_id] = "admin"
            bot.reply_to(message, "Пользователь стал админом.")
        except:
            bot.reply_to(message, "Ошибка. Укажите ID.")
    else:
        bot.reply_to(message, "Нет прав.")

# Игровая функция
import random

@bot.message_handler(commands=['guess'])
def guess_game(message):
    number = random.randint(1, 10)
    bot.reply_to(message, "Угадай число от 1 до 10!")

    @bot.message_handler(func=lambda m: True)
    def check_answer(m):
        try:
            if int(m.text) == number:
                bot.reply_to(m, "🎉 Верно!")
            else:
                bot.reply_to(m, "❌ Неверно. Попробуй ещё.")
        except:
            pass

# Обработка всех сообщений (если юзер в муте — игнор)
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.from_user.id in muted_users:
        return
    # можно добавить доп. обработку

# Запуск бота
bot.polling()
