from subprocess import call
from subprocess import check_output
import subprocess
from db import DB


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
            self.execute_slave("mysqlrpladmin", args)

    def check_all_slaves(self):
        for slave in self.slaves:
            master_data = "--master={}:{}@{}".format(self.user, self.password,
                self.host)
            slave_data = "--slave={}:{}@{}".format(slave.user, slave.password,
                slave.host)

            args = [master_data, slave_data]
            self.execute_slave("mysqlrplcheck", args)


    def compare_all_slaves(self):
        for slave in self.slaves:
            master_data = "--server1={}:{}@{}".format(self.user, self.password,
                self.host)
            slave_data = "--server2={}:{}@{}".format(slave.user, slave.password,
                slave.host)
            difftype = "--difftype=unified"
            output_format = "--format=vertical"
            databases = "{}:{}".format(self.db, slave.db)

            args = [master_data, slave_data, difftype, output_format, databases]
            self.execute_slave("mysqldbcompare", args)

    def execute_slave(self, bin_command, args = []):
        print("Running {} with:\n\t{}".format(bin_command, args))
        command_to_run = [bin_command] + args

        result = ''
        try:
            result = subprocess.Popen(command_to_run, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            print("--"*50)
            output, error = result.communicate()
            errorcode = result.returncode
            if errorcode==0:
                print("OK")
            else:
                print("[Saida:\n{}\n]".format(output))
            print("--"*50)
        except:
            print("Error in command exection")
