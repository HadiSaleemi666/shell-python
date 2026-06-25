import sys, os, subprocess, shlex

# def ParseArgumentsForQuotes(processedArgumentsList):
#     inSingleQuote = False
#     inDoubleQuote = False
#     parsedArgument = ""
#     parsedArgumentsList = []
#     afterBackSlash = False
#     processedArgumentsList = ",".join(processedArgumentsList)

#     if len(processedArgumentsList) == 0:
#         return parsedArgumentsList
    
#     for character in processedArgumentsList:
#         if afterBackSlash:
#             parsedArgument += character
#             afterBackSlash = False
#             continue
#         match character:
#             case ",":
#                 if not inSingleQuote or not inDoubleQuote:
#                     parsedArgumentsList.append(parsedArgument)
#                     parsedArgument = ""
#                 else:
#                     parsedArgument += character
#             case "'":
#                 if not inSingleQuote and not inDoubleQuote:
#                     inSingleQuote = True
#                 elif inSingleQuote and not inDoubleQuote:
#                     inSingleQuote = False
#                 elif inSingleQuote and inDoubleQuote:
#                     continue
#                 else:
#                     parsedArgument += character
#             case '"':
#                 if not inSingleQuote and not inDoubleQuote:
#                     inDoubleQuote = True
#                 elif not inSingleQuote and inDoubleQuote:
#                     inDoubleQuote = False
#                 elif inSingleQuote and inDoubleQuote:
#                     continue
#                 else:
#                     parsedArgument += character
#             case " ":
#                 if inSingleQuote or inDoubleQuote:
#                     parsedArgument += character
#                 else:
#                     continue
#             case "\\":
#                 afterBackSlash = True
#             case _:
#                 parsedArgument += character

#     if (len(parsedArgument) > 0):
#         parsedArgumentsList.append(parsedArgument)
    
#     return parsedArgumentsList

# def ProcessArguments(rawArguments):
#     inSingleQuote = False
#     inDoubleQuote = False
#     processedArgument = ""
#     afterBackslash = False
#     processedArgumentsList = []

#     if len(rawArguments) == 0:
#         return processedArgumentsList

#     for i in range(len(rawArguments)):
#         if afterBackslash:
#             processedArgument += rawArguments[i]
#             afterBackslash = False
#             continue
#         match rawArguments[i]:
#             case "'":
#                 if not inSingleQuote and not inDoubleQuote:
#                     processedArgument += rawArguments[i]
#                     inSingleQuote = True
#                 elif inSingleQuote and not inDoubleQuote:
#                     processedArgument += rawArguments[i]
#                     inSingleQuote = False
#                 else:
#                     processedArgument += rawArguments[i]

#             case '"':
#                 if not inDoubleQuote and not inSingleQuote:
#                     processedArgument += rawArguments[i]
#                     inDoubleQuote = True
#                 elif inDoubleQuote and not inSingleQuote:
#                     processedArgument += rawArguments[i]
#                     inDoubleQuote = False
#                 else:
#                     processedArgument += rawArguments[i]
#             case " ":
#                 if not inDoubleQuote and not inSingleQuote:
#                     if i - 1 > 0 and rawArguments[i - 1] != " ":
#                         processedArgumentsList.append(processedArgument)
#                         processedArgument = ""
#                     else:
#                         continue
#                 else:
#                     processedArgument += rawArguments[i]
#             case "\\":
#                 afterBackslash = True
#             case _:
#                 processedArgument += rawArguments[i]

#     if (len(processedArgument) != 0):
#         processedArgumentsList.append(processedArgument)
    
#     return processedArgumentsList

def getExecutablePath(executable):
    system_path = os.environ.get('PATH')
    directories = system_path.split(os.pathsep)
    found = False
    path = ""
    for directory in directories: 
        if os.path.exists(directory) and executable in os.listdir(directory) and os.access(f"{directory}{os.path.sep}{executable}", os.X_OK):
            found = True
            path = directory + os.path.sep + executable
            return found, path
    return found, path

def main():
    # TODO: Uncomment the code below to pass the first stage
     builtinCommands = ["echo", "type", "exit", "pwd", "cd"]
     while (True):
        sys.stdout.write("$ ")
        userInput = input()
        #.find() returns -1 if it fails to find specified delimeter
        # rawArguments = userInput[userInput.find(" ") + 1:] if userInput.find(" ") + 1 != 0 else "" 
        # command = userInput[:userInput.find(" ")] if userInput.find(" ") + 1 != 0 else userInput
        try:
            parsedInput = shlex.split(userInput)
        except ValueError:
            continue

        command = parsedInput[:1]
        arguments = parsedInput[1:]


        processedArgumentsList = []
        #processedArgumentsList = ProcessArguments(rawArguments)
        #parsedArgumentsList = ParseArgumentsForQuotes(processedArgumentsList)
        
        if (command[0] == "exit"):
            break

        elif (command[0] == "echo"):
            print(' '.join(arguments) if len(arguments) > 0 else "")

        elif (command[0] == "type"):
            if (arguments[0] in builtinCommands):
                print(f"{" ".join(arguments)} is a shell builtin")
            else:
                found, path = getExecutablePath(" ".join(arguments))
                if (found):
                    print(f"{" ".join(arguments)} is {path}")
                else:
                    print(f"{" ".join(arguments)}: not found")

        elif (command[0] == "pwd"):
            print(os.getcwd())

        elif (command[0] == "cd"):
            path = " ".join(arguments)
            if (path == "~"):
                path = os.environ.get('HOME')
            if (os.path.exists(path)):
                os.chdir(path)
            else:
                print(f"{command[0]}: {path}: No such file or directory")
                
        else:
            found, path = getExecutablePath(command[0])
            if (found):
                subprocess.run((command[0] + " " + " ".join(arguments)), shell=True)
            else:
                print(f"{command[0]}: command not found")


if __name__ == "__main__":
    main()
