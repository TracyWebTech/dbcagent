from subprocess import call
from DB import DB


class MasterDB(DB):
    def __init__(self, host, user, password, log_file, log_position):
        super(MasterDB, self).__init__(host, user, password, log_file, log_position)
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
            rpl_user = "--rpl-user={}:{}".format(slave.user, slave.password)
            others_args = [execute, rpl_user]
            self.execute_slave("mysqlrpladmin", slave, others_args)

    def check_all_slaves(self):
        for slave in self.slaves:
            self.execute_slave("mysqlrplcheck", slave)

    def execute_slave(self, bin_command, slave, others_args = []):
        master_data = "--master={}:{}@{}".format(self.user, self.password,
            self.host)
        slave_data = "--slave={}:{}@{}".format(slave.user, slave.password,
            slave.host)
        command_to_run = [bin_command, master_data, slave_data] + others_args

        call(command_to_run)
