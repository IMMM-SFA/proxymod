"""
Reads config.ini and validates parameters.

@author:  Chris R. Vernon (chris.vernon@pnnl.gov)
"""

import argparse
import os

from configobj import ConfigObj
import proxymod.logger as logger


class ReadConfig:

    def __init__(self, config=None, model_name=None, in_one=None, in_two=None):

        # check and validate ini file exists
        if config is None and model_name is None:
            args = self.parse_args()
            ini = self.check_file(args.config_file)

            # fake model name
            self.model_name = args.model_name
        else:
            ini = self.check_file(config)
            self.model_name = model_name

        # instantiate config object
        c = ConfigObj(ini)

        # root outputs directory full path
        root_out = self.make_ifnot(c['OUTPUTS']['out_dir'])
        self.out_dir = self.make_ifnot(os.path.join(root_out, '{}_outputs'.format(self.model_name)))

        # build logger
        self.log = logger.make_log(self.out_dir, self.model_name)

        # get config keys
        try:
            p = c['PROJECT']
        except KeyError:
            raise("Missing [PROJECT] node in {}".format(ini))

        try:
            i = c['INPUTS']
        except KeyError:
            if (in_one is not None) and (in_two is not None):
                i = None
            else:
                raise("Missing [INPUTS] node in {}.  Must define inputs since none are being passed into the model as parameters.".format(ini))

        try:
            o = c['OUTPUTS']
        except KeyError:
            raise("Missing [OUTPUTS] node in {}.".format(ini))

        # desired minimum model runtime in seconds
        self.runtime = self.valid_range(p['runtime'], 0, None, 'int')

        # do you want the model to fail after 5 seconds?  0 if no, 1 if yes
        self.failure = self.valid_range(p['failure'], 0, 1, 'int')

        # input directory full path
        if i is not None:
            self.in_dir = self.check_dir(i['in_dir'])

        if in_one is None:
            # fake input file one name with extension
            self.in_file_one = self.check_file(os.path.join(self.in_dir, i['in_file_one']))
        else:
            self.in_file_one = in_one

        if in_two is None:
            self.in_file_two = self.check_file(os.path.join(self.in_dir, i['in_file_two']))
        else:
            self.in_file_two = in_two

        # fake output file one name with extension
        self.out_file_one = os.path.join(self.out_dir, 'output1_{}_{}.csv')

        # fake output file two name with extension
        self.out_file_two = os.path.join(self.out_dir, 'output2_{}_{}.csv')

    @staticmethod
    def check_dir(pth):
        """
        Check existence of directory

        :param pth:         full path to directory
        :return:            input or exception
        """
        if os.path.isdir(pth):
            return pth
        else:
            raise(IOError("Directory does not exist: {}".format(pth)))

    @staticmethod
    def check_file(pth):
        """
        Check existence of file

        :param pth:         full path to file with file name and extension
        :return:            input or exception
        """
        if os.path.isfile(pth):
            return pth
        else:
            raise(IOError("File does not exist: {}".format(pth)))

    @staticmethod
    def valid_range(v, start, end, typ):
        """
        Validate range of values for a parameter and apply type

        :param v:           value
        :param start:       lower limit for value (>= start)
        :param end:         upper limit for value (<= end)
        :return:            typed value
        """
        try:
            v = eval('{}({})'.format(typ, v))
        except TypeError:
            raise("Cannot convert type '{}' to type '{}' for value '{}'".format(type(v), typ, v))

        if start is None:
            raise(ValueError("Start value cannot be None"))

        if (end is None) and (v < start):
            raise (ValueError("Value '{}' is not within range {} to {}".format(v, start, end)))

        elif (end is None) and (v > start):
            return v

        elif (v < start) or (v > end):
            raise(ValueError("Value '{}' is not within range {} to {}".format(v, start, end)))

        else:
            return v

    @staticmethod
    def make_ifnot(pth):
        """
        Make directory if
        :param pth:
        :return:
        """
        if not os.path.isdir(pth):
            os.makedirs(pth)

        return pth


    @staticmethod
    def parse_args():
        """
        Parser for command line arguments

        :return:        parser object
        """
        parser = argparse.ArgumentParser()

        # config file
        parser.add_argument('-config_file', type=str, required=True,
                            help="Input configuration file full path with file name and extension")

        # model name
        parser.add_argument('-model_name', type=str, required=True, help="Proxy model name")

        return parser.parse_args()


