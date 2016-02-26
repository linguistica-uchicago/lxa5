# -*- encoding: utf8 -*-

from PyQt5.QtCore import (QThread, pyqtSignal)

# We spawn another
# thread to set up a "Linguistica component worker" using QThread.
# In this way, this worker (with lots of heavy computational work) works in a
# separate thread that is not the main thread for the GUI, and therefore the GUI
# stays responsive and (most probably) nothing freezes.


class LinguisticaWorker(QThread):

    # progress_signal is a custom PyQt signal. It has to be defined within this
    # QThread subclass but *outside* __init__ here.

    progress_signal = pyqtSignal(str, int)
    # str is for the progress label text
    # int is the progress percentage target, for updating the progress bar
    # bool (True or False) is whether the progress percentage increments
    #   gradually or not

    def __init__(self, lexicon, parent=None):
        QThread.__init__(self, parent)

        self.lexicon = lexicon

    def run(self):
        # this "run" method is never explicitly called
        # it is run by the built-in "start" method of this QThread

        # What happens here:  Each of the Linguistica component
        # is run for the specified corpus file with the specified parameters.
        # When a component is done, emit a signal with info to update the
        # progress dialog label text and progress bar

        self.progress_signal.emit("Extracting word ngrams...", 0)
        self.lexicon.run_phon_module(verbose=True)

        self.progress_signal.emit('Computing morphological signatures...', 20)
        self.lexicon.run_signature_module(verbose=True)

        self.progress_signal.emit('Computing tries...', 40)
        self.lexicon.run_trie_module(verbose=True)

        self.progress_signal.emit('Computing phonology...', 60)
        self.lexicon.run_phon_module(verbose=True)

        self.progress_signal.emit('Computing word neighbors...',  80)
        self.lexicon.run_manifold_module(verbose=True)

        self.progress_signal.emit('All done!',  100)

    def get_lexicon(self):
        return self.lexicon
