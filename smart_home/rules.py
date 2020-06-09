from smart_home.bindings.blind import Blind

from smart_home.bindings.light import Light
from smart_home.bindings.push_button import PushButton


class SimpleRule:
    def __init__(self, name: str, push_button: PushButton, light: Light):
        self.name = name
        self.__push_button = push_button
        self.__light = light
        self.__push_button.when_click = self.click
        self.__push_button.when_double_click = self.double_click

    def click(self):
        self.__light.toggle()

    def double_click(self):
        self.__light.toggle()


class TwoLightsRule:
    def __init__(self, name: str, push_button: PushButton, main: Light, secondary: Light):
        self.name = name
        self.__push_button = push_button
        self.__main = main
        self.__secondary = secondary
        self.__push_button.when_click = self.click
        self.__push_button.when_double_click = self.double_click
        self.__push_button.when_long_press = self.turn_on

    def click(self):
        if self.__main.is_on() or self.__secondary.is_on():
            self.turn_off()
        else:
            self.__main.on()

    def turn_on(self):
        self.__main.on()
        self.__secondary.on()

    def turn_off(self):
        self.__main.off()
        self.__secondary.off()

    def double_click(self):
        if not self.__main.is_on() and not self.__secondary.is_on():
            self.turn_off()
            self.__main.on()
        else:
            self.__main.toggle()
            self.__secondary.toggle()


class BlindRule:
    def __init__(self, name: str, push_button: PushButton, blind: Blind):
        self.name = name
        self.__push_button = push_button
        self.__blind = blind
        self.__push_button.when_click = self.click
        self.__push_button.when_double_click = self.double_click

    def click(self):
        if self.__blind.is_moving():
            self.__blind.stop()
        else:
            self.__blind.toggle()

    def double_click(self):
        self.__blind.toggle()
