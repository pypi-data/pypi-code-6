import matplotlib
matplotlib.use('Agg')

from matplotlib.testing.decorators import image_comparison

import matplotlib.pylab as plt
import matplottheme as mpt
import numpy as np

@image_comparison(baseline_images=['summary1'], extensions=['png'])
def test_summary1():
    fig = plt.figure(figsize=(12, 14))
    ax = fig.add_subplot(321)
    
    np.random.seed(0)

    for i in range(8):
        y = np.random.normal(size=1000).cumsum()
        x = np.arange(1000)

        mpt.plot(ax, x, y, label='Data {index}'.format(index=str(i + 1)))
    mpt.legend(ax, ncol=2, loc='lower left')
    
    ax = fig.add_subplot(322)
    
    np.random.seed(0)

    x = np.arange(6)
    y1 = np.random.uniform(size=6) * 100
    y2 = np.random.uniform(size=6) * 100

    mpt.bar(ax, x, y1, width=0.4, label='Data 1', annotations=[str(int(d)) for d in y1])
    mpt.bar(ax, x + 0.4, y2, width=0.4, label='Data 2', annotations=[str(int(d)) for d in y2])
    ax.set_xticks(np.arange(6) + 0.4)
    ax.set_xticklabels(['Set {index}'.format(index=str(i)) for i in np.arange(6) + 1])
    mpt.legend(ax)
    
    ax = fig.add_subplot(323)
    
    np.random.seed(1)

    for i in range(8):
        x = np.random.normal(size=1000) + i

        mpt.hist(ax, x, label='Data {index}'.format(index=str(i + 1)),
                 grid=True, orientation='horizontal')
    
    ax = fig.add_subplot(324)
    
    np.random.seed(0)

    x = np.random.normal(size=(1000, 8))

    mpt.boxplot(ax, x, ticks=['Set {index}'.format(index=i + 1) for i in range(8)])
    
    ax = fig.add_subplot(325)
    
    np.random.seed(0)

    for i in range(8):
        x = np.random.normal(size=1000) + i
        y = np.random.normal(size=1000) + i

        mpt.scatter(ax, x, y, label='Data {index}'.format(index=str(i + 1)))
    mpt.legend(ax, title='Legend', scatterpoints=3)
    
    fig.tight_layout()
