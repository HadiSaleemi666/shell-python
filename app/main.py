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

def getDirectory(prefix, userInput, startIndex, isUserWritingArgument):
    prefix = userInput[startIndex:] if isUserWritingArgument and len(prefix) == 0 else prefix
    endIndex = userInput.find(prefix) if len(prefix) > 0 and prefix != userInput[startIndex:] else len(userInput)
    directory = os.getcwd() + os.path.sep + userInput[startIndex:endIndex] if startIndex != endIndex else os.getcwd()
    directory = directory[:len(directory) - 1] if directory.endswith("/") else directory
    return directory

def CompleteWord(prefix, state):
    #state is simply a counter used to identify the number of options available as well as to identify the stopping condition
    global matches
    userInput = readline.get_line_buffer()
    startIndex = userInput.find(" ")
    startIndex += 1
    isUserWritingArgument = bool(startIndex)
    directory = getDirectory(prefix, userInput, startIndex, isUserWritingArgument)
    
    if prefix == '' and not isUserWritingArgument:
        return None
    
    if state == 0:
        match isUserWritingArgument: 
            case True:
                documentsInCWDList = os.listdir(directory) 
                documentsInCWDList = list(set(documentsInCWDList))
                matches = [document for document in documentsInCWDList if document.startswith(prefix)] if len(prefix) > 0 and len(documentsInCWDList) > 1 else documentsInCWDList

            case _:
                commands = getAutoCompleteList()
                commands = list(set(commands))
                matches = [command for command in commands if command.startswith(prefix)]

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
     completerDelimiters = readline.get_completer_delims()
     readline.set_completer_delims(completerDelimiters.replace("-", ""))
     readline.set_completer(CompleteWord)
     readline.parse_and_bind("tab: complete")
     readline.set_completion_display_matches_hook(DisplayMatches)

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