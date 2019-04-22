from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

BUFSIZE = 1024


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZE).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError("Cleint propably left :("):
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


if __name__ == "__main__":
    host = input("Give the server ip address to which u connect")
    port = int(input("please give the port on which the app will work"))
    addr = (host, port)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(addr)

    top = tkinter.Tk()
    top.title("Chatter")
    message_frame = tkinter.Frame(top)
    msg = tkinter.StringVar()
    msg.set("Type your messages here.")
    scrollbar = tkinter.Scrollbar(message_frame)
    message_frame.pack()
    msg_list = tkinter.Listbox(message_frame, height=15, width=60, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)



    entry_field = tkinter.Entry(top, textvariable=msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()
    top.protocol("WM_DELETE_WINDOW", on_closing)

    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()

