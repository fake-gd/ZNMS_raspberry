#!/usr/bin/python
# coding:utf-8
import RPi.GPIO as GPIO
from time import sleep

def control(control):
    GPIO.setmode(GPIO.BCM)#设置引脚编码
    GPIO.setup(14,GPIO.OUT)#输出
    p=GPIO.PWM(14,50)#设置引脚和频率
    p.start(0)#初始化占空比
    sleep(0.5)
    if control==1:
        p.ChangeDutyCycle(2.5)#设置占空比（2.5-12.5，分别对应0度到180度）
    else :
        p.ChangeDutyCycle(12.5)
    sleep(0.1)
    p.ChangeDutyCycle(0)
