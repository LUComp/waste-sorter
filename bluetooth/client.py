import bluetooth

# Specify the server's Bluetooth address (replace with actual address)
server_address = 'B8:27:EB:9A:19:C0'  # Replace with the server's Bluetooth MAC address
port = 1  # Same port number as the server

# Create the client socket
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Connect to the server
client_socket.connect((server_address, port))
print(f"Connected to the server at {server_address}")

try:
    # Send a message to the server
    message = "Hello from the client!"
    client_socket.send(message)
    print(f"Sent: {message}")

    # Receive a response from the server
    response = client_socket.recv(1024)  # Receive up to 1024 bytes
    print(f"Received: {response.decode('utf-8')}")

finally:
    # Close the client socket
    client_socket.close()
