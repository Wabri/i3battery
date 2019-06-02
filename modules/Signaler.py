class Signaler():
############################################
# ------------ Signal handler ------------ #
############################################

    def signal_handler(self, sig, frame):
        from modules.Helper import Helper
        import sys
        print("\nI3Battery stop!")
        print('-'*79)
        Helper().print_infos()
        print('-'*79)
        print('Bye Bye!')
        sys.exit(0)
