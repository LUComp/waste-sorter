import bluetooth
import RPi.GPIO as GPIO
from rp.servo import set_angle

if __name__ == "main":
    # Set GPIO numbering mode
    GPIO.setmode(GPIO.BOARD)

    pin = 11
    GPIO.setup(pin, GPIO.OUT)

    pwm = GPIO.PWM(pin, 50)
    pwm.start(0)

    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    # Bind the socket to any available port on the Bluetooth adapter
    port = bluetooth.PORT_ANY
    server_socket.bind(("14:13:33:0A:AF:32", port))

    # Start listening for incoming connections (backlog of 1)
    server_socket.listen(1)

    bluetooth_address, server_port = server_socket.getsockname()

    print(f"Server is listening on Bluetooth address: {bluetooth_address}, port: {server_port}")

    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)  # Receive up to 1024 bytes
            if not data:
                break
            set_angle(pwm, pin, float(data.decode('utf-8')))

    finally:
        # Close the sockets
        client_socket.close()
        server_socket.close()
