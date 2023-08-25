#!/bin/bash
#Program Name: update_code.sh
#Author name: Wenhao Fang
#Date Created: Aug 24rd 2023
#Date updated:
#Description of the script: update github codes

# project_name="ArgusWatcher"
# github_url='https://github.com/simonangel-fong/ArgusWatcher.git'
# host_ip="54.162.108.69"
project_name
github_url
host_ip

###########################################################
## Download codes from github
###########################################################
cd ~
sudo rm -r ~/${project_name}  # remove the exsting directory
if [ -z ${github_url} ]; then # if github url is empty
  echo -e "\n$(date +'%Y-%m-%d %R') Cannot clone code from github because github_url is not given."
else
  echo -e "\n$(date +'%Y-%m-%d %R') Downloading codes from github..."
  git clone $github_url # clone codes from github
  echo -e "$(date +'%Y-%m-%d %R') Code downloaded."
fi

###########################################################
## Reload supervisor and nginx
###########################################################
echo -e "\n$(date +'%Y-%m-%d %R') Reload supervisor"
sudo service supervisor reload

echo -e "$(date +'%Y-%m-%d %R') Reload nginx"
sudo service nginx reload

###########################################################
## Setup completed
###########################################################
echo -e "\n$(date +'%Y-%m-%d %R') Setup completed. \n"
read -p "Press Enter to continue..."

sudo rm -rf update_code.sh
sudo nano update_code.sh
source update_code.sh
