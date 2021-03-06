# i3battery

[![CircleCI](https://circleci.com/gh/Wabri/i3battery.svg?style=svg)](https://circleci.com/gh/Wabri/i3battery)

![LOGO](resources/LOGO.png)

I made this script for my configuration of [i3wm](i3wm.org) because in this distro there isn't a battery warning notifier.

This script regularly checks your battery charge and shows a warning in a text notify and if abilitate also an audio warning if you are about to completely drain your battery.

## Install

You need to clone the repository with:

```bash
git clone https://github.com/Wabri/i3battery
```

Then move into i3battery directory:

```bash
cd i3battery
```

And finally run and install i3battery:

```Bash
./install.sh
```

Try to run the help command:

```Bash
i3battery --help
```

If this return the commands list you can use than the i3battery is installed and you can use it.

To test notifications and audio you can use the arguments test:

```bash
i3battery --test-notify --test-audio
```

## Configurations

There are some arguments that you can use to change the configuration:

* **`--audio`** to abilitate audio (default=disable)
* **`--audio_path=<path_to_audio_directory>`** to specify the audio directory (default=.config/i3battery/audio/)
* **`--no-notify`** to disabilitate notifications (default=abilitate)
* **`--wt=<wt1>,<wt2>,<wt3>`** to set the warning threshold to different values (default=20,15,5)
* **`--time=<value>`** to define the time of cycle (default=20)
* **`--power-path=<value>`** to specify the path of the system class power supply (default=/sys/class/power_supply/)
* **`--bat=<value>`** to specify the battery you want to use (default=BAT0)

Here is an example:

```bash
i3battery --audio --audio-path=/home/wabri/.config/i3battery/audio/ --wt=77,78,76 --time=7 --power-path=/sys/class/power_supply/ --bat=BAT0
```

The default audio warning is installed on `~/.config/i3battery/audio/`, you can change by override the files inside it (Warning: need to be wav files):

* `warning.wav` -> use when reach one of the threshold
* `plug-in.wav` -> use when the adapter goes online
* `plug-out.wav` -> use when the adapter goes offline

## I3 users

To use this on i3wm you need to append to your i3 config file this line:

```i3wm
exec --no-startup-id i3battery
```

The most common use is audio without notifications:

```i3wm
exec --no-startup-id i3battery --audio --no-notify
```

You can configure the running with the configurations below.

## How to make sure the used battery is the right one

Execute this command on terminal:

```Bash
ls /sys/class/power_supply/ | grep "BAT"
```

This can have multiple output:

1. The output is not null and return only the **BAT0** string, you don't need to do anything else and you can use the script as is.
2. You have more than one batteries the output will be something like this:

    ```Bash
    BAT0 BAT1 BAT2
    ```

    In this case you need to specify what battery you want to use for this script by adding this argument:

    ```Bash
    i3battery --bat=BAT2
    ```

3. You have no output, this is the hard one. Maybe your power supply are stored in other path, than you need to find it and add the argument for that path:

    ```Bash
    i3battery --power-path=/sys/class/power_supply/
    ```

    Make sure to use the right battery even in this case (e.g. BAT1, BAT0)
