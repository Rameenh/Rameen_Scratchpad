import distutils.util
import io
import sys


def main():
    tasks = []  # the upper layer of our variable list
    loops = []
    taskExecOrder = []
    elementNamesForLoop = []
    taskNoForLoop = []
    currentLine = -1
    addingElementsToLoop = False
    buildingLoop = False
    taskVars = dict()  # the list of variables for the individual task
    taskNo = -2  # keeps track of the task number for indexing
    path = "script.WTF"
    f = open(path, "r")
    d = open(path, 'r')
    for line in f:
        currentLine = currentLine + 1
        if line == '\n':
            if taskVars:  # ensures task variable list isn't empty; prevents adding empty sub lists to main list
                tasks.append(dict(taskVars))
                taskVars.clear()  # empties out variable list for task since we're ready to move to the next set
            if addingElementsToLoop:  # detects if we're done with the element name block for the loop in script
                addingElementsToLoop = False  # we're done with the block so set the flag to false
            continue  # move forward one line
        elif '[' in line:  # if the line we're on is a task line
            taskNo = taskNo + 1  # increments the task number counter since we've moved to the next task
            if "Task" in line and not buildingLoop:
                taskExecOrder.append(taskNo)  # adding task number to the execution list
        else:  # above ensures we're not parsing a task header nor blank line
            x = (line.split('='))  # all other lines are variable assignment lines, no need to check for '='
            x0 = x[0].strip()  # remove trailing/leading spaces
            x1 = x[1].strip().replace('"', "")  # does above but also removes quotation marks
            taskVars[x0] = x1  # add the temporary variable pair to the task's variable list

            if "# of Tasks" in x0:
                numberOfTasks = x1

            if "Loop over elements" in x1:  # detects if we've encountered a loop builder task
                buildingLoop = True  # set a flag that we're building a loop for the script
                addingElementsToLoop = True  # set a flag that we're adding element names from script for loop

            if addingElementsToLoop and "Element" in x0:  # if we're on a line that adds an element name for the loop
                elementNamePre = x0.split(' ')  # split the left side of the variable assigner by space
                elementName = elementNamePre[1]  # retrieve the second word of the left side, that's the element name
                elementNamesForLoop.append(int(elementName))

            if "End loop" in x1:  # script will have "End loop" in right side of task type to end loop block
                buildingLoop = False  # set the building loop flag to false since the loop block is done
                loops.append(list([list(elementNamesForLoop), list(taskNoForLoop)]))
                elementNamesForLoop.clear()
                taskNoForLoop.clear()
                taskExecOrder.pop()

                for i in range(len(loops[len(loops) - 1][0])):
                    for j in range(len(loops[len(loops) - 1][1])):
                        taskExecOrder.append([loops[len(loops) - 1][1][j], i+1])

            if buildingLoop and not addingElementsToLoop:  # if we're building a loop & are not in the name adding phase
                if taskNo not in taskNoForLoop:  # ensure the task no. isn't already in the task list for the loop
                    taskNoForLoop.append(taskNo)  # add the current task no. to the list of tasks we need to run in loop

    if taskVars:  # ensures task variable list isn't empty; prevents adding empty sub lists to main list
        tasks.append(dict(taskVars))
        taskVars.clear()  # empties out variable list for task since we're ready to move to the next set

    for i in range(len(taskExecOrder)):
        if not isinstance(taskExecOrder[i], list):
            taskNoRemember = taskExecOrder[i]
            toReplace = [taskNoRemember, None]
            taskExecOrder[i] = toReplace

    taskNames = list()
    for i in range(len(taskExecOrder)):
        taskNames.append(tasks[taskExecOrder[i][0]+1]['Task type'])

    taskArgs = list()
    for i in range(len(taskExecOrder)):
        tasks[taskExecOrder[i][0] + 1].pop("Task type", None)
        taskArgs.append(tasks[taskExecOrder[i][0]+1])

    for i in range(len(taskNames)):
        name = taskNames[i]
        args = taskArgs[i]

        if not taskExecOrder[i][1] is None:  # if the element in the taskExecOrder isn't None
            args['Element'] = taskExecOrder[i][1]  # set the element to be operated on to the one in taskExecOrder

        if "Measure element efficiency (RFB)".upper() in name.upper():
            measure_element_efficieny_rfb(args)
        elif name.upper() == "Pre-test initialization".upper():
            pretest_initialization(args)
        elif "Find element n".upper() in name.upper():
            find_element(args)
        elif name.upper() == "Save results".upper():
            save_results(args)
        elif name.upper() == "Prompt user for action".upper():
            prompt_user_for_action(args)
        elif "Home system".upper() in name.upper():
            home_system(args)

def measure_element_efficieny_rfb(varlist):
    element = varlist['Element']
    freqRange = varlist['Frequency range']
    on_off_cycles = varlist['RFB.#on/off cycles']
    return


def pretest_initialization(varlist):
    return


def find_element(varlist):
    element = varlist['Element']
    xIncrMM = varlist['X Incr. (mm)']
    XPts = varlist['X #Pts.']
    thetaIncrDeg = varlist['Theta Incr. (deg)']
    thetaPts = varlist['Theta #Pts.']
    scopeChannel = varlist['Scope channel']
    AcquisitionType = varlist['Acquisition type']
    averages = varlist['Averages']
    dataStorage = varlist['Data storage']
    storageLocation = varlist['Storage location']
    dataDirectory = varlist["Data directory"]
    maxPosErrMM = varlist["Max. position error (+/- mm)"]
    elemPosTest = varlist["ElementPositionTest"]
    return


def save_results(varlist):
    saveSummaryFile = bool(distutils.util.strtobool(varlist["Save summary file"]))
    WriteUACalibration = bool(distutils.util.strtobool(varlist["Write UA Calibration"]))
    PromptForCalWrite = bool(distutils.util.strtobool(varlist["PromptForCalWrite"]))
    return


def prompt_user_for_action(varlist):
    promptType = varlist["Prompt type"]
    return


def home_system(varlist):
    axisToHome = varlist['Axis to home']
    return


def printList(list2):
    for x in range(len(list2)):
        print(list2[x])


def printList2(list2):
    print(str(list2)[1:-1])


main()
