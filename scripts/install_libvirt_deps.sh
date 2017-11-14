#!/bin/bash

if [ "${1}99" != "99" ]; then
    LP_PATH=${1}
else
    LP_PATH=${PWD}
fi

if [ "${USER}" != "root" ]; then
    sudo dnf install libvirt-devel -yq
    sudo dnf install libguestfs-tools python-libguestfs -yq
else
    dnf install libvirt-devel -yq
    dnf install libguestfs-tools python-libguestfs -yq
fi

pip install ${LP_PATH}\[libvirt\]

if [ -n "${VIRTUAL_ENV}" ]; then
   ${PWD}/scripts/install_selinux_venv.sh
fi
