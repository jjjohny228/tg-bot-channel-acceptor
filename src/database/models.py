from datetime import datetime
from peewee import Model, SqliteDatabase, BigIntegerField, SmallIntegerField, IntegerField, DateTimeField, CharField


db = SqliteDatabase('database.db')


class _BaseModel(Model):
    class Meta:
        database = db


class User(_BaseModel):
    class Meta:
        db_table = 'users'

    name = CharField(default='Пользователь')
    telegram_id = BigIntegerField(unique=True, null=False)
    registration_timestamp = DateTimeField(default=datetime.now())


class Admin(_BaseModel):
    class Meta:
        db_table = 'admins'

    telegram_id = BigIntegerField(unique=True, null=False)
    name = CharField()


def register_models() -> None:
    for model in _BaseModel.__subclasses__():
        model.create_table()
