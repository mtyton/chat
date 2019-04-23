# chat
a simple chat, written with python standard library
# How to run it?
## Requirements
You have to run it with python3.
On linux it's necessary to install _tkinter:
  to install this you just type:
  ```apt-get install python3-tk``` - works with Debian machines
  ```dnf install python3-tkinter ``` - on Fedora
  
## Server
Simply go to the server directory and start it with command 
```python main.py ```
Defaultly server runs on a port:30300 and on localhost ip adress
## Client
Simply go to the client directory and start it with command
```python client.py ```
Programme will ask you to pass two data, ip and port, you don't have to do that if your server is running on a default settings.
after showing up the window just send your username first

##TODO:
- write some tests
- add some kind of binary to launch it easier
