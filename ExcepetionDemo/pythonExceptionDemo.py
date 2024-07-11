""""""
import logging
import os
import datetime
from logging.handlers import RotatingFileHandler

class UserLog(object):

    def __init__(self):

        # 获取当前日志记录器
        self.logger1 = logging.getLogger(__name__)
        # 从日志管理器的字典中移除当前模块对应的日志记录器，防止重复
        logging.Logger.manager.loggerDict.pop(__name__)
        # 将当前日志记录器的处理器列表清空
        self.logger1.handlers = []
        # 从当前日志记录器中移除所有已有的处理器
        self.logger1.removeHandler(self.logger1.handlers)

        if not self.logger1.handlers:

            self.logger1.setLevel(logging.DEBUG)  # 测试环境
            # self.logger1.setLevel(logging.WARNING) #生产环境

            # 文件名字
            base_dir = os.path.dirname(os.path.abspath(__file__))
            log_dir = os.path.join(base_dir, "logs")
            log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
            log_name = log_dir + "/" + log_file

            # 文件输出日志， writes formatted logging records to disk files
            self.file_handle = logging.FileHandler(log_name, 'a', encoding='utf-8')

            # 实现日志文件的轮转
            self.file_handle = RotatingFileHandler(log_name, maxBytes=10000, backupCount=5)

            # 这里可以设置日志等级，INFO,WARNING,DEBUG,ERROR
            self.file_handle.setLevel(logging.INFO)


            # 加上日志时间进行操作
            formatter = logging.Formatter(
                '%(asctime)s %(filename)s--> %(funcName)s %(levelno)s: %(levelname)s ----->%(message)s')
            self.file_handle.setFormatter(formatter)
            self.logger1.addHandler(self.file_handle)

    def get_log(self):
        return self.logger1

    def close_handle(self):
        #从当前日志记录器中移除所有已有的处理器
        self.logger1.removeHandler(self.file_handle)
        #移除文件处理器
        self.file_handle.close()

def main_test():
    logger = UserLog().get_log()
    #加载info信息
    logger.info("这是一个信息日志")
    #加载warning
    logger.warning("这是一个警告日志")
    #加载error
    logger.error("这是一个错误日志")

if __name__ == '__main__':
    main_test()
