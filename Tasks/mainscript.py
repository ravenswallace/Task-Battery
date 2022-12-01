import csv
import os
import pickle as pkl
import random
import time
import psychopy
import taskScripts
from numpy import full
from psychopy import core, event, gui, visual

# Main script written by Ian Goodall-Halliwell. Subscripts are individually credited. Many have been extensively modified, for better or for worse (probably for worse o__o ).
# from Tasks.taskScripts import memoryTask
os.chdir(os.path.dirname(os.path.realpath(__file__)))
if not os.path.exists(os.path.join(os.getcwd(), "log_file")):
    os.mkdir(os.path.join(os.getcwd(), "log_file"))
# This class is responsible for creating and holding the information about how each task should run.
# It contains the number of repetitions and a global runtime variable.
# It also contains the subject ID, and will eventually use the experiment seed to randomize trial order.
class metadatacollection:
    def __init__(self, INFO: str, main_log_location: str):
        """
        This is a multi-line Google style docstring.
        Args:
            INFO (str): This is a string.
        Returns:
            None
        Raises:
            None
        """
        self.INFO = INFO
        self.main_log_location = main_log_location
        # Don't really know what this is, best to leave it be probably
        self.sbINFO = "Test"

    # This opens the GUI
    def rungui(self):
        self.sbINFO = gui.DlgFromDict(self.INFO)

    # This writes info collected from the GUI into the logfile
    def collect_metadata(self: object) -> None:
        """
        This function is used to collect metadata.
        """
        print(self.sbINFO.data)
        if os.path.exists(os.path.join(os.getcwd() + self.sbINFO.data[1])):
            os.remove(os.path.join(os.getcwd() + self.sbINFO.data[1]))
        if not os.path.exists(os.path.join(os.getcwd(), "log_file")):
            os.mkdir(os.path.join(os.getcwd(), "log_file"))
        with open(
            os.path.join(
                f"{os.getcwd()}/log_file/output_log_{self.sbINFO.data[1]}_{self.INFO['Experiment Seed']}_full.csv"
            ),
            "w",
            newline="",
        ) as f:
            fq = self._extracted_from_collect_metadata_8(f)
        fq.close()

    # TODO Rename this here and in `collect_metadata`
    def _extracted_from_collect_metadata_8(self, f: str) -> str:  # type: ignore
        """
        This is a multi-line Google style docstring.
        """
        result = open(
            os.path.join(
                f"{os.getcwd()}/log_file/output_log_{self.sbINFO.data[1]}_{self.INFO['Experiment Seed']}.csv"
            ),
            "w",
            newline="",
        )
        metawriter = csv.writer(f)
        metawriter2 = csv.writer(result)
        self._extracted_from_collect_metadata_11(metawriter)
        self._extracted_from_collect_metadata_11(metawriter2)
        random.seed(a=int(metacoll.INFO["Experiment Seed"]))
        metawriter.writerow(["Time after setup", taskbattery.time.getTime()])
        metawriter2.writerow(["Time after setup", taskbattery.time.getTime()])
        writer = csv.DictWriter(f, fieldnames=taskbattery.resultdict)
        writer.writeheader()
        writer2 = csv.DictWriter(result, fieldnames=taskbattery.resultdict)
        writer2.writeheader()
        return result

    # TODO Rename this here and in `collect_metadata`
    def _extracted_from_collect_metadata_11(self, arg0: csv.writer) -> None:
        arg0.writerow(["METADATA:"])
        arg0.writerow(self.sbINFO.inputFieldNames)
        arg0.writerow(self.sbINFO.data)


