#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################
# ------------ Signal handler ------------ #
############################################

import glob
import time
import os
import signal
import sys


def signal_handler(sig, frame):
    print("\nI3Battery stop!")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

############################################
# ------------ Notify manager ------------ #
############################################

def notify_warning(use, level):
    os.system("{} '{}'".format(use, str(level)))

def audio_warning(use):
    os.system("{} ~/.config/i3battery/warning.ogg".format(use))

############################################
# ------------- Config loader ------------ #
############################################

audio = False
audio_use = "play"
notify = True
notify_use = "notify-send"
warning_threshold = [20, 15, 5]

for arg in sys.argv[1:]:
    key_value = arg.split("=")

    if "--audio" in key_value[0]:
        audio = True

    if "--audio_use" in key_value[0]:
        audio_use = str(key_value[1])

    if "--no-notify" in key_value[0]:
        notify = False

    if "--notify_use" in key_value[0]:
        notify_use = str(key_value[1])

    if "--wt" in key_value[0]:
        warnings = key_value[1].split(",")
        for threshold in range(len(warnings)):
            warning_threshold[threshold] = (int)(warnings[threshold])

############################################
# ------------ Battery manager ----------- #
############################################

power_path = "/sys/class/power_supply/"

batteries = list()
for bat_dir in glob.glob(power_path + "BAT*"):
    batteries.append(bat_dir)

battery = "BAT0" if "BAT0" in batteries.pop() else exit()

has_alerted1 = False
has_alerted2 = False
has_alerted3 = False

power_supply_online = True if float(
    open(power_path + "AC/online", 'r').read()) == 1 else False

has_alerted_full = False
has_alerted_charging = power_supply_online
has_alerted_discharging = not power_supply_online

while True:
    power_supply_online = True if float(
        open(power_path + "AC/online", 'r').read()) == 1 else False
    capacity = float(open(power_path+battery+"/capacity", 'r').read())
    print("-"*10)
    print("Power: {}%".format(capacity))
    print("Status: {}".format(
        "Discharging" if not power_supply_online else "Charging"))

    if not power_supply_online:

        if capacity < warning_threshold[2] and not has_alerted3 and has_alerted2:
            has_alerted3 = True
            if notify:
                notify_warning(notify_use,
                    "Warning: battery below {}".format(warning_threshold[2]))
            if audio:
                audio_warning(audio_use)

        if capacity < warning_threshold[1] and not has_alerted2 and has_alerted1:
            has_alerted2 = True
            if notify:
                notify_warning(notify_use,
                    "Warning: battery below {}".format(warning_threshold[1]))
            if audio:
                audio_warning(audio_use)

        if capacity < warning_threshold[0] and not has_alerted1:
            has_alerted1 = True
            if notify:
                notify_warning(notify_use,
                    "Warning: battery below {}".format(warning_threshold[0]))
            if audio:
                audio_warning(audio_use)

        if has_alerted_charging and not has_alerted_discharging:
            has_alerted_discharging = False
            if notify:
                notify_warning(notify_use,"Warning: battery discharging")

        has_alerted_charging = False
        has_alerted_full = False
    else:
        has_alerted1 = False
        has_alerted2 = False
        has_alerted3 = False
        has_alerted_discharging = False

        if not has_alerted_charging:
            has_alerted_charging = True
            if notify:
                notify_warning(notify_use,"Notice: battery charging")

        if capacity >= 98:
            if not has_alerted_full:
                has_alerted_full = True
                if notify:
                    notify_warning(notify_use,"Notice: battery full")

    time.sleep(10)
