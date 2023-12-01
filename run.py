# ************************************************************************************* #
#
# This file starts the app DashVolcano.
# Type the command: python run.py
#
# The DashVolcano app was tested with: Python 3.7.4 on Ubuntu 20.04.4 LTS
#                                      Python 3.8.3 on Mac OS Monterey version 12.5.1
#
# Author: F. Oggier
# Last update: Aug 30 2022
# ************************************************************************************* #

from DashVolcano.index import app

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
