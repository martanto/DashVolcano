# ************************************************************************************ #
#
# This file performs the following 4 tasks:
# 1) it defines a bunch of constant variables used across the code.
# 2) It loads GVP data from two files, downloaded from the GVP DB:
#    * one that contains volcano data, it needs to be named:
#      GVP_Volcano_List.xlsx
#    * one that contains eruption data, it needs to be named:
#      GVP_Eruption_Results.xlsx
# 3) It creates an index for GEOROC data, based on the content of the
#    folder \GeorocGVPmapping.
#    Due to the sheer size of GEOROC dataset, the GEOROC data
#    is not loaded in memory. Instead, an index linking GVP data and GEOROC
#    data is created. Upon calling, the app will load the necessary GEOROC
#    data.
# 4) It displays in terminal a summary of statistics of the laded data.
#
# HARD CODED DATA WARNING 1: some volcano names are inconsistent between
# both files, this was fixed manually for files downloaded in 2021, if new
# inconsistencies appear in further downloads, this may need either further
# manual fixes, or to be coded once and for all.
#
# HARD CODED DATA WARNING 2: GEOROC volcano names are decided algorithmically;
# for some volcano, the result is not good, and some manual fix is done, to get
# a meaningful name.
#
# Author: F. Oggier
# Last update: Aug 30 2022
#              April 10 2023
# ************************************************************************************* #

import pandas as pd
import numpy as np

import os

import plotly.express as px

file_directory = os.path.dirname(os.path.realpath(__file__))
top_directory = os.path.abspath(os.path.join(file_directory, os.pardir))

# ************************************************************************************#
# constants: rocks
# ************************************************************************************#

# GVP names for rocks
rock_sorted = ['Trachybasalt / Tephrite Basanite', 'Foidite', 'Basalt / Picro-Basalt',
               'Andesite / Basaltic Andesite', 'Trachyandesite / Basaltic Trachyandesite',
               'Phono-tephrite /  Tephri-phonolite', 'Dacite', 'Trachyte / Trachydacite',
               'Phonolite', 'Rhyolite']

# this is where the rock data is
allrocks = ['Major Rock ' + str(i) for i in range(1, 6)] + ['Minor Rock ' + str(i) for i in range(1, 6)]
majorrocks = ['Major Rock ' + str(i) for i in range(1, 6)]

# corresponding shorter names that will be used as column names
rock_col = ['Tephrite Basanite', 'Foidite', 'Basalt', 'Andesite', 'Trachyandesite', 'Tephri-phonolite',
            'Dacite', 'Trachyte', 'Phonolite', 'Rhyolite']

# main rocks
main_rocks = ['Basalt', 'Andesite', 'Dacite', 'Rhyolite']

rock_col_long = main_rocks + \
                ['Weighted Basalt', 'Weighted Andesite', 'Weighted Dacite', 'Weighted Rhyolite'] + \
                ['Felsic', 'Intermediate', 'Mafic']

rock_groups = ['Basalt,Andesite,Dacite,Rhyolite', 'Weighted {Basalt,Andesite,Dacite,Rhyolite}',
               'Felsic,Intermediate,Mafic']
               
# ************************************************************************************#
# constants: VEI, morphology and tectonics
# ************************************************************************************#

VEIcols = ['max VEI', 'mean VEI', 'min VEI']

# Primary Volcano Classification
shapes = ['Shield(s)', 'Stratovolcano(es)', 'Caldera', 'Stratovolcano', 'Submarine',
          'Shield', 'Fissure vent(s)', 'Complex', 'Pyroclastic shield',
          'Pyroclastic cone(s)', 'Pyroclastic cone', 'Volcanic field', 'Caldera(s)',
          'Lava dome(s)', 'Lava cone', 'Compound', 'Maar', 'Crater rows', 'Tuff ring(s)',
          'Explosion crater(s)', 'Complex(es)', 'Tuff cone(s)', 'Fissure vent',
          'Subglacial', 'Cone(s)', 'Maar(s)', 'Lava dome', 'Stratovolcano?']
          
# ************************************************************************************#
# constants: events
# ************************************************************************************#

