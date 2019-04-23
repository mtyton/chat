from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from msg import Message
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
    """
    starts after client connected, simply sends history of chat to the client
    history - messages since the server was started
    :param client:
    :return:
    """
    for message in sended_messages:
        client.send(bytes(message.prefix+": ", "utf8") + message.text)
        time.sleep(0.05)


def accept_connection():
    """
    Simply accepts connection from clients
    :return:
    """
    while True:
        client, client_address = SERVER.accept()
        client.send(bytes("Welcome on chat, first send your username", "utf8"))
        adresses[client] = client_address
        Thread(target=handle_client, args=(client, )).start()


def handle_client(client):
    """
    Receives message from exact client and broadcasts it
    :param client:
    :return:
    """
    client_name = client.recv(BUFSIZE).decode("utf8")
    ip = client.getsockname()[0]
    print("{}@{}".format(client_name, ip))
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
    """
    Simply sends message to every client
    :param message:
    :param prefix:
    :return:
    """
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
