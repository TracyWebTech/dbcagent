import json


class DB(object):
    def __init__(self, host, user, password, status='unknow'):
        self.host = host
        self.user = user
        self.password = password
        self.conn_status = status
        self.databases = []

    def insert_db(self, name, tables=[]):
        db = {}
        db['name'] = name
        db['tables'] = tables
        self.databases.append(db)

    def set_conn_status(self, conn_status):
        self.conn_status = conn_status

    def to_json(self):
        private_info = {
            'user': self.user,
            'password': self.password,
        }
        attributes = private_info.copy()
        attributes.update(self.host_info)

        return json.dumps(attributes)

    def host_info(self):
        dic = {
            'host': self.host,
            'status': self.conn_status,
            'databases': self.databases,
        }
        return dic

    def __str__(self):
        return self.to_json()
