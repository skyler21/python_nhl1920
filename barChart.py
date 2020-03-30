import numpy as np
import matplotlib.pyplot as plt

# data to plot
n_groups = 10
means_frank = (2, 1, 4, 4, 2, 1, 0, 0, 0, 0)
means_guido = (1, 2, 2, 1, 4, 3, 0, 0, 0, 0)

print (type(means_frank))
# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, means_frank, bar_width,
alpha=opacity,
color='b',
label='CBJ')

rects2 = plt.bar(index + bar_width, means_guido, bar_width,
alpha=opacity,
color='g',
label='OTT')

plt.xlabel('Goals')
plt.ylabel('Games')
plt.title('Goals by team')
plt.xticks(index + bar_width, ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
plt.legend()

plt.tight_layout()
plt.show()