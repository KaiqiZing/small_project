"""异常监控模块"""
import time
import logging
import os
import datetime
from logging.handlers import RotatingFileHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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
        self.file_handle = RotatingFileHandler(self.log_name, maxBytes=10000, backupCount=5)
        self.file_handle.setLevel(logging.ERROR)

        # 日志格式
        formatter = logging.Formatter('%(asctime)s %(filename)s --> %(funcName)s %(levelno)s: %(levelname)s -----> %(message)s')
        self.file_handle.setFormatter(formatter)
        self.logger.addHandler(self.file_handle)

        # 启动日志文件变化监控
        self.start_file_monitor()

    def start_file_monitor(self):
        observer = Observer()
        observer.schedule(LogFileHandler(self.log_name), os.path.dirname(self.log_name))
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

    def on_modified(self, event):
        if event.src_path == self.log_file and event.event_type == 'modified':
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if "ERROR" in line:
                        print(f"Error found in log: {line.strip()}")

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
    logger.error("This is an error message.")
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

"""
说明
使用 watchdog 监控文件变化：

watchdog 提供了 Observer 和 FileSystemEventHandler 类，可以用来监控文件系统的变化，例如文件的修改、创建、删除等。
在 UserLog 类中，通过 start_file_monitor 方法启动对日志文件的监控。一旦日志文件被修改（例如有新日志写入），会触发 on_modified 方法。
日志记录器的使用：

日志记录器配置与之前类似，使用了 RotatingFileHandler 来实现日志文件的滚动和归档，确保日志文件不会无限增长。
日志记录器的级别可以根据需要设置为 logging.DEBUG 或 logging.WARNING，可以根据环境需求进行调整。
定期扫描和异常处理：

在 LogFileHandler 的 on_modified 方法中可以编写代码来处理日志文件的变化，例如实时读取最新日志并进行分析、报警等操作。
通过这种方式，你可以实现一个基本的日志监控系统，能够实时响应日志文件的变化，并及时处理异常事件。



解释：
LogFileHandler 类：

on_modified 方法中，当日志文件被修改时，程序会读取新的日志行。然后，它会检查每一行日志，如果发现包含 "ERROR" 字符串的行，就会打印出来或者进行其他你想要的处理。
示例用法：

在 __main__ 中创建了一个示例日志文件，包含了不同级别的日志消息（INFO、WARNING、ERROR）。监控程序 observer 被设置为监视这个日志文件，但只会处理包含 "ERROR" 字符串的行。
通过这样的设置，监控程序会专门处理错误级别的日志消息，而忽略掉其他不感兴趣的消息。这种方法比调整日志记录器的级别更加灵活，因为它不影响日志记录的实际配置。





"""