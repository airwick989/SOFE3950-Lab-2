from ast import arguments
import os, sys, time, signal, multiprocessing


cmd = "/bin/python3"
userInput = input("Enter a program name with appropriate arguments: ")
userInput = userInput.strip().split()
program = userInput[0]

pid = os.fork()
if pid == 0:

    print(f"CHILD: child with pid = {os.getpid()}\n")
    if len(userInput) > 1:
        sys.argv = userInput
        script_descriptor = open(program)
        a_script = script_descriptor.read()
        exec(a_script)
        script_descriptor.close()
    else:
        os.execv(cmd, (cmd, program))
        sys.exit()

elif pid > 0:

    print(f"PARENT: parent with pid = {os.getpid()}\n")
    print("--- EVERYTHING BELOW IS FROM INSIDE THE INVOKED PROGRAM ---\n")
    wval = os.wait()
    print("\n--- BACK INSIDE THE SHELL ---\n")
    print(f"PARENT: child has finished with exit code {wval}\n")
    
else:
    print("forking error\n")


