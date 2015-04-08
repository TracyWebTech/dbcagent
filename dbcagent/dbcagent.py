from time import sleep
import json
import requests

from masterdb import MasterDB
from db import DB


def check(master):
    master.check_all_slaves()


def health(master):
    master.health_all_slaves()


def compare(master):
    comp_list = master.compare_all_slaves()
    return comp_list


if __name__ == '__main__':

    user = 'replicator'
    password = '123456'
    db = 'dbexample'

    host1 = '10.10.10.3'
    log_file1 = 'mysql-bin.000007'
    log_position1 = '1411'

    host2 = '10.10.10.4'
    log_file2 = 'mysql-bin.000007'
    log_position2 = '1757'

    master1 = MasterDB(host1, user, password, db, log_file1, log_position1,
                       token='bananabananabanana')
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
        comp_list = compare(master1)
        json_comp = json.dumps(comp_list, sort_keys=True)
        print("Status: {}".format(json_comp))
        sleep(5)
        url = "http://10.10.10.2:8000/monitor/send-status"
        payload = json_comp

        try:
            headers = {'Content-type': 'application/json'}

            r = requests.post(url, data=payload, headers=headers)

            print("\n\tSever status: {}\n".format(r.status_code))
            
            if r.status_code==500:
                print(r.text)
                break

        except Exception as e:
            print("Erro {}".format(str(e)))
