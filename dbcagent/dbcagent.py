from time import sleep
import json
import requests

from slavedb import SlaveDB
from db import DB


def check(slave):
    slave.check_all_masters()


def health(slave):
    slave.health_all_masters()


def compare(slave):
    comp_list = slave.compare_all_masters()
    return comp_list


if __name__ == '__main__':

    host = '10.10.10.3'
    user = 'replicator'
    password = '123456'
    db = 'dbexample'

    slave = SlaveDB(host, user, password, token='bananabananabanana')
    slave.insert_db(db)

    slave.read_master_info()

    while True:
        print(".")
        sleep(1)
        comp_list = compare(slave)
        json_comp = json.dumps(comp_list, sort_keys=True)
        print("Status: {}".format(json_comp))
#        sleep(5)
#        url = "http://10.10.10.2:8000/monitor/send-status"
#        payload = json_comp
#
#        try:
#            headers = {'Content-type': 'application/json'}
#
#            r = requests.post(url, data=payload, headers=headers)
#
#            print("\n\tSever status: {}\n".format(r.status_code))
#
#            if r.status_code==500:
#                print(r.text)
#                break
#
#        except Exception as e:
#            print("Erro {}".format(str(e)))
