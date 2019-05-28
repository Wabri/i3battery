all: audio notify

install: pip
	sudo chmod +x i3battery.py
	sudo cp i3battery.py /usr/bin/i3battery

notify: install
	python3 -m pip install notify2

audio: install
	mkdir -p ~/.config/i3battery/audio/
	sudo cp resources/audio/* ~/.config/i3battery/audio/
	python3 -m pip install pygame

pip:
	sudo apt install python3-pip

unistall:
	sudo rm -r /usr/bin/i3battery
	sudo rm -r ~/.config/i3battery
