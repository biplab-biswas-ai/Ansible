#!/usr/bin/python
import json
import subprocess
import os
import sys
from collections import namedtuple
from ansible.module_utils.basic import *

Options = namedtuple('Options',
                ['connection', 'module_path', 'forks', 'become',
                 'become_method', 'become_user', 'check']
            )
options = Options(
    connection='local', module_path='', forks=1, become=True,
    become_method='sudo', become_user='root', check=False)



DMI_DICT = {
                    'bios_date': '/sys/devices/virtual/dmi/id/bios_date',
                    'bios_version': '/sys/devices/virtual/dmi/id/bios_version',
                    'form_factor': '/sys/devices/virtual/dmi/id/chassis_type',
                    'product_name': '/sys/devices/virtual/dmi/id/product_name',
                    'product_serial': '/sys/devices/virtual/dmi/id/product_serial',
                    'product_uuid': '/sys/devices/virtual/dmi/id/product_uuid',
                    'product_version': '/sys/devices/virtual/dmi/id/product_version',
                    'system_vendor': '/sys/devices/virtual/dmi/id/sys_vendor'
                    }
def get_file_content(path, default=None, strip=True):
    data = default
    if os.path.exists(path) and os.access(path, os.R_OK):
        try:
            try:
                datafile = open(path)
                data = datafile.read()
                if strip:
                    data = data.strip()
                if len(data) == 0:
                    data = default
            finally:
                datafile.close()
        except:
            # ignore errors as some jails/containers might have readable permissions but not allow reads to proc
            # done in 2 blocks for 2.4 compat
            pass
    return data

for (key, path) in DMI_DICT.items():
    data = get_file_content(path)
    if data is not None:
        print key, ':', data




#command_ls = 'sudo ls /sys/devices/virtual/dmi/id/product_*'
#ls_exec = (subprocess.Popen(command_ls, stdout=subprocess.PIPE, shell=True)).communicate()
#for i in ls_exec:
#    if i:
#      print basename(i),
