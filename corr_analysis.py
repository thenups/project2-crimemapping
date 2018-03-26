# Analysis was done to see if one of the largest states (california) showed any correlation between school shootings and homicides

# Loading dependents
import pandas as pd
import numpy as np
import scipy
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.interpolate import *
import scipy
from scipy.stats import pearsonr


def correlation_analysis():
	# Loading files
	filepath = "cleaned_crime_by_jurisdiction.csv"
	csv1 = pd.read_csv(filepath)
	df = pd.DataFrame(csv1)

	#df.head()

	# Pre-processing the file for homicide data for CA
	df.groupby('agency_jurisdiction').crimes_percapita.mean().sort_values(ascending=False)
	df_new = df[['report_year', 'population', 'violent_crimes', 'homicides', 'state']]
	df_new_top_violent = df_new.groupby(['state', 'report_year']).sum()
	df_new_top_violent = df_new_top_violent.reset_index('report_year')

	vio_crime_values = df_new_top_violent.loc[['CA'],['report_year', 'homicides']]

	#plotting the data for all years for homicides, CA
	x2 = vio_crime_values['report_year']
	y2 = vio_crime_values['homicides']
	p2 = np.polyfit(x2, y2, 1)

	plt.plot(x2,y2, color='green', marker='o', linestyle='')
	#plt.plot(x3,y3_adj, color='green', marker='^', linestyle='')
	plt.plot(x2, np.polyval(p2, x2), color='red')
	#plt.plot(x3, np.polyval(p3, x3), color='gray')
	#blue_patch = mpatches.Patch(label='homocides')
	#orange_patch = mpatches.Patch(color='green', label='school shootings (*100)')
	#plt.legend(handles=[blue_patch, orange_patch])
	plt.xlabel('year')
	plt.ylabel('number of homicides')
	plt.title('Number of Homicides in CA over Time')
	plt.savefig('/images/ca_homicides.jpeg', dpi = 200)
	plt.show()

	####################################################################################################

	# Analysis on shootings for CA for all years
	filepath = 'cleaned_school_shootings_1990_2018.csv'
	csv2 = pd.read_csv(filepath)
	df_school = pd.DataFrame(csv2)

	#df_school.head()

	# pre-processing the file
	df_school = df_school[['City', 'State', 'Fatalities', 'Year']]

	#df_school.head()

	df_school.State.replace(['New York', 'Texas', 'Tennessee', 'Nevada', 'California', 'Iowa', 'Ohio',\
                        'Massachusetts', 'Georgia', 'Illinois', 'North Carolina', 'Florida', 'South Carolina',\
                        'Michigan', 'Arizona', 'Washington', 'Arkansas', 'Pennsylvania', 'Alabama',\
                        'Maryland', 'Indiana', 'Kentucky', 'Mississippi', 'Nebraska', 'Missouri',\
                        'Oklahoma', 'Alaska', 'Virginia', 'New Hampshire', 'New Mexico', 'Hawaii',\
                        'Connecticut', 'Louisiana', 'Wisconsin', 'Utah', 'Colorado', 'Wyoming', 'Delaware']\
                        , ['NY', 'TX', 'TN', 'NV', 'CA', 'IA', 'OH', 'MA', 'GA', 'IL', 'NC', 'FL', \
                        'SC','MI', 'AZ', 'WA', 'AR', 'PA', 'AL', 'MD', 'IN', 'KY', 'MS', 'NE', 'MO',\
                        'OK', 'AK', 'VA', 'NH', 'NM', 'HI', 'CT', 'LA', 'WI', 'UT', 'CO', 'WY', 'DE'], inplace=True)

	df_school = df_school[['State', 'Year', 'Fatalities']]
	df_school = df_school.groupby(['State', 'Year']).sum()
	df_new_school = df_school.reset_index('Year')

	# df_new_school.head()

	school_shootings = df_new_school.loc[['CA'],['Year', 'Fatalities']]

	# plotting the school shootings data for all years for CA
	x1 = school_shootings['Year']
	y1 = school_shootings['Fatalities']
	p1 = np.polyfit(x1, y1, 1)

	plt.plot(x1,y1, color='blue', marker='o', linestyle='')
	#plt.plot(x3,y3_adj, color='green', marker='^', linestyle='')
	plt.plot(x1, np.polyval(p1, x1), color='red')
	#plt.plot(x3, np.polyval(p3, x3), color='gray')
	#blue_patch = mpatches.Patch(label='homocides')
	#orange_patch = mpatches.Patch(color='green', label='school shootings (*100)')
	#plt.legend(handles=[blue_patch, orange_patch])
	plt.xlabel('year')
	plt.ylabel('number of school shootings')
	plt.title('Number of Shootings in CA over Time')
	plt.savefig('/images/ca_school_shootings.jpeg', dpi = 200)
	plt.show()

###################################################################################################
	
	# finding the correlation values for school shootings vs. homicide rate in CA
	x = scipy.array(y1)
	y2 = y2[:-1]
	y = scipy.array(y2)

	r_row1, p_value1 = pearsonr(x, y)

	# print(r_row1, p_value1)

