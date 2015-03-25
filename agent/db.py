import json


class DB(object):
    def __init__(self, host, user, password, db, log_file, log_position):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.log_file = log_file
        self.log_position = log_position

    def to_json(self):
        dic = {
                'host': self.host,
                'user': self.user,
                'password': self.password,
                'log_file': self.log_file,
                'log_position': self.log_position,
              }
        return json.dumps(dic)

    def __str__(self):
        return self.to_json()
