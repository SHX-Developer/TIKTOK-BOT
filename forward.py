from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

import sqlite3
import datetime

import config
import inline_markups
import reply_markups





#  LIBRARY VARIABLES

bot = Bot(config.token)
dp = Dispatcher(bot)

db = sqlite3.connect('database.db', check_same_thread = False)
sql = db.cursor()

date_time = datetime.datetime.now().date()





#  FORWARD

async def forward(message):

    sql.execute('SELECT id FROM user_access')
    data = sql.fetchall()
    sql.execute('SELECT COUNT(id) FROM user_profile')
    all_users = sql.fetchone()[0]
    total = 0
    
    await bot.send_message(message.chat.id, '<b> Рассылка началась  ✅ </b>', parse_mode = 'html', reply_markup = None)
    for row in data:
        try:
            await bot.send_message(
                chat_id = row[0], 
                text = 'TEXT', 
                parse_mode = 'html', 
                reply_markup = None)

            total += 1
            print(f'[{row[0]}]: получил сообщение  ✅')

        except Exception as e:
            print(f'[{row[0]}]: заблокировал бота  ❌')

    else:
        blocked_users = all_users - total
        await bot.send_message(284929331, f'<b>👥  Количество пользователей:</b>  {all_users}', parse_mode = 'html')
        await bot.send_message(284929331, f'<b>✅  Получили:</b>  {total}', parse_mode = 'html')
        await bot.send_message(284929331, f'<b>❌  Заблокировали: </b>  {blocked_users}', parse_mode = 'html')