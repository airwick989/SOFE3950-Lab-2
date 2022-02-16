-----------myShell USER MANUAL-----------



Setup
----------------------------------------
- Open your Linux terminal and ensure you have python Installed.
- To check if you have Python installed, enter 'python3 --version'
- If Python is not installed, enter 'sudo apt-get install python3' and enter your credentials
- After ensuring Python is installed in your Linux environment, see the "Launching myShell" section of this manual.



Launching myShell
----------------------------------------
- WARNING: myShell must be launched in a Linux environment for full functionality.
- WARNING: If myShell is launched in Windows, some functionality may be limited.

1. Ensure you have python installed in 
2. Open the folder containing myshell.py in a Linux terminal
3. Enter 'python3 myshell.py' to launch myShell



Launching myShell with a Batchfile 
----------------------------------------
- It is possible to launch myShell and have it automatically take input from a batchfile.
- When launching myShell.py from your Linux terminal, you can include the name of the batchfile after myShell.py
- Format:	'python3 myshell.py <batchFile>'
- This will cause myShell to execute the commands in the batchfile line by line.



Commands
----------------------------------------
1. cd
	- 'cd <directory>' changes the current working directory to <directory>
	- If the <directory> argument is not present, it will report the current directory.
2. clr
	- 'clr' will clear the screen
3. dir
	- 'dir <directory>' lists the contents of directory <directory>
	- If the <directory> argument is not present, it will list the contents of the current directory.
4. environ
	- 'environ' lists all the environment strings
5. echo
	- 'echo <comment1> <comment2> ... <commentn>' displays a everything entered after 'echo' on the terminal
6. help
	- 'help' will display the user manual on the terminal
7. pause
	- 'pause' will pause the operation of the shell until the Enter key is pressed
8. quit
	- 'quit' will exit the shell



Invocation of External Programs 
----------------------------------------
- Entering anything other than the list of recognized commands will be interpreted as a program invocation of the external program named <programname>. 
- Following the program name, you can enter a list of arguments to pass to the external program.
- Format:	'<programname>'		OR	'<programname> <arg1> <arg2> ... <argn>'

- To run an external program in the background, follow the same steps above, and enter '&' after the program name or after the last argument.
- WARNING: Ensure there is a space between the program name or last argument and the '&' symbol, otherwise it will be interpreted as part of the program name or last argument
- Format:	'<programname> &'	OR	'<programname> <arg1> <arg2> ... <argn> &'



I/O Redirection
----------------------------------------
- The input and output streams can be redirected to files with '<', '>', '>>'.

- Input Redirection:
	- Done using '<'.
	- Placed after a command, where every line in the input file will be passed to the command.
	- Format:	'<command> < <inputSource>'
	- If the command is given a parameter ('<command> <parameter> < <inputSource>'), the parameter will be ignored.
	- Example Input:	'echo < file.txt'

- Output Redirection using Truncate:
	- Done using '>'.
	- Placed after a command, where all output to the terminal is redirected to a specified output file.
	- If the output file exists, it will be overwitten. If it does not exist, the file will be created.
	- Format:	'<command> > <outputDestination>'	OR	'<command> <parameter> > <outputDestination>'
	- Example Input:	'dir C:\Users\johndoe\Desktop > file.txt'

- Output Redirection using Append:
	- Done using '>>'.
	- Placed after a command, where all output to the terminal is redirected to a specified output file.
	- If the output file exists, the output will be appended to the end of the file. If it does not exist, the file will be created.
	- Format:	'<command> >> <outputDestination>'	OR	'<command> <parameter> >> <outputDestination>'
	- Example Input:	'echo Hello, my name is John Doe >> file.txt'

- WARNING: For a given command, a maximum of 1 input redirection and 1 output redirection (of either type) is supported
- WARNING: It does not matter where the input and output redirection occurs in the user input, so long as all redirection comes after the command
- Sample Accepted Inputs:	'echo < inputFile.txt > outputFile.txt'
				'dir >> outputFile.txt < directory.txt'