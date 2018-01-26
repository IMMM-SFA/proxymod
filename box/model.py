"""
Model interface for box model.

@author:  Chris R. Vernon (chris.vernon@pnnl.gov)
"""

import logger
import time

from config_reader import ReadConfig


class Box:

    def __init__(self, config=None, model_name=None, model_order=0, start_yr=None, end_yr=None, step=None,
                 target_yr=None, in_one=None, in_two=None):

        self.c = ReadConfig(config, model_name, in_one, in_two)

        # first model (0) or second (1)
        self.model_order = model_order

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

        # get target year
        if target_yr is None:
            self.target_yr = target_yr
        else:
            self.target_yr = int(target_yr)

        # for coupling transfer
        self.out_one_dict = {}
        self.out_two_dict = {}

        # set initial values for for sum and max params
        self.param_1 = None
        self.param_2 = None

        self.log = self.c.log

        if target_yr is None and start_yr is None:
            msg = "Either 'target_yr' or 'start_yr, end_yr, and step' need to be defined."
            self.log.error(msg)
            raise(ValueError(msg))

        elif target_yr is None:
            self.run = 'all'
        else:
            self.run = 'step'

        # mirror configuration file in log file
        self.log_config()

        self.log.info('Starting {}'.format(self.c.model_name))

        # run model
        self.model()

        self.log.info('Completed {}'.format(self.c.model_name))

        # remove any handlers that may exist
        logger.kill_log(self.log)

    def model(self):
        """
        Run box model.
        """
        # pause model before running code based on user setting
        time.sleep(self.c.runtime)

        # raise error if user wants a failure
        if self.c.failure == 1:
            msg = "You raised an error on purpose."
            self.log.error(msg)
            raise(RuntimeError(msg))

        # process data
        if self.run == 'all':
            self.execute_all()

        else:
            self.execute_step()

    def read_inputs(self):
        """
        Read in files and set initial parameter value (1:sum and 2:max of input)
        """
        # check for coupling
        if type(self.c.in_file_one) is dict and type(self.c.in_file_two) is dict:

            if self.model_order == 0:

                for k in self.c.in_file_one.keys():
                    self.param_1 = sum(self.c.in_file_one[k])

                for k in self.c.in_file_two.keys():
                    self.param_2 = max(self.c.in_file_two[k])

            if self.model_order == 1:
                self.param_1 = {}
                self.param_2 = {}

                for k in self.c.in_file_one.keys():
                    self.param_1[k] = float(self.c.in_file_one[k]) / 8

                for k in self.c.in_file_two.keys():
                    self.param_2[k] = float(self.c.in_file_two[k]) / 8

        else:

            # if first model in order
            if self.model_order == 0:

                # read in file one
                with open(self.c.in_file_one) as one:

                    # pass header
                    one.next()

                    for line in one:
                        self.param_1 = sum([float(i) for i in line.strip().split(',')])

                # read in file two
                with open(self.c.in_file_two) as two:

                    # pass header
                    two.next()

                    for line in two:
                        self.param_2 = max([float(i) for i in line.strip().split(',')])

            else:

                self.param_1 = {}
                with open(self.c.in_file_one) as one:

                    one.next()

                    for line in one:
                        r = line.strip().split(',')
                        self.param_1[r[0]] = float(r[1]) / 8

                self.param_2 = {}
                with open(self.c.in_file_two) as two:

                    two.next()

                    for line in two:
                        rx = line.strip().split(',')
                        self.param_2[rx[0]] = float(rx[1]) / 4

    def execute_step(self):
        """
        Process specific time step
        :return:
        """
        # read input files
        self.read_inputs()

        if self.model_order == 0:

            # write output file one
            with open(self.c.out_file_one.format(self.c.model_name, self.target_yr), 'w') as out:

                out.write('year,vals\n')

                out.write('{},{}\n'.format(self.target_yr, self.param_1))

            # write output file two
            with open(self.c.out_file_two.format(self.c.model_name, self.target_yr), 'w') as out_two:

                out_two.write('year,vals\n')

                out_two.write('{},{}\n'.format(self.target_yr, self.param_2))

        else:
            # write output file one
            with open(self.c.out_file_one.format(self.c.model_name, self.target_yr), 'w') as out:

                out.write('year,vals\n')

                out.write('{},{}\n'.format(self.target_yr, self.param_1[str(self.target_yr)]))

            # write output file two
            with open(self.c.out_file_two.format(self.c.model_name, self.target_yr), 'w') as out_two:

                out_two.write('year,vals\n')

                out_two.write('{},{}\n'.format(self.target_yr, self.param_2[str(self.target_yr)]))

    def execute_all(self):
        """
        Execute all time steps at once.  Create two output files that 1) sum values in file one
        and 2) get the max of the values in file two.
        """
        # read input files
        self.read_inputs()

        yrs = '{}_{}'.format(self.start_year, self.end_year)

        if self.model_order == 0:

            # write output file one
            with open(self.c.out_file_one.format(self.c.model_name, yrs), 'w') as out:

                out.write('year,vals\n')

                for yr in range(self.start_year, self.end_year + self.step, self.step):

                    out.write('{},{}\n'.format(yr, self.param_1))
                    self.out_one_dict[str(yr)] = self.param_1

                    self.param_1 += self.param_1

            # write output file one
            with open(self.c.out_file_two.format(self.c.model_name, yrs), 'w') as out_two:

                out_two.write('year,vals\n')

                for yr in range(self.start_year, self.end_year + self.step, self.step):

                    out_two.write('{},{}\n'.format(yr, self.param_2))
                    self.out_two_dict[str(yr)] = self.param_2

                    self.param_2 += self.param_2

        else:

            # write output file one
            with open(self.c.out_file_one.format(self.c.model_name, yrs), 'w') as out:

                out.write('year,vals\n')

                for yr in range(self.start_year, self.end_year + self.step, self.step):

                    out.write('{},{}\n'.format(yr, self.param_1[str(yr)]))
                    self.out_one_dict[str(yr)] = self.param_1[str(yr)]

            # write output file one
            with open(self.c.out_file_two.format(self.c.model_name, yrs), 'w') as out_two:

                out_two.write('year,vals\n')

                for yr in range(self.start_year, self.end_year + self.step, self.step):

                    out_two.write('{},{}\n'.format(yr, self.param_2[str(yr)]))
                    self.out_two_dict[str(yr)] = self.param_2[str(yr)]

    def log_config(self):
        """
        Log validated configuration options.
        """
        for i in dir(self.c):

            # create configuration object from string
            x = eval('self.c.{0}'.format(i))

            # ignore magic objects
            if type(x) == str and i[:2] != '__':

                # log result
                self.log.info('CONFIG: [PARAMETER] {0} -- [VALUE] {1}'.format(i, x))


if __name__ == '__main__':

    Box()