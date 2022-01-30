import os
from multiprocessing import Process, Pool
from time import sleep, perf_counter


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(plist):
    name = plist[0]
    balance = plist[1]
    info('function f from ' + name)
    print('hello', name)
    print('my balance = ', balance)
    print('....')


if __name__ == '__main__':
    info('main line')
    start_time = perf_counter()
    p = Process(target=f, args=(['bob', 500],))
    p.start()
    p.join()
    end_time = perf_counter()
    print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
    #
    #
    with Pool(processes=2) as pl:
        pl.map(f, [['jay', 1000], ['lilac', 2000]])
        res = pl.apply_async(os.getpid, ())
        print('pid = ', res.get())
        mres = [pl.apply_async(os.getpid, ()) for i in range(2)]
        print([r.get() for r in mres])

