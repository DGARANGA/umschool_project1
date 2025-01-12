# t.me/finalpythonproject_bot

from random import randint, random

import telebot
from aiogram import types

bot = telebot.TeleBot("7265759378:AAHTkTywUg36q10ZZebcM39COb5A8Qb9hMk")

import psycopg2

# Подключение бд и курсора

conn = psycopg2.connect(
    dbname="final python project",
    user="postgres",
    password="Vse_Ravno_Zabudy",
    host="localhost",
    port=5432,
)
cur = conn.cursor()


c1 = telebot.types.BotCommand(command="answer", description="Ответить на вопрос")
c2 = telebot.types.BotCommand(command="show_my_stat", description="Посмотреть свою статистику")
c3 = telebot.types.BotCommand(command="set_question", description="Написать свой вопрос")
c4 = telebot.types.BotCommand(command="show_all_stat", description="Посмотреть статистику всех пользователей")
bot.set_my_commands([c1, c2, c3, c4])


#   Проверки на всякий
# cur.execute("BEGIN")
# cur.execute("INSERT INTO users VALUES(3, 'EXAMPLE', false, ARRAY[1, 2, 3], ARRAY['Да', 'Да', 'Нет'])")
# cur.execute("SELECT * FROM users")
# print(cur.fetchall())
# cur.execute("COMMIT")
# cur.close()
# conn.close()

# Взаимодействия с sql на всякий

"""
Выполнение команды:
cur.execute("SELECT * FROM ___")

Получение всех строк:
cur.execute("SELECT * FROM ___")
all_records = cur.fetchall()

Получение одной строки:
cur.execute("SELECT * FROM ___ WHERE id = 1;")
record = cur.fetchone()

Получение нескольких строк:
number_of_rows = 5
cur.execute("SELECT * FROM employees;")
rows = cur.fetchmany(number_of_rows)
for row in rows:
    print(row)

Закрыть курсор:
cur.close()

Закрыть соединение:
conn.close
"""


class UserStates(telebot.handler_backends.StatesGroup):
    name = telebot.handler_backends.State()
    answer = telebot.handler_backends.State()
    new_question = telebot.handler_backends.State()


# Генерация бд


cur.execute("BEGIN")
cur.execute(
    "CREATE TABLE IF NOT EXISTS users (id BIGINT NOT NULL, name VARCHAR, is_admin BOOLEAN, question_answer TEXT, id_used_questions INT); CREATE TABLE IF NOT EXISTS questions (id BIGINT NOT NULL, question_text VARCHAR)"
           )
cur.execute("INSERT INTO questions VALUES""""
            (1, 'Солнце – это звезда?'),
            (2, 'Вода состоит из двух элементов: водорода и кислорода?'),
            (3, 'Кошки умеют летать?'),
            (4, 'Земля круглая?'),
            (5, 'В Швейцарии нет моря?'),
            (6, 'Все медузы ядовиты?'),
            (7, 'Кофе делают из зёрен?'),
            (8, 'У людей есть три глаза?'),
            (9, 'Луна светит сама?'),
            (10, 'В мире есть полярные медведи?'),
            (11, 'Птицы могут плавать под водой?'),
            (12, 'Арбуз — это овощ?'),
            (13, 'Ушки на торте – это детали для украшения?'),
            (14, 'Все собаки умеют лаять?'),
            (15, 'Слон — это самый большой наземный животное?'),
            (16, 'В леднике всегда тепло?'),
            (17, 'У человека есть зубы?'),
            (18, 'В Москве есть Кремль?'),
            (19, 'Дороги всегда ровные?'),
            (20, 'Радуга состоит из нескольких цветов?')
            """)
cur.execute("COMMIT")


# Запись пользователей и разделение админов


"""
Здесь происходит запись пользователей и разделение
их на админов и обычных (по id пользователей в телеграмме)
с помощью состояний
"""


@bot.message_handler(commands=["start"])
def add_user_to_the_bd(message):
    markup2 = telebot.types.ReplyKeyboardMarkup()
    markup2.add(telebot.types.KeyboardButton("/answer"))
    try:
        cur.execute("Begin")
        cur.execute(f"INSERT INTO users(id, id_used_questions) VALUES ({message.chat.id}, 1)")
        if message.chat.id == 5870829304 or 2087840117:
            cur.execute(
                f"UPDATE users SET is_admin = true WHERE ID = {message.chat.id}"
            )
            bot.send_message(message.chat.id, "Поздравляем, вы админ!")
        cur.execute("COMMIT")
        bot.send_message(
            message.chat.id,
            """
Здравствуйте, это телеграм бот для опросов.
У него есть несколько команд:
Для всех пользователей:
/answer - ответить на вопрос
/show_my_stat - посмотреть свою статистику
И для админов:
/set_question - задать свой вопрос
/show_all_stat - посмотреть общую статистику пользователей

За привилегией администратора
обращайтесь по тг @BabaevTim10

Для начала напишите своё имя:
        """,
        )
        bot.set_state(message.from_user.id, UserStates.name)
    except (psycopg2.errors.DuplicateTable, RecursionError):
        bot.send_message(
            message.chat.id,
            f"Извините, но вы уже зарегистрированы. Хотите ответить на вопрос?",
            reply_markup=markup2,
        )
        cur.execute("ROLLBACK")


