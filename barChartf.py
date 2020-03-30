import matplotlib.pyplot as plt
import numpy as np


def chart(n_groups, v_name, v_data, v_agnst, h_name, h_data, h_agnst):
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.20
    opacity = 0.8

    rects1 = plt.bar(index, v_data, bar_width,
                     alpha=opacity,
                     color='b',
                     label=v_name)

    rects2 = plt.bar(index + bar_width, h_data, bar_width,
                     alpha=opacity,
                     color='g',
                     label=h_name)

    rects3 = plt.bar(index + bar_width + bar_width, v_agnst, bar_width,
                      alpha=opacity,
                      color='b',
                      hatch = '/')

    rects4 = plt.bar(index + bar_width + bar_width + bar_width, h_agnst, bar_width,
                     alpha=opacity,
                     color='g',
                     hatch='/')

    plt.xlabel('Goals')
    plt.ylabel('Games')
    plt.title('Goals by team')
    plt.xticks(index + bar_width, ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
    plt.legend()

    plt.tight_layout()
    plt.show()
    return
