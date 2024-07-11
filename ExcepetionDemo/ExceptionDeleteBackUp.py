import os
import datetime
import logging
import time
import unittest
from logging.handlers import RotatingFileHandler
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


"""实现代码中处理日志文件的备份和删除"""
class UserLog:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.handlers = []  # 清空 handlers，防止重复添加
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

    def handle_backup_and_deletion(self):
        """
        处理日志文件的备份和删除
        """
        log_files = [f for f in os.listdir(os.path.dirname(self.log_name)) if f.endswith(".log")]
        # 获取当前日志文件夹中所有以.log 结尾的文件列表

        log_files.sort()
        # 对获取到的日志文件列表按文件名进行排序，确保处理顺序
        # 备份超过指定数量的旧日志文件
        if len(log_files) > self.file_handle.backupCount:
            # 如果当前日志文件数量超过设置的备份数量
            for file_to_backup in log_files[:len(log_files) - self.file_handle.backupCount]:
                # 对于超出备份数量的旧文件进行处理
                backup_path = os.path.join(os.path.dirname(self.log_name), f"backup_{file_to_backup}")
                # 确定备份文件的路径，文件名前面添加"backup_"
                os.rename(os.path.join(os.path.dirname(self.log_name), file_to_backup), backup_path)
                # 将旧文件重命名为备份文件

        # 删除备份时间过长的日志文件（示例：超过 7 天）
        current_time = datetime.datetime.now()
        # 获取当前时间
        for backup_file in os.listdir(os.path.dirname(self.log_name)):
            # 遍历文件夹中的所有文件
            if backup_file.startswith("backup_") and (current_time - datetime.datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(os.path.dirname(self.log_name), backup_file)))) > datetime.timedelta(
                    days=7):
                # 如果文件以"backup_"开头，并且其修改时间超过 7 天
                os.remove(os.path.join(os.path.dirname(self.log_name), backup_file))
                # 删除该备份文件

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





class TestUserLog(unittest.TestCase):
    def setUp(self):
        self.user_log = UserLog()

    def test_log_file_creation(self):
        # 检查日志文件是否创建
        log_file_path = self.user_log.log_name
        self.assertTrue(os.path.exists(log_file_path))

    def test_backup_creation(self):
        # 模拟生成超过备份数量的日志文件
        for i in range(7):
            new_log_file = os.path.join(os.path.dirname(self.user_log.log_name),
                                        f"{datetime.datetime.now().strftime('%Y-%m-%d')}_{i}.log")
            with open(new_log_file, 'w') as f:
                f.write("Test log line\n")
        self.user_log.handle_backup_and_deletion()
        time.sleep(1)
        backup_files = [f for f in os.listdir(os.path.dirname(self.user_log.log_name)) if f.startswith("backup_")]
        self.assertTrue(len(backup_files) > 0)


    def test_deletion_of_old_backups(self):
        # 模拟创建一个旧的备份文件，检查是否在超过 7 天后被删除
        old_backup_file = "backup_2024-07-01.log"
        old_backup_path = os.path.join(os.path.dirname(self.user_log.log_name), old_backup_file)
        with open(old_backup_path, 'w') as f:
            f.write("Old backup content\n")
        os.utime(old_backup_path, (
        datetime.datetime.now().timestamp() - 8 * 24 * 60 * 60, datetime.datetime.now().timestamp() - 8 * 24 * 60 * 60))
        self.user_log.handle_backup_and_deletion()
        self.assertFalse(os.path.exists(old_backup_path))

if __name__ == '__main__':
    unittest.main()


"""
在上述代码中，添加了 handle_backup_and_deletion 方法来处理日志文件的备份和删除。
对于备份，当当前的日志文件数量超过 RotatingFileHandler 中设置的 backupCount 时，将最早的日志文件进行备份。
对于删除，这里示例为删除超过 7 天的备份日志文件，可以根据实际需求调整时间阈值和删除条件。


首先，通过 os.listdir 获取日志文件夹中的所有 .log 文件，并对其进行排序。
然后，检查文件数量是否超过设置的备份数量。如果超过，就从最早的文件开始进行备份，通过重命名的方式将其转换为备份文件。
接下来，获取当前时间，并再次遍历文件夹中的文件。对于以 backup_ 开头且修改时间超过 7 天的备份文件，使用 os.remove 进行删除，以释放存储空间并保持备份的整洁。
"""