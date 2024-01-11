from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



#  MENU
menu_reply = ReplyKeyboardMarkup(resize_keyboard = True)
menu_reply.row('🏠', '👥', '➕', '💬', '👤')

cancel_reply = ReplyKeyboardMarkup(resize_keyboard = True)
cancel_reply.row('Отменить')