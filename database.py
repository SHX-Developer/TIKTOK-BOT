import telebot
import sqlite3
import datetime

import config





#  LIBRARY VARIABLES

bot = telebot.TeleBot(config.token)

db = sqlite3.connect("database.db", check_same_thread=False)
sql = db.cursor()

date_time = datetime.datetime.now().date()





#  DATABASE

async def add_user_data(message):
    
    sql.execute('INSERT INTO access (id, username, firstname, lastname, date) VALUES (?, ?, ?, ?, ?)',
    (message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, date_time))
    
    sql.execute('INSERT INTO profile (id, username, photo, follows, followers, likes, bio) VALUES (?, ?, ?, ?, ?, ?, ?)',
    (message.chat.id, message.from_user.username, 'No', 0, 0, 0, '-'))

    sql.execute(f'CREATE TABLE IF NOT EXISTS video_{message.chat.id} (id INTEGER PRIMARY KEY, views INTEGER, likes INTEGER, comments INTEGER)')

    db.commit()

