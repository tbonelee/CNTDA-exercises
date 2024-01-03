import sys
from socket import *

# parse cli args
# python smtp_client.py <sender> <receiver> <subject> <message>
try:
    mail_server = sys.argv[1]
    sender = sys.argv[2]
    receiver = sys.argv[3]
    subject = sys.argv[4]
except IndexError:
    print('Usage: python smtp_client.py <mail_server> <sender> <receiver> <subject>')
    sys.exit()


msg = "\r\n I love computer networks!"

endmsg = "\r\n.\r\n" # end of message of SMTP

# Choose a mail server (e.g. Google mail server) and call it mailserver

# Create socket called client_socket and establish a TCP connection with mailserver
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((mail_server, 587))

recv = client_socket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
    client_socket.close()
    sys.exit()


# Send HELO command and print server response.
client_hostname = 'localhost'
hello_command = f'HELO {client_hostname}\r\n'
client_socket.send(hello_command.encode())
recv1 = client_socket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')
    client_socket.close()
    sys.exit()


# Send MAIL FROM command and print server response.
mail_from_command = f'MAIL FROM: <{sender}>\r\n'
client_socket.send(mail_from_command.encode())
recv2 = client_socket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')
    client_socket.close()
    sys.exit()

# Send RCPT TO command and print server response.
rcpt_to_command = f'RCPT TO: <{receiver}>\r\n'
client_socket.send(rcpt_to_command.encode())
recv3 = client_socket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')
    client_socket.close()
    sys.exit()

# Send DATA command and print server response.
data_command = 'DATA\r\n'
client_socket.send(data_command.encode())
recv4 = client_socket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')
    client_socket.close()
    sys.exit()
# Send header
client_socket.send(f'Subject: {subject}\r\n'.encode())
client_socket.send(f'From: {sender}\r\n'.encode())
client_socket.send(f'To: {receiver}\r\n'.encode())
client_socket.send("\r\n".encode())
# Send message data.
client_socket.send(msg.encode())
# Message ends with a single period.
client_socket.send(endmsg.encode())
recv5 = client_socket.recv(1024).decode()
print(recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')
    client_socket.close()
    sys.exit()

# Send QUIT command and get server response.
quit_command = 'QUIT\r\n'
client_socket.send(quit_command.encode())
recv6 = client_socket.recv(1024).decode()
print(recv6)
if recv6[:3] != '221':
    print('221 reply not received from server.')
    client_socket.close()
    sys.exit()