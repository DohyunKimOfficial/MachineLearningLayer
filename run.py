import time
import subprocess
import signal


class GracefulExit(Exception):
    pass


def signal_handler(signum, frame):
    raise GracefulExit()


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

processes = []

processes.append(subprocess.Popen(['python', 'scheduler.py']))
processes.append(subprocess.Popen(['python', 'worker.py']))
processes.append(subprocess.Popen(['python', 'worker.py']))
processes.append(subprocess.Popen(['python', 'worker.py']))
processes.append(subprocess.Popen(['python', 'worker.py']))
processes.append(subprocess.Popen(['python', 'worker.py']))

try:
    while True:
        time.sleep(60)
except GracefulExit:
    for process in processes:
        process.terminate()
    print "Subprocess exiting gracefully"
