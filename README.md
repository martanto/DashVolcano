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
and create the virtual environment
> $ python3 -m venv venv
