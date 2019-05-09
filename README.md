# i3battery

![LOGO](LOGO.png)

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

* basics functions:

    ```bash
    make install
    ```

* all audio support and notifications:

    ```bash
    make all
    ```

Now you can use i3battery.

For the default audio settings you need to install sox:

```bash
sox
```

These dependencies are install with the make all command or you can install with apt-get.

To test notifications and audio you can use the argument test:

```bash
i3battery --test-notify --audio-notify --audio-use=<command_audio>
```

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

## Configurations

There are some arguments that you can use to change the configuration:

* **--audio** to abilitate audio (default=disable)
* **--audio_use=<command_to_use>** to specify the command to run the audio (default=play)
* **--no-notify** to disabilitate notifications (default=abilitate)
* **--wt=<wt1>,<wt2>,<wt3>** to set the warning threshold to different values (default=20,15,5)
* **--time=<value>** to define the time of cycle (default=20)

Here is an example:

```bash
i3battery --audio --audio_use=play --no-notify --wt=40,30,10 --time=5
```

The default audio warning is installed on `~/.config/i3battery/warning.wav`, you can change by override this file.

You can use different audio play with this arguments:

```bash
i3battery --audio_use=<command_to_use>
```
