
import sys
from socket import *

# parse cli args
try:
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3] if not sys.argv[3].startswith('/') else sys.argv[3].split('/')[1]
except IndexError: # if not enough args
    print('index error')
    print('Usage: python client.py <server_host> <server_port> <filename>')
    sys.exit()
except ValueError: # if port is not int
    print('value error')
    print('Usage: python client.py <server_host> <server_port> <filename>')
    sys.exit()

# create socket
client_socket = socket(AF_INET, SOCK_STREAM) # SOCK_STREAM for TCP
client_socket.connect((server_name, server_port))

# send HTTP get request to f'/{filename}'
request = f'GET /{filename} HTTP/1.1\r\nHost: {server_name}:{server_port}\r\n\r\n'
client_socket.send(request.encode())

# receive HTTP response
response_message = ""
content_length = 0
while True:
    response = client_socket.recv(1024)
    if not response:
        print(response_message)
        sys.exit()
    response_message += response.decode()

    if "\r\n\r\n" in response.decode():
        try:
            content_length = int(response.decode().split('Content-Length: ')[1].split('\r\n')[0])
            break
        except IndexError:
            # no content length header just go on
            pass



length_without_body = len(response_message.split('\r\n\r\n')[0]) + 4

while len(response_message) - length_without_body < content_length:
    response = client_socket.recv(1024)
    response_message += response.decode()

print(response_message)