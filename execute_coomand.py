from subprocess import Popen, PIPE, STDOUT
import datetime
import time
import os


class ExecuteCommand():
    def __init__(self):
        self.log_txt = ""
        self.log_path = self.get_current_directory()

    def get_current_directory(self):
        current_dictionary = os.path.abspath(os.getcwd())
        return current_dictionary

    def save_execute_log(self):
        now = datetime.datetime.now()
        current_time = "%04d%02d%02d%02d%02d%02d" % (
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        save_name = self.log_path+"/log_"+current_time+".txt"
        f = open(save_name, "w+")
        with open(save_name, 'w') as f:
            f.write(self.log_txt)
        self.log_txt = ""
        print(save_name+" saved")

    def get_start_time(self):
        start_time = time.time()
        now = datetime.datetime.now()
        current_time = "Current time: %02d:%02d:%02d" % (
            now.hour, now.minute, now.second)
        self.log_txt += current_time+"\n"
        return start_time

    def get_execution_time(self, start_time):
        elapsed_time = time.time() - start_time
        execution_time = 'Execution time: ' + \
            str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        self.log_txt += execution_time+"\n"

    def show_command(self, command):
        line_len = 5
        self.log_txt += "\n"+"-"*line_len+command+"-"*line_len+"\n"
        print(command)
        print('-'*50)

    def execute_os_command(self,password,commands):
        for command in commands:
            try:
                os.system('echo %s|sudo -S %s' % (password, command))
            except:
                self.show_command("FAILED!!")
                self.save_execute_log()
                exit()

    # user command
    def execute_command(self, commands, **kwargs):
        for command in commands:
            self.show_command(command)
            start_time = self.get_start_time()
            command = command.split()
            cmd = Popen(command, stdout=PIPE, stderr=STDOUT, **kwargs)
            for line in cmd.stdout:
                line = line.decode()
                self.log_txt += line
                # print(line)
            self.get_execution_time(start_time)

    def execute_command_with_raise_error(self, commands, **kwargs):
        for command in commands:
            self.show_command(command)
            start_time = self.get_start_time()
            command = command.split()
            cmd = Popen(command, stdout=PIPE, stderr=STDOUT, **kwargs)
            for line in cmd.stdout:
                line = line.decode()
                self.log_txt += line
                # print(line)
            cmd.communicate()
            if cmd.returncode != 0:
                self.show_command("FAILED!!")
                self.save_execute_log()
                print('-'*50)
                raise SyntaxError(line)
            self.get_execution_time(start_time)

    # sudo command
    def execute_sudo_command(self, commands, sudo_password, **kwargs):
        for command in commands:
            self.show_command(command)
            start_time = self.get_start_time()
            cmd = command.split()
            cmd1 = Popen(['echo', sudo_password], stdout=PIPE)
            cmd2 = Popen(['sudo', '-S'] + cmd, stdin=cmd1.stdout,
                         stdout=PIPE, stderr=STDOUT, **kwargs)
            for line in cmd2.stdout:
                line = line.decode()
                self.log_txt += line
                # print(line)
            self.get_execution_time(start_time)

    def execute_sudo_command_with_raise_error(self, commands, sudo_password, **kwargs):
        for command in commands:
            self.show_command(command)
            start_time = self.get_start_time()
            cmd = command.split()
            cmd1 = Popen(['echo', sudo_password], stdout=PIPE)
            cmd2 = Popen(['sudo', '-Si'] + cmd, stdin=cmd1.stdout,
                         stdout=PIPE, stderr=STDOUT, **kwargs)
            for line in cmd2.stdout:
                line = line.decode()
                self.log_txt += line
                # print(line)
            cmd2.communicate()
            if cmd2.returncode != 0:
                self.show_command("Failed!!")
                self.save_execute_log()
                print('-'*50)
                raise SyntaxError(line)
            self.get_execution_time(start_time)

    def cd_commmand(self, cd_path):
        do_command = "cd "+cd_path
        self.show_command(do_command)
        start_time = self.get_start_time()
        try:
            os.chdir(cd_path)
            current_directory = os.path.abspath(os.getcwd())
            text = "current_directory: "+str(current_directory)+"\n"
            self.log_txt += text
            self.get_execution_time(start_time)
        except FileNotFoundError as e:
            self.show_command(str(e))
            self.show_command("FAILED!!")
            self.save_execute_log()
            exit()

    def get_command_return_value(self, command, **kwargs):
        command = command.split()
        cmd = Popen(command, stdout=PIPE, stderr=STDOUT, **kwargs)
        output, _ = cmd.communicate()
        output = output.decode(encoding="utf-8").split('\n')
        return output

    def handler(self, signum, frame):
        print("\nCtrl-c was pressed. Exit.")
        self.show_command("KeyboardInterrupt")
        self.save_execute_log()
        exit(1)


if __name__ == "__main__":
    pass
