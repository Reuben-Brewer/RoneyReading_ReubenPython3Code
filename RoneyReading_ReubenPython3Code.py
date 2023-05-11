# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision D, 05/10/2023

Verified working on: Python Windows 10 64-bit.
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import platform
import time
import datetime
import threading
import traceback
from copy import deepcopy
import collections
import random
import keyboard #"sudo pip install keyboard" https://pypi.org/project/keyboard/, https://github.com/boppreh/keyboard
import json
#########################################################

#########################################################
#os.add_dll_directory(r'C:\VLC') #DIDN'T NEED TO DO THIS AFTER INSTALLING THE 64-BIT VERSION (vlc-3.0.17.4-win64.exe) TO C:\VLC
import vlc #pip install python-vlc
#########################################################

#########################################################
import gtts #pip3 install gTTS pyttsx3
#########################################################

#########################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
#########################################################

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

##########################################################################################################
##########################################################################################################
def LoadAndParseJSONfile_RoneyReadingParameters():
    global ParametersToBeLoaded_Directory_TO_BE_USED
    global ParametersToBeLoaded_RoneyReadingParameters_Dict

    #################################
    JSONfilepathFull_RoneyReadingParameters = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_RoneyReadingParameters.json"

    #def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):
    ParametersToBeLoaded_RoneyReadingParameters_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_RoneyReadingParameters, 1, 1)
    #################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0):

    try:
        #################################

        ##############
        with open(JSONfilepathFull) as ParametersToBeLoaded_JSONfileObject:
            ParametersToBeLoaded_JSONfileParsedIntoDict = json.load(ParametersToBeLoaded_JSONfileObject)

        ParametersToBeLoaded_JSONfileObject.close()
        ##############

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        ##############
        for key, value in ParametersToBeLoaded_JSONfileParsedIntoDict.items():
            if USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS == 1:
                if key.upper().find("_FLAG") != -1:
                    GlobalsDict[key] = PassThrough0and1values_ExitProgramOtherwise(key, value)
                else:
                    GlobalsDict[key] = value
            else:
                GlobalsDict[key] = value

            if PrintResultsFlag == 1:
                print(key + ": " + str(value))

        ##############
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        return ParametersToBeLoaded_JSONfileParsedIntoDict
        #################################
    except:
        #################################
        exceptions = sys.exc_info()[0]
        print("LoadAndParseJSONfile_AddDictKeysToGlobalsDict Error, Exceptions: %s" % exceptions)
        traceback.print_exc()
        return dict()
        #################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def PassThrough0and1values_ExitProgramOtherwise(InputNameString, InputNumber):

    try:
        InputNumber_ConvertedToFloat = float(InputNumber)
    except:
        exceptions = sys.exc_info()[0]
        print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber for variable_name '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()

    try:
        if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
            return InputNumber_ConvertedToFloat
        else:
            input("PassThrough0and1values_ExitProgramOtherwise Error. '" + InputNameString + "' must be 0 or 1 (value was " + str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")
            sys.exit()
    except:
        exceptions = sys.exc_info()[0]
        print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
        input("Press any key to continue")
        sys.exit()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def CreateNewDirectoryIfItDoesntExist(directory):
    try:
        if os.path.isdir(directory) == 0: #No directory with this name exists
            os.makedirs(directory)
    except:
        exceptions = sys.exc_info()[0]
        print("CreateNewDirectoryIfItDoesntExist, Exceptions: %s" % exceptions)
        traceback.print_exc()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def getTimeStampString():

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y---%H_%M_%S')

    return st
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def SortListAlphabetically(InputList):
    try:
        OutputList = sorted(InputList, key=lambda v: v.lower())
        return OutputList
    except:
        exceptions = sys.exc_info()[0]
        print("SortListAlphabetically, exceptions: %s" % exceptions)
        return list()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def RemoveDuplicatesFromList(InputList):
    try:
        OutputList = list(set(InputList))
        return OutputList
    except:
        exceptions = sys.exc_info()[0]
        print("RemoveDuplicatesFromList, exceptions: %s" % exceptions)
        return list()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def CreateDictOfReadingWords(FileToRead):

    #######################################
    #######################################
    #######################################
    try:
        AllLinesInFile_ListOfStrings = ""
        with open(FileToRead) as StatementFile:
            AllLinesInFile_ListOfStrings = StatementFile.readlines()
        StatementFile.close()

        #print("AllLinesInFile_ListOfStrings: Type: " + str(type(AllLinesInFile_ListOfStrings)) + ", Values: " + str(AllLinesInFile_ListOfStrings))

    except:
        exceptions = sys.exc_info()[0]
        print("CreateDictOfReadingWords, Step 0: opening file and reading all lines, Exceptions: %s" % exceptions)
        return dict()
        traceback.print_exc()
    #######################################
    #######################################
    #######################################

    #######################################
    #######################################
    #######################################
    try:

        DictOfWordsOrganizedByWordLength = dict()
        for index, LineString in enumerate(AllLinesInFile_ListOfStrings):
            #######################################
            #######################################
            LineString = LineString.strip()

            AllLinesInFile_ListOfStrings[index] = LineString

            if LineString.find("#") == -1: #Not a comment
                WordLengthInt = len(LineString)

                if WordLengthInt > 0:

                    #######################################
                    if WordLengthInt not in DictOfWordsOrganizedByWordLength:
                        #print("Adding '" + str(WordLengthInt) + "' as a key in DictOfWordsOrganizedByWordLength!")
                        DictOfWordsOrganizedByWordLength[WordLengthInt] = dict([("WordsList", list()), ("NumberOfWords", -1)])

                    DictOfWordsOrganizedByWordLength[WordLengthInt]["WordsList"].append(LineString)
                    #######################################

            #######################################
            #######################################

        #print("DictOfWordsOrganizedByWordLength: " + str(DictOfWordsOrganizedByWordLength))

    except:
        exceptions = sys.exc_info()[0]
        print("CreateDictOfReadingWords, Step 1: Creating DictOfWordsOrganizedByWordLength, Exceptions: %s" % exceptions)
        return dict()
        traceback.print_exc()
    #######################################
    #######################################
    #######################################

    #######################################
    #######################################
    #######################################
    try:

        for WordLengthInt in DictOfWordsOrganizedByWordLength:
            #######################################
            #######################################
            ListOfWordsWithoutDuplicates = RemoveDuplicatesFromList(DictOfWordsOrganizedByWordLength[WordLengthInt]["WordsList"])

            SortedListOfWordsWithoutDuplicates = SortListAlphabetically(ListOfWordsWithoutDuplicates)

            DictOfWordsOrganizedByWordLength[WordLengthInt]["WordsList"] = SortedListOfWordsWithoutDuplicates

            DictOfWordsOrganizedByWordLength[WordLengthInt]["NumberOfWords"] = len(DictOfWordsOrganizedByWordLength[WordLengthInt]["WordsList"])
            #######################################
            #######################################

        #print("DictOfWordsOrganizedByWordLength: " + str(DictOfWordsOrganizedByWordLength))

    except:
        exceptions = sys.exc_info()[0]
        print("CreateDictOfReadingWords, Step 2: Sorting and culling-duplicates of DictOfWordsOrganizedByWordLength, Exceptions: %s" % exceptions)
        return dict()
        traceback.print_exc()
    #######################################
    #######################################
    #######################################

    return [AllLinesInFile_ListOfStrings, DictOfWordsOrganizedByWordLength]

##########################################################################################################
##########################################################################################################

###########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global WordToDisplayFrame
    global TabStyle
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global WordToDisplay_LabelList
    global WordToDisplay
    global TkinterBGcolorToBeSet

    if EXIT_PROGRAM_FLAG == 0:
    #########################################################
    #########################################################

        root["bg"] = TkinterBGcolorToBeSet
        WordToDisplayFrame.configure(background=TkinterBGcolorToBeSet)
        TabStyle.configure('TNotebook.', background=TkinterBGcolorToBeSet, foreground=TkinterBGcolorToBeSet, bordercolor=TkinterBGcolorToBeSet)
        TabStyle.configure('TNotebook', background=TkinterBGcolorToBeSet,foreground=TkinterBGcolorToBeSet, bordercolor=TkinterBGcolorToBeSet)
        TabStyle.configure('.', background=TkinterBGcolorToBeSet,foreground=TkinterBGcolorToBeSet, bordercolor=TkinterBGcolorToBeSet)

        for Index, LabelObject in enumerate(WordToDisplay_LabelList):
            LabelObject["bg"] = TkinterBGcolorToBeSet
            if Index <= len(WordToDisplay) - 1:
                LabelObject["text"] = WordToDisplay[Index]
            else:
                LabelObject["text"] = " " #So that we don't get remnants from prior words

        root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    #########################################################
    #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback():
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global TabControlObject
    global Tab_MainControls
    global TabStyle

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    TabControlObject = ttk.Notebook(root)

    Tab_MainControls = ttk.Frame(TabControlObject)
    TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

    TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

    ############# #Set the tab header font
    TabStyle = ttk.Style()
    #TabStyle.theme_use('default')
    TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'), padx=0, pady=0)
    #############

    #################################################
    #################################################

    ###########################################################
    ###########################################################
    global WordToDisplayFrame
    WordToDisplayFrame = Frame(Tab_MainControls)
    WordToDisplayFrame.grid(row=0, column=0, padx=0, pady=0, rowspan=1, columnspan=1, sticky='w')
    ###########################################################
    ###########################################################

    ###########################################################
    ###########################################################
    global WordToDisplay_LabelList
    WordToDisplay_LabelList = list()

    for Index in range(0, 8):
        WordToDisplay_LabelList.append(Label(WordToDisplayFrame, text=" ", font=("Helvetica", 275))) #, width=1
        WordToDisplay_LabelList[Index].bind("<Button-1>", lambda event, LetterIndexIntoWordString=Index: WordToDisplay_LabelList_ClickResponseFunction(event, LetterIndexIntoWordString))
        WordToDisplay_LabelList[Index].grid(row=0, column=Index, padx=0, pady=0, columnspan=1, rowspan=1)
    ###########################################################
    ###########################################################
    
    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    #################################################
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("RoneyReading_ReubenPython3Code")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################
    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def WordToDisplay_LabelList_ClickResponseFunction(event, LetterIndexIntoWordString):
    global WordToDisplay
    global AllCorrectWordsList
    global NextWordsNeedsToBeShownFlag

    if LetterIndexIntoWordString <= len(WordToDisplay) - 1:
        SaySound_VLC(WordToDisplay[LetterIndexIntoWordString])

    print("WordToDisplay_LabelList_ClickResponseFunction event fired for WordToDisplay = " + WordToDisplay + "Index = " + str(LetterIndexIntoWordString))

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def KeyPressResponse_Correct(event):
    global WordToDisplay
    global AllCorrectWordsList
    global NextWordsNeedsToBeShownFlag

    AllCorrectWordsList.append(WordToDisplay)
    NextWordsNeedsToBeShownFlag = 1

    print("The word '" + str(WordToDisplay) + "' was CORRECTLY identified.")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def KeyPressResponse_Incorrect(event):
    global WordToDisplay
    global AllIncorrectWordsList
    global NextWordsNeedsToBeShownFlag

    AllIncorrectWordsList.append(WordToDisplay)
    NextWordsNeedsToBeShownFlag = 1

    print("The word '" + str(WordToDisplay) + "' was INCORRECTLY identified.")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def KeyPressResponse_Skip(event):
    global NextWordsNeedsToBeShownFlag

    NextWordsNeedsToBeShownFlag = 1

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def KeyPressResponse_SayWord(event):
    global WordToDisplay

    SayWord_GoogleTextToSpeech(WordToDisplay)

    #print("KeyPressResponse_SayWord event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def KeyPressResponse_SayAllLetters(event):
    global WordToDisplay

    for Letter in WordToDisplay:
        SaySound_VLC(Letter)

    #print("KeyPressResponse_SayAllLetters event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def SaySound_VLC(Letter):
    global WordToDisplay
    global LetterSounds_FileDirectory
    global TimeIntoMP3fileToStartMillisecondsInt
    global DurationOfMP3fileToPlaySecondsFloat

    LetterMP3filepathFull = LetterSounds_FileDirectory + "\\" + Letter + ".mp3"
    #print("LetterMP3filepathFull: " + LetterMP3filepathFull)
    LetterMP3Object = vlc.MediaPlayer(LetterMP3filepathFull)

    LetterMP3Object.play()
    LetterMP3Object.set_time(TimeIntoMP3fileToStartMillisecondsInt) #ms
    time.sleep(DurationOfMP3fileToPlaySecondsFloat)
    LetterMP3Object.stop()

    #print("SaySound_VLC event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def SayWord_GoogleTextToSpeech(StringToSay):
    global GoogleTextToSpeechMP3filesDirectory

    tts = gtts.gTTS(StringToSay)  # make request to google to get synthesis

    WordFileNameFullPath = GoogleTextToSpeechMP3filesDirectory + "\\" + StringToSay + ".mp3"
    #print("SayWord_GoogleTextToSpeech, WordFileNameFullPath: " + str(WordFileNameFullPath))

    tts.save(WordFileNameFullPath)  # save the audio file

    WordMP3Object = vlc.MediaPlayer(WordFileNameFullPath)

    WordMP3Object.play()

    #playsound(WordFileNameFullPath)  # play the audio file

    #print("SayWord_GoogleTextToSpeech event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ########################################################################################################## unicorn

    ####################################################
    ####################################################
    random.seed()
    ####################################################
    ####################################################

    ####################################################
    ####################################################
    global ParametersToBeLoaded_Directory_TO_BE_USED
    ParametersToBeLoaded_Directory_TO_BE_USED = os.getcwd() + "//ParametersToBeLoaded"

    global ResultsOutputFileDirectory
    ResultsOutputFileDirectory = os.getcwd() + "\\Results"

    global LetterSounds_FileDirectory
    LetterSounds_FileDirectory = os.getcwd() + "\\LetterSounds\\"

    global GoogleTextToSpeechMP3filesDirectory
    GoogleTextToSpeechMP3filesDirectory = os.getcwd() + "\\GoogleTextToSpeechMP3files\\"

    CreateNewDirectoryIfItDoesntExist(ResultsOutputFileDirectory)
    CreateNewDirectoryIfItDoesntExist(LetterSounds_FileDirectory)
    CreateNewDirectoryIfItDoesntExist(GoogleTextToSpeechMP3filesDirectory)
    ####################################################
    ####################################################

    ####################################################
    ####################################################
    global InputFileName
    global NumberOfMinutesToTestFor
    global USE_IMPORTED_WORDS_LIST_RAW_FLAG
    global RandomizeFlag
    global DisplayOnlyWordsOfThisLengthList

    LoadAndParseJSONfile_RoneyReadingParameters()
    ####################################################
    ####################################################

    global InputFileDirectory
    InputFileDirectory = os.getcwd() + "\\WordLists"

    global InputFileNameFullPath
    InputFileNameFullPath = InputFileDirectory + "\\" + InputFileName
    print("InputFileNameFullPath: " + str(InputFileNameFullPath))

    global TimeIntoMP3fileToStartMillisecondsInt
    TimeIntoMP3fileToStartMillisecondsInt = 250

    global DurationOfMP3fileToPlaySecondsFloat
    DurationOfMP3fileToPlaySecondsFloat = 1.25

    global TkinterBGcolorToBeSet
    TkinterBGcolorToBeSet = '#%02x%02x%02x' % (240, 240, 240)  # RGB

    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global EndingTime_MainLoopThread
    EndingTime_MainLoopThread = -11111.0

    global LoopCounter_MainLoopThread
    LoopCounter_MainLoopThread = 0

    global root

    global root_Xpos
    root_Xpos = 0

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920

    global root_height
    root_height = 1080

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30

    global TabControlObject
    global Tab_MainControls

    global AllLinesInFile_ListOfStrings_RAW_IMPORT
    AllLinesInFile_ListOfStrings_RAW_IMPORT = list()

    global DictOfWordsOrganizedByWordLength
    DictOfWordsOrganizedByWordLength = dict()

    global WordToDisplay
    WordToDisplay = ""

    global AllWordsToDisplayList
    AllWordsToDisplayList = list()

    global AllCorrectWordsList
    AllCorrectWordsList = list()

    global AllIncorrectWordsList
    AllIncorrectWordsList = list()

    global NextWordsNeedsToBeShownFlag
    NextWordsNeedsToBeShownFlag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    print("Starting GUI thread...")
    GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
    GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
    GUI_Thread_ThreadingObject.start()
    time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    [AllLinesInFile_ListOfStrings_RAW_IMPORT, DictOfWordsOrganizedByWordLength] = CreateDictOfReadingWords(InputFileNameFullPath)
    print("AllLinesInFile_ListOfStrings_RAW_IMPORT: " + str(AllLinesInFile_ListOfStrings_RAW_IMPORT))
    print("DictOfWordsOrganizedByWordLength: " + str(DictOfWordsOrganizedByWordLength))

    ##########################################################################################################
    '''
    for WordLengthInt in DictOfWordsOrganizedByWordLength:
        print("DictOfWordsOrganizedByWordLength WordLengthInt = " + str(WordLengthInt) +
              " NumberOfWords = " + str(DictOfWordsOrganizedByWordLength[WordLengthInt]["NumberOfWords"]) +
              ", WordsList = " + str(DictOfWordsOrganizedByWordLength[WordLengthInt]["WordsList"]) + ".")
    '''
    ##########################################################################################################

    ##########################################################################################################
    if USE_IMPORTED_WORDS_LIST_RAW_FLAG == 0:
        AllWordsToDisplayList = list()
        for WordLengthInt in DisplayOnlyWordsOfThisLengthList:
            if WordLengthInt in DictOfWordsOrganizedByWordLength:
                AllWordsToDisplayList = AllWordsToDisplayList + DictOfWordsOrganizedByWordLength[WordLengthInt]["WordsList"]

        print("AllWordsToDisplayList: " + str(AllWordsToDisplayList))

    else:
        AllWordsToDisplayList = list(AllLinesInFile_ListOfStrings_RAW_IMPORT)
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    keyboard.on_release_key("y", KeyPressResponse_Correct)
    keyboard.on_release_key("n", KeyPressResponse_Incorrect)
    keyboard.on_release_key("s", KeyPressResponse_Skip)
    keyboard.on_release_key("h", KeyPressResponse_SayAllLetters) #h is for help
    keyboard.on_release_key("g", KeyPressResponse_SayWord) #g is for give-up

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    print("Starting main loop 'test_program_for_ProgramOfTimeScheduledEvents_ReubenPython2and3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread

        ##########################################################################################################
        if RandomizeFlag == 1:
            IntegerIndex = random.randint(0, len(AllWordsToDisplayList) - 1)
        else:
            IntegerIndex = LoopCounter_MainLoopThread
        ##########################################################################################################

        if IntegerIndex < len(AllWordsToDisplayList) - 1:
            WordToDisplay = AllWordsToDisplayList[IntegerIndex]
        else:
            LoopCounter_MainLoopThread = 0 #Start over
        #print(WordToDisplay)

        ##########################################################################################################
        while NextWordsNeedsToBeShownFlag == 0 and EXIT_PROGRAM_FLAG == 0:
            CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
            if CurrentTime_MainLoopThread >= NumberOfMinutesToTestFor*60.0:
                print("TIMES UP!")
                EXIT_PROGRAM_FLAG = 1

            time.sleep(0.1)
        ##########################################################################################################

        ##########################################################################################################
        ColorIntensityMin = 155
        ColorIntensityMax = 255
        TkinterBGcolorToBeSet = '#%02x%02x%02x' % (random.randint(ColorIntensityMin, ColorIntensityMax), random.randint(ColorIntensityMin, ColorIntensityMax), random.randint(ColorIntensityMin, ColorIntensityMax))  # RGB
        ##########################################################################################################

        NextWordsNeedsToBeShownFlag = 0
        LoopCounter_MainLoopThread = LoopCounter_MainLoopThread + 1
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ################################################# THIS IS THE EXIT ROUTINE!
    #################################################
    print("Exiting main program 'test_program_for_ProgramOfTimeScheduledEvents_ReubenPython2and3Class.")
    #################################################
    #################################################

    #################################################
    #################################################
    EndingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    NumberOfWordsAttempted = len(AllCorrectWordsList) + len(AllIncorrectWordsList)

    if NumberOfWordsAttempted > 0:
        ProgramCompletionPercentage = 100.0*NumberOfWordsAttempted/len(AllWordsToDisplayList)
        ProgramDurationMinutes = (EndingTime_MainLoopThread - StartingTime_MainLoopThread)/60.0

        CorrectPercentage = 100.0*len(AllCorrectWordsList)/NumberOfWordsAttempted
        IncorrectPercentage = 100.0*len(AllIncorrectWordsList)/NumberOfWordsAttempted

        print("ProgramCompletionPercentage: " + str(ProgramCompletionPercentage) + "(examined " + str(NumberOfWordsAttempted) + " out of " + str(len(AllWordsToDisplayList)) + " words)")
        print("ProgramDurationMinutes: " + str(ProgramDurationMinutes))
        print("CorrectPercentage: " + str(CorrectPercentage) + ", IncorrectPercentage: " + str(IncorrectPercentage))
        print("AllIncorrectWordsList: " + str(AllIncorrectWordsList))

        ################# save
        with open(ResultsOutputFileDirectory + "\\IncorrectWords_" + str(getTimeStampString()) + ".txt", "a") as TxtFileToWriteTo: #Will append to file if it exists, create new file with this as first entry if file doesn't exist.
            for IncorrectWord in AllIncorrectWordsList:
                TxtFileToWriteTo.write(IncorrectWord + "\n")
        #################

    #################################################
    #################################################


##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################