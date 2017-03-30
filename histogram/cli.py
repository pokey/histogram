# -*- coding: utf-8 -*-
import re

import click
import numpy as np
from click import UsageError

from histogram import histogram
from histogram.distributions import distributions


@click.command()
@click.option(
    '--bins',
    '-n',
    default='auto',
    help="Number of bins to use; integer or algorithm to use"
)
@click.option(
    '--log-x/--no-log-x',
    '-x',
    default=False,
    help="Whether to use log scale for x axis"
)
@click.option(
    '--log-y/--no-log-y',
    '-y',
    default=False,
    help="Whether to use log scale for y axis"
)
@click.option(
    '--chart-type',
    '-c',
    type=click.Choice(['scatter', 'bar']),
    default='scatter',
    help="Whether to use log scale for y axis"
)
@click.option(
    '--fit-dist',
    '-f',
    type=click.Choice(distributions.keys()),
    default=None,
    help="Whether to probability distribution to the input"
)
@click.option(
    '--tests/--no-tests',
    default=True,
    help="Whether to do goodness-of-fit tests"
)
@click.option(
    '--out',
    '-o',
    type=click.Path(),
    default='temp-plot.html',
    help="Output path for plot"
)
@click.argument('input', type=click.File('r'), default='-')
def main(bins, log_x, log_y, chart_type, fit_dist, tests, out, input):
    """Display histogram"""
    if chart_type == 'bar' and fit_dist is not None:
        raise UsageError("Bar chart not supported in combination with "
                         "fit_dist")
    if tests and fit_dist == "skewnorm":
        click.echo(
            "WARNING: Running goodness-of-fit tests with skewnorm is slow",
            err=True
        )
    if re.match('\d+', bins):
        bins = int(bins)
    data = np.array([float(x) for x in input])
    histogram(data, bins, log_x, log_y, chart_type, fit_dist, tests, out)


if __name__ == "__main__":
    main()