noteruptive = ['VEI (Explosivity Index)', 'Property damage', 'Fatalities', 'Evacuations',
               'Fauna kill', 'Seismicity (volcanic)', 'Edifice destroyed', 'Thermal anomaly',
               'Earthquakes (undefined)', 'Deformation (inflation)', 'Deformation (deflation)',
               'Earthquake (tectonic)', 'Deformation (undefined)', 'Volcanic tremor']

grouped_events = [['Glow', 'Liquid sulfur', 'Loud audible noises', 'Fumarolic or solfataric', 'Lightning',
                   'Eruption cloud', 'Volcanic smoke', 'Degassing'],
                  ['Directed explosion', 'Lava lake',
                   'Flames', 'Lahar or mudflow', 'Ashfall', 'Lapilli', 'Avalanche'],
                  ['Incandescent ejecta', 'Scoria', 'Lava dome formation', 'Lava fountains'],
                  ['Caldera formation', 'Cinder cone formation', 'Crater formation',
                   'Island formation', 'Fissure formation', 'Spine formation',
                   'Partial collapse at end of eruption'],
                  ['Lava flow(s)', 'Explosion', 'Blocks', 'Bombs', 'Ash Plume',
                   'Tephra', 'Pyroclastic flow', 'Ash'],
                  ['Jokulhaup', 'Phreatic activity', 'Phreatomagmatic eruption', 'Pumice',
                   'Mud', 'Tsunami', 'Water fountain']]

by_severity_events = [
    # Possible to be existed without any magmatic activity
    ['Fumarolic or solfataric', 'Degassing', 'Loud audible noises', 'Water fountain',
     'Mud', 'Flames', 'Glow', 'Liquid sulfur', 'Lahar or mudflow', 'Jokulhaup', 'Volcanic smoke',
     'Phreatic activity', 'Ash', 'AshFall'],
    # Existed due to magmatic eruption (effusive)
    ['Lava lake', 'Lava fountains', 'Cinder cone formation', 'Fissure formation', 'Lava flow(s)',
     'Island formation', 'Lava dome formation', 'Spine formation', 'Incandescent ejecta', 'Blocks'],
    # Existed due to magmatic eruption (explosive)
    ['Pyroclastic flow', 'Phreatomagmatic eruption', 'Explosion', 'Ash Plume', 'Eruption cloud',
     'Lightning', 'Tephra', 'Lapilli', 'Scoria', 'Bombs', 'Pumice'],
    # Extreme volcanic phenomena
    ['Partial collapse at end of eruption', 'Avalanche', 'Tsunami', 'Directed explosion', 'Crater formation',
     'Caldera formation']]
          
# ************************************************************************************#
# constants: chemicals
# ************************************************************************************#

# GEOROC labels
lbls = ['none', 'FEO(WT%)', 'CAO(WT%)', 'FEO(WT%)+CAO(WT%)', 'MGO(WT%)', 'FEO(WT%)+MGO(WT%)',
        'CAO(WT%)+MGO(WT%)', 'FEO(WT%)+CAO(WT%)+MGO(WT%)']
        
# PET DB
lbls2 = ['none', 'FEO', 'CAO', 'FEO+CAO', 'MGO', 'FEO+MGO', 'CAO+MGO', 'FEO+CAO+MGO']

# columns of interest
chemcols = ['ROCK NAME', 'ERUPTION DAY', 'ERUPTION MONTH', 'ERUPTION YEAR',
            'SIO2(WT%)', 'TIO2(WT%)', 'AL2O3(WT%)',
            'FE2O3(WT%)', 'CAO(WT%)', 'MGO(WT%)', 'MNO(WT%)',
            'FEO(WT%)', 'K2O(WT%)', 'NA2O(WT%)', 'P2O5(WT%)',
            'H2O(WT%)', 'H2OP(WT%)', 'H2OM(WT%)']

morechems = ['FEO(WT%)', 'CAO(WT%)', 'MGO(WT%)']

