# UDP heartbeat server
# We will need the following module to generate randomized lost packets
from socket import *
import time

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
server_socket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
LIVENESS_TIMEOUT_SECONDS = 3
server_socket.settimeout(LIVENESS_TIMEOUT_SECONDS)
server_socket.bind(('', 12000))

while True:
    # Receive the client packet along with the address it is coming from
    try:
        message, address = server_socket.recvfrom(1024)
        print(f'Received heartbeat from {address}', message.decode())
    except timeout:
        print('Heartbeat timeout')
        break