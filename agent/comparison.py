from db import DB
from mysqltools import MySQLTools

class Comparison:
    def __init__(self):
        pass
    
    def compare(self, master, slave, db1, db2):
        master_data = "--server1={}:{}@{}".format(master.user, master.password,
            master.host)
        slave_data = "--server2={}:{}@{}".format(slave.user, slave.password,
            slave.host)
        difftype = "--difftype=unified"
        output_format = "--format=vertical"
        databases = "{}:{}".format(db1, db2)
        additional = "--run-all-tests"

        args = [master_data, slave_data, difftype, output_format, additional,
                databases]
        mysqltools = MySQLTools()
        output_result, error_result = mysqltools.execute("mysqldbcompare", args)

        print("*"*100)
        print("{}".format(output_result))
        print("*"*100)
