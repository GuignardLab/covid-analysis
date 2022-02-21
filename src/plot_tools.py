import pandas as pd
from scipy.ndimage.filters import generic_filter
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import warnings

def get_lethality_rate(data: pd.DataFrame,
                       country: str, *,
                       smoothing_size=7,
                       additional_plots=[],
                       death_delay=1,
                       height=2,
                       start=None,
                       end=None):
    """
    Plot a figure with including the lethatlity rate and
    some other plots if asked to.
    It is a fairly simple function but should allow you to
    do few things that could be useful.
    The lethality of a given day `d` is computed as the number
    of positive persons during `max(1, death_delay)` days divided
    by the number of death during `max(1, death_delay)` days,
    `death_delay` days after the day `d`.
    
    Args:
    ----
        country (str): The name of the country to plot
        smoothing_size (int): the size of the smoothing in days
            default value: 7, meaning that each value is the
            average value over 7 days
        additional_plot (list of str): List of values to plot.
            The available values can be accessed by doing
            `data.keys()`.
            Default value: [] (no other plot is made)
        death_delay (int): The delay in days to compute the
            lethality ratio
        height (int): the height of 1 plot (given than the width is 10).
        start (str): starting date from which to make the plot.
            The date is expected to be in the format 'yyyy-mm-dd'.
            If None is given starts at the begining of the dataset.
            Default None
        end (str): ending date to which to make the plot.
            The date is expected to be in the format 'yyyy-mm-dd'.
            If None is given ends at the end of the dataset.
            Default `None`
    """
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    country_data = data[data['location']==country]
    if start is None:
        start = country_data['date'].min()
    if end is None:
        end = country_data['date'].max()
    to_keep = (start<=country_data['date'])&(country_data['date']<=end)
    sub_data = country_data[to_keep] 
    dates = sub_data['date'][to_keep]
    months = np.array([date.fromisoformat(d).strftime('%b-%Y') for d in dates])
    all_ticks = np.arange(len(months))
    ticks = np.where(months[1:]!=months[:-1])[0]
    tick_labels = months[ticks+1]
    nb_plots = 1+len(additional_plots)
    fig, axes = plt.subplots(nb_plots, 1, figsize=(10, height*nb_plots), sharex=True)
    if 1 < nb_plots:
        ax = axes[0]
    else:
        ax = axes

    cases = generic_filter(country_data.sort_values('date')['new_cases'],
                           np.nanmean, size=smoothing_size)
    death = generic_filter(country_data.sort_values('date')['new_deaths'],
                           np.nanmean, size=smoothing_size)
    if death_delay == 0:
        lethality_rate = death/cases
    else:
        lethality_rate = death[death_delay:]/cases[:-death_delay]
    lethality_rate[1<lethality_rate]=0
    lethality_rate = lethality_rate[to_keep[death_delay:]]
    all_ticks = all_ticks[len(all_ticks)-len(lethality_rate):]
    ax.plot(all_ticks, lethality_rate, '-', label='Lethality ratio')
    ax.set_ylabel('Ratio death over #cases')
    ax.legend()
    ax.set_title(country)
    if 1 < nb_plots:
        for ax, val in zip(axes[1:], additional_plots):
            Y = generic_filter(country_data.sort_values('date')[val],
                               np.nanmean, size=smoothing_size)[to_keep]
            ax.plot(Y, '-', label=val)
            ax.set_ylabel(f'#{val}')
            if 'per_hundred' in val:
                ax.set_ylim(0, 100)
            ax.legend()
    step_ticks = max(1, len(ticks)//6)
    ax.set_xticks(ticks[::step_ticks])
    ax.set_xticklabels(tick_labels[::step_ticks])
    fig.tight_layout()
    return fig