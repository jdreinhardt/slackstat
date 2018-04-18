#!python3
# 
# Slack Stat
# Easily send system monitoring to a Slack channel
# Requires a config file as input parameter
# 
# Author: Derek Reinhardt
# Email: derek.reinhardt@outlook.com
# Date: 18 Apr 2018
# Version: 1.0.1
# Status: Production
# 

import sys
import winstats
import json
import requests
import socket
from win32file import GetDriveType
import configparser
import queue
    
def getConfigValue(file, value):
    parser = configparser.SafeConfigParser()
    parser.read(file)
    return parser.get('config', value)

def getHostName():
    device_name = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    device_ip = s.getsockname()[0]
    return device_name + ' (' + device_ip + ')'

def getDriveStats(allow_remote):
    drives = winstats.get_drives()
    for drive in drives:
        vol_info = winstats.get_vol_info(drive)
        drive_type = GetDriveType(drive + ":\\")
        if (drive_type == 4 and allow_remote == 'False'):
            break
        else:
            drive_name = 'Drive: ' + drive + ' (' + vol_info.name + ') '
            fs_usages = winstats.get_fs_usage(drive)
            usage_percent = '{percent:.2%}'.format(percent=fs_usages.used/fs_usages.total)
            usage_stats = "Usage: " + usage_percent
            validateUsage(usage_percent, drive_name + usage_stats)
        

def getCPUStats():
    usage = winstats.get_perf_data(r'\Processor(_Total)\% Processor Time', fmts='double', delay=100)
    usage_percent = '%.02f%%' % usage[0]
    validateUsage(usage_percent, 'CPU Utilization at ' + usage_percent)

def getMemoryStats():
    mem_info = winstats.get_mem_info()
    usage_percent = str(mem_info.MemoryLoad) + '%'
    validateUsage(usage_percent, 'Memory Usage at ' + usage_percent)

def validateUsage(usage_percent, stat_string):
    USERNAME_OVERRIDE = getConfigValue(configFile, 'USERNAME_OVERRIDE')
    hostname = getHostName()

    danger_string = '*DANGER* on ' + hostname
    warning_string = '*WARNING* on ' + hostname
    advisory_string = '*ADVISORY* on ' + hostname
    if (USERNAME_OVERRIDE == 'SystemID'):
        danger_string = '*DANGER*'
        warning_string = '*WARNING*'
        advisory_string = '*ADVISORY*'
    
    DANGER_LIMIT = getConfigValue(configFile, 'DANGER_LIMIT')
    WARNING_LIMIT = getConfigValue(configFile, 'WARNING_LIMIT')
    ADVISORY_LIMIT = getConfigValue(configFile, 'ADVISORY_LIMIT')

    if (float(usage_percent.strip(' \t\n\r%')) > float(DANGER_LIMIT)):
        notification = danger_string + '\n' + stat_string
    elif (float(usage_percent.strip(' \t\n\r%')) > float(WARNING_LIMIT)):
        notification = warning_string + '\n' + stat_string
    elif (float(usage_percent.strip(' \t\n\r%')) > float(ADVISORY_LIMIT)):
        notification = advisory_string + '\n' + stat_string
    else:
        return

    sendSlackNotification(hostname, notification, USERNAME_OVERRIDE)

def sendSlackNotification(hostname, notification, USERNAME_OVERRIDE):
    SLACK_WEBHOOK = getConfigValue(configFile, 'SLACK_WEBHOOK')
    ICON_OVERRIDE = getConfigValue(configFile, 'ICON_OVERRIDE')
    CHANNEL_OVERRIDE = getConfigValue(configFile, 'CHANNEL_OVERRIDE')

    payload = {}
    payload['text'] = notification
    if (USERNAME_OVERRIDE == "SystemID"):
        payload['username'] = hostname
    elif (USERNAME_OVERRIDE != "''"):
        payload['username'] = USERNAME_OVERRIDE
    if (ICON_OVERRIDE != "''"):
        payload['icon_url'] = ICON_OVERRIDE
    if (CHANNEL_OVERRIDE != "''"):
        payload['channel'] = CHANNEL_OVERRIDE

    requests.post(SLACK_WEBHOOK, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

def main(argv):
    if (len(argv) == 0):
        print("Must provide config file")
    if (len(argv) == 1):
        global configFile
        configFile = argv[0]

        MONITOR_CPU = getConfigValue(configFile, 'MONITOR_CPU')
        MONITOR_MEMORY = getConfigValue(configFile, 'MONITOR_MEMORY')
        MONITOR_DRIVES = getConfigValue(configFile, 'MONITOR_DRIVES')
        ALLOW_REMOTE_DISK = getConfigValue(configFile, 'ALLOW_REMOTE_DISK')

        if (MONITOR_CPU == 'True'):
            getCPUStats()
        if (MONITOR_MEMORY == 'True'):
            getMemoryStats()
        if (MONITOR_DRIVES == 'True'):
            getDriveStats(ALLOW_REMOTE_DISK)

if __name__ == '__main__':
    main(sys.argv[1:])
