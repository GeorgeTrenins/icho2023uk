#!/usr/bin/env python
# -*-coding:utf-8 -*-

from __future__ import print_function, division, absolute_import
import math
import warnings
import numpy as np
import matplotlib.pyplot as plt


pKw = 14.0
Kw = 1.0e-14

### buffer capacity ###
def beta(pH, ca, pKa):

	H = 10**(-pH)
	Ka = 10**(-pKa)
	ln10 = np.log(10.0)
	ans = ca*Ka*H/(H+Ka)**2
	ans += Kw/H + H
	return ln10 * ans

### Speciation ###
def get_species(pH, *args):
	# For an n-protic acid, calculate the ratio of [H_(n-j) A^(j-)]/c_tot
	# given a pH and the pKas
	pKas = np.asarray(args, dtype=float) # 1
	if np.any(pKas[1:] < pKas[:-1]):
		raise ValueError("The pKas are expected in increasing order!")
	n = len(args)
	m = len(pH)
	num = np.ones((n+1, m))
	for i, pKa in enumerate(pKas):
		num[i+1] = num[i]*10**(pH - pKa)
	den = np.sum(num, axis=0)
	return num/den

def plot_speciation(lines, pH, *pKas):
	
	species = get_species(pH, *pKas)
	for line,y in zip(lines,species):
		line.set_ydata(100*y)



### pH calculations ###

def build_equation(ca, *args, counterion=0.0):
	# For an n-protic acid, given the total acid concentration
	# in mol/dm^3 and the pKas, construct the polynomial equation 
	# for the concentration of H+.

	# Can also simulate titration by specifying the 
	# concentration of counterions.

	# Returns the coefficients of [H+]^(n+2) ... [H+]^0

	pKas = np.asarray(args, dtype=float)
	n = len(pKas)
	if ca < 0:
		raise ValueError("Acid concentration must be positive!")
	if counterion < 0:
		raise ValueError("Counterion concentration must be positive!")
	if np.any(pKas[1:] <= pKas[:-1]):
		raise ValueError("The pKas are expected in increasing order!")
	pKa_cum = np.cumsum(pKas)
	Kj = 10**(-pKa_cum)
	#                      -2   -1   0  1...n  n+1  n+2
	Kj = np.concatenate(([0.0, 0.0, 1.0], Kj, [0.0, 0.0]))
	p = Kj[2:] - np.arange(-1, n+2, 1)*ca*Kj[1:-1] - Kw*Kj[:-2]
	p += counterion*Kj[1:-1]

	return p

def find_pH(ca, *args, counterion=0.0):
	# Given the total acid concentration in mol/dm^3 and
	# the pKas, find the pH of the solution

	# Can also simulate titration by specifying the 
	# concentration of counterions.

	p = build_equation(ca, *args, counterion=counterion)
	solns = np.roots(p) # this gives all roots (n+2 in general)
	solns = solns.tolist()
	eps = 1.0e-8
	candidates = []
	for s in solns:
		reH, imH = np.real(s), np.imag(s)
		if reH < min(10**(-pKw/2) - eps, Kw/(counterion+1.0e-16)):
			# unphysically low concentration - ignore
			continue
		elif reH > len(args)*ca + 10**(-pKw/2) + eps:
			# unphysically high concentration - ignore
			continue
		elif abs(imH/reH) > eps:
			# complex root - ignore
			continue
		else:
			candidates.append(reH)
	nH = len(candidates)
	if nH == 0:
		warnings.warn("Something went wrong, failed to find a solution!")
		return None
	elif nH == 1:
		return -math.log10(candidates[0])
	else:
		warnings.warn("Something went wrong, found multiple solutions!")
		return -np.log10(candidates)

if __name__ == "__main__":

	import argparse
	import matplotlib.pyplot as plt

	parser = argparse.ArgumentParser()
	parser.add_argument('ca', type=float, help="Total concentration of acid.")
	parser.add_argument('pKa', nargs='+', type=float, help='Acid pKas.')
	parser.add_argument('--cation', type=float, default=0.0, help='Concentration of counterion')
	args = parser.parse_args()
	
	print("  Acid concentration: {:.3e} M".format(args.ca))
	print("         Acid pKa(s): {:}".format(args.pKa))
	print("Cation concentration: {:}".format(args.cation))
	print("         Solution pH: {:.2f}".format(find_pH(args.ca, *args.pKa, counterion=args.cation)))

	fig, ax = plt.subplots()
	base_conc = np.linspace(0.0, 2*len(args.pKa)*args.ca, 500) # twofold excess
	pHs = []
	for conc in base_conc:
		pHs.append(find_pH(args.ca, *args.pKa, counterion=conc))
	pHs = np.asarray(pHs)
	ax.plot(base_conc, pHs)
	ax.axvline(args.cation, color='k', ls=':')
	ax.set_ylim([0,14])
	plt.show()

