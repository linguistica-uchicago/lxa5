# -*- encoding: utf8 -*-

import os
import json
from pathlib import Path

from networkx.readwrite import json_graph

from PyQt5.QtCore import (Qt, QUrl)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QAction, QVBoxLayout,
                             QTreeWidget, QFileDialog, QLabel, QTreeWidgetItem,
                             QTableWidget, QTableWidgetItem, QSplitter,
                             QProgressDialog, QMessageBox, QDialog, QGridLayout,
                             QSpinBox, QSizePolicy, QHBoxLayout, QPushButton,
                             QShortcut)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebKitWidgets import QWebView

from linguistica import (read_corpus, read_wordlist)

from linguistica.util import (SEP_SIG, SEP_NGRAM,
                              PARAMETERS_RANGES, PARAMETERS_HINTS,
                              double_sorted)

from linguistica.gui.worker import LinguisticaWorker

from linguistica.gui.util import (MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT,
                                  TREEWIDGET_WIDTH_MIN, TREEWIDGET_WIDTH_MAX,
                                  TREEWIDGET_HEIGHT_MIN,
                                  WORDLIST, WORD_NGRAMS, BIGRAMS, TRIGRAMS,
                                  SIGNATURES, SIGS_TO_STEMS, WORDS_TO_SIGS,
                                  TRIES, WORDS_AS_TRIES,
                                  SUCCESSORS, PREDECESSORS,
                                  PHONOLOGY, PHONES, BIPHONES, TRIPHONES,
                                  MANIFOLDS, WORD_NEIGHBORS, VISUALIZED_GRAPH,
                                  SHOW_MANIFOLD_HTML,
                                  CONFIG_DIR, CONFIG_LAST_FILE,
                                  process_all_gui_events)


