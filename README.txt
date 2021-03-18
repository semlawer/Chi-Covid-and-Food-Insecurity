Documentation for CAPP-30122 Project

Project: COVID-19 and Food Insecurity in Chicago
By: Sophia Mlawer, Valeria Balza, Gabriela Palacios, Mariel Wiechers

Language Requirements: Python 3.7

External Libraries Needed:
PosgreSQL (13.2)
PostGIS (3.1)

Please note PosgreSQL and PostGIS should be installed on your local machine before running the program. 
We use (brew install postgres and brew install postgis)

Required Python Libraries:
Please see requirements.txt for a complete list.

To Run Software:
First, to launch the Django application with the created databases, 
type the following command in the bash command line:
    bash setup.sh

Alternatively, to create the databases from scratch and launch the Django
application, type the following command in the bash command line:
    bash setup.sh -d scrap

Please note the second option takes some time to run.


Explanation of the Above Steps:
(1) Run the command bash setup.sh from the project root. The script verifies the 
current installation of Python; creates a new virtual environment, "env"; 
and then installs the required packages in that environment using the 
requirements.text file

(2) The file then activates the virtual environment and launch the Django web application. 
Once the server is running, navigate to your local webhost in your browser of choice. If 
the databases are greated from scratch, the file go.py is called to extract and clean all data 
sources, run regression analysis, and create SQL databases. 

(5) Once the Django application is launched, feel free to interact with either the 
Django-created map or table where you can filter the layers of the map and 
use the table to show specific zip codes or find the zip codes that fit 
socioeconomic descriptions.

Please see our write up for the list of python files and what each of them does.
