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
    """
    Makes a directory with names from a list.
    """
    for folder in needed:
        place = here +"/"+ folder
        os.mkdir(place)

def check_for_folders(folders, here):
    """
    Checks the names of the folder list against the currrent directory. If the result is not
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

def make_folders(folders, here):
    """
    A dcitionary for locating folders in the directory.
    """
    my_folders = {}
    for folder in folders:
        place = here +"/"+ folder
        my_folders[folder] = place
    return my_folders
def get_the_data(end_points):
    """
    Takes an api url and returns a response object
    """
    data = {}
    for pair in end_points:
        data[pair[0]] = requests.get(pair[1])
    return data
def write_the_data(aDict, here):
    """
    Writes the response objects to local in JSON
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
    """
    Gets the data and writes it to a local JSON file
    """
    the_dict = get_the_data(end_points)
    write_the_data(the_dict, here)
def json_file_get(this_path):
    """
    Reads the local JSON in
    """
    with open(this_path, 'r') as infile:
        data = json.load(infile)
        return data
def unpack_survey_results(survey_results):
    unpacked = []
    for location_data in survey_results:
        location = location_data['location']
        for each_dict in location_data['dailyTotals']:
            each_dict['location']=location
            unpacked.append(each_dict)
    return unpacked
def json_file_to_csv(the_jsons, prefix):
    for obj in the_jsons:
        the_dict = json_file_get(obj[1])
        keys = the_dict[0].keys()
        file_name = '{}/{}.csv'.format(prefix, obj[0])
        with open(file_name, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(the_dict)
def dict_to_csv(the_dict, a_name, prefix):
    keys = the_dict[0].keys()
    file_name = '{}/{}.csv'.format(prefix, a_name)
    with open(file_name, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(the_dict)

def getIndexValues(aDf, anInt):
    return aDf.index.get_level_values(anInt).unique()
def getSummaryByKeyValue(aDf, anInt):
    aList = list(getIndexValues(aDf, anInt))
    theSummaries = {}
    for key in aList:
        aSummary = aDf.loc[key].describe().to_dict()
        theSummaries.update({key:aSummary["pcs_m"]})
    return aList, theSummaries
def convertStringToDate(aTuple):
    convertedDates = []
    for pair in aTuple:
        newPair = (datetime.datetime.strptime(pair[0], "%Y-%m-%d"), datetime.datetime.strptime(pair[1], "%Y-%m-%d"))
        convertedDates.append(newPair)
    return convertedDates
def getSummaryByKeyValueMulti(aDf, anInt):
    aList = list(getIndexValues(aDf, anInt))
    theSummaries = {}
    for key in aList:
        aSummary = aDf.loc[idx[:,key,:,:], :].describe().to_dict()
        theSummaries.update({key:aSummary["pcs_m"]})
    return aList, theSummaries
def makeListOfBars(aDict, aKey):
    aList = []
    theKeys = aDict.keys()
    for key in theKeys:
        values = aDict[key][aKey]
        aList.append([key,values])
    return aList
def sortInReverse(the_data, anIndex):
    the_data_sorted = sorted(the_data, key=lambda row: row[anIndex], reverse=True)
    return the_data_sorted
def percent_of_total_and_frequency(quantDict, freqDict, total, num_samps):
    new_dict = {}
    for k,v in quantDict.items():
        freq = freqDict[k]
        new_dict.update({k:[v,v/total,freq,freq/num_samps]})
    return new_dict
def quantity_frequency(quant, freq, codes):
    qVsF = []
    for code in codes:
        qVsF.append([code, quant[code], freq[code]])
    return qVsF
def get_data_by_date_range(a_df, date_range):
    this_data = a_df[a_df['py_date'].between(date_range[0], date_range[1])]
    return this_data
def get_code_totals_from_date_range(a_df):
    return a_df.groupby(['code_id'])["quantity"].aggregate(np.sum).sort_values(ascending=False)
def get_code_frequency_from_date_range(data):
    return a_df.groupby(["code_id"])['code_id'].count().sort_values(ascending=False)
def get_num_samps(a_df):
    return a_df[['location_id', 'py_date','quantity']].groupby(['location_id', 'py_date']).sum().count().values[0]
def get_tuples_from_series(a_df):
    return list(zip(a_df.index, a_df))
def get_the_rest(a_list, total_quant):
    some_number = 0
    for x in a_list:
        some_number += x[1]
    return total_quant - some_number
def make_blocks(a_df, percent, end_start, total_quant, code_dict, top_ten=False):
    code_totals = get_code_totals_from_date_range(a_df)
    code_totals_tuple = get_tuples_from_series(code_totals)
    print(code_totals_tuple)
    code_greater_than = [
        (x[0],x[1],code_dict[x[0]][1])
        for i,x in enumerate(code_totals_tuple)
        if x[1] >= percent
    ]
    the_rest = get_the_rest(code_greater_than, total_quant)
    code_greater_than.append(("Other", the_rest,"*All other objects"))
    return code_greater_than
def start_end_date(start, end, date_format):
    return ((datetime.datetime.strptime(start, date_format), datetime.datetime.strptime(end, date_format)))
def a_color_map(color_map_name='PuBuGn', look_up_table_entries=100):
    # provide a color map https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
    return plt.cm.get_cmap(color_map_name,look_up_table_entries)
def title_styles(fs=12, ff='sans-serif', fw='normal',va='baseline', ha='center'):
    """For sup title use the following values:

    ff='sans-serif', fw='roman', fs=14, ha='left', va='baseline'
    """
    return ({
        'fontsize': fs,
        'fontfamily':ff,
        'fontweight': fw,
        'verticalalignment': va,
        'horizontalalignment': ha,
    })
def title_position(x=0, pad=15):
    """For sup title use the following values:

    x=0.13, pad=0
    """
    return({
        'x':x,
        'pad':pad,
    })
def title_content_color(content="A title", color="black"):
    return {'label':content, 'color':color}
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
def save_the_figure(folder='a/file/path/', file_name='a_file', file_suffix='.svg'):
    save_me = '{}/{}{}'.format(folder, file_name, file_suffix)
    plt.savefig(save_me, bbox_inches="tight")
def make_stacked_blocks(the_data, ax, color):
    the_bottom = 0
    for i,block in enumerate(the_data):
            if i == 0:
                ax.bar(1, block[1], color=next(color), edgecolor="white", alpha=0.9,
                        label="{}: {:,}".format(block[2],block[1]))
                the_bottom += block[1]
            else:
                ax.bar(1, block[1], color=next(color), edgecolor="white",alpha=0.9,
                       bottom=the_bottom,
                       label="{}: {:,}".format(block[2],block[1]))
                the_bottom += block[1]
