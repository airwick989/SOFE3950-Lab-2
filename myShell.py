import os, sys, threading



#change directory command
def cd(path):
    try:
        if(path == ""): #If path parameter is not present, simply print the current working directory
            print(f"The current working directory is {os.getcwd()}\n")
        else:
            os.chdir(os.path.abspath(path)) #Changes the current working directory to path parameter
    except Exception:
        print("cd: no such file or directory: {}".format(path)) #error message



#Print the contents of the passed directory
def dir(path):
    contents = []   #Used to hold directory contents
    i = 1   #Counter for printing list

    try:
        if(path == ""): #If path parameter is not present, print contents of the current working directory
            contents = os.listdir(os.getcwd())  #Get the contents of the directory
            print(f"The contents of the current working directory are: \n")
            for item in contents:   #Format and print the contents
                print(f"{i} - {item}\n")
                i = i+1
        else:
            contents = os.listdir(path)
            print(f"The contents of the specified directory are: \n")
            for item in contents:
                print(f"{i} - {item}\n")
                i = i+1
    except Exception:
        print("dir: no such file or directory: {}".format(path))    #error message



#Displays user manual in terminal
def help(): #Retrieve every line from the user manual
    with open("readme.txt") as file_in:
        lines = []
        for line in file_in:
            lines.append(line)
    
    for line in lines:  #Print and format the user manual for display in terminal
        print(f"\033[34m{line}\033[37m")



#Helper function that will use the exec system call to run the passed program
#Used in the invoke() and invokeProgram() methods
def runProgram(userInput):
    cmd = "/bin/python3"
    if len(userInput) > 1:  #Checks if there are arguments passed to the program
        program = userInput[0]
        sys.argv = userInput

        try:    #try to open and read the program
            script_descriptor = open(program)
            a_script = script_descriptor.read()
        except Exception:   #print error if program doesn't exist
            print(f"\033[31m{program} is not a recognized program within the current directory...\033[37m\n")
            sys.exit()

        try:    #Try to execute the program and close upon completion
            exec(a_script)
            script_descriptor.close()
            sys.exit()
        except Exception:   #Abort the program and return to the shell if an error within the external program has occurred
            print("\033[31mAborted invoked program:\nThe program you invoked incurred an error.")
            print("Try checking the number of arguments you passed, just in case.\033[37m")
            sys.exit()
    else:   #if no parameters were passed with the program, rebuilds the program name as a single string
        program = ""
        for arg in userInput:
            program += arg
        
        try:    #Try to execute the program and close upon completion
            os.execv(cmd, (cmd, program))
            sys.exit()
        except Exception:   #Abort the program and return to the shell if program doesn't exist or if an error within the external program has occurred
            print("\033[31mAborted invoked program:\nEither the entered program name is not a recognized program in the directory")
            print("OR an error has incurred inside the invoked program.\033[37m")
            sys.exit()



#Invokes the program passed to it to be run in a child process
def invoke(userInput):
    pid = os.fork() #Creates child process
    
    if pid == 0:    #In the child, display pid and run the program using the helper function
        print(f"CHILD: child with pid = {os.getpid()}\n")
        runProgram(userInput)
    elif pid > 0:   #In the parent, display pid, wait for child process's termination, display child's exit code upon termination, then return to shell
        print(f"PARENT: parent with pid = {os.getpid()}\n")
        print("--- EVERYTHING BELOW IS FROM INSIDE THE INVOKED PROGRAM ---\n")
        wval = os.wait()
        print("\n--- BACK INSIDE THE SHELL ---\n")
        print(f"PARENT: child has finished with exit code {wval}\n")
        
    else:   #error message
        print("\033[31mforking error\n\033[37m")



