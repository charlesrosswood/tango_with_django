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
import csv
import json

from rango.models import CSVfiles
# from rango import analysis 
# from rango.models import SiteUserForm, WallPostForm
# from rango.forms import *

def binning_data( dataset, num_of_bins ):
	"""
	This function will take an x-y dataset and returned the binned version
	of the dataset, e.g. 
	an array of [ [x-max value of bin, number of occurances in bin],... ]
	"""
	array = []

	

	return array

def binned_amounts( csvfile ):
	"""
	This function does no analysis, it just groups transactions that occur
	in a particular category together, it does not generate a histogram.
	"""
	csvfile.csv_file.open(mode='rb') # opening the file for reading ans such like
	csv_list = csvfile.csv_file.read().split('\n')

	data_dict = {}

	for row in csv_list[1:]:
		if row != '' and row != '\n':
			row = row.split('"')
			new_row = []
			for i in xrange(len(row)):
				if i%2 == 0: # then even element
					temp_to_add = row[i].split(',')
					temp_to_add = [element for element in temp_to_add if (element.strip() != '' and element.strip() != ',')]
					new_row.extend( temp_to_add )
				else: # then odd element
					new_row.extend( [str(row[i])] )

			category = new_row[4].lower()
			if category not in data_dict.keys():
				data_dict.update( {category:[float(new_row[3])]} )
				data_dict.update( {'totals':[float(new_row[3])]} )
			else:
				data_dict[ category ].append(float(new_row[3]))
				data_dict[ 'totals' ].append(float(new_row[3]))

	csvfile.csv_file.close()

	return_dict = {}

	for category, data in data_dict.iteritems():
		binned_data = []

		min_data = min(data)
		max_data = max(data)
		data_range = abs(max_data - min_data)
		bin_size = data_range / 30.0

		# bin_min = min_data
		# bin_max = bin_min + bin_size

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
				if (datum >= bin_mins[i]) and (datum  < bin_maxs[i]):
					frequencies[i] += 1 
					success = True
			if success == False:
				print "Failed to bin data: ", datum

		for i in xrange(len(bin_maxs)):
			xy_dataset.append( [ bin_maxs[i], frequencies[i] ] )

		return_dict.update( {category:xy_dataset} )

	return return_dict