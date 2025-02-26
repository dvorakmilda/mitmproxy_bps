#!/bin/bash
export DISPLAY=:0
export XAUTHORITY=/home/pi/.Xauthority
chromium --noerrdialogs --kiosk http://192.168.222.104/schema/panel.htm --incognito

