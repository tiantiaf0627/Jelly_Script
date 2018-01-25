import json
import csv
import sys
import datetime
import os
import numpy as np
import matplotlib.pyplot as plt

def get_user_date_folder(username_array):

	date_array = []

	for userNameFolder in username_array:
		date_folders = os.listdir(''.join(["../data/", userNameFolder]))
		date_folders.sort()

		temp_date_folders = []

		for dateFolder in date_folders:
			if "2018-" in dateFolder:
				temp_date_folders.append(dateFolder)
		date_array.append(temp_date_folders)
	print(date_array)

	return date_array

def get_user_folder():
	username_folder_list = os.listdir('../data')
	username_folder_list.sort()

	username_array = []

	for userNameFolder in username_folder_list:
		if len(userNameFolder) < 5:
			username_array.append(userNameFolder)
			print(userNameFolder)
	return username_array

def get_files_per_user(username_array, date_array):
	username_folder_index = 0
	file_array = []
	for userNameFolder in username_array:

		files_per_user = []

		print(userNameFolder)
		for dateFolder in date_array[username_folder_index]:
			date_folder_abs = ''.join(["../data/", userNameFolder + "/", dateFolder])

			number_of_files_per_day = len(os.listdir(date_folder_abs))
			temp_file_array = os.listdir(date_folder_abs)
			temp_file_array.sort()
			if 50 < number_of_files_per_day < 500:
				files_per_user.append(temp_file_array)

		file_array.append(files_per_user)

		username_folder_index = username_folder_index + 1;

	return file_array

def get_all_files_per_user(username_array, date_array):
	username_folder_index = 0
	file_array = []
	for userNameFolder in username_array:

		files_per_user = []

		print(userNameFolder)
		for dateFolder in date_array[username_folder_index]:
			date_folder_abs = ''.join(["../data/", userNameFolder + "/", dateFolder])
			temp_file_array = os.listdir(date_folder_abs)
			temp_file_array.sort()
			files_per_user.append(temp_file_array)

		file_array.append(files_per_user)

		username_folder_index = username_folder_index + 1;

	return file_array

def get_files_stat(file_array):

	average_recording_array = []
	std_recording_array = []
	username_folder_index = 0

	for user_idx in range(len(file_array)):

		number_of_files_per_user = 0
		number_of_days_per_user = 0
		number_of_files_array = []

		for date_idx in range(len(file_array[user_idx])):
			number_of_files_per_day = len(file_array[user_idx][date_idx])
			if 50 < number_of_files_per_day < 500:
				number_of_files_per_user = number_of_files_per_user + number_of_files_per_day
				number_of_days_per_user = number_of_days_per_user + 1
				number_of_files_array = np.append(number_of_files_array, number_of_files_per_day)

		average_recording_array = np.append(average_recording_array, np.mean(number_of_files_array, dtype=int))
		std_recording_array = np.append(std_recording_array, np.std(number_of_files_array, dtype=int))
		print(number_of_files_array)
		username_folder_index = username_folder_index + 1


	file_stat = [average_recording_array, std_recording_array]
	print(file_stat)
	return file_stat

def plot_files_stat(username_array, file_stat):

	plt.errorbar(range(len(username_array)), file_stat[0], yerr=file_stat[1], fmt='o',
			 markeredgewidth=2, elinewidth=2, capsize=5)

	plt.xticks(range(len(username_array)), username_array)

	plt.xlabel('Participant ID', fontsize=12)
	plt.ylabel('Number Of Recordings', fontsize=12)
	plt.show()

def get_file_distribution_per_user(files_array):
	file_distribution = []
	for jelly_idx in range(len(files_array)):
		file_distribution_per_user = np.zeros(24)
		for date_idx in range(len(files_array[jelly_idx])):
			for file_idx in range(len(files_array[jelly_idx][date_idx])):
				timestamp = datetime.datetime.fromtimestamp(float(files_array[jelly_idx][date_idx][file_idx][11:24]) / 1000)
				hour = timestamp.hour
				file_distribution_per_user[hour] = file_distribution_per_user[hour] + 1
		file_distribution.append(file_distribution_per_user/len(files_array[jelly_idx]))
		print(file_distribution_per_user)
	return file_distribution

def plot_file_distribution(jelly_id, file_distribution):
	number_of_jelly = int(len(jelly_id))
	f, ax_arr = plt.subplots(int(number_of_jelly/2), int(number_of_jelly/2))

	plt.setp(ax_arr, xticks=range(8, 21, 4),
			 yticks=[0, 10, 20, 30, 40])

	plt.subplots_adjust(hspace=0.5)

	colors = ['r', 'g', 'b', 'k']

	for jelly_idx in range(len(file_distribution)):
		ax_arr[int(jelly_idx / 2), int(jelly_idx % 2)].\
			plot(range(24)[8:21], file_distribution[jelly_idx][8:21], c=colors[jelly_idx])
		ax_arr[int(jelly_idx / 2), int(jelly_idx % 2)].\
			set_title('Participant {}'.format(jelly_id[jelly_idx]))
		ax_arr[int(jelly_idx / 2), int(jelly_idx % 2)]. \
			set_ylabel('Number of Recordings')
		ax_arr[int(jelly_idx / 2), int(jelly_idx % 2)]. \
			set_xlabel('Hour of the Day')
		ax_arr[int(jelly_idx / 2), int(jelly_idx % 2)]. \
			set_xlim([8, 20])
		ax_arr[int(jelly_idx / 2), int(jelly_idx % 2)]. \
			set_ylim([0, 40])
	plt.show()

def filter_file_distribution(file_distribution):

	filtered_file_distribution = []

	for jelly_idx in range(len(file_distribution)):
		filter_file_distribution_per_user = np.zeros(24)
		for hour_idx in range(len(file_distribution[jelly_idx])):
			if hour_idx == 0:
				filter_file_distribution_per_user[hour_idx] = int((file_distribution[jelly_idx][hour_idx] +
																   file_distribution[jelly_idx][hour_idx+1]) / 2)
			elif hour_idx == 23:
				filter_file_distribution_per_user[hour_idx] = int((file_distribution[jelly_idx][hour_idx] +
																		file_distribution[jelly_idx][hour_idx - 1])/2)
			else:
				filter_file_distribution_per_user[hour_idx] = int((file_distribution[jelly_idx][hour_idx] +
																		file_distribution[jelly_idx][hour_idx - 1] +
																		file_distribution[jelly_idx][hour_idx + 1]) / 3)
		filtered_file_distribution.append(filter_file_distribution_per_user)
	print(filtered_file_distribution)
	return filtered_file_distribution

if __name__=='__main__':
	# Get name and date
	jellyID = get_user_folder()
	dateArray = get_user_date_folder(jellyID)

	# Get file array
	filesArray = get_files_per_user(jellyID, dateArray)

	# Get file stat
	fileStat = get_files_stat(filesArray)

	# Plot the File Stat
	plot_files_stat(jellyID, fileStat)

	# Get the File Distribution Per hour
	fileDistribution = get_file_distribution_per_user(filesArray)

	fileDistribution = filter_file_distribution(fileDistribution)

	# Plot the Recordings per Hour/Distribution
	plot_file_distribution(jellyID, fileDistribution)

	# Write File
















