# i3battery

I made this script for my configuration of [i3wm](i3wm.org) because in this distro there isn't a battery warning notifier.

This script regularly checks your battery charge and shows a warning in a text notify and if abilitate also an audio warning if you are about to completely drain your battery.

## Dependencies

For the default notify settings you need to install a notify deamon:
```bash
apt-get install libnotify-bin notify-osd
```
For the default audio settings you need to install sox:
```bash
apt-get install sox
```

You can use different notify sender and audio play by set in arguments when i3battery is lauch:
```bash
i3battery --audio_use=<command_to_use> --notify_use=<command_to_use>
```

## Install

You need to clone the repository with:
```bash
git clone https://github.com/Wabri/i3battery
```
Then run the make file:
```bash
make install
```
Now you can use i3battery.

## I3 users

To use this on i3wm you need to append to your i3 config file this line:
```i3wm
exec --no-startup-id i3battery
```

## Configurations

There are some arguments that you can use to change the configuration:
* **--audio** to abilitate audio (default=disable)
* **--audio_use=<command_to_use>** to specify the command to run the audio (default=play)
* **--no-notify** to disabilitate notifications (default=abilitate)
* **--notify_use=<command_to_use>** to specify the command to run the notify (default=notify-send)
* **--wt=<wt1>,<wt2>,<wt3>** to set the warning threshold to different values (default=20,15,5)
* **--time=<value>** to define the time of cycle (default=20)

Here is an example:
```bash
i3battery --audio --audio_use=play --no-notify --notify_use=notify-send --wt=40,30,10 --time=5
```

The default audio warning is installed on `~/.config/i3battery/warning.ogg`, you can change by override this file.
