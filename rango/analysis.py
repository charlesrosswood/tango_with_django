# Create your views here.
from django.core.management import setup_environ
from tango_with_django_project import settings
setup_environ(settings)
# from django.http import HttpResponse
# from django.template import RequestContext
# from django.shortcuts import render_to_response
# from django.forms.models import modelformset_factory
# from django.views.decorators import csrf
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect

import datetime
from dateutil.relativedelta import *
import csv
import json

from rango.models import CSVfiles
# from rango import analysis 
# from rango.models import SiteUserForm, WallPostForm
# from rango.forms import *

def binning_data( data, num_of_bins ):
	"""
	This function will take an x-y dataset and returned the binned version
	of the dataset, e.g. 
	an array of [ [x-max value of bin, number of occurances in bin],... ]
	"""
	binned_data = []

	min_data = min(data)
	max_data = max(data)
	data_range = abs(max_data - min_data)
	bin_size = data_range / float(num_of_bins)

	bin_mins = [min_data]
	bin_maxs = [bin_mins[-1] + bin_size]

	while bin_maxs[-1] < max_data:
		bin_mins.append( bin_maxs[-1] )
		bin_maxs.append( bin_mins[-1] + bin_size )

	frequencies = [0] * len(bin_maxs)
	xy_dataset = []

	for datum in data:
		success = False
		for i in xrange(len(bin_maxs)):
			# print "range", bin_mins[i], bin_maxs[i], 'datum', datum
			if (datum >= bin_mins[i]) and (datum  <= bin_maxs[i]):
				# if (i != len(bin_maxs)-1) and (datum < bin_maxs[i]):
				frequencies[i] += 1 
				success = True
				# elif (i == len(bin_maxs)) and (datum <= bin_maxs[i]):
				# 	if category == 'employment':
				# 		print "datum", datum, "range", bin_mins[-1], bin_maxs[-1]
				# 	frequencies[i] += 1 
				# 	success = True

			# elif (datum >= bin_mins[-1]) and (datum  <= bin_maxs[-1]):
			# 	if category == 'employment':
			# 		print "datum", datum, "range", bin_mins[-1], bin_maxs[-1]
			# 	frequencies[-1] += 1
			# 	success = True

		if success == False:
			print "Failed to bin data: ", datum

	for i in xrange(len(bin_maxs)):
		xy_dataset.append( [ bin_maxs[i], frequencies[i] ] )

	return xy_dataset

def groupingTransactions( x, y, minimum_x_constraint ):
	"""
	This function will group y_data values together based on some condition on 
	how close x_values are allowed to get.
	"""
	if len(x) != len(y):
		print "ERROR: datasets of different lengths"
		return [], []

	if len(y) > 1:

		new_x = []
		new_y = []

		summed_transaction_amounts = 0 # adds the transaction amount for transactions on one day
		for i in xrange(1,len(x)):

			if i == 1: # if it's the first transaction in the list...
				current_date = x[i] # ...then set the running date to that date
				summed_transaction_amounts += y[i]
			elif (x[i] < (current_date+minimum_x_constraint)) and (i != len(x)-1): # else if the transaction is part of the same transaction (e.g. it happened on the same date)...
				summed_transaction_amounts += y[i] # ...add the transaction amount to the amount to add
				# continue # ...do nothing
			elif (x[i] < (current_date+minimum_x_constraint)) and (i == len(x)-1): # else if this is the last transaction in the list...
				# current_date = x[i] # ...make the date to add the current date
				summed_transaction_amounts += y[i] # ...add the transaction amount on and append the data point
				new_x.append( current_date )
				new_y.append( summed_transaction_amounts )
			elif i == len(x)-1:
				new_x.append( current_date )
				new_y.append( summed_transaction_amounts )

				new_x.append( x[i] )
				new_y.append( y[i] )
			else: # else the transaction is neither the first nor last in the list, and isn't on the same day as the previous one
				new_x.append( current_date ) # add the previous defined date
				new_y.append( summed_transaction_amounts ) # add the previous total transactions
				current_date = x[i]
				summed_transaction_amounts = y[i]
	
	else:
		return [], []
	
	return new_x, new_y

