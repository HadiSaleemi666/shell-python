import sys, os, subprocess, shlex, readline

redirectionTypeList = ["1>", ">", "2>", ">>", "1>>", "2>>"]
builtinCommands = ["echo", "type", "exit", "pwd", "cd"]
matches = []

def getAutoCompleteList():
    autoCompleteList = [command for command in builtinCommands]
    system_path = os.environ.get('PATH')
    directories = system_path.split(os.pathsep)
    executableDirectoryList = []
    for directory in directories: 
        if os.path.exists(directory):
            executableDirectoryList = os.listdir(directory)
            autoCompleteList += executableDirectoryList
            
    return autoCompleteList


def RedirectOutput(argumentsList):
    indexOfArgumentsRemoval = -10
    isRedirectionUnsuccessful = False
    redirectionType = None

    for type in redirectionTypeList:
        try:
            indexOfArgumentsRemoval = argumentsList.index(type)
        except ValueError:
            continue
        redirectionType = type

    if redirectionType is not None:

        try:
            redirectedLocation = argumentsList[indexOfArgumentsRemoval + 1]
        except IndexError:
            print("Redirection specified but no location is provided.")
            isRedirectionUnsuccessful = True
            return isRedirectionUnsuccessful, indexOfArgumentsRemoval
        
        if not os.path.exists(redirectedLocation):
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
            
        match redirectionType:
            case "2>":
                sys.stderr = open(redirectedLocation, 'w')
            case "1>" | ">":
                sys.stdout = open(redirectedLocation, 'w')
            case "1>>" | ">>":
                sys.stdout = open(redirectedLocation, 'a')
            case "2>>":
                sys.stderr = open(redirectedLocation, 'a')
            case _:
                pass
    else:
        return isRedirectionUnsuccessful, indexOfArgumentsRemoval
    
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

def CompleteWord(prefix, state):
    #state is simply a counter used to identify the number of options available as well as to identify the stopping condition
    if prefix == '':
        prefix = '?'
    if state == 0: 
        matches = []
        commands = getAutoCompleteList()
    for command in commands:
        if command.startswith(prefix):
            matches.append(command)
    sorted(matches)
    print("\x07")
    return matches[state] + " " if state < len(matches) else None
    
def DisplayMatches(substitution, matches, longest_match_len):
    print()
    print("  ".join(sorted(matches)))
    sys.stdout.write("$ " + readline.get_line_buffer())
    sys.stdout.flush()


def main():
    # TODO: Uncomment the code below to pass the first stage
     originalSTDOUT = sys.stdout
     originalSTDERR = sys.stderr
     readline.set_completer(CompleteWord)
     readline.parse_and_bind("tab: complete")
     #readline.set_completion_display_matches_hook(DisplayMatches)

     while (True):
        sys.stdout.write("$ ")
        sys.stdout.flush()
        userInput = input()
        parsedInput = ""

        try:
            parsedInput = shlex.split(userInput)
        except ValueError:
            continue

        if not parsedInput:
            continue
   
        command = parsedInput[:1]
        arguments = parsedInput[1:]
        indexOfArgumentRemoval = -1

        #redirect output
        for redirectionType in redirectionTypeList:
            if redirectionType in arguments:
                isRedirectionUnsuccessful, indexOfArgumentRemoval = RedirectOutput(arguments)
            
                if (isRedirectionUnsuccessful):
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
                subprocess.run([command[0]] + arguments, executable=path, stdout=sys.stdout, stderr=sys.stderr)
            else:
                print(f"{command[0]}: command not found")
        
        if sys.stdout != originalSTDOUT:
            sys.stdout = originalSTDOUT

        if sys.stderr != originalSTDERR:
            sys.stderr = originalSTDERR


if __name__ == "__main__":
    main()