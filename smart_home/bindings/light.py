from gpiozero import LED

from smart_home.bindings.gpio import Pin


class Light:
    def __init__(self, name: str, pin: Pin):
        self.name = name
        self.pin = pin
        self.__led = LED(pin.value, active_high=False)

    def on(self):
        self.__led.on()

    def off(self):
        self.__led.off()

    def toggle(self):
        self.__led.toggle()

    def is_on(self):
        return self.__led.is_active