# noinspection PyAttributeOutsideInit
class MainWindow(QMainWindow):
    def __init__(self, screen_height, screen_width, version, parent=None):
        super(MainWindow, self).__init__(parent)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.version = version

        # basic main window settings
        self.resize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.setWindowTitle('Linguistica {}'.format(self.version))

        # lexicon and lexicon tree
        self.lexicon = None
        self.lexicon_tree = None
        self.initialize_lexicon_tree()

        # set up major display, parameter window, then load main window
        self.majorDisplay = QWidget()
        self.parameterWindow = QWidget()
        self.load_main_window()

        # 'File' menu and actions
        select_corpus_action = self.create_action(text='&Select corpus...',
                                                  slot=self.corpus_dir_dialog,
                                                  tip='Select a corpus file',
                                                  shortcut='Ctrl+N')
        select_wordlist_action = self.create_action(text='&Select wordlist...',
                                                    slot=self.wordlist_dir_dialog,
                                                    tip='Select a wordlist file',
                                                    shortcut='Ctrl+W')
        run_file_action = self.create_action(text='&Run...',
                                             slot=self.run_file,
                                             tip='Run the input file',
                                             shortcut='Ctrl+D')
        parameters_action = self.create_action(text='&Parameters...',
                                               slot=self.parameters_dialog,
                                               tip='Change parameters',
                                               shortcut='Ctrl+P')

        file_menu = self.menuBar().addMenu('&File')
        file_menu.addAction(select_corpus_action)
        file_menu.addAction(select_wordlist_action)
        file_menu.addAction(run_file_action)
        file_menu.addAction(parameters_action)

        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.showMessage('No input file loaded. To select one: File --> '
                                'Select corpus... or Select wordlist...')

    def initialize_lexicon_tree(self):
        self.lexicon_tree = QTreeWidget()
        self.lexicon_tree.setEnabled(True)
        self.lexicon_tree.setMinimumWidth(TREEWIDGET_WIDTH_MIN)
        self.lexicon_tree.setMaximumWidth(TREEWIDGET_WIDTH_MAX)
        self.lexicon_tree.setMinimumHeight(TREEWIDGET_HEIGHT_MIN)
        self.lexicon_tree.setHeaderLabel('')
        self.lexicon_tree.setItemsExpandable(True)
        # noinspection PyUnresolvedReferences
        self.lexicon_tree.itemClicked.connect(self.tree_item_clicked)

    def create_action(self, text=None, slot=None, tip=None, shortcut=None):
        """
        This create actions for the File menu, things like
        Read Corpus, Rerun Corpus etc
        """
        action = QAction(text, self)
        if shortcut:
            action.setShortcut(shortcut)
        if tip:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot:
            # noinspection PyUnresolvedReferences
            action.triggered.connect(slot)
        if shortcut:
            # noinspection PyUnresolvedReferences
            QShortcut(QKeySequence(shortcut), self).activated.connect(slot)
        return action

    def _get_filename_from_dialog(self, ftype='input'):
        self.determine_last_file()
        if self.last_file_path and self.last_file_type == ftype:
            open_dir = self.last_file_path
        else:
            open_dir = os.getcwd()
        # noinspection PyTypeChecker,PyCallByClass
        fname = QFileDialog.getOpenFileName(self,
                                            'Select the {} file'.format(ftype),
                                            open_dir)
        process_all_gui_events()

        # HACK: fname is supposed to be a string (at least according to the
        # PyQt5 documentation), but for some reason fname is a tuple.
        # So we need this hack to make sure that fname is a string of a filename
        # -- Jackson Lee, 2015/06/22

        # update: it's turned out that this behavior is due to compatibility
        # between PyQt and PySide. The "tuple" behavior is in line with the
        # newer API2 for PyQt. (PyQt on python 3 uses API2 by default.)
        # more here: http://srinikom.github.io/pyside-bz-archive/343.html
        # so perhaps we keep our current hack for now?
        # -- Jackson Lee, 2015/08/24

        if fname and any(fname) and (type(fname) is tuple):
            return fname[0]
        else:
            # if this hack isn't needed somehow...
            return fname

    def corpus_dir_dialog(self):
        """
        Pop up the "open a file" dialog and ask for which corpus text file
        to use
        """
        self.corpus_filename = self._get_filename_from_dialog(ftype='corpus')

        process_all_gui_events()

        if type(self.corpus_filename) != str:
            return

        # note that self.corpus_filename is an absolute full path
        self.corpus_name = os.path.basename(self.corpus_filename)
        self.corpus_stem_name = Path(self.corpus_name).stem

        self.lexicon = read_corpus(self.corpus_filename)
        self.initialize_lexicon_tree()
        self.load_main_window(major_display=QWidget(),
                              parameter_window=QWidget())
        process_all_gui_events()

        self.status.clearMessage()
        self.status.showMessage(
            'Corpus selected: {}'.format(self.corpus_filename))

    def wordlist_dir_dialog(self):
        """
        Pop up the "open a file" dialog and ask for which corpus text file
        to use
        """
        self.corpus_filename = self._get_filename_from_dialog(ftype='wordlist')

        process_all_gui_events()

        if type(self.corpus_filename) != str:
            return

        # note that self.corpus_filename is an absolute full path
        self.corpus_name = os.path.basename(self.corpus_filename)
        self.corpus_stem_name = Path(self.corpus_name).stem

        self.lexicon = read_wordlist(self.corpus_filename)
        self.initialize_lexicon_tree()
        self.load_main_window(major_display=QWidget(),
                              parameter_window=QWidget())
        process_all_gui_events()

        self.status.clearMessage()
        self.status.showMessage(
            'Wordlist selected: {}'.format(self.corpus_filename))

    def parameters_dialog(self):
        if self.lexicon is None:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Warning)
            warning.setText('Parameters can only be accessed when an input '
                            'file is specified.')
            warning.setWindowTitle('No input file selected')
            warning.setStandardButtons(QMessageBox.Ok)
            warning.exec_()
            return

        process_all_gui_events()

        parameters = self.lexicon.parameters()
        dialog = QDialog()
        layout = QVBoxLayout()
        layout.addWidget(
            QLabel('Filename: {}'.format(Path(self.corpus_filename).name)))
        file_type = 'Wordlist' if self.lexicon.file_is_wordlist else 'Corpus'
        layout.addWidget(QLabel('Type: {}'.format(file_type)))

        grid = QGridLayout()
        self.parameter_spinboxes = [QSpinBox() for _ in range(len(parameters))]

        for i, parameter_name in enumerate(sorted(parameters.keys())):
            self.parameter_spinboxes[i].setObjectName(parameter_name)
            self.parameter_spinboxes[i].setRange(
                *PARAMETERS_RANGES[parameter_name])
            self.parameter_spinboxes[i].setValue(parameters[parameter_name])
            self.parameter_spinboxes[i].setSingleStep(1)
            # noinspection PyUnresolvedReferences
            self.parameter_spinboxes[i].valueChanged.connect(
                self.update_parameter)

            grid.addWidget(QLabel(parameter_name), i, 0)
            grid.addWidget(self.parameter_spinboxes[i], i, 1)
            grid.addWidget(QLabel(PARAMETERS_HINTS[parameter_name]), i, 2)

        layout.addLayout(grid)

        reset_button = QPushButton()
        reset_button.setText('&Reset')
        # noinspection PyUnresolvedReferences
        reset_button.clicked.connect(self.reset_parameters)

        spacer = QWidget()  # just for padding in tool_bar
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        tool_bar = QHBoxLayout()
        tool_bar.addWidget(spacer)  # so that the buttons are right-aligned
        tool_bar.addWidget(reset_button)

        layout.addLayout(tool_bar)

        dialog.setLayout(layout)
        dialog.setWindowTitle('Parameters')
        dialog.exec_()

    def reset_parameters(self):
        self.lexicon.use_default_parameters()

        for i, (_, value) in \
                enumerate(sorted(self.lexicon.parameters().items())):
            self.parameter_spinboxes[i].setValue(value)

    def update_parameter(self):
        for i in range(len(self.lexicon.parameters())):
            parameter_name, new_value = \
                self.parameter_spinboxes[i].objectName(), \
                self.parameter_spinboxes[i].value()
            self.lexicon.change_parameters(**{parameter_name: new_value})

    def update_progress(self, progress_text, target_percentage):
        """
        Update the progress dialog. This function is triggered by the
        "progress_signal" emitted from the linguistica component worker thread.
        """
        self.progressDialog.setLabelText(progress_text)
        self.progressDialog.setValue(target_percentage)
        process_all_gui_events()

    # noinspection PyProtectedMember
    def run_file(self):
        if self.lexicon is None:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Warning)
            warning.setText('No input file is selected.')
            warning.setWindowTitle('Error')
            warning.setStandardButtons(QMessageBox.Ok)
            warning.exec_()
            return

        self.status.clearMessage()
        self.status.showMessage('Running the file {} now...'
                                .format(self.corpus_name))

        print('\nInput file in use:\n{}\n'.format(self.corpus_filename),
              flush=True)

        # set up the Linguistica components worker
        # The worker is a QThread. We spawn this thread, and the linguistica
        # components run on this new thread but not the main thread for the GUI.
        # This makes the GUI still responsive
        # while the long and heavy running process of
        # the Linguistica components is ongoing.

        self.lxa_worker = LinguisticaWorker(self.lexicon)
        self.lxa_worker.progress_signal.connect(self.update_progress)

        # set up progress dialog

        process_all_gui_events()
        self.progressDialog = QProgressDialog()
        self.progressDialog.setRange(0, 100)  # it's like from 0% to 100%
        self.progressDialog.setLabelText('Initializing...')
        self.progressDialog.setValue(0)  # initialize as 0 (= 0%)
        self.progressDialog.setWindowTitle(
            'Processing {}'.format(self.corpus_name))
        self.progressDialog.setCancelButton(None)
        self.progressDialog.resize(400, 100)
        process_all_gui_events()

        self.progressDialog.show()

        # We disable the "cancel" button
        # Setting up a "cancel" mechanism may not be a good idea,
        # since it would probably involve killing the linguistica component
        # worker at *any* point of its processing.
        # This may have undesirable effects (e.g., freezing the GUI) -- BAD!

        # make sure all GUI stuff up to this point has been processed before
        # doing the real work of running the Lxa components
        process_all_gui_events()

        # Now the real work begins here!
        self.lxa_worker.start()

        process_all_gui_events()

        self.lexicon = self.lxa_worker.get_lexicon()

        print('\nAll Linguistica components run for the file', flush=True)
        self.status.clearMessage()
        self.status.showMessage('{} processed'.format(self.corpus_name))

        self.load_main_window(major_display=QWidget(),
                              parameter_window=QWidget())
        self.populate_lexicon_tree()
        self.update_last_file()
        process_all_gui_events()

        # display corpus name (in the tree header label)
        file_type = 'wordlist' if self.lexicon.file_is_wordlist else 'corpus'
        header_label = 'File: {}\nFile type: {}\n\n# word types: {:,}\n'.format(
            self.corpus_name, file_type, self.lexicon.number_of_word_types())
        if file_type == 'corpus':
            header_label += '# word tokens: {:,}\n'.format(
                self.lexicon.number_of_word_tokens())
        self.lexicon_tree.setHeaderLabel(header_label)

    @staticmethod
    def ensure_config_dir_exists():
        if not os.path.isdir(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)

    def determine_last_file(self):
        self.last_file_path = None
        self.last_file_type = None
        self.last_file_encoding = None

        if not os.path.isfile(CONFIG_LAST_FILE):
            return

        with open(CONFIG_LAST_FILE, encoding='utf8') as f:
            config_last_file = json.load(f)

        self.last_file_path = config_last_file['last_file_path']
        self.last_file_type = config_last_file['last_file_type']
        self.last_file_encoding = config_last_file['last_file_encoding']

    def update_last_file(self):
        self.ensure_config_dir_exists()
        with open(CONFIG_LAST_FILE, 'w', encoding='utf8') as f:
            if self.lexicon.file_is_wordlist:
                file_type = 'wordlist'
            else:
                file_type = 'corpus'

            config = {'last_file_path': self.lexicon.file_abspath,
                      'last_file_type': file_type,
                      'last_file_encoding': self.lexicon.encoding,
                      }

            json.dump(config, f)

    def populate_lexicon_tree(self):
        self.lexicon_tree.clear()
        process_all_gui_events()

        # wordlist
        ancestor = QTreeWidgetItem(self.lexicon_tree, [WORDLIST])
        self.lexicon_tree.expandItem(ancestor)

        # word ngrams
        ancestor = QTreeWidgetItem(self.lexicon_tree, [WORD_NGRAMS])
        self.lexicon_tree.expandItem(ancestor)
        for item_str in [BIGRAMS, TRIGRAMS]:
            item = QTreeWidgetItem(ancestor, [item_str])
            self.lexicon_tree.expandItem(item)

        # signatures
        ancestor = QTreeWidgetItem(self.lexicon_tree, [SIGNATURES])
        self.lexicon_tree.expandItem(ancestor)
        for item in [SIGS_TO_STEMS, WORDS_TO_SIGS]:
            self.lexicon_tree.expandItem(QTreeWidgetItem(ancestor, [item]))

        # tries
        ancestor = QTreeWidgetItem(self.lexicon_tree, [TRIES])
        self.lexicon_tree.expandItem(ancestor)
        for item in [WORDS_AS_TRIES, SUCCESSORS, PREDECESSORS]:
            self.lexicon_tree.expandItem(QTreeWidgetItem(ancestor, [item]))

        # phonology
        ancestor = QTreeWidgetItem(self.lexicon_tree, [PHONOLOGY])
        self.lexicon_tree.expandItem(ancestor)
        for item in [PHONES, BIPHONES, TRIPHONES]:
            self.lexicon_tree.expandItem(QTreeWidgetItem(ancestor, [item]))

        # manifolds
        ancestor = QTreeWidgetItem(self.lexicon_tree, [MANIFOLDS])
        self.lexicon_tree.expandItem(ancestor)
        for item in [WORD_NEIGHBORS, VISUALIZED_GRAPH]:
            self.lexicon_tree.expandItem(QTreeWidgetItem(ancestor, [item]))

        self.status.clearMessage()
        self.status.showMessage('Navigation tree populated')
        print('Lexicon navigation tree populated', flush=True)

    def load_main_window(self, major_display=None, parameter_window=None):
        """
        Refresh the main window for the updated display content
        (most probably after a click or some event is triggered)
        """
        # get sizes of the three major PyQt objects
        major_display_size = self.majorDisplay.size()
        parameter_window_size = self.parameterWindow.size()
        lexicon_tree_size = self.lexicon_tree.size()

        if major_display:
            self.majorDisplay = major_display
        if parameter_window:
            self.parameterWindow = parameter_window

        # apply sizes to the major three objects
        self.majorDisplay.resize(major_display_size)
        self.parameterWindow.resize(parameter_window_size)
        self.lexicon_tree.resize(lexicon_tree_size)

        # set up:
        # 1) main splitter (b/w lexicon-tree+parameter window and major display)
        # 2) minor splitter (b/w lexicon-tree and parameter window)
        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainSplitter.setHandleWidth(10)
        self.mainSplitter.setChildrenCollapsible(False)

        self.minorSplitter = QSplitter(Qt.Vertical)
        self.minorSplitter.setHandleWidth(10)
        self.minorSplitter.setChildrenCollapsible(False)

        self.minorSplitter.addWidget(self.lexicon_tree)
        self.minorSplitter.addWidget(self.parameterWindow)

        self.mainSplitter.addWidget(self.minorSplitter)
        self.mainSplitter.addWidget(self.majorDisplay)

        self.setCentralWidget(self.mainSplitter)

    def sig_to_stems_clicked(self, row):
        signature = self.sig_to_stems_major_table.item(row, 0).text()
        print(signature)
        signature = tuple(signature.split(SEP_SIG))

        stems = sorted(self.lexicon.signatures_to_stems()[signature])
        number_of_stems_per_column = 5

        # create a master list of sublists, where each sublist contains k stems
        # k = number_of_stems_per_column
        stem_rows = list()
        stem_row = list()

        for i, stem in enumerate(stems, 1):
            stem_row.append(stem)
            if not i % number_of_stems_per_column:
                stem_rows.append(stem_row)
                stem_row = list()
        if stem_row:
            stem_rows.append(stem_row)

        # set up the minor table as table widget
        sig_to_stems_minor_table = QTableWidget()
        sig_to_stems_minor_table.horizontalHeader().hide()
        sig_to_stems_minor_table.verticalHeader().hide()
        sig_to_stems_minor_table.clear()
        sig_to_stems_minor_table.setRowCount(len(stem_rows))
        sig_to_stems_minor_table.setColumnCount(number_of_stems_per_column)

        # fill in the minor table
        for row, stem_row in enumerate(stem_rows):
            for col, stem in enumerate(stem_row):
                item = QTableWidgetItem(stem)
                sig_to_stems_minor_table.setItem(row, col, item)

        sig_to_stems_minor_table.resizeColumnsToContents()

        minor_table_title = QLabel('{} (number of stems: {})'
                                   .format(SEP_SIG.join(signature), len(stems)))

        minor_table_widget_with_title = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(minor_table_title)
        layout.addWidget(sig_to_stems_minor_table)
        minor_table_widget_with_title.setLayout(layout)

        new_display = QSplitter(Qt.Horizontal)
        new_display.setHandleWidth(10)
        new_display.setChildrenCollapsible(False)

        new_display.addWidget(self.sig_to_stems_major_table)
        new_display.addWidget(minor_table_widget_with_title)
        new_display_width = self.majorDisplay.width() / 2
        new_display.setSizes(
            [new_display_width * 0.4, new_display_width * 0.6])

        self.load_main_window(major_display=new_display)
        self.status.clearMessage()
        self.status.showMessage('{} selected'.format(signature))

    def unavailable_for_wordlist(self):
        self.load_main_window(major_display=QWidget(),
                              parameter_window=QWidget())
        self.status.showMessage('')
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Warning)
        warning.setText('Unavailable for a wordlist')
        warning.setWindowTitle('Error')
        warning.setStandardButtons(QMessageBox.Ok)
        warning.exec_()

    def tree_item_clicked(self, item):
        """
        Trigger the appropriate action when something in the lexicon tree
        is clicked, and update the major display plus parameter window
        """
        item_str = item.text(0)

        if item_str in {WORD_NGRAMS, SIGNATURES, TRIES, PHONOLOGY, MANIFOLDS}:
            return

        print('loading', item_str, flush=True)

        self.status.clearMessage()
        self.status.showMessage('Loading {}...'.format(item_str))

        new_display = None
        new_parameter_window = None

        if item_str == WORDLIST:
            new_display = self.create_major_display_table(
                self.lexicon.word_phonology_dict().items(),
                key=lambda x: x[1].count, reverse=True,
                headers=['Word', 'Count', 'Frequency', 'Phones',
                         'Unigram plog', 'Avg unigram plog',
                         'Bigram plog', 'Avg bigram plog'],
                row_cell_functions=[
                    lambda x: x[0], lambda x: x[1].count,
                    lambda x: x[1].frequency,
                    lambda x: ' '.join(x[1].phones),
                    lambda x: x[1].unigram_plog,
                    lambda x: x[1].avg_unigram_plog,
                    lambda x: x[1].bigram_plog,
                    lambda x: x[1].avg_bigram_plog],
                cutoff=0)

        elif item_str == BIGRAMS:
            if self.lexicon.file_is_wordlist:
                self.unavailable_for_wordlist()
                return
            new_display = self.create_major_display_table(
                self.lexicon.word_bigram_counter().items(),
                key=lambda x: x[1], reverse=True,
                headers=['Bigram', 'Count'],
                row_cell_functions=[lambda x: SEP_NGRAM.join(x[0]),
                                    lambda x: x[1]],
                cutoff=2000)

        elif item_str == TRIGRAMS:
            if self.lexicon.file_is_wordlist:
                self.unavailable_for_wordlist()
                return
            new_display = self.create_major_display_table(
                self.lexicon.word_trigram_counter().items(),
                key=lambda x: x[1], reverse=True,
                headers=['Trigram', 'Count'],
                row_cell_functions=[lambda x: SEP_NGRAM.join(x[0]),
                                    lambda x: x[1]],
                cutoff=2000)

        elif item_str == SIGS_TO_STEMS:
            self.sig_to_stems_major_table = self.create_major_display_table(
                self.lexicon.signatures_to_stems().items(),
                key=lambda x: len(x[1]), reverse=True,
                headers=['Signature', 'Stem count', 'A few stems'],
                row_cell_functions=[lambda x: SEP_SIG.join(x[0]),
                                    lambda x: len(x[1]),
                                    lambda x: ', '.join(sorted(x[1])[:2]) +
                                              ', ...'],
                cutoff=0)
            # noinspection PyUnresolvedReferences
            self.sig_to_stems_major_table.cellClicked.connect(
                self.sig_to_stems_clicked)
            new_display = self.sig_to_stems_major_table

        elif item_str == WORDS_TO_SIGS:
            new_display = self.create_major_display_table(
                self.lexicon.words_to_signatures().items(),
                key=lambda x: len(x[1]), reverse=True,
                headers=['Word', 'Signature count', 'Signatures'],
                row_cell_functions=[lambda x: x[0],
                                    lambda x: len(x[1]),
                                    lambda x: ', '.join([SEP_SIG.join(sig)
                                                         for sig in
                                                         sorted(x[1])])],
                cutoff=2000)

        elif item_str == WORDS_AS_TRIES:
            words = self.lexicon.broken_words_left_to_right().keys()
            words_to_tries = dict()
            # key: word (str)
            # value: tuple of (str, str)
            # for left-to-right and right-to-left tries

            for word in words:
                l_r = ' '.join(self.lexicon.broken_words_left_to_right()[word])
                r_l = ' '.join(self.lexicon.broken_words_right_to_left()[word])
                words_to_tries[word] = (l_r, r_l)  # left-right, right-left

            new_display = self.create_major_display_table(
                words_to_tries.items(),
                key=lambda x: x[0], reverse=False,
                headers=['Word', 'Reversed word',
                         'Left-to-right trie', 'Right-to-left trie'],
                row_cell_functions=[lambda x: x[0], lambda x: x[0][::-1],
                                    lambda x: x[1][0], lambda x: x[1][1]],
                cutoff=0, set_text_alignment=[(3, Qt.AlignRight)])

        elif item_str == SUCCESSORS:
            new_display = self.create_major_display_table(
                self.lexicon.successors().items(),
                key=lambda x: len(x[1]), reverse=True,
                headers=['String', 'Successor count', 'Successors'],
                row_cell_functions=[lambda x: x[0],
                                    lambda x: len(x[1]),
                                    lambda x: ', '.join(sorted(x[1]))],
                cutoff=0)

        elif item_str == PREDECESSORS:
            new_display = self.create_major_display_table(
                self.lexicon.predecessors().items(),
                key=lambda x: len(x[1]), reverse=True,
                headers=['String', 'Predecessor count', 'Predecessors'],
                row_cell_functions=[lambda x: x[0],
                                    lambda x: len(x[1]),
                                    lambda x: ', '.join(sorted(x[1]))],
                cutoff=0)

        elif item_str == PHONES:
            new_display = self.create_major_display_table(
                self.lexicon.phone_dict().items(),
                key=lambda x: x[1].count, reverse=True,
                headers=['Phone', 'Count', 'Frequency', 'Plog'],
                row_cell_functions=[lambda x: x[0],
                                    lambda x: x[1].count,
                                    lambda x: x[1].frequency,
                                    lambda x: x[1].plog],
                cutoff=0)

        elif item_str == BIPHONES:
            new_display = self.create_major_display_table(
                self.lexicon.biphone_dict().items(),
                key=lambda x: x[1].count, reverse=True,
                headers=['Biphone', 'Count', 'Frequency',
                         'Mutual information (MI)', 'Weighted MI'],
                row_cell_functions=[lambda x: SEP_NGRAM.join(x[0]),
                                    lambda x: x[1].count,
                                    lambda x: x[1].frequency,
                                    lambda x: x[1].MI,
                                    lambda x: x[1].weighted_MI],
                cutoff=0)

        elif item_str == TRIPHONES:
            new_display = self.create_major_display_table(
                self.lexicon.phone_trigram_counter().items(),
                key=lambda x: x[1], reverse=True,
                headers=['Triphone', 'Count'],
                row_cell_functions=[lambda x: SEP_NGRAM.join(x[0]),
                                    lambda x: x[1]],
                cutoff=0)

        elif item_str == WORD_NEIGHBORS:
            if self.lexicon.file_is_wordlist:
                self.unavailable_for_wordlist()
                return
            word_to_freq = self.lexicon.word_unigram_counter()
            new_display = self.create_major_display_table(
                self.lexicon.words_to_neighbors().items(),
                key=lambda x: word_to_freq[x[0]], reverse=True,
                headers=['Word', 'Word count', 'Neighbors'],
                row_cell_functions=[lambda x: x[0],
                                    lambda x: word_to_freq[x[0]],
                                    lambda x: ' '.join(x[1])],
                cutoff=0)

        elif item_str == VISUALIZED_GRAPH:
            if self.lexicon.file_is_wordlist:
                self.unavailable_for_wordlist()
                return

            graph_width = self.screen_width - TREEWIDGET_WIDTH_MAX - 50
            graph_height = self.screen_height - 70
            html_name = 'show_manifold.html'

            manifold_name = '{}_manifold.json'.format(self.corpus_stem_name)
            manifold_filename = os.path.join(CONFIG_DIR, manifold_name)
            print('manifold_filename', manifold_filename)

            manifold_json_data = json_graph.node_link_data(
                self.lexicon.neighbor_graph())
            json.dump(manifold_json_data, open(manifold_filename, 'w'))

            viz_html = os.path.join(CONFIG_DIR, html_name)
            print('viz_html', viz_html)

            # write the show_manifold html file
            with open(viz_html, 'w') as f:
                print(SHOW_MANIFOLD_HTML.format(os.path.dirname(__file__),
                                                graph_width, graph_height,
                                                manifold_filename), file=f)

            url = Path(viz_html).as_uri()
            print('url:', url)

            new_display = QWebView()
            new_display.setUrl(QUrl(url))

        self.load_main_window(major_display=new_display,
                              parameter_window=new_parameter_window)

        self.status.clearMessage()
        self.status.showMessage('{} selected'.format(item_str))

    @staticmethod
    def create_major_display_table(input_iterable,
                                   key=lambda x: x, reverse=False,
                                   headers=None, row_cell_functions=None,
                                   cutoff=0,
                                   set_text_alignment=None):
        """
        This is a general function for creating a tabular display for the
        major display.
        """

        if not input_iterable:
            print('Warning: input is empty', flush=True)
            return

        if not hasattr(input_iterable, '__iter__'):
            print('Warning: input is not an iterable', flush=True)
            return

        number_of_headers = len(headers)
        number_of_columns = len(row_cell_functions)

        if number_of_headers != number_of_columns:
            print('headers and cell functions don\'t match', flush=True)
            return

        len_input = len(input_iterable)

        table_widget = QTableWidget()
        table_widget.clear()
        table_widget.setSortingEnabled(False)

        # set up row count
        if cutoff and cutoff < len_input:
            actual_cutoff = cutoff
        else:
            actual_cutoff = len_input

        table_widget.setRowCount(actual_cutoff)

        # set up column count and table headers
        table_widget.setColumnCount(number_of_headers)
        table_widget.setHorizontalHeaderLabels(headers)

        # fill in the table
        for row, x in enumerate(double_sorted(input_iterable, key=key,
                                              reverse=reverse)):
            for col, fn in enumerate(row_cell_functions):
                cell = fn(x)

                if isinstance(cell, (int, float)):
                    # cell is numeric
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, cell)
                else:
                    # cell is not numeric
                    item = QTableWidgetItem(cell)

                if set_text_alignment:
                    for align_col, alignment in set_text_alignment:
                        if col == align_col:
                            item.setTextAlignment(alignment)

                table_widget.setItem(row, col, item)

            if not row < actual_cutoff:
                break

        table_widget.setSortingEnabled(True)
        table_widget.resizeColumnsToContents()

        return table_widget
