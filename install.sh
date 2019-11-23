#!/usr/bin/env bash

_remove_older_i3battery() {
	sudo rm -rf /usr/bin/i3battery
	sudo rm -rf /opt/i3battery/
}

_install_i3battery() {
	sudo cp -rp packages/i3battery /opt/i3battery
	sudo ln -s /opt/i3battery/i3battery.py /usr/bin/i3battery
}

_create_configuration() {
	mkdir -p ~/.config/i3battery/audio
	sudo cp -r resources/audio ~/.config/i3battery/audio
}

_setting_up() {
	sudo apt install python3-pip
	python3 -m pip install pygame notify2
}

echo '******************************************'
echo '---> Launch older i3battery into space'
_remove_older_i3battery
echo '******************************************'
echo '---> Put new batteries on /opt/i3battery'
_install_i3battery
echo '******************************************'
echo '---> Prepare the music on .config/i3battery/'
_create_configuration
echo '******************************************'
echo '---> Letting the pilots enter in'
_setting_up
echo '******************************************'
echo '---> I3battery installation completed'
