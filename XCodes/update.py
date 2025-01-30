#!/usr/bin/python3
import os
import json
import base64
# import urllib2
from itertools import cycle, zip_longest as izip
from itertools import zip_longest

rConfigPath = '/home/xtreamcodes/iptv_xtream_codes/config'
linkupdate = 'https://xtreamtools.org/XCodes/update.zip'
linkupdate2 = 'https://dl.dropboxusercontent.com/scl/fi/34md6ri77tl17x0asvmwf/update.zip?rlkey=fhn0iuwcgwyk9jgqr6nbq8bgc'

class bcolors:
    ODINHEADER = '\033[95m'
    ODINBLUE = '\033[94m'
    ODINGREEN = '\033[92m'
    ODINWARNING = '\033[93m'
    ODINFAIL = '\033[91m'
    ODINENDC = '\033[0m'


def doDecrypt():
    rDecrypt = decrypt()
    if rDecrypt:
        # print ("Server ID: %s%d" % (" "*10, int(rDecrypt["server_id"])))
        # print ("Host: %s%s" % (" "*15, rDecrypt["host"]))
        # print ("Port: %s%d" % (" "*15, int(rDecrypt["db_port"])))
        # print ("Username: %s%s" % (" "*11, rDecrypt["db_user"]))
        # print ("Password: %s%s" % (" "*11, rDecrypt["db_pass"]))
        # print ("Database: %s%s" % (" "*11, rDecrypt["db_name"]))
        mserverid = int(rDecrypt["server_id"])
        mhost = rDecrypt["host"]
        mysqlport = int(rDecrypt["db_port"])
        mysqlusername = rDecrypt["db_user"]
        mysqlpassword = rDecrypt["db_pass"]
        mysqldatabase = rDecrypt["db_name"]

        # MYSQL UPDATE QUERY
        updatequery = 'DROP TABLE IF EXISTS odin_blocker; CREATE TABLE odin_blocker (id int(11) NOT NULL AUTO_INCREMENT,timestamp datetime DEFAULT NULL,ip varchar(255) DEFAULT NULL,PRIMARY KEY (id));'

        mysql_cmd = ('mysql -u {} -p{} {} -e "{}" 2> /dev/null'.format(mysqlusername, mysqlpassword, mysqldatabase, updatequery))
        # 2> /dev/null - put end the command to supress warning myslql secure.

        # Run the MySQL command using os.system
        os.system(mysql_cmd)
    else:
        print("Config file could not be read!")


def decrypt():
    try:
        with open(rConfigPath, 'rb') as f:
            data = f.read()

        decoded_data = base64.b64decode(data)
        decrypted_data = ''.join(chr(c ^ k) for c, k in zip(decoded_data, cycle(b'5709650b0d7806074842c6de575025b1')))
        result = json.loads(decrypted_data)
        # print(result)
        return result
    except:
        return None


print(bcolors.ODINHEADER + 'INSTALLING PREREQUISITES' + bcolors.ODINENDC)
os.system('apt-get update > /dev/null && apt-get upgrade -y > /dev/null')
os.system('apt-get install unzip e2fsprogs python3-paramiko -y > /dev/null')
os.system('chattr -i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null')
os.system('rm -rf /home/xtreamcodes/iptv_xtream_codes/admin > /dev/null')
os.system('rm -rf /home/xtreamcodes/iptv_xtream_codes/pytools > /dev/null')
print(bcolors.ODINHEADER + 'DOWNLOADING UPDATE...' + bcolors.ODINENDC)
os.system('wget -O /tmp/update.zip "{}" 2>/dev/null'.format(linkupdate))
os.system('wget -O /tmp/update.zip "{}" 2>/dev/null'.format(linkupdate2))
print('APPLYING UPDATE...')
os.system('unzip /tmp/update.zip -d /tmp/update/ > /dev/null')
os.system('cp -rf /tmp/update/XtreamUI-master/* /home/xtreamcodes/iptv_xtream_codes/ > /dev/null')
os.system('rm -rf /tmp/update/XtreamUI-master > /dev/null')
os.system('rm /tmp/update.zip > /dev/null')
os.system('rm -rf /tmp/update > /dev/null')
print(bcolors.ODINHEADER + "INSTALLING AND UPDATING YOUTUBE MODULE" + bcolors.ODINENDC)
os.system("sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl 2> /dev/null")
os.system("sudo chmod a+rx /usr/local/bin/youtube-dl > /dev/null")
os.system("cp /usr/local/bin/youtube-dl /home/xtreamcodes/iptv_xtream_codes/bin/ > /dev/null")
os.system("sudo chmod a+rx /home/xtreamcodes/iptv_xtream_codes/bin/youtube-dl > /dev/null")
os.system('chown -R xtreamcodes:xtreamcodes /home/xtreamcodes/ > /dev/null')
os.system('chmod +x /home/xtreamcodes/iptv_xtream_codes/permissions.sh > /dev/null')
os.system('/home/xtreamcodes/iptv_xtream_codes/permissions.sh > /dev/null')
os.system('find /home/xtreamcodes/ -type d -not \( -name .update -prune \) -exec chmod -R 777 {} + > /dev/null')
print(bcolors.ODINHEADER + 'RESTARTING ODIN SERVICES...' + bcolors.ODINENDC)
os.system('/home/xtreamcodes/iptv_xtream_codes/start_services.sh > /dev/null')
os.system('chattr +i /home/xtreamcodes/iptv_xtream_codes/GeoLite2.mmdb > /dev/null')
print(' ')
print(bcolors.ODINBLUE + 'UPDATING YOUR DATABASE IF NEEDED' + bcolors.ODINENDC)

                # Starting mysql update querys.
                # DECOMPILE TO GET USER AND PASSWORD FROM MYSQL CONFIG
doDecrypt()  # install the new database tables

