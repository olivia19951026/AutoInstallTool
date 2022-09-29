
APT_INSTALL_DRBD_COMMAND = [
    "add-apt-repository -y ppa:linbit/linbit-drbd9-stack",
    "ls /etc/apt/sources.list.d/",
    "apt-get -y install drbd-dkms",
    "apt-get install drbd-utils",
    "apt-cache policy drbd-dkms",
    "apt-cache policy drbd-utils",
    "drbdadm --version"
]

APT_INSTALL_LINSTOR_COMMAND = [
    "add-apt-repository -y ppa:linbit/linbit-drbd9-stack",
    "ls /etc/apt/sources.list.d/",
    "apt-get -y install linstor-client",
    "apt-get -y install linstor-satellite",
    "apt-cache policy linstor-client",
    "apt-cache policy linstor-satellite",
    "apt-cache policy linstor-common",
    "linstor --version"
]

APT_INSTALL_LINSTOR_CONTROLLER_COMMAND = [
    "add-apt-repository -y ppa:linbit/linbit-drbd9-stack",
    "ls /etc/apt/sources.list.d/",
    "apt-get -y install linstor-client",
    "apt-get -y install linstor-satellite",
    "apt-get -y install linstor-controller",
    "apt-cache policy linstor-client",
    "apt-cache policy linstor-satellite",
    "apt-cache policy linstor-controller",
    "apt-cache policy linstor-common",
    "linstor --version"
]

APT_UNINSTALL_DRBD_COMMAND = [
    "apt-get remove -y --purge drbd-dkms drbd-utils",
    "apt -y autoremove",
    "apt-cache policy drbd-dkms",
    "apt-cache policy drbd-utils",
    "drbdadm --version"
]

APT_UNINSTALL_LINSTOR_COMMAND = [
    "systemctl stop linstor-satellite",
    "apt-get remove -y --purge linstor-satellite linstor-client linstor-common",
    "apt -y autoremove",
    "apt-cache policy linstor-client",
    "apt-cache policy linstor-satellite",
    "apt-cache policy linstor-common",
    "rm -rf /etc/linstor/",
    "rm -rf /var/lib/linstor/",
    "linstor --version"
]

APT_UNINSTALL_LINSTOR_CONTROLLER_COMMAND = [
    "systemctl stop linstor-controller",
    "systemctl stop linstor-satellite",
    "apt-get remove -y --purge linstor-controller linstor-satellite linstor-client linstor-common",
    "apt -y autoremove",
    "apt-cache policy linstor-client",
    "apt-cache policy linstor-satellite",
    "apt-cache policy linstor-controller",
    "apt-cache policy linstor-common",
    "rm -rf /etc/linstor/",
    "rm -rf /var/lib/linstor/",
    "linstor controller version",
    "linstor --version"
]

INSTALL_LINSTOR_CONTROLLER_SYSTEMCTL_COMMAND = [
    "systemctl start linstor-satellite",
    "systemctl status linstor-satellite --no-pager",
    "systemctl start linstor-controller",
    "systemctl status linstor-controller --no-pager",
    "linstor controller version",
    "systemctl stop linstor-controller",
    "systemctl status linstor-controller --no-pager",
    "systemctl stop linstor-satellite",
    "systemctl status linstor-satellite --no-pager"
]

INSTALL_LINSTOR_SYSTEMCTL_COMMAND = [
    "systemctl start linstor-satellite",
    "systemctl status linstor-satellite --no-pager",
    "systemctl stop linstor-satellite",
    "systemctl status linstor-satellite --no-pager"
]

SOURCE_INSTALL_DRBD_COMMAND = [
    "apt-get -y install make flex xmlto po4a xsltproc asciidoctor",
    "apt-get -y install coccinelle",
    "cd drbd-utils-9.21.4",
    "./configure --prefix=/usr --localstatedir=/var --sysconfdir=/etc",
    "make",
    "make install",
    "cd ../drbd-9.1.8/",
    "make",
    "make install",
    "drbdadm --version"
]

SOURCE_UNINSTALL_LINSTOR_COMMAND_1 = [
    "systemctl stop linstor-satellite",
    "rm -rf /var/lib/linstor",
    "rm -rf /var/lib/linstor.d/",
    "rm -rf /etc/linstor/",
    "rm /lib/systemd/system/linstor-satellite.service",
    "rm -rf /usr/share/linstor-server/"
]

SOURCE_UNINSTALL_LINSTOR_COMMAND_2 = [
    "systemctl status linstor-satellite  --no-pager",
    "linstor --version"
]

SOURCE_UNINSTALL_LINSTOR_CONTROLLER_COMMAND_1 = [
    "systemctl stop linstor-satellite",
    "systemctl stop linstor-controller",
    "rm -rf /var/lib/linstor",
    "rm -rf /var/lib/linstor.d/",
    "rm -rf /etc/linstor/",
    "rm /lib/systemd/system/linstor-satellite.service",
    "rm /lib/systemd/system/linstor-controller.service",
    "rm -rf /usr/share/linstor-server/"
]

SOURCE_UNINSTALL_LINSTOR_CONTROLLER_COMMAND_2 = [
    "linstor controller version",
    "systemctl status linstor-controller --no-pager",
    "systemctl status linstor-satellite --no-pager",
    "linstor --version"
]

toml_data = {
    "db": {
        "user": "linstor",
        "password": "linstor",
        "connection_url": "jdbc:h2:/var/lib/linstor/linstordb"
    }
}
