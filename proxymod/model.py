"""
Model interface for proxymod

Copyright (c) 2018, Battelle Memorial Institute

Open source under license BSD 2-Clause - see LICENSE and DISCLAIMER

@author:  Chris R. Vernon (chris.vernon@pnnl.gov)
"""

import math
import time

from proxymod.config_reader import ReadConfig
import proxymod.logger as logger


class Prox:

    def __init__(self,
                 config=None,
                 model_name=None,
                 start_yr=None,
                 end_yr=None,
                 step=None,
                 runtime=None,
                 failure=None,
                 target_yr=None,
                 in_one=None,
                 in_two=None):

        self.c = ReadConfig(config, model_name, in_one, in_two)

        # start year in YYYY format
        if start_yr is None:
            self.start_year = start_yr
        else:
            self.start_year = int(start_yr)

        # end year in YYYY format
        if end_yr is None:
            self.end_year = end_yr
        else:
            self.end_year = int(end_yr)

        # time step in years
        if step is None:
            self.step = step
        else:
            self.step = int(step)

        # how long to run
        if runtime is None:
            self.runtime = runtime
        else:
            self.runtime = int(runtime)

        # how long to run before failure
        if failure is None:
            self.failure = failure
        else:
            self.failure = int(failure)

        # get target year
        if target_yr is None:
            self.target_yr = target_yr
        else:
            self.target_yr = int(target_yr)

        self.yr_range = self.set_yr_range()

        # set initial values for for sum and max params
        if in_one is None:
            self.param_1 = None
        else:
            self.param_1 = in_one

        if in_two is None:
            self.param_2 = None
        else:
            self.param_2 = in_two

        self.log = self.c.log

        if (target_yr is None) and (start_yr is None):
            msg = "Either 'target_yr' or 'start_yr, end_yr, and step' need to be defined."
            self.log.error(msg)
            raise (ValueError(msg))

        elif target_yr is None:
            yrs = '{}_{}'.format(self.start_year, self.end_year)
        else:
            yrs = self.target_yr

        self.out_file_1 = self.c.out_file_one.format(self.c.model_name, yrs)
        self.out_file_2 = self.c.out_file_two.format(self.c.model_name, yrs)

        self.log.info('Starting {}'.format(self.c.model_name))

        # mirror configuration file in log file
        self.log_config()

        self.prepare()

        self.idx = 0
        self.set_yr = 0

    def prepare(self):
        """
        Run proxymod model.
        """
        # pause model before running code based on user setting
        time.sleep(self.c.runtime)

        # raise error if user wants a failure
        if self.c.failure == 1:
            msg = "You raised an error on purpose."
            self.log.error(msg)
            self.close()

            raise (RuntimeError(msg))

        # read and modify input data
        self.read_data()

    def close(self):
        """
        Clean up logger.
        """

        self.log.info('Completed {}'.format(self.c.model_name))

        # remove any handlers that may exist
        logger.kill_log(self.log)

    def set_yr_range(self):
        """
        Set year range to evaluate.
        :return:                list of years
        """

        if (self.start_year is None) and (self.end_year is None):
            return [self.target_yr]

        else:
            return range(self.start_year, self.end_year + self.step, self.step)

    def modify(self):
        """
        Modify dictionary values to be square root of each value.
        :param d:               dictionary {yr: value}
        :return:                dictionary {yr: value}
        """
        yr = str(self.set_yr)
        self.param_1[yr] = math.sqrt(self.param_1[yr])
        self.param_2[yr] = math.sqrt(self.param_2[yr])

    @staticmethod
    def read_csv(f, yr_range):
        """
        Read CSV to dictionary in format { yr: value }
        :param f:               full path with filename and extension of input CSV
        :return:                dictionary
        """
        d = {}
        with open(f, 'rU') as o:

            for idx, line in enumerate(o):

                # pass header
                if idx > 0:

                    row = line.strip().split(',')

                    if int(row[0]) in yr_range:
                        d[row[0]] = float(row[1])

        return d

    def read_data(self):
        """
        Read inputs to dictionary and modify values.
        """
        typ_1 = type(self.c.in_file_one)
        typ_2 = type(self.c.in_file_two)

        # if both inputs are CSV
        if (typ_1 is str) and (typ_2 is str):

            self.param_1 = self.read_csv(self.c.in_file_one, self.yr_range)
            self.param_2 = self.read_csv(self.c.in_file_two, self.yr_range)

        elif (typ_1 is str) and (typ_2 is dict):

            self.param_1 = self.read_csv(self.c.in_file_one, self.yr_range)
            self.param_2 = self.c.in_file_two

        elif (typ_1 is dict) and (typ_2 is str):

            self.param_1 = self.c.in_file_one
            self.param_2 = self.read_csv(self.c.in_file_two, self.yr_range)

        elif (typ_1 is dict) and (typ_2 is dict):

            self.param_1 = self.c.in_file_one
            self.param_2 = self.c.in_file_two

        else:
            msg = "Type for either input one or two must be either 'str' or 'dict'"
            self.log.error(msg)
            raise (ValueError(msg))

    @staticmethod
    def build_output(f, d):
        """
        Write output file.
        """
        with open(f, 'w') as out:
            out.write('year,value\n')

            for k in d.keys():
                out.write('{},{}\n'.format(k, d[k]))

    def advance(self):
        """
        Execute time steps.  Create two output files that 1) sum values in file one
        and 2) get the max of the values in file two.
        """
        if (self.idx == 0) and (self.target_yr is None):
            self.set_yr = self.start_year
            self.idx += 1
        elif (self.idx == 0) and (self.target_yr is not None):
            self.set_yr = self.target_yr
        else:
            self.set_yr += self.step

        self.modify()

        self.build_output(self.out_file_1, self.param_1)
        self.build_output(self.out_file_2, self.param_2)

    def log_config(self):
        """
        Log validated configuration options.
        """
        for i in dir(self.c):

            # create configuration object from string
            x = eval('self.c.{0}'.format(i))

            # ignore magic objects and out file names
            if (type(x) == str) and (i[:2] != '__') and ('out_file_' not in i):
                # log result
                self.log.info('CONFIG: [PARAMETER] {0} -- [VALUE] {1}'.format(i, x))
