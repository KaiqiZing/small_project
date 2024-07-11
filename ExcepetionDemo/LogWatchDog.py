import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    """
    事件处理器
    """
    def on_modified(self, event):
        # 当文件被修改时触发此方法
        if not event.is_directory:
            print(f'文件 {event.src_path} 被修改')

if __name__ == "__main__":
    # 要监视的目录路径
    # 监控某个文件夹下哪些文件被修改
    path_to_monitor = 'D:/small_project-master/small_project-master/ExcepetionDemo/logs/'  # 这里可以将 '.' 替换为你要监控的实际目录路径
    event_handler = FileChangeHandler()
    observer = Observer()
    # 将事件处理程序与要监视的路径关联起来，并设置递归监视（包括子目录）
    #简述：1.先创建观察者observer = Observer();
    #2.创建事件处理类FileChangeHandler继承FileSystemEventHandler，当目录被创建修改删除时用于触发对应的，文件系统事件处理类;
        #2.1FileSystemEventHandler 处理流程：1.接到事件后开始触发dispatch(event),2.触发on_any_event(
    # event)把事件方法进行分派处理，3.开始执行对应事件如：on_created(event),on_deleted(event), on_modified(event)
    #3.观察者observer 将事件处理类和要监控的路径：path_to_monitor 进行关联，当操作系统检测到系统文件发生改变时，会发送给相应的事件给watchdog;
    #4.观察者收到这些事件后，会调用事件处理类对应的方法如：on_modified, on_deleted, on_moved, on_created;
    #5.调用observer.start()启动观察者线程，该线程会在后台持续监听文件系统事件
    observer.schedule(event_handler, path_to_monitor, recursive=True)
    observer.start()  # 启动观察者

    try:
        while True:
            time.sleep(1)  # 保持程序运行，持续监听
    except KeyboardInterrupt:
        observer.stop()  # 按 Ctrl+C 停止监听

    observer.join()  # 等待观察者线程结束



"""
定义了一个继承自 FileSystemEventHandler 的类 FileChangeHandler，并重写了 on_modified 方法，用于处理文件修改事件。在这个方法中，可以添加你需要在文件被修改时执行的具体操作，这里只是简单地打印出被修改文件的路径。

在 __main__ 部分，首先指定要监视的目录路径（path_to_monitor）。

创建 FileChangeHandler 的实例 event_handler 和 Observer 的实例 observer。
使用 observer.schedule 方法将事件处理程序与要监视的路径关联起来，并通过设置 recursive=True 来递归监视目录及其子目录中的文件变化。
调用 observer.start 启动观察者，使其开始监听文件系统事件。
使用一个无限循环保持程序运行，以便持续监听文件系统的变化。当按下 Ctrl+C 时，捕获 KeyboardInterrupt 异常，调用 observer.stop 停止观察者，并使用 observer.join 等待观察者线程结束。
除了文件修改事件（on_modified），watchdog 还支持其他文件系统事件，如文件创建（on_created）、文件删除（on_deleted）、文件移动（on_moved）等。你可以根据需要在 FileChangeHandler 类中添加相应的方法来处理这些事件。例如，添加 on_created 方法来处理文件创建事件：
当 recursive=True 时（这是默认情况），如果 path 是一个目录，那么不仅会监控该目录本身的变化，还会递归地监控其所有子目录的变化，即子目录中的文件和子目录的创建、修改、删除、移动等操作都会触发相应的事件。
而当 recursive=False 时，如果 path 是一个目录，只会监控该目录本身的变化，不会深入监控其子目录中的文件和子目录的变化。如果 path 是一个文件，则无论 recursive 的值如何，都只会监控该文件的变化。


"""
"""
实现原理：
`watchdog`是一个用于监控文件系统事件的 Python 库。它可以检测文件和目录的变化，如创建、修改、删除、移动等，并触发相应的事件处理。`watchdog`非常适用于开发需要实时监控文件系统变化的应用，如自动化构建、日志分析、文件同步等。其主要实现或者可以说`watchdog`的构件是基于以下类：
- **Observer**：观察者，用于监视目录并将调用分派给事件处理程序；
- **Event handler**：文件系统事件和事件处理程序；说白了，Observer监控目录，触发 Event handler 针对事件做出响应。

`watchdog`库实现了一个基于操作系统文件系统事件通知机制的文件和目录变化监控系统。其核心原理如下：
- **操作系统级别的通知机制**：在 Linux 系统中，`watchdog`利用了`inotify`内核子系统，它可以跟踪文件系统中的各种事件，如打开、关闭、读取、写入、移动、删除、创建等。
在 MacOS 系统中，利用了`kqueue`通知机制。在 Windows 系统中，使用的是`ReadDirectoryChangesW API`来获取文件系统变动的通知。
- **事件驱动编程**：`watchdog`库通过封装上述操作系统的 API，创建了一个异步事件驱动模型。它初始化一个观察者（Observer）对象，该对象负责监视指定的文件或目录。
- **事件调度与处理**：用户定义一个继承自`FileSystemEventHandler`的类，并覆盖其中的方法（如`on_modified`、`on_created`、`on_deleted`等），用来处理不同类型的文件系统事件。
观察者将这个事件处理器与需要监控的路径相关联，并设置是否递归监控子目录。当操作系统检测到文件系统发生改变时，会发送相应的事件给`watchdog`，观察者接收到这些事件后，会调用已注册的事件处理器对应的方法。
- **线程管理**：`watchdog`内部通常使用线程来监听文件系统事件，这样可以在主线程执行其他任务的同时，后台线程能够持续监听和处理文件系统变动，保证了监控的实时性。
总的来说，`watchdog`库通过底层的操作系统接口监听文件系统事件，然后通过事件驱动的方式，让开发者能够轻松地编写响应这些事件的回调函数，从而实现对文件和目录变更的实时监控。
"""