import schedule    
from datetime import datetime, timedelta, time
import time
from timeout_decorator import timeout, TimeoutError

def print_func(x):
    print(x)

print_func("nice to meet you")


@timeout(5)
def yo():
    schedule.every(1).seconds.do(print_func, "nyan").tag('taskA')
    while True:
        schedule.run_pending()
        time.sleep(1)

def ya():
    schedule.every(1).seconds.do(print_func, "yaaa").tag('taskB')
    while True:
        schedule.run_pending()
        time.sleep(1)


try:
    yo()   
except TimeoutError:
    print("timeout")

schedule.clear('taskA')

ya()
    