def read_transactions_csv( csvfile ):
	"""
	This function does no analysis, it just groups transactions that occur
	in a particular category together, it does not generate a histogram.
	"""
	csvfile.csv_file.open(mode='rb') # opening the file for reading ans such like
	csv_list = csvfile.csv_file.read().split('\n')

	data_dict = { }
	data_dict[ 'totals' ] = {'amount':[], 'date':[]}
	data_dict[ 'in' ] = {'amount':[], 'date':[]}
	data_dict[ 'out' ] = {'amount':[], 'date':[]}

	title_row = csv_list[0].split('"')
	new_title_row = []
	for i in xrange(len(title_row)):
		if i%2 == 0: # then even element
			temp_to_add = title_row[i].split(',')
			temp_to_add = [element.replace('\r','') for element in temp_to_add if (element.strip() != '' and element.strip() != ',')]
			new_title_row.extend( temp_to_add )
		else: # then odd element
			new_title_row.extend( [str(title_row[i]).replace('\r','')] )

	try:
		group_column = new_title_row.index("Group")
	except:
		group_column = new_title_row.index("transactionTag")
	# group_column = new_title_row.index("Tag")
	try:
		tag_column = new_title_row.index("Tag")
	except:
		tag_column = new_title_row.index("transactionTag") 

	try:
		amount_column = new_title_row.index("Amount")
	except:
		amount_column = new_title_row.index("transactionAmount")

	try:		
		date_column = new_title_row.index("Date")
	except:
		date_column = new_title_row.index("transactionDateTime")

	for row in csv_list[1:]:
		if row != '' and row != '\n':
			row = row.split('"')
			new_row = []
			for i in xrange(len(row)):
				if i%2 == 0: # then even element
					temp_to_add = row[i].split(',')

					temp_to_add = [element.replace('\r','') for element in temp_to_add if ( element.strip() != ',' and element.strip() != '')]
					new_row.extend( temp_to_add )
				else: # then odd element
					new_row.extend( [str(row[i]).replace('\r','')] )

			category = new_row[group_column].lower()
			tag = new_row[tag_column].lower()

			try:
				date = datetime.datetime.strptime(new_row[date_column], '%d/%m/%Y')
			except:
				elements_of_date = new_row[date_column].split('-')
				date_stringy = str(elements_of_date[0])
				for element_of_date in elements_of_date[1:]:
					if len(element_of_date) < 2:
						element_of_date = '0' + str(element_of_date)
					date_stringy += '-' + str(element_of_date)

				date = datetime.datetime.strptime(date_stringy, '%Y-%m-%d')

			amount = float(new_row[amount_column])

			if category not in data_dict.keys():
				data_dict.update( {category:{'amount':[], 'date':[]}})
			if tag not in data_dict.keys():
				data_dict.update( {tag:{'amount':[], 'date':[]}})

			data_dict[category][ 'amount' ].append( amount )
			data_dict[category][ 'date' ].append( date )
			data_dict[tag][ 'amount' ].append( amount )
			data_dict[tag][ 'date' ].append( date )

			data_dict[ 'totals' ][ 'amount' ].append( amount )
			data_dict[ 'totals' ][ 'date' ].append( date )

			if amount < 0.0 :
				data_dict[ 'out' ][ 'amount' ].append( amount )
				data_dict[ 'out' ][ 'date' ].append( date )
			else:
				data_dict[ 'in' ][ 'amount' ].append( amount )
				data_dict[ 'in' ][ 'date' ].append( date )

	csvfile.csv_file.close()

	return_dict = {}

	today = datetime.datetime.now()

	for category, data in data_dict.iteritems():

		days_since_now = []
		for i in xrange(len(data[ 'date' ])):
			days_since_now.append( abs((today - data[ 'date' ][i]).total_seconds()/86400.0) )

		new_diffs, grouped_spends = groupingTransactions( days_since_now, data_dict[category][ 'amount' ], 1 )

		if new_diffs != [] and grouped_spends != []:
			inserting_zero_element = [0.0] + new_diffs

			spends_per_day = []
			time_diffs = []

			for i in xrange(len(grouped_spends)):
				spends_per_day.append( grouped_spends[i] / (inserting_zero_element[i+1]-inserting_zero_element[i]) )
				time_diffs.append( (inserting_zero_element[i+1]-inserting_zero_element[i]) )

			return_dict.update( {category:{}} )

			for i in xrange(20):
				num_of_bins = ((i+1)*3)
				spends_per_day_dataset = binning_data( spends_per_day, num_of_bins )
				frequency_dataset = binning_data( time_diffs, num_of_bins )

				dict_to_add = {i:{'spends per day':spends_per_day_dataset, 'frequency':frequency_dataset}}
				return_dict[ category ].update( dict_to_add )


	return return_dict
	
