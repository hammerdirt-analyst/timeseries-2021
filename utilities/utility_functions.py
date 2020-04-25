"""
Utitlity functions for summarizing and analyzing data from the litter database. Used with a jupyter notebook.

Creates folder structures, groups data, creates graphs and outputs JSON format data.

See the repo @hammerdirt/three_year_final for the accompanying notebooks and intended use.

Contact roger@hammerdirt.ch or @hammerdirt

"""
import os
import json
import csv
import requests
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

idx = pd.IndexSlice

def make_directory(needed, here):
    """Makes a directory with names from a list.
    """
    for folder in needed:
        place = here +"/"+ folder
        os.mkdir(place)
def check_for_folders(folders, here):
    """Checks the names of the folder list against the currrent directory. If the result is not
    an empty set then the required names are added to the directory structure.
    """
    current_dir = os.listdir()
    curr_dir_set = set(current_dir)
    folder_set = set(folders)
    needed = folder_set.difference(curr_dir_set)
    if needed:
        make_directory(needed, here)
        print("Added folders to the local working directory")
    else:
        print("Directory already in place")
def make_project_folder(here, project_name):
    """Makes a subdirectory with the specified 'project_name'
    in the directory specified by 'here'.

    Used in all notebooks that read or write data.
    """
    project_folder = '{}/{}'.format(here, project_name)
    if os.path.isdir(project_folder):
        project_folder = project_folder
    else:
        os.mkdir(project_folder)
    return project_folder

def make_folders(folders, here):
    """Takes an array of directory names and one directory. Returns
    a dcitionary of named directories ie.. {'name':'a/file/path/'}.

    Used in all notebooks that read or write data.
    """
    my_folders = {}
    for folder in folders:
        place = here +"/"+ folder
        my_folders[folder] = place
    return my_folders
def get_the_data(end_points):
    """Takes an array of 2d tuples or arrays ('name', 'url') and
    returns a dictionary of named data objects.

    Used in all notebooks that read or write data.
    """
    data = {}
    for pair in end_points:
        data[pair[0]] = requests.get(pair[1])
    return data
def write_the_data(aDict, here):
    """Writes the response objects (a JSON object) to the provided location.

    Used in notebooks that make an api call
    """
    file_names = list(aDict.keys())
    outPut = []
    for name in file_names:
        file_name = here + '/data/'+name+ ".json"
        outPut.append(file_name)
        with open(file_name, 'w') as outfile:
            json.dump(aDict[name].json(), outfile)

    print(outPut)
def put_the_data_to_local(end_points, here):
    """Gets the data from the provided URL and writes it to the provided location.

    Used in notebooks that make an api call
    """
    the_dict = get_the_data(end_points)
    write_the_data(the_dict, here)
def json_file_get(this_path):
    """Reads the local JSON in from the provided file path.

    Used in all notebooks that read in JSON data.
    """
    with open(this_path, 'r') as infile:
        data = json.load(infile)
        return data
def unpack_survey_results(survey_results):
    """Unpacks the surveys-results api-endpoint and adds the location name to each result dict.

    Used in notebooks that make an api call to 'https://mwshovel.pythonanywhere.com/api/surveys/daily-totals/code-totals/swiss/'
    """
    unpacked = []
    for location_data in survey_results:
        location = location_data['location']
        for each_dict in location_data['dailyTotals']:
            each_dict['location']=location
            unpacked.append(each_dict)
    return unpacked
def unpack_daily_totals(survey_results):
    """Unpacks the daily-totals api-endpoint. Returns an array of dictionaries. One dictionary for each day.

    Used in notebooks that make an api call to 'https://mwshovel.pythonanywhere.com/api/surveys/daily-totals/swiss/'
    """
    unpacked = []
    for location_data in survey_results:
        location = location_data['location']
        for each_list in location_data['results']:
            day_total = {}
            day_total['location']=location
            day_total['date']=each_list[0]
            day_total['total']=each_list[1]
            unpacked.append(day_total)
    return unpacked
def json_file_to_csv(the_jsons, prefix):
    """Retrieves the specified JSON files and converts to .csv. Takes an array of 2d tuples:
    ('desired_file_name','path/to/json') and a prefix directory ie.. '/this/is/the/directory/'

    Used in any notebook that is saving JSON to .csv
    """
    for obj in the_jsons:
        the_dict = json_file_get(obj[1])
        keys = the_dict[0].keys()
        file_name = '{}/{}.csv'.format(prefix, obj[0])
        with open(file_name, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(the_dict)
def dict_to_csv(the_dict, a_name, prefix):
    """Converts an array of dicts to a .csv file.

    Used to convert 'unpack_survey_results' and 'unpacked_daily_totals' to .csv
    """
    keys = the_dict[0].keys()
    file_name = '{}/{}.csv'.format(prefix, a_name)
    with open(file_name, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(the_dict)
def get_data_by_date_range(a_df, date_range):
    """Slices a dataframe by the given data range.

    Used in notebooks using pandas with a column called py_date
    """
    this_data = a_df[a_df['py_date'].between(date_range[0], date_range[1])]
    return this_data
def get_code_totals_from_date_range(a_df):
    return a_df.groupby(['code'])["quantity"].aggregate(np.sum).sort_values(ascending=False)
def get_tuples_from_series(a_df):
    """Makes a 2d tuple from the index value and column value of a
    dataframe of series with one column and an index
    """
    return list(zip(a_df.index, a_df))
def get_the_rest(a_list, total_quant):
    """Returns the difference between some given value and the sum of an array of 2d tuples.
    """
    some_number = 0
    for x in a_list:
        some_number += x[1]
    return total_quant - some_number

def start_end_date(start, end, date_format):
    """Returns a tuple datetime objects (start, end) from string dates using the given format.
    """
    return ((datetime.datetime.strptime(start, date_format), datetime.datetime.strptime(end, date_format)))
def a_color_map(color_map_name='PuBuGn', look_up_table_entries=100):
    # provide a color map https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
    return plt.cm.get_cmap(color_map_name,look_up_table_entries)
def legend_style(t_fs=14, fs=11, b_box_a=(1,1.02), loc='upper left', title=None):
    return({
        "title_fontsize":t_fs,
        "fontsize":fs,
        "bbox_to_anchor":b_box_a,
        "loc":loc,
        "title":title
    })
def legend_t_align(title="A legend title", align="left"):
    return {'title':title, 'align':align}
def axis_label_props(label="An axis label", ff='sans-serif', pad=15, color='black', sz=12, ha='left', x=0):
    return({
        'fontfamily':ff,
        'lablepad':pad,
        'color':color,
        'size':sz,
        'label':label,
        'ha':ha,
        'x':x
    })
def adjust_subplot_params(left=0.125, right=0.9, bottom=0.1,
                            top=0.87, wspace=0.2, hspace=0.2):
    return ({"top":top, "left":left, "right":right, "bottom":bottom,
            "wspace":wspace, "hspace":hspace})
def file_params(folder, file_name, file_suffix):
    return {'folder':folder, 'file_name':file_name, 'file_suffix':file_suffix}
def save_the_figure(folder='a/file/path/', file_name='a_file', file_suffix=[]):
    for ext in file_suffix:
        save_me = '{}/{}{}'.format(folder, file_name, ext)
        if ext == '.jpeg':
            plt.savefig(save_me, bbox_inches="tight", dpi=300)
        else:
            plt.savefig(save_me, bbox_inches="tight")
