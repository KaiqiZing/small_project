
import threading

def print_text(text):
    for i in range(10):
        print(text)

thread1 = threading.Thread(target=print_text, args=("Thread 1",))
thread2 = threading.Thread(target=print_text, args=("Thread 2",))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("All threads finished!")

