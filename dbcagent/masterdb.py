from db import DB


class MasterDB(DB):
    def __init__(self, host, user, password, status, log_file,
                 log_pos):

        self.log_file = log_file
        self.log_pos = log_pos

        super(MasterDB, self).__init__(host, user, password, status)


    def replication_info(self):
        dic = super(MasterDB, self).host_info()
        dic['log_file'] = self.log_file
        dic['log_pos'] = self.log_pos

        return dic
