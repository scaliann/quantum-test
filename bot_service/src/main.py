import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command

from .config import settings
from .handlers import PostHandlers

# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# Initialize handlers
post_handlers = PostHandlers()

# Register handlers
dp.message.register(post_handlers.handle_start, CommandStart())
dp.message.register(post_handlers.handle_posts_command, Command("posts"))
dp.message.register(post_handlers.handle_post_selection)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
