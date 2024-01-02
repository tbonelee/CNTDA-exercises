# multithreaded web server
from socket import *
from threading import *

def handle_request_in_thread(connection_socket, client_address):

    try:
        # receive message from the client
        message = connection_socket.recv(1024)
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



# create a TCP socket
server_socket = socket(AF_INET, SOCK_STREAM)

# bind the socket to server address and server port
PORT = 12000
server_socket.bind(('', PORT))

# listen
server_socket.listen()

while True:
    # establish the connection
    print('Ready to serve...')
    connection_socket, client_address = server_socket.accept()

    # thread for handling the request
    thread = Thread(target=handle_request_in_thread, args=(connection_socket, client_address))
    thread.start()

server_socket.close()