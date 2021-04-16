import numpy as np

inf = 100


def delta(x):
    return [inf if ix == 0 else 0 for ix in x]


def inertia_free(x, use_h=False, k=2, h=delta):
    if use_h:
        return k * h(x)
    else:
        return k * x


def delta(x):
    return inf if x == 0 else 0


def clean_lag(x, use_h=False, i_lag=2, h=delta):
    y = np.zeros_like(x)
    if use_h:
        for i in range(len(x)):
            y[i] = x[i] * h(x[i - i_lag])
    else:
        for i in range(len(x)):
            y[i] = x[i - i_lag]

    return y


def aperiodic_h(x, period):
    return [(1 / period) * np.exp(-ix / period) if ix >= 0 else 0 for ix in x]


def aperiodic_link(x, use_h=False, period=3, h=aperiodic_h):
    y = np.asarray(x)
    if use_h:
        return h(x, period)
    y[0] = 0
    for i in range(len(x) - 1):
        y[i + 1] = y[i] * (period - 1) / period + x[i + 1] * (1 / period)

    return y


def black_box(x, use_h=True, L=5):
    h = np.ones_like(x)
    y = np.zeros_like(x)

    if not use_h:
        print('Чёрный ящик задаётся только своей весовой функцией')
        return y

    for i in range(len(x)):
        for j in range(L):
            y[i] += h[j] * x[i - j]
    return y
