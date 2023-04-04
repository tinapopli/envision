import RPi.GPIO as GPIO

import time

import pygame.mixer

import os

GPIO.setmode(GPIO.BCM)

# Set up ultrasonic sensor

TRIG = 11
ECHO = 13

GPIO.setup (TRIG, GPIO.OUT)

GPIO.setup (ECHO, GPIO.IN)

# Set up vibrating motor

MOTOR_PIN = 7

GPIO.setup(MOTOR_PIN, GPIO.OUT)

# Set up audio output

pygame.mixer.init()

# Define the range for object detection

MIN_DISTANCE = 10 # in cm

MAX_DISTANCE = 100 # in cm

def measure_distance():

    GPIO.output(TRIG, False)
    print("Waiting For Sensor To Settle")
    time.sleep(1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
          pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print("Distance:",distance,"cm")


    return distance

try:
    while True:

        distance = measure_distance()

        if distance >= MIN_DISTANCE and distance <= MAX_DISTANCE:

# Object detected within range

            print ("Object detected at", distance, "cm")

# Activate vibrating motor
            #time.sleep(1)

            GPIO.output(MOTOR_PIN, True)
            pygame.mixer.music.load("beep.wav")

            pygame.mixer.music.play()
            time.sleep(1.5)

            GPIO.output(MOTOR_PIN, False)

# Play audio output


            # time.sleep(1)


            # while pygame.mixer.music.get_busy() == True:

                # continue

        else:

# No object detected within range

            print ("No object detected")

            time.sleep(1)

except KeyboardInterrupt:

    GPIO.cleanup()

    pygame.mixer.quit()