missing_oxides = ['B2O3(WT%)', 'CR2O3(WT%)', 'FEOT(WT%)', 'NIO(WT%)', 'H2OT(WT%)', 'CO2(WT%)',
                  'CO1(WT%)', 'F(WT%)', 'CL(WT%)', 'CL2(WT%)', 'OH(WT%)', 'CH4(WT%)', 'SO2(WT%)',
                  'SO3(WT%)', 'SO4(WT%)', 'S(WT%)'] + ['LOI(WT%)']
                 
oxides = ['SIO2(WT%)', 'TIO2(WT%)', 'B2O3(WT%)', 'AL2O3(WT%)', 'CR2O3(WT%)', 'FE2O3(WT%)', 'FEO(WT%)',
          'FEOT(WT%)', 'CAO(WT%)', 'MGO(WT%)', 'MNO(WT%)', 'NIO(WT%)', 'K2O(WT%)', 'NA2O(WT%)', 'P2O5(WT%)',
          'H2O(WT%)', 'H2OP(WT%)', 'H2OM(WT%)', 'H2OT(WT%)', 'CO2(WT%)', 'CO1(WT%)', 'F(WT%)', 'CL(WT%)',
          'CL2(WT%)', 'OH(WT%)', 'CH4(WT%)', 'SO2(WT%)', 'SO3(WT%)', 'SO4(WT%)', 'S(WT%)'] + ['LOI(WT%)']
                      
colsrock = ['UNIQUE_ID', 'TECTONIC SETTING', 'MATERIAL', 'LOCATION COMMENT']

# GEOROC
colorscale = {'none': 'blue', 'FEO(WT%)': '#FA8072', 'CAO(WT%)': '#E9967A',
              'FEO(WT%)+CAO(WT%)': '#FFA07A', 'MGO(WT%)': '#DC143C',
              'FEO(WT%)+MGO(WT%)': '#FF0000', 'CAO(WT%)+MGO(WT%)': '#B22222',
              'FEO(WT%)+CAO(WT%)+MGO(WT%)': '#8B0000'}

# ************************************************************************************#
# loads GVP eruption data
# ************************************************************************************#
GVP_Eruption_Results = os.path.join(top_directory, 'GVP_Eruption_Results.xlsx')

df = pd.read_excel(GVP_Eruption_Results, engine='openpyxl')
df.columns = list(df[0:1].values[0])
df = df.drop(df.index[[0]])
# removes rows where volcano name = Unknown source
# 600000 = volcano number for Unknown source
df = df[df['Volcano Name'] != 'Unknown Source']
# keeps only confirmed eruptions
df = df[df["Eruption Category"] == 'Confirmed Eruption']
# removes unnamed volcanoes
df = df[df['Volcano Name'] != 'Unnamed']

lst_eruptions = list(df['Eruption Number'].values)

# ************************************************************************************#
# loads GVP volcano data
# ************************************************************************************#
GVP_Volcano_List = os.path.join(top_directory, 'GVP_Volcano_List.xlsx')

gvpxl = pd.read_excel(GVP_Volcano_List, engine='openpyxl')
gvpxl.columns = list(gvpxl[0:1].values[0])
dfv = gvpxl.drop(gvpxl.index[[0]])

# different volcanoes with same name, adds the region to the name
# volcano numbers should not change across different downloads from GVP
rep_names = [353060, 357060, 382001, 342140, 344020, 353120, 261180, 263220, 351021, 224004]
idx = dfv[dfv["Volcano Number"].isin(rep_names)].index
dfv.loc[idx, 'Volcano Name'] = dfv.loc[idx, 'Volcano Name'] + '-' + dfv.loc[idx, 'Subregion']

# this adjusts the names for eruptions as well (in df)
for no in rep_names:
    new_name = dfv[dfv["Volcano Number"] == no]['Volcano Name'].values[0]
    df.loc[df["Volcano Number"] == no, "Volcano Name"] = new_name

