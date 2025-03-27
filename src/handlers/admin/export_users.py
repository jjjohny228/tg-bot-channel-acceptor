import os

from openpyxl import Workbook
from aiogram import Dispatcher
from aiogram.types import KeyboardButton, Message

from config import Config
from src.database.user import get_all_users
from src.database.admin import get_admin_ids
from src.create_bot import bot


class Keyboards:
    reply_button_for_admin_menu = KeyboardButton('📥 Экспорт пользователей 📥')
    reply_button_for_admin_menu2 = KeyboardButton('📥 Скачать базу данных 📥')


output_filename = 'Пользователи.xlsx'


class Utils:
    @staticmethod
    async def write_users_to_xl() -> None:
        wb = Workbook()
        ws = wb.active
        ws.append(('№', 'telegram_id', 'Имя', 'Дата регистрации'))
        for n, user_data in enumerate(get_all_users(), 1):
            ws.append((n, *user_data))
        wb.save(output_filename)

    @staticmethod
    async def send_users_xl(to_message: Message) -> None:
        with open(output_filename, 'rb') as excel_file:
            await to_message.answer_document(document=excel_file)
        os.remove(output_filename)

    @staticmethod
    async def send_database() -> None:
        """
        Function send database to all admin users
        """
        print('Бд отправлена')
        for admin_id in {*get_admin_ids(), *Config.ADMIN_IDS}:
            with open('database.db', 'rb') as database_file:
                await bot.send_document(admin_id, database_file)


class Handlers:
    @staticmethod
    async def __handle_admin_export_button(message: Message):
        await Utils.write_users_to_xl()
        await Utils.send_users_xl(message)

    @staticmethod
    async def __handle_admin_download_db_button(message: Message):
        await message.answer_document(document=open('database.db', 'rb'))

    @classmethod
    def register_export_users_handlers(cls, dp: Dispatcher):
        dp.register_message_handler(cls.__handle_admin_export_button, is_admin=True,
                                    text=Keyboards.reply_button_for_admin_menu.text)
        dp.register_message_handler(cls.__handle_admin_download_db_button, is_admin=True,
                                    text=Keyboards.reply_button_for_admin_menu2.text)
