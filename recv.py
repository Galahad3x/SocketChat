import sys
import os
import socket
import signal
from datetime import datetime


def check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 3500

ip = input("Type other pc's IP: ")

s.connect((ip, port))

name = input("Write your username: ")

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((ip, port))

s2.send(name.encode())
othername = s.recv(1024).decode()

pid = os.fork()

if pid == 0:
    #addr = "(" + ip + "," + str(port) + ")"
    addr = othername
    while True:
        reciev = s.recv(1024).decode()
        if reciev == "!DC" or reciev == "":
            print(addr + " has disconnected")
            break
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string + " " + addr + " sent: " + reciev)
        print("Type a message: ")
    os.kill(os.getppid(),signal.SIGUSR1)
    os._exit(0)

def usrdisc(signum,stack):
    s.close()
    s2.close()
    os._exit(0)

signal.signal(signal.SIGUSR1, usrdisc)

dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

while True:
    message = input()
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if message[0] == '!' or not check_pid(pid):
        mess = "!DC"
        s2.send(mess.encode())
        os.kill(pid,signal.SIGTERM)
        break
    s2.send(message.encode())
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string + ": You sent: " + message)
    print("Type a message: ")

s.close()
s2.close()
