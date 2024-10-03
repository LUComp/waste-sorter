import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set the GPIO pin number where the signal wire is connected (e.g., pin 11)
servo_pin = 11

# Set the pin as an output pin
GPIO.setup(servo_pin, GPIO.OUT)

# Set the PWM signal frequency (usually 50Hz for servo motors)
pwm = GPIO.PWM(servo_pin, 50)

# Start PWM with a duty cycle of 0 (servo at 0 degrees)
pwm.start(0)

def set_angle(angle):
    """
    Set the servo motor to the desired angle.

    :param angle: The angle to set the servo (0 to 180 degrees).
    """
    # Convert the angle to the corresponding duty cycle for PWM
    duty_cycle = 2 + (angle / 18)  # 2 to 12 is a common range for 0-180 degrees
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        # Get the desired angle from the user
        angle = float(input("Enter the angle (0 to 180): "))
        if 0 <= angle <= 180:
            set_angle(angle)
        else:
            print("Please enter a valid angle between 0 and 180 degrees.")
except KeyboardInterrupt:
    # Clean up the GPIO and stop PWM when the program is stopped
    pwm.stop()
    GPIO.cleanup()
    print("\nProgram exited gracefully.")
