# ygCloud RainDrop MAIN: Settings/other client configurator
import time
import socket
import os
from PIL import ImageTk, Image
import configparser
from context_menu import menus

config = configparser.ConfigParser()
config.read(r'raindrop.conf')

kyrioshost = (config.get('kyrios', 'kyrioshost'))
kyriosport = (config.get('kyrios', 'kyriosport'))
kyriospasskey = (config.get('kyrios', 'kyriospasskey'))
print(f"kh={kyrioshost} kp={kyriosport} kpk={kyriospasskey}")

sock = socket.socket()
HOST = '172.18.80.1'
PORT = 1777
PASSKEY = 6969

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

def fileSent(filename):
    # file sent menu tkinter
    print("file sent menu")
    fs = tk.Tk()
    fs.title('RainDrop')
    fs.resizable(False, False)
    fs.geometry('300x150')
    fs.iconbitmap('icon.ico')
    img2 = ImageTk.PhotoImage(Image.open("RainDrop.png"))
    panel2 = ttk.Label(fs, image=img2)
    panel2.pack()
    sentl = ttk.Label(
        fs,
        text="The file has been successfully sent.",
        font=("Calibri", 10)
    )
    sentl.pack()
    fs.mainloop()

# fileSent("ya")

def main(sock, format, file, status):
    print(f"trying to connect socket to {HOST}:{PORT} with passkey {PASSKEY}")
    status.configure(text=f"Connecting to {HOST}:{PORT}")
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
            sendFile(sock, file, status)

    else:
        if result.decode() == "passkeyrejected":
            print("passkey has been rejected. closing socket and returning None...")
            sock.close()
            return None
        else:
            print(f"unexpected message received: {result.decode()}")
            print("exiting...")
            exit()

def sendFile(sock, filepath, status):
    print("------------------ file sender ------------------")
    sock.sendall(bytes(filepath, 'utf-8'))
    print("sent file path...")
    size = os.path.getsize(filepath)
    sock.sendall(bytes(str(size), 'utf-8'))
    print("sent file size...")
    print("starting file send. do not quit if this looks stuck!")
    basename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        #status.config(text='You pressed the button!')
        print(f"reading '{basename}'...")
        readbytes = f.read(int(size))
        if not readbytes:
            print("file received. closing socket and breaking...")
            sock.close()
            return None
        print(f"sending '{basename}'...")
        sock.sendall(readbytes)
        sock.close()
        print(f"'{basename}' has been successfully sent.")
        root.destroy()
        fileSent(basename)

# create the root window
root = tk.Tk()
root.title('RainDrop Sender')
root.resizable(False, False)
root.geometry('300x175')
root.iconbitmap('icon.ico')

def select_file():
    filetypes = (
        ('All files', '*.*'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if not os.path.isfile(filename):
        print("nah dawg")
        showinfo(
            title='RainDrop Error',
            message="File not selected."
        )
    else:
        #status.config(text='Sending file, hang on...')
        basename = os.path.basename(filename)
        #showinfo(
        #    title='Sending file...',
        #    message=f"Sending '{basename}'..."
        #)
        main(sock, "file", filename, status)

def verifyPasskey(sock, PASSKEY, status):
    encReq = sock.recv(1024)
    Req = encReq.decode('utf-8')
    print(f"Req={Req}")
    if Req=="sendpasskey":
        pk = f"passkey={PASSKEY}"
        print(f"pk request confirmed. sending={pk}")
        encPk= bytes(pk, 'utf-8')
        sock.sendall(encPk)
        encOutcome = sock.recv(1024)
        outcome = encOutcome.decode('utf-8')
        print(f"outcome={outcome}")
        if outcome=='passkeyaccepted':
            status.configure(text="Connected to Kyrios")
            print("accepted! sending acknowledgement")
            ack = bytes('approval acknowledged', 'utf-8')
            sock.sendall(ack)
            encReq = sock.recv(1024)
            Req = encReq.decode('utf-8')
            if Req=="sendpasskey":
                print("error: passkey requested again. exiting..")
                exit()
            if Req=='sendtask':
                print("requested to send task")
                #sendTask()

        else:
            status.configure(text="Could not connect to Kyrios! Check passkey.")
            print("rejected. exiting...")
    else:
        status.configure(text="Request error from Kyrios")
        print("request text does not match expectations!")


def clientlist():
    status.configure(text="Connecting to Kyrios...")
    ksock = socket.socket()
    ksock.connect((kyrioshost, int(kyriosport)))
    verifyPasskey(ksock, kyriospasskey, status)


status = ttk.Label(
    root,
    text="Not connected to Kyrios"
)

open_button = ttk.Button(
    root,
    text='Select file',
    command=select_file
)

client_button = ttk.Button(
    root,
    text='Select receiver',
    command=clientlist
)


img = ImageTk.PhotoImage(Image.open("RainDrop.png"))
panel = ttk.Label(
    root,
    image = img
)
panel.pack()
client_button.pack()
open_button.pack()
status.pack()

root.mainloop()