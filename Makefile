install:
	sudo chmod +x i3battery.py
	sudo cp i3battery.py /usr/bin/i3battery
	mkdir -p ~/.config/i3battery/audio/
	sudo cp resources/* ~/.config/i3battery/audio/

notify: install
	sudo apt-get install libnotify-bin notify-osd

audio: install
	python3 -m pip install playsound

all: audio notify

unistall:
	sudo rm -r /usr/bin/i3battery
	sudo rm -r ~/.config/i3battery
