import ipywidgets as widgets
import matplotlib.pyplot as plt
from . import utils
import numpy as np
from IPython.display import display

def main():
	# Create widgets
	pKa1_w = widgets.FloatSlider(
    min=-4, max=18, step=0.01, value=2.0,
    description=r'\(\mathrm{p}K_{\mathrm{a},1}\)',
    layout=widgets.Layout(width='auto', grid_area='pKa1')) # read in pKa1
	#
	i2_w = widgets.Checkbox(
			value=False, description=' ', 
			disabled=False, indent=False,
			layout=widgets.Layout(width='auto', grid_area='i2')) # turn diprotic on/off
	pKa2_w = widgets.FloatSlider(
			min=-4, max=18, step=0.01, value=6.0, 
			description=r'\(\mathrm{p}K_{\mathrm{a},2}\)',
			layout=widgets.Layout(width='auto', grid_area='pKa2')) # read in pKa2
	#
	i3_w = widgets.Checkbox(
			value=False, description=' ', 
			disabled=False, indent=False,
			layout=widgets.Layout(width='auto', grid_area='i3')) # turn triprotic on/off
	pKa3_w = widgets.FloatSlider(
			min=-4, max=18, step=0.01, value=10.0, 
			description=r'\(\mathrm{p}K_{\mathrm{a},3}\)',
			layout=widgets.Layout(width='auto', grid_area='pKa3')) # read in pKa3
	# Arrange widgets into grid
	controls = widgets.GridBox(
			children=[pKa1_w, pKa2_w, pKa3_w, i2_w, i3_w],
					layout=widgets.Layout(
							width='65%', grid_template_rows='auto',
							grid_template_columns='90% 10%',
							grid_template_areas='''
							"  pKa1 . "
							"  pKa2 i2 "
							"  pKa3 i3 "
							''')
				)

	# Set up the plot
	fig = plt.figure(constrained_layout=True, figsize=(6, 4))
	ax = fig.add_subplot(111)
	pH = np.linspace(0, 14, 100)
	ax.set_xlim([-1,15])
	ax.set_xlabel('pH')
	ax.set_ylim([-10,110])
	ax.set_ylabel(r'% conc.')
	lines = []
	nans = np.nan*np.ones_like(pH)
	fig.set_label('Ion Speciation')
	for i in range(4):
			lines.append(ax.plot(pH, nans)[0])

	# Define
	def update(pKa1, pKa2, pKa3, i2, i3):
			args = [pKa1,]
			pKa2_w.value = max(pKa1, pKa2_w.value)
			pKa3_w.value = max(pKa2_w.value, pKa3_w.value)

			if i2:
				args.append(pKa2_w.value)
			else:
				i3_w.value = False
				lines[-2].set_ydata(nans)
				
			if i3_w.value:
				args.append(pKa3_w.value)
			else:
				lines[-1].set_ydata(nans)				

			utils.plot_speciation(lines, pH, *args)
			fig.canvas.draw_idle()

	wplot = widgets.interactive_output(update, dict(pKa1=pKa1_w, pKa2=pKa2_w, pKa3=pKa3_w, i2=i2_w, i3=i3_w))
	display(widgets.VBox([controls,wplot]))
