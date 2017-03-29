import re
from functools import update_wrapper

import click
import numpy as np

import deep_stats.activations.histogram
from deep_stats.activations.layer_activations import LayerActivations
from deep_stats.config import Config


def pass_activations_context(f):
    """
    Used for subcommands of activations to pass config and model as first two
    params
    """
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        layer_activations = ctx.find_object(LayerActivations)
        return ctx.invoke(f, layer_activations, *args, **kwargs)
    return update_wrapper(new_func, f)


@click.group(chain=True)
@click.option(
    '--input',
    '-i',
    type=click.Path(exists=True),
    default='data/train.jpg',
    help='Input data to train on'
)
@click.pass_context
def activations(ctx, input):
    """Various activation stats"""
    config = ctx.find_object(Config)
    ctx.obj = LayerActivations(config.model, config.layers, input)


@activations.command()
@pass_activations_context
@click.option(
    '--min',
    '-l',
    default=0.01,
    help="Minimum value to display in histogram range"
)
@click.option(
    '--max',
    '-h',
    default=np.inf,
    help="Maximum value to display in histogram range"
)
@click.option(
    '--bins',
    '-n',
    default='auto',
    help="Number of bins to use; integer or algorithm to use"
)
@click.option(
    '--log-x/--no-log-x',
    default=False,
    help="Whether to use log scale for x axis"
)
@click.option(
    '--log-y/--no-log-y',
    default=False,
    help="Whether to use log scale for y axis"
)
@click.option(
    '--fit/--no-fit',
    default=True,
    help="Whether to fit a linear function to the histogram"
)
def histogram(layer_activations, min, max, bins, log_x, log_y, fit):
    """Display histogram of activations"""
    if re.match('\d+', bins):
        bins = int(bins)
    deep_stats.activations.histogram(
        layer_activations,
        min,
        max,
        bins,
        log_x,
        log_y,
        fit
    )