####################################################################################################

	# Building dataframes with crime, school shooting df and homicide data
	crime_per_year = {}
	year_list = []

	def build_year_list(num_year):
		start_year = 1990
		for i in range(0, num_year-1):
			year_list.append(start_year+i)
    
    return year_list, r_row1, p_value1, crime_per_year, df_crime, df_homocides, crime_list

    build_year_list(26)

    def violent_crime_count(year_list):
    	for i in range(len(year_list)):
        	crime_count = df[df['report_year'] == year_list[i]]['violent_crimes'].sum()
        	crime_per_year.update({year_list[i]: crime_count})
    
    violent_crime_count(year_list)

    df_crime = pd.DataFrame(crime_per_year, index=[0])
    df_crime = df_crime.transpose()
    df_crime = df_crime.rename(index=str, columns={0: "value"})

    homocides_per_year = {}
    def homocide_count(year_list):
    	for i in range(len(year_list)):
    		homocide_count = df[df['report_year'] == year_list[i]]['homicides'].sum()
    		homocides_per_year.update({year_list[i]: homocide_count})
    
    homocide_count(year_list)

	df_homocides = pd.DataFrame(homocides_per_year, index=[0])
	df_homocides = df_homocides.transpose()
	df_homocides = df_homocides.rename(index=str, columns={0: "value"})

	fatalities_per_year = {1990: 2, 1991: 12, 1992: 14, 1993: 37, 1994: 23, 1995: 15, 1996: 24, 1997: 17,\
							1998: 28, 1999: 22, 2000: 14, 2001: 10, 2002: 15, 2003: 10, 2004: 9, 2005: 14,\
							2006: 25, 2007: 39, 2008: 24, 2009: 14, 2010: 14, 2011: 8, 2012: 44, 2013: 24,\
							2014: 17}

	df_sch_deaths = pd.DataFrame(fatalities_per_year, index=[0])
	df_sch_deaths = df_sch_deaths.transpose()
	df_sch_deaths = df_sch_deaths.rename(index=str, columns={0: "value"})

	# performing correlation calculations
	lists2 = homocides_per_year.items()
	x2, y2 = zip(*lists2)

	lists3 = fatalities_per_year.items()
	x3, y3 = zip(*lists3)

	y3_adj = []
	for i in range(len(y3)):
		y3_adj.append(y3[i]*100)

	p2 = np.polyfit(x2, y2, 1)
	p3 = np.polyfit(x3, y3_adj, 1)

	# Given the y output variables range school shootings were multiplied by 100
	plt.plot(x2,y2, color='blue', marker='o', linestyle='')
	plt.plot(x3,y3_adj, color='green', marker='^', linestyle='')
	plt.plot(x2, np.polyval(p2, x2), color='red')
	plt.plot(x3, np.polyval(p3, x3), color='gray')
	blue_patch = mpatches.Patch(label='homocides')
	orange_patch = mpatches.Patch(color='green', label='school shootings (*100)')
	plt.legend(handles=[blue_patch, orange_patch])
	plt.xlabel('year')
	plt.ylabel('number of murders')
	plt.title('Amount of Murders over Time')
	plt.savefig('/images/murders.jpeg', dpi = 200)
	plt.show()

	# Building a dictionary of tuples
	lists1 = crime_per_year.items()

	# Unpacking the list of tuples into an x, y value
	x1, y1 = zip(*lists1)
	p1 = np.polyfit(x1, y1, 1)

	# plotting data
	plt.plot(x1,y1, 'o', linestyle='')
	plt.plot(x1, np.polyval(p1, x1), color='red')
	plt.xlabel('year')
	plt.ylabel('number of crimes')
	plt.title('Amount of Violent Crime over Time')
	plt.savefig('/images/violent_crimes.jpeg', dpi = 200)
	plt.show()

	# Building a list of the crime values only - no keys or indexes
	crime_list = []
	for key, value in crime_per_year.items():
		crime_list.append(value)

	# Building a list of the death values only - no keys or indexes
	death_list = []
	for key, value in fatalities_per_year.items():
		death_list.append(value)

	# Building a list of the murder values only - no keys or indexes
	murder_list = []
	for key, value in homocides_per_year.items():
		murder_list.append(value)


	# using Scipy to do some basic stats on the data that we have
	# studying correlation between school fatalities and total violent crime
	x4 = scipy.array(death_list)
	y4 = scipy.array(crime_list)
	r_row4, p_value4 = pearsonr(x4, y4)

	# Studying correlation between school deaths and murders
	x6 = scipy.array(death_list)
	y6 = scipy.array(murder_list)
	r_row6, p_value6 = pearsonr(x6, y6)

	return r_row6, r_row4, p_value6, p_value4, r_row1, p_value1, crime_per_year, df_crime,\
	df_homocides, crime_list, vio_crime_values, school_shootings
