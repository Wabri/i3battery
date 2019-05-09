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
# ------------ Global variables ---------- #
############################################

aspected_arguments = {
    'pre-config': [
        '--help'
    ],
    'pre-run': [
        '--test-audio',
        '--test-notify'
    ],
    'config': [
        '--audio',
        '--audio-path',
        '--no-notify',
        '--wt',
        '--time',
        '--power-path',
        '--bat'
    ]
}

############################################
# ------------ Help printer -------------- #
############################################

help_info = 'I3battery infos\n\nWeb Repository: https://github.com/Wabri/i3battery\nVersion: 1.0.1\nMantainers: Wabri - Gabriele Puliti'

help_output = {
    '--help': ['Print all the command and usage', '--help'],
    '--audio': ['Abilitate audio (default=disabled)', '--audio'],
    '--audio-path': ['Set the audio path (default=~/.config/i3battery/audio/', '--audio-path=<absolute_path>'],
    '--no-notify': ['Disabilitate notification (default=abilitated)', '--no-notify'],
    '--wt': ['Set the warning threshold to different values. You can use a non order list of the value, the scripts order for you. You can set up max 3 values. (default=20,15,5)', '--wt=<value_1>,<value_2>,<value_3>'],
    '--time': ['Define the time of cycle (default=20)', '--time=<seconds>'],
    '--power-path': ['Specify the path of the system class power supply (default=/sys/class/power_supply/)', '--power-path=<absolute_path>'],
    '--bat': ['Specify the battery you want to use (default=BAT0)', '--bat=<battery_name>'],
    '--test-audio': ['Use it to test the audio notifications', '--test-audio'],
    '--test-notify': ['Use it to test the notifications functionality', '--test-notify']
}

help_command_example = 'i3battery --audio --audio-path=/home/wabri/.config/i3battery/audio/ --wt=77,78,76 --time=7 --power-path=/sys/class/power_supply/ --bat=BAT0'

def print_help():
    print('-'*20)
    print(help_info)
    print('-'*20)
    print()
    print("Usage: i3battery", end=" ")
    for key in help_output.keys():
        print("[{}]".format(help_output[key][1]), end=" ")
    print("\n\nThese are the common i3battery argument:")
    for key in help_output.keys():
        print('   {}   {}'.format(key, help_output[key][0]))
    print()
    print("Here it's an example:")
    print('   {}'.format(help_command_example))

############################################
# ------------ Notify manager ------------ #
############################################


def notify_warning(notification_type, battery_name, text_show):
    notify2.init(notification_type)
    n = notify2.Notification(
        notification_type, battery_name + ' - ' + text_show)
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
    print('-'*20)
    print(help_info)
    print('-'*20)
    print('Bye Bye!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

############################################
# ------------- Config loader ------------ #
############################################

args = sys.argv[1:]

if aspected_arguments['pre-config'][0] in args:
    print_help()
    exit()

print("-"*23)
print("I3Battery configuration")
print("-"*23)

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

    if aspected_arguments['config'][0] in key_value[0]:
        print("Setting up audio")
        audio = True
        print("audio={}".format(audio))

    if aspected_arguments['config'][1] in key_value[0]:
        print("Setting up audio path")
        audio_path = key_value[1]
        print("audio_path={}".format(audio_path))

    if aspected_arguments['config'][2] in key_value[0]:
        print("Setting up no notifications")
        notify = False
        print("notify={}".format(notify))

    if aspected_arguments['config'][3] in key_value[0]:
        print("Setting up warning threshold")
        warnings = key_value[1].split(",")
        for threshold in range(len(warnings)):
            warning_threshold[threshold] = (float)(warnings[threshold])
            print("warning_threshold {}={}".format(
                threshold, warnings[threshold]))

    if aspected_arguments['config'][4] in key_value[0]:
        print("Setting up time cycle")
        time_cycle = float(key_value[1])
        print("time_cycle={}".format(time_cycle))

    if aspected_arguments['config'][5] in key_value[0]:
        print("Setting up power_path")
        power_path = key_value[1]
        print("power_path={}".format(power_path))

    if aspected_arguments['config'][6] in key_value[0]:
        print("Setting up battery")
        battery = key_value[1]
        print("battery={}".format(battery))

    if aspected_arguments['pre-run'][0] in key_value[0]:
        test_audio = True

    if aspected_arguments['pre-run'][1] in key_value[0]:
        test_notify = True

if test_audio:
    print("Audio test")
    print("Warning audio")
    audio_warning(audio_path + "warning.wav")
    print("Plug-in audio")
    audio_warning(audio_path + "plug-in.wav")
    print("Plug-out audio")
    audio_warning(audio_path + "plug-out.wav")

if test_notify:
    print("Notify test")
    notify_warning('Notification Test', 'NO_BATTERY', "Test")

if test_audio or test_notify:
    exit()

warning_threshold = sorted(warning_threshold, reverse=False)
battery_path = power_path + battery


############################################
# ------------ Battery manager ----------- #
############################################

print("-"*15)
print("I3battery start")
print("-"*15)

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
                notify_warning('I3Battery warning', battery, 'discharging')
            if audio:
                audio_warning(audio_path+"plug-out.wav")

        if capacity < warning_threshold[threshold] and not has_alerted[threshold]:
            has_alerted[threshold] = True
            print("Warning battery below threshold {}".format(
                warning_threshold[threshold]))
            if notify:
                notify_warning('I3Battery warning', battery, 'battery below {}'.format(
                    warning_threshold[threshold]))
            if audio:
                audio_warning(audio_path+"warning.wav")
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
                notify_warning('I3Battery notice', battery, 'charging')
            if audio:
                audio_warning(audio_path+"plug-in.wav")

        if capacity >= 98:
            if not has_alerted_full:
                has_alerted_full = True
                if notify:
                    notify_warning('I3Battery notice', battery, 'full')

    print("-"*10)
    time.sleep(time_cycle)