#primary method for program invocation
#Checks if external program is to be run in the background or normally
def invokeProgram(userInput):
    if userInput[len(userInput) - 1] == '&':    #Checks if the '&' symbol is present at the end of the command
        if len(userInput) > 2:  #If arguments are present, correctly rebuild the list of arguments with the '&' symbol
            arguments = userInput[:len(userInput) - 1]
        else:   #If no arguments present, simply retrieve the program name
            arguments = userInput

        #Since '&' symbol is present at the end of the command, the external program is run as a seprate thread in the background
        background_program = threading.Thread(target= runProgram, name= "myShell.backgroundProgram", args= (arguments,))#Creates thread
        background_program.start()  #Thread begins execution
        background_program.join()   #Collect thread upon completion
    else:   #If no '&' symbol present, invoke the external program in a child process in the invoke() method
        invoke(userInput)



#Main body of user input execution
#Checks which command has been entered in the shell and performs appropriate actions
def execute(userInput):
    userInput = userInput.strip().split(" ")    #Tokenize the user input
    command = userInput[0]  #The first segment of the input is the command or program name
    parameter = ""

    for i in range(1, len(userInput)):  #Rebuilds the remaining portion of the user input as a single list of parameters
        if i == 1:
            parameter += userInput[i]
        else:
            parameter += f" {userInput[i]}"

    if '<' in userInput or '>' in userInput or '>>' in userInput:   #If any redirection tokens are detected in input, jump to redirection() method
        redirection(userInput)
    elif command == "cd":   #If the first token in the input is 'cd', the command performed is cd()
        cd(parameter)
    elif command == "clr":  #If the first token in the input is 'clr', the terminal window is cleared
        os.system('clear')
    elif command == "dir":  #If the first token in the input is 'dir', the command performed is dir()
        dir(parameter)
    elif command == "environ":  #If the first token in the input is 'environ', the environment strings are printed in the terminal
        print(f"{os.environ}\n")
    elif command == "echo": #If the first token in the input is 'echo', print the remaining portion of the input to the terminal
        print(f"{parameter}\n")
    elif command == "help": #If the first token in the input is 'help', the command performed is help()
        help()
    elif command == "pause":    #If the first token in the input is 'pause', the shell pauses until the enter key is pressed
        input("Press Enter key to continue...\n")
    elif command == "quit": #If the first token in the input is 'quit', the shell terminates execution
        print("\033[32mExiting shell...\n>>\033[37m")
        sys.exit()
    else:   #If the first token in the input is not a recognized command, it is interpreted as an invocation of an external program
        command = userInput
        invokeProgram(command)



