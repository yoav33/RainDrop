# ygCloud RainDrop: Individual listener
import socket
import os
import subprocess
import configparser
import time
from context_menu import menus

PORT = 1777
HOST = '0.0.0.0'
PASSKEY = 6969
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addcopy = "n"

def listenloop(sock):
    sock.listen()

def main(sock):
    # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('waiting for client connection...')
    sock.listen(1)
    print(f"listening on: {HOST}:{PORT}")
    conn, addr = sock.accept()  # Note: execution waits here until the client calls sock.connect()
    data = conn.recv(1024)
    print(data.decode())
    expectedpk = f"passkey={PASSKEY}"
    print(f"expected={expectedpk}")
    if data.decode() == expectedpk:
        print("passkey verified! sending request to send format.")
        sf = f"sendformat"
        print(f"sending={sf}")
        encsf = bytes(sf, 'utf-8')
        conn.sendall(encsf)
        encformat = conn.recv(1024)
        format = encformat.decode()
        print(f"format={format}")
        print("------------------ forwarding to format receiver ------------------")
        # if statements for format: send to different receiving functions
        if format == "file":
            recvFile(sock, conn)
    else:
        print("passkey does not match! closing socket and returning None.")
        print("sending rejection...")
        rej = f"passkeyrejected"
        print(f"sending={rej}")
        encrej = bytes(rej, 'utf-8')
        conn.sendall(encrej)
        sock.close()
        return None

def recvFile(sock, conn):
    print("file receiver")
    ready = "ready to receive file"
    print("sending ready message...")
    conn.sendall(bytes(ready, 'utf-8'))
    encname = conn.recv(1024)
    name = encname.decode()
    print(f"name={name}")
    encsize = conn.recv(1024)
    size = encsize.decode()
    os.chdir("imports")
    basename = os.path.basename(name)
    print(f"basename={basename}")
    if addcopy == "y":
        while os.path.isfile(basename):
            basename = basename + " (copy)"
            print(f"file already exists in imports folder, adding '(copy)' to end of filename. {basename}")
        else:
            print("saving file name...")
    with open(basename, "wb") as f:
        print("receiving file. do not quit if this looks stuck!")
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = conn.recv(int(size))
            print(f"writing to '{basename}', hang on...")
            if not bytes_read:
                print("socket has been closed by sender")
                print("----------------------------------")
                print(f"{basename} successfully received!")
                print(f"file sender: {sock.getsockname()}")
                print("sending acknowledgement.")
                cdir = os.getcwd()
                #cdir = cdir + f"\{basename}"
                fileRecMenu(basename, cdir)
                os.chdir('..')
                break
            f.write(bytes_read)

def fileRecMenu(file, cdir):
    print(f"file received menu for: '{file}'")
    print(cdir)
    subprocess.Popen(fr'explorer "{cdir}"')
    print("opened imports folder.")

def verifyPasskey(sock, PASSKEY):
    encReq = ksock.recv(1024)
    Req = encReq.decode('utf-8')
    print(f"Req={Req}")
    if Req=="sendpasskey":
        pk = f"passkey={PASSKEY}"
        print(f"pk request confirmed. sending={pk}")
        encPk= bytes(pk, 'utf-8')
        ksock.sendall(encPk)
        encOutcome = ksock.recv(1024)
        outcome = encOutcome.decode('utf-8')
        print(f"outcome={outcome}")
        if outcome=='passkeyaccepted':
            print("accepted! sending acknowledgement")
            ack = bytes('approval acknowledged', 'utf-8')
            ksock.sendall(ack)
            encReq = ksock.recv(1024)
            Req = encReq.decode('utf-8')
            if Req=="sendpasskey":
                print("error: passkey requested again. exiting..")
                exit()
            if Req=='sendtask':
                print("requested to send task")
                task = bytes('raindroplistener', 'utf-8')
                ksock.sendall(task)
                encReq = ksock.recv(1024)
                Req = encReq.decode('utf-8')
                if Req == "sendlocalip":
                    print("requested local ip")
                    task = bytes(f"{ip}", 'utf-8')
                    ksock.sendall(task)
                    encReq = ksock.recv(1024)
                    Req = encReq.decode('utf-8')
                    if Req == "sendport":
                        task = bytes(f"{PORT}", 'utf-8')
                        ksock.sendall(task)
                        encReq = ksock.recv(1024)
                        Req = encReq.decode('utf-8')
                        if Req == "sendname":
                            print(f"name={username}")
                            task = bytes(username, 'utf-8')
                            ksock.sendall(task)
                            return None
                #sendTask(
                print("oopsie woopsie")
                input("error in communications to kyrios!! press ENTER to exit.")
                exit()

        else:
            print("rejected. exiting...")
            exit()
    else:
        print("request text does not match expectations!")

config = configparser.ConfigParser()
config.read(r'raindrop.conf')
username = (config.get('raindrop', 'username'))
kyrioshost = (config.get('kyrios', 'kyrioshost'))
kyriosport = (config.get('kyrios', 'kyriosport'))
kyriospasskey = (config.get('kyrios', 'kyriospasskey'))
hn = socket.gethostname()
ip = socket.gethostbyname(hn)
sock.bind(("0.0.0.0", int(PORT)))
print(f"local ip: {ip}")
print(f"port: {PORT}")
ksock = socket.socket()
print("kyrios sock initiated")
print(f"connecting to kyrios at {kyrioshost}:{kyriosport} with passkey {kyriospasskey}...")
connectionSuccessful = False
while not connectionSuccessful:
    try:
        ksock.connect((kyrioshost, int(kyriosport)))  # Note: if execution gets here before the server starts up, this line will cause an error, hence the try-except
        print('socket connected')
        connectionSuccessful = True
    except:
        pass
verifyPasskey(ksock, kyriospasskey)
while True:
    try:
        main(sock)
    except KeyboardInterrupt:
        print("kbi")