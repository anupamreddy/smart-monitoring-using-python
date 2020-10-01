import cv2
import numpy as np
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = 'XXXXXXXXXXX@gmail.com'
email_password = 'XXXXXXXX'
email_send = 'XXXXXXXXXXXXX@gmal.com'

subject = 'alert'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = 'Hi there, sending this email from Python!'
msg.attach(MIMEText(body,'plain'))


server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)

tim=time.time()+(20*60*60)

while(time.time()<tim):
    cap1=cv2.VideoCapture(0)
    fourcc=cv2.VideoWriter_fourcc('X','V','I','D')
    out1=cv2.VideoWriter('out1.mp4',fourcc,29.99,(1280,720))
    sec=time.time()+20
    while(cap1.isOpened()):
        if(time.time()>sec):
            break
        ret, frame=cap1.read()
        if(ret == True):
            image = cv2.resize(frame, (1280,720))
            out1.write(image)
            cv2.imshow('output',image)
            if(cv2.waitKey(1) & 0xFF == ord('q')):
                break    
    cv2.destroyAllWindows()                    
    cap1.release()
    out1.release()
    cap = cv2.VideoCapture('out1.mp4')
    frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

    out = cv2.VideoWriter("output.mp4", fourcc, 5.0, (1280,720))
    alert= cv2.VideoWriter("alert.mp4", fourcc, 5.0, (1280,720))
    alertv=0

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    print(frame1.shape)
    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if cv2.contourArea(contour) < 1200:
                image = cv2.resize(frame1, (1280,720))
                alertv=1
                #print("\n\n change \n\n")
                continue

            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)
        #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

        if(alertv==1):
            alert.write(image)
            alertv=0
        image = cv2.resize(frame1, (1280,720))
        out.write(image)
        cv2.imshow("feed", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if(ret==False):
            break

        if cv2.waitKey(40) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    out.release()  
    alert.release()

    filename='alert.mp4'
    attachment  =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()

    server.sendmail(email_user,email_send,text)
server.quit()   
    



    
