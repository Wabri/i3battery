class Helper():
    """This class contains all the infos of i3battery to help user and mantainers.

    Attributes:
    ----------
        _help_info (str): Store the infos about the script and the reference of the project.
        _commands (dict: {str:[str,str]}): key-value of command that can be use with this software, the value is an array of infos that contains
            the explanation of teh command and the second value is the how is used in the argument format for the script.
        _help_command_example (str): An usage example of the script with all the commands.

    """


    _help_info = 'I3battery infos\n\nWeb Repository: https://github.com/Wabri/i3battery\nVersion: 1.0.1\nMantainers: Wabri - Gabriele Puliti'

    _commands = {
        '--help': [
            'Print all the command and usage',
            '--help'
        ],
        '--audio': [
            'Abilitate audio (default=disabled)',
            '--audio'
        ],
        '--audio-path': [
            'Set the audio path (default=~/.config/i3battery/audio/)',
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
        ],
        '--test-audio': [
            'Use it to test the audio notifications',
            '--test-audio'
        ],
        '--test-notify': [
            'Use it to test the notifications functionality',
            '--test-notify'
        ]
    }

    _help_command_example = 'i3battery --audio --audio-path=/home/wabri/.config/i3battery/audio/ --wt=77,78,76 --time=7 --power-path=/sys/class/power_supply/ --bat=BAT0'


    def print_infos(self):
        """This method is used to print the infos of the project: repository URL, version and mantainers.

        Simply print some infos about the i3battery stored in the Helper class.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        print(self._help_info)


    def print_help(self):
        """This is the method to retrive the help page of the i3battery.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self.print_infos()
        print("Usage: i3battery", end=" ")
        for key in self._commands.keys():
            print("[{}]".format(self._commands[key][1]), end=" ")
        print("\n\nThese are the common i3battery argument:")
        for key in self._commands.keys():
                print('   {}   {}'.format(key, self._commands[key][0]))
        print()
        print("Here it's an example:")
        print('   {}'.format(self._help_command_example))

