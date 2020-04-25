def title_styles(fs=12, ff='sans-serif', fw='normal', color='black'):
    """Returns a dictionary of values for the fontdict of plt.title

    See: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.title.html
    """
    return ({
        'fontsize': fs,
        'fontfamily':ff,
        'fontweight': fw,
        'color':color,
    })
def title_position(loc='left', pad=15,):
    """Returns a dictionary of values for the chart title position

    See: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.title.html
    """
    return({
        'loc':loc,
        'pad':pad,

    })
def the_sup_title_position(x=0, y=0.97, ha='left', va='top'):
    """Returns a dictionary of values for the figure title position
    See https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.suptitle.html
    """
    return({
        'x':x,
        'y':y,
        'ha':ha,
        'va':va,
    })
def title_content(label="A title"):
    """Sets the label property for a title or any other componet
    """
    return {'label':label}
