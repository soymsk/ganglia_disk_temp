# -*- coding: utf-8 -*-
import os
import re
import random
from subprocess import check_output

NAME_PREFIX = 'disk_temp'

def get_disktemp(name):
    disk = name.replace(NAME_PREFIX + '_', '')
    disk_info = check_output(['sudo', '/sbin/smartctl', '-a', '/dev/%s' % disk])
    temp_line = [line for line in disk_info.split('\n') if line.find('Temp') >= 0][0]
    return float(re.split('[\s\t]+', temp_line)[-1])

def metric_init(params):
    units = 'Celcius'
    disks = ['sda']
    descriptors = [{
        'name': '_'.join([NAME_PREFIX, disk]), # metircs name
        'call_back': get_disktemp,
        'time_max': 60,
        'value_type': 'float',
        'units': units,
        'slope': 'both',
        'format': '%f',
        'description': 'Disk temperature (%s) on disk /dev/%s' % (units, disk),
        'groups': 'disk'
    } for disk in disks]
    return descriptors

def metric_cleanup():
    pass

if __name__ == '__main__':
    print get_disktemp('_'.join([NAME_PREFIX, 'sda']))
