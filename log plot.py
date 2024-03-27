import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_DIRECTORY = r"C:\Users\QiweiFu\Downloads\EXP240326-1/export 2.csv"
x = pd.read_csv(FILE_DIRECTORY)
x = (x-0.15)*1000
y = np.log10((x-0.15)*100)*(x-0.15)*1000


# histogram on linear scale
plt.subplot(211)
hist, bins, _ = plt.hist(x, bins=150, histtype = 'step')

# histogram on log scale.
# Use non-equal bin sizes, such that they look equal on log scale.
logbins = np.logspace(np.log10(1),np.log10(100000),len(bins))
plt.subplot(212)
plt.hist(x, bins=logbins, histtype = 'step')
plt.xscale('log')
plt.show()