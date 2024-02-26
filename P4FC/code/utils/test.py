"""
@Title        : 提供一些假设检验的格式化
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-01-02 22:00:52
@Description  : 
"""


import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tools.sm_exceptions import InterpolationWarning
from pandas import Series
from numpy import ndarray
from matplotlib.figure import Figure
from typing import Union

import warnings

warnings.simplefilter(action='ignore', category=InterpolationWarning)
warnings.filterwarnings('ignore', '.*output shape of zoom.*')


def adf_test(x: Union[Series, ndarray]) -> Series:
    """Function for performing the Augmented Dickey-Fuller test for stationary

    Null Hypothesis: time series is not stationary
    Alternative Hypothesis: time series is stationary

    Parameters
    ----------
    x : Series | ndarray
        The time series to be checked for stationarity

    Returns
    -------
    Series
        A `Series` with the ADF test's results
    """
    indices = ['Test Statistic', 'p-value',
               '# of Lags Used', '# of Observations Used']
    adf_test = adfuller(x, autolag='AIC')
    results = pd.Series(adf_test[0:4], index=indices)

    for key, value in adf_test[4].items():
        results[f'Critical Value ({key})'] = value

    return results


def kpss_test(x: Union[Series, ndarray], h0_type: str = 'c') -> Series:
    """Function for performing the Kwiatkowski-Phillips-Schmidt-Shin test for stationarity

    Null Hypothesis: time series is stationary
    Alternate Hypothesis: time series is not stationary

    Parameters
    ----------
    x : Series | ndarray
        The time series to be checked for stationarity
    h0_type : str, {'c', 'ct'}
        Indicates the null hypothesis of the KPSS test:
        - 'c': The data is stationary around a constant(default)
        - 'ct': The data is stationary around a trend

    Returns
    -------
    Series
        A `Series` with the KPSS test's results
    """
    indices = ['Test Statistic', 'p-value', '# of lags']
    kpss_test = kpss(x, regression=h0_type)
    results = pd.Series(kpss_test[0:3], index=indices)

    for key, value in kpss_test[3].items():
        results[f'Critical Value ({key})'] = value
    return results


def test_autocorrelation(x: Union[Series, ndarray],
                         n_lags: int = 40, alpha: float = .05, h0_type: str = 'c') -> Figure:
    """Function for testing the stationary of a series by using
    - the ADF test
    - the KPSS test
    - ACF/PACF plots

    Parameters
    ----------
    x : Series | ndarray
        The time series to be checked for stationarity
    n_lags : int, optional
        The number of lags for the ACF/PACF plots, by default 40
    alpha : float, optional
        Significance level for the ACF/PACF plots, by default .05
    h0_type : str, {'c', 'ct'}
        Indicates the null hypothesis of the KPSS test:
        - 'c': The data is stationary around a constant(default)
        - 'ct': The data is stationary around a trend

    Returns
    -------
    Figure
        Figure containing the ACF/PACF plot
    """
    adf_results = adf_test(x)
    kpss_results = kpss_test(x, h0_type)

    print(f"ADF test statistics: {adf_results['Test Statistic']:.2f} "
          f"(p-val: {adf_results['p-value']:.2f})")

    print(f"KPSS test statistic: {kpss_results['Test Statistic']:.2f} "
          f"(p-val: {kpss_results['p-value']:.2f})")

    fig, ax = plt.subplots(2, figsize=(16, 10))
    plot_acf(x, ax=ax[0], lags=n_lags, alpha=alpha)
    plot_pacf(x, ax=ax[1], lags=n_lags, alpha=alpha)

    return fig


if __name__ == '__main__':
    kpss_test()
