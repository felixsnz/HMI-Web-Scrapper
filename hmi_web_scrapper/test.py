import ftplib
import configparser
import os

config = configparser.ConfigParser()
config.read('../config.ini')

hmi_ip_address = config['hmi']['ip']
hmi_user = config['hmi']['user']
hmi_password = config['hmi']['password']

ftp = ftplib.FTP(hmi_ip_address)
ftp.login(hmi_user, hmi_password)

#ftp.cwd("logs")
#ftp.cwd("")

from ftplib import FTP

def handle_list_line(line):
    parts = line.split(maxsplit=8)
    if len(parts) == 9:
        perms, _, _, _, _, _, _, _, name = parts
        if perms[0] == 'd':
            print('Folder: ', name)

ftp.retrlines('LIST', handle_list_line)

ftp.quit()