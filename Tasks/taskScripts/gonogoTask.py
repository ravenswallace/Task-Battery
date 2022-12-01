import csv
import glob
import os
import pathlib
import random
import sys
import time
from collections import deque
import numpy as np
import numpy.random
import pygame
from psychopy import core, data, event, gui, logging, visual
from psychopy.misc import fromFile



def get_response(input_method: str, timeStamped, myClock):
    # if participants don't respond we will set up a null value so we don't get an error
    thisResp = None
    thisRT = np.nan
    for key, RT in event.getKeys(
        keyList=["escape", "q", "left", "right", "space"], timeStamped=timeStamped
    ):
        if key in ["escape", "q"]:
            if trig_collector:
                trig_collector.endCollection()
            # core.quit()
        else:
            thisResp = key
            thisRT = myClock.getTime()
   
        
    return thisResp, thisRT


def HelpWin(myClock, myWin, dfile):
    global trig_collector
    input_method = "keyboard"
    resp_device = None
    # let the script know if we are in the scanner or not (true/false)

    # Create dummy period (time needed for the scanner to collect 2 volumes)

    ################################## Define all variables experiment ######################################
    # collect participant info, create logfile
    info = {"Subject": "test", "Age": "", "Gender": ["male", "female", "other"]}
    myWin.flip()
    # if participants don't respond we will set up a null value so we don't get an error

    sans = [
        "Helvetica",
        "Gill Sans MT",
        "Arial",
        "Verdana",
    ]  # use the first font found on this list
    try:
        lines1 = pathlib.Path(f"{os.path.dirname(os.path.abspath(__file__))}//resources//GoNoGo_Task//GoNoGo_instr_1.txt").read_text()

        lines2 = pathlib.Path(f"{os.path.dirname(os.path.abspath(__file__))}//resources//GoNoGo_Task//GoNoGo_instr_2.txt").read_text()

        lines3 = pathlib.Path(f"{os.path.dirname(os.path.abspath(__file__))}//resources//GoNoGo_Task//GoNoGo_instr_3.txt").read_text()

    except:
        lines1 = pathlib.Path(f"{os.path.dirname(os.path.abspath(__file__))}taskScripts//resources//GoNoGo_Task//GoNoGo_instr_1.txt").read_text()

        lines2 = pathlib.Path(f"{os.path.dirname(os.path.abspath(__file__))}taskScripts//resources//GoNoGo_Task//GoNoGo_instr_2.txt").read_text()

        lines3 = pathlib.Path(f"{os.path.dirname(os.path.abspath(__file__))}taskScripts//resources//GoNoGo_Task//GoNoGo_instr_3.txt").read_text()

    instrTxt1 = visual.TextStim(myWin, text=lines1, color="black")
    instrTxt2 = visual.TextStim(myWin, text=lines2, color="black")
    instrTxt3 = visual.TextStim(myWin, text=lines3, color="black")
    try:
        instrimg = visual.ImageStim(myWin, image=f"{os.path.dirname(os.path.abspath(__file__))}//resources//GoNoGo_Task//Go.jpg", size=[2, 1])

    except:
        instrimg = visual.ImageStim(myWin, image=f"{os.path.dirname(os.path.abspath(__file__))}taskScripts//resources//GoNoGo_Task//Go.jpg", size=[2, 1])

    # Before each part of the task begins, you will be informed what type of stimuli you will have to attend to by a cue in red (WORD, PICTURE or BOX).\n\
    # \nPlease give equal importance to SPEED and ACCURACY when completing this task. We would like you to respond as FAST as possible while maintaining a high \
    # level of ACCURACY.\n\
    # \nIf you have any questions, please ask the researcher before we start.\n\
    # \nWhen you are ready to begin the task, please press the left button.
    readyTxt = visual.TextStim(
        myWin, text="The experiment will start shortly.", color="black"
    )
    finishTxt = visual.TextStim(myWin, text="End of Experiment!", color="black")
    ######### Set up constant variables outside of loop ############
    dataFile = open(dfile, "r")
    # read in csv file with conditions on
    # dataFile = open('resources/GoNoGo_Task/gonogo_stimuli.csv', 'r')
    reader = csv.reader(dataFile, delimiter=",")
    # read in first line of the csv file and assign this to the variable header
    header = dataFile.readline()
    # strip the header to remove \n from the end and split this line into as many entries as there are columns in the header file (i.e., into each of the columns headers)
    hdr = header.strip().split(";")
    lines = dataFile.readlines()  # assign all other information into the variable lines
    # create an empty list in which we can append items from the csv file into
    go_words = []
    nogo_words = []
    go_box = []
    nogo_box = []
    global go_img
    go_img = []
    global nogo_img
    nogo_img = []
    scrambled_word = []
    scrambled_pic = []
    for enum, line in enumerate(lines):  # read in row by row from csv file
        if line == "\n":
            continue
        data = line.strip().split(",")
        Block = data[0]
        Condition = data[1]
        if data[2] != "":
            item3 = data[2]
            go_box.append(item3)
            nogo_box.append(item3)
        if data[3] != "":
            try:
                item6 = f"{str(os.path.dirname(os.path.abspath(__file__)))}/resources/GoNoGo_Task/{data[3]}"

            except:
                item6 = f"{str(os.path.dirname(os.path.abspath(__file__)))}taskScripts/resources/GoNoGo_Task/{data[3]}"

            scrambled_word.append(item6)

    # Participant ID
    Part_ID = info["Subject"]
    _extracted_from_HelpWin_134(instrTxt1, myWin)
    _extracted_from_HelpWin_134(instrTxt2, myWin)
    _extracted_from_HelpWin_134(instrTxt3, myWin)
    _extracted_from_HelpWin_134(instrimg, myWin)
    myWin.flip()
    trig_collector = None
    # Start being ready to get triggers
    if trig_collector:
        trig_collector.start()
    # readyTxt.draw()
    # myWin.flip()
    # event.waitKeys(keyList=['return'])
    if trig_collector:
        trig_collector.waitForVolume(5)
    # else:
    # event.waitKeys(keyList=['return'])
    return scrambled_word, scrambled_pic, input_method, resp_device, Part_ID, sans


