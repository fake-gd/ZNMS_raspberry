#!/usr/bin/python
# coding:utf-8
from linkkit import linkkit
import B1K
import SG90_concrol
import keyvalue
import receive
import shared
import time
import face

known_face_encodings,known_face_names= face.load_known_faces_and_initialize_camera()#预加载人脸图片
operation = None
key=None

lk = linkkit.LinkKit(
        host_name="cn-shanghai",
        product_key=shared.ProductKey,
        device_name=shared.DeviceName,
        device_secret=shared.DeviceSecret)
lk.thing_setup("lock.json")
lk.on_thing_enable = receive.on_thing_enable
lk.on_thing_disable = receive.on_thing_disable
lk.on_connect = receive.on_connect
lk.on_thing_prop_post = receive.on_thing_prop_post
lk.on_subscribe_topic = receive.on_subscribe_topic
lk.on_topic_message = receive.on_topic_message
lk.on_publish_topic = receive.on_publish_topic
lk.on_unsubscribe_topic = receive.on_unsubscribe_topic


lk.connect_async()#linkkit异步连接
time.sleep(2)


while 1:
    shared.status=B1K.B1Kstatus()#读取电位器的状态——0 or 1
    if shared.status==0 and shared.lock_value==1 and operation==1:#使用硬件开锁后手动关锁判定
        shared.lock_value=0
        operation=0
    #shared.pre_lock_value=shared.status
    if shared.status==0 and shared.lock_value==1 and shared.pre_lock_value==1 and operation==0:#使用远程开锁后手动关锁判定
        shared.lock_value=0
        shared.pre_lock_value=0
    if shared.status!=shared.pre_status:#锁状态改变，则发送数据
        print('lock_status:',shared.status)
        shared.pre_status=shared.status
        prop_data = {
        "mark":shared.status
        }
        lk.thing_post_property(prop_data)
        
    if shared.lock_value!=shared.pre_lock_value:#接收到的开锁命令发生改变，则记录上一次开锁命令
        print('lock_value:',shared.lock_value)
        shared.pre_lock_value=shared.lock_value
        shared.swap = 1
    if shared.swap==1:#开锁命令改变则控制舵机
        if shared.lock_value==1:
            SG90_concrol.control(1)#开锁
            shared.swap=0
        else :
            SG90_concrol.control(0)#关锁
            shared.swap=0
    key=keyvalue.getkey()#读取键盘输入
    if key!=None and key=='A':#按下按键‘A’，则进入密码开锁
        print('input password')
        key=None
        password=''
        while 1:
            key1 = keyvalue.getkey()
            if not key1==None:
                password = password + key1
                if password==shared.true_password:#密码正确与否判定
                    SG90_concrol.control(1)#开锁
                    shared.status=B1K.B1Kstatus()
                    print(shared.status)
                    prop_data = {
                    "mark":shared.status
                    }
                    lk.thing_post_property(prop_data)#开锁后发送锁状态
                    shared.lock_value=1
                    operation=1
                    break
                if len(password)>4:#只能输入四位密码
                    password=''
                if key1=='#':
                    print('exit')
                    break
                print('password:',password)
    if key!=None and key=='B':#按下B，则进入人脸识别开锁
        face.recognize_faces(known_face_encodings,known_face_names)#人脸识别算法，返回开锁人姓名
        print(shared.name)
        SG90_concrol.control(1)
        shared.lock_value=1
        operation=1
    time.sleep(0.2)
    