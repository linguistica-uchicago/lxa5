# -*- encoding: utf8 -*-

import sys
import os
from pprint import pformat

import linguistica as lxa
from linguistica.util import (ENCODING, PARAMETERS)

lxa_version = lxa.__version__


def determine_use_wordlist():
    use_wordlist_response = None
    while use_wordlist_response is None:
        use_wordlist_response = input('\nAre you using a wordlist file? [N/y] ')

    if use_wordlist_response and use_wordlist_response[0].lower() == 'y':
        use_wordlist = True
    else:
        use_wordlist = False

    return use_wordlist


def get_file_abspath():
    file_abspath = None
    while file_abspath is None:
        file_path = input('\nPath to your file: ')

        if sys.platform.startswith('win'):
            file_path = file_path.replace('/', os.sep)
        else:
            file_path = file_path.replace('\\', os.sep)

        file_abspath = os.path.abspath(file_path)

        if not os.path.isfile(file_abspath):
            print('Invalid file path!')
            file_abspath = None

    return file_abspath


def get_output_dir(output_dir_):
    change_dir_response = None
    while change_dir_response is None:
        change_dir_response = input('Change it? [N/y] ')

    if change_dir_response and change_dir_response[0].lower() == 'y':
        new_output_dir = None
        while new_output_dir is None:
            new_output_dir = input('Specify output directory: ')

            if sys.platform.startswith('win'):
                new_output_dir = new_output_dir.replace('/', os.sep)
            else:
                new_output_dir = new_output_dir.replace('\\', os.sep)

            new_output_dir = os.path.abspath(new_output_dir)

            if not os.path.isdir(new_output_dir):
                try:
                    os.mkdir(new_output_dir)
                except FileNotFoundError:
                    print('Cannot make a new directory in a non-existing one!')
                    new_output_dir = None

        output_dir_ = new_output_dir

    return output_dir_


def get_encoding():
    encoding = ENCODING
    print('\nDefault encoding for input and output files:', encoding)

    change_encoding_ans = None
    while change_encoding_ans is None:
        change_encoding_ans = input('Change encoding? [N/y] ')

    if change_encoding_ans and change_encoding_ans[0].lower() == 'y':
        new_encoding = None
        while new_encoding is None:
            new_encoding = input('New encoding: ')
            if not new_encoding:
                new_encoding = None
        encoding = new_encoding

    return encoding


def get_new_parameters():
    change_parameters_ans = None
    while change_parameters_ans is None:
        change_parameters_ans = input('\nChange any parameters? [N/y] ')

    new_parameter_value_pairs = list()

    if change_parameters_ans and change_parameters_ans[0].lower() == 'y':
        print('\nEnter parameter-value pairs\n'
              '(e.g. "min_stem_length=3 max_affix_length=3" without quotes):')

        parameter_value_str = None

        while not parameter_value_str:
            parameter_value_str = input()

            for parameter_value in parameter_value_str.split():
                try:
                    parameter, value = parameter_value.split('=')
                except ValueError:
                    print('Invalid parameter-value pair: ' + parameter_value)
                    parameter_value_str = None
                    break

                if parameter not in PARAMETERS:
                    print('Unknown parameter: ', parameter)
                    parameter_value_str = None
                    break

                try:
                    value_int = int(value)
                except ValueError:
                    print('Cannot parse {} as an integer for parameter {}'
                          .format(value, parameter))
                    parameter_value_str = None
                    break

                new_parameter_value_pairs.append((parameter, value_int))

    return new_parameter_value_pairs


def main():
    print('\n================================================================\n'
          'Welcome to Linguistica {}!\n'
          '================================================================'
          .format(lxa_version))

    # --------------------------------------------------------------------------
    # determine if file is a wordlist or a corpus text

    use_wordlist = determine_use_wordlist()

    print('--------------------------------------------')

    # --------------------------------------------------------------------------
    # get file path

    file_abspath = get_file_abspath()

    print('\nFull file path:\n{}'.format(file_abspath))
    print('--------------------------------------------')

    # --------------------------------------------------------------------------
    # determine output directory

    output_dir = os.path.join(os.path.dirname(file_abspath), 'lxa_outputs')

    print('\nDefault output directory:\n{}'.format(output_dir))

    output_dir = get_output_dir(output_dir)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    print('--------------------------------------------')

    # --------------------------------------------------------------------------
    # change encoding, if instructed

    encoding = get_encoding()

    print('--------------------------------------------')

    # --------------------------------------------------------------------------
    # create the Linguistica object

    if use_wordlist:
        lxa_object = lxa.read_wordlist(file_abspath, encoding=encoding)
    else:
        lxa_object = lxa.read_corpus(file_abspath, encoding=encoding)

    # --------------------------------------------------------------------------
    # change parameters, if instructed

    print('\nParameters:\n{}'.format(pformat(lxa_object.parameters())))

    new_parameter_value_pairs = get_new_parameters()

    if new_parameter_value_pairs:
        lxa_object.change_parameters(**dict(new_parameter_value_pairs))

        print('\nParameters after the changes:\n{}'
              .format(pformat(lxa_object.parameters())))

    print('--------------------------------------------')

    # --------------------------------------------------------------------------
    # run all Linguistica modules on the given file

    print('\nRunning all Linguistica modules on the given file:')

    lxa_object.run_all_modules(verbose=True)

    print('--------------------------------------------')

    # --------------------------------------------------------------------------
    # output results as files

    print('\nGenerating output files...\n')

    lxa_object.output_all_results(directory=output_dir, verbose=True)

    print('\nResults are in ' + output_dir)