# TODO Rename this here and in `HelpWin`
def _extracted_from_HelpWin_134(arg0, myWin):
    # create a fixation cross

    arg0.draw()
    myWin.flip()
    event.waitKeys(keyList=["return"])


#
###BLOCK C. SCRAMBLED
def Block_C(
    thisrun,
    myClock,
    myWin,
    writer,
    resdict,
    scrambled_word,
    scrambled_pic,
    input_method,
    resp_device,
    Part_ID,
    sans,
    runtime,
):
    global go_words
    global nogo_words
    global go_box
    global nogo_box
    # List of numbers we can select from to determine number of consecutive go trials before a no go
    consecutive_gotrials = [1, 2, 3, 4, 5, 6]
    # length of jitter options in seconds for item and fixation
    jitter_item = [0.75, 1, 1.25]
    jitter_fixation = [0.5, 0.75, 1]
    # create a fixation cross
    fixation = visual.TextStim(myWin, text="+", color="black")
    scrambled_img = []
    # SPLIT THE MINIBLOCKS HERE
    if thisrun == 1:
        slants = ["h"]
    elif thisrun == 2:
        slants = ["h"]
    # Cue block 3
    # This will wait for 3 seconds
    # This will wait for 3 seconds
    for i in slants:
        diff = i
        if thisrun == 1 and diff == "e":
            cond = "scrambled words easy"
            for i in scrambled_word:
                scrambled_img.append(i)
        elif thisrun == 1 and diff == "h":
            cond = "scrambled pics hard"
            for i in scrambled_pic:
                scrambled_img.append(i)
        elif thisrun == 2 and diff == "e":
            cond = "scrambled pics easy"
            for i in scrambled_pic:
                scrambled_img.append(i)
        elif thisrun == 2 and diff == "h":
            cond = "scrambled words hard"
            for i in scrambled_word:
                scrambled_img.append(i)
        # Number of go trials in the block
        remaining_trials = 1
        # Keeping a track of how many trials we have completed
        random.shuffle(scrambled_img)
        if len(consecutive_gotrials) == 0:
            consecutive_gotrials = [1, 2, 3, 4, 5, 6]
        random_gotrials = np.random.choice(consecutive_gotrials, 1, replace=False)
        # As the above line returns a one-value list, we need to select that value so that we have an int to manipulate (this is important for the next line)
        number_gotrials = random_gotrials[0]
        # -I made this, trying to choose one of the three box conditions in the xlsx file at random, with replacement.
        gobox_item = np.random.choice(scrambled_img, number_gotrials, replace=True)
        nogobox_item = np.random.choice(scrambled_img, 1, replace=False)
        # Now we can go through the list line by line and call the stimuli in
        d = 0
        # Start Consecutive Go Trials
        tasktimer = core.MonotonicClock()
        while tasktimer.getTime() <= runtime:
            random_gotrials = np.random.choice(consecutive_gotrials, 1, replace=False)
            # As the above line returns a one-value list, we need to select that value so that we have an int to manipulate (this is important for the next line)
            number_gotrials = random_gotrials[0]
            # -I made this, trying to choose one of the three box conditions in the xlsx file at random, with replacement.
            gobox_item = np.random.choice(scrambled_img, number_gotrials, replace=True)
            nogobox_item = np.random.choice(scrambled_img, 1, replace=False)
            numoftrials = np.random.choice(consecutive_gotrials)
            for i in range(0, len(gobox_item)):
                if numoftrials != 0:
                    # Draw fixation cross
                    fixation.draw()
                    rand_jitter_fix = random.choice(jitter_fixation)
                    myWin.flip()
                    core.wait(rand_jitter_fix)
                    rt_clock = core.Clock()
                    # Prepare and draw each stimuli each iteration
                    go_stimulus = visual.ShapeStim(
                        myWin,
                        units="",
                        lineWidth=4,
                        lineColor="black",
                        lineColorSpace="rgb",
                        fillColor=None,
                        fillColorSpace="rgb",
                        vertices=((-0.41, 0.5), (0.59, 0.5), (0.5, -0.5), (-0.5, -0.5)),
                        closeShape=True,
                        pos=(-0.06, 0),
                        size=1,
                        ori=0.0,
                        opacity=1.0,
                        contrast=1.0,
                        depth=0,
                        interpolate=True,
                        name=None,
                        autoLog=None,
                        autoDraw=False,
                    )
                    go_stimulusv = visual.ImageStim(
                        myWin, size=0.44, image=gobox_item[i], pos=(0, 0)
                    )
                    durStim = random.choice(jitter_item)
                    contTrial = True
                    event.clearEvents()  # start each trial by clearing event buffer to prevent any previous keys interfering with the current trial
                    rt_clock.reset()
                    Onset = myClock.getTime()
                    resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = (
                        "Stimulus start",
                        myClock.getTime(),
                        "Type: Go",
                    )
                    writer.writerow(resdict)
                    (
                        resdict["Timepoint"],
                        resdict["Time"],
                        resdict["Auxillary Data"],
                        resdict["Is_correct"],
                    ) = (None, None, None, None)
                    while contTrial and rt_clock.getTime() < durStim:
                        go_stimulusv.draw()
                        go_stimulus.draw()
                        myWin.flip()  # IIIII
                        thisResp, thisRT = get_response(
                            input_method, resp_device, myClock, myClock
                        )
                        RT = 0
                        corrAns = "left"
                        isCorrect = "noResponse"
                        if thisResp is not None:
                            contTrial = False
                            RT = rt_clock.getTime()
                            isCorrect = int(thisResp == corrAns)
                            if isCorrect == 1:
                                isCorrect = True
                                # resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = "Stimulus end", myClock.getTime(), "Type: Go", isCorrect
                                # writer.writerow(resdict)
                                # resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = None, None,None, None
                            else:
                                isCorrect = False
                    while rt_clock.getTime() < durStim:
                        go_stimulusv.draw()
                        go_stimulus.draw()
                        myWin.flip()
                    # Write data into logfile
                    (
                        resdict["Timepoint"],
                        resdict["Time"],
                        resdict["Auxillary Data"],
                        resdict["Is_correct"],
                    ) = ("Stimulus end", myClock.getTime(), "Type: Go", isCorrect)
                    writer.writerow(resdict)
                    (
                        resdict["Timepoint"],
                        resdict["Time"],
                        resdict["Auxillary Data"],
                        resdict["Is_correct"],
                    ) = (None, None, None, None)
                    boxtype = "square"
                    itemid = gobox_item[i].split("\\")
                    itemname = itemid[-1][:-4]
                    # resdict['Timepoint'], resdict['Time'], resdict['Is_correct'] = 'Go_task_start', myClock.getTime(), isCorrect
                    # writer.writerow(resdict)
                    remaining_trials = remaining_trials - 1
                    numoftrials = numoftrials - 1
                    continue
                # Start No Go Trial
                # Draw fixation point
                fixation.draw()
                rand_jitter_fix = random.choice(jitter_fixation)
                myWin.flip()
                core.wait(rand_jitter_fix)
                rt_clock = core.Clock()
                # Prepare and draw the stimulus
                for line_nogo in nogobox_item:
                    if diff == "e":
                        nogo_stimulus = visual.ShapeStim(
                            myWin,
                            units="",
                            lineWidth=4,
                            lineColor="black",
                            lineColorSpace="rgb",
                            fillColor=None,
                            fillColorSpace="rgb",
                            vertices=(
                                (-0.22, 0.5),
                                (0.78, 0.5),
                                (0.5, -0.5),
                                (-0.5, -0.5),
                            ),
                            closeShape=True,
                            pos=(-0.12, 0),
                            size=1,
                            ori=0.0,
                            opacity=1.0,
                            contrast=1.0,
                            depth=0,
                            interpolate=True,
                            name=None,
                            autoLog=None,
                            autoDraw=False,
                        )
                    elif diff == "h":
                        nogo_stimulus = visual.ShapeStim(
                            myWin,
                            units="",
                            lineWidth=4,
                            lineColor="black",
                            lineColorSpace="rgb",
                            fillColor=None,
                            fillColorSpace="rgb",
                            vertices=(
                                (-0.31, 0.5),
                                (0.69, 0.5),
                                (0.5, -0.5),
                                (-0.5, -0.5),
                            ),
                            closeShape=True,
                            pos=(-0.09, 0),
                            size=1,
                            ori=0.0,
                            opacity=1.0,
                            contrast=1.0,
                            depth=0,
                            interpolate=True,
                            name=None,
                            autoLog=None,
                            autoDraw=False,
                        )
                    nogo_stimulusv = visual.ImageStim(
                        myWin, size=0.44, pos=(0, 0), image=nogobox_item[0]
                    )
                    durStim = random.choice(jitter_item)
                    contTrial = True
                    event.clearEvents()  # start each trial by clearing event buffer to prevent any previous keys interfering with the current trial
                    rt_clock.reset()
                    Onset = myClock.getTime()
                    resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = (
                        "Stimulus start",
                        myClock.getTime(),
                        "Type: NoGo",
                    )
                    writer.writerow(resdict)
                    resdict["Timepoint"], resdict["Time"], resdict["Auxillary Data"] = (
                        None,
                        None,
                        None,
                    )
                    while contTrial and rt_clock.getTime() < durStim:
                        nogo_stimulusv.draw()
                        nogo_stimulus.draw()
                        myWin.flip()
                        thisResp, thisRT = get_response(
                            input_method, resp_device, myClock, myClock
                        )
                        RT = 0
                        isCorrect = "noResponse"
                        if thisResp is not None:
                            contTrial = False
                            isCorrect = False
                            RT = rt_clock.getTime()
                            # resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = "Stimulus end", myClock.getTime(), "Type: NoGo",isCorrect
                            # writer.writerow(resdict)
                            # resdict['Timepoint'], resdict['Time'], resdict['Auxillary Data'], resdict['Is_correct'] = None, None,None, None
                        else:
                            isCorrect = True
                    while rt_clock.getTime() < durStim:
                        nogo_stimulusv.draw()
                        nogo_stimulus.draw()
                        myWin.flip()
                    # Write data into logfile
                    (
                        resdict["Timepoint"],
                        resdict["Time"],
                        resdict["Auxillary Data"],
                        resdict["Is_correct"],
                    ) = ("Stimulus end", myClock.getTime(), "Type: NoGo", isCorrect)
                    writer.writerow(resdict)
                    (
                        resdict["Timepoint"],
                        resdict["Time"],
                        resdict["Auxillary Data"],
                        resdict["Is_correct"],
                    ) = (None, None, None, None)
                    if diff == "e":
                        boxtype = "easy"
                    elif diff == "h":
                        boxtype = "hard"
                    itemid = nogobox_item[0].split("\\")
                    itemname = itemid[-1][:-4]
                    # resdict['Timepoint'], resdict['Time'], resdict['Is_correct'] = 'NoGo_task_start', myClock.getTime(), isCorrect
                    # writer.writerow(resdict)
                    remaining_trials = remaining_trials - 1
                    d = d + 1
                    numoftrials = np.random.choice(consecutive_gotrials)
                # This removes the items from the list that you have used (true sampling without replacement)
                consecutive_gotrials = [
                    x for x in consecutive_gotrials if x not in random_gotrials
                ]
        


