import ipywidgets as widgets
import matplotlib.pyplot as plt
from . import utils
import numpy as np
from IPython.display import display

def main():
	# Create widgets
	pKa = widgets.FloatSlider(
    min=2, max=12, step=0.025, value=4.0,
    description=r'\(\mathrm{p}K_{\mathrm{a}}\)',
    layout=widgets.Layout(width='auto', grid_area='pKa')) # read in pKa1
	#
	ca = widgets.FloatSlider(
			min=0.0, max=0.1, step=0.0001, value=0.02, 
			description=r'\(c_{\mathrm{a}}\)',
			layout=widgets.Layout(width='auto', grid_area='ca')) # read in pKa2
	# Arrange widgets into grid
	controls = widgets.GridBox(children=[pKa, ca],
		layout=widgets.Layout(
								width='65%', grid_template_rows='auto',
								grid_template_columns='100% 100%',
								grid_template_areas='''
								"  pKa "
								"  ca "
								''')
					)

	# Set up the plot
	fig = plt.figure(constrained_layout=True, figsize=(6, 4))
	ax = fig.add_subplot(111)
	pH = np.linspace(1.5, 12.5, 500)
	ax.set_xlim([1,13])
	ax.set_xlabel('pH')
	ax.set_ylim([-0.005,0.08])
	ax.set_ylabel(r'$\beta$')
	nans = np.nan*np.ones_like(pH)
	fig.set_label('Buffer capacity')
	line, = ax.plot(pH, nans)

	# Define
	def update(pKa, ca):
		beta = utils.beta(pH, ca, pKa)
		line.set_ydata(beta)
		fig.canvas.draw_idle()

	wplot = widgets.interactive_output(update, dict(pKa=pKa, ca=ca))
	display(widgets.VBox([controls,wplot]))
