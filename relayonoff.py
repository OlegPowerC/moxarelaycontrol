import time
import datetime
import paramiko as paramiko
import configparser
import keyring
import argparse

CONFIGCOMMAND = "conf t"
WRITECOMMAND = "save"
TIMEOUTREGULARCOMMSNDSEC = 1
TIMEOUTLONGCOMMANDSEC = 3

def domassconfig(PGFG, logfile, WriteToLog,timeout_intercmd):
    for confcmd in PGFG:
        chan.send(confcmd + '\n')
        time.sleep(int(timeout_intercmd))
    ret = chan.recv(99999)
    rstr1 = ret.decode('utf-8')
    if DEBUG:
        print(rstr1)
    if WriteToLog == 1:
        logfile.write(rstr1)


if __name__ == '__main__':
    WriteToLog = 0
    DEBUG = False
    parcer = argparse.ArgumentParser(description="MOXA EDS-510/518 relay on/off")
    parcer.add_argument('-i', type=str, help="switch IP", required=True)
    parcer.add_argument('-c', type=str, help="file with commands", required=True)
    parcer.add_argument('-l', type=str, help="write log")
    parcer.add_argument('-u', type=str, help="Username - if You want use other Username rather User in config file")
    parcer.add_argument('-p', type=str, help="Password - if You want use other Username rather User in config file")
    parcer.add_argument('-f', type=str, default="configmoxa.txt", help="config - default 'moxaconfig.txt")
    args = parcer.parse_args()

    now = datetime.datetime.now()

    cpsw = configparser.ConfigParser()

    cpcmd = configparser.ConfigParser()
    cpcmd.read(args.c)

    if args.u != None:
        if args.p == None:
            print("Please provide passowrd")
            exit(1)
        USER = args.u
        PASSWORD = args.p
    else:
        configname = 'configmoxa.txt'
        cp = configparser.ConfigParser()
        cp.read(args.f)

        USER = cp.get('access', 'username')
        KEYCHAINNAME = cp.get('access', 'keychainname')

        # Читаем из Keyring OS пароль нашего пользователя
        PASSWORD = keyring.get_password(KEYCHAINNAME, USER)

    HOST = args.i
    logfileneme = None

    if args.l != None:
        WriteToLog = 1
        logfileneme = 'sessionlog.txt'
        logtofile = open(logfileneme, 'a')

    cmdparam = cpcmd.get('configcmd', 'ccmd')
    cmdstr = cpcmd.get('cmd', cmdparam)
    CONFCOMMAND = cmdstr.split('\n')

    timeout_intercmd =  cpcmd.get('timesettings', 'timeout')

    if DEBUG:
        print(CONFCOMMAND)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # apply command to each switch
    try:
        client.connect(HOST, username=USER, password=PASSWORD)
        if DEBUG:
            print("connected")
        if WriteToLog == 1:
            logtofile.write((HOST + ' ' + 'connected' + '\r\n'))
        chan = client.invoke_shell()
        time.sleep(TIMEOUTREGULARCOMMSNDSEC)
        chan.send('term len 0\n')
        time.sleep(TIMEOUTREGULARCOMMSNDSEC)

        output = chan.recv(99999)
        if DEBUG:
            print(output.decode('utf-8'))
        if WriteToLog == 1:
            logtofile.write(output.decode('utf-8'))

        chan.send(CONFIGCOMMAND + '\n')
        time.sleep(TIMEOUTREGULARCOMMSNDSEC)
        ret = chan.recv(99999)

        if DEBUG:
            print(ret.decode('utf-8'))

        domassconfig(CONFCOMMAND, logfileneme, WriteToLog,timeout_intercmd)

        chan.send('exit\n')
        time.sleep(TIMEOUTREGULARCOMMSNDSEC)
        chan.send(WRITECOMMAND + '\n')
        time.sleep(TIMEOUTLONGCOMMANDSEC)
        ret = chan.recv(99999)

        if DEBUG:
            print(ret.decode('utf-8'))
        if WriteToLog == 1:
            logtofile.write(ret.decode('utf-8'))
        client.close()
        if WriteToLog == 1:
            logtofile.write((HOST + ' ' + 'disconnected' + '\r\n'))
    except Exception as e:
        print(e)
        if WriteToLog == 1:
            logtofile.write((HOST + ' ' + str(e) + '\r\n'))
if WriteToLog == 1:
    logtofile.close()
