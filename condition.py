#-*- coding:utf-8 -*-

from urllib import request
import time
import threading
import random

#Locks, RLocks, Semaphores, Conditions, Events and Queues
#http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/


class Producter(threading.Thread):
    def __init__(self, integers, condition):
        threading.Thread.__init__(self)
        self.integers = integers
        self.condition = condition

    def run(self):
        i = 1        
        while True:
            integer = random.randint(0, 256)
            self.condition.acquire()
            print("Producter-condition acquires by %s" % self.name)
            self.integers.append(integer)
            print('%d appended to list by %s' % (integer, self.name))
            print('Producter-condition notified by %s' % self.name)
            self.condition.notify()  #唤醒消费者线程
            print('Producter-condition released by %s' % self.name)
            self.condition.release()
            time.sleep(0.5)
            i += 1
            if i >= 10:
                break
            

class Consumer(threading.Thread):
    def __init__(self, integers, condition):
        threading.Thread.__init__(self)
        self.integers = integers
        self.condition = condition
    def run(self):
        i = 1
        while True:
            self.condition.acquire()
            print('Consumer-condition acquired by %s' % self.name)
            while True:
                if self.integers:
                    integer = self.integers.pop()
                    print('%d popped from list by %s' % (integer, self.name))
                    break
                print('Consumer-condition wait by %s' % self.name)
                self.condition.wait()  #等待商品，并且释放资源
            print("Consumer-condtion released by %s" % self.name)
            self.condition.release()
            i += 1
            if i >= 10:
                break

def main():
    integers = list()
    condition = threading.Condition()
    t1 = Producter(integers, condition)
    t2 = Consumer(integers, condition)

    t1.start()
    t2.start()
    t1.join()
    t1.join()

if __name__ == "__main__":
    main()
