from modules.Helper import Helper
import sys

class Signaler():
    """This class contains all the method use to handle the interrupt.
    """

    def signal_handler(self, sig, frame):
        """This method is used to define how the script handle the interruption of some sort.

        Simply print some infos about the i3battery stored in the Helper class.

        Parameters
        ----------
        sig :
            The type of the signal
        frame :
            The frame argument is the stack frame, also known as execution frame. It point to the frame that was interrupted by the signal.
            The parameter is required because any thread might be interrupted by a signal, but the signal is only received in the main thread.

        Returns
        -------
        None

        """
        print("\nI3Battery stop!")
        print('-'*79)
        Helper().print_infos()
        print('-'*79)
        print('Bye Bye!')
        sys.exit(0)
