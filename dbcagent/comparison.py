import re
from datetime import datetime

from mysqltools import MySQLTools


R_TABLES = re.compile("TABLE[\s]+([^\s]*)[\s]+(.*)")
R_CONNECTION = re.compile("# server[\d] on ([^:]+):[\s]+...([^:|.]+)")


class Comparison:
    def __init__(self, master, slave):
        self.master = master
        self.slave = slave
        self.tables = {}

    def compare(self, db1, db2):
        self.db1 = db1
        self.db2 = db2

        master_data = "--server1={}:{}@{}".format(self.master.user,
                                                  self.master.password,
                                                  self.master.host)
        slave_data = "--server2={}:{}@{}".format(self.slave.user,
                                                 self.slave.password,
                                                 self.slave.host)
        difftype = "--difftype=unified"
        output_format = "--format=vertical"
        databases = "{}:{}".format(self.db1, self.db2)
        additional = "--run-all-tests"

        args = [master_data, slave_data, difftype, output_format, additional,
                databases]
        mysqltools = MySQLTools()
        output_result, error_result = mysqltools.execute("mysqldbcompare",
                                                         args)
        if error_result != 0:
            if self.is_database_connected(self.slave.host, output_result):
                self.slave.set_conn_status('connected')
            else:
                self.slave.set_conn_status('ERROR')

        self.check_table_status(output_result)

        return self.tables

    def get_comparison(self, db1, db2):
        tables_status = self.compare(db1, db2)
        master_data = self.master.replication_info()
        database = {}
        database['name'] = db2
        database['tables'] = tables_status
        database['date'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        master_data['databases'] = [database]
        return master_data

    def is_database_connected(self, db_host, output_result):
        res = R_CONNECTION.findall(output_result)
        for host, status in res:
            if host == db_host:
                if 'connected' in status:
                    return 1
                else:
                    return 0

    def check_table_status(self, output_result):
        res = R_TABLES.findall(output_result)
        for r in res:
            table_status = 'pass'

            if 'FAIL' in r[1]:
                table_status = 'FAIL'
            elif 'WARN' in r[1]:
                table_status = 'WARN'
            elif 'SKIP' in r[1]:
                table_status = 'SKIP'

            self.tables[r[0]] = table_status

'''
Basic structure of a output with replication conficts:

# server1 on 10.10.10.3: ... connected.
# server2 on 10.10.10.4: ... connected.
# Checking databases dbexample on server1 and dbexample on server2
#
#                                                   Defn    Row     Data
# Type      Object Name                             Diff    Count   Check
# -------------------------------------------------------------------------
# TABLE     t1                                      pass    pass    FAIL
#
# Data differences found among rows:
--- `dbexample`.`t1`
+++ `dbexample`.`t1`
@@ -1,5 +1,5 @@
 *************************       1. row *************************
     id: 1
     - name: alberto
     -  age: 22
     + name: Alberto
     +  age: 23
      1 row.

# TABLE     t2                                      pass    pass    pass

# Database consistency check failed.
#
# ...done

'''
