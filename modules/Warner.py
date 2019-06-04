class Warner():
############################################
# ------------ Notify manager ------------ #
############################################


    def notify_warning(self,notification_type, battery_name, text_show):
        try:
            import notify2
            notify2.init(notification_type)
            n = notify2.Notification(
                notification_type, battery_name + ' - ' + text_show)
            n.show()
        except:
            print("-"*79)
            print("Notify support are not installed")
            print("Read the installation guide on: https://github.com/Wabri/i3battery#install")
            print("-"*79)
            print()



    def audio_warning(self, path):
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
        except:
            print("-"*79)
            print("Audio support are not installed")
            print("Read the installation guide on: https://github.com/Wabri/i3battery#install")
            print("-"*79)
            print()

