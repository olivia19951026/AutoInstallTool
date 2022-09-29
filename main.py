import os
import config
import command
from execute_coomand import ExecuteCommand
from get_command import GetCommand
from check_config import CheckConfig
import toml
import signal

class AutoInstall():
    def __init__(self) -> None:
        self.ec = ExecuteCommand()
        self.gc = GetCommand()
        self.cc = CheckConfig()

    def check_sudo_password(self):
        commands = ["pwd"]
        self.print_processing("Check Sudo Password")
        self.ec.execute_sudo_command_with_raise_error(
            commands, config.SUDO_PASSWORD)

    def execute_apt_install_drbd(self):
        if config.APT_INSTALL_DRBD in config.YES:
            self.print_processing("Execute Apt Install DRBD")
            commands = self.gc.get_apt_install_drbd_command()
            self.ec.execute_sudo_command_with_raise_error(commands, config.SUDO_PASSWORD)

    def execute_apt_install_linstor(self):
        if config.APT_INSTALL_LINSTOR in config.YES:
            self.print_processing("Execute Apt Install Linstor")
            commands = self.gc.get_apt_install_linstor_command()
            self.ec.execute_sudo_command_with_raise_error(commands, config.SUDO_PASSWORD)
            commands = self.gc.get_apt_install_linstor_systemctl_command()
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)

    def execute_apt_uninstall_drbd(self):
        if config.APT_UNINSTALL_DRBD in config.YES:
            self.print_processing("Execute Apt Uninstall DRBD")
            commands = self.gc.get_apt_uninstall_drbd_command()
            commands = command.APT_UNINSTALL_DRBD_COMMAND
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)

    def execute_apt_uninstall_linstor(self):
        if config.APT_UNINSTALL_LINSTOR in config.YES:
            self.print_processing("Execute Apt Uninstall Linstor")
            commands = self.gc.get_apt_uninstall_linstor_command()
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)

    def execute_source_install_drbd(self):
        if config.SOURCE_INSTALL_DRBD in config.YES:
            make_commands = ["make", "make install"]
            self.print_processing("Execute Source Install DRBD")
            self.ec.cd_commmand(self.gc.source_drbd_folder_path)
            if len(self.cc.source_drbd_gz_list) > 0:
                commands = self.gc.get_tar_source_package_command(self.cc.source_drbd_gz_list)
                self.ec.execute_command_with_raise_error(commands)
            commands = self.gc.get_source_install_drbd_command()
            self.ec.execute_sudo_command_with_raise_error(commands, config.SUDO_PASSWORD)
            cd_path = self.gc.source_drbd_utils_path
            self.ec.cd_commmand(self.gc.source_drbd_utils_path+"/")
            command = [cd_path+"/configure --prefix=/usr --localstatedir=/var --sysconfdir=/etc"]
            commands = command+make_commands
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
            self.ec.cd_commmand(self.gc.source_drbd_path+"/")
            self.ec.execute_sudo_command(make_commands, config.SUDO_PASSWORD)
            commands = ["drbdadm --version"]
            self.ec.execute_sudo_command_with_raise_error(commands, config.SUDO_PASSWORD)

    def execute_source_install_linstor(self):
        if config.SOURCE_INSTALL_LINSTOR in config.YES:
            make_commands = ["make", "make install"]
            self.print_processing("Execute Source Install Linstor")
            if len(self.cc.source_linstor_gz_list) > 0:
                self.ec.cd_commmand(self.gc.source_linstor_folder_path)
                commands = self.gc.get_tar_source_package_command(self.cc.source_linstor_gz_list)
                self.ec.execute_command_with_raise_error(commands)
            commands = ["apt-get -y install python3-setuptools help2man gradle"]
            self.ec.execute_sudo_command_with_raise_error(commands, config.SUDO_PASSWORD)
            self.ec.cd_commmand(self.gc.source_python_linstor_path+"/")
            self.ec.execute_sudo_command(make_commands, config.SUDO_PASSWORD)
            self.ec.cd_commmand(self.gc.source_linstor_client_path+"/")
            self.ec.execute_sudo_command(make_commands, config.SUDO_PASSWORD)
            current_path = self.gc.source_linstor_server_path+"/"
            self.ec.cd_commmand(current_path)
            if config.ARCHITECTURE in config.ARM64:
                commands = ["cp build.gradle build.gradle.orig"]
                self.ec.execute_sudo_command_with_raise_error(commands, config.SUDO_PASSWORD)
                self.edit_build_gradle(current_path)
            commands = [current_path+"gradlew getProtoc",current_path + "gradlew assemble"]
            self.ec.execute_os_command(config.SUDO_PASSWORD, command)
            self.ec.cd_commmand(current_path+"build/distributions")
            linstor_server_name = self.gc.source_linstor_server_path.split("/")[-1]
            unzip_command = "unzip "+linstor_server_name+".zip" 
            self.ec.execute_sudo_command([unzip_command], config.SUDO_PASSWORD)
            self.ec.cd_commmand(current_path)
            self.creat_and_edit_toml_file("linstor.toml")
            commands = self.gc.get_source_install_linstor_server_command()
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
            commands = self.gc.get_source_install_linstor_systemctl_command()
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
            commands = ["linstor --version"]
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)

    def execute_source_uninstall_drbd(self):
        if config.SOURCE_UNINSTALL_DRBD in config.YES:
            self.print_processing("Execute Source Uninstall DRBD")
            current_kernel_version = self.ec.get_command_return_value("uname -r")[0]
            cd_path = "/lib/modules/"+current_kernel_version+"/updates"
            self.ec.cd_commmand(cd_path)
            commands = ["rm drbd.ko", "rm drbd_transport_tcp.ko"]
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
            count_file = len([entry for entry in os.listdir(
                cd_path) if os.path.isfile(os.path.join(cd_path, entry))])
            if count_file == 0:
                commands = ["rm -rf updates"]
            else:
                commands = []
            commands += ["/sbin/depmod -a", "drbdadm --version"]
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
            cd_path = self.gc.source_drbd_utils_path
            self.ec.cd_commmand(cd_path)
            commands = ["make uninstall", "drbdadm --version"]
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
            if config.SOURCE_CLEAN_DRBD in config.YES:
                commands = ["make clean"]
                self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
                cd_path = self.gc.source_drbd_path
                self.ec.cd_commmand(cd_path)
                self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)

    def execute_source_uninstall_linstor(self):
        if config.SOURCE_UNINSTALL_LINSTOR in config.YES:
            self.print_processing("Execute Source Uninstall Linstor")
            commands = self.gc.get_source_uninstall_linstor_command_1()
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
            commands = ["make uninstall"]
            self.ec.cd_commmand(self.gc.source_linstor_client_path)
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
            self.ec.cd_commmand(self.gc.source_python_linstor_path)
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
            commands = self.gc.get_source_uninstall_linstor_command_1()
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
        if config.SOURCE_CLEAN_DRBD in config.YES:
            commands = ["make clean"]
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)
            self.ec.cd_commmand(self.gc.source_linstor_client_path)
            self.ec.execute_sudo_command(commands, config.SUDO_PASSWORD)

    def print_processing(self, processing):
        self.ec.show_command(processing)

    def creat_and_edit_toml_file(self, output_file_name):
        with open(output_file_name, "w") as toml_file:
            toml.dump(command.toml_data, toml_file)

    def edit_build_gradle(self, file_path):
        file_name = file_path+"build.gradle"
        with open(file_name, "rt") as file_data:
            write_file_data = ""
            for line in file_data:
                write_file_data += line.replace('-linux-x86_64.zip','-linux-aarch_64.zip')
        with open(file_name, 'w') as file:
            file.write(write_file_data)

    def run(self):
        signal.signal(signal.SIGINT, self.ec.handler)
        self.cc.check_all_config()
        self.check_sudo_password()
        self.execute_apt_install_drbd()
        self.execute_apt_install_linstor()
        self.execute_apt_uninstall_drbd()
        self.execute_apt_uninstall_linstor()
        self.execute_source_install_drbd()
        self.execute_source_install_linstor()
        self.execute_source_uninstall_drbd()
        self.execute_source_uninstall_linstor()
        self.ec.show_command("Successful!!")
        self.ec.save_execute_log()

if __name__ == "__main__":
    automatic_installation = AutoInstall()
    automatic_installation.run()

 