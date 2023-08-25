#!/bin/bash
#Program Name: test_code.sh
#Author name: Wenhao Fang
#Date Created: Aug 24rd 2023
#Date updated:
#Description of the script: test django at port 8000

# Test django project
python3 manage.py runserver 0.0.0.0:8000
echo $(date +'%Y-%m-%d %R') 'Test django project on port 8000'
read -p 'Press Enter to continue'

sudo rm -rf test_code.sh
sudo nano test_code.sh
source test_code.sh