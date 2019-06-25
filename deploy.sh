#!/bin/bash

git_archive_url="https://cnm.cool/tmp/dns-server.tar.gz"
conf_url="https://cnm.cool/tmp/encrypted.cfg"
use_cython=1

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
prefix=""

# prepare
[[ $os = 'ubuntu' ]] || [[ $os = 'debian' ]] && apt update && apt install -y gcc make libssl-dev openssl wget python3 python3-pip python3-dev
[[ $os = 'centos' ]] && yum install -y gcc make openssl-devel wget centos-release-scl &&
    yum install -y rh-python36-python rh-python36-python-pip rh-python36-scldevel rh-python36-python-devel &&
    prefix="/opt/rh/rh-python36/root/" &&
    extra_systemd_line="Environment=\"LD_LIBRARY_PATH=$prefix/usr/lib64/\""
[[ $os = 'archlinux' ]] && pacman -Sy --noconfirm gcc make openssl wget python python-pip
[[ $os = 'fedora' ]] && dnf install -y gcc make openssl openssl-devel wget python python-pip

python3="$prefix/usr/bin/python3"
pip3="$prefix/usr/bin/pip3"

rm -rf dns-server /opt/dns-server
"$pip3" install pyOpenSSL dnslib pycryptodome pycryptodomex Cython || exit 2

wget "$git_archive_url" -O dns-server.tar.gz &&
    tar xvzf dns-server.tar.gz &&
    mv dns-server /opt &&
    cd /opt/dns-server &&
    PATH="$PATH:$prefix/usr/bin/" make &&
    cd - &&
    echo dns-server installtion done, at /opt/dns-server. ||
    exit $?

wget "$conf_url" -O dns-server.conf &&
    mv dns-server.conf /opt/dns-server/ &&
    echo configuration installation done, at /opt/dns-server/dns-server.conf. ||
    exit $?

if [[ $use_cython = 1 ]]; then
    server_exe="/opt/dns-server/server"
else
    server_exe="$python3 /opt/dns-server/server.py"
fi

echo "
[Unit]
Description=DNS Server Service

[Service]
TimeoutStartSec=0
ExecStart=$server_exe 0.0.0.0:53 /opt/dns-server/dns-server.conf
$extra_systemd_line

[Install]
WantedBy=multi-user.target
" > /tmp/dns-server.m.service &&
    mv /tmp/dns-server.m.service /etc/systemd/system/ &&
    systemctl enable dns-server.m.service --now &&
    sleep 2 &&
    ps aux | grep -v grep | grep dns-server &&
    echo Systemd setup done. ||
    exit $?



