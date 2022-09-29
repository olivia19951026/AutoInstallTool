#  Default lastest version for apt install
LATEST_VERSION = ""

# "Y","Yes","yes","y","YES" for Yes,
# "N","No","no","n" for No
NO = ["no", "n", "NO", "No"]
YES = ["y", "Y", "Yes", "yes", "YES"]

# Enter your password for sudo command
SUDO_PASSWORD = "19941123"

# ---------------------------------------------------
# apt install package setting
# ---------------------------------------------------

# Apt Install Version
APT_DRBD_DKMS_VERSION = LATEST_VERSION
APT_DRBD_UTILS_VERSION = LATEST_VERSION
APT_LINSTOR_CLIENT_VERSION = LATEST_VERSION
APT_LINSTOR_SATELLITE_VERSION = LATEST_VERSION
APT_LINSTOR_CONTROLLER_VERSION = LATEST_VERSION

# Apt Install Package
APT_INSTALL_DRBD = "no"
APT_INSTALL_LINSTOR = "no"
APT_INSTALL_LINSTOR_CONTROLLER = "no"

# Apt Uninstall Package
APT_UNINSTALL_DRBD = "no"
APT_UNINSTALL_LINSTOR = "no"
APT_UNINSTALL_LINSTOR_CONTROLLER = "no"

# ---------------------------------------------------
# source code install package setting
# ---------------------------------------------------
# Enviroment Architecture ARM64 or x86
ARM64 = ["ARM64", "Arm64", "arm64"]
X86 = ["x86", "X86"]
ARCHITECTURE = "X86"

# Source Package Path
SOURCE_DRBD_FOLDER_PATH = "/home/olivia/Desktop/python/drbd"
SOURCE_LINSTOR_FOLDER_PATH = "/home/olivia/Desktop/python/linstor"

# Source Install Version
SOURCE_DRBD_VERSION = "9.1.8"
SOURCE_DRBD_UTILS_VERSION = "9.21.4"
SOURCE_PYTHON_LINSTOR_VERSION = "1.14.0"
SOURCE_LINSTOR_CLIENT_VERSION = "1.14.0"
SOURCE_LINSTOR_SERVER_VERSION = "1.19.1"

# Source Install Package
SOURCE_INSTALL_DRBD = "no"
SOURCE_INSTALL_LINSTOR = "yes"
SOURCE_INSTALL_LINSTOR_CONTROLLER = "yes"

# Source Uninstall Package
SOURCE_UNINSTALL_DRBD = "no"
SOURCE_CLEAN_DRBD = "no"
SOURCE_UNINSTALL_LINSTOR = "no"
SOURCE_UNINSTALL_LINSTOR_CONTROLLER = "no"
SOURCE_CLEAN_LINSTOR = "no"
