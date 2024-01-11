from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



#  INLINE
next_inline = InlineKeyboardMarkup()
next_inline.row(InlineKeyboardButton(text = "⬇️", callback_data = "next"))


profile_inline = InlineKeyboardMarkup()
profile_inline.row(InlineKeyboardButton(text = "Изменить профиль", callback_data = "edit_profile"))
profile_inline.row(InlineKeyboardButton(text = "Мои видео", callback_data = "my_videos"))

