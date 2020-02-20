import socket
import os
import sys
from time import sleep
import signal
from datetime import datetime


def check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


port = 3500

log = False
if len(sys.argv) >= 3:
    if sys.argv[1] == "-l":
        logfile = sys.argv[2]
        log = True
        lgf = open(logfile, "w")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', port))

name = input("What's your username? ")

print("Listening")
s.listen(3)

c, addr = s.accept()
print("Got connection from" + str(addr))

c2, addr2 = s.accept()

othername2 = c2.recv(1024).decode()
c.send(name.encode())

addr = othername2

if log:
    lgf.write("Conversation between " + str(name) + " and " + str(othername2) + "\n")

pid = os.fork()

if pid == 0:
    while True:
        message = c2.recv(1024).decode()
        if message == "!DC" or message == "":
            print(str(addr) + " has disconnected")
            if log:
                lgf.write(str(addr) + " has disconnected" + "\n")
                print(str(addr) + " has disconnected" + "\n")
            break
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string + " " + str(addr) + " sent: " + message)
        if log:
            lgf.write(dt_string + " " + str(addr) + " sent: " + message + "\n")
            print(dt_string + " " + str(addr) + " sent: " + message + "\n")
        print("Type a message: ")
    os.kill(os.getppid(),signal.SIGUSR1)
    os._exit(0)

def usrdisc(signum,stack):
    c.close()
    c2.close()
    s.close()
    lgf.close()
    os._exit(0)

signal.signal(signal.SIGUSR1, usrdisc)

while True:
    message2 = input()
    if message2[0] == '!' or not check_pid(pid):
        c.send("!DC".encode())
        os.kill(pid,signal.SIGTERM)
        break
    c.send(message2.encode())
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string + ": You sent: " + message2)
    if log:
        lgf.write(dt_string + " " + name + " sent: " + message2 + "\n")
    print("Type a message: ")

c.close()
c2.close()
s.close()
lgf.close()
