from subprocess import call
from subprocess import check_output
import subprocess
from db import DB


class MySQLTools:
    def __init__(self):
        pass


    def execute(self, bin_command, args = []):
        print("Running {} with:\n\t{}".format(bin_command, args))
        command_to_run = [bin_command] + args

        result = ''
        try:
            result = subprocess.Popen(command_to_run, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            print("--"*50)
            output, error = result.communicate()
            errorcode = result.returncode

            return output, errorcode
        except:
            print("Error in command exection")
