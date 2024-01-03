# UDP heartbeat client
from socket import *
import random
import time

# Create a UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)

idx = 0
while True:
    # Send message
    message = f'Heartbeat {idx}'
    idx += 1

    # Generate random number in the range of 0 to 3
    rand = random.randint(0, 3)
    # sleep for rand seconds
    print(f'Sleep for {rand} seconds')
    time.sleep(rand)
    client_socket.sendto(message.encode(), ('localhost', 12000))
