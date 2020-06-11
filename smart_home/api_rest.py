import os
import subprocess

from fastapi import FastAPI

from smart_home.models import ItemCreation, RuleCreation, LightAction
from smart_home.services import gpio_service

app = FastAPI()


@app.get("/system/app-info")
def read_app_info():
    return {"app_info": "smart-home-r1"}


@app.post("/system/reboot")
def reboot():
    os.system('sudo reboot now')


@app.post("/system/shutdown")
def reboot():
    os.system('sudo shutdown now')


@app.post("/system/update")
def update():
    subprocess.Popen("cd /home/pi/PycharmProjects/smart-home", shell=True)
    result = subprocess.Popen("git pull origin master", shell=True, stdout=subprocess.PIPE)
    subprocess.Popen("sudo python3 /home/pi/PycharmProjects/smart-home/setup.py install", shell=True,
                               stdout=subprocess.PIPE)
    return {"git": result.stdout.read()}


@app.post("/items")
def create_item(item_creation: ItemCreation):
    gpio_service.create_item(item_creation)


@app.get("/items")
def read_items():
    return gpio_service.read_items()


@app.post("/rules")
def create_rules(rule_creation: RuleCreation):
    print(rule_creation)
    gpio_service.create_rule(rule_creation)


@app.get("/lights")
def read_lights():
    return gpio_service.read_lights()


@app.put("/lights/{name}")
def switch_light(name: str, light_action: LightAction):
    return gpio_service.switch_light(name, light_action.switch)


@app.delete("/")
def delete_all():
    gpio_service.delete_all()


@app.post("/")
def create_all():
    gpio_service.create_all()
