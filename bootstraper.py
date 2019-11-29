import os
import subprocess
import time    
import subprocess    
import threading    
from threading import start_new_thread


cmd1 = "py -3 weatherStation.py"
cmd2 = "py -3 mqqtBrooker.py.py"
cmd3 = "py -3 RestAPI.py"
file_name1 = "/tmp/one"    
file_name2 = "/tmp/two"
file_name2 = "/tmp/three"


def my_function(command, file_name, lock):
    process_obj = subprocess.Popen(command, stdout=subprocess.PIPE)
    command_output, command_error = process_obj.communicate()
    print (command_output)
    lock.acquire()
    with open(file_name, 'a+') as f:
        f.write(command_output)
        print ("writing")
    lock.release()


if __name__ == '__main__':
    keep_running = True
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    while keep_running:
        try:
            start_new_thread(my_function, (cmd1, file_name1, lock1))
            start_new_thread(my_function, (cmd2, file_name2, lock2))
            time.sleep(10)
        except KeyboardInterrupt:
            keep_running = False