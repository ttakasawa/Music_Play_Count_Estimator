import os

# import using:
# from Python.global_imports import *

results_directory = os.path.abspath('../../../Results/')
html_results = os.path.join(results_directory, 'HTML_Generator')
sql_results = os.path.join(results_directory, 'MySQL')
dataset_results = os.path.join(results_directory, 'DatasetSelection')
original_dataset_results = os.path.join(results_directory, 'OriginalDatasetSelection')

code_directory = os.path.abspath('../..')
bash_code = os.path.join(code_directory, 'BASH')
sql_code = os.path.join(code_directory, 'MySQL')
python_code = os.path.join(code_directory, 'Python')
