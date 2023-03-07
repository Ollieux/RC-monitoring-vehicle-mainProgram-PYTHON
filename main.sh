#!/bin/bash

while ! ping -c1 google.com &>/dev/null; do sleep 1; done

source /home/rpi/project/env/bin/activate

python /home/rpi/Rpi-Repo/App/main.py