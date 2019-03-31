#!/usr/bin/env python
#coding: UTF-8
import time
import RPi.GPIO as GPIO
import SimpleMFRC522
import string
import sys
import os
reader = SimpleMFRC522.SimpleMFRC522()
# Welcome message
print("Looking for cards.Press Ctrl-C to stop.")
def ledbling():
    led=13
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,True)
    time.sleep(1)
    GPIO.output(led,False)

def restart_program():
    python = sys.executable
    os.execl(python,python,* sys.argv)
try:
    id,text = reader.read()
    print(text)
    a = string.atoi(text)
    if a==4:
        ledbling()
    time.sleep(1)
    GPIO.cleanup()
    restart_program()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()