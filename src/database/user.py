from typing import Generator
from datetime import datetime, timedelta

from .models import User


# region SQL Create

def create_user_if_not_exist(telegram_id: int, name: str) -> bool:
    if not get_user_by_telegram_id_or_none(telegram_id):
        User.create(name=name, telegram_id=telegram_id)
        return True
    return False


# endregion


# region SQL Select


def get_users_total_count() -> int:
    return User.select().count()


def get_users_by_hours(hours: int):
    start_time = datetime.now() - timedelta(hours=hours)
    users_count = User.select().where(User.registration_timestamp >= start_time).count()

    return users_count


def get_user_ids() -> Generator:
    yield from (user.telegram_id for user in User.select())


def get_all_users() -> tuple:
    yield from ((user.telegram_id, user.name, user.registration_timestamp) for
                user in User.select())


def get_user_by_telegram_id_or_none(telegram_id: int) -> None:
    return User.get_or_none(User.telegram_id == telegram_id)


# endregion
