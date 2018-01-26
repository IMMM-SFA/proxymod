"""
Build different box model interactions.

@author:  Chris R. Vernon (chris.vernon@pnnl.gov)
"""

from box.model import Box


def file_pass_all(config_1, config_2):
    """
    Transfer the outputs of one model to another through file exchange.  Run both models for
    all time steps before moving to next one.

    :param config_1:        Full path with file name and extension to the config file for model 1
    :param config_2:        Full path with file name and extension to the config file for model 1
    """
    # run first model
    model_1 = Box(config=config_1,
                  model_name='proxy_gcam',
                  model_order=0,
                  start_yr=2005,
                  end_yr=2100,
                  step=5)

    # run second model
    model_2 = Box(config=config_2,
                  model_name='proxy_cerf',
                  model_order=1,
                  start_yr=2005,
                  end_yr=2100,
                  step=5)


def file_pass_step(config_1, config_2):
    """
    Transfer the outputs of one model to another through file exchange.  Run both models for
    all time steps before moving to next one.

    :param config_1:        Full path with file name and extension to the config file for model 1
    :param config_2:        Full path with file name and extension to the config file for model 1
    """
    # run first model
    model_1 = Box(config=config_1,
                  model_name='proxy_gcam',
                  model_order=0,
                  target_yr=2005)

    # run second model
    model_2 = Box(config=config_2,
                  model_name='proxy_cerf',
                  model_order=1,
                  target_yr=2005)


def one_way(config_1, config_2):
    """
    Transfer the outputs of one model to another through file exchange.  Run both models for
    all time steps before moving to next one.

    :param config_1:        Full path with file name and extension to the config file for model 1
    :param config_2:        Full path with file name and extension to the config file for model 1
    """
    # run first model
    model_1 = Box(config=config_1,
                  model_name='proxy_gcam',
                  model_order=0,
                  start_yr=2005,
                  end_yr=2100,
                  step=5)

    # run second model
    model_2 = Box(config=config_2,
                  model_name='proxy_cerf',
                  model_order=1,
                  in_one=model_1.out_one_dict,
                  in_two=model_1.out_two_dict,
                  start_yr=2005,
                  end_yr=2100,
                  step=5)


if __name__ == "__main__":

    config_1 = '/users/ladmin/repos/github/box/example/config_1.ini'
    config_2 = '/users/ladmin/repos/github/box/example/config_2.ini'
    config_2b = '/users/ladmin/repos/github/box/example/config_2b.ini'
    config_2c = '/users/ladmin/repos/github/box/example/config_2c.ini'

    # file pass with all years ran before passing
    # file_pass_all(config_1, config_2)

    # file pass with one year ran at a time
    # file_pass_step(config_1, config_2b)

    # one-way coupling from model_1 to model_2
    one_way(config_1, config_2c)