# name mismatch, between df and dfv
# this gives df the same names as in dfv, but sadly this is done manually
# so the problem may reappear if new cvs are downloaded (in which case should be automated)
df.loc[df["Volcano Number"] == 371030, "Volcano Name"] = 'Krysuvik'
df.loc[df["Volcano Number"] == 264230, "Volcano Name"] = 'Lewotolo'
df.loc[df["Volcano Number"] == 223020, "Volcano Name"] = 'Nyamuragira'
df.loc[df["Volcano Number"] == 263170, "Volcano Name"] = 'Cereme'
df.loc[df["Volcano Number"] == 382030, "Volcano Name"] = 'San Jorge'
df.loc[df["Volcano Number"] == 231001, "Volcano Name"] = 'Harrat Ash Shamah'
df.loc[df["Volcano Number"] == 357072, "Volcano Name"] = 'Tromen'
df.loc[df["Volcano Number"] == 382081, "Volcano Name"] = 'Picos Volcanic System'
df.loc[df["Volcano Number"] == 371080, "Volcano Name"] = 'Langjokull'
df.loc[df["Volcano Number"] == 221270, "Volcano Name"] = 'Alutu'
df.loc[df["Volcano Number"] == 300083, "Volcano Name"] = 'Vilyuchik'


# function to aggregate VEI data from eruptions (df) with that of volcanoes (dfv)
def retrieve_vinfo_byno(df1, df2):
    # df1 = volcanos (dfv)
    # df2 = eruptions (df)

    veirock_data = []
    # Unknown sources are already removed
    # All volcano numbers from eruption (df) are present in the volcano df (dfv)
    for nno in df2['Volcano Number'].unique():
        datv = [nno]
        # extracts vei
        lstvei = list(df2[df2['Volcano Number'] == nno]['VEI'].values)
        # extracts valid vei
        valid_vei = [float(x) for x in lstvei if type(x) == str]
        # reliability
        rel = len(valid_vei) / len(lstvei)
        datv.extend([len(lstvei), rel])
        if rel > 0:
            # max, mean and min
            datv.extend([max(valid_vei), sum(valid_vei) / len(valid_vei), min(valid_vei)])
        else:
            # uses NaN so the columns of the dataframe are dtype float and not object
            datv.extend([np.NaN, np.NaN, np.NaN])
        # extracts rocks (all rocks, both major and minor)
        rocks_orig = list(df1[df1['Volcano Number'] == nno][allrocks].values[0])
        # '\xa0' is used when the data is not there
        rocks = [r for r in rocks_orig if not (r in ['\xa0', 'No Data (checked)'])]
        ridx = [0] * 10
        for r in rocks:
            ridx[rock_sorted.index(r)] = rocks_orig.index(r) + 1
        # append binary rock composition
        datv.extend([x if x == 0 else 1 for x in ridx])
        # append rock composition
        datv.extend(ridx)
        veirock_data.append(datv)
    return veirock_data


# volcanoes with no eruption data
dfvne = dfv[~dfv['Volcano Name'].isin(df['Volcano Name'])]

# total no of volcanoes
totalgvp = len(dfv.index)

cols = ['Volcano Number', 'eruption no', 'reliability'] + VEIcols + rock_col + ['Weighted ' + r for r in rock_col]
# creates a new dataframe containing VEI data and merges with the volcano dataframe (dfv)
# note that the merging is based on either 'right' or 'left':
# 'left' means that volcanoes are kept even with no eruptive data
# 'right' means we only keep volcanoes with eruptions (thus possibly VEI and eruptive events)
# the only data not considered by taking 'right' is the rock composition
dfv = dfv.merge(pd.DataFrame(np.array(retrieve_vinfo_byno(dfv, df)), columns=cols), on='Volcano Number', how='right')

# country data is not available with eruption data
# after merging using 'right', only countries with eruptive data are kept
lst_countries = sorted(list(dfv['Country'].unique()))
# names of volcanoes are thus only volcanoes with eruptive data if 'right' was chosen during merging
# using GVP data from Oct 2021, there should be 861 volcanoes with eruptive data
lst_names = list(dfv['Volcano Name'].unique())

# replaces string by integers for decision tree
dfv['Primary Volcano Type'] = dfv['Primary Volcano Type'].replace(shapes, [shapes.index(sp) for sp in shapes])

# ***************************************************************************************#
# loads GVP events data
# ***************************************************************************************#

# events are in another sheet
GVP_Eruption_Results = os.path.join(top_directory, 'GVP_Eruption_Results.xlsx')

