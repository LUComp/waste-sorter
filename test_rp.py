import bluetooth

# Raspberry Pi server address (replace with your Pi's Bluetooth address)
server_address = 'B8:27:EB:9A:19:C0'  # Example address
port = 1  # Port number for the Bluetooth connection (1 for RFCOMM)

# Create the Bluetooth client socket
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    # Connect to the Raspberry Pi's Bluetooth server
    client_socket.connect((server_address, port))
    print(f"Connected to the server at {server_address}")

    while True:
        # Ask the user for an angle between 0 and 180
        angle = input("Enter the angle (0 to 180, or 'q' to quit): ")

        # Allow the user to exit the loop
        if angle.lower() == 'q':
            print("Exiting...")
            break
        
        # Validate the input and send the angle to the Raspberry Pi
        try:
            angle = int(angle)
            if 0 <= angle <= 180:
                # Send the angle as a string to the Raspberry Pi
                client_socket.send(str(angle))
                print(f"Sent angle: {angle}")
            else:
                print("Please enter a valid angle between 0 and 180.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            
except bluetooth.btcommon.BluetoothError as err:
    print(f"Failed to connect or send data: {err}")
finally:
    # Close the connection when done
    client_socket.close()
    print("Connection closed.")
