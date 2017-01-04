#!/usr/bin/python
import json
import subprocess
import os
import sys
from collections import namedtuple
from ansible.module_utils.basic import *
import pprint
DMI_FACT = {}
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
    else:
#        command_cat = "sudo cat "
#        data = (subprocess.Popen(command_cat, stdout=subprocess.PIPE, shell=True)).communicate()
        data = subprocess.check_output(["/usr/bin/cat", path])
    return data

for (key, path) in DMI_DICT.items():
    data = get_file_content(path)
    if data is not None:
#       print json.dumps({key : data})
        DMI_FACT[key] = data.strip()



#pprint.pprint(DMI_FACT)


def main():
    module = AnsibleModule(argument_spec={})
    module.exit_json(changed=False, meta=DMI_FACT)

if __name__ == '__main__':
    main()