# Creates a list of all the tasks, and allows you to iterate through them without closing the window
class taskbattery(metadatacollection):
    time = core.Clock()
    resultdict = {
        "Timepoint": None,
        "Time": None,
        "Is_correct": None,
        "Experience Sampling Question": None,
        "Experience Sampling Response": None,
        "Task": None,
        "Task Iteration": None,
        "Participant ID": None,
        "Response_Key": None,
        "Auxillary Data": None,
        "Assoc Task": None,
    }
    # self.win = visual.Window(size=(1280, 800),color='white', winType='pyglet',fullscr=True)
    def __init__(self, tasklist: list, ESQtask: str, INFO: dict) -> None:
        self.tasklist = tasklist
        taskbattery.ESQtask = ESQtask
        self.INFO = INFO
        self.taskexeclist = []
        self.win = visual.Window(
            size=(1440, 960), color="white", winType="pyglet", fullscr=True
        )
        self.text = text_2 = visual.TextStim(
            win=self.win,
            name="text_2",
            text="Welcome to our experiment. \n Please follow the instructions on-screen and notify the attending researcher if anything is unclear \n We are thankful for your participation. \n Press <return/enter> to continue.",
            font="Arial",
            anchorHoriz="center",
            anchorVert="center",
            wrapWidth=None,
            ori=0,
            color="black",
            colorSpace="rgb",
            opacity=1,
            languageStyle="LTR",
            depth=0.0,
        )
        taskbattery.win = self.win

    def run_battery(self):
        """
        This function runs the battery of tasks.

        Args:
            self: The object itself.

        Returns:
            None
        """
        self.text.draw(self.win)
        self.win.flip()
        time.sleep(1)
        event.waitKeys(keyList=["return"])
        self.win.flip()
        for en, i in enumerate(self.tasklist):
            os.chdir(os.getcwd())
            i.show()
            i.run()
            pp = len(self.tasklist)
            if en < len(self.tasklist):
                i.end()


