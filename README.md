
# proxymod

## *A lightweight Python package to simulate model interactions*

## Contact
Chris Vernon (chris.vernon@pnnl.gov)

## Description

**proxymod** enables modelers to explore multiple types of model interactations without bearing the large overhead of getting up-to-speed on learning to run multiple complex models. This package also expedites the testing of various interactions by eliminating the runtime associated with complex models by using proxy models to emulate their characteristics but run for a user-defined amount of time.

**proxymod** instances can be configured with a configuration file, two input CSV files, two output CSV files, the ability to introduce an error during runtime, a defined runtime, and the ability to inherit and return Python objects.  These options give the user freedom to quickly test multiple types of model interactions for as many model instances as they wish.

The following are some potential use-cases of **proxymod**:
- testing messaging services
- setting up a modeling framework for multi-model interaction
- testing HPC environments with multiple model setups

## Terminology

There are many different definitions for types of model coupling. **proxymod** adopts the Kraucunas (2018) nomenclature where each coupling type fits into the following two categories:  *Coupling* is defined as two or more model components exchanging information and *Forcing or boundary conditions* which are defined as the process where outputs from one model are used to drive another. These are described as the following:

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
2. Setup your configuration.ini files and prepare an arrangement of **proxymod** instances that suits your needs
3. Run it!

## Full coupling - file transfer


```python
from proxymod.model import Prox

def file_transfer(config_1, config_2, config_3):
    """
    This function creates three instances of proxymod models. A configuration.ini
    file has been prepared for each.  This test utilizes the built in CSV files as
    data and transfers them to the next model in the configuration.
    """

    # instantiate first model
    model_1 = Prox( config=config_1,
                    model_name = 'model_1',
                    start_yr = 2010,
                    end_yr = 2100,
                    step = 5)

    # instantiate second model
    model_1 = Prox( config=config_2,
                    model_name = 'model_2',
                    start_yr = 2010,
                    end_yr = 2100,
                    step = 5)

    # instantiate third model
    model_1 = Prox( config=config_3,
                    model_name = 'model_3',
                    start_yr = 2010,
                    end_yr = 2100,
                    step = 5)


if __name__ == '__main__':

    # create the path references to your config files
    config_1 = '/ft_config_1.ini'
    config_2 = '/ft_config_2.ini'
    config_3 = '/ft_config_3.ini'

    # run it
    file_transfer(config_1, config_2, config_3)
```



