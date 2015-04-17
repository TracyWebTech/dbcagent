#!/bin/bash

export DATABASE="dbexample"
export MASTER_USER="replicator"
export MASTER_PWD="123456"

if [ -e $1 ]
then
	$DATABASE=$1
fi

if [ -e $2 ]
then
	$MASTER_USER=$2
fi

if [ -e $3 ]
then
	$MASTER_PWD=$3
fi


mysql -u root -p'123456' -e "create database $DATABASE"
mysql -u root -p'123456' -e "create user '$MASTER_USER'@'%' identified by '$MASTER_PWD';"
mysql -u root -p'123456' -e "grant replication slave on *.* to '$MASTER_USER'@'%';"

