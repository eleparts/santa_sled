import pygame
from signal import pause
from pitop.pma import LED, Button,ServoMotor
from pitop.labs import WebController,WebServer
from pitop import Camera, DriveController, Pitop
from pitop.processing.algorithms.line_detect import process_frame_for_line
from time import sleep

# Assemble a robot
button=Button("D1")
yellow=LED("D0")
red=LED("D7")
servo = ServoMotor("S0")
robot = Pitop()
robot.add_component(DriveController(left_motor_port="M3", right_motor_port="M0"))
robot.add_component(Camera())
pygame.init()
song=pygame.mixer.Sound('song.wav')

STOP_ANGLE = 0
TARGET_SPEED = 25
servo.target_angle = 90 # This centers the servo
def servo_f():
    print("Setting target speed to", -TARGET_SPEED)
    servo.target_speed = -TARGET_SPEED

    print("Sweeping using the target speed")
    servo.sweep() # Sweeps using the target_speed we just set

    current_angle = servo.current_angle
    # Monitor the servo motor angle and speed while it's moving
    while current_angle > -STOP_ANGLE:
        current_angle = servo.current_angle
        current_speed = servo.current_speed
        print(f"current_angle: {current_angle} | current_speed: {current_speed}")
        sleep(0.05)


# Set up logic based on line detection
def drive_based_on_frame(frame):
    processed_frame = process_frame_for_line(frame)
    robot.miniscreen.display_image(processed_frame.robot_view)
    if processed_frame.line_center is None:
        robot.drive.stop()
        red.off()
        yellow.off()
        song.stop()
        servo_f()
    else:
        print(f"Target angle: {processed_frame.angle:.2f} deg ", end="\r")
        robot.drive.forward(0.25, hold=True)
        robot.drive.target_lock_drive_angle(processed_frame.angle)

def sled_main():
    print("button pushed")
    red.on()
    yellow.on()
    song.play(-1)
    sleep(2)
    robot.camera.on_frame = drive_based_on_frame


button.when_pressed=sled_main

# On each camera frame, detect a line


