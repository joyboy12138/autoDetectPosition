import cv2
import datetime

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        print("监测到人脸")
        now = datetime.datetime.now()
        filename = "./photos/photo_{}-{}-{}_{}-{}-{}.jpg".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        cv2.imwrite(filename, frame)
    else:
        print("没有监测到人脸")
    # cv2.imshow("Face Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
