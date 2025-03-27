from aiogram import types, Dispatcher, Bot

from src.utils import logger
from src.database.user import create_user_if_not_exist
from src.filters.filter_func import check_is_admin
from src.handlers.admin.admin import admin_kb
from src.create_bot import bot


async def cmd_start(message: types.Message):
    is_admin = await check_is_admin(message)
    if not is_admin:
        await message.answer("Hello! I'm a bot that manages channel join requests.")
    else:
        await message.answer('Добро пожаловать в админку', reply_markup=admin_kb)

async def process_join_request(chat_join: types.ChatJoinRequest):
    try:
        # Approve the join request
        logger.info(f"Approved join request for user {chat_join.from_user.id}")

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
        logger.info(f"Sent welcome message to user {chat_join.from_user.id}")
        create_user_if_not_exist(chat_join.from_user.id, chat_join.from_user.username)
        await chat_join.approve()

    except Exception as e:
        logger.error(f"Error processing join request: {e}", exc_info=True)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_chat_join_request_handler(process_join_request)