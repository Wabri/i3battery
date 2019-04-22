install:
	sudo chmod +x i3battery.py
	sudo cp i3battery.py /usr/bin/i3battery
	mkdir ~/.config/i3battery
	sudo cp resources/warning.ogg ~/.config/i3battery/warning.ogg

all: install
	sudo apt-get install libnotify-bin notify-osd sox

unistall:
	sudo rm -r /usr/bin/i3battery
	sudo rm -r ~/.config/i3battery
