import socket
import select
import time

def broadcast_data (sock, message):
    """Send broadcast message to all clients other than the
       server socket and the client socket from which the data is received."""
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:            
            socket.send(message.encode())

try:
    if __name__ == "__main__":
        # List to keep track of socket descriptors
        CONNECTION_LIST=[]
        # Do basic steps for server like create, bind and listening on the socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port=5000
        server_socket.bind(("192.168.94.1", port))
        server_socket.listen(10)

        # Add server socket to the list of readable connections
        CONNECTION_LIST.append(server_socket)
        itemData={}
        f = open("input.txt", "r")
        flines = f.readlines()
        for i in range(1,len(flines)):
            nline = flines[i].split()
            itemData[nline[0]] = int(nline[1]) #Puts data in dictionary organized by {"Item Name":[Units,Price]} for updating and reading
        print(itemData)
        f.close()
        for item in itemData:
            print(item)
            flag=False

            bprice=itemData[item]
            constbp=bprice

            print("Server process started...")
            flag2=True

            while flag2:
                # Get the list sockets which are ready to be read through select
                read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
                SOCK=CONNECTION_LIST[0]
                for sock in read_sockets:
                    if sock == server_socket:
                        # Handle the case in which there is a new connection recieved
                        # through server_socket
                        sockfd, addr = server_socket.accept()
                        CONNECTION_LIST.append(sockfd)
                        print("Client (%s, %s) connected" % addr)
                        data="Base price: "+str(constbp)
                        sockfd.send(data.encode())
                        data2="Current price: "+str(bprice)
                        sockfd.send(data2.encode())
                    else:
                        # Data recieved from client, process it
                        try:
                            #In Windows, sometimes when a TCP program closes abruptly,
                            # a "Connection reset by peer" exception will be thrown
                            data = sock.recv(4096)
                        except:
                            #broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                            print("Client (%s, %s) is offline" % addr)
                            sock.close()
                            CONNECTION_LIST.remove(sock)
                            if len(CONNECTION_LIST) == 2:
                                flag=True
                            data=False

                        if data:
                            data=data.decode()
                            # The client sends some valid data, process it
                            if data == "q" or data == "Q":
                                #broadcast_data(sock, "Client (%s, %s) quits" % addr)
                                print("Client (%s, %s) quits" % addr)
                                sock.close()
                                CONNECTION_LIST.remove(sock)
                                if len(CONNECTION_LIST) == 2:
                                    flag=True
                            elif int(data)>bprice:
                                bprice=int(data)
                                data="Current price: "+data
                                broadcast_data(sock, data)

                    if flag:
                        print("Item sold to Client(%s,%s)" %addr)
                        print("At price:",bprice)
                        sock=CONNECTION_LIST[1]
                        win="You won the item at price: "+str(bprice)
                        sock.send(win.encode())
                        time.sleep(2)
                        sock.close()
                        CONNECTION_LIST.remove(sock)
                        flag2=False                
        server_socket.close()	
except:
    print("Something went wrong!")
    for i in range(1,len(CONNECTION_LIST)):
        sock=CONNECTION_LIST[i]
        sock.close()