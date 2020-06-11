import threading
import time
from enum import Enum

from gpiozero import DigitalOutputDevice

from smart_home.bindings.gpio import Pin


class State(Enum):
    UP = 0
    DOWN = 1


class Blind:
    DELAY_TIME = 13 + 7

    def __init__(self, name: str, pin_up: Pin, pin_down: Pin, kind="Blind"):
        self.name = name
        self.pin_up = pin_up
        self.pin_down = pin_down
        self.__blind_up = DigitalOutputDevice(pin_up.value, active_high=False)
        self.__blind_down = DigitalOutputDevice(pin_down.value, active_high=False)
        self.kind = kind
        self.__state = State.DOWN
        self.stop()
        print('INFO:     Blind:', pin_up.name, '-', pin_down.value, pin_up.name, '-', pin_down.value)

    def __delay_stop(self):
        time.sleep(self.DELAY_TIME)  # double time
        self.stop()

    def stop(self):
        self.__blind_up.off()
        self.__blind_down.off()

    def down(self):
        self.__blind_up.off()
        self.__blind_down.on()
        self.__state = State.DOWN
        threading.Thread(target=self.__delay_stop).start()

    def up(self):
        self.__blind_down.off()
        self.__blind_up.on()
        self.__state = State.UP
        threading.Thread(target=self.__delay_stop).start()

    def toggle(self):
        if self.__state == State.UP:
            self.down()
        else:
            self.up()

    def keep_on(self):
        if self.__state == State.UP:
            self.up()
        else:
            self.down()

    def is_moving(self) -> bool:
        return self.__blind_up.is_active or self.__blind_down.is_active