xl = pd.ExcelFile(GVP_Eruption_Results, engine='openpyxl')
# extracts second sheet
dfev = xl.parse("Events")
dfev.columns = list(dfev[0:1].values[0])
dfev = dfev.drop(dfev.index[[0]])

by_severity_flat = []
for bse in by_severity_events:
    by_severity_flat += bse

severity_colors = {}
# category 1
for i in range(len(px.colors.sequential.gray)):
    severity_colors[by_severity_flat[i]] = px.colors.sequential.gray[i]
severity_colors[by_severity_flat[12]] = px.colors.sequential.Brwnyl[0]
severity_colors[by_severity_flat[13]] = px.colors.sequential.Brwnyl[1]
severity_colors[by_severity_flat[14]] = px.colors.sequential.Brwnyl[2]
# category 2
for i in range(len(px.colors.sequential.solar[2:])):
    severity_colors[by_severity_flat[15 + i]] = px.colors.sequential.solar[i]
# category 3 beginning
for i in range(len(px.colors.sequential.Pinkyl)):
    severity_colors[by_severity_flat[25 + i]] = px.colors.sequential.Pinkyl[i]
# category 3 end and 4
for i in range(len(px.colors.sequential.OrRd)):
    severity_colors[by_severity_flat[32 + i]] = px.colors.sequential.OrRd[i]

# ******************************************************************************************#
# loads Georoc data
# *******************************************************************************************#

# chooses subsets of data in terms of arcs, the data is automatically loaded from the mapping directory
lst_arcs = []

GeorocGVPmapping_dir = os.path.join(top_directory, 'GeorocGVPmapping')

path_for_arcs = os.listdir(GeorocGVPmapping_dir)
for folder in path_for_arcs:
    # lists files in each folder
    GeorocGVPmapping_dir_tmp = os.path.join(GeorocGVPmapping_dir, '{}'.format(folder))

    tmp = os.listdir(GeorocGVPmapping_dir_tmp)
    # adds the path to include directory if file is not empty
    lst_arcs += ['%s' % folder + '/' + f for f in tmp if
                 os.stat(os.path.join(GeorocGVPmapping_dir_tmp, '{}'.format(f))).st_size != 0]

# removes the extension (.txt)
lst_arcs = [f[:-4] for f in lst_arcs]

# reads mapping files, associates volcano names to data file
# and names between GVP (values) and Georoc (keys)
dict_volcano_file = {}
dict_Georoc_GVP = {}

# creates a dictionary which attaches the GVP name for every Georoc name
# and a dictionary which attaches a data file to every Georoc name
for fname in lst_arcs:
    fnameext = fname + '.txt'
        
    # open mapping file
    nameconv_csv = os.path.join(GeorocGVPmapping_dir, '{}'.format(fnameext))
    nameconv = pd.read_csv(nameconv_csv, delimiter=';')

    # Georoc names are from the column GEOROC
    for nn in nameconv['GEOROC']:
        
        # new value for this key
        newvalue = list(nameconv[nameconv['GEOROC'] == nn].values)[0][0]
        # if key not yet in the dictionary
        if not (nn in dict_volcano_file.keys()):
            # if new value (that is GVP name) is already in dictionary
            # this happens when one volcano has data in different arc files
            if newvalue in dict_Georoc_GVP.values():
                # updates Georoc_GVP
                # find old (existing key)
                old_key = [k for k in dict_Georoc_GVP.keys() if dict_Georoc_GVP[k] == newvalue][0]
                # append Georoc rock names
                new_key = old_key + ',' + nn
                # removes duplicates
                clean_key = sorted(list(set(new_key.split(','))))
                new_key = ''
                for kp in clean_key:
                    new_key += kp + ','
                if new_key.endswith(','):
                    new_key = new_key[:-1]
                # add new key/value
                dict_Georoc_GVP[new_key] = dict_Georoc_GVP[old_key]
                # removes the old key (only if different, otherwise this deletes the record)
                if new_key != old_key:
                    del dict_Georoc_GVP[old_key]
                    # then updates volcano_file
                    # if no new file name, just update the key
                    dict_volcano_file[new_key] = dict_volcano_file[old_key]
                    if not (fname + '.csv' in dict_volcano_file[new_key]):
                        # if new file name
                        dict_volcano_file[new_key].append(fname + '.csv')
                    del dict_volcano_file[old_key]
                # when both keys are the same (new clause)   
                else:
                    dict_volcano_file[new_key].append(fname + '.csv')      
            else:
                # just add new key and new value
                dict_volcano_file[nn] = [fname + '.csv']
                dict_Georoc_GVP[nn] = newvalue
        else:
            if newvalue in dict_Georoc_GVP.values():
                # GVP data appears in more than one file, so update the file paths
                dict_volcano_file[nn].append(fname + '.csv')
            else:
                print("double key", nn)
                
