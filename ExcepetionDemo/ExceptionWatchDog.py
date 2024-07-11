import os
import logging
import datetime
from logging.handlers import RotatingFileHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class UserLog(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.handlers = []  # 清空handlers，防止重复添加
        self.logger.setLevel(logging.DEBUG)  # 测试环境

        # 创建日志文件夹
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 日志文件名
        log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
        self.log_name = os.path.join(log_dir, log_file)

        # 文件输出日志
        self.file_handle = logging.handlers.RotatingFileHandler(self.log_name, maxBytes=10000, backupCount=5)
        self.file_handle.setLevel(logging.ERROR)

        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s --> %(funcName)s %(levelno)s: %(levelname)s -----> %(message)s')
        self.file_handle.setFormatter(formatter)
        self.logger.addHandler(self.file_handle)

        # 启动日志文件变化监控
        self.start_file_monitor()

    def start_file_monitor(self):
        observer = Observer()
        #事件处理程序与监控路径关联起来，
        observer.schedule(LogFileHandler(self.log_name), os.path.dirname(self.log_name))
        #启动观察者
        observer.start()
        print(f"Started monitoring {self.log_name} for changes...")

    def get_log(self):
        return self.logger

    def close_handle(self):
        self.logger.removeHandler(self.file_handle)
        self.file_handle.close()

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file
        self.error_lines = set()  # 用于存储已经打印过的包含"ERROR"的行

    def on_modified(self, event):
        if event.src_path == self.log_file and event.event_type == 'modified':
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if "ERROR" in line and line not in self.error_lines:  # 检查是否已经打印过
                        print(f"Error found in log: {line.strip()}")
                        self.error_lines.add(line)  # 将该行添加到已打印集合

# 示例用法
if __name__ == "__main__":
    # 创建监控程序实例
    # 创建日志实例
    user_log = UserLog()

    # 获取日志记录器
    logger = user_log.get_log()

    # 模拟写入一些日志
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is a message.")
    logger.critical("This is a critical message.")

    # 模拟运行时持续写入日志
    try:
        while True:
            logger.info("Still running...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the program...")

    # 关闭日志处理器
    user_log.close_handle()
