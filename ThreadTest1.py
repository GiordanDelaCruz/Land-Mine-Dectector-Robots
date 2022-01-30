import threading
from threading import Thread
from time import sleep, perf_counter

def stask():
    print('Starting a task in a single thread ... Thread id... ', threading.get_ident(), '...OS Thread ID...', threading.get_native_id())
    # do something
    sleep(1)
    print('done')

def ptask():
    t = threading.current_thread()
    print('Starting a multi-threaded task ... Thread name... ', t.name, '....Thread ID...', threading.get_ident(), '...OS Thread ID...', threading.get_native_id())
    # do something
    sleep(1)
    print('done')


start_time = perf_counter()

stask()
stask()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')

#
#
#


start_time = perf_counter()

# create two new threads
t1 = Thread(target=ptask)
t2 = Thread(target=ptask)

# start the threads

t1.start()
# print('starting thread ', t1.getName())

t2.start()
# print('starting thread ', t2.name)

# wait for the threads to complete
t1.join()
t2.join()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')


