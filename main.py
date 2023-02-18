# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pyautogui as gui
import cv2
import time
import operator
import uuid
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


# 获取鼠标坐标
def getCoordinate():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    print(mac)
    while True:
        # 获取初始坐标
        positionFirst = gui.position()
        # print(positionFirst)
        time.sleep(20)
        # 5秒后获取第二次坐标
        positionSecond = gui.position()
        # 判断两次坐标是否一致
        if operator.eq(positionFirst, positionSecond):
            print("坐标相同")
            # confirm = gui.confirm(text="长时间未操作", title="提示", buttons=['OK'])
            # confirm = gui.alert(text="长时间未操作", title="提示", button='OK')
            # print(confirm)
            # ret = mail(getMac())
            # if ret:
            #     print("邮件发送成功")
            # else:
            #     print("邮件发送失败")
            imgDesk = getImgDesk()  # 截图
            imgFace = getimgFace()  # 拍照片
            sendImgEmail(imgDesk, imgFace)  # 发送邮件
            print("发送成功")
        else:
            print("坐标不相同")


# 截取图片
def getImgDesk():
    # imgName = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())+".png"
    img = {"name": None, "file": None}
    imgName = str(time.strftime("%Y年%m月%d日%H时%M分%S秒", time.localtime())) + ".png"  # 注意不能用-或者：等符号
    screenshot = gui.screenshot(str(imgName))
    img["name"] = imgName
    img["file"] = screenshot
    return img


# 获取本机mac地址并转换成位置信息
def getMac():
    positionInfo = {"047f0e1c3eba": "1-2"}
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return positionInfo.get(mac)


# 发送普通邮件
def mail(mac):
    ret = True
    my_sender = '826465530@qq.com'  # 发件人邮箱账号
    my_pass = 'aknnouzgbozjbdhi'  # 发件人邮箱密码
    my_user = '826465530@qq.com'  # 收件人邮箱账号，我这边发送给自己

    try:
        msg = MIMEText(str(mac) + '占座位', 'plain', 'utf-8')
        msg['From'] = formataddr(["电子阅览室", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["老大", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "电子阅览室"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


# 发送带有图片的邮件
def sendImgEmail(imgDesk, imgFace):
    # mail_host = "826465530@qq.com"  # SMTP服务器地址
    mail_sender = "826465530@qq.com"  # 账号
    mail_passwd = "aknnouzgbozjbdhi"  # 密码

    msg = MIMEMultipart('related')
    msg["Subject"] = "这里是邮件主题"
    msg["From"] = mail_sender  # 发送人
    msg["To"] = mail_sender  # 接收人

    # html格式的邮件正文
    content = '''
    <body>
    <p>测试Python发送带图片的邮件...</p>
    <p>图片如下：</p>
    <p><img src="cid:imgDesk" alt="imgDesk"></p>
    <p><img src="cid:imgFace" alt="imgFace"></p>
    </body>
    '''
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    # 读取图片
    fp1 = open(imgDesk["name"], 'rb')  # 打开文件
    fp2 = open(imgFace, mode="rb")
    imgDesk = MIMEImage(fp1.read())  # 读入 msgImage 中
    imgFace = MIMEImage(fp2.read())  # 读入 msgImage 中
    fp1.close()  # 关闭文件
    fp2.close()  # 关闭文件

    # 定义图片 ID，在 HTML 文本中引用
    fp1.add_header('Content-ID', 'imgDesk')
    fp2.add_header('Content-ID', 'imgFace')
    msg.attach(imgDesk)
    msg.attach(imgFace)

    # 发送邮件
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
    s.login(mail_sender, mail_passwd)  # 登录邮箱
    s.sendmail(mail_sender, [mail_sender], msg.as_string())
    s.quit()


# 调用摄像头拍

def getimgFace():
    '''
    调用摄像头拍照并保存图片到本地
    :return: None
    '''
    cap = cv2.VideoCapture(0)
    imgName = str(time.strftime("%Y年%m月%d日%H时%M分%S秒", time.localtime())) + ".png"  # 注意不能用-或者：等符号
    while (cap.isOpened()):
        ret, frame = cap.read()
        # cv2.imshow("Capture_Paizhao", frame) # 显示窗口
        cv2.imwrite(imgName, frame)
        print("保存" + imgName + "成功!")
        break
    cap.release()
    cv2.destroyAllWindows()
    return imgName


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # getCoordinate()
    # im2 = gui.screenshot('123.png')
    # sendImgEmail()
    # print(getImg()["name"])
    # getCoordinate()
    getimgFace()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
