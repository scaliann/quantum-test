from aiogram import types
from aiogram.filters import CommandStart, Command

from .api_client import PostAPIClient
from .keyboard_builder import KeyboardBuilder
from .message_formatter import MessageFormatter


class PostHandlers:
    def __init__(self):
        self.api_client = PostAPIClient()
        self.keyboard_builder = KeyboardBuilder()
        self.message_formatter = MessageFormatter()

    async def handle_start(
        self,
        message: types.Message,
    ):
        await message.reply(
            "Добро пожаловать в QuantumBot! Используйте /posts для того, чтобы увидеть последние посты."
        )

    async def handle_posts_command(
        self,
        message: types.Message,
    ):
        try:
            posts = await self.api_client.get_posts()
            keyboard = self.keyboard_builder.build_posts_keyboard(posts)
            await message.reply("Выберите пост, чтобы посмотреть:", reply_markup=keyboard)
        except Exception as e:
            await message.reply(
                "К сожалению, не удалось обработать пост. Пожалуйста, попробуйте позже."
            )

    async def handle_post_selection(
        self,
        message: types.Message,
    ):
        if not message.text.startswith("Заголовок"):
            return

        try:
            post_id = int(message.text.split("Номер поста: ")[-1].strip(")"))
            post = await self.api_client.get_post(post_id)
            formatted_message = self.message_formatter.format_post(post)
            await message.reply(formatted_message, parse_mode="Markdown")
        except Exception as e:
            await message.reply("К сожалению, не удалось получить детали поста.")