# between GVP (keys) and Georoc (value)
dict_GVP_Georoc = {v: k for k, v in dict_Georoc_GVP.items()}

# lists all names for one GEOROC site
longnames = [x for x in dict_Georoc_GVP.keys() if len(x) >= 80 and len(x.split(',')) >= 2]

# splits every name to remove -
longnames2 = [x.replace('-', ',').split(',') for x in longnames]

# removes spaces
longnames3 = []
mostcommon = []
for x in longnames2:
    longstrip = [y.strip() for y in x]
    longnames3.append(longstrip)
    
    # counts iterations
    cnt = [longstrip.count(x) for x in longstrip]
    maxcnt = max(cnt)
    # finds the shortest name
    smallword = min(longstrip, key=len)
    # finds most common word
    if maxcnt > 1:
        # 
        if 'GRANDE DECOUVERTE' in longstrip:
            mostcommon.append('SOUFRIERE GUADELOUPE')
        else:
            mostcommonword = longstrip[cnt.index(max(cnt))]
            mostcommon.append(mostcommonword)
    # checks if smallest name is included into at list two others
    elif sum([smallword in x for x in longstrip]) >= 2:
        mostcommon.append(smallword)
    # uses the term containing MOUNT
    elif any(['MOUNT' in x for x in longstrip]): 
        mostcommon.append([x for x in longstrip if 'MOUNT' in x][0])
    # some particular cases
    elif 'VULSINI (VULSINI VOLCANIC DISTRICT)' in longstrip:    
        mostcommon.append('VULSINI VOLCANIC DISTRICT')
    elif 'ZEALANDIA BANK' in longstrip:
        mostcommon.append('ZEALANDIA BANK')
    elif 'SUMISUJIMA' in longstrip:
        mostcommon.append('SUMISUJIMA')    
    
    else:
        print('missing name for', [y.strip() for y in x])
        mostcommon.append(smallword)

dict_Georoc_sl = {}
for x, y in zip(longnames, mostcommon):
    # for exceptions where names need modifying
    dict_Georoc_sl[y.strip() + ' (' + str(len(x.split(','))) + ' SITES)'] = x

dict_Georoc_ls = {}
for shrt, lng in dict_Georoc_sl.items():
    dict_Georoc_ls[lng] = shrt
                
# extract names to be in drop-down menu
# only those in the mapping files (that is attached to GVP data) are used
grnames = list(dict_Georoc_GVP.keys())
# this is where the aggregated name can be printed
# print([x for x in grnames if 'TONGARIRO' in x])
# changes exceptions
for kk, value in zip(dict_Georoc_sl.keys(), dict_Georoc_sl.values()):
    grnames[grnames.index(value)] = kk

# alphabetical sorting
grnames = sorted(grnames)

# displays at loading
print('#####################################')
print('#                                   #')
print('# Basic Statistics                  #')
print('#                                   #')
print('#####################################')


print('Number of GVP volcanoes: ', totalgvp)
print('Number of GVP eruptions (confirmed): ', len(df.index))
print('Number of volcanoes with known eruption(s): ', len(dfv.index))

# prints the number of GEOROC names
print('Number of GEOROC volcanoes: ', len(grnames))

#
witheruptiondata = len(df[df['Volcano Name'].isin(list(dict_GVP_Georoc.keys()))]['Volcano Name'].unique())

print('Number of GEOROC volcanoes with eruption data: ', witheruptiondata)
