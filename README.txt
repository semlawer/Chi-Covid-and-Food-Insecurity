Documentation for CAPP-30122 Project

Project: COVID-19 and Food Insecurity in Chicago
By: Sophia Mlawer, Valeria Balza, Gabriela Palacios, Mariel Wiechers

Language Requirements: Python 2.7 ????

External Libraries Needed:

Required Python Libraries:
Please see requirements.txt for a complete list.

To Run Software: Check order????????
python3.7 -m venv env
bash install.sh
source env/bin/activate
DJANGO LINES ??????????
python3 go.py

Explanation of the Above Steps:
(1) Run the command bash install.sh from the project root. The script verifies the 
current installation of Python; creates a new virtual environment, "env"; 
and then installs all the external libraries and required packages in that 
environment using the requirements.text file

(2) Activate the virtual environment with the command source env/bin/activate.
To deactive it, type deactive

(3) Launch the Django web application from the project root with the command:
_______ . Once the server is running, navigate to your local webhost (????)
in your browser of choice. The page might take some time to load so please 
enjoy a cup of coffee as it loads. 

(4) In the command line, enter python3 go.py which will build the data from
a combination of csv files, API, and web scraping. Additionally this will 
go on to run the regression and ready the data for the Django interface.

(5) Then feel free to interact with either the Django-created map or table
where you can filter the layers of the map and use the table to show specific
zip codes or find the zip codes that fit socioeconomic descriptions.

Please see our write up for the list of python files and what each of them does.

You may see these error messages:
??????
