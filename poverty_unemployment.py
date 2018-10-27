#!/usr/bin/env python3

import pandas as pd
from scipy.stats import fisher_exact

data = pd.read_csv('/storage/s8zrzug3/PUMS-HUS/hus.csv')

'''
Question: Is there anything wrong with our use
of HUPAOC? It says "children under 6 and 6 to 17".
Does that mean that it requires at least one child
from each age group or that any child from either
age group will fulfill the requirement?
'''


def poverty_test():
	'''
	Test for statistical significance with
	Fisher's Exact Test to examine effect
	of single-parenthood on whether or not
	a family falls below the poverty line. 
	'''
	def __are_impoverished(data):
		'''
		Evaluates dataframe to examine whether
		a particular household falls below the
		poverty threshold.
		'''
		def __get_level(people, state):
			'''
			Accepts num. people and state they live in,
			returns poverty threshold for these parameters.
			'''
			if people > 8:
				people = 8
			people_to_level = {
				1: 12060,
				2: 16240,
				3: 20420,
				4: 24600,
				5: 28780,
				6: 32960,
				7: 37140,
				8: 41320
			}
			hawaii_levels = {
				1: 13860,
				2: 18670,
				3: 23480,
				4: 28290,
				5: 33100,
				6: 37910,
				7: 42720,
				8: 47530
			}
			alaska_levels = {
				1: 15060,
				2: 20290,
				3: 25520,
				4: 30750,
				5: 35980,
				6: 41210,
				7: 46440,
				8: 51670
			}
			if state == 15: #Hawaii
				return hawaii_levels[people]
			elif state == 2: #Alaska
				return alaska_levels[people]
			else:
				return people_to_level[people]

		return pd.Series([
			True if __get_level(row['NP'], row['ST']) > row['FINCP'] else False
			for index, row in data.iterrows()
		])

	impoverished = __are_impoverished(data)

	#Pull rows for each classification
	num_single_impoverished = data.loc[
		((data['HHT'] == 2) | (data['HHT'] == 3)) & #Single mother or single father
		(data['HUPAOC'] == 3) &	#Children less than 18 present
		(impoverished) #Below poverty line
	]['WGTP'].sum()

	num_single_not_impoverished = data.loc[
		((data['HHT'] == 2) | (data['HHT'] == 3)) & #Single mother or single father
		(data['HUPAOC'] == 3) &	#Children less than 18 present
		(~impoverished) #Above poverty line
	]['WGTP'].sum()

	num_married_impoverished = data.loc[
		(data['HHT'] == 1) & #Married parents
		(data['HUPAOC'] == 3) &	#Children less than 18 present
		(impoverished) #Below poverty line
	]['WGTP'].sum()

	num_married_not_impoverished = data.loc[
		(data['HHT'] == 1) & #Married parents
		(data['HUPAOC'] == 3) &	#Children less than 18 present
		(~impoverished) #Above poverty line
	]['WGTP'].sum()

	#Test for stat. sig.
	t,p = fisher_exact([
		[num_single_impoverished, num_married_impoverished],
		[num_single_not_impoverished, num_married_not_impoverished]
	], equal_var=False)

	if p < .05:
		print("Effect of marriage on poverty is statistically significant.")
	else:
		print("Effect of marriage on poverty is not statistically significant.")

	percent_impoverished = num_single_impoverished / (num_single_impoverished + num_single_not_impoverished)
	print(percent_impoverished, "\% of single parents are impoverished.")


def percent_unemployed():
	'''
	Calculate the percentage of single-parent households
	where the householder is unemployed.
	'''
	num_unemployed = float(data.loc[
		(
			(data['WORKSTAT'] == 11) |  #Single father, unemployed
			(data['WORKSTAT'] == 14)	#Single mother, unemployed
		) & (data['HUPAOC'] == 3)		#Children less than 18 present
	]['WGTP'].sum())
	num_employed = float(data.loc[
		(
			(data['WORKSTAT'] == 10) |  #Single father, employed
			(data['WORKSTAT'] == 13)    #Single mother, employed
		) & (data['HUPAOC'] == 3)		#Children less than 18 present
	]['WGTP'].sum())
	percent = num_unemployed / (num_employed + num_unemployed)
	print("Percent unemployed: ", percent)


def main():
	poverty_test()
	percent_unemployed()
	percent_single_by_race()

if __name__ == '__main__':
	main()