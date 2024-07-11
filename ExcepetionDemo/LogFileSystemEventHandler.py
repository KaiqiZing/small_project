# coding=utf-8
import time
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        print(f'文件创建: {event.src_path}')

    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'文件修改: {event.src_path}')


    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f'文件删除:{event.src_path}')

    def on_moved(self, event):
        if event.is_directory:
            return
        print(f'文件重命名:{event.src_path}')

if __name__ == "__main__":
    path = "."  # 要监视的目录
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()