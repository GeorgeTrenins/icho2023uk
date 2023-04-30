# -*-coding:utf-8 -*-

from __future__ import print_function, division, absolute_import
import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
from . import utils
from IPython.display import display, Markdown

interact_manual = widgets.interactive
npts = 1000

def get_equiv_pH(equiv, V_add, pH):
	# approximate the pH at the equivalence point
	idx = np.argmin(np.abs(V_add-equiv))
	V0 = V_add[idx]
	if V0 > equiv:
		b = (idx-1, idx)
	else:
		b = (idx, idx+1)

	if b[-1] >= len(V_add):
		# prevent out-of-range error
		ans = pH[-1] + 100
	else:
		slope = (pH[b[1]] - pH[b[0]])/(V_add[b[1]] - V_add[b[0]])
		ans = slope*(equiv-V_add[b[0]]) + pH[b[0]]
	return ans

def plot_pH(na, pKa, Vi, C, line, vline, hline, fig, Vmax=50.0):
	# na in mol/dm^3
	# Vi abd Vmax in mL
	Vi = Vi/1000
	Vmax = Vmax/1000
	V_add = np.linspace(0, Vmax, npts)
	ca = na/(Vi + V_add)
	cb = C*V_add/(Vi+V_add)
	pH = []
	for x, y in zip(ca, cb):
		pH.append(utils.find_pH(x, pKa, counterion=y))
	line.set_ydata(np.asarray(pH))
	equiv = 1000*na/C
	xdata = np.asarray(vline.get_xdata())
	xdata[:] = equiv
	vline.set_xdata(xdata)
	#
	ydata = np.asarray(hline.get_ydata())
	ydata[:] = get_equiv_pH(equiv, V_add*1000, pH)
	hline.set_ydata(ydata)
	#
	fig.canvas.draw_idle()


def main():
	# Create widgets
	pKa = widgets.FloatText(
    value=4.76,
		step=0.5,
    description=r'\(\mathrm{p}K_{\mathrm{a}}\)',
    disabled=False
	)

	na = widgets.FloatText(
    value=0.0001,
		step=0.00005,
    description=r'\(n_{\mathrm{a}} / \mathrm{M}\)',
    disabled=False
	)

	Vi = widgets.FloatText(
    value=100.0,
		step=25.0,
    description=r'\(V_{\mathrm{i}} / \mathrm{mL}\)',
    disabled=False
	)

	C = widgets.FloatText(
    value=0.004,
		step=0.0001,
    description=r'\(C / \mathrm{M}\)',
    disabled=False
	)

	fig = plt.figure(constrained_layout=True, figsize=(6, 4))
	ax = fig.add_subplot(111)
	Vmax = 50.0
	V_add = np.linspace(0, Vmax, npts)
	pH = np.empty_like(V_add)*np.nan
	line, = ax.plot(V_add, pH)
	ax.set_xlim(-5, Vmax+5)
	ax.set_xlabel(r'$V_{\mathrm{t}} / \mathrm{mL}$')
	ax.set_ylim(0, 14)
	ax.set_ylabel(r'$\mathrm{pH}$')
	vline = ax.axvline(x=Vmax/2, ls='-', c='k', lw='1')
	hline = ax.axhline(y=7.0, ls='-', c='k', lw='1')
	fig.set_label('Titration Curve')

	widget=interact_manual(
		lambda na, pKa, Vi, C: (plot_pH(na, pKa, Vi, C, line, vline, hline, fig, Vmax)),
		{'manual' : True, 'manual_name' : 'Plot curve'}, 
		na=na, pKa=pKa, Vi=Vi, C=C)

	box_layout = widgets.Layout(
									width='70%',
									justify_content='center')

	top = widgets.HBox([pKa, na])
	bottom =  widgets.HBox([Vi, C])
	controls = widgets.HBox([widgets.VBox([top, bottom, widget.children[-2]], layout=box_layout),])

	display(widgets.VBox([controls,] + list(widget.children[-1:])))

	# interact_manual(lambda na, pKa, Vi, C: (plot_pH(na, pKa, Vi, C, line, fig, Vmax)),
	#  na=controls[0], pKa=controls[1], Vi=controls[2], C=controls[3])
