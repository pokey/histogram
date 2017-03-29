import click
import numpy as np
import plotly
import yaml
from plotly.graph_objs import Bar, Layout, Marker, Scatter

from histogram.distributions import distributions
from histogram.util.func import pairwise
from histogram.util.stats import (
    format_fit_params,
    format_kstest,
    format_probplot
)


EN_DASH = '\u2013'
FIT_COLOR = 'rgb(31, 119, 180)'
DATA_COLOR = 'rgb(255, 127, 14)'


def perform_fit(boundaries, data, dist_name, do_tests):
    dist = distributions[dist_name]
    fit_params = dist.fit(data)
    data_size = len(data)

    x = boundaries[:-1]
    y = [
        (dist.cdf(right, *fit_params) -
         dist.cdf(left, *fit_params)) * data_size
        for left, right in pairwise(boundaries)
    ]

    yaml_out = dict(
        fitParams=format_fit_params(fit_params),
    )

    if do_tests:
        yaml_out.update(dict(
            ksTest=format_kstest(data, dist_name, fit_params),
            probplot=format_probplot(data, dist_name, fit_params),
        ))

    click.echo(yaml.dump(yaml_out, default_flow_style=False))

    return Scatter(
        x=x,
        y=y,
        mode='lines',
        marker=Marker(color=FIT_COLOR),
        name='Fit',
    )


def histogram(data, bins, log_x, log_y, chart_type, fit_dist, do_tests, out):
    hist, boundaries = np.histogram(data, bins)

    if chart_type == 'scatter':
        x = boundaries[:-1]
        data_trace = Scatter(
            x=x,
            y=hist,
            mode='markers',
            marker=Marker(color=DATA_COLOR),
            name='Data',
        )
    else:
        # Convert boundaries to string describing range
        x = [
            "{:.1f}{}{:.1f}".format(left, EN_DASH, right)
            for left, right in pairwise(boundaries)
        ]
        data_trace = Bar(x=x, y=hist)

    traces = [data_trace]
    if fit_dist is not None:
        traces.append(perform_fit(boundaries, data, fit_dist, do_tests))

    plotly.offline.plot({
        "data": traces,
        "layout": Layout(
            title="Histogram",
            xaxis=dict(type='log' if log_x else None),
            yaxis=dict(type='log' if log_y else None),
        )
    }, filename=out)
