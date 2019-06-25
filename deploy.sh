#!/bin/bash

git_archive_url="https://cdn.example.com/dns-server.tar.gz"
conf_url="https://cdn.example.com/encrypted.cfg"

function naive_check_os () {
    [[ -e /etc/fedora-release ]] && echo 'fedora' && return 0
    if [[ -e /usr/bin/lsb_release ]]; then
        lsb_release -a | grep 'Ubuntu' > /dev/null 2>&1 && echo 'ubuntu' && return 0
        lsb_release -a | grep 'Debian' > /dev/null 2>&1 && echo 'debian' && return 0
    fi
    [[ -e /usr/bin/yum ]] && yum --version | grep -F 'centos.org' > /dev/null 2>&1 && echo 'centos' && return 0
    uname -r | grep -F '-ARCH' > /dev/null 2>&1 && echo 'archlinux' && return 0
    echo 'unsupported' && return 1
}

os=$(naive_check_os)
python3="/usr/bin/python3"
pip3="/usr/bin/pip3"

# prepare
[[ $os = 'ubuntu' ]] || [[ $os = 'debian' ]] && apt update && apt install -y gcc make libssl-dev openssl wget python3 python3-pip
[[ $os = 'centos' ]] && yum install -y gcc make openssl-devel wget centos-release-scl &&
    yum install -y rh-python36-python rh-python36-python-pip &&
    python3="/opt/rh/rh-python36/root/usr/bin/python3" && pip3="/opt/rh/rh-python36/root/usr/bin/pip3"
[[ $os = 'archlinux' ]] && pacman -Sy --noconfirm gcc make openssl wget python python-pip
[[ $os = 'fedora' ]] && dnf install -y gcc make openssl openssl-devel wget python python-pip

rm -rf dns-server
"$pip3" install pyOpenSSL dnslib pycryptodome pycryptodomex || exit 2

wget "$git_archive_url" -O dns-server.tar.gz &&
    tar xvzf dns-server.tar.gz &&
    mv dns-server /opt &&
    echo dns-server installtion done, at /opt/dns-server. ||
    exit $?

wget "$conf_url" -O dns-server.conf &&
    mv dns-server.conf /opt/dns-server/ &&
    echo configuration installation done, at /opt/dns-server/dns-server.conf. ||
    exit $?

echo "
[Unit]
Description=DNS Server Service

[Service]
TimeoutStartSec=0
ExecStart=$python3 /opt/dns-server/server.py 0.0.0.0:53 /opt/dns-server/dns-server.conf

[Install]
WantedBy=multi-user.target
" > /tmp/dns-server.m.service &&
    mv /tmp/dns-server.m.service /etc/systemd/system/ &&
    systemctl enable dns-server.m.service --now &&
    sleep 2 &&
    ps aux | grep -v grep | grep dns-server &&
    echo Systemd setup done. ||
    exit $?



