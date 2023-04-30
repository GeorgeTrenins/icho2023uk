# -*-coding:utf-8 -*-

from __future__ import print_function, division, absolute_import
import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
from . import utils

fig = plt.figure(constrained_layout=True, figsize=(4, 3))
ax = fig.add_subplot(111)

ca = 0.01
cb_max = 0.02
npts = 500
cb = np.linspace(0, cb_max, npts)
pKa = -7
pH = []
for val in cb:
	pH.append(utils.find_pH(ca, pKa, counterion=val))
pH = np.asarray(pH)

line, = ax.plot(pH, cb*1000)
ax.set_xlim(1, 13)
ax.set_xlabel(r'$\mathrm{pH}$')
ax.set_ylim(-50*cb_max, 1050*cb_max)
ax.set_ylabel(r'$c_b / \mathrm{mM}$')

fig.savefig('buffer_strong.png', dpi=300)

pKa = 7
pH = []
for val in cb:
	pH.append(utils.find_pH(ca, pKa, counterion=val))
pH = np.asarray(pH)
line.set_xdata(pH)
ax.set_xlim(3.5, 12.5)
fig.savefig('buffer_weak.png', dpi=300)
