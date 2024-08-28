import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_DIRECTORY = r"C:\Users\QiweiFu\Documents\EXP240605-5/export-exp.csv"
z = pd.read_csv(FILE_DIRECTORY)
x = (z-0.15)*1000
y = np.log10((z-0.15)*100)*(z-0.15)*200

plt.rcParams['axes.facecolor'] = 'black'
# histogram on linear scale
plt.subplot(211)
hist, bins, _ = plt.hist(z, bins=500, histtype = 'step')

# histogram on log scale.
# Use non-equal bin sizes, such that they look equal on log scale.
logbins = np.logspace(np.log10(100), np.log10(100000), len(bins))
plt.subplot(212)
plt.hist(z, bins=logbins, histtype = 'step', fill= True)
plt.xscale('log')
plt.show()