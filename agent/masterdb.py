from db import DB
from mysqltools import MySQLTools
from comparison import Comparison

class MasterDB(DB):
    def __init__(self, host, user, password, db, log_file, log_position):
        super(MasterDB, self).__init__(host, user, password, db, log_file, log_position)
        self.slaves = []

    def update_slaves(self):
        pass

    def insert_slave(self, slave):
        self.slaves.append(slave)

    def remove_slave(self, slave):
        try:
            self.slaves.remove(slave)
        except Exception, e:
            print("Error: {}".format(e))

    def list_all_slaves(self):
        content = []
        for slave in self.slaves:
            content.append("-"*10)
            content.append(str(slave))
        return "\n".join(content)


    def start_all_slaves(self):
        self.admin_all_slaves('start')

    def stop_all_slaves(self):
        self.admin_all_slaves('stop')

    def health_all_slaves(self):
        self.admin_all_slaves('health')

    def admin_all_slaves(self,execute):
        for slave in self.slaves:
            master_data = "--master={}:{}@{}".format(self.user, self.password,
                self.host)
            slave_data = "--slave={}:{}@{}".format(slave.user, slave.password,
                slave.host)
            rpl_user = "--rpl-user={}:{}".format(slave.user, slave.password)

            args = [master_data, slave_data, rpl_user, execute]
            mysqltools = MySQLTools()
            mysqltools.execute("mysqlrpladmin", args)

    def check_all_slaves(self):
        for slave in self.slaves:
            master_data = "--master={}:{}@{}".format(self.user, self.password,
                self.host)
            slave_data = "--slave={}:{}@{}".format(slave.user, slave.password,
                slave.host)

            args = [master_data, slave_data]
            mysqltools = MySQLTools()
            mysqltools.execute("mysqlrplcheck", args)


    def compare_all_slaves(self):
        comparison_list = []
        for slave in self.slaves:
            comparison = Comparison(self, slave)
            slave_data = comparison.get_comparison(self.db, slave.db)
            comparison_list.append(slave_data)

        return comparison_list