def main(logloc: str, myClock, myWin, writer, resdict: dict, runtime, dfile):
    """
    This is a multi-line Google style docstring.

    Args:
        logloc (str): The location of the log file.
        myClock (core.Clock): The clock object.
        myWin (visual.Window): The window object.
        writer (csv.writer): The csv writer object.
        resdict (Dict): The dictionary object.
        runtime (int): The runtime of the experiment.
        dfile (str): The location of the data file.

    Returns:
        None
    """
    # instrTxt1, myWin, instrTxt2, readyTxt, sans, resp_device, Part_ID, f, input_method, nogo_words, go_words, scrambled_pic, scrambled_word, fmri_log, finishTxt = runexp(logloc, myWin)
    scrambled_word, scrambled_pic, input_method, resp_device, Part_ID, sans = HelpWin(
        myClock, myWin, dfile
    )
    resdict["Timepoint"], resdict["Time"] = "Go/NoGo Initialized", myClock.getTime()
    writer.writerow(resdict)
    thisrun = 2
    Block_C(
        thisrun,
        myClock,
        myWin,
        writer,
        resdict,
        scrambled_word,
        scrambled_pic,
        input_method,
        resp_device,
        Part_ID,
        sans,
        runtime,
    )
    # Block_B(thisrun)
    # Block_A(thisrun)
    resdict["Timepoint"], resdict["Time"] = "Go/NoGo Finished", myClock.getTime()
    writer.writerow(resdict)
    ############################################End Experiment###############################################################
    # If in fMRI mode, store the triggers
    if trig_collector:
        trig_collector.endCollection()
        v_t = trig_collector.getVolumeTimings(myClock)
        # Create a file which has the fMRI timings in
    myWin.flip()
    fin_time = myClock.getTime()


def runexp(logfilelocation, time, myWin, writer, resdict, runtime, dfile, seed):
    writer = writer[0]
    random.seed(a=seed)
    resdict["Timepoint"], resdict["Time"] = "gonogo START", time.getTime()
    writer.writerow(resdict)
    main(logfilelocation, time, myWin, writer, resdict, runtime, dfile)
