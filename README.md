# DashVolcano
This is a project about volcano data analytics.

DashVolcano is an app, to be downloaded and ran locally.
It create a visual interface, to jointly display volcanic data from two major databases:
(1) the Geochemistry of Rocks of the Oceans and  Continents (GEOROC, https://georoc.eu/georoc/new-start.asp) of the Digital Geochemistry Infrastructure (DIGIS), and 
(2) the Volcanoes of the World (VOTW) of the Smithsonian’s Global Volcanism Program (GVP, https://volcano.si.edu/). 

Set-up and Directory structure
--

To install DashVolcano on your computer, the 3 folders and 2 excel files should be downloaded into one local folder, let us call it MyNewFolder. 
The resulting directory structure will thus be: 

MyNewFolder, containing the 3 folders (DashVolcano.1.0., GeorocGVPmapping, GeorocDataset) and the 2 excel files (GVP_Eruption_Results.xlsx, GVP_Volcano_List.xlsx).

DashVolcano is written in python, you thus need python3 installed on your computer
(DashVolcano was tested with: Python 3.7.4 on Ubuntu 20.04.4 LTS, and Python 3.8.3 on Mac OS Monterey version 12.5.1). 

It is suggested to set up a python virtual environment, to make sure the dependencies are consistent, and to avoid conflicting with possible other existing python set-ups. To do so, using the command line in a terminal window, go into the folder DashVolcano.1.0:

> $ cd DashVolcano.1.0.

and create the virtual environment: 

> $ python3 -m venv venv

If successful, you will see a new folder named venv inside the folder DashVolcano.1.0.

Once the virtual python environment is created (this is done only once), it needs to be activated (this is needed every time the terminal window is opened again):

> DashVolcano.1.0$ source venv/bin/activate

You can tell whether the environment is activated by checking before your computer's name:

> (venv) yourname@yourcomputername: 

To start the app, type the following command:

> python run.py

Some packages are needed to run the app. If a package is missing, the app will not start, instead an error message will appear, giving the name of the package that is not found.

To install a missing package,the synthax is as follows:

> (venv) $ python -m pip install dash==2.0.0

The packages that are likely to be needed are:
* dash==2.0.0
* dash-bootstrap-components==1.0.0
* dash-core-components==2.0.0
* dash-html-components==2.0.0
* geopandas==0.10.2
* numpy==1.20.3
* openpyxl==3.0.7
* pandas==1.3.5
* plotly==5.3.1

Downloading the GVP and GEOROC datasets
--

The GVP data is provided into two excel files: GVP_Eruption_Results.xlsx, GVP_Volcano_List.xlsx. 
This data was downloaded from https://volcano.si.edu/ in 2021. GVP data is regularly updated. It is possible to download more recent datasets to update those provided, but the filenames and type (xlsx), as well as their location in the folder structure, have to remain the same. It is also advised to download both volcano and eruption files around the same period, otherwise volcano names may be present in one file and not in the other, which will cause errors when running the app.

The folder structure to store GEOROC datasets is provided, but the datasets themselves should be downloaded directly from https://georoc.eu/georoc/new-start.asp, where they are grouped by tectonic settings. 

**Example.** In the folder GeorocDataset, there is a folder named Complex_Volcanic_Settings_comp. It currently contains a single example file, ETNA_SICILY.csv. On the left menu of  https://georoc.eu/georoc/new-start.asp, choose Locations, then Complex Volcanic Settings,then Download complete precompiled dataset. You will obtain 7 files: CENTRAL-NEW_YORK_KIMBERLITES.csv, OAXACA_MEXICO.csv, ETNA_SICILY.csv, POTIGUAR_BASIN.csv, FINGER_LAKES_FIELD_NEW_YORK.csv, USTICA_ISLAND_ITALY.csv, HYBLEAN_OR_IBLEAN_PLATEAU_SICILY.csv. Each of these files will have a prefix, that serves as an identifier, and also contains a date, e.g. 2022-06-1VOFM5_ETNA_SICILY.csv. There is no need to change the filename. The app will read the data by ignoring the prefix, and if there are several files, the most recent should be chosen.

**Inclusions.** The file containing inclusions data should also be downloaded from https://georoc.eu/georoc/new-start.asp, on the left menu, choose Inclusions. Note that the current file in the Inclusions_comp folder is not complete, it is an example file that should be replaced. 


Running the app
--

Once the app is set up, only 2 steps are required. From inside the DashVolcano.1.0 folder, activate the virtual environment and launch the app.

> DashVolcano.1.0$ source venv/bin/activate

> python run.py

Once the app runs successfully, a message appears in the terminal window, something like

> Dash is running on http://127.0.0.1:8050/

and some statistics are displayd. To lauch the app, write the url

> http://localhost:8050/

in the browser of your choice.

Adding your own data
--

**Georoc - GVP mapping files**

The GeorocGVPMapping folder contains a .txt file for each .csv in the GeorocDataset folder. Each file is of the form

>GVP;GEOROC

for example, the file ETNA_SICILY.txt contains

>GVP;GEOROC
Etna;ETNA

The first column contains names of GVP volcanoes, the second column contains GEOROC names. More precisely, the GVP name is the name that can be found in the column 'Volcano Name' of the GVP_Volcano_List.xlsx, the second column contains names that appear in the LOCATION or LOCATION column of a precompiled file downloaded from GEOROC. It has to be the same name as that found in between two / / for the LOCATION COLUMN, or the first name before the first comma (if any) in the LOCATION COMMENT.

Here is a more complex from the file ANATOLIA-IRAN_BELT_-_CENOZOIC_QUATERNARY.txt.

>Samsari Volcanic Center;SAMSARI CALDERA,SAMSARI VOLCANIC CHAIN

Note there is no space before and after the GVP names, or the GEOROC names.

These mapping files have been compiled algorithmically, with manual checks, but these checks are not exhaustive. There are more than 500 .csv files of data, the longitude and latitude ranges come with different levels of precision, and the location names may not always contain the volcano name itself. It is possible to simply append more GEOROC location names if a mapping file is not complete (and similarly to remove possibly inaccurate data).


**Manual Datasets**

It is also possible to add more samples with their rock composition, if the desired samples are not (yet) present in the GEOROC dataset. They need to be in the same format as GEOROC format, and put in the ManualDataset folder. The mapping files need to be updated correspondingly. Examples are found in the ManualDataset folder.



