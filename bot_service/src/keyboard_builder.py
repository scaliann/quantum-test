from typing import List
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from .schemas import Post


class KeyboardBuilder:
    @staticmethod
    def build_posts_keyboard(posts: List[Post]) -> ReplyKeyboardMarkup:
        buttons = []
        for post in posts:
            buttons.append([KeyboardButton(text=f"📝 {post.title} (ID: {post.id})")])

        return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
