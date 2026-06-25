import sys, os, subprocess, shlex

def ParseArguments(splitRawArgumentsList):
    inSingleQuote = False
    inDoubleQuote = False
    parsedArgument = ""
    parsedArgumentsList = []
    splitRawArgumentsList = ",".join(splitRawArgumentsList)

    if len(splitRawArgumentsList) == 0:
        return parsedArgumentsList
    
    for character in splitRawArgumentsList:
        match character:
            case ",":
                if not inSingleQuote or not inDoubleQuote:
                    parsedArgumentsList.append(parsedArgument)
                    parsedArgument = ""
                else:
                    parsedArgument += character
            case "'":
                if not inSingleQuote and not inDoubleQuote:
                    inSingleQuote = True
                elif inSingleQuote and not inDoubleQuote:
                    inSingleQuote = False
                elif inSingleQuote and inDoubleQuote:
                    continue
                else:
                    parsedArgument += character
            case '"':
                if not inSingleQuote and not inDoubleQuote:
                    inDoubleQuote = True
                elif not inSingleQuote and inDoubleQuote:
                    inDoubleQuote = False
                elif inSingleQuote and inDoubleQuote:
                    continue
                else:
                    parsedArgument += character
            case " ":
                if inSingleQuote or inDoubleQuote:
                    parsedArgument += character
                else:
                    continue
            case _:
                parsedArgument += character

    if (len(parsedArgument) > 0):
        parsedArgumentsList.append(parsedArgument)
    
    return parsedArgumentsList

def SplitRawArguments(rawArguments):
    inSingleQuote = False
    inDoubleQuote = False
    splitArgument = ""
    splitRawArgumentsList = []
    specialQuotes = ["'", '"']

    if len(rawArguments) == 0:
        return splitRawArgumentsList

    for i in range(len(rawArguments)):
        match rawArguments[i]:
            case "'":
                if not inSingleQuote and not inDoubleQuote:
                    splitArgument += rawArguments[i]
                    inSingleQuote = True
                elif inSingleQuote and not inDoubleQuote:
                    splitArgument += rawArguments[i]
                    inSingleQuote = False
                else:
                    splitArgument += rawArguments[i]

            case '"':
                if not inDoubleQuote and not inSingleQuote:
                    splitArgument += rawArguments[i]
                    inDoubleQuote = True
                elif inDoubleQuote and not inSingleQuote:
                    splitArgument += rawArguments[i]
                    inDoubleQuote = False
                else:
                    splitArgument += rawArguments[i]
            case " ":
                if not inDoubleQuote and not inSingleQuote:
                    if i - 1 > 0 and rawArguments[i - 1] in specialQuotes:
                        splitRawArgumentsList.append(splitArgument)
                        splitArgument = ""
                    else:
                        continue
                else:
                    splitArgument += rawArguments[i]
            case _:
                splitArgument += rawArguments[i]

    if (len(splitArgument) != 0):
        splitRawArgumentsList.append(splitArgument)
    
    return splitRawArgumentsList

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
        rawArguments = userInput[userInput.find(" ") + 1:] if userInput.find(" ") + 1 != 0 else "" 
        command = userInput[:userInput.find(" ")] if userInput.find(" ") + 1 != 0 else userInput
        shlexOutput = shlex.split(userInput)

        splitRawArgumentsList = []
        splitRawArgumentsList = SplitRawArguments(rawArguments)
        parsedArgumentsList = ParseArguments(splitRawArgumentsList)
        
        if (command == "exit"):
            break

        elif (command == "echo"):
            print(' '.join(parsedArgumentsList) if len(parsedArgumentsList) > 0 else "")

        elif (command == "type"):
            if (parsedArgumentsList[0] in builtinCommands):
                print(f"{" ".join(parsedArgumentsList)} is a shell builtin")
            else:
                found, path = getExecutablePath(" ".join(parsedArgumentsList))
                if (found):
                    print(f"{" ".join(parsedArgumentsList)} is {path}")
                else:
                    print(f"{" ".join(parsedArgumentsList)}: not found")

        elif (command == "pwd"):
            print(os.getcwd())

        elif (command == "cd"):
            path = " ".join(parsedArgumentsList)
            if (path == "~"):
                path = os.environ.get('HOME')
            if (os.path.exists(path)):
                os.chdir(path)
            else:
                print(f"{command}: {path}: No such file or directory")
                
        else:
            found, path = getExecutablePath(command)
            if (found):
                subprocess.run((command + " " + " ".join(shlexOutput)), shell=True)
            else:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
