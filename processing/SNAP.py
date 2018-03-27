import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import pearsonr

def foreclosure():

	filepath = "../SNAP_data.csv"
	csv = pd.read_csv(filepath)
	df_SNAP = pd.DataFrame(csv)

	df_SNAP = df_SNAP.set_index('Fiscal Year')

	df_SNAP = df_SNAP.loc['2004':'2014']['Average Participation']

	x1 = df_fore.index.get_values()
	y1 = df_fore['Home_repos']
	y3 = df_fore['foreclosure_filings']

	x2 = df_homocides.loc['2004':'2014'].index.get_values()
	y2 = df_homocides.loc['2004':'2014']['value']
	y4 = df_sch_deaths.loc['2002':'2016']['value']
	y5 = df_SNAP

	fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(8,12))
	#ax1 = plt.gca()
	#ax1.set_ylim(ax1.get_ylim()[::-1])
	ax1.plot(x1, y1, 'o', linestyle='', color='red')
	ax2.plot(x2, y2, '^', linestyle='', color='black')
	ax3.plot(x1, y3, '*', linestyle='', color='green')
	ax4.plot(x1, y4, '_', linestyle='', color='purple')
	ax5.plot(x1[:-2], y5, '+', linestyle='', color='violet')
	plt.tight_layout()
	plt.xlabel('year')
	#plt.ylabel('number of repos')
	#ax1 = plt.gca()
	#ax1.set_ylim(ax1.get_ylim()[::-1])
	#plt.title('Number of Home Repos over Time')
	plt.show()