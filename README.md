# pyRNAfold

Collection of scripts and `jupyter` notebooks to analyse and visualize the output of `RNAfold` program from `Vienna RNA` package.

# Setup

Clone the repo:

`$ git clone https://github.com/eco32i/pyRNAfold.git`

If you want to use `python 3` virtualenv (tested on Ubuntu 16.04):

- Navigate to `pyRNAfold/scripts` and run the `bootstrap.sh` script that will install system wide dependencies and create Python 3 virtual environment called `pyRNA` in `$HOME/.venv`:

   `$ ./bootstrap.sh --all`

   The list of installed packages in the final virtualenv is given in `requirements.txt` file.

Alternatively, you can use `conda` to create an environment with the same dependencies.

To run the notebooks, activate `pyRNA` environment:

`$ source ~/.venv/pyRNA/bin/activate`

Or, if you are using `conda` environment:

`$ source activate pyRNA`

Then go to `notebooks` directory and start `jupyter` session:

`$ jupyter notebook`

# Notebooks (HSR1 is used throughout as an example)

- **Folding**: explains the output of RNAfold and how it is parsed
- **Folding analysis**: an example of working with the output of RNAfold for different temperatures
- **Heatmaps**: `bokeh` heatmaps

