from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import sqlite3
import datetime
import asyncio
import random

import config
import inline_markups
import reply_markups
import database





#  LIBRARY VARIABLES

storage = MemoryStorage()

bot = Bot(config.token)
dp = Dispatcher(bot, storage = MemoryStorage())

db = sqlite3.connect('database.db', check_same_thread = False)
sql = db.cursor()

video_db = sqlite3.connect('videos.db', check_same_thread = False)
video_sql = video_db.cursor()

date_time = datetime.datetime.now().date()



#  STATES

class UploadVideo(StatesGroup):
    video = State()
    description = State()



#  CREATING DATABASE
sql.execute('CREATE TABLE IF NOT EXISTS access (id INTEGER, username TEXT, firstname TEXT, lastname TEXT, date DATE)')
sql.execute('CREATE TABLE IF NOT EXISTS profile (id INTEGER, username TEXT, photo TEXT, follows INTEGER, followers INTEGER, likes INTEGER, bio TEXT)')
sql.execute('CREATE TABLE IF NOT EXISTS video (id INTEGER, count INTEGER)')
db.commit()









#  START COMMAND

@dp.message_handler(commands = ['start'])
async def start_command(message: types.Message):
    sql.execute('SELECT id FROM access WHERE id = ?', (message.chat.id,))
    user_id = sql.fetchone()

    if user_id == None:
        await database.add_user_data(message)
        await bot.send_message(message.chat.id, '<b> Добро пожаловать в TIK TOK ! </b>', parse_mode = 'html', reply_markup = reply_markups.menu_reply)

    else:
        await bot.send_message(message.chat.id, '<b> Главное меню: </b>', parse_mode = 'html', reply_markup = reply_markups.menu_reply)





#  TEXT

@dp.message_handler()
async def text(message: types.Message):
    video_count = sql.execute('SELECT count FROM video').fetchone()[0]


#  TIK TOKS

    if message.text == '🏠':
        try:
            random_number = random.randint(1, video_count)

            user_id = sql.execute('SELECT user_id FROM videos WHERE id = ?', (random_number,)).fetchone()[0]
            user_username = sql.execute('SELECT username FROM profile WHERE id = ?', (user_id,)).fetchone()[0]

            with open(f'video/{random_number}.mp4', 'rb') as random_video:
                await bot.send_video(
                    chat_id = message.chat.id,
                    video = random_video,
                    caption = f'<b>Автор:</b>  <code>{user_username}</code>',
                    parse_mode = 'html',
                    reply_markup = inline_markups.next_inline)

        except:
            await bot.send_message(message.chat.id, '<b> Видео не найдены ! </b>', parse_mode = 'html')



#  FRIENDS

    elif message.text == '👥':
        pass



#  UPLOAD

    elif message.text == '➕':
        await bot.send_message(message.chat.id, '<b> Отправьте видео: </b>', parse_mode = 'html', reply_markup = reply_markups.cancel_reply)
        await UploadVideo.video.set()




#  NOTIFICATIONS

    elif message.text == '💬':
        pass




#  PROFILE

    elif message.text == '👤':
        data = sql.execute('SELECT * FROM profile WHERE id = ?', (message.chat.id,)).fetchone()

        await bot.send_message(
            chat_id = message.chat.id,
            text =
            f'<b>Юзернейм:</b>  <code>{data[1]}</code>'
            f'\n\n<b>Подписки:</b>  {data[3]}'
            f'\n<b>Подписчики:</b>  {data[4]}'
            f'\n<b>Лайки:</b>  {data[5]}'
            f'\n\n<b>Био:</b>  {data[6]}',
            parse_mode = 'html',
            reply_markup = inline_markups.profile_inline)








#  CALLBACK
@dp.callback_query_handler(lambda call: True)
async def callback_queries(call: types.CallbackQuery):
    video_count = sql.execute('SELECT count FROM video').fetchone()[0]


