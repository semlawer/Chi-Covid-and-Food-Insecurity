#!/bin/bash
# for color prints
Yellow="\033[0;33m"
Red='\033[0;31m'
Cyan='\033[0;36m'
Green='\033[0;32m'
Blue='\033[1;34m'
White='\033[0;37m'
Color_Off='\033[0m'

clear

# 1. First check to see if the correct version of Python is installed on the local machine 
printf "${Blue}1. Checking Python version... \n${Color_Off}"
REQ_PYTHON_V="370"

ACTUAL_PYTHON_V=$(python -c 'import sys; version=sys.version_info[:3]; print("{0}{1}{2}".format(*version))')
ACTUAL_PYTHON3_V=$(python3 -c 'import sys; version=sys.version_info[:3]; print("{0}{1}{2}".format(*version))')

if [[ $ACTUAL_PYTHON_V > $REQ_PYTHON_V ]] || [[ $ACTUAL_PYTHON_V == $REQ_PYTHON_V ]];  then 
    PYTHON="python"
elif [[ $ACTUAL_PYTHON3_V > $REQ_PYTHON_V ]] || [[ $ACTUAL_PYTHON3_V == $REQ_PYTHON_V ]]; then 
    PYTHON="python3"
else
    printf "${White}    Python 3.7 is not installed on this machine. Please install Python 3.7 before continuing. \n${Color_Off}"
    exit 1
fi

printf "${White}    --Python 3.7 is installed \n${Color_Off}"

#2. Check the version
printf "${Blue}2. Please check your Postgres (13.2) and PostGis (3.1) versions \xF0\x9F\x94\x8D \n${Color_Off}"

# 3. What OS are we running on?
PLATFORM=$($PYTHON -c 'import platform; print(platform.system())')

printf "${Blue}2. Checking OS Platform... \n${Color_Off}"
printf "${White}    --OS=Platform=$PLATFORM \n${Color_Off}"

# 4. Create Virtual environment and install requirements
printf "${Blue}Creating new virtual environment and install requirements... \n${Color_Off}"

# Ask if the user wants to remove the env directory if it exists 
if [[ -d env ]]; then
    printf "${Cyan}Virtual environment already exists. Do you want to remove it and create a new one?[y/n] \n${Color_Off}"
    read ans_env
    if [ $ans_env == y ]; then
        printf "${Red}Deleting virtual environment... \n${Color_Off}"
        rm -rf env
        $PYTHON -m venv env
        printf "${Blue}4. Installing Requirements... \n${Color_Off}"
        if [[ ! -e "requirements.txt" ]]; then 
            printf "${White}    --Need to requirements.txt to install packages. \n${Color_Off}"
            exit 1
        fi
        source env/bin/activate
        pip install -r requirements.txt
        if [[ ! -d env ]]; then 
            echo -e "    --Could not create virtual environment...Please make sure venv is installed"
            exit 1
        fi
    else
        source env/bin/activate
    fi
else
    $PYTHON -m venv env
    source env/bin/activate
    printf "${Blue}4. Installing Requirements... \n${Color_Off}"
    if [[ ! -e "requirements.txt" ]]; then 
        printf "${White}    --Need to requirements.txt to install packages. \n${Color_Off}"
        exit 1
    fi
    pip install -r requirements.txt
fi

# 5. Select the way to get test the code: loaded data or run scraper

# optional flags for selecting the way to get the data
# : loaded dat

while getopts d: opt; do
    case $opt in
        d) data=${OPTARG};;
    esac
done

## 
if [ "$data" == scrap ]; then
    if [ -f "CS_covid_food/chifood.sqlite3" ]; then
        printf "${Red}Removing sqlite3 file to load the new one... \n${Color_Off}"
        rm CS_covid_food/chifood.sqlite3
    fi
    printf "${Blue}Running scraping functions... \n${Color_Off}"
    printf "${Red}This process may take a while. Please grab a coffee and enjoy waiting!! \xE2\x8F\xB3 \xF0\x9F\x8D\xB5\n \n${Color_Off}"
    $PYTHON go.py
fi


#prelims 
printf "${Blue}Starting Django... \n${Color_Off}"
pkill postgres 

db_name='final_project_db'
username='capp_cs_122'

initdb -D $db_name
pg_ctl -D $db_name -l logfile start # killall postgres
createuser  --superuser -w  $username 
createdb --owner=$username $db_name
psql -U $username -d $db_name -c 'CREATE EXTENSION postgis;'
psql -U $username -d $db_name -c 'CREATE EXTENSION postgis_topology;'
printf "${Green}Success!! ${Yellow}$db_name ${Green}PostGIS DB was created with owner ${Yellow}$username \n${Color_Off}"
$PYTHON CS_covid_food/manage.py makemigrations
$PYTHON CS_covid_food/manage.py migrate
$PYTHON CS_covid_food/manage.py shell < CS_covid_food/populate_layers.py
printf "${Yellow}Launching Django app... \n${Color_Off}"
$PYTHON CS_covid_food/manage.py runserver 5000
