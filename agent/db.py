import json


class DB(object):
    def __init__(self, host, user, password, db, log_file, log_position):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.log_file = log_file
        self.log_position = log_position
        self.conn_status = "unknow"

    def set_conn_status(status):
        self.conn_status = conn_status

    def to_json(self):
        dic = {
                'host': self.host,
                'user': self.user,
                'password': self.password,
                'log_file': self.log_file,
                'log_position': self.log_position,
              }
        return json.dumps(dic)

    def replication_info(self):
        dic = {
                'host': self.host,
                'log_file': self.log_file,
                'log_position': self.log_position,
              }
        return dic

    def __str__(self):
        return self.to_json()
