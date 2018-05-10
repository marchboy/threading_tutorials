#-*- coding:utf-8 -*-

from urllib import request
import time
import threading


#Locks, RLocks, Semaphores, Conditions, Events and Queues
#http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/


class FetchUrls(threading.Thread):
    """
    Thread checking URLs
    类FetchUrls是threading.Thread的子类，他拥有一个URL列表和一个写URL内容的文件对象
    """
    def __init__(self, urls, output, lock=None):
        """
        Constructor
        @param urls list of urls to check
        @param output file to write urls output
        """
        threading.Thread.__init__(self)
        self.urls = urls
        self.output = output
        self.lock = lock  #传入的lock对象

    def run(self):
        """
        实现父类Thread的run方法，打开URL，并且一个一个的下载URL的内容
        """
        while self.urls:
            url = self.urls.pop()
            req = request.Request(url)
            try:
                d = request.urlopen(req)
            except request.URLError as e:
                print('URL %s failed: %s' % (url, e.reason))

            self.lock.acquire()  #获得lock对象，并阻塞其他线程获取lock对象
            print('lock acquired by %s' % self.name)
            print("-" * 35)
            self.output.write(d.read())
            print('write done by %s' % self.name)
            print('lock release by %s ' % self.name)
            self.lock.release()  #释放lock对象，其他线程可以重新获取lock对象
            print('URL %s fetched by %s' % (url, self.name))

            """
            如果一个锁的状态是unlocked，调用acquire()方法改变它的状态为locked；
            如果一个锁的状态是locked，acquire()方法将会阻塞，直到另一个线程调用release()方法释放了锁；
            如果一个锁的状态是unlocked调用release()会抛出RuntimeError异常；
            如果一个锁的状态是locked，调用release()方法改变它的状态为unlocked。
            """


def main():
    urls1 = ['http://www.google.com', 'http://www.baidu.com']
    urls2 = ['http://www.yahoo.com', 'http://www.youtube.com']
    lock = threading.Lock()
    f = open('output_with_nolock.txt', 'wb+')
    # t1 = FetchUrls(urls1, f)
    # t2 = FetchUrls(urls2, f)
    t1 = FetchUrls(urls1, f, lock)
    t2 = FetchUrls(urls2, f, lock)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    f.close()

if __name__ == "__main__":
    main()
