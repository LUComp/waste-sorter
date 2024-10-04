import bluetooth

server_address = "B8:27:EB:9A:19:C0" 
port = 1 

rp_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    rp_socket.connect((server_address, port))
    print(f"Connected to the server at {server_address}")

    while True:
        angle = input("Enter the angle (0 to 180, or 'q' to quit): ")
        if angle.lower() == "q":
            print("Exiting...")
            break
        try:
            angle = int(angle)
            if 0 <= angle <= 180:
                rp_socket.send(str(angle))
                print(f"Sent angle: {angle}")
            else:
                print("Please enter a valid angle between 0 and 180.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

except bluetooth.btcommon.BluetoothError as err:
    print(f"Failed to connect or send data: {err}")
finally:
    # Close the connection when done
    rp_socket.close()
    print("Connection closed.")
