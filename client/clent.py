from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

BUFSIZE = 1024


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZE).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError("Client propably left :("):
            break


def send(event=None):
    if msg:
        if msg.get() != "{quit}":
            client_socket.send(bytes(msg.get(), "utf8"))
            msg.set("")
        else:
            client_socket.send(bytes(msg.get(), "utf8"))
            client_socket.close()
            top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    msg.set("{quit}")
    send()


def set_defaults():
    """
    Invoked when the user didn't pass one of the two required data
    :return:
    """
    return 30300, "127.0.0.1"


if __name__ == "__main__":
    print("You don't have top write anything if you haven't change settings in server file")
    host = input("Give the server ip address to which u connect")
    port = input("please give the port on which the app will work")
    if not host or not port:
        port, host = set_defaults()
    port = int(port)
    addr = (host, port)
    client_socket = socket(AF_INET, SOCK_STREAM) # creating socket for a client
    client_socket.connect(addr)

    top = tkinter.Tk() # creating our window object
    top.title("Chatter")
    message_frame = tkinter.Frame(top)
    msg = tkinter.StringVar()
    msg.set("Type your messages here.")
    scrollbar = tkinter.Scrollbar(message_frame)
    message_frame.pack()
    # there we place our received messages
    msg_list = tkinter.Listbox(message_frame, height=15, width=60, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    # entry field part
    entry_field = tkinter.Entry(top, textvariable=msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()
    top.protocol("WM_DELETE_WINDOW", on_closing)

    #simply starts a thread which handles receiving messages
    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()