#Method to handle I/O redirection
def redirection(userInput):

    #Flags to be used later
    inputflag = False
    outputFlag = False
    outputAppendFlag = False
    endOfStatement = 0
    inputSource = ""
    outputSource = ""
    fdin = sys.__stdin__
    fdout = sys.__stdout__
    strError = "\033[31mAbort Execution:\nOnly 1 input and output redirection is supported in a command\033[37m\n"

    if '<' in userInput:    #Checks if any input redirection tokens are present
        if userInput.count('<') > 1:    #If there is more than 1 input redirection token, print an error and return to the shell
            print(strError)
            return
        else:   
            inputIndex = userInput.index('<')   #Retrieve the index of the input redirection token in the user input
            inputflag = True    #Set the input flag true, used for later
    

    if '>' in userInput:    #Checks if any output with truncate redirection tokens are present
        if userInput.count('>') > 1:    #If there is more than 1 token, print an error and return to the shell
            print(strError)
            return
        else:
            outputIndex = userInput.index('>')  #Retrieve the index of the redirection token in the user input
            outputFlag = True   #Set output flag true, used for later
    
    if '>>' in userInput: #Checks if any output with append redirection tokens are present
        if userInput.count('>>') > 1:   #Error handling and initialization...
            print(strError)
            return
        else:
            outputIndex = userInput.index('>>')
            outputAppendFlag = True
    
    if outputFlag and outputAppendFlag: #If both types of output flags are raised, print error and return to shell
        print(strError)
        return


    try:    #Try to execute commands with redirection
        #If the input flag and either of the output flags are raised, segment the user input accordingly
        if((inputflag and outputFlag) or (inputflag and outputAppendFlag)):
            endOfStatement = min(inputIndex, outputIndex)
            if inputIndex < outputIndex:
                inputSource = userInput[inputIndex + 1:outputIndex]
                outputSource = userInput[outputIndex + 1:]
            else:
                inputSource = userInput[inputIndex + 1:]
                outputSource = userInput[outputIndex + 1:inputIndex]
            
            #Rebuilds the file names for the input and output sources as strings
            inputSource = " ".join(inputSource)
            outputSource = " ".join(outputSource)
            fdin = open(inputSource, "r")   #open a file descriptor for the input source
        elif(inputflag):    #If only input redirection is detected, segment the user input accordingly
            endOfStatement = inputIndex
            inputSource = userInput[endOfStatement + 1:]

            inputSource = " ".join(inputSource)
            fdin = open(inputSource, "r")
        else:   #If only output redirection is detected, segment the user input accordingly
            endOfStatement = outputIndex
            outputSource = userInput[endOfStatement + 1:]
            outputSource = " ".join(outputSource)


        if outputFlag:  #If the output with truncate flag is raised, open a file descriptor for the output destination in mode 'w+'
            fdout = open(outputSource, 'w+') #Mode 'w+' will create the file if it does not exist
        elif outputAppendFlag:  #If the output with append flag is raised, open a file descriptor for the output destination in mode 'a'
            if os.path.exists(outputSource):
                fdout = open(outputSource, 'a') #Mode 'a' will append to the end of the file if it exists
            else:
                fdout = open(outputSource, 'w+')    #Default to mode 'w+' if file does not exist

        #Redirect the input and output streams to their respective file descriptors
        sys.stdin = fdin
        sys.stdout = fdout

        #prompt is the command portion of the user input
        prompt = userInput[:endOfStatement]
        prompt = " ".join(prompt)

        #---All initialization for I/O redirection is complete at this point---#

        #Print statement is only for information purposes. May be commented out
        print(f"\ncommand: {prompt} | input source: {inputSource} | output source: {outputSource}\n")

        if inputflag:   #If the input flag is raised, retrieve every line from the input source
            lines = []
            for line in fdin:
                lines.append(line)
            
            for line in lines:  #Execute every line from the input source via the command in the user input (prompt)
                line = line.strip()
                passedCommand = prompt + " " + line
                execute(passedCommand)
        else:   #If there is no input redirection, simply execute the command in the user input (prompt)
            execute(prompt) #If there is output redirection, all output statements in the execution will be printed to the output destination

        #Close any open file descriptors
        if inputflag:
            fdin.close()
        if outputFlag or outputAppendFlag:
            fdout.close()

        #Redirect the I/O channels to their default streams
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

    except Exception:   #If an error occurs, prints error message
        print("\033[31mAborted Execution:\nPlease check the file name(s) entered\033[37m\n")
    

    
########################################################-- LOOP STARTS HERE --################################################################

#This if for starting the shell with a batchfile
if len(sys.argv) > 1:   #Only perform the following if the shell is launched with an argument
    try:    #try to open the batchfile and retrieve every line
        with open(sys.argv[1]) as file_in:
            lines = []
            for line in file_in:
                lines.append(line)
        
        for line in lines:  #execute every command in the batchfile
            line = line.strip()
            execute(line)
    except Exception:   #If an error occurs, print an error message and launch the shell
        print(f"{sys.argv[1]} is not a recognized batch file in the current directory or it contains troublesome commands...\nContinuing normal execution\n")

while True: #Continous loop: display the current working directory and retrieve user input
    userInput = input(f"\033[32m{os.getcwd()}\nmyshell>>\033[37m ")
    execute(userInput)  #Execute the user input