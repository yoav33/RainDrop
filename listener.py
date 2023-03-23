# ygCloud RainDrop: Individual listener
import socket
import os
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
    sock.bind(("0.0.0.0", int(PORT)))
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
                print("----------------------------------")
                print(f"{basename} successfully received!")
                print(f"file sender: {sock.getsockname()}")
                print("sending acknowledgement.")
                ready = "ready to receive file"
                print("file received")
                conn.sendall(bytes(ready, 'utf-8'))
                os.chdir('..')
                break
            f.write(bytes_read)

main(sock)