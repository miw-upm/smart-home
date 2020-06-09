from peewee import Model, SqliteDatabase, CharField, Field, ForeignKeyField

from smart_home.bindings import gpio

DATABASE_NAME = "/home/pi/data/smart-home.db"
db = SqliteDatabase(DATABASE_NAME, field_types={'pin': 'text'}, check_same_thread=False)


class PinField(Field):
    field_type = "pin"

    def db_value(self, value: gpio.Pin):
        return value.name

    def python_value(self, value):
        return gpio.Pin[value]


class Entity(Model):
    class Meta:
        database = db


class ItemEntity(Entity):
    name = CharField(unique=True)
    kind = CharField()


class PinEntity(Entity):
    name = PinField(unique=True)
    type = CharField()
    owner = ForeignKeyField(ItemEntity, backref='pins')


class RuleEntity(Entity):
    name = CharField(unique=True)
    kind = CharField()
    trigger = ForeignKeyField(ItemEntity)


class RuleActionEntity(Entity):
    owner = ForeignKeyField(RuleEntity, backref='actions')
    item = ForeignKeyField(ItemEntity)


db.create_tables([ItemEntity, PinEntity, RuleEntity, RuleActionEntity])