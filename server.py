# Name:Leila Sarkamari
# Lab 5-CIS 41B 
import os
import socket
import threading
import sys

# Define server configurations
BUFFER_SIZE = 1024

def change_directory(current_directory, new_directory):
    '''
    Accept a new directory path and change the client's current directory to the new directory. 
    Then send back your choice of 'success' or ‘fail’ status.
    '''
    try:
        new_path = os.path.abspath(os.path.join(current_directory, new_directory))
        if os.path.isdir(new_path):  # if successful 
            return new_path, 'success'
        else:
            return current_directory, 'fail' #if fail
    except Exception as e:
        return current_directory, 'fail' #if fail

def list_current_directory(current_directory):
    '''
    Send back the list of files and directories in the client's current directory. 
    Only for the current directory
    '''
    try:
        return os.listdir(current_directory)
    except Exception as e:
        return [str(e)]

def list_recursive(current_directory):
    '''
    Send back the list of subdirectories from a recursive walk of the client's current directory.
    '''
    try:
        result = []
        for root, dirs, files in os.walk(current_directory):
            for name in dirs:
                result.append(os.path.join(root, name))
        return result
    except Exception as e:
        return [str(e)]

def handle_client(client_socket, address):
    '''
    Handle the client to interact with the user
    '''
    print(f"Accepted connection from {address}")
    current_directory = os.getcwd()
    
    while True:
        try:
            request = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not request:
                break

            parts = request.strip().split()
            command = parts[0]

            if command == 'ls':
                response = f"Listing of {current_directory}\n" + '\n'.join(list_current_directory(current_directory))
            elif command == 'lsr':
                response = f"Recursive listing of {current_directory}\n" + '\n'.join(list_recursive(current_directory))
            elif command == 'cd':
                if len(parts) != 2:
                    response = 'Invalid directory command format. Use "cd dir_name".'
                else:
                    new_directory = parts[1]
                    current_directory, status = change_directory(current_directory, new_directory)
                    if status == 'success':
                        response = f"New path: {current_directory}"
                    else:
                        response = "No such directory"
            elif command == 'q':
                response = "Quit"
                client_socket.send(response.encode('utf-8'))
                break
            else:
                response = "Invalid command"

            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            print(f"Error handling request from {address}: {e}")
            break

    client_socket.close()
    print(f"Connection from {address} closed")

if len(sys.argv) != 3:
    print("Usage: server.py <max_clients> <timeout>")
    sys.exit(1)

try:
    max_clients = int(sys.argv[1])
    timeout = int(sys.argv[2])
except ValueError:
    print("Both max_clients and timeout must be integers.")
    sys.exit(1)

if not (1 <= max_clients <= 4) or not (3 < timeout < 120):
    print("Invalid arguments: max_clients should be between 1 and 4, timeout should be between 4 and 119 seconds")
    sys.exit(1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 5551))
server_socket.listen(max_clients)
server_socket.settimeout(timeout)

print(f"Server started, listening on port 5551 for up to {max_clients} clients with {timeout} seconds timeout")

try:
    while True:
        try:
            client_socket, address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
            client_handler.start()
        except socket.timeout:
            print("Server timed out waiting for connections")
            break

finally:
    server_socket.close()
    print("Server shut down")
