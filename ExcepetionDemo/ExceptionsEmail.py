import smtplib
from email.mime.text import MIMEText
import time
import os
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 邮件配置
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_username@example.com'
SMTP_PASSWORD = 'your_password'
EMAIL_FROM = 'your_username@example.com'
EMAIL_TO = 'recipient@example.com'

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file

    def on_modified(self, event):
        if event.src_path == self.log_file and event.event_type == 'modified':
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if "ERROR" in line:
                        self.send_email(line.strip())

    def send_email(self, error_message):
        subject = 'Error Alert'
        body = f'Error message: {error_message}'

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
            server.quit()
            print("Email notification sent successfully.")
        except Exception as e:
            print(f"Failed to send email notification: {e}")

# 示例用法
if __name__ == "__main__":
    # 创建监控程序实例
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "logs")
    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    log_path = os.path.join(log_dir, log_file)

    if not os.path.exists(log_path):
        with open(log_path, 'w') as f:
            f.write("INFO: This is an info message.\n")
            f.write("WARNING: This is a warning message.\n")
            f.write("ERROR: This is an error message.\n")
            f.write("ERROR: Another error message.\n")
            f.write("INFO: Another info message.\n")

    observer = Observer()
    observer.schedule(LogFileHandler(log_path), os.path.dirname(log_path))
    observer.start()
    print(f"Started monitoring {log_path} for errors...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
"""
解释：
邮件配置：

设置了 SMTP 服务器地址、端口、用户名、密码等信息，用于发送邮件。
send_email 方法：

当监控到含有 "ERROR" 字符串的日志行时，调用 send_email 方法发送邮件通知。
示例用法：

在 __main__ 中启动监控程序，监听日志文件，并且每当发现含有 "ERROR" 的日志行时，发送邮件通知。
请确保将 SMTP_SERVER、SMTP_PORT、SMTP_USERNAME、SMTP_PASSWORD、EMAIL_FROM 和 EMAIL_TO 替换为你实际的邮件服务器和邮箱地址。这样，当日志文件被修改并包含错误消息时，你会收到邮件通知。
"""