install:
	sudo chmod +x i3battery
	sudo cp i3battery.py /usr/bin/i3battery
	sudo cp resources/warning.ogg ~/.config/i3battery/warning.ogg
	sudo apt install sox
	sudo apt-get --reinstall install libnotify-bin notify-osd

add: install
	echo "\n#Start the battery notification script\nexec --no-startup-id i3battery" >> ~/.config/i3/config
