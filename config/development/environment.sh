#!/bin/bash

IP=$1
last_n=${IP##*.}

MYSQL_CONF_FILE=/etc/mysql/my.cnf
DATABASE_NAME=dbexample

#sudo apt-get update

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password 123456'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 123456'

sudo apt-get -y install mysql-server mysql-utilities

sudo sed -i "s/#server-id.\+$/server-id\t\t= $last_n/" $MYSQL_CONF_FILE
sudo sed -i 's/#log_bin/log_bin/' $MYSQL_CONF_FILE
sudo sed -i "s/#binlog_do_db.\+$/binlog_do_db\t\t= $DATABASE_NAME/" $MYSQL_CONF_FILE
sudo sed -i 's/^bind-address/#bind-address/' $MYSQL_CONF_FILE


sudo service mysql restart


ln -s /vagrant ~/dbcagent || true
