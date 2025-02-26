#!/bin/bash
export DISPLAY=:1
export XAUTHORITY=/home/pi/.Xauthority
chromium --noerrdialogs --kiosk http://192.168.222.104/elektromery/panel.htm?pars=[object%20Object]&opts=target%3Amain%3B

