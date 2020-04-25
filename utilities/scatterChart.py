import matplotlib.dates as mdates
from matplotlib import cm
from matplotlib import colors as mcolors
import matplotlib.pyplot as plt
from utilities.utility_functions import save_the_figure as save_the_figure
import numpy as np

def scatterPlot(**kwargs):

    fig, ax = plt.subplots(figsize=(8,5))

    number_of_locations = len(kwargs['locations'])
    number_of_samples= len(kwargs['a_df'])
    if(number_of_locations > 1):
        plural_or_not = 'locations'
    else:
        plural_or_not = 'location'

    kwargs['the_title']["label"] = "Total number of samples: {} from {} {}.".format(
        number_of_samples,
        number_of_locations,
        plural_or_not
    )
    kwargs['the_sup_title']["label"] = '{}, {} - {}'.format(kwargs['the_sup_title']["label"], kwargs['min_date'], kwargs['max_date'])

    color_map = plt.cm.get_cmap(kwargs['color_map'], 100)
    color=iter(color_map(np.linspace(.2,.75, number_of_locations)))
    a_df = kwargs['a_df']

    for location in kwargs['locations']:
        new_color = next(color)
        new_df = a_df[a_df['location'] == location]
        x=new_df['py_date']
        y=new_df['total']
        plt.scatter(x, y, color=new_color, label=location, s=kwargs['point_size'], edgecolor=kwargs['edge_c'])

    plt.ylabel(kwargs['y_axis']['label'],
               fontfamily=kwargs['y_axis']['fontfamily'],
               labelpad=kwargs['y_axis']['lablepad'],
               color=kwargs['y_axis']['color'],
               size=kwargs['y_axis']['size']
              )

    plt.xlabel(kwargs['x_axis']['label'],
               fontfamily=kwargs['x_axis']['fontfamily'],
               labelpad=kwargs['x_axis']['lablepad'],
               color=kwargs['x_axis']['color'],
               size=kwargs['x_axis']['size'],
               ha='left',
               x=0
              )

    plt.subplots_adjust(**kwargs['subplot_params'])
    plt.title(
        kwargs['the_title']['label'],
        fontdict=kwargs['title_style'],
        pad=kwargs['the_title_position']['pad'],
        loc=kwargs['the_title_position']['loc'],
        )
    plt.suptitle(kwargs['the_sup_title']['label'],
                 fontdict=kwargs['sup_title_style'],
                 # color=kwargs['sup_title_style']['color'],
                 x=kwargs['sup_title_position']['x'],
                 y=kwargs['sup_title_position']['y'],
                 va=kwargs['sup_title_position']['va'],
                 ha=kwargs['sup_title_position']['ha']
                )

    plt.grid(b=True, which='major', axis='both')

    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    days = mdates.DayLocator()
    weeks = mdates.WeekdayLocator(byweekday=1, interval=1, tz=None)
    years_fmt = mdates.DateFormatter(kwargs['x_tick_date']['years'])
    months_fmt = mdates.DateFormatter(kwargs['x_tick_date']['months'])
    days_fmt = mdates.DateFormatter(kwargs['x_tick_date']['days'])


    if(kwargs['ticks'] == 'years'):
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.xaxis.set_minor_locator(months)
    elif(kwargs['ticks'] == 'months'):
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_minor_formatter(months_fmt)
    elif(kwargs['ticks']== 'days'):
        ax.xaxis.set_major_locator(weeks)
        ax.xaxis.set_major_formatter(days_fmt)
        ax.xaxis.set_minor_locator(days)


    save_the_figure(**kwargs['save_this'])

    plt.show()
    plt.close()
