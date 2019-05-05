#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import glob
import time
import os
import signal
import sys

############################################
# ------------ Signal handler ------------ #
############################################


def signal_handler(sig, frame):
    print("\nI3Battery stop!")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


############################################
# ------------- Config loader ------------ #
############################################


audio = False
audio_use = "play"
notify = True
notify_use = "notify-send"
warning_threshold = [20, 15, 5]
time_cycle = 20.0
test_audio = False
test_notify = False

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

    if "--time" in key_value[0]:
        time_cycle = float(key_value[1])

    if "--test_audio" in key_value[0]:
        test_audio = True

    if "--test_notify" in key_value[0]:
        test_notify = True

if test_audio:
    audio_warning(audio_use)

if test_notify:
    notify_warning(notify_use, "Test")

if test_audio or test_notify:
    exit()

warning_threshold = sorted(warning_threshold, reverse=True)

############################################
# ------------ Notify manager ------------ #
############################################


def notify_warning(use, text):
    os.system("{} '{}'".format(use, str(text)))


def audio_warning(use):
    os.system("{} ~/.config/i3battery/warning.ogg".format(use))


############################################
# ------------ Battery manager ----------- #
############################################

power_path = "/sys/class/power_supply/"

batteries = list()
for bat_dir in glob.glob(power_path + "BAT*"):
    batteries.append(bat_dir)

adapter = glob.glob(power_path+"AC*")[0]

battery = "BAT0" if "BAT0" in batteries.pop() else exit()

has_alerted = [False, False, False]
threshold = 2

power_supply_online = True if float(
    open(adapter+"/online", 'r').read()) == 1 else False

has_alerted_full = False
has_alerted_charging = power_supply_online
has_alerted_discharging = not power_supply_online

while True:
    power_supply_online = True if float(
        open(adapter+"/online", 'r').read()) == 1 else False
    capacity = float(open(power_path+battery+"/capacity", 'r').read())
    print("-"*10)
    print("Power: {}%".format(capacity))
    print("Status: {}".format(
        "Discharging" if not power_supply_online else "Charging"))

    if not power_supply_online:

        if capacity < warning_threshold[threshold] and not has_alerted[threshold] and has_alerted[threshold - 1]:
            has_alerted[threshold] = True
            print("Warning battery below threshold {}".format(warning_threshold[threshold]))
            if notify:
                notify_warning(notify_use,
                               "Warning: battery below {}".format(warning_threshold[threshold]))
            if audio:
                audio_warning(audio_use)
            threshold -= 1

        if has_alerted_charging and not has_alerted_discharging:
            has_alerted_discharging = False
            if notify:
                notify_warning(notify_use, "Warning: battery discharging")

        has_alerted_charging = False
        has_alerted_full = False
    else:
        has_alerted = [False, False, False]
        has_alerted_discharging = False
        threshold = 2

        if not has_alerted_charging:
            has_alerted_charging = True
            if notify:
                notify_warning(notify_use, "Notice: battery charging")

        if capacity >= 98:
            if not has_alerted_full:
                has_alerted_full = True
                if notify:
                    notify_warning(notify_use, "Notice: battery full")

    time.sleep(time_cycle)
