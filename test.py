import os, sys, time, signal, multiprocessing


cmd = "/bin/python3"

pid = os.fork()
if pid == 0:
    print(f"CHILD: child with pid = {os.getpid()}\n")
    os.execv(cmd, (cmd, "hello.py"))
    sys.exit()
elif pid > 0:
    print(f"PARENT: parent with pid = {os.getpid()}\n")
    wval = os.wait()
    print(f"PARENT: child has finished with exit code {wval}\n")
else:
    print("forking error")