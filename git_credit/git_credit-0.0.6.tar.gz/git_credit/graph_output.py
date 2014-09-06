"""Display a matplotlib graph of the git credit for users with it installed."""


# NB: these kinda suck. I'm very new to matplotlib and haven't messed around
#     with it much yet. If anyone wants to pretty these up a bit, I'm welcome
#     to receive pull requests for that :)


try:
    import numpy
    from matplotlib import pylab, pyplot
except ImportError:
    ENABLED = False
else:
    ENABLED = True


def pie_chart(all_credit, graph_title):
    """Display the all_credit dictionary as a pie chart with matplotlib."""

    if not ENABLED:
        return

    # magic numbers are magical. at least the user can resize afterwards
    pylab.figure(1, figsize=(6, 6))
    pylab.axes([0.1, 0.1, 0.8, 0.8])

    pylab.pie(
        all_credit.values(),
        labels=all_credit.keys(),
        autopct='%1.1f%%',
        shadow=True,
        startangle=90,
    )

    pylab.title(graph_title)

    pylab.show()


def bar_chart(all_credit, graph_title):
    """Display a bar chart with the all_credit dictionary.

    Args:

        all_credit: dictionary of {author: lines in HEAD}
        graph_title: string title to display with the graph
    """

    if not ENABLED:
        return

    fig = pyplot.figure()
    chart = fig.add_subplot(111)

    np_arange = numpy.arange(len(all_credit))
    width = 0.25  # the width of the bars

    # setup the bars
    chart.bar(
        np_arange,
        all_credit.values(),
        width,
    )

    # axes and labels
    chart.set_xlim(-width, len(np_arange) + width)
    chart.set_ylim(0, max(all_credit.values()))
    chart.set_ylabel("Lines of code in HEAD")
    chart.set_title(graph_title)

    # this looks good for a couple people, but crappy for many :/
    chart.set_xticks(np_arange + (width / 2))

    # add x axis labels
    pyplot.setp(
        chart.set_xticklabels(all_credit.keys()),
        rotation=290,
        fontsize=10,
    )

    pyplot.show()