#  SEND MESSAGE
    if call.data == 'next':
        try:
            random_number = random.randint(1, video_count)

            user_id = sql.execute('SELECT user_id FROM videos WHERE id = ?', (random_number,)).fetchone()[0]
            user_username = sql.execute('SELECT username FROM profile WHERE id = ?', (user_id,)).fetchone()[0]

            with open(f'video/{random_number}.mp4', 'rb') as random_video:
                await bot.send_video(
                    chat_id = call.message.chat.id,
                    video = random_video,
                    caption = f'<b>Автор:</b>  <code>{user_username}</code>',
                    parse_mode = 'html',
                    reply_markup = inline_markups.next_inline)

        except:
            await bot.send_message(call.message.chat.id, '<b> Видео не найдены ! </b>', parse_mode = 'html')





#  EDIT INLINE PHOTO
    if call.data == 'edit_photo':
        with open('photo/photo.jpg', 'rb') as photo:
            bot.edit_message_media(
                media = types.InputMedia(
                type = 'photo',
                media = photo,
                chat_id = call.message.chat.id,
                message_id = call.message.message_id,
                caption = '<b> TEXT </b>',
                parse_mode = 'html'),
                reply_markup = None)




#  STATES
@dp.message_handler(content_types = types.ContentTypes.ANY, state = UploadVideo.video)
async def check_video(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['video'] = message.video

    #  CANCEL

        if message.text == 'Отменить':
            await bot.send_message(message.chat.id, '<b> Отменено. </b>', parse_mode = 'html', reply_markup =reply_markups.menu_reply)
            await delete_message_2(message)
            await state.finish()

    #  VIDEO

        elif message.video:

            #  LOADING MESSAGE
            await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
            await bot.send_message(message.chat.id, '<b> Загрузка видео . . . </b>', parse_mode = 'html', reply_markup = None)

            #  UPDATE COUNT
            sql.execute('UPDATE video SET count = count + 1')
            db.commit()

            #  DOWNLOAD VIDEO
            video_count = sql.execute('SELECT count FROM video').fetchone()[0]
            await message.video.download(destination_file = f'video/{video_count}.mp4')

            #  CREATE TABLE OF VIDEO
            video_sql.execute(f'CREATE TABLE IF NOT EXISTS video_{video_count} (video_id INTEGER, user_id INTEGER, views INTEGER, likes INTEGER, comments INTEGER)')
            video_db.commit()

            #  INSERT VALUES
            sql.execute('INSERT INTO videos (id, user_id) VALUES (?, ?)', (video_count, message.chat.id))
            sql.execute(f'INSERT INTO video_{message.chat.id} (id, views, likes, comments) VALUES (?, ?, ?, ?)', (video_count, 0, 0, 0))
            db.commit()
            video_sql.execute(f'INSERT INTO video_{video_count} (video_id, user_id, views, likes, comments) VALUES (?, ?, ?, ?, ?)', (video_count, message.chat.id, 0, 0, 0))
            video_db.commit()

            #  SUCCESS UPLOAD MESSAGE
            await bot.send_message(message.chat.id, '<b> ✅  Загрузка вашего видео успешно завершена ! </b>', parse_mode = 'html', reply_markup = reply_markups.menu_reply)
            await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id + 1)
            await state.finish()

    #  OTHER

        else:
            await delete_message_2(message)
            await bot.send_message(message.chat.id, '<b> Отправьте видео: </b>', parse_mode = 'html', reply_markup = reply_markups.cancel_reply)










#  DELETE MESSAGE 1
async def delete_message_1(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    except:
        pass

#  DELETE MESSAGE 2
async def delete_message_2(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except:
        pass

#  DELETE MESSAGE 3
async def delete_message_3(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 2)
    except:
        pass





#  ON START UP
async def start_bot(_):
    await bot.send_message(284929331, 'The bot is successfully enabled ✅')



#  LAUNCH THE BOT
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True, on_startup = start_bot)
