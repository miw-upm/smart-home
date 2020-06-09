import time

from gpiozero import Button

from smart_home.bindings.gpio import Pin


class PushButton:
    ANTI_BOUNCE_TIME = 0.2
    LONG_PRESS_TIME = 1
    DOUBLE_CLICK_TIME = 2

    def __init__(self, name: str, pin: Pin, kind="Button"):
        self.name = name
        self.pin = pin
        self.__button = Button(pin.value, hold_time=PushButton.LONG_PRESS_TIME)
        self.kind = kind
        self.__last_time = time.time()
        self.when_click = None
        self.when_double_click = None
        self.when_long_press = None
        self.__button.when_pressed = self.__pressed
        self.__button.when_held = self.__held

    def __pressed(self):
        rise_time = time.time() - self.__last_time
        if rise_time < PushButton.ANTI_BOUNCE_TIME:
            return
        self.__last_time = time.time()
        if rise_time < PushButton.DOUBLE_CLICK_TIME:
            if self.when_double_click is not None:
                self.when_double_click()
        else:
            if self.when_click is not None:
                self.when_click()

    def __held(self):
        self.__last_time = time.time()
        if self.when_long_press is not None:
            self.when_long_press()
