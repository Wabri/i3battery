install:
	sudo chmod +x i3battery.py
	sudo cp i3battery.py /usr/bin/i3battery
	mkdir ~/.config/i3battery
	sudo cp resources/warning.ogg ~/.config/i3battery/warning.ogg

notify: install
	python3 -m pip install notify2

all: notify

unistall:
	sudo rm -r /usr/bin/i3battery
	sudo rm -r ~/.config/i3battery
