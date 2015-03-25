import re

from db import DB
from mysqltools import MySQLTools

class Comparison:
    def __init__(self, master, slave):
        self.master = master
        self.slave = slave
        self.tables = {}

    def compare(self, db1, db2):
        self.db1 = db1
        self.db2 = db2

        master_data = "--server1={}:{}@{}".format(self.master.user,
            self.master.password, self.master.host)
        slave_data = "--server2={}:{}@{}".format(self.slave.user,
            self.slave.password, self.slave.host)
        difftype = "--difftype=unified"
        output_format = "--format=vertical"
        databases = "{}:{}".format(self.db1, self.db2)
        additional = "--run-all-tests"

        args = [master_data, slave_data, difftype, output_format, additional,
                databases]
        mysqltools = MySQLTools()
        output_result, error_result = mysqltools.execute("mysqldbcompare", args)

        self.check_table_status(output_result)

        return self.tables

    def get_comparison(self, db1, db2):
        tables_status = self.compare(db1, db2)
        slave_data = self.slave.replication_info()
        slave_data[db2] = tables_status

        return slave_data

    def check_table_status(self, output_result):
        r_tables = re.compile("TABLE[\s]+([^\s]*)[\s]+(.*)")
        res = r_tables.findall(output_result)
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
