from comparison import Comparison
from db import DB
from masterdb import MasterDB
from mysqltools import MySQLTools


class SlaveDB(DB):
    def __init__(self, host, user, password, status='connected', token=''):

        super(SlaveDB, self).__init__(host, user, password, status)

        self.masters = []
        self.token = token;

    def read_master_info(self):
        master_info_file = "/var/lib/mysql/master.info"
        lines = []
        with open(master_info_file) as f:
            lines = f.read().splitlines()

        master_log_file = lines[1].strip()
        master_log_pos = lines[2].strip()
        master_host = lines[3].strip()
        user = lines[4].strip()
        password = lines[5].strip()

        # FIXME: master databases
        master = MasterDB(master_host, user, password, status='unknow',
                          log_file=master_log_file, log_pos=master_log_pos)
        master.insert_db(self.databases[0]['name'])
        self.insert_master(master)

    def insert_master(self, master):
        self.masters.append(master)

    def remove_master(self, slave):
        try:
            self.masters.remove(slave)
        except Exception, e:
            print("Error: {}".format(e))

    def list_all_masters(self):
        content = []
        for slave in self.masters:
            content.append("-"*10)
            content.append(str(slave))
        return "\n".join(content)

    def start_all_masters(self):
        self.admin_all_masters('start')

    def stop_all_masters(self):
        self.admin_all_masters('stop')

    def health_all_masters(self):
        self.admin_all_masters('health')

    def admin_all_masters(self, execute):
        for slave in self.masters:
            master_data = "--master={}:{}@{}".format(self.user, self.password,
                                                     self.host)
            slave_data = "--slave={}:{}@{}".format(slave.user, slave.password,
                                                   slave.host)
            rpl_user = "--rpl-user={}:{}".format(slave.user, slave.password)

            args = [master_data, slave_data, rpl_user, execute]
            mysqltools = MySQLTools()
            mysqltools.execute("mysqlrpladmin", args)

    def check_all_masters(self):
        for slave in self.masters:
            master_data = "--master={}:{}@{}".format(self.user, self.password,
                                                     self.host)
            slave_data = "--slave={}:{}@{}".format(slave.user, slave.password,
                                                   slave.host)

            args = [master_data, slave_data]
            mysqltools = MySQLTools()
            mysqltools.execute("mysqlrplcheck", args)

    def compare_all_masters(self):
        comparison_list = []
        for master in self.masters:
            comparison = Comparison(master, self)
            db1 = master.databases[0]['name']
            db2 = self.databases[0]['name']
            print("DB1: {}\tDB2: {}".format(db1, db2))
            master_data = comparison.get_comparison(db1, db2)
            comparison_list.append(master_data)

        slave_dict = self.host_info()
        slave_dict['token'] = self.token;
        slave_dict['masters'] = comparison_list

        return slave_dict
