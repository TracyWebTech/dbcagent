import subprocess


class MySQLTools:
    def __init__(self):
        pass

    def execute(self, bin_command, args=[]):
        print("Running {} with:\n\t{}".format(bin_command, args))
        command_to_run = [bin_command] + args

        result = ''
        try:
            result = subprocess.Popen(command_to_run, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            output, error = result.communicate()
            errorcode = result.returncode

            return output, errorcode
        except:
            print("Error in command execution")
