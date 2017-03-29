Histogram
=========

A cli to display histograms and fit distributions to data.  Input should be a
file containing a single float value per line.  Example usage:

- Display histogram of file
  ```
  histogram input.txt
  ```
- Display histogram from stdin:
  ```
  <cmd> | histogram
  ```
- Fit exponential distribution and show using log scale:
  ```
  histogram --log-y --fit-dist expon input.txt
  ```
- Fit a power law distribution to the input and show on log-log scale:
  ```
  histogram --log-x --log-y --fit-dist powerlaw input.txt
  ```
- Fit a normal distribution to the input
  ```
  histogram --fit-dist norm
  ```

Installation
------------
Run `pip install -e .` in this directory.

Notes
------
- The graphs are interactive, allowing you to inspect values, zoom, pan, etc.
- The ideal number of bins to use for the histograms is automatically computed.
  If you'd prefer to manually specify the bins, use the `--bins` parameter.
- Run `histogram --help` to see a full list of options
- If you'd like to filter the input values by size,
  [`jq`](https://stedolan.github.io/jq/) is a useful tool for this.  For
  example:
  ```
  cat input.txt | jq 'select(. > 0.01 and . < 2000)' | histogram
  ```

Credits
-------

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage)
project template.  The plots are created using the fantastic
[plotly](https://github.com/plotly/plotly.py) library.
