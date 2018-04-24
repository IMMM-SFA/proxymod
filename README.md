# proxymod

## *A lightweight Python package to simulate model interactions*

## Contact
Chris R. Vernon (chris.vernon@pnnl.gov)

## License
Copyright (c) 2018, Battelle Memorial Institute;
Open source under license BSD 2-Clause - see LICENSE and DISCLAIMER

## Description

**proxymod** enables modelers to explore multiple types of model interactations without bearing the large overhead of getting up-to-speed on learning to run multiple complex models. This package also expedites the testing of various interactions by eliminating the runtime associated with complex models by using proxy models to emulate their characteristics but run for a user-defined amount of time.

**proxymod** instances can be configured with the following to mirror what you may encounter in a real model:
- a configuration file,
- two input CSV files,
- two output CSV files,
- the ability to introduce an error during runtime,
- a defined runtime,
- generated log file during runtime,
- a start year, end year, and year interval for running timesteps,
- a target year if you only wish to run one timestep,
- a model name for each instance,
- and the ability to inherit and return Python objects.

These options give the user freedom to quickly test multiple types of model interactions for as many model instances as they wish.

The following are some potential use-cases of **proxymod**:
- testing messaging services
- setting up a modeling framework for multi-model interaction
- testing HPC environments with multiple model setups

## Terminology

There are many different definitions for types of model coupling. **proxymod** adopts the Kraucunas (2018) nomenclature where each coupling type fits into the following two categories:  *Coupling* where two or more model components exchange information and *Forcing or boundary conditions* which are defined as the process where outputs from one model are used to drive another. These are described as the following:

| Type | Term | Definition |
| --- | ---| --- |
| Coupling | Full coupling | All resolved variables in both models are fully reconciled or integrated |
| Coupling | Tight coupling | Models and/or components exchange information at every time step |
| Coupling | Hard coupling | There is a high degree of sofware integration (e.g., flux coupler) |
| Forcing | Partial coupling | Some, but not all, variables are reconciled or integrated |
| Forcing | Loose coupling | Models and/or components exchange information less frequently |
| Forcing | Soft coupling | Low, or no, software integration (e.g., sneaker-net)

## Setup

1. Clone **proxymod** by running the following command in your terminal:  `git clone https://github.com/IMMM-SFA/proxymod`
2. Run `python setup.py install` in the directory where **proxymod** was installed.  Note:  if you have multiple versions of Python installed, make sure you know which version of you are calling when your run `python` from your terminal.
3. Setup your configuration.ini files and prepare an arrangement of **proxymod** instances that suits your needs
4. Run it!

## The proxymod configuration file

The following is an example configuration.ini used by a **proxymod** model:
```
# example config file for the proxymod model
[PROJECT]

# desired minimum model runtime in seconds
runtime = 10

# do you want the model to fail after 5 seconds?  0 if no, 1 if yes
failure = 0

[INPUTS]
# input directory full path
in_dir = /example/inputs

# fake input file one name with extension
in_file_one = in_file_one.csv

# fake input file two name with extension
in_file_two = in_file_two.csv

[OUTPUTS]
# output directory full path
out_dir = /example/outputs
```
There may not be a need to include all of the content in this configuration file.  For instance, if you were inheriting the output files from one model run using a previous model's outputs (see "Loose coupling - one-way - run all timesteps" section below) you could remove the `[INPUTS]` section of the config file.  The following details optional versus required sections of the configuration file:

| Parameter | Type | Description |
| --- | --- | --- |
| `[PROJECT]` | Required | Node for Project level settings |
| `runtime` | Required | Nested in `[PROJECT]` node, integer of desired minimum model runtime in seconds |
| `failure` | Required | Nested in `[PROJECT]` node, integer where 1 will make the model fail after 5 seconds and 0 will not fail |
| `[INPUTS]` | Optional | Node for Inputs level settings |
| `in_dir` | Optional | Nested in `[INPUTS]` node, full path to inputs directory |
| `in_file_one` | Optional | Nested in `[INPUTS]` node, full path to fake input file number one |
| `in_file_two` | Optional | Nested in `[INPUTS]` node, full path to fake input file number two |
| `[OUTPUTS]` | Required | Node for Output level settings |
| `out_dir` | Required | Nested in `[OUTPUTS]` node, full path to outputs directory |

