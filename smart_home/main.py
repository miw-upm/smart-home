import os

import uvicorn

from smart_home.api_rest import app

if __name__ == "__main__":
    NET_UP = "inet "
    ip = "127.0.0.1"
    ip_eth0 = os.popen('ip addr show eth0').read()
    ip_wlan0 = os.popen('ip addr show wlan0').read()
    if NET_UP in ip_eth0:
        ip = ip_eth0.split(NET_UP)[1].split('/')[0]
    elif NET_UP in ip_wlan0:
        ip = ip_wlan0.split(NET_UP)[1].split('/')[0]
    uvicorn.run(app, host=ip)
