from time import sleep
from masterdb import MasterDB
from db import DB


def check(master):
    master.check_all_slaves()

def health(master):
    master.health_all_slaves()

def compare(master):
    comp_list = master.compare_all_slaves()
    print("Status: {}".format(comp_list))


if __name__ == '__main__':

    user = 'replicator';
    password = '123456';
    db = 'dbexample';

    host1 = '10.10.10.3';
    log_file1 = 'mysql-bin.000007';
    log_position1 = '1411';

    host2 = '10.10.10.4';
    log_file2 = 'mysql-bin.000007';
    log_position2 = '1757';

    master1 = MasterDB(host1, user, password, db, log_file1, log_position1)
    slave2 = DB(host1, user, password, db, log_file1, log_position1)

    master2 = MasterDB(host2, user, password, db, log_file2, log_position2)
    slave1 = DB(host2, user, password, db, log_file2, log_position2)


    master1.insert_slave(slave1)
    master2.insert_slave(slave2)

    print("list slaves of master1")
    print(master1.list_all_slaves())
    print("list slaves of master2")
    print(master2.list_all_slaves())

    while True:
        compare(master1)
	sleep(5)