# OPEN THE TRIAL FILES AND CUT THEM INTO BLOCKS
# This creates a class which feeds all the necessary information into the task functions imported from each task file
# Allows you to create different task instances, which will be useful for creating blocks (my current project)
# Saves the log file after each task. It takes some extra time, but it prevents a crash from corrupting the file
class task(taskbattery, metadatacollection):
    def __init__(
        self,
        task_module,
        main_log_location,
        backup_log_location,
        name,
        trialclass,
        runtime,
        dfile,
        ver,
        esq=False,
    ):
        """
        Initialize the task object.

        Args:
            task_module: The imported task function.
            main_log_location: The location of the main log file.
            backup_log_location: The location of the backup log file.
            name: A name for each task to be written in the logfile.
            trialclass: Has something to do with writing task name into the logfile I think? Probably don't touch this.
            runtime: A "universal" "maximum" time each task can take. Will not stop mid trial, but will prevent trial repetions after the set time in seconds.
            dfile: The location of the data file.
            ver: The version of the task.
            esq: The esq flag.
        """
        self.main_log_location = main_log_location  # The location of the main log file
        self.backup_log_location = (
            backup_log_location  # The location of the backup log file
        )
        self.task_module = task_module  # The imported task function.
        self.name = name  # A name for each task to be written in the logfile.
        self.trialclass = trialclass  # Has something to do with writing task name into the logfile I think? Probably don't touch this.
        self.runtime = runtime  # A "universal" "maximum" time each task can take. Will not stop mid trial, but will prevent trial repetions after the set time in seconds.
        self.esq = esq  # The esq flag.
        self.ver = ver  # The version of the task.
        self.dfile = dfile  # The location of the data file.

    def initvers(self):
        os.chdir(os.getcwd())
        try:
            f = open(os.path.join(os.getcwd(), self.dfile), "r", newline="")
        except Exception:
            try:
                f = open(
                    os.path.join(os.path.join(os.getcwd(), "taskScripts"), self.dfile),
                    "r",
                    newline="",
                )
            except Exception:
                f = open(os.path.join(os.getcwd(), self.dfile), "r", newline="")
        d_reader = csv.DictReader(f)
        # get fieldnames from DictReader object and store in list
        self.headers = d_reader.fieldnames
        r = csv.reader(f)
        l = list(r)
        self.l = l
        incrordecr = random.choice([-1, 1])
        amnt = random.randint(5, 15)
        self.runtime = self.runtime + amnt * incrordecr
        with open(self.main_log_location, "a", newline="") as o:
            metawrite = csv.writer(o)
            metawrite.writerow(" ")
            metawrite.writerow(["Runtime Mod", (amnt * incrordecr)])

    def setver(self):
        ###
        ###   ###   NEED TO LOAD THE FILES FROM CSV AND PRESERVE THE HEADERS, THEN PUT THE OLD HEADERS INTO THE NEW BLOCK CSVs
        ###
        self.ver_a = random.sample(self.l, round(len(self.l) / 2))
        b = self.l
        for val in self.ver_a:
            b[:] = [x for x in b if x != val]
        random.shuffle(b)
        b.insert(0, *[self.headers])
        self.ver_b = b
        random.shuffle(self.ver_a)
        self.ver_a.insert(0, self.headers)
        lis = [self.ver_a, self.ver_b]
        for enum, thing in enumerate(lis):
            if not os.path.exists(f"{os.getcwd()}//tmp"):
                os.mkdir(f"{os.getcwd()}//tmp")
            if not os.path.exists(f"{os.getcwd()}//tmp//{self.name}"):
                os.mkdir(f"{os.getcwd()}//tmp//{self.name}")
            if os.path.exists(
                f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_{str(enum)}.csv"
            ):
                os.remove(
                    f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_{str(enum)}.csv"
                )
            with open(
                f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_{str(enum)}.csv",
                mode="w",
                newline="",
            ) as file:
                file_writer = csv.writer(
                    file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                for subthing in thing:
                    file_writer.writerow(subthing)
        self._ver_a_name = f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_0.csv"
        self._ver_b_name = f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_1.csv"

    def setver3(self):
        ###
        ###   ###   NEED TO LOAD THE FILES FROM CSV AND PRESERVE THE HEADERS, THEN PUT THE OLD HEADERS INTO THE NEW BLOCK CSVs
        ###
        self.ver_a = random.sample(self.l, round(len(self.l) / 3))
        b = self.l
        for val in self.ver_a:
            b[:] = [x for x in b if x != val]
        random.shuffle(b)
        self.ver_b = random.sample(b, round(len(b) / 2))
        c = b
        for val in self.ver_a:
            c[:] = [x for x in c if x != val]
        random.shuffle(c)
        c.insert(0, *[self.headers])
        self.ver_c = c
        random.shuffle(self.ver_a)
        random.shuffle(self.ver_b)
        self.ver_a.insert(0, self.headers)
        self.ver_b.insert(0, self.headers)
        lis = [self.ver_a, self.ver_b, self.ver_c]
        for enum, thing in enumerate(lis):
            if not os.path.exists(f"{os.getcwd()}//tmp"):
                os.mkdir(f"{os.getcwd()}//tmp")
            if not os.path.exists(f"{os.getcwd()}//tmp//{self.name}"):
                os.mkdir(f"{os.getcwd()}//tmp//{self.name}")
            if os.path.exists(
                f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_{str(enum)}.csv"
            ):
                os.remove(
                    f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_{str(enum)}.csv"
                )
            with open(
                f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_{str(enum)}.csv",
                mode="w",
                newline="",
            ) as file:
                file_writer = csv.writer(
                    file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                for subthing in thing:
                    file_writer.writerow(subthing)
        self._ver_a_name = f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_0.csv"
        self._ver_b_name = f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_1.csv"
        self._ver_c_name = f"{os.getcwd()}//tmp//{self.name}//{self.name}_version_2.csv"
        self._ver_d_name = None

    def run(self):
        global prevname
        if (
            not os.path.exists(self.main_log_location)
            and self.main_log_location.split(".")[1] is None
        ):
            os.mkdir(self.main_log_location.split("/")[0])
        with open(self.main_log_location, "a", newline="") as fr:
            with open(
                (self.main_log_location.split(".")[0] + "_full.csv"), "a", newline=""
            ) as f:
                fre = csv.writer(fr)
                r = csv.writer(f)
                writer = self._extracted_from_run_12(f, r)
                writer2 = self._extracted_from_run_12(fr, fre)
                taskbattery.resultdict = {
                    "Timepoint": None,
                    "Time": None,
                    "Is_correct": None,
                    "Experience Sampling Question": None,
                    "Experience Sampling Response": None,
                    "Task": self.name,
                    "Task Iteration": "1",
                    "Participant ID": self.trialclass[1],
                    "Response_Key": None,
                    "Auxillary Data": None,
                    "Assoc Task": None,
                }
                if self.esq == False:
                    if self.ver == 1:
                        dataver = self.task_module.runexp(
                            self.backup_log_location,
                            taskbattery.time,
                            taskbattery.win,
                            [writer, writer2],
                            taskbattery.resultdict,
                            self.runtime,
                            self._ver_a_name,
                            int(metacoll.INFO["Experiment Seed"]),
                        )
                    if self.ver == 2:
                        dataver = self.task_module.runexp(
                            self.backup_log_location,
                            taskbattery.time,
                            taskbattery.win,
                            [writer, writer2],
                            taskbattery.resultdict,
                            self.runtime,
                            self._ver_b_name,
                            int(metacoll.INFO["Experiment Seed"]),
                        )
                    if self.ver == 3:
                        dataver = self.task_module.runexp(
                            self.backup_log_location,
                            taskbattery.time,
                            taskbattery.win,
                            [writer, writer2],
                            taskbattery.resultdict,
                            self.runtime,
                            self._ver_c_name,
                            int(metacoll.INFO["Experiment Seed"]),
                        )
                    if self.ver == 4:
                        dataver = self.task_module.runexp(
                            self.backup_log_location,
                            taskbattery.time,
                            taskbattery.win,
                            [writer, writer2],
                            taskbattery.resultdict,
                            self.runtime,
                            self._ver_d_name,
                            int(metacoll.INFO["Experiment Seed"]),
                        )
                if self.esq == True:
                    taskbattery.resultdict = {
                        "Timepoint": None,
                        "Time": None,
                        "Is_correct": None,
                        "Experience Sampling Question": None,
                        "Experience Sampling Response": None,
                        "Task": self.name,
                        "Task Iteration": "1",
                        "Participant ID": self.trialclass[1],
                        "Response_Key": None,
                        "Auxillary Data": None,
                        "Assoc Task": taskbattery.prevname,
                    }
                    self.task_module.runexp(
                        self.backup_log_location,
                        taskbattery.time,
                        taskbattery.win,
                        [writer, writer2],
                        taskbattery.resultdict,
                        self.runtime,
                        None,
                        int(metacoll.INFO["Experiment Seed"]),
                    )
                    dataver = None
        taskbattery.resultdict = {
            "Timepoint": None,
            "Time": None,
            "Is_correct": None,
            "Experience Sampling Question": None,
            "Experience Sampling Response": None,
            "Task": None,
            "Task Iteration": None,
            "Participant ID": None,
            "Response_Key": None,
            "Auxillary Data": None,
            "Assoc Task": None,
        }
        if dataver != None:
            self.name = f"{self.name}-{dataver}"
        taskbattery.prevname = self.name

    # TODO Rename this here and in `run`
    def _extracted_from_run_12(self, arg0, arg1):
        result = csv.DictWriter(arg0, fieldnames=taskbattery.resultdict)
        arg1.writerow(["EXPERIMENT DATA:", self.name])
        arg1.writerow(["Start Time", taskbattery.time.getTime()])
        return result


class taskgroup(taskbattery, metadatacollection):
    def __init__(self, tasks, instrpath):
        self.tasks = tasks
        self.instrpath = instrpath

    def show(self):
        text_inst = visual.TextStim(
            win=taskbattery.win,
            name="text_4",
            text="",
            font="Open Sans",
            pos=(0, 0),
            height=0.1,
            wrapWidth=None,
            ori=0.0,
            color="black",
            colorSpace="rgb",
            opacity=None,
            languageStyle="LTR",
            depth=0.0,
        )
        try:
            with open(
                os.path.join(os.path.join(os.getcwd(), "taskScripts"), self.instrpath),
                newline="",
            ) as f:
                lines1 = f.read()
        except Exception:
            with open(os.path.join(os.getcwd(), self.instrpath), newline="") as f:
                lines1 = f.read()
        text_inst.setText(lines1)
        text_inst.draw()
        taskbattery.win.flip()
        time.sleep(1)
        event.waitKeys(keyList=["return"])

    def run(self):
        for taskgrp in self.tasks:
            for task in taskgrp:
                print(f"Now initializing {task.name}")
                task.initvers()
                print(f"Now setting up {task.name}")
                task.setver3()
                print(f"Now running {task.name}")
                task.run()
                print(f"Now starting ESQ for {task.name}")
                taskbattery.ESQtask.run()

    def end(self):
        text_inst = visual.TextStim(
            win=taskbattery.win,
            name="text_1",
            text="This is the end of this phase of the experiment. \n Please take a break if you need to before continuing with the study",
            font="Open Sans",
            pos=(0, 0),
            height=0.1,
            wrapWidth=None,
            ori=0.0,
            color="black",
            colorSpace="rgb",
            opacity=None,
            languageStyle="LTR",
            depth=0.0,
        )
        text_inst.draw()
        taskbattery.win.flip()
        time.sleep(1)
        event.waitKeys(keyList=["return"])
        taskbattery.win.flip()

    def shuffle(self):
        a = self.tasks
        for a in self.tasks:
            random.shuffle(a)
        random.shuffle(self.tasks)
        print("")


### HAVE TO EXPOSE ESQ TASK TO MOVIE SCRIPT
if __name__ == "__main__":
    # Info Dict
    INFO = {
        "Experiment Seed": random.randint(1, 9999999),
        "Subject": "Enter Name Here",
    }
    # Main and backup data file
    # Run the GUI and save output to logfile
    metacoll = metadatacollection(INFO)
    metacoll.rungui()
    metacoll.collect_metadata()
    metacoll.INFO["Block Runtime"] = 75
    # Defining output datafile
    datafile = str(
        f"{os.getcwd()}/log_file/output_log_{metacoll.INFO['Subject']}_{metacoll.INFO['Experiment Seed']}.csv"
    )
    datafileBackup = "log_file/testfullbackup.csv"
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    # with open("tmp/esqtmp.pkl",'wb') as frrr:
    #         pkl.dump([datafile,datafileBackup,metacoll.sbINFO.data,int(metacoll.INFO['Block Runtime'])],frrr)
    ESQTask = task(
        taskScripts.ESQ,
        datafile,
        datafileBackup,
        "Experience Sampling Questions",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        1,
        esq=True,
    )
    # Defining each task as a task object
    friendTask = task(
        taskScripts.otherTask,
        datafile,
        datafileBackup,
        "Friend Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Other_Task/Other_Stimuli.csv",
        1,
    )
    youTask = task(
        taskScripts.selfTask,
        datafile,
        datafileBackup,
        "You Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Self_Task/Self_Stimuli.csv",
        1,
    )
    gonogoTask = task(
        taskScripts.gonogoTask,
        datafile,
        datafileBackup,
        "GoNoGo Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        1,
    )
    fingertapTask = task(
        taskScripts.fingertappingTask,
        datafile,
        datafileBackup,
        "Finger Tapping Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        1,
    )
    readingTask = task(
        taskScripts.readingTask,
        datafile,
        datafileBackup,
        "Reading Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Reading_Task/sem_stim_run.csv",
        1,
    )
    memTask = task(
        taskScripts.memoryTask,
        datafile,
        datafileBackup,
        "Memory Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Memory_Task/Memory_prompts.csv",
        1,
    )
    zerobackTask = task(
        taskScripts.zerobackTask,
        datafile,
        datafileBackup,
        "Zero-Back Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources//ZeroBack_Task//ConditionsSpecifications_ES_zeroback.csv",
        1,
    )
    onebackTask = task(
        taskScripts.onebackTask,
        datafile,
        datafileBackup,
        "One-Back Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources//ZeroBack_Task//ConditionsSpecifications_ES_oneback.csv",
        1,
    )
    easymathTask1 = task(
        taskScripts.easymathTask,
        datafile,
        datafileBackup,
        "Easy Math Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Maths_Task/new_math_stimuli1.csv",
        1,
    )
    hardmathTask1 = task(
        taskScripts.hardmathTask,
        datafile,
        datafileBackup,
        "Hard Math Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Maths_Task/new_math_stimuli2.csv",
        1,
    )
    twobackTaskfaces1 = task(
        taskScripts.twobacktaskfaces,
        datafile,
        datafileBackup,
        "Two-Back Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        1,
    )
    twobackTaskscenes1 = task(
        taskScripts.twobacktaskscenes,
        datafile,
        datafileBackup,
        "Two-Back Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        1,
    )
    # Block 2
    friendTask2 = task(
        taskScripts.otherTask,
        datafile,
        datafileBackup,
        "Friend Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Other_Task/Other_Stimuli.csv",
        2,
    )
    youTask2 = task(
        taskScripts.selfTask,
        datafile,
        datafileBackup,
        "You Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Self_Task/Self_Stimuli.csv",
        2,
    )
    gonogoTask2 = task(
        taskScripts.gonogoTask,
        datafile,
        datafileBackup,
        "GoNoGo Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        2,
    )
    fingertapTask2 = task(
        taskScripts.fingertappingTask,
        datafile,
        datafileBackup,
        "Finger Tapping Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        2,
    )
    readingTask2 = task(
        taskScripts.readingTask,
        datafile,
        datafileBackup,
        "Reading Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Reading_Task/sem_stim_run.csv",
        2,
    )
    memTask2 = task(
        taskScripts.memoryTask,
        datafile,
        datafileBackup,
        "Memory Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Memory_Task/Memory_prompts.csv",
        2,
    )
    zerobackTask2 = task(
        taskScripts.zerobackTask,
        datafile,
        datafileBackup,
        "Zero-Back Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources//ZeroBack_Task//ConditionsSpecifications_ES_zeroback.csv",
        2,
    )
    onebackTask2 = task(
        taskScripts.onebackTask,
        datafile,
        datafileBackup,
        "One-Back Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources//ZeroBack_Task//ConditionsSpecifications_ES_oneback.csv",
        2,
    )
    easymathTask2 = task(
        taskScripts.easymathTask,
        datafile,
        datafileBackup,
        "Easy Math Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Maths_Task/new_math_stimuli1.csv",
        2,
    )
    hardmathTask2 = task(
        taskScripts.hardmathTask,
        datafile,
        datafileBackup,
        "Hard Math Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Maths_Task/new_math_stimuli2.csv",
        2,
    )
    twobackTaskfaces2 = task(
        taskScripts.twobacktaskfaces,
        datafile,
        datafileBackup,
        "Two-Back Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        2,
    )
    twobackTaskscenes2 = task(
        taskScripts.twobacktaskscenes,
        datafile,
        datafileBackup,
        "Two-Back Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        2,
    )
    # Block 3
    friendTask3 = task(
        taskScripts.otherTask,
        datafile,
        datafileBackup,
        "Friend Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Other_Task/Other_Stimuli.csv",
        3,
    )
    youTask3 = task(
        taskScripts.selfTask,
        datafile,
        datafileBackup,
        "You Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Self_Task/Self_Stimuli.csv",
        3,
    )
    gonogoTask3 = task(
        taskScripts.gonogoTask,
        datafile,
        datafileBackup,
        "GoNoGo Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        3,
    )
    fingertapTask3 = task(
        taskScripts.fingertappingTask,
        datafile,
        datafileBackup,
        "Finger Tapping Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/GoNoGo_Task/gonogo_stimuli.csv",
        3,
    )
    readingTask3 = task(
        taskScripts.readingTask,
        datafile,
        datafileBackup,
        "Reading Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Reading_Task/sem_stim_run.csv",
        3,
    )
    memTask3 = task(
        taskScripts.memoryTask,
        datafile,
        datafileBackup,
        "Memory Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Memory_Task/Memory_prompts.csv",
        3,
    )
    zerobackTask3 = task(
        taskScripts.zerobackTask,
        datafile,
        datafileBackup,
        "Zero-Back Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources//ZeroBack_Task//ConditionsSpecifications_ES_zeroback.csv",
        3,
    )
    onebackTask3 = task(
        taskScripts.onebackTask,
        datafile,
        datafileBackup,
        "One-Back Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources//ZeroBack_Task//ConditionsSpecifications_ES_oneback.csv",
        3,
    )
    easymathTask3 = task(
        taskScripts.easymathTask,
        datafile,
        datafileBackup,
        "Easy Math Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Maths_Task/new_math_stimuli1.csv",
        3,
    )
    hardmathTask3 = task(
        taskScripts.hardmathTask,
        datafile,
        datafileBackup,
        "Hard Math Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources/Maths_Task/new_math_stimuli2.csv",
        3,
    )
    # twobackTask3 = task(taskScripts.twobacktask, datafile, datafileBackup,"Two-Back Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources/GoNoGo_Task/gonogo_stimuli.csv', 3)
    movieTask1 = task(
        taskScripts.movieTask,
        datafile,
        1,
        "Movie Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources//Movie_Task//csv//sorted_filmList.csv",
        1,
    )
    movieTask2 = task(
        taskScripts.movieTask,
        datafile,
        2,
        "Movie Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources//Movie_Task//csv//sorted_filmList.csv",
        2,
    )
    movieTask3 = task(
        taskScripts.movieTask,
        datafile,
        3,
        "Movie Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources//Movie_Task//csv//sorted_filmList.csv",
        3,
    )
    movieTask4 = task(
        taskScripts.movieTask,
        datafile,
        4,
        "Movie Task",
        metacoll.sbINFO.data,
        int(metacoll.INFO["Block Runtime"]),
        "resources//Movie_Task//csv//sorted_filmList.csv",
        4,
    )
    # Defining task GROUPS (groups will always be shown together, preceded by an instruction screen)
    self_other = taskgroup(
        [[friendTask, friendTask2, friendTask3], [youTask, youTask2, youTask3]],
        "resources/group_inst/self_other.txt",
    )
    gonogo_fingtap = taskgroup(
        [
            [gonogoTask, gonogoTask2, gonogoTask3],
            [fingertapTask, fingertapTask2, fingertapTask3],
        ],
        "resources/group_inst/gonogo_fingtap.txt",
    )
    reading_memory = taskgroup(
        [[readingTask, readingTask2, readingTask3], [memTask, memTask2, memTask3]],
        "resources/group_inst/reading_memory.txt",
    )
    oneback_zeroback = taskgroup(
        [
            [zerobackTask, zerobackTask2, zerobackTask3],
            [onebackTask, onebackTask2, onebackTask3],
        ],
        "resources/group_inst/oneback_zeroback.txt",
    )
    ezmath_hrdmath = taskgroup(
        [
            [easymathTask1, easymathTask2, easymathTask3],
            [hardmathTask1, hardmathTask2, hardmathTask3],
        ],
        "resources/group_inst/ezmath_hrdmath.txt",
    )
    twobackTask_grp = taskgroup(
        [
            [twobackTaskfaces1, twobackTaskfaces2],
            [twobackTaskscenes1, twobackTaskscenes2],
        ],
        "resources/group_inst/ezmath_hrdmath.txt",
    )
    movie_main = taskgroup(
        [[movieTask1, movieTask2]], "resources/group_inst/movie_main.txt"
    )
    fulltasklist = [
        self_other,
        gonogo_fingtap,
        reading_memory,
        oneback_zeroback,
        ezmath_hrdmath,
        movie_main,
        twobackTask_grp,
    ]
    # Shuffles the order of the tasks in taskgroups
    for blk in fulltasklist:
        blk.shuffle()
    # Shuffle the order of the taskgroups
    random.shuffle(fulltasklist)
    tasks = fulltasklist
    tbt = taskbattery(tasks, ESQTask, INFO)
    tbt.run_battery()
    print("Success")
