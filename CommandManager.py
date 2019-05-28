class CommandManager():

    _help_info = 'I3battery infos\n\nWeb Repository: https://github.com/Wabri/i3battery\nVersion: 1.0.1\nMantainers: Wabri - Gabriele Puliti'

    _commands = {
        'pre-config': {
            '--help': [
                'Print all the command and usage',
                '--help'
            ]
        },
        'config': {
            '--audio': [
                'Abilitate audio (default=disabled)',
                '--audio'
            ],
            '--audio-path': [
                'Set the audio path (default=~/.config/i3battery/audio/',
                '--audio-path=<absolute_path>'
            ],
            '--no-notify': [
                'Disabilitate notification (default=abilitated)',
                '--no-notify'
            ],
            '--wt': [
                'Set the warning threshold to different values. You can use a non order list of the value, the scripts order for you. You can set up max 3 values. (default=20,15,5)',
                '--wt=<value_1>,<value_2>,<value_3>'
            ],
            '--time': [
                'Define the time of cycle (default=20)',
                '--time=<seconds>'
            ],
            '--power-path': [
                'Specify the path of the system class power supply (default=/sys/class/power_supply/)', '--power-path=<absolute_path>'
            ],
            '--bat': [
                'Specify the battery you want to use (default=BAT0)',
                '--bat=<battery_name>'
            ]
        },
        'pre-run': {
            '--test-audio': [
                'Use it to test the audio notifications',
                '--test-audio'
            ],
            '--test-notify': [
                'Use it to test the notifications functionality',
                '--test-notify'
            ]
        }
}

    _help_command_example = 'i3battery --audio --audio-path=/home/wabri/.config/i3battery/audio/ --wt=77,78,76 --time=7 --power-path=/sys/class/power_supply/ --bat=BAT0'

    def print_help(self):
        print('-'*20)
        print(self._help_info)
        print('-'*20)
        print()
        print("Usage: i3battery", end=" ")
        for key_category in self._commands.keys():
            for key_argument in self._commands[key_category].keys():
                print("[{}]".format(self._commands[key_category][key_argument][1]), end=" ")
        print("\n\nThese are the common i3battery argument:")
        for key_category in self._commands.keys():
            for key_argument in self._commands[key_category].keys():
                print('   {}   {}'.format(key_argument, _commands[key_category][key_argument][0]))
        print()
        print("Here it's an example:")
        print('   {}'.format(_help_command_example))

    def get_pre_config_args(self):
        return self._commands['pre-config'].keys()

