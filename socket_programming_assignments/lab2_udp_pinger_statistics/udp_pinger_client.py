from socket import *
import time

# Create a UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)
# Set a timeout value of 1 second
client_socket.settimeout(1)
# Ping to server

SERVER_HOST = 'localhost'
SERVER_PORT = 12000
samples = []
for i in range(10):
    start = time.time()
    message = f'Ping {i+1} {time.time()}'
    client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
    try:
        data, server = client_socket.recvfrom(1024)
        end = time.time()
        print(f'{data.decode()} {end - start}')
        samples.append(end - start)
    except timeout:
        print('Request timed out')

client_socket.close()


# min, max, avg
print()
print(f"min, max, avg for RTT(sample size = {len(samples)})")
print(f'min: {min(samples)}')
print(f'max: {max(samples)}')
print(f'avg: {sum(samples)/len(samples)}')