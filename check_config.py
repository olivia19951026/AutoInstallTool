import config
import re
from os import path


class CheckConfig():
    def __init__(self):
        self.source_drbd_gz_list = []
        self.source_linstor_gz_list = []

    def check_yes_no_format(self, commmand_name, config_command):
        yes_no_table = config.YES+config.NO
        if type(config_command) != str:
            raise TypeError(
                commmand_name+" input should be a string !! ex: 'Yes' or 'No'")
        elif config_command not in yes_no_table:
            raise ValueError(
                commmand_name+" input can only be  "+str(yes_no_table) )

    def check_version_format(self, package_name, version):
        if version == config.LATEST_VERSION:
            pass
        elif type(version) == str and re.match(r"^\d+.\d+.\d+$", version):
            pass
        elif type(version) != str:
            raise TypeError(package_name+" input should be a string !! ex. '__.__.__' , "
                            "where _ -> should be a number. ex:'1.14.0'")
        else:
            raise ValueError(package_name+" input format should be '__.__.__' ,"
                             " where _ -> should be a number. ex: '1.14.0'")

    def check_password_format(self, password_name, password):
        if type(password) != str:
            raise TypeError(
                password_name+" should be a string !! ex: '123456'")
        elif len(password) <= 0:
            raise SyntaxError("Please input value for " + password_name+" in config.py!!")

    def check_enviorment_architecture(self):
        architecture_table = config.ARM64 + config.X86
        if type(config.ARCHITECTURE) != str:
            raise TypeError("ARCHITECTURE should be a string !! ex: 'x86'")
        elif config.ARCHITECTURE in architecture_table :
            pass
        else:    
            ValueError("Input for ARCHITECTURE can only"+ str(architecture_table))
        
    def check_input_path(self, path_name, my_path):
        if type(my_path) != str:
            raise TypeError(
                path_name+" should be a string !! ex: '/home/ubuntu/'")
        elif (path.exists(my_path) == False):
            raise OSError(path_name+" : "+my_path +" folder path does not exist")

    def check_soure_package_exists(self, package_path, gz_list):
        if path.exists(package_path) == True:
            pass
        else:
            package_path = package_path+".tar.gz"
            if path.exists(package_path) == True:
                gz_list.append(package_path)
            else:
                raise OSError(
                    package_path+" does not exist!! please check source "+package_path+" path")

    def check_source_drbd_package(self):
        if config.SOURCE_INSTALL_DRBD in config.YES or config.SOURCE_UNINSTALL_DRBD in config.YES:
            my_path = config.SOURCE_DRBD_FOLDER_PATH
            if my_path.endswith("/") == False:
                my_path = my_path+"/"
            self.check_input_path("SOURCE_DRBD_FOLDER_PATH", my_path)
            source_drbd_version = my_path+"drbd" + '-' + config.SOURCE_DRBD_VERSION
            source_drbd_utils_version = my_path+"drbd-utils" + '-' + config.SOURCE_DRBD_UTILS_VERSION
            self.check_soure_package_exists(source_drbd_version, self.source_drbd_gz_list)
            self.check_soure_package_exists(source_drbd_utils_version, self.source_drbd_gz_list)

    def check_source_linstor_package(self):
        if config.SOURCE_INSTALL_LINSTOR in config.YES or config.SOURCE_UNINSTALL_LINSTOR in config.YES:
            my_path = config.SOURCE_LINSTOR_FOLDER_PATH
            if my_path.endswith("/") == False:
                my_path = my_path+"/"
            self.check_input_path("SOURCE_LINSTOR_FOLDER_PATH", my_path)
            source_python_linstor_version = my_path+"python-linstor" + '-' + config.SOURCE_PYTHON_LINSTOR_VERSION
            source_linstor_client_version = my_path+"linstor-client" + '-' + config.SOURCE_LINSTOR_CLIENT_VERSION
            source_linstor_server_version = my_path+"linstor-server" + '-' + config.SOURCE_LINSTOR_SERVER_VERSION
            self.check_soure_package_exists(source_python_linstor_version, self.source_linstor_gz_list)
            self.check_soure_package_exists(source_linstor_client_version, self.source_linstor_gz_list)
            self.check_soure_package_exists(source_linstor_server_version, self.source_linstor_gz_list)

    def check_all_config(self):
        self.check_enviorment_architecture()
        self.check_password_format("SUDO_PASSWORD", config.SUDO_PASSWORD)
        self.check_version_format("APT_DRBD_DKMS_VERSION", config.APT_DRBD_DKMS_VERSION)
        self.check_version_format("APT_DRBD_UTILS_VERSION", config.APT_DRBD_UTILS_VERSION)
        self.check_version_format("APT_LINSTOR_CLIENT_VERSION", config.APT_LINSTOR_CLIENT_VERSION)
        self.check_version_format("APT_LINSTOR_SATELLITE_VERSION", config.APT_LINSTOR_SATELLITE_VERSION)
        self.check_version_format("APT_LINSTOR_CONTROLLER_VERSION", config.APT_LINSTOR_CONTROLLER_VERSION)
        self.check_version_format("SOURCE_DRBD_VERSION", config.SOURCE_DRBD_VERSION)
        self.check_version_format("SOURCE_DRBD_UTILS_VERSION", config.SOURCE_DRBD_UTILS_VERSION)
        self.check_version_format("SOURCE_PYTHON_LINSTOR_VERSION", config.SOURCE_PYTHON_LINSTOR_VERSION)
        self.check_version_format("SOURCE_LINSTOR_CLIENT_VERSION", config.SOURCE_LINSTOR_CLIENT_VERSION)
        self.check_version_format("SOURCE_LINSTOR_SERVER_VERSION", config.SOURCE_LINSTOR_SERVER_VERSION)
        self.check_yes_no_format("APT_INSTALL_DRBD", config.APT_INSTALL_DRBD)
        self.check_yes_no_format("APT_INSTALL_LINSTOR", config.APT_INSTALL_LINSTOR)
        self.check_yes_no_format("APT_INSTALL_LINSTOR_CONTROLLER", config.APT_INSTALL_LINSTOR_CONTROLLER)
        self.check_yes_no_format("APT_UNINSTALL_DRBD",config.APT_UNINSTALL_DRBD)
        self.check_yes_no_format("APT_UNINSTALL_LINSTOR", config.APT_UNINSTALL_LINSTOR)
        self.check_yes_no_format("APT_UNINSTALL_LINSTOR_CONTROLLER", config.APT_UNINSTALL_LINSTOR_CONTROLLER)
        self.check_yes_no_format("SOURCE_INSTALL_DRBD", config.SOURCE_INSTALL_DRBD)
        self.check_yes_no_format("SOURCE_INSTALL_LINSTOR", config.SOURCE_INSTALL_LINSTOR)
        self.check_yes_no_format("SOURCE_INSTALL_LINSTOR_CONTROLLER", config.SOURCE_INSTALL_LINSTOR_CONTROLLER)
        self.check_yes_no_format("SOURCE_UNINSTALL_DRBD", config.SOURCE_UNINSTALL_DRBD)
        self.check_yes_no_format("SOURCE_CLEAN_DRBD", config.SOURCE_CLEAN_DRBD)
        self.check_yes_no_format("SOURCE_UNINSTALL_LINSTOR", config.SOURCE_UNINSTALL_LINSTOR)
        self.check_yes_no_format("SOURCE_UNINSTALL_LINSTOR_CONTROLLER", config.SOURCE_UNINSTALL_LINSTOR_CONTROLLER)
        self.check_yes_no_format("SOURCE_CLEAN_LINSTOR", config.SOURCE_CLEAN_LINSTOR)
        self.check_source_drbd_package()
        self.check_source_linstor_package()


if __name__ == "__main__":
    check_config = CheckConfig()
    check_config.check_all_config()
