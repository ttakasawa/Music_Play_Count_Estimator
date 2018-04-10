import csv
import os

# import using:
# from Code.Python.global_imports import *

# Results Directories
results_directory = os.path.abspath('../../../Results/')
html_results = os.path.join(results_directory, 'HTML_Generator')
sql_results = os.path.join(results_directory, 'MySQL')
dataset_results = os.path.join(results_directory, 'DatasetSelection')
json_extraction_results = os.path.join(results_directory, 'json_extraction')

original_dataset_results = os.path.join(results_directory, 'OriginalDatasetSelection')

# Code Directories
code_directory = os.path.abspath('../..')
bash_code = os.path.join(code_directory, 'BASH')
sql_code = os.path.join(code_directory, 'MySQL')
python_code = os.path.join(code_directory, 'Python')

# Data Directories
data_directory = os.path.abspath('../../../Data/')
html_data = os.path.join(data_directory, 'HTML_Generator')

results_directories = [results_directory, html_results, sql_results, dataset_results, json_extraction_results]
code_directories = [code_directory, bash_code, sql_code, python_code]
data_directories = [data_directory, html_data]


def EnsureDirectoriesExist():
    for dirlist in [results_directories, code_directories, data_directories]:
        for dir in dirlist:
            if not os.path.exists(dir):
                os.makedirs(dir)


def csv_open(path, delim=','):
    with open(path, 'r') as file:
        return list(csv.reader(file, delimiter=delim))


def write_csv_data(data, file_path, delim=","):
    with open(file_path, 'w') as outfile:
        writer = csv.writer(outfile, delimiter=delim)
        for item in data:
            writer.writerow(item)


EnsureDirectoriesExist()
