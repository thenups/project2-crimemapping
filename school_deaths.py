# Dependencies
import pandas as pd
import matplotlib.pyplot as plt

# Read in CSV and create DataFrame
filepath = 'cleaned_school_shootings_1990_2018.csv'
csv = pd.read_csv(filepath)
df = pd.DataFrame(csv)

def school_death_df():
	#View head and dtypes
	# df.head()

	# Function to build list of years
	def build_year_list(num_year):
    	start_year = 1990
    	for i in range(0, num_year-1):
        	year_list.append(start_year+i)
    	return year_list

	# Variables
	year_list = []
	fatality_counter = 0
	fatalities_per_year = {}

	#Calling the function
	build_year_list(26)

	# year_list

	# Function to assign deaths to the year
	def fatality_counter(year_list):
    	for i in range(len(year_list)):
        	fatality_count = df[df['Year'] == year_list[i]]['Fatalities'].sum()
        	fatalities_per_year.update({year_list[i]:fatality_count})
    	return fatalities_per_year

	# Calling the fundtion
	fatality_counter(year_list)

	# Building the DF from the list/dict data
	school_deaths_df = pd.DataFrame(fatalities_per_year, index=[0])

	school_deaths_df = school_deaths_df.transpose()
	school_deaths_df = school_deaths_df.rename(index=str, columns={0: "value"})

	# school_deaths_df.head()

	school_deaths_df = school_deaths_df.reset_index()

	#school_deaths_df.head()

	school_deaths_df = school_deaths_df.rename(index=str, columns={'index': "year"})

	#school_deaths_df.head()

	# One way to work with list/dicts data
	# lists = fatalities_per_year.items()

	# One way to unpack a dict into its key and value
	# x, y = zip(*lists)

	# Plotting data to show correlation
	y = school_deaths_df.value
	x = school_deaths_df.year

	plt.plot(x,y)
	plt.xlabel('year')
	plt.ylabel('number of school shootings')
	plt.title('Number of Shootings over Time')
	plt.xticks(rotation=70)
	plt.show()

return school_deaths_df