@bot.message_handler(state=UserStates.name)
def name_state(message):
    markup2 = telebot.types.ReplyKeyboardMarkup()
    markup2.add(telebot.types.KeyboardButton("/answer"))
    bot.send_message(
        message.chat.id, "Спасибо, хотите ответить на вопрос?", reply_markup=markup2
    )
    with bot.retrieve_data(message.from_user.id) as data:
        data["name"] = message.text
    bot.delete_state(message.from_user.id)
    cur.execute("Begin")
    cur.execute(
        f"UPDATE users SET name = '{data["name"]}' WHERE id = {message.chat.id}"
    )
    cur.execute("COMMIT")

    """"
    Здесь будет работа с вопросами из таблички questions:
    выдача вопросов просмотр личной статистики и действия админов
                                                Админы	Обычные пользователи
    проходят опрос	                              +	        +
    создают вопрос(+ запись времени публикации)	  +	        -
    удаляют вопрос	                              +	        -
    """
    # Выдаёт вопрос

    """Переделывай рандомайзер (Выдаёт разные вопросы)"""


def get_random_id_question(message):
    cur.execute("ROLLBACK")

    cur.execute(f"SELECT id_used_questions FROM users WHERE id = {message.chat.id}")
    question_id = cur.fetchone()

    cur.execute(f"UPDATE users SET id_used_questions = {int(question_id[0]) + 1} WHERE id = {message.chat.id}")

    return int(question_id[0])


@bot.message_handler(commands=["answer"])
def send_question(message):
    cur.execute("ROLLBACK")
    question = get_random_id_question(message)



    markup1 = telebot.types.ReplyKeyboardMarkup()
    markup1.add(telebot.types.KeyboardButton("Да"))
    markup1.add(telebot.types.KeyboardButton("нет"))


    try:
        cur.execute(f"SELECT question_text FROM questions WHERE id = {question}")
        global question_text
        question_text = cur.fetchall()[0]

        bot.send_message(
            message.chat.id,
            f"{str(question_text).replace('(', '').replace(')', '').replace(',', '').replace("'", '')}", reply_markup=markup1
        )
        bot.set_state(message.chat.id, UserStates.answer)
        return question_text

    except IndexError:
        cur.execute("ROLLBACK")
        bot.delete_state(message.from_user.id)
        bot.send_message(message.chat.id, "К сожалению вопросы закончились(")

        cur.execute(f"UPDATE users SET id_used_questions = {question} WHERE id = {message.chat.id}")


        # Ответ пользователя


@bot.message_handler(state=UserStates.answer)
def answer_state(message):
    with bot.retrieve_data(message.from_user.id) as data:
        data["answer"] = message.text
    bot.delete_state(message.from_user.id)

    cur.execute(f"SELECT question_answer FROM users WHERE ID = {message.chat.id}")
    save_info = [cur.fetchall()]
    save_info = str(make_facking_str(save_info[0]))

    new_info = (
        str([f"{question_text}: {data["answer"] + ';  '}"])
        .replace("(", "")
        .replace(")", "")
        .replace("'", "")
        .replace("[", "")
        .replace("]", "")
    )

    save_info = (
        str(save_info)
        .replace("(", "")
        .replace(")", "")
        .replace("{", "")
        .replace("}", "")
        .replace("'None,', ", "")
        .replace("[", "")
        .replace("]", "")
        .replace('"', "")
        .replace("'", "")
    )

    markup2 = telebot.types.ReplyKeyboardMarkup()
    markup2.add(telebot.types.KeyboardButton("/answer"))

    cur.execute(f"SELECT question_answer FROM users WHERE ID = {message.chat.id}")
    is_question_answer_empty = cur.fetchall()
    if is_question_answer_empty:
        cur.execute("BEGIN")

        cur.execute(
            f"UPDATE users SET question_answer = ARRAY['{save_info}', '{new_info}']"
        )
        cur.execute("COMMIT")
    else:
        cur.execute("BEGIN")
        cur.execute(
            f"UPDATE users SET question_answer = ARRAY['{save_info}','{new_info}']"
        )
        cur.execute("COMMIT")
    bot.send_message(message.chat.id, "Ваш ответ записан, ещё вопросик?", reply_markup=markup2)


