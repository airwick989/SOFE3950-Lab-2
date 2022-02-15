import os, sys, time



#convert to absolute path and change directory
def cd(path):
    try:
        if(path == ""):
            print(f"The current working directory is {os.getcwd()}\n")
        else:
            os.chdir(os.path.abspath(path))
    except Exception:
        print("cd: no such file or directory: {}".format(path))



def dir(path):
    contents = []
    i = 1

    try:
        if(path == ""):
            contents = os.listdir(os.getcwd())
            print(f"The contents of the current working directory are: \n")
            for item in contents:
                print(f"{i} - {item}\n")
                i = i+1
        else:
            contents = os.listdir(path)
            print(f"The contents of the specified directory are: \n")
            for item in contents:
                print(f"{i} - {item}\n")
                i = i+1
    except Exception:
        print("dir: no such file or directory: {}".format(path))



def help():
    with open("help.txt") as file_in:
        lines = []
        for line in file_in:
            lines.append(line)
    
    for line in lines:
        print(f"\033[34m{line}\033[37m")



def invoke(userInput):
    cmd = "/bin/python3"
    pid = os.fork()
    
    if pid == 0:

        print(f"CHILD: child with pid = {os.getpid()}\n")
        if len(userInput) > 1:
            program = userInput[0]
            sys.argv = userInput

            try:
                script_descriptor = open(program)
                a_script = script_descriptor.read()
            except Exception:
                print(f"\033[31m{program} is not a recognized program within the current directory...\033[37m\n")
                sys.exit()

            try:
                exec(a_script)
                script_descriptor.close()
                sys.exit()
            except Exception:
                print("\033[31mAborted invoked program:\nThe program you invoked incurred an error.")
                print("Try checking the number of arguments you passed, just in case.\033[37m")
                sys.exit()
        else:
            program = ""
            for arg in userInput:
                program += arg
            
            try:
                os.execv(cmd, (cmd, program))
                sys.exit()
            except Exception:
                print("\033[31mAborted invoked program:\nEither the entered program name is not a recognized program in the directory")
                print("OR an error has incurred inside the invoked program.\033[37m")
                sys.exit()

    elif pid > 0:
        print(f"PARENT: parent with pid = {os.getpid()}\n")
        print("--- EVERYTHING BELOW IS FROM INSIDE THE INVOKED PROGRAM ---\n")
        wval = os.wait()
        print("\n--- BACK INSIDE THE SHELL ---\n")
        print(f"PARENT: child has finished with exit code {wval}\n")
        
    else:
        print("\033[31mforking error\n\033[37m")



def execute(userInput):
    userInput = userInput.strip().split(" ")
    command = userInput[0]
    parameter = ""

    for i in range(1, len(userInput)):
        if i == 1:
            parameter += userInput[i]
        else:
            parameter += f" {userInput[i]}"

    if '<' in userInput or '>' in userInput or '>>' in userInput:
        redirection(userInput)
    elif command == "cd":
        cd(parameter)
    elif command == "clr":
        os.system('clear')
    elif command == "dir":
        dir(parameter)
    elif command == "environ":
        print(f"{os.environ}\n")
    elif command == "echo":
        print(f"{parameter}\n")
    elif command == "help":
        help()
    elif command == "pause":
        input("Press Enter key to continue...\n")
    elif command == "quit":
        print("\033[32mExiting shell...\n>>\033[37m")
        sys.exit()
    else:
        command = userInput
        invoke(command)



def redirection(userInput):

    inputflag = False
    outputFlag = False
    outputAppendFlag = False
    endOfStatement = 0
    inputSource = ""
    outputSource = ""
    fdin = sys.__stdin__
    fdout = sys.__stdout__

    if '<' in userInput:
        inputIndex = userInput.index('<')
        inputflag = True
    

    if '>' in userInput:
        outputIndex = userInput.index('>')
        outputFlag = True
    elif '>>' in userInput:
        outputIndex = userInput.index('>>')
        outputAppendFlag = True


    if((inputflag and outputFlag) or (inputflag and outputAppendFlag)):
        endOfStatement = min(inputIndex, outputIndex)
        if inputIndex < outputIndex:
            inputSource = userInput[inputIndex + 1:outputIndex]
            outputSource = userInput[outputIndex + 1:]
        else:
            inputSource = userInput[inputIndex + 1:]
            outputSource = userInput[outputIndex + 1:inputIndex]
        
        inputSource = " ".join(inputSource)
        outputSource = " ".join(outputSource)
        fdin = open(inputSource, "r")
    elif(inputflag):
        endOfStatement = inputIndex
        inputSource = userInput[endOfStatement + 1:]

        inputSource = " ".join(inputSource)
        fdin = open(inputSource, "r")
    else:
        endOfStatement = outputIndex
        outputSource = userInput[endOfStatement + 1:]
        outputSource = " ".join(outputSource)


    if outputFlag:
        fdout = open(outputSource, 'w+')
    elif outputAppendFlag:
        if os.path.exists(outputSource):
            fdout = open(outputSource, 'a')
        else:
            fdout = open(outputSource, 'w+')

    sys.stdin = fdin
    sys.stdout = fdout

    prompt = userInput[:endOfStatement]
    prompt = " ".join(prompt)

    print(f"\ncommand: {prompt} | input source: {inputSource} | output source: {outputSource}\n")

    if inputflag:
        lines = []
        for line in fdin:
            lines.append(line)
        
        for line in lines:
            line = line.strip()
            prompt = "".join(line)
            print(prompt)

    if inputflag:
        fdin.close()
    if outputFlag:
        fdout.close()
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__

    
    



########################################################-- LOOP STARTS HERE --################################################################

if len(sys.argv) > 1:
    try:
        with open(sys.argv[1]) as file_in:
            lines = []
            for line in file_in:
                lines.append(line)
        
        for line in lines:
            line = line.strip()
            execute(line)
    except Exception:
        print(f"{sys.argv[1]} is not a recognized batch file in the current directory...\nContinuing normal execution\n")
        
while True:
    userInput = input(f"\033[32m{os.getcwd()}\nmyshell>>\033[37m ")
    execute(userInput)
    
    


