# ygCloud RainDrop MAIN: Settings/other client configurator
import time
import socket
import os

sock = socket.socket()

HOST = 'localhost'
PORT = 1777
PASSKEY = 6969

def main(sock, format, file):
    print(f"trying to connect socket to {HOST}:{PORT} with passkey {PASSKEY}")
    sock.connect((HOST, PORT))
    print('socket connected. sending passkey...')
    pk = f"passkey={PASSKEY}"
    print(f"sending={pk}")
    encPk = bytes(pk, 'utf-8')
    sock.sendall(encPk)
    result = sock.recv(1024)
    print(f"received: {result.decode()}")
    if result.decode() == "sendformat":
        print("passkey verified and requested to send format")
        sock.sendall(bytes(format, 'utf-8'))
        encack = sock.recv(1024)
        print(encack.decode())
        if encack.decode() == "ready to receive file":
            sendFile(sock, file)

    else:
        if result.decode() == "passkeyrejected":
            print("passkey has been rejected. closing socket and returning None...")
            sock.close()
            return None
        else:
            print(f"unexpected message received: {result.decode()}")
            print("exiting...")
            exit()

def sendFile(sock, filepath):
    print("------------------ file sender ------------------")
    sock.sendall(bytes(filepath, 'utf-8'))
    print("sent file path...")
    size = os.path.getsize(filepath)
    sock.sendall(bytes(str(size), 'utf-8'))
    print("sent file size...")
    print("starting file send. do not quit if this looks stuck!")
    basename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        print(f"reading '{basename}'...")
        readbytes = f.read(int(size))
        if not readbytes:
            print("file received. closing socket and breaking...")
            sock.close()
            return None
        print(f"sending '{basename}'...")
        sock.sendall(readbytes)
        print(f"'{basename}' has been successfully sent.")

print("enter path for file to be sent:")
filepath = input("> ")
main(sock, "file", filepath)