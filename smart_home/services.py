from smart_home.bindings import gpio
from smart_home.bindings.blind import Blind
from smart_home.bindings.light import Light
from smart_home.bindings.push_button import PushButton
from smart_home.entities import db, PinEntity, ItemEntity, RuleEntity, RuleActionEntity
from smart_home.bindings.gpio import Pin
from smart_home.models import ItemCreation, Item, RuleCreation, LightDto
from smart_home.rules import SimpleRule, TwoLightsRule, BlindRule


class GpioService:
    lights = dict()
    buttons = dict()
    blinds = dict()

    def __init__(self):

        self.start_gpios()
        self.start_rules()

    def start_gpios(self):
        for item in ItemEntity.select().where(ItemEntity.kind == 'Light').prefetch(PinEntity):
            self.lights[item.name] = Light(name=item.name, pin=item.pins[0].name)
        for item in ItemEntity.select().where(ItemEntity.kind == 'PushButton').prefetch(PinEntity):
            self.buttons[item.name] = PushButton(name=item.name, pin=item.pins[0].name)
        for item in ItemEntity.select().where(ItemEntity.kind == 'Blind').prefetch(PinEntity):
            self.blinds[item.name] = Blind(name=item.name, pin_up=item.pins[0].name, pin_down=item.pins[1].name)
        db.close()

    def start_rules(self):
        for rule in RuleEntity.select().where(RuleEntity.kind == 'SimpleRule').prefetch(RuleActionEntity):
            SimpleRule(rule.name, self.buttons[rule.trigger.name], self.lights[rule.actions[0].item.name])
        for rule in RuleEntity.select().where(RuleEntity.kind == 'TwoLightsRule').prefetch(RuleActionEntity):
            TwoLightsRule(rule.name, self.buttons[rule.trigger.name], self.lights[rule.actions[0].item.name],
                          self.lights[rule.actions[1].item.name])
        for rule in RuleEntity.select().where(RuleEntity.kind == 'BlindRule').prefetch(RuleActionEntity):
            BlindRule(rule.name, self.buttons[rule.trigger.name], self.blinds[rule.actions[0].item.name])
        print('start rules...')

    @db.atomic()
    def create_item(self, item_creation: ItemCreation):
        light1 = ItemEntity.create(name=item_creation.name, kind=item_creation.kind)
        PinEntity.create(owner=light1, type="l1", name=Pin[item_creation.pin])

    def read_items(self):
        items = []
        for item in ItemEntity.select().prefetch(PinEntity):
            pins = ""
            for pin in item.pins:
                pins = pins + str(pin.name) + " "
            items.append(Item(id=item.id, name=item.name, kind=item.kind, pin=pins))
        print(items)
        return items

    @db.atomic()
    def create_rule(self, rule_creation: RuleCreation):
        button1 = ItemEntity.select().where(ItemEntity.name == rule_creation.trigger)
        rule1 = RuleEntity.create(name=rule_creation.name, kind=rule_creation.kind, trigger=button1)
        for item in rule_creation.items:
            light = ItemEntity.select().where(ItemEntity.name == item)
            RuleActionEntity.create(owner=rule1, item=light)

    def read_lights(self):
        light_dtos = []
        for light in self.lights.values():
            light_dtos.append(LightDto(name=light.name, on=light.is_on(), pin=light.pin.name))
        return light_dtos

    def switch_light(self, name, value):
        if value:
            self.lights[name].on()
        else:
            self.lights[name].off()
        return LightDto(name=self.lights[name].name, on=self.lights[name].is_on(), pin=self.lights[name].pin.name)

    def create_all(self):
        light1 = ItemEntity.create(name="r1-light-ceiling", kind="Light")
        PinEntity.create(owner=light1, type="l1", name=gpio.Pin.OUT_0)
        light2 = ItemEntity.create(name="r2-light-ceiling", kind="Light")
        PinEntity.create(owner=light2, type="l2", name=gpio.Pin.OUT_1)
        light3 = ItemEntity.create(name="r2-light-bedhead", kind="Light")
        PinEntity.create(owner=light3, type="l3", name=gpio.Pin.OUT_2)
        button1 = ItemEntity.create(name="r1-button", kind="PushButton")
        PinEntity.create(owner=button1, type="b1", name=gpio.Pin.IN_0)
        button2 = ItemEntity.create(name="r2-button-entry", kind="PushButton")
        PinEntity.create(owner=button2, type="b2", name=gpio.Pin.IN_1)
        button3 = ItemEntity.create(name="r2-button-bedhead", kind="PushButton")
        PinEntity.create(owner=button3, type="b3", name=gpio.Pin.IN_2)
        button4 = ItemEntity.create(name="r2-button-blind", kind="PushButton")
        PinEntity.create(owner=button4, type="b4", name=gpio.Pin.IN_3)
        blind1 = ItemEntity.create(name="r2-blind", kind="Blind")
        PinEntity.create(owner=blind1, type="up", name=gpio.Pin.OUT_3)
        PinEntity.create(owner=blind1, type="down", name=gpio.Pin.OUT_4)
        rule1 = RuleEntity.create(name="rule1", kind='SimpleRule', trigger=button1)
        RuleActionEntity.create(owner=rule1, item=light1)
        rule2 = RuleEntity.create(name="rule2", kind='TwoLightsRule', trigger=button2)
        RuleActionEntity.create(owner=rule2, item=light2)
        RuleActionEntity.create(owner=rule2, item=light3)
        rule3 = RuleEntity.create(name="rule3", kind='TwoLightsRule', trigger=button3)
        RuleActionEntity.create(owner=rule3, item=light3)
        RuleActionEntity.create(owner=rule3, item=light2)
        rule4 = RuleEntity.create(name="rule4", kind='BlindRule', trigger=button4)
        RuleActionEntity.create(owner=rule4, item=blind1)
        db.close()

    def delete_all(self):
        RuleActionEntity.delete().execute()
        RuleEntity.delete().execute()
        PinEntity.delete().execute()
        ItemEntity.delete().execute()
        db.close()


gpio_service = GpioService()
