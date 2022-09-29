import command
import config


class GetCommand():
    def __init__(self):
        self.source_drbd_path = ""
        self.source_drbd_utils_path = ""
        self.source_python_linstor_path = ""
        self.source_linstor_client_path = ""
        self.source_linstor_server_path = ""
        self.source_drbd_folder_path = ""
        self.source_linstor_folder_path = ""
        self.get_drbd_package_path()
        self.get_linstor_package_path()

    def get_drbd_package_path(self):
        if config.SOURCE_INSTALL_DRBD in config.YES or config.SOURCE_UNINSTALL_DRBD in config.YES:
            my_path = config.SOURCE_DRBD_FOLDER_PATH
            if my_path.endswith("/") == False:
                my_path = my_path+"/"
            self.source_drbd_folder_path = my_path
            self.source_drbd_path = self.source_drbd_folder_path + \
                "drbd"+'-'+config.SOURCE_DRBD_VERSION
            self.source_drbd_utils_path = self.source_drbd_folder_path + \
                "drbd-utils"+'-'+config.SOURCE_DRBD_UTILS_VERSION

    def get_linstor_package_path(self):
        if config.SOURCE_INSTALL_LINSTOR in config.YES or config.SOURCE_UNINSTALL_LINSTOR in config.YES:
            my_path = config.SOURCE_LINSTOR_FOLDER_PATH
            if my_path.endswith("/") == False:
                my_path = my_path+"/"
            self.source_linstor_folder_path = my_path
            self.source_python_linstor_path = self.source_linstor_folder_path+"python-linstor" +\
                '-'+config.SOURCE_PYTHON_LINSTOR_VERSION
            self.source_linstor_client_path = self.source_linstor_folder_path+"linstor-client" +\
                '-'+config.SOURCE_LINSTOR_CLIENT_VERSION
            self.source_linstor_server_path = self.source_linstor_folder_path+"linstor-server" +\
                '-'+config.SOURCE_LINSTOR_SERVER_VERSION

    def get_apt_install_drbd_command(self):
        commands = command.APT_INSTALL_DRBD_COMMAND
        # get drbd dkms version
        if config.APT_DRBD_DKMS_VERSION == config.LATEST_VERSION:
            commands[2] = command.APT_INSTALL_DRBD_COMMAND[2]
        else:
            commands[2] = command.APT_INSTALL_DRBD_COMMAND[2] + "=" + config.APT_DRBD_DKMS_VERSION+"*"
        # get drbd utils version
        if config.APT_DRBD_UTILS_VERSION == config.LATEST_VERSION:
            commands[3] = command.APT_INSTALL_DRBD_COMMAND[3]
        else:
            commands[3] = command.APT_INSTALL_DRBD_COMMAND[3] + "=" + config.APT_DRBD_UTILS_VERSION+"*"
        return commands

    def get_apt_install_linstor_command(self):
        # check linstor controller = "yes"
        if config.APT_INSTALL_LINSTOR_CONTROLLER in config.YES:
            commands = command.APT_INSTALL_LINSTOR_CONTROLLER_COMMAND
            if config.APT_LINSTOR_CLIENT_VERSION == config.LATEST_VERSION:
                pass
            else:
                commands[2] = command.APT_INSTALL_LINSTOR_CONTROLLER_COMMAND[2] +\
                    "="+config.APT_LINSTOR_CLIENT_VERSION+"*"
            if config.APT_LINSTOR_SATELLITE_VERSION == config.LATEST_VERSION:
                pass
            else:
                commands[3] = command.APT_INSTALL_LINSTOR_CONTROLLER_COMMAND[3] +\
                    "="+config.APT_LINSTOR_SATELLITE_VERSION+"*"
            if config.APT_LINSTOR_CONTROLLER_VERSION == config.LATEST_VERSION:
                pass
            else:
                commands[4] = command.APT_INSTALL_LINSTOR_CONTROLLER_COMMAND[4] +\
                    "="+config.APT_LINSTOR_CONTROLLER_VERSION+"*"
        # check linstor controller  = "No"
        elif config.APT_INSTALL_LINSTOR_CONTROLLER in config.NO:
            commands = command.APT_INSTALL_LINSTOR_COMMAND
            if config.APT_LINSTOR_CLIENT_VERSION == config.LATEST_VERSION:
                pass
            else:
                commands[2] = command.APT_INSTALL_LINSTOR_COMMAND[2] +\
                    "="+config.APT_LINSTOR_CLIENT_VERSION+"*"
            if config.APT_LINSTOR_SATELLITE_VERSION == config.LATEST_VERSION:
                pass
            else:
                commands[3] = command.APT_INSTALL_LINSTOR_COMMAND[3] +\
                    "="+config.APT_LINSTOR_SATELLITE_VERSION+"*"
        return commands

    def get_apt_install_linstor_systemctl_command(self):
        # check linstor controller = "yes"
        if config.APT_INSTALL_LINSTOR_CONTROLLER in config.YES:
            commands = command.INSTALL_LINSTOR_CONTROLLER_SYSTEMCTL_COMMAND
        # check linstor controller  = "No"
        elif config.APT_INSTALL_LINSTOR_CONTROLLER in config.NO:
            commands = command.INSTALL_LINSTOR_SYSTEMCTL_COMMAND
        return commands

    def get_apt_uninstall_drbd_command(self):
        commands = command.APT_UNINSTALL_DRBD_COMMAND
        return commands

    def get_apt_uninstall_linstor_command(self):
        if config.APT_UNINSTALL_LINSTOR_CONTROLLER in config.YES:
            commands = command.APT_UNINSTALL_LINSTOR_CONTROLLER_COMMAND
        elif config.APT_UNINSTALL_LINSTOR_CONTROLLER in config.NO:
            commands = command.APT_UNINSTALL_LINSTOR_COMMAND
        return commands

    def get_source_install_drbd_command(self):
        commands = list()
        commands.append(
            "apt-get -y install make flex xmlto po4a xsltproc asciidoctor")
        commands.append("apt-get -y install coccinelle")
        return commands

    def get_source_install_linstor_server_command(self):
        current_path = self.source_linstor_server_path
        linstor_server_name = self.source_linstor_server_path.split("/")[-1]
        command_1 = "cp -r "+current_path+"/build/distributions/" + \
            linstor_server_name+" /usr/share/linstor-server"
        if config.SOURCE_INSTALL_LINSTOR_CONTROLLER in config.YES:
            command_2 = "cp "+current_path + \
                "/scripts/linstor-controller.service /lib/systemd/system/"
        elif config.SOURCE_INSTALL_LINSTOR_CONTROLLER in config.NO:
            command_2 = "rm /usr/share/linstor-server/bin/Controller"
        command_3 = "cp "+current_path + \
            "/scripts/linstor-satellite.service /lib/systemd/system/"
        command_4 = "mkdir /etc/linstor"
        command_5 = "cp "+current_path+"/docs/linstor.toml-example /etc/linstor/"
        command_6 = "mv "+current_path+"/linstor.toml" " /etc/linstor/"
        commands = [command_1, command_2, command_3,
                    command_4, command_5, command_6]
        return commands

    def get_source_install_linstor_systemctl_command(self):
        commands = ["systemctl daemon-reload"]
        if config.SOURCE_INSTALL_LINSTOR_CONTROLLER in config.YES:
            commands += command.INSTALL_LINSTOR_CONTROLLER_SYSTEMCTL_COMMAND
        elif config.SOURCE_INSTALL_LINSTOR_CONTROLLER in config.NO:
            commands += command.INSTALL_LINSTOR_SYSTEMCTL_COMMAND
        return commands

    def get_source_uninstall_linstor_command_1(self):
        commands = list()
        if config.SOURCE_UNINSTALL_LINSTOR_CONTROLLER in config.YES:
            commands = command.SOURCE_UNINSTALL_LINSTOR_CONTROLLER_COMMAND_1
        elif config.SOURCE_UNINSTALL_LINSTOR_CONTROLLER in config.NO:
            commands = command.SOURCE_UNINSTALL_LINSTOR_COMMAND_1
        return commands

    def get_source_uninstall_linstor_command_2(self):
        commands = list()
        if config.SOURCE_UNINSTALL_LINSTOR_CONTROLLER in config.YES:
            commands = command.SOURCE_UNINSTALL_LINSTOR_CONTROLLER_COMMAND_2
        elif config.SOURCE_UNINSTALL_LINSTOR_CONTROLLER in config.NO:
            commands = command.SOURCE_UNINSTALL_LINSTOR_COMMAND_2
        return commands

    def get_tar_source_package_command(self, gz_list):
        commands = list()
        commands.append("ls -l")
        for command in gz_list:
            commands.append("tar zxvf "+command)
        return commands
