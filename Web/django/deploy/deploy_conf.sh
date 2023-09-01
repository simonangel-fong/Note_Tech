#!/bin/bash
#Program Name: deploy_conf.sh
#Author name: Wenhao Fang
#Date Created: Aug 23rd 2023
#Date updated:
#Description of the script: Configuration for deployment.

# # shortcut to update deployment script
# sudo rm -rf ArgusWatcher deploy_conf.sh env # remove existing script
# sudo nano deploy_conf.sh  # create a new sh file

project_name="ArgusWatcher"
github_url='https://github.com/simonangel-fong/ArgusWatcher.git'
host_ip="18.206.179.90"
# project_name=$1 # refer 1st argument
# github_url=$2 # refer 2nd argument
# host_ip=$3  # refer 3rd argument

###########################################################
## Updates OS
###########################################################
echo -e "\n$(date +'%Y-%m-%d %R') Updating package on Linux..."
yes | sudo apt-get update  # update the package on Linux system.
# sudo apt-get upgrade # downloads and installs the updates for each outdated package and dependency
echo $(date +'%Y-%m-%d %R') Package updated.
read -p "Press Enter to continue..."

###########################################################
## Firewall
###########################################################
# echo -e "\n$(date +'%Y-%m-%d %R') Installing Firwall..."
# sudo apt-get install ufw        # install firewall
# echo $(date +'%Y-%m-%d %R') Firwall installed.

# echo -e "\n$(date +'%Y-%m-%d %R') Configure Firwall"
# sudo ufw default allow outgoing # Allow outgoing traffic
# sudo ufw default deny incoming  # Deny all incoming traffic
# sudo ufw allow ssh              # Allow ssh traffic
# sudo ufw allow 8000             # Allow the port 8000, the port to test django while configuring deployment
# yes | sudo ufw enable           # Enables firewall

# echo -e "\n$(date +'%Y-%m-%d %R') Firwall status:"
# sudo ufw status # Status of firewall
# read -p "Press Enter to continue..."

###########################################################
## Install MySQL
###########################################################
echo -e "\n$(date +'%Y-%m-%d %R') Installing MySQL related packages..."
sudo apt-get install mysql-server
sudo systemctl start mysql

sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
echo $(date +'%Y-%m-%d %R') MySQL related packages installed.
read -p "Press Enter to continue..."

###########################################################
## Configure MySQL
###########################################################
# sudo mysql_secure_installation # may create issue

sudo systemctl start mysql
echo "Check Mysql status:"
systemctl status mysql.service
read -p "Press Enter to continue..."

echo "Input username for MySQL:"
read user
echo "Input password for MySQL:"
read pwd

sudo mysql -u root -e "CREATE USER '${user}'@'localhost' IDENTIFIED BY '${pwd}';"

sudo mysql -u root -e "GRANT CREATE, ALTER, DROP, INSERT, UPDATE, INDEX, DELETE, SELECT, REFERENCES, RELOAD on *.* TO '${user}'@'localhost' WITH GRANT OPTION;"

sudo mysql -u root -e "FLUSH PRIVILEGES;"

mysql -u$user -p$pwd -e "CREATE DATABASE django_db;"

sudo mysql -u$user -p$pwd -e 'show databases;'
echo "MySQL configuration completed."
read -p "Press Enter to continue..."

###########################################################
## Establish virtual environment
###########################################################
cd ~
echo -e "\n$(date +'%Y-%m-%d %R') Installing venv package..."
sudo apt-get install python3-venv # Install pip package
# sudo apt-get install virtualenv # Install pip package
echo -e "$(date +'%Y-%m-%d %R') Venv package installed."

echo -e "\n$(date +'%Y-%m-%d %R') Creating virtual environment..."
python3 -m venv env # Creates virtual environment
echo -e "$(date +'%Y-%m-%d %R') Virtual environment Created."

echo -e "$(date +'%Y-%m-%d %R') Activate virtual environment."
source env/bin/activate # Activates venv

###########################################################
## Download codes from github
###########################################################
cd ~
sudo rm -rf ~/${project_name}
if [ -z ${github_url} ]; then # if github url is empty
  echo -e "\n$(date +'%Y-%m-%d %R') Cannot clone code from github because github_url is not given."
else
  echo -e "\n$(date +'%Y-%m-%d %R') Downloading codes from github..."
  sudo git clone $github_url # clone codes from github
  echo $(date +'%Y-%m-%d %R') Code downloaded.
fi
read -p "Press Enter to continue..."

###########################################################
## Install packages within venv
###########################################################
cd ~
cd ${project_name}
echo -e "\n$(date +'%Y-%m-%d %R') Installing packages within virtual environment..."
if test -f requirements.txt; then # if requirements file exists
  pip install -r requirements.txt
  pip install mysqlclient # install mysqlclient
  pip install gunicorn # install gunicorn
fi
pip install django  # install django if not installed
pip install gunicorn # install gunicorn
echo $(date +'%Y-%m-%d %R') Env Package installed.
pip list
read -p "Press Enter to continue..."

###########################################################
## Djnago project configuration
###########################################################
cd ~

env_file=~/${project_name}/${project_name}/${project_name}/.env
sudo bash -c "sudo cat >$env_file <<ENV
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=test.arguswatcher@gmail.com
EMAIL_HOST_PASSWORD=ojgkondpujxfcxao
RECIPIENT_ADDRESS=simonangelfong@gmail.com

MYSQL_DATABASE_NAME=django_db
MYSQL_USERNAME=adam
MYSQL_PASSWORD=adam123456
MYSQL_HOST=localhost
MYSQL_PORT=3306
ENV"

