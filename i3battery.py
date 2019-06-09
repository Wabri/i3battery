#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import signal
import sys
import time

import modules.Helper as hp
import modules.Warner as wr
import modules.Signaler as sn

############################################
# ------------- Main Script -------------- #
############################################

print('-'*79)
hp.Helper().print_infos()

if __name__== '__main__':
    signal.signal(signal.SIGINT, sn.Signaler().signal_handler)

    helper = hp.Helper()
    warner = wr.Warner()

    args = sys.argv[1:]

    if '--help' in args:
        print('-'*79)
        helper.print_help()
        exit()

    print('-'*79)
    print("Load i3Battery configuration")
    print()
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

    for arg in args:
        key_value = arg.split("=")

        if '--audio' in key_value[0]:
            print("Setting up audio")
            audio = True
            print("audio={}".format(audio))

        if '--audio-path' in key_value[0]:
            print("Setting up audio path")
            audio_path = key_value[1]
            print("audio_path={}".format(audio_path))

        if '--no-notify' in key_value[0]:
            print("Setting up no notifications")
            notify = False
            print("notify={}".format(notify))

        if '--wt' in key_value[0]:
            print("Setting up warning threshold")
            warnings = key_value[1].split(",")
            for threshold in range(len(warnings)):
                warning_threshold[threshold] = (float)(warnings[threshold])
                print("warning_threshold {}={}".format(
                    threshold, warnings[threshold]))

        if '--time' in key_value[0]:
            print("Setting up time cycle")
            time_cycle = float(key_value[1])
            print("time_cycle={}".format(time_cycle))

        if '--power-path' in key_value[0]:
            print("Setting up power_path")
            power_path = key_value[1]
            print("power_path={}".format(power_path))

        if '--bat' in key_value[0]:
            print("Setting up battery")
            battery = key_value[1]
            print("battery={}".format(battery))

        if '--test-audio' in key_value[0]:
            test_audio = True

        if '--test-notify' in key_value[0]:
            test_notify = True

    if test_audio:
        print("Audio test")
        print("Warning audio")
        warner.audio_warning(audio_path + "warning.wav")
        print("Plug-in audio")
        warner.audio_warning(audio_path + "plug-in.wav")
        print("Plug-out audio")
        warner.audio_warning(audio_path + "plug-out.wav")

    if test_notify:
        print("Notify test")
        warner.notify_warning('Notification Test', 'NO_BATTERY', "Test")

    if test_audio or test_notify:
        print('-'*79)
        exit()

    warning_threshold = sorted(warning_threshold, reverse=False)
    battery_path = power_path + battery

    print("-"*79)
    print("I3battery start")
    print("-"*79)

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
        print("Power: {}%".format(capacity))
        print("Status: {}".format(
            "Discharging" if not power_supply_online else "Charging"))

        if not power_supply_online:

            if has_alerted_charging and not has_alerted_discharging:
                has_alerted_discharging = False
                if notify:
                    warner.notify_warning('I3Battery warning', battery, 'discharging')
                if audio:
                    warner.audio_warning(audio_path+"plug-out.wav")

            if capacity < warning_threshold[threshold] and not has_alerted[threshold]:
                has_alerted[threshold] = True
                print("Warning battery below threshold {}".format(
                    warning_threshold[threshold]))
                if notify:
                    warner.notify_warning('I3Battery warning', battery, 'battery below {}'.format(
                        warning_threshold[threshold]))
                if audio:
                    warner.audio_warning(audio_path+"warning.wav")
                threshold -= 1

            has_alerted_charging = False
            has_alerted_full = False

        else:
            has_alerted = [False, False, False]
            has_alerted_discharging = False
            threshold = 2

            if not has_alerted_charging:
                has_alerted_charging = True
                if notify:
                    warner.notify_warning('I3Battery notice', battery, 'charging')
                if audio:
                    warner.audio_warning(audio_path+"plug-in.wav")

            if capacity >= 98:
                if not has_alerted_full:
                    has_alerted_full = True
                    if notify:
                        warner.notify_warning('I3Battery notice', battery, 'full')

        print("-"*79)
        time.sleep(time_cycle)

print('-'*79)
