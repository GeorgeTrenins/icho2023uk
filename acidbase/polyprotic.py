# -*-coding:utf-8 -*-

from __future__ import print_function, division, absolute_import
import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
from . import utils
from IPython.display import display, Markdown

interact_manual = widgets.interact.options(manual=True, manual_name="Calculate pH")

def find_pH(ca, pKa):
	pKas = np.asarray(pKa.split(','), dtype=float)
	ans = utils.find_pH(ca, *pKas)
	display(Markdown('$\mathrm{{pH}} = {:.2f}$'.format(ans)))


def main():
	# Create widgets
	pKa = widgets.Text(
    value='-2, 1.99',
    placeholder='Type a list of pKa values',
    description=r'\(\mathrm{p}K_\mathrm{a}\)s:',
    disabled=False
)

	ca = widgets.FloatText(
    value=0.001,
		step=0.0001,
    description=r'\(c_{\mathrm{a}} / \mathrm{M}\)',
    disabled=False
	)

	interact_manual(find_pH, ca=ca, pKa=pKa)