def read_turk_csv( csvfile ):
	"""
	This function does no analysis, it just groups transactions that occur
	in a particular category together, it does not generate a histogram.
	"""
	csvfile.csv_file.open(mode='rb') # opening the file for reading ans such like
	csv_list = csvfile.csv_file.read().split('\n')

	data_dict = { }
	# data_dict[ 'totals' ] = {'amount':[], 'date':[]}
	# data_dict[ 'in' ] = {'amount':[], 'date':[]}
	# data_dict[ 'out' ] = {'amount':[], 'date':[]}

	new_title_row = csv_list[0].split(',')
	print 'new_title_row', new_title_row, len(new_title_row)
	# new_title_row = []
	# for i in xrange(len(title_row)):
	# 	if i%2 == 0: # then even element
	# 		temp_to_add = title_row[i].split(',')
	# 		temp_to_add = [element.replace('\r','') for element in temp_to_add if (element.strip() != '' and element.strip() != ',')]
	# 		new_title_row.extend( temp_to_add )
	# 	else: # then odd element
	# 		new_title_row.extend( [str(title_row[i]).replace('\r','')] )

	# try:
	for i in xrange(len(new_title_row)):
		title = new_title_row[i]
		print i, title

		if "HITID" in title:
			HITID_column = i
		elif "Merchant_Name" in title:
			Merchant_Name_column = i
		elif "Transaction_Amount" in title:
			Transaction_Amount_column = i
		elif "Internal_Tag" in title:
			Internal_Tag_column = i
		elif "Merchant_Code" in title:
			Merchant_Code_column = i
		elif "Worker" in title:
			Worker_column = i
		elif "Answer" in title:
			Answer_column = i
		elif "Date" in title:
			Date_column = i
	# HITID_column = new_title_row.index('"HITID"')
	# # except:
	# 	# HITID_column = new_title_row.index("HITID")
	# # group_column = new_title_row.index("Tag")

	# # try:
	# Merchant_Name_column = new_title_row.index('"Merchant_Name"')
	# # except:
	# # 	Merchant_Name_column = new_title_row.index("Merchant_Name")

	# # try:		
	# Transaction_Amount_column = new_title_row.index('"Transaction_Amount"')
	# # except:
	# # 	Transaction_Amount_column = new_title_row.index("Transaction_Amount")

	# # try:
	# Internal_Tag_column = new_title_row.index('"Internal_Tag"')
	# # except:
	# 	# Internal_Tag_column = new_title_row.index("Internal_Tag") 


	# Merchant_Code_column = new_title_row.index('"Merchant_Code"')
	# Worker_column = new_title_row.index('"Worker"')
	# Answer_column = new_title_row.index('"Answer"')
	# Date_column = new_title_row.index('"Date"')

	high_level_tag_dict = {}
	low_level_tag_dict = {}

	for row in csv_list[1:]:
		if row != '' and row != '\n':
			new_row = row.split(',')

			narrative = new_row[Merchant_Name_column].lower()
			mcc_tag = new_row[Merchant_Code_column].lower().strip()
			
			turk_tag = new_row[Answer_column].lower()
			high_level_tag = turk_tag.split('::')[0]
			low_level_tag = turk_tag.split('::')[1]

			if mcc_tag[0] == '"':
				mcc_tag = mcc_tag[1:]
			if mcc_tag[-1] == '"':
				mcc_tag = mcc_tag[:-1]

			# if turk_tag[0] == '"':
			# 	turk_tag = turk_tag[1:]
			# if turk_tag[-1] == '"':
			# 	turk_tag = turk_tag[:-2]

			if high_level_tag[0] == '"':
				high_level_tag = high_level_tag[1:]
			if high_level_tag[-1] == '"':
				high_level_tag = high_level_tag[:-1]

			if low_level_tag[0] == '"':
				low_level_tag = low_level_tag[1:]
			if low_level_tag[-1] == '"':
				low_level_tag = low_level_tag[:-1]


			if mcc_tag not in high_level_tag_dict.keys():
				high_level_tag_dict.update( {mcc_tag:{}} )#{'high level tag':{}, 'low level tag':{}}})
			if mcc_tag not in low_level_tag_dict.keys():
				low_level_tag_dict.update( {mcc_tag:{}} )#{'high level tag':{}, 'low level tag':{}}})
			# if narrative not in data_dict.keys():
			# 	data_dict.update( {narrative:{'high level tag':{}, 'low level tag':{}}})

			if high_level_tag not in high_level_tag_dict[mcc_tag].keys():#['high level tag'].keys():
				high_level_tag_dict[mcc_tag].update( {high_level_tag:1} )
			else:
				high_level_tag_dict[mcc_tag][high_level_tag] += 1

			if low_level_tag not in low_level_tag_dict[mcc_tag].keys():#['high level tag'].keys():
				low_level_tag_dict[mcc_tag].update( {low_level_tag:1} )
			else:
				low_level_tag_dict[mcc_tag][low_level_tag] += 1
			
			# if low_level_tag not in data_dict[mcc_tag]['low level tag'].keys():
			# 	data_dict[mcc_tag]['low level tag'].update( {low_level_tag:1} )
			# else:
			# 	data_dict[mcc_tag]['low level tag'][low_level_tag] += 1

			# if high_level_tag not in data_dict[narrative]['high level tag'].keys():
			# 	data_dict[narrative]['high level tag'].update( {high_level_tag:1} )
			# else:
			# 	data_dict[narrative]['high level tag'][high_level_tag] += 1
			
			# if low_level_tag not in data_dict[narrative]['low level tag'].keys():
			# 	data_dict[narrative]['low level tag'].update( {low_level_tag:1} )
			# else:
			# 	data_dict[narrative]['low level tag'][low_level_tag] += 1

	data_dict['high level tags'] = high_level_tag_dict
	data_dict['low level tags'] = low_level_tag_dict

	csvfile.csv_file.close()

	return_dict = {}

	# today = datetime.datetime.now()
	return_dict['high level tags'] = {}
	return_dict['low level tags'] = {}

	for high_or_low_level_tag in data_dict.keys():
		for mcc_tag, data in data_dict[high_or_low_level_tag].iteritems(): # category can be mcc_category or transaction narrative
			if mcc_tag not in return_dict[high_or_low_level_tag].keys():
				return_dict[high_or_low_level_tag].update( {mcc_tag:[]} )
			for high_level_tag in data.keys():
				dict_to_add = {
					'tag': high_level_tag,
					'value': data[high_level_tag]
					}
				return_dict[high_or_low_level_tag][mcc_tag].append( dict_to_add )
			
	return return_dict