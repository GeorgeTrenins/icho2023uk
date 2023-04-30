# -*-coding:utf-8 -*-

from __future__ import print_function, division, absolute_import
import ipywidgets as widgets
import numpy as np
import matplotlib.pyplot as plt
from . import utils
from IPython.display import display, Markdown

interact_manual = widgets.interact.options(manual=True, manual_name="Calculate pH")

def find_pH(ca, pKa):
	ans = utils.find_pH(ca, pKa)
	display(Markdown('$\mathrm{{pH}} = {:.2f}$'.format(ans)))


def main():
	# Create widgets
	pKa = widgets.FloatText(
    value=7.0,
		step=0.5,
    description=r'\(\mathrm{p}K_{\mathrm{a}}\)',
    disabled=False
	)

	ca = widgets.FloatText(
    value=0.001,
		step=0.0001,
    description=r'\(c_{\mathrm{a}} / \mathrm{M}\)',
    disabled=False
	)

	interact_manual(find_pH, ca=ca, pKa=pKa)
