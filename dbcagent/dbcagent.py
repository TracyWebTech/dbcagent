import json
import requests
from time import sleep
from ConfigParser import SafeConfigParser

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

    conf_file = '/tmp/dbcagent_config.ini'
    parser = SafeConfigParser()
    parser.read(conf_file)

    host = '10.10.10.3'
    user = 'replicator'
    password = '123456'
    db = 'dbexample'

    host = parser.get('slave','host')
    user = parser.get('slave','user')
    password = parser.get('slave','password')
    db = parser.get('slave','database')

    slave = SlaveDB(host, user, password, token='bananabananabanana')
    slave.insert_db(db)

    slave.read_master_info()

    while True:
        comp_list = compare(slave)
        json_comp = json.dumps(comp_list, sort_keys=True)
        print("Status: {}".format(json_comp))
        sleep(5)
        url = "http://10.10.10.2:8000/monitor/send-status"
        payload = json_comp

        try:
            headers = {'Content-type': 'application/json'}

            r = requests.post(url, data=payload, headers=headers)

            print("\n\tSever status: {}\n".format(r.status_code))

        except Exception as e:
            print("Erro {}".format(str(e)))
