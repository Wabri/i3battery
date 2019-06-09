install:
	sudo rm -f /usr/bin/i3battery
	sudo cp -r ../i3battery /opt
	sudo ln -s /opt/i3battery/i3battery.py /usr/bin/i3battery

notify: install
	python3 -m pip install notify2

audio: install
	mkdir -p ~/.config/i3battery/audio/
	sudo cp resources/audio/* ~/.config/i3battery/audio/
	python3 -m pip install pygame

all: audio notify

unistall:
	sudo rm -rf /usr/bin/i3battery
	sudo rm -rf /opt/i3battery/
	sudo rm -rf ~/.config/i3battery
