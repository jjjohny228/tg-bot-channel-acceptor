import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatJoinRequest, FSInputFile
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Bot token and channel ID from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello! I'm a bot that manages channel join requests.")


@dp.chat_join_request()
async def process_join_request(chat_join: ChatJoinRequest, bot: Bot):
    try:
        # Approve the join request
        logging.info(f"Approved join request for user {chat_join.from_user.id}")

        # Send welcome message
        welcome_text = (f"Hello, {chat_join.from_user.username}\n"
                        f"Your application has been approved! ✅\n\n"
                        f"Now we can be friends and start earning together, I need motivated people!\n\n"
                        f"✅ GET HACK BOT FREE ✅\n\n"
                        f"Without saying too much, I made a video for you and gave you brief instructions on "
                        f"how to earn your first 100$ using a bot:\n\n"
                        f"🤖 GET FREE BOT: @VINEET_MINES_BOT\n\n"
                        f"🔥 My telegram chanel: https://t.me/+mQo0L-LPM2E2Nzlk")

        await bot.send_animation(
            chat_id=chat_join.from_user.id,
            animation="https://telegra.ph/file/fe3109510bb674fa9216d.mp4",
            caption=welcome_text
        )
        logging.info(f"Sent welcome message to user {chat_join.from_user.id}")
        await chat_join.approve()

    except Exception as e:
        logging.error(f"Error processing join request: {e}", exc_info=True)


async def main():
    logging.info("Starting bot")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())