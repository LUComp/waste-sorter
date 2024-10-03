import bluetooth

# Create the server socket
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Bind the socket to any available port on the Bluetooth adapter
port = bluetooth.PORT_ANY
server_socket.bind(("", port))

# Start listening for incoming connections (backlog of 1)
server_socket.listen(1)

# Get the server Bluetooth address and port number
bluetooth_address, server_port = server_socket.getsockname()

print(f"Server is listening on Bluetooth address: {bluetooth_address}, port: {server_port}")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

try:
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)  # Receive up to 1024 bytes
        if not data:
            break
        print(f"Received: {data.decode('utf-8')}")

        # Send a response back to the client
        response = "Hello from the server!"
        client_socket.send(response)
        print(f"Sent: {response}")

finally:
    # Close the sockets
    client_socket.close()
    server_socket.close()
