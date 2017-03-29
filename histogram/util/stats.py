from scipy.stats import kstest, probplot


def format_fit_params(fit_params):
    ret = {}

    if len(fit_params) == 2:
        loc, scale = fit_params
    else:
        shape, loc, scale = fit_params
        ret['shape'] = str(shape)

    ret['loc'] = '{:.3g}'.format(loc)
    ret['scale'] = '{:.3g}'.format(scale)

    return ret


def format_kstest(data, dist_name, fit_params):
    D, p = kstest(data, dist_name, fit_params)
    return dict(
        D='{:.3g}'.format(float(D)),
        p='{:.3g}'.format(float(p)),
    )


def format_probplot(data, dist_name, fit_params):
    # Suggested by http://stats.stackexchange.com/a/27966
    _, (_, _, r) = probplot(data, fit_params, dist_name)
    return dict(
        r='{:.3g}'.format(float(r)),
    )
