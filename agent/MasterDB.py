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
        self.execute_all_slaves('start')

    def stop_all_slaves(self):
        self.execute_all_slaves('stop')

    def health_all_slaves(self):
        self.execute_all_slaves('health')

    def execute_all_slaves(self,execute):
        for slave in self.slaves:
            call(["mysqlrpladmin",
                 "--master={}:{}@{}".format(self.user, self.password,
                     self.host),
                 "--slave={}:{}@{}".format(slave.user, slave.password,
                     slave.host), 
                 "--rpl-user={}:{}".format(slave.user, slave.password),
                 execute
                ])

    def check_all_slaves(self):
        for slave in self.slaves:
            call(["mysqlrplcheck",
                 "--master={}:{}@{}".format(self.user, self.password,
                     self.host),
                 "--slave={}:{}@{}".format(slave.user, slave.password,
                     slave.host), 
                ])
