import socket
import _thread
import sys

def recv_data():
    #Receive data from other clients connected to server
    while 1:
        try:
            recv_data = client_socket.recv(4096)            
        except:
            #Handle the case when server process terminates
            print("Server closed connection, thread exiting.")
            _thread.interrupt_main()
            break
        if not recv_data:
                # Recv with no data, server closed connection
                print("Server closed connection, thread exiting.")
                _thread.interrupt_main()
                break
        else:
                print(recv_data.decode(),"")

def send_data():
    #Send data from other clients connected to server
    while 1:
        send_data = input()
        if send_data == "q" or send_data == "Q":
            client_socket.send(send_data.encode())
            _thread.interrupt_main()
            break
        else:
            client_socket.send(send_data.encode())
        
if __name__ == "__main__":

    print("AUCTIONING SYSTEM")
    print("Connecting to server at 192.168.94.1:5000")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.94.1', 5000))
    intro=client_socket.recv(1024)
    print (intro.decode())
    intro1 = client_socket.recv(1024)
    print(intro1.decode())
    print("Connected to server at 192.168.94.1:5000")
    print("Enter your bids(q or Q to quit):")

    _thread.start_new_thread(recv_data,())
    _thread.start_new_thread(send_data,())

    try:
        while 1:
            continue
    except:
        print("Client program quits....")
        client_socket.close()