python3 ~/${project_name}/${project_name}/manage.py makemigrations AppTest # need to modify app name
python3 ~/${project_name}/${project_name}/manage.py migrate

python3 ~/${project_name}/${project_name}/manage.py runserver 0.0.0.0:8000

echo $(date +'%Y-%m-%d %R') Deactivate virtual environment
deactivate
cd ~
echo $(date +'%Y-%m-%d %R') Django migrate complate.
read -p "Press Enter to continue..."

###########################################################
## Configuration gunicorn
## Configuration gunicorn.socket
###########################################################
echo -e "\n$(date +'%Y-%m-%d %R') Create gunicorn socket conf file"
socket_conf=/etc/systemd/system/gunicorn.socket

sudo bash -c "sudo cat >$socket_conf <<SOCK
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
SOCK"

###########################################################
## Configuration gunicorn.service
###########################################################
echo -e "$(date +'%Y-%m-%d %R') Create gunicorn service conf file"
service_conf=/etc/systemd/system/gunicorn.service

sudo bash -c "sudo cat >$service_conf <<SERVICE
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=root
Group=www-data 
WorkingDirectory=/home/ubuntu/${project_name}/${project_name}
ExecStart=/home/ubuntu/env/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    ${project_name}.wsgi:application

[Install]
WantedBy=multi-user.target
SERVICE"

###########################################################
## Apply gunicorn configuration
###########################################################
echo -e "$(date +'%Y-%m-%d %R') Apply gunicorn configuration"
sudo systemctl daemon-reload          # reload daemon
sudo systemctl start gunicorn.socket  # Start gunicorn
sudo systemctl enable gunicorn.socket # enable on boots
sudo systemctl restart gunicorn       # restart gunicorn

# echo -e "$(date +'%Y-%m-%d %R') Gunicorn status: \n"
# sudo systemctl status gunicorn

###########################################################
## Configuration nginx
###########################################################
echo -e "\n$(date +'%Y-%m-%d %R') Installing nginx package..."
sudo apt-get install nginx # install nginx
echo -e "\n$(date +'%Y-%m-%d %R') Nginx package installed."

echo -e "$(date +'%Y-%m-%d %R') Configure nginx conf"
nginx_conf=/etc/nginx/nginx.conf
sudo sed -i '1cuser root;' $nginx_conf

echo -e "$(date +'%Y-%m-%d %R') Configure nginx for django project"
django_conf=/etc/nginx/sites-available/django.conf
sudo bash -c "cat >$django_conf <<DJANGO_CONF
server {
  listen 80;
  server_name ${host_ip};
  location = /favicon.ico { access_log off; log_not_found off; }
  location /static/ {
    root /home/ubuntu/${project_name}/${project_name};
  }

  location /media/ {
    root /home/ubuntu/${project_name}/${project_name};
  }

  location / {
    include proxy_params;
    proxy_pass http://unix:/run/gunicorn.sock;
  }
}
DJANGO_CONF"

sudo ln -sf /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled
echo -e "$(date +'%Y-%m-%d %R') Creat link in sites-enabled directory."

echo -e "\n$(date +'%Y-%m-%d %R') Test nignx syntax:"
sudo nginx -t

# restart nginx
echo -e "\n$(date +'%Y-%m-%d %R') Restart nignx"
sudo systemctl restart nginx

# echo -e "\n$(date +'%Y-%m-%d %R') Nignx status:"
# systemctl status nginx

###########################################################
## Configuration supervisor
###########################################################
echo -e "\n$(date +'%Y-%m-%d %R') Installing supervisor package..."
sudo apt-get install supervisor # install supervisor
echo -e "$(date +'%Y-%m-%d %R') Supervisor package installed."

echo -e "$(date +'%Y-%m-%d %R') Create directory for logging"
sudo mkdir -p /var/log/gunicorn

echo -e "$(date +'%Y-%m-%d %R') Configure supervisor for gunicorn"
supervisor_gunicorn=/etc/supervisor/conf.d/gunicorn.conf

sudo bash -c "cat >$supervisor_gunicorn <<SUP_GUN
[program:gunicorn]
    directory=/home/ubuntu/${project_name}/${project_name}
    command=/home/ubuntu/env/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock  ${project_name}.wsgi:application
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/gunicorn/gunicorn.err.log
    stdout_logfile=/var/log/gunicorn/gunicorn.out.log

[group:guni]
    programs:gunicorn
SUP_GUN"

echo -e "$(date +'%Y-%m-%d %R') Reread configuration file"
sudo supervisorctl reread # tell supervisor read configuration file

echo -e "$(date +'%Y-%m-%d %R') Update supervisor configuration"
sudo supervisorctl update # update supervisor configuration

echo -e "$(date +'%Y-%m-%d %R') Configuration status:\n"
sudo supervisorctl status # verify configuration status

###########################################################
## Firewall configuration for production
###########################################################
echo -e "\n$(date +'%Y-%m-%d %R') Configure Firwall after deployment configuration"
sudo ufw delete allow 8000 # disable port 8000
sudo ufw allow http/tcp
sudo ufw allow https/tcp
sudo ufw allow "Nginx HTTPS"

echo -e "\n$(date +'%Y-%m-%d %R') Firwall status:"
sudo ufw status # Status of firewall

echo -e "\n$(date +'%Y-%m-%d %R') List available app:"
sudo ufw app list

###########################################################
## Setup completed
###########################################################
echo -e "\n$(date +'%Y-%m-%d %R') Setup completed. \n"
read -p "Press Enter to continue..."