def make_facking_str(listik):

    " ".join(str(x) for x in listik)
    return listik


@bot.message_handler(commands=["show_my_stat"])
def show_user_stat(message):
    cur.execute("ROLLBACK")
    cur.execute(f"SELECT name FROM users WHERE id = {message.chat.id}")
    name = cur.fetchall()
    cur.execute(f"SELECT question_answer FROM users WHERE id = {message.chat.id}")
    answers = cur.fetchall()
    cur.execute(f"SELECT is_admin FROM users WHERE ID = {message.chat.id}")
    is_admin__ = cur.fetchall()
    if is_admin__ and answers is not None:
        bot.send_message(
            message.chat.id,
            f"""Ваше имя: {str(name).replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',', '').replace("'", '')}, ваши ответы: {str(answers).replace('{', '').replace('}', '').replace('"', '').replace('"\"', '').replace('[', '').replace('(', '').replace(')', '').replace(']', '').replace(',', '').replace("'", '').replace('\\', '').replace('None', '')}. Вы админ\n""",
        )
    elif is_admin__:
        bot.send_message(
            message.chat.id,
            f"""Ваше имя: {str(name).replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',', '').replace("'", '')}, у вас ещё нет ответов. Вы админ\n""",
        )
    elif answers is not None:
        bot.send_message(
            message.chat.id,
            f"""Ваше имя: {str(name).replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',', '').replace("'", '')}, ваши ответы: {str(answers).replace('{', '').replace('}', '').replace('"', '').replace('"\"', '').replace('[', '').replace('(', '').replace(')', '').replace(']', '').replace(',', '').replace("'", '').replace('\\', '').replace('None', '')}. Вы не являетесь админом(\n""",
        )
    else:
        bot.send_message(
            message.chat.id,
            f"""Ваше имя: {str(name).replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',', '').replace("'", '')}, у вас ещё нет ответов. Вы не являетесь админом(\n""",
        )

        # ФИШКИ АДМИНА


@bot.message_handler(commands=["set_question"])
def new_question_text(message):
    cur.execute("ROLLBACK")
    cur.execute(f"SELECT is_admin FROM users WHERE ID = {message.chat.id}")
    is_admin = cur.fetchall()
    if is_admin:
        bot.send_message(message.chat.id, "Хотите задать свой вопрос? Напишите его:")
        bot.set_state(message.chat.id, UserStates.new_question)
    else:
        bot.send_message(
            message.chat.id,
            "К сожалению для вас эта команда не доступна, но вы можете купить привилегии админа обратившись по тг: @BabaevTim10",
        )


@bot.message_handler(state=UserStates.new_question)
def set_new_question(message):
    with bot.retrieve_data(message.from_user.id) as data:
        data["new_question"] = message.text
    bot.delete_state(message.from_user.id)
    cur.execute(f"SELECT id FROM questions ORDER BY id DESC LIMIT 1")
    last_id = cur.fetchone()
    if last_id is not None:
        last_id = last_id[0] + 1
        cur.execute("BEGIN")
        cur.execute(
            f"INSERT INTO questions VALUES ({last_id}, '{data["new_question"]}')"
        )
        cur.execute("COMMIT")
    else:
        cur.execute("BEGIN")
        cur.execute(f"INSERT INTO questions VALUES (1, '{data["new_question"]}')")
        cur.execute("COMMIT")
    bot.send_message(
        message.chat.id,
        "Ваш вопрос записан, теперь на него будут отвечать остальные пользователи",
    )


@bot.message_handler(commands=["show_all_stat"])
def show_all_users_stat(message):
    cur.execute("ROLLBACK")
    cur.execute(f"SELECT is_admin FROM users WHERE ID = {message.chat.id}")
    is_admin = cur.fetchall()
    if not is_admin:
        bot.send_message(
            message.chat.id,
            "К сожалению для вас эта команда не доступна, но вы можете купить привелегии админа обратившийсь по тегу: @BabaevTim10",
        )
    else:
        cur.execute("SELECT name, question_answer FROM users")
        all_info_users = cur.fetchall()
        bot.send_message(
            message.chat.id,
            f"{str(all_info_users[0]).replace('{', '').replace('}', '').replace('"', '').replace('"\"', '').replace('[', '').replace(']', '').replace(',', '').replace("'", '').replace('\\', '').replace('None', '').replace('(', '').replace(')', '')};",
        )


bot.add_custom_filter(telebot.custom_filters.StateFilter(bot))
bot.infinity_polling()