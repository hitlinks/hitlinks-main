import socket
import re

PORT = 8080  # Global variable for the port

# Create a server socket that listens for incoming connections
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(("0.0.0.0", PORT))
server_sock.listen(1)

print(f"Waiting for a request on port {PORT}...")

while True:
    client_sock, addr = server_sock.accept()
    print(f"Received request from {addr}")

    # Read request data from client
    request_data = client_sock.recv(4096).decode(errors="ignore")
    
    if request_data:
        # Extract the host from the request
        host_match = re.search(r"Host:\s*([^\r\n]+)", request_data)
        
        if host_match:
            host = host_match.group(1)
            print(f"Connecting to: {host}")

            # Connect to the requested host
            remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_sock.connect((host, 80))
            remote_sock.send(request_data.encode())

            # Receive response from remote server
            response = remote_sock.recv(4096)
            remote_sock.close()

            # Send response back to client
            client_sock.send(response)

    client_sock.close()
