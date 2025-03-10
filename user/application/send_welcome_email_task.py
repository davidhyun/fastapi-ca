import smtplib
from celery import Task
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import get_settings

settings = get_settings()

class SendWelcomeEmailTask(Task):
    # 어플리케이션 내에서 유일한 값을 가지는 이름을 부여
    # 이름 미지정시 셀러리는 태스크를 제대로 찾지 못한다
    name = "send_welcome_email_task"

    # 태스크 수행될 때 run 함수 호출됨    
    def run(self, receiver_email: str):
        sender_email = "hyunh317@gmail.com"
        password = settings.email_password
        
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "회원 가입을 환영합니다."
        
        body = "TIL 서비스를 이용해주셔서 감사합니다."
        message.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(message)