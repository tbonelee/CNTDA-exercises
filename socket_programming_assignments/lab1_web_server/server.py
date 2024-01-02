# import socket module
from socket import *
import sys # In order to terminate the program

server_socket = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket
PORT = 6789
server_socket.bind(('', PORT))
server_socket.listen(1)


while True:
    # Establish the connection
    print('Ready to serve...')
    connection_socket, addr = server_socket.accept()

    try:
        message = connection_socket.recv(1024) # ex) GET /hello.html HTTP/1.1
        filename = message.split()[1]
        f = open(filename[1:])
        output_data = f.read() # Read until EOF
        # Send one HTTP header line into socket
        connection_socket.send('HTTP/1.1 200 OK\r\n\r\n'.encode()) # body와 header를 구분

        # Send the content of the requested file to the client
        for i in range(0, len(output_data)):
            connection_socket.send(output_data[i].encode())
        connection_socket.send("\r\n".encode()) # body 끝을 알리기 위해


    except IOError:
        print('IOError')
        # Send response message for file not found
        connection_socket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())

        pass
    finally:
        # Close client socket
        connection_socket.close()


server_socket.close()

sys.exit() # Terminate the program after sending the corresponding data