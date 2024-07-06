# Name:Leila Sarkamari
# Lab 5-CIS 41B 
import socket

def promt_user():
    '''
    function to prompt the user for a command, read in and validate the user's choice: the command must be one of the 4 choices above, and the command cd should have 1 word after it.

    '''
    print("Commands:")
    print("ls           list files")
    print("lsr          list directories recursively")
    print("cd dir_name  go to dir_name")
    print("q            quit")

def validate_command(command):
    parts = command.strip().split()
    if not parts:
        return False, "Invalid command"
    cmd = parts[0]
    if cmd not in ['ls', 'lsr', 'cd', 'q']:
        return False, "Invalid command"
    if cmd == 'cd' and len(parts) != 2:
        return False, "Invalid directory command format. Use 'cd dir_name'."
    return True, command

def process_change_directory_response(response):
    if response == 'success':
        print("Directory changed successfully")
    else:
        print("No such directory")

def process_listing_response(response, is_recursive):
    if is_recursive:
        print("Recursive listing:")
    else:
        print("Listing of current directory:")
    print(response)


server_ip = "127.0.0.1"
server_port = 5551

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

print(f"Connected to server at {server_ip}:{server_port}")
promt_user()

while True:
    command = input("Enter choice: ").strip()
    is_valid, validated_command_or_error = validate_command(command)

    if not is_valid:
        print(validated_command_or_error)
        continue

    if validated_command_or_error == 'q':
        client_socket.send(validated_command_or_error.encode('utf-8'))
        print("Connection closed by the client")
        break

    client_socket.send(validated_command_or_error.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')

    if validated_command_or_error.startswith('cd'):
        process_change_directory_response(response)
    elif validated_command_or_error == 'ls':
        process_listing_response(response, is_recursive=False)
    elif validated_command_or_error == 'lsr':
        process_listing_response(response, is_recursive=True)

client_socket.close()
