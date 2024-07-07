import face_recognition
import cv2
import numpy as np
import os
import keyvalue
import shared

def load_known_faces_and_initialize_camera():
    known_face_encodings = []
    known_face_names = []
    folder_path = "/home/pi/Adafruit_Python_DHT/aliyun_iot_demo_python/photo/"  # 存放图片的文件夹
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)

            if len(face_encoding) > 0:
                known_face_encodings.append(face_encoding[0])
                known_face_names.append(os.path.splitext(filename)[0])

    # 初始化摄像头
    
    print("ok")
    return known_face_encodings, known_face_names

def recognize_faces(known_face_encodings, known_face_names):
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    status = 0  # status用于判断是否捕捉到认识的人
    shared.name='0'
    face_encodings=None
    output = np.empty((240, 320, 3), dtype=np.uint8)  # 初始化一个空的NumPy数组，用于存储从视频流中捕获的每一帧图像。
    empty_frame = np.zeros((240, 320, 3), dtype=np.uint8)  # 创建一个全黑的空白帧
    while True:
        print("Capturing image.")
        ret, frame = camera.read()  # 读取摄像头中的一帧

        if not ret:
            print("Failed to capture image.")
            break
        cv2.imshow('Video', frame)
        # 将帧转换为RGB格式（如果需要）
        output = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 在当前视频帧中找到所有人脸及其编码
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(output, face_locations)

        # 遍历每张找到的人脸，看看是否是已知的面孔
        for face_encoding in face_encodings:
            # 看看面孔是否与已知面孔匹配
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            shared.name = "Unknown"

            # 计算面孔距离（越低越好）
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            # 只有在面孔距离低于某个阈值时才考虑匹配
            if matches[best_match_index] and face_distances[best_match_index] < 0.38:
                shared.name = known_face_names[best_match_index]
                status = 1
            print("I see someone named {}!".format(shared.name))

        # 显示当前帧
        

        # 如果按下 'q' 键或status为1，则退出循环
        if cv2.waitKey(1) & 0xFF == ord('q') or status == 1:
            #cv2.imshow('Video', empty_frame)
            break
        key=keyvalue.getkey()
        if key!=None and key=='#':
            shared.name = '0'
            break
    #cv2.imshow('Video', empty_frame)
    # 释放摄像头并关闭所有窗口
    camera.release()
    cv2.destroyAllWindows()
'''
# 调用函数进行人脸识别
known_face_encodings, known_face_names, camera = load_known_faces_and_initialize_camera()
name = recognize_faces(known_face_encodings, known_face_names, camera)
print("Recognized:", name)
'''