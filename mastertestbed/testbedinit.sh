#! /bin/bash

# This script gets the SCADA testbed to be able to execute.

# NOTE: It is recommended that the testbed be used in Fedora.
#	The testbed has not been tested in other linux distros and may not be compatible.

# NOTE: This script installs the following packages:
#		python-configobj
#		pyserial
#		python-setuptools

sudo true

# WARNING: For other linux distros, the install commands/package names may need to be changed.
#	   Ex. (Debian):
#		sudo apt-get install python-configobj
#		sudo apt-get install python-serial
#		sudo apt-get install python-setuptools
#	   NOTE: The above commands have not been tested.

# Install appropriate packages (Fedora):
sudo yum install python-configobj
sudo yum install pyserial
sudo yum install python-setuptools

echo "Executing..."
cd trunk && chmod 755 *.py
cd scripts
chmod 755 *.sh
cd ../sims
chmod 755 *.py
chmod 755 */*.py
cd ../attacks
chmod 755 *.py
cd ../protolibs && chmod 755 *.py
cd modbus-tk.hg
chmod 755 *.py
chmod 755 */*.py
sudo python setup.py install
cd build/lib*/modbus_tk
chmod 755 *.py
cd ../../../../..
cd sims/rtupipe && python mkconfig.py
cd ../rtuwater && python mkconfig.py
cd ../rtutank && python mkconfig.py
cd ../tcppipe && python mkconfig.py
cd ../tcptank && python mkconfig.py
echo "Done!"

# After script finishes:
#	run "python" and type "import modbus_tk" and hit 'Enter/Return'
#	press CTRL-D
#	Go to scripts folder and enter:
#		./run.sh logfilename
#		NOTE: logfilename can be any name for the log file and will be
#		      located in the 'trunk' directory
