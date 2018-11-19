"""import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint
from models import Users
from django.core.mail import send_mail
randint(100, 999)

fromaddr = "dromed007@gmail.com"


def get_random(x):
    startRandom = 10**(x-1)
    endRandom = (10**x)-1
    return randint(startRandom, endRandom)

def sendMails():
    users = Users.objects.all();
    for user in users:
        token = hex(get_random(32)).split('x')[-1]
        toaddr = user.emailID

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Automatic reply: Registration Confirmation"

        body = "*This is an automatically-generated message. Please do not reply*   Your token number is: " + token

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "drone007admin")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

#str = "padhiarisourav@gmail.com" #get USER'S EMAIL ID

#token =hex(get_random(32)).split('x')[-1]



#toaddr = "anantgarg5@gmail.com"

def main():
    sendMails()


if __name__ == '__main__':
    main()"""
from django.core.mail import send_mail
from models import Users

from random import randint


randint(100, 999)

def get_random(x):
    startRandom = 10**(x-1)
    endRandom = (10**x)-1
    return randint(startRandom, endRandom)


users = Users.objects.all();
for user in users:
    token = hex(get_random(32)).split('x')[-1]
    toaddr = user.emailID


send_mail('Token for DroMed Registration', 
    "*This is an automatically-generated message. Please do not reply*   Your token number is: " + token, 
    'dromed007@gmail.com', [toaddr])





