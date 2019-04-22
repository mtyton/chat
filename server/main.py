from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from Messages.msg import Message
import time


clients = {}
adresses = {}
sended_messages = []

HOST = "127.0.0.1"
PORT = 30300
BUFSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def send_history_to_client(client):
    for message in sended_messages:
        client.send(bytes(message.prefix+": ", "utf8") + message.text)
        time.sleep(0.05)


def accept_connection():
    while True:
        client, client_address = SERVER.accept()
        client.send(bytes("Welcome on chat, first send your username", "utf8"))
        adresses[client] = client_address
        Thread(target=handle_client, args=(client, )).start()


def handle_client(client):
    client.send(bytes("If you want to quit just write {quit}", "utf8"))
    client_name = client.recv(BUFSIZE).decode("utf8")
    print("{} joined the chat".format(client_name))
    clients[client] = client_name
    msg = "{} has joined the chat".format(client_name)
    send_history_to_client(client)
    broadcast(bytes(msg, "utf8"))
    while True:
        msg = client.recv(BUFSIZE).decode("utf8")
        if msg != "{quit}":
            broadcast(bytes(msg, "utf8"), client_name)
        else:
            client.close()
            del clients[client]
            msg = "{} has left the chat".format(client_name)
            broadcast(bytes(msg, "utf8"))
            break


def broadcast(message, prefix=""):
    mess = Message(message, prefix)
    sended_messages.append(mess)
    for sock in clients:
        sock.send(bytes(prefix+": ", "utf8") + message)


if __name__  == "__main__":
    SERVER.listen(5)
    print("Waiting for connections")
    accept_thread = Thread(target=accept_connection)
    accept_thread.start()
    accept_thread.join()
    SERVER.close()
