class Warner():
    """This class define the methods to show notifications and sound warnings.
    """

    def notify_warning(self,notification_type, battery_name, text_show):
        """This method show notification pop-up.

        If the import of notify2 complete without errors starts the initialization
            of notification, otherwise print the infos to solve that errors.
        The notification variable is an Object of Notification class of the notify2
            library, when create the constructor take 3 arguments: title of the
            notification and the text to put down the title. In this case the title
            will be the name of the type of the warning and the text is the couple
            formed by the name of the battery analized (example: BAT0) and some more
            infos like the percentage of the battery.
        Once the notification variable are created, it can be show on screen with
            command show().

        Parameters
        ----------
        notification_type : str
            Type of the notification to show
        battery_name : str
            Name of the battery analized
        text_show : str
            Short description of the notification cause

        Returns
        -------
        bool
            True if there is no error in the notification, False otherwise.

        """
        try:
            import notify2
            notify2.init(notification_type)
            notification = notify2.Notification(
                notification_type, battery_name + ' - ' + text_show)
            notification.show()
            return True
        except:
            print("-"*79)
            print("Notify support are not installed")
            print("Read the installation guide on: https://github.com/Wabri/i3battery#install")
            print("-"*79)
            print()
            return False

    def audio_warning(self, path):
        """This method send an audio warning.

        If pygame library are not installed the method print some infos like where the user need
            to retrive the instruction to install that.
        Otherwise the mixer is initialized, the sound loaded and play. The time library is used
            to wait that sound is finished before continue.

        Parameters
        ----------
        path : str
           This argument is the path of the audio that need to be reproduce

        Returns
        -------
        bool
            True if there is no error in the audio, False otherwise.

        """
        try:
            import os
            import time
            os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
            from pygame import mixer
            mixer.init()
            sound = mixer.Sound(path)
            sound.play()
            time.sleep(sound.get_length())
            mixer.quit()
            return True
        except:
            print("-"*79)
            print("Audio support are not installed")
            print("Read the installation guide on: https://github.com/Wabri/i3battery#install")
            print("-"*79)
            print()
            return False

