#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import signal
import sys
import time

try:
  os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
  from pygame import mixer
except:
  print("-"*20)
  print("Audio support are not installed")
  print("Read the installation guide on: https://github.com/Wabri/i3battery#install")
  print("-"*20)
  print("")
 
try:
  import notify2
except:
  print("-"*20)
  print("Notify support are not installed")
  print("Read the installation guide on: https://github.com/Wabri/i3battery#install")
  print("-"*20)
  print("")

  
############################################
# ------------ Notify manager ------------ #
############################################

def notify_warning(notification_type, battery_name, text_show):
    notify2.init(notification_type)
    n = notify2.Notification(notification_type, battery_name + ' - ' + text_show)
    n.show()

    
def audio_warning(path):
    mixer.init()
    sound = mixer.Sound(path)
    sound.play()
    time.sleep(sound.get_length())
    mixer.quit()


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

power_path = "/sys/class/power_supply/"
battery = "BAT0"
audio = False
audio_path = os.path.expanduser('~') + '/.config/i3battery/audio/'
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

    if "--audio-path" in key_value[0]:
        audio_path = key_value[1]

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

    if "--test-audio" in key_value[0]:
        test_audio = True

    if "--test-notify" in key_value[0]:
        test_notify = True

    if "--power-path" in key_value[0]:
        power_path = key_value[1]

    if "--bat" in key_value[0]:
        battery = key_value[1]

if test_audio:
    print("Audio test")
    audio_warning(audio_path + "warning.wav")

if test_notify:
    notify_warning('Notification Test', 'NO_BATTERY', "Test")

if test_audio or test_notify:
    exit()

warning_threshold = sorted(warning_threshold, reverse=True)
battery_path = power_path + battery


############################################
# ------------ Battery manager ----------- #
############################################

adapter = glob.glob(power_path+"AC*")[0]

has_alerted = [False, False, False]

threshold = 2

power_supply_online = True if float(
    open(adapter+"/online", 'r').read()) == 1 else False

has_alerted_full = False
has_alerted_charging = power_supply_online
has_alerted_discharging = not power_supply_online

threshold = 2

while True:
    power_supply_online = True if float(
        open(adapter+"/online", 'r').read()) == 1 else False
    capacity = float(open(battery_path+"/capacity", 'r').read())
    print("-"*10)
    print("Power: {}%".format(capacity))
    print("Status: {}".format(
        "Discharging" if not power_supply_online else "Charging"))

    if not power_supply_online:

        if capacity < warning_threshold[threshold] and not has_alerted[threshold] and has_alerted[threshold - 1]:
            has_alerted[threshold] = True
            print("Warning battery below threshold {}".format(
                warning_threshold[threshold]))
            if notify:
                notify_warning(notify_use,
                               "Warning: battery below {}".format(warning_threshold[threshold]))
            if audio:
                audio_warning(audio_path+"warning.wav")
            threshold -= 1

        if has_alerted_charging and not has_alerted_discharging:
            has_alerted_discharging = False
            if notify:
                notify_warning(notify_use, "Warning: battery discharging")
            if audio:
                audio_warning(audio_path+"plug-out.wav")

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
            if audio:
                audio_warning(audio_path+"plug-in.wav")

        if capacity >= 98:
            if not has_alerted_full:
                has_alerted_full = True
                if notify:
                    notify_warning(notify_use, "Notice: battery full")

    time.sleep(time_cycle)