## Examples
Run these interactively using the Jupyter Notebook version of this section: [proxymod Jupyter Notebook Examples](https://github.com/IMMM-SFA/proxymod/blob/master/example/proxymod_tutorial.ipynb)

### Loose coupling - one-way - run all timesteps

This is an example of creating a three-model file exchange loose coupling. Each model runs until it has completed and the resulting output files (two for each model) are passed to the next model in line. Each model will create its own output directory and log file.


```python
from proxymod.model import Prox


def loose_coupling(config_1, config_2, config_3):
    """
    This function creates three instances of proxymod models. A configuration.ini
    file has been prepared for each.  This test utilizes the built in CSV files as
    data and transfers them to the next model in the configuration.
    """

    # instantiate first model
    model_1 = Prox(config=config_1,
                   model_name='model_1',
                   start_yr=2010,
                   end_yr=2100,
                   step=5)
    # run model_1
    model_1.advance()

    # cleanup log objects
    model_1.close()

    # instantiate second model
    model_2 = Prox( config=config_2,
                    model_name='model_2',
                    start_yr=2010,
                    end_yr=2100,
                    step=5,
                    in_one=model_1.out_file_1,
                    in_two=model_1.out_file_2)

    model_2.advance()
    model_2.close()

    # instantiate third model
    model_3 = Prox( config=config_3,
                    model_name='model_3',
                    start_yr=2010,
                    end_yr=2100,
                    step=5,
                    in_one=model_2.out_file_1,
                    in_two=model_2.out_file_2)

    model_3.advance()
    model_3.close()


# create the path references to your config files
config_1 = '/Users/d3y010/repos/github/proxymod/example/config_1.ini'
config_2 = '/Users/d3y010/repos/github/proxymod/example/config_2.ini'
config_3 = '/Users/d3y010/repos/github/proxymod/example/config_3.ini'

# run it
loose_coupling(config_1, config_2, config_3)
```

### Tight coupling - one-way - run one timestep at a time

This is an example of creating a three-model file exchange tight coupling. Each model runs until a single timestep and the resulting output files (two for each model) are passed to the next model in line. Each model will create its own output directory and log file.


```python
from proxymod.model import Prox


def tight_coupling(config_1, config_2, config_3, start_yr, end_yr, step):
    """
    This function creates three instances of proxymod models. A configuration.ini
    file has been prepared for each.  This test utilizes the built in CSV files as
    data and transfers them to the next model in the configuration per timestep.
    """

    for yr in range(start_yr, end_yr + step, step):

        # instantiate first model
        model_1 = Prox(config=config_1,
                       model_name='model_1',
                       target_yr=yr)
        # run model_1
        model_1.advance()
        model_1.close()

        # instantiate second model
        model_2 = Prox( config=config_2,
                        model_name='model_2',
                        target_yr=yr,
                        in_one=model_1.out_file_1,
                        in_two=model_1.out_file_2)

        model_2.advance()
        model_2.close()

        # instantiate third model
        model_3 = Prox( config=config_3,
                        model_name='model_3',
                        target_yr=yr,
                        in_one=model_2.out_file_1,
                        in_two=model_2.out_file_2)

        model_3.advance()
        model_3.close()


# create the path references to your config files
config_1 = '/Users/d3y010/repos/github/proxymod/example/config_1.ini'
config_2 = '/Users/d3y010/repos/github/proxymod/example/config_2.ini'
config_3 = '/Users/d3y010/repos/github/proxymod/example/config_3.ini'

# run it
tight_coupling(config_1, config_2, config_3, 2010, 2025, 5)
```

### Tight coupling - two-way - run one timestep at a time

This is an example of creating a three-model file exchange tight coupling where feedback is provided to the upstream models from the subsequent runs. Each model runs until a single timestep and the resulting output files (two for each model) are passed to the next model in line. Each model will create its own output directory and log file.


```python
from proxymod.model import Prox


def tight_coupling_twoway(config_1, config_2, config_3, start_yr, end_yr, step):
    """
    This function creates three instances of proxymod models. A configuration.ini
    file has been prepared for each.  This test utilizes the built in CSV files as
    data and transfers them to the next model in the configuration per timestep. Each
    timestep repeats based on feedback provided by the two downstream models.
    """

    for yr in range(start_yr, end_yr + step, step):


        # instantiate first model
        model_1 = Prox(config=config_1,
                       model_name='model_1',
                       target_yr=yr)
        # run model_1
        model_1.advance()
        model_1.close()

        # instantiate second model
        model_2 = Prox( config=config_2,
                        model_name='model_2',
                        target_yr=yr,
                        in_one=model_1.out_file_1,
                        in_two=model_1.out_file_2)

        model_2.advance()
        model_2.close()

        # instantiate third model
        model_3 = Prox( config=config_3,
                        model_name='model_3',
                        target_yr=yr,
                        in_one=model_2.out_file_1,
                        in_two=model_2.out_file_2)

        model_3.advance()
        model_3.close()

        # INCORPORATING TIMESTEP FEEDBACK FROM MODEL_2 and MODEL_3 in MODEL_1
        model_1 = Prox( config=config_1,
                        model_name='model_1',
                        target_yr=yr,
                        in_one=model_2.out_file_1,
                        in_two=model_3.out_file_2)
        model_1.advance()
        model_1.close()

        model_2 = Prox( config=config_2,
                        model_name='model_2',
                        target_yr=yr,
                        in_one=model_1.out_file_1,
                        in_two=model_1.out_file_2)
        model_2.advance()
        model_2.close()

        model_3 = Prox( config=config_3,
                        model_name='model_3',
                        target_yr=yr,
                        in_one=model_2.out_file_1,
                        in_two=model_2.out_file_2)
        model_3.advance()
        model_3.close()

# create the path references to your config files
config_1 = '/Users/d3y010/repos/github/proxymod/example/config_1.ini'
config_2 = '/Users/d3y010/repos/github/proxymod/example/config_2.ini'
config_3 = '/Users/d3y010/repos/github/proxymod/example/config_3.ini'

# run it
tight_coupling_twoway(config_1, config_2, config_3, 2010, 2025, 5)
```
