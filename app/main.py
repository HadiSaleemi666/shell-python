import sys, os, subprocess, shlex

def RedirectOutput(argumentsList):
    #redirecting output
    indexOfArgumentsRemoval = -1
    isRedirectionUnsuccessful = False
    for i in range(len(argumentsList)):
        match argumentsList[i]:
            case "1>" | ">":
                #redirection of standard output case
                indexOfArgumentsRemoval = i
                try:
                    redirectedLocation = argumentsList[i + 1]
                except IndexError:
                    print("Redirection specified but no location is provided.")
                    isRedirectionUnsuccessful = True
                    return isRedirectionUnsuccessful, indexOfArgumentsRemoval
                if os.path.exists(redirectedLocation):
                    sys.stdout = open(redirectedLocation, 'w')
                else:
                    createFile = []
                    createFile.append("touch")
                    createFile.append(redirectedLocation)
                    found, path = getExecutablePath(createFile[0])
                    if (found):
                        subprocess.run(createFile, executable=path)
                    else:
                        print("Error occurred in 'touch' path retrieval.")
                        isRedirectionUnsuccessful = True
                        return isRedirectionUnsuccessful, indexOfArgumentsRemoval
                    sys.stdout = open(redirectedLocation, 'w')
            case _:
                continue
    return isRedirectionUnsuccessful, indexOfArgumentsRemoval

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

        try:
            parsedInput = shlex.split(userInput)
        except ValueError:
            continue

        command = parsedInput[:1]
        arguments = parsedInput[1:]
        originalOutputLocation = sys.stdout
        indexOfArgumentRemoval = -1

        #redirect output
        if "1>" in arguments or ">" in arguments:
            isRedirectionUnsuccessful, indexOfArgumentRemoval = RedirectOutput(arguments)
        
            if (isRedirectionUnsuccessful):
                sys.stdout = originalOutputLocation
                continue
            
            arguments = arguments[:indexOfArgumentRemoval]
        
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
                subprocess.run([command[0]] + arguments, executable=path, stdout=sys.stdout)
            else:
                print(f"{command[0]}: command not found")
        
        if sys.stdout != originalOutputLocation:
            sys.stdout = originalOutputLocation


if __name__ == "__main__":
    main()
