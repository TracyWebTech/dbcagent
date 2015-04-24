# dbcagent

Agent for monitoring conflicts in mysql database replication

## Features

## Requirements
python, python-pip, mysql-server, mysql-client mysql-utilities


## Getting Started
### Step 1. Install Vagrant

  Download and install Vagrant from http://www.vagrantup.com

### Step 2. Up Vitual Machines

  The development environment has 3 virtual machines that start with the command:
  ```
  vagrant up
  ```

## Quick Example
  Let's configure a ring model replication with 3 hosts like the following
  configuration:

  ```
  Replica1 is master of  Replica2
  Replica2 is master of  Replica3
  Replica3 is master of  Replica1
  ```

To configure this environment, set the following configurations in each VM:
### Configure replica1
  - Access VM:

  ```
  vagrant ssh replica1
  ```

  - Create configuration file for DBCAgent in `/tmp/dbcagent_config.ini` with the content:

  ```
  [slave]
  host = 10.10.10.3
  user = replicator
  password = 123456
  database = dbexample
  ```

  - Create replication with the command: 

  ```
  mysqlreplicate --master=replicator:123456@10.10.10.5 \
  --slave=replicator:123456@10.10.10.3 --rpl-user=replicator:123456
  ```

### Configure replica2
  - Access VM:

  ```
  vagrant ssh replica2
  ```

  - Create configuration file for DBCAgent in `/tmp/dbcagent_config.ini` with the content:

  ```
  [slave]
  host = 10.10.10.4
  user = replicator
  password = 123456
  database = dbexample
  ```

  - Create replication with the command: 

  ```
  mysqlreplicate --master=replicator:123456@10.10.10.3 \
  --slave=replicator:123456@10.10.10.4 --rpl-user=replicator:123456
  ```

### Configure replica3
  - Access VM:

  ```
  vagrant ssh replica3
  ```

  - Create configuration file for DBCAgent in `/tmp/dbcagent_config.ini` with the content:

  ```
  [slave]
  host = 10.10.10.5
  user = replicator
  password = 123456
  database = dbexample
  ```

  - Create replication with the command: 

  ```
  mysqlreplicate --master=replicator:123456@10.10.10.4 \
  --slave=replicator:123456@10.10.10.5 --rpl-user=replicator:123456
  ```

### Running Agent in each VM
Run agent as user mysql:

  ```
  cd /vagrant/dbcagent
  sudo -u mysql python dbcagent.py
  ```
