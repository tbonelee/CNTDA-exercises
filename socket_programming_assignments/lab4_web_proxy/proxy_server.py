from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage: "python proxy_server.py server_ip"\n[ server_ip : It is the IP Address Of Proxy Server]')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcp_server_socket = socket(AF_INET, SOCK_STREAM)

# Fill in start.
server_ip = sys.argv[1]
server_port = 8888
tcp_server_socket.bind((server_ip, server_port))
tcp_server_socket.listen(1)
# Fill in end.

while True:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcp_client_socket, client_address = tcp_server_socket.accept()
    message = tcp_client_socket.recv(1024).decode()
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print('filename',filename)
    file_exist = "false"
    filetouse = "/" + filename
    print('filetouse',filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        file_exist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcp_client_socket.send("HTTP/1.0 200 OK\r\n".encode())
        tcp_client_socket.send("Content-Type:text/html\r\n".encode())
        # Fill in start.
        for i in range(0, len(outputdata)):
            tcp_client_socket.send(outputdata[i].encode())
        # Fill in end.
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if file_exist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            print('hostn',hostn)
            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn, 80))
                # Fill in end.
                # Create a temporary file on this socket and ask port 80
                # for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                fileobj.write(f"GET http://{filename} HTTP/1.0\n\n".encode())
                # Read the response into buffer
                # Fill in start.
                buff = fileobj.readlines()
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache
                tmpFile = open("./" + filename, "wb")
                # Fill in start.
                for i in range(0, len(buff)):
                    tmpFile.write(buff[i])
                    tcp_client_socket.send(buff[i])
                # Fill in end.
                tmpFile.close()
            except Exception as e:
                print("Illegal request", e, type(e))
        else:
            # HTTP response message for file not found
            # Fill in start.
            tcp_client_socket.send("HTTP/1.0 404 Not Found\r\n".encode())
            tcp_client_socket.send("Content-Type:text/html\r\n".encode())
            # Fill in end.
    # Close the client and the server sockets
    tcp_client_socket.close()
# Fill in start.
tcp_server_socket.close()
# Fill in end.