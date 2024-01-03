from socket import *
import time

# Create a UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)
# Set a timeout value of 1 second
client_socket.settimeout(1)
# Ping to server

SERVER_HOST = 'localhost'
SERVER_PORT = 12000
for i in range(10):
    start = time.time()
    message = f'Ping {i+1} {time.time()}'
    client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
    try:
        data, server = client_socket.recvfrom(1024)
        print(f'{data.decode()} {time.time() - start}')
    except timeout:
        print('Request timed out')

client_socket.close()
