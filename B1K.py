#!/usr/bin/python
import wiringpi

def B1Kstatus():
    GPIO_INPUT_Pin = 7
    INPUT = 0
    HIGH = 1
    LOW = 0
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(GPIO_INPUT_Pin,INPUT)
    return wiringpi.digitalRead(GPIO_INPUT_Pin)
