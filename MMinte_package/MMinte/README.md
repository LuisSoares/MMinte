#Instructions on how to install MMinte on your machine
##What you will need to have installed in your machine.
* Python 2.7
* Firefox
* pip
* virtualenv

#Then you:
1. Download the package from github.com/mendessoares/MMinte
2. Use the terminal on your machine to go to the folder where you downloaded the package to
3. Go to MMinte by typing ``cd MMinte``
4. Create a virtual environment by typing ``virtualenv env``
5. This will create a folder in MMinte called env. This is where all the packages and modules you need for doing all the analysis will be stored. This avoids potential conflicts between the versions of packages and modules needed for MMinte and any you may have in your system.
6. Enter your virtual environment by typing ``source env/bin/activate`` . This command assumes you are right outside your env folder.
7. Then type ``bash install-requiredPKG.sh``
8. Wait for everything to get installed.
9. Once all is installed (you will see a message in the terminal and you bet the prompt back) you are ready to run MMinte from your virtual environment.
10. Type ``cd site``
11. And lets launch MMinte. Type ``python launchMMinte``
12. Open a Firefox browser and go to the address http://0.0.0.0:5000 
13. Play with MMinte
14. When you are done, close the browser window and press CTRL+C on your terminal. To leave your virtual environment just type ``deactivate``


#In case you want to see how the program is going
1. Go to the supportFile folder
2. You can open the file logError_file.txt on any text editor, BUT,
3. If you want to keep track of things happening in real time, type ``tail - logError_file.txt`` in the terminal when your are in the folder.
 

#Requirements:
biopython==1.66

CherryPy==3.8.0

cobra==0.4.0b3

cycler==0.9.0

DataSpyre==0.2.0

Jinja2==2.8

MarkupSafe==0.23

matplotlib==1.5.0

numpy==1.10.1

pandas==0.17.1

pyparsing==2.0.6

python-dateutil==2.4.2

python-libsbml==5.12.0

pytz==2015.7

scipy==0.16.1

six==1.10.0

wheel==0.24.0

requests==2.8.1