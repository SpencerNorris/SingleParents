#!/usr/bin/env python3

import pandas as pd

def percent_single_by_race():
	'''
	Get the percent of households with children under 18
	that are single-parent households, with a breakdown
	by broad racial group.
	'''
	race_codes = [
		1 : 'White alone',
		2 : 'Black or African American alone',
		3 : 'American Indian alone',
		6 : 'Asian alone',
		9 : 'Two or more races'
	]

	for code in race_codes.keys():
		num_single = data.loc[
			(data['SFR'] == 3) &
			(data['RAC1P'] == code)  #Matches on race code
		]['WGTP'].sum()

		num_total = data.loc[
			(
				(data['SFR'] == 2) |
				(data['SFR'] == 3)
			) &
			(data['RAC1P'] == code)  #Matches on race code
		]['WGTP'].sum()
		percent = float(num_single) / float(num_total)
		print(percent, "\% of ", race_codes[code], " families are single-parent families.")

def main():
	percent_single_by_race()

if __name__ == '__main__':
	main()