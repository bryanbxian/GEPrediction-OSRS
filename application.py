from __future__ import absolute_import, division, print_function, unicode_literals
from preprocessing import prepare_data, regression_f_test, recursive_feature_elim, item_selection
from models import univariate_data, create_time_steps, show_plot, multivariate_data, multi_step_plot
import tensorflow as tf
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import json

TRAIN_SPLIT = 0
tf.random.set_seed(13)
STEP = 1

def apply_univariate(df, item_to_predict, model, item_std, item_mean, past_history=30):

	df_newest_values = df.tail(past_history)[item_to_predict].values
	reshaped_values = np.reshape(df_newest_values, (past_history, 1))
	formatted_values = np.array([reshaped_values])

	#### Unnormalizing the data (so we can see actual prices in GP)
	def unnormalized(val):
		return (val*item_std) + item_mean

	print("PREDICTION: {}".format(unnormalized(model.predict(formatted_values)[0])))
	
	# TODO: write predictions to file, and later get matching real price

def apply_multivariate_single_step(df, item_to_predict, model, item_std, item_mean, past_history=30):

	df_newest_values = df.tail(past_history).values
	formatted_values = np.array([df_newest_values])

	#### Unnormalizing the data (so we can see actual prices in GP)
	def unnormalized(val):
		return (val*item_std) + item_mean

	print("PREDICTION: {}".format(unnormalized(model.predict(formatted_values)[0])))

def apply_multivariate_multi_step(df, item_to_predict, model, item_std, item_mean, future_target=5, past_history=30):
	df_newest_values = df.tail(past_history).values
	formatted_values = np.array([df_newest_values])

	#### Unnormalizing the data (so we can see actual prices in GP)
	def unnormalized(val):
		return (val*item_std) + item_mean

	print("PREDICTION: {}".format(unnormalized(model.predict(formatted_values)[0])))

def main():
	model_types = ['uni', 'multiS', 'multiM']
	items_to_predict = ['Old_school_bond', 'Rune_platebody', 'Adamant_platebody', 'Amulet_of_power']
	
	# SELECT ITEMS
	items_selected = item_selection()

	for item_to_predict in items_to_predict:
		# FEATURE EXTRACTION
		preprocessed_df = prepare_data(item_to_predict, items_selected, DATA_FOLDER="data/newest/")

		# FEATURE SELECTION & NORMALIZATION
		if not os.path.isfile('models/features/{}_{}_features.txt'.format(item_to_predict, model_types[0])):
			print ("Model for {} hasn't been created, please run models.py first.".format(item_to_predict))
			return
		specific_feature_list = []
		with open('models/features/{}_{}_features.txt'.format(item_to_predict, model_types[0]), 'r') as filehandle:
			specific_feature_list = json.load(filehandle)
		selected_df, pred_std, pred_mean = regression_f_test(preprocessed_df, item_to_predict, \
			specific_features=specific_feature_list, number_of_features=len(specific_feature_list)-1)

		for model_type in model_types:
			# LOADING AND APPLYING MODEL
			loaded_model = tf.keras.models.load_model('models/{}_{}_model.h5'.format(item_to_predict, model_type))

			if (model_type == 'uni'):
				apply_univariate(selected_df, item_to_predict, loaded_model, pred_std, pred_mean)
			elif (model_type == 'multiS'):
				apply_multivariate_single_step(selected_df, item_to_predict, loaded_model, pred_std, pred_mean)
			elif (model_type == 'multiM'):
				apply_multivariate_multi_step(selected_df, item_to_predict, loaded_model, pred_std, pred_mean)
			else:
				print("Unrecognized model type.")

if __name__ == "__main__":
	main()