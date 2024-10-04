import RPi.GPIO as GPIO
import time


def set_angle(pwm, pin, angle):
    duty_cycle = 2 + (angle / 18)  # 2 to 12 is a common range for 0-180 degrees
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(0)
