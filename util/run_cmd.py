import subprocess
from subprocess import PIPE
from threading import Timer
import traceback


def run_cmd(cmd, timeout=10):

    def kill_proc(p):
        p.terminate()

    print '[DEBUG] run cmd:', cmd
    proc = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout, kill_proc, [proc])

    try:
        timer.start()
        (outs, errs) = proc.communicate()
    except Exception as e:
        print 'exception:', e
    finally:
        timer.cancel()

    ret = proc.returncode
    return (ret, outs